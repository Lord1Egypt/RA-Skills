"""Smart cascade — capability-aware routing with confidence gating.

Instead of "ask 3 models, vote", this does:
  1. Classify task type from the question
  2. Pick the best model for that type (from capability map)
  3. If confident → done (1 API call)
  4. If uncertain → escalate to arbiter
  5. If arbiter uncertain → full panel vote
  6. Weight votes by measured accuracy

Average: ~1.2 calls per question instead of 3.
"""

from __future__ import annotations

import json
import os
import time
from dataclasses import dataclass, field
from pathlib import Path

from .models import MODELS, PANELS, get_panel
from .voter import call_model, vote, VoteResult
from .parser import parse_answer


# Load capability map if available
_CAPABILITY_MAP = None

def _load_capability_map() -> dict:
    global _CAPABILITY_MAP
    if _CAPABILITY_MAP is not None:
        return _CAPABILITY_MAP
    
    # Try multiple locations
    candidates = [
        Path(__file__).parent.parent / "capability_map.json",
        Path(os.environ.get("OPENCLAW_WORKSPACE", "")) / "skills" / "nim-ensemble" / "capability_map.json",
    ]
    for p in candidates:
        if p.exists():
            with open(p) as f:
                _CAPABILITY_MAP = json.load(f)
            return _CAPABILITY_MAP
    
    _CAPABILITY_MAP = {}
    return _CAPABILITY_MAP


# Task type classification keywords
TASK_KEYWORDS = {
    "code": [
        "code", "function", "bug", "vulnerability", "sql", "injection", 
        "safe", "unsafe", "secure", "insecure", "python", "javascript",
        "cursor.execute", "eval(", "exec(", "import os", "subprocess",
        "def ", "class ", "return ", "```",
    ],
    "compliance": [
        "compliant", "violated", "following the rule", "follow the rule",
        "preamble", "personality", "soul", "character", "behavior", "tone",
        "helpdesk", "filler", "direct", "rule", "policy", "guideline",
    ],
    "reasoning": [
        "taller than", "greater than", "then", "therefore",
        "majority", "consistent", "inconsistent", "implies",
        "logically", "deduce", "infer",
    ],
    "factual": [
        "prime", "multiply", "calculate", "what is", "is it true",
        "how many", "which year", "capital of",
    ],
    "nuance": [
        "urgent", "routine", "fyi", "priority", "severity",
        "subtle", "gray area", "borderline", "edge case",
        "drifting", "minor", "major",
    ],
}

# Default panels — good starting points, override via capability_map.json
# ELO-seeded panels: NIM wins on classification (kimi-k2=85%, jamba=75%)
# Copilot (60%) reserved for deep/long-context analysis only
_DEFAULT_BEST_FOR_TASK = {
    "code":       ["kimi-k2", "jamba-mini", "dracarys-70b"],
    "compliance": ["kimi-k2", "jamba-mini", "dracarys-70b"],
    "reasoning":  ["kimi-k2", "jamba-mini", "gemma-27b"],
    "factual":    ["kimi-k2", "jamba-mini", "dracarys-70b"],
    "nuance":     ["kimi-k2", "jamba-mini", "dracarys-70b"],
    "general":    ["kimi-k2", "jamba-mini", "dracarys-70b"],
}

# Default weights (equal) — override via capability_map.json profiling
_DEFAULT_MODEL_WEIGHT = 0.75


def _get_routing():
    """Load routing from capability_map.json if available, else use defaults."""
    cap = _load_capability_map()
    
    if not cap or "routing_policy" not in cap:
        return _DEFAULT_BEST_FOR_TASK, {}
    
    policy = cap["routing_policy"]
    
    # Build BEST_FOR_TASK from routing_policy panels (try both key names)
    best_for = {}
    panels = policy.get("panels", policy.get("recommended_panels", {}))
    for task_type, models in panels.items():
        best_for[task_type] = models
    # Merge defaults for any missing task types
    for k, v in _DEFAULT_BEST_FOR_TASK.items():
        if k not in best_for:
            best_for[k] = v
    
    # Build MODEL_WEIGHTS from profiles — extract accuracy floats from nested dicts
    weights = {}
    for alias, profile in cap.get("profiles", {}).items():
        cats = profile.get("category_scores", {})
        w = {}
        for cat, info in cats.items():
            # Handle both formats: {"accuracy": 0.9, ...} or plain float 0.9
            if isinstance(info, dict):
                w[cat] = info.get("accuracy", _DEFAULT_MODEL_WEIGHT)
            else:
                w[cat] = float(info)
        # Add overall as "general"
        if "general" not in w:
            w["general"] = profile.get("accuracy", _DEFAULT_MODEL_WEIGHT)
        weights[alias] = w
    
    return best_for, weights

ARBITER = "kimi-k2"  # 85% accuracy on ground-truth benchmark (ELO-seeded 2026-03-14)


@dataclass
class CascadeResult:
    """Result of a smart cascade."""
    answer: str
    confidence: float        # 0-1 weighted confidence
    task_type: str           # detected task type
    stage: str               # "primary", "arbiter", "panel"
    calls_made: int          # total API calls
    models_used: list[str]
    votes: list[tuple[str, str, float]]  # (model, answer, weight)
    elapsed_s: float = 0.0
    reasoning: str = ""      # why this answer


def classify_task(question: str) -> str:
    """Classify a question into a task type using keyword matching."""
    question_lower = question.lower()
    
    scores = {}
    for task_type, keywords in TASK_KEYWORDS.items():
        score = sum(1 for kw in keywords if kw.lower() in question_lower)
        if score > 0:
            scores[task_type] = score
    
    if not scores:
        return "general"
    
    return max(scores, key=scores.get)


def smart_vote(
    question: str,
    task_type: str = None,
    answer_patterns: list[str] = None,
    system_prompt: str = None,
    max_tokens: int = 150,
    confidence_threshold: float = 0.85,
    skip_cascade: bool = False,
) -> CascadeResult:
    """Capability-aware cascade with confidence gating.
    
    Stage 1: Best model for task type (1 call)
      → if answer is clear and model weight ≥ threshold → done
    Stage 2: Arbiter verification (1 more call)
      → if arbiter agrees → done
      → if arbiter disagrees → weighted vote between them
    Stage 3: Full panel (3 more calls, 5 total)
      → weighted majority vote
    
    Args:
        question: The question to answer
        task_type: Override auto-classification (code/compliance/reasoning/factual/nuance/general)
        answer_patterns: Expected answer tokens
        system_prompt: Optional system prompt
        max_tokens: Max tokens per call
        confidence_threshold: Min weighted confidence to accept at stage 1
        skip_cascade: If True, go straight to full panel vote (fallback mode)
    """
    t0 = time.time()
    
    # Classify task
    # Normalize answer patterns to uppercase
    if answer_patterns:
        answer_patterns = [p.strip().upper() for p in answer_patterns]
    if task_type is None:
        task_type = classify_task(question)
    
    # Load routing (from capability_map.json if available, else defaults)
    best_for_task, model_weights = _get_routing()
    
    if skip_cascade:
        # Fallback: just do weighted panel vote
        return _weighted_panel_vote(question, task_type, answer_patterns, 
                                    system_prompt, max_tokens, t0,
                                    best_for_task, model_weights)
    
    # Get best model for this task type
    best_models = best_for_task.get(task_type, best_for_task["general"])
    primary = best_models[0]
    
    # Stage 1: Primary expert
    ans1, raw1 = call_model(question, primary, system_prompt, max_tokens)
    
    # Re-parse with custom patterns
    if answer_patterns and ans1 != "ERROR":
        ans1 = parse_answer(raw1, patterns=answer_patterns)
    
    # Arbiter gets full weight by default; others get default weight
    default_w = 1.0 if primary == ARBITER else _DEFAULT_MODEL_WEIGHT
    weight1 = model_weights.get(primary, {}).get(task_type, default_w)
    calls = 1
    
    if ans1 == "ERROR":
        # Primary failed, go to arbiter
        pass
    elif ans1 == "UNCLEAR":
        # Primary uncertain, escalate
        pass
    elif weight1 >= confidence_threshold:
        # Primary confident and reliable → done
        return CascadeResult(
            answer=ans1,
            confidence=weight1,
            task_type=task_type,
            stage="primary",
            calls_made=1,
            models_used=[primary],
            votes=[(primary, ans1, weight1)],
            elapsed_s=time.time() - t0,
            reasoning=f"{primary} answered {ans1} (weight {weight1:.0%} on {task_type}). High confidence, no escalation needed.",
        )
    
    # Stage 2: Arbiter
    if primary == ARBITER:
        # Primary IS the arbiter — skip stage 2 entirely, go to panel
        arbiter_ans = ans1
        arbiter_weight = weight1
    else:
        arbiter_ans, arbiter_raw = call_model(question, ARBITER, system_prompt, max_tokens)
        calls += 1
        
        if answer_patterns and arbiter_ans != "ERROR":
            arbiter_ans = parse_answer(arbiter_raw, patterns=answer_patterns)
        
        arbiter_weight = model_weights.get(ARBITER, {}).get(task_type, 1.0)  # Arbiter gets full weight by default
    
        # If primary answered and arbiter agrees → done
        if ans1 not in ("ERROR", "UNCLEAR") and arbiter_ans == ans1:
            combined_conf = (weight1 + arbiter_weight) / 2
            return CascadeResult(
                answer=ans1,
                confidence=combined_conf,
                task_type=task_type,
                stage="arbiter",
                calls_made=calls,
                models_used=[primary, ARBITER],
                votes=[(primary, ans1, weight1), (ARBITER, arbiter_ans, arbiter_weight)],
                elapsed_s=time.time() - t0,
                reasoning=f"{primary} and {ARBITER} agree on {ans1}. Combined confidence {combined_conf:.0%}.",
            )
        
        # If arbiter is confident and primary wasn't → trust arbiter
        if arbiter_ans not in ("ERROR", "UNCLEAR") and arbiter_weight >= confidence_threshold:
            if ans1 in ("ERROR", "UNCLEAR"):
                return CascadeResult(
                    answer=arbiter_ans,
                    confidence=arbiter_weight,
                    task_type=task_type,
                    stage="arbiter",
                    calls_made=calls,
                    models_used=[primary, ARBITER],
                    votes=[(primary, ans1, weight1), (ARBITER, arbiter_ans, arbiter_weight)],
                    elapsed_s=time.time() - t0,
                    reasoning=f"{primary} was {ans1}. {ARBITER} answered {arbiter_ans} (weight {arbiter_weight:.0%}). Trusting arbiter.",
                )
    
    # Stage 3: Disagreement or low confidence → full panel weighted vote
    # Get remaining models from the task panel (excluding already-called)
    panel_models = best_for_task.get(task_type, best_for_task.get("general", _DEFAULT_BEST_FOR_TASK["general"]))
    already_called = {primary, ARBITER} if primary != ARBITER else {primary}
    remaining = [m for m in panel_models if m not in already_called]
    
    # Add more models if panel is too small
    if len(remaining) < 2:
        backup = [m for m in ["llama-3.3", "gemma-27b", "nemotron-super-49b", "kimi-k2"] 
                  if m not in already_called and m not in remaining]
        remaining.extend(backup[:3 - len(remaining)])
    
    # Start with primary vote (no duplicates)
    all_votes = []
    if ans1 not in ("ERROR",):
        all_votes.append((primary, ans1, weight1))
    # Add arbiter only if it's a different model
    if primary != ARBITER and arbiter_ans not in ("ERROR",):
        all_votes.append((ARBITER, arbiter_ans, arbiter_weight))
    
    for model in remaining:
        ans, raw = call_model(question, model, system_prompt, max_tokens)
        calls += 1
        if answer_patterns and ans != "ERROR":
            ans = parse_answer(raw, patterns=answer_patterns)
        w = model_weights.get(model, {}).get(task_type, _DEFAULT_MODEL_WEIGHT)
        if ans != "ERROR":
            all_votes.append((model, ans, w))
    
    # Weighted majority vote
    answer, confidence = _weighted_majority(all_votes)
    all_models = [primary] + ([ARBITER] if primary != ARBITER else []) + remaining
    
    return CascadeResult(
        answer=answer,
        confidence=confidence,
        task_type=task_type,
        stage="panel",
        calls_made=calls,
        models_used=all_models,
        votes=all_votes,
        elapsed_s=time.time() - t0,
        reasoning=f"Full panel vote: {len(all_votes)} votes across {calls} calls. Weighted majority: {answer} ({confidence:.0%}).",
    )


def _weighted_majority(votes: list[tuple[str, str, float]]) -> tuple[str, float]:
    """Compute weighted majority from (model, answer, weight) tuples."""
    if not votes:
        return "UNCLEAR", 0.0
    
    # Accumulate weights per answer
    answer_weights = {}
    total_weight = 0
    for model, ans, weight in votes:
        if ans not in ("ERROR", "UNCLEAR"):
            answer_weights[ans] = answer_weights.get(ans, 0) + weight
            total_weight += weight
    
    if not answer_weights:
        return "UNCLEAR", 0.0
    
    best_answer = max(answer_weights, key=answer_weights.get)
    confidence = answer_weights[best_answer] / total_weight if total_weight > 0 else 0
    
    return best_answer, round(confidence, 3)


def _weighted_panel_vote(question, task_type, answer_patterns, system_prompt,
                         max_tokens, t0, best_for_task=None, model_weights=None) -> CascadeResult:
    """Direct weighted panel vote (skip cascade)."""
    if best_for_task is None or model_weights is None:
        bft, mw = _get_routing()
        if best_for_task is None:
            best_for_task = bft
        if model_weights is None:
            model_weights = mw
    panel_models = best_for_task.get(task_type, best_for_task.get("general", ["kimi-k2", "jamba-mini", "dracarys-70b"]))

    from concurrent.futures import ThreadPoolExecutor, as_completed

    all_votes = []

    def _call(model):
        ans, raw = call_model(question, model, system_prompt, max_tokens)
        if answer_patterns and ans != "ERROR":
            ans = parse_answer(raw, patterns=answer_patterns)
        w = model_weights.get(model, {}).get(task_type, _DEFAULT_MODEL_WEIGHT)
        return model, ans, w

    with ThreadPoolExecutor(max_workers=len(panel_models)) as pool:
        futures = {pool.submit(_call, m): m for m in panel_models}
        for fut in as_completed(futures):
            model, ans, w = fut.result()
            if ans != "ERROR":
                all_votes.append((model, ans, w))

    answer, confidence = _weighted_majority(all_votes)

    return CascadeResult(
        answer=answer,
        confidence=confidence,
        task_type=task_type,
        stage="panel",
        calls_made=len(panel_models),
        models_used=panel_models,
        votes=all_votes,
        elapsed_s=time.time() - t0,
        reasoning=f"Direct panel vote ({task_type}): {answer} ({confidence:.0%}).",
    )


def smart_vote_batch(
    questions: list[dict],
    max_parallel: int = 5,
    **kwargs,
) -> list[CascadeResult]:
    """Smart vote on multiple questions.
    
    Each question dict: {"text": "...", "task_type": "code", "answer_patterns": [...]}
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    results = [None] * len(questions)
    
    def _vote_one(idx, q):
        text = q.get("text", q.get("question_text", ""))
        kw = {**kwargs}
        if "task_type" in q:
            kw["task_type"] = q["task_type"]
        if "answer_patterns" in q:
            kw["answer_patterns"] = q["answer_patterns"]
        return idx, smart_vote(text, **kw)
    
    with ThreadPoolExecutor(max_workers=max_parallel) as pool:
        futures = {pool.submit(_vote_one, i, q): i for i, q in enumerate(questions)}
        for fut in as_completed(futures):
            idx, result = fut.result()
            results[idx] = result
    
    return results


def scale_batch(
    items: list[dict],
    k: int | str = 3,
    max_parallel: int = 5,
) -> list[CascadeResult]:
    """Batch multiple questions through scale().
    
    Each item dict:
        {"question": "...", "context": "...", "answer_patterns": ["YES", "NO"]}
    
    All fields except 'question' are optional.
    
    Returns list of CascadeResults in same order as input.
    """
    from concurrent.futures import ThreadPoolExecutor, as_completed
    
    results = [None] * len(items)
    
    def _run_one(idx, item):
        question = item.get("question", item.get("text", item.get("question_text", "")))
        return idx, scale(
            question=question,
            k=k,
            context=item.get("context"),
            answer_patterns=item.get("answer_patterns"),
            system_prompt=item.get("system_prompt"),
            max_tokens=item.get("max_tokens", 150),
            models=item.get("models"),
            tag=item.get("tag"),
            message_id=item.get("message_id"),
        )
    
    with ThreadPoolExecutor(max_workers=max_parallel) as pool:
        futures = {pool.submit(_run_one, i, item): i for i, item in enumerate(items)}
        for fut in as_completed(futures):
            try:
                idx, result = fut.result()
                results[idx] = result
            except Exception as e:
                # Find the index for this future and record the error
                idx = futures[fut]
                results[idx] = CascadeResult(
                    answer="ERROR", confidence=0.0, task_type="general",
                    stage="error", calls_made=0, models_used=[],
                    votes=[], reasoning=f"Batch item error: {e}",
                )
    
    return results


def scale(
    question: str,
    k: int | str = "auto",
    context: str = None,
    answer_patterns: list[str] = None,
    system_prompt: str = None,
    max_tokens: int = 150,
    models: list[str] = None,
    tag: str = None,
    message_id: str = None,
) -> CascadeResult:
    """Scale inference by asking k models the same question.
    
    The core API — control the cost/accuracy tradeoff with a single parameter.
    
    Args:
        question: The question to ask (should end with "Answer X or Y")
        k: Number of models to query:
           - "auto": smart cascade (start with 1, escalate on uncertainty)
           - 1: single best model (fastest, cheapest)
           - 3: ensemble of 3 diverse models (balanced)
           - 5: maximum confidence panel
           - Any int: picks that many models from diverse families
        context: Material to judge against (code, email, transcript, etc.)
                 Placed in system message so question stays clean.
        answer_patterns: Expected answer tokens (e.g. ["YES", "NO"])
        system_prompt: Optional system prompt (overrides context placement)
        max_tokens: Max tokens per call
        models: Override model selection (list of aliases)
    
    Returns:
        CascadeResult with answer, confidence, calls_made
    """
    # Build effective system prompt: context goes in system message
    effective_system = system_prompt
    if context and not system_prompt:
        effective_system = f"Here is the material to evaluate:\n\n{context}"
    elif context and system_prompt:
        effective_system = f"{system_prompt}\n\nHere is the material to evaluate:\n\n{context}"
    
    # Normalize answer patterns once at entry
    if answer_patterns:
        answer_patterns = [p.strip().upper() for p in answer_patterns]

    if k == "auto":
        return smart_vote(question, answer_patterns=answer_patterns,
                         system_prompt=effective_system, max_tokens=max_tokens)
    
    k = int(k)
    if k < 1:
        raise ValueError("k must be >= 1 or 'auto'")
    
    t0 = time.time()

    # k=1: single best model — use task-type routing
    if k == 1:
        if models:
            model = models[0]
            task_type = "general"
        else:
            task_type = classify_task(question)
            best_for_task, _ = _get_routing()
            model = best_for_task.get(task_type, best_for_task["general"])[0]
        try:
            ans, raw = call_model(question, model, effective_system, max_tokens)
        except Exception:
            # Copilot down, network error — try NIM fallback
            from .health import _mark_dead, _get_substitute
            _mark_dead(model)
            sub = _get_substitute(model)
            if sub:
                try:
                    ans, raw = call_model(question, sub, effective_system, max_tokens)
                    model = sub
                except Exception:
                    ans, raw = "ERROR", "Primary and substitute both failed"
            else:
                ans, raw = "ERROR", "Primary failed, no substitute"
        if answer_patterns and ans != "ERROR":
            ans = parse_answer(raw, patterns=answer_patterns)

        return CascadeResult(
            answer=ans,
            confidence=1.0 if ans != "ERROR" else 0.0,
            task_type=task_type,
            stage="primary",
            calls_made=1,
            models_used=[model],
            votes=[(model, ans, 1.0)],
            elapsed_s=time.time() - t0,
            reasoning=f"Single model ({model}): {ans}",
        )

    # k >= 2: pick diverse models
    if models:
        selected = models[:k]
        effective_k = len(selected)
    else:
        families_seen = set()
        diverse_order = []
        # NIM first (better on classification), Copilot for diversity
        for alias in ["kimi-k2", "jamba-mini", "dracarys-70b",
                      "gemma-27b", "llama-3.3", "cp-4.1",
                      "mistral-medium", "cp-flash", "cp-mini"]:
            if alias in MODELS:
                fam = MODELS[alias]["family"]
                if fam not in families_seen:
                    diverse_order.append(alias)
                    families_seen.add(fam)
                else:
                    diverse_order.append(alias)

        effective_k = min(k, len(diverse_order))
        selected = diverse_order[:effective_k]
    
    # Parallel ensemble vote
    all_votes = []
    calls = 0
    
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from .health import _mark_dead, _is_dead, _get_substitute
    
    def _call(alias):
        # Skip known-dead models, swap in substitute
        effective_alias = alias
        if _is_dead(alias):
            sub = _get_substitute(alias)
            if sub:
                effective_alias = sub
            else:
                return alias, "ERROR", "Model dead, no substitute"
        
        try:
            ans, raw = call_model(question, effective_alias, effective_system, max_tokens)
        except Exception as e:
            # Copilot token expired, network error, etc. — try NIM substitute
            _mark_dead(effective_alias)
            sub = _get_substitute(effective_alias)
            if sub:
                try:
                    ans, raw = call_model(question, sub, effective_system, max_tokens)
                    if answer_patterns and ans != "ERROR":
                        ans = parse_answer(raw, patterns=answer_patterns)
                    return sub, ans, raw
                except Exception:
                    pass
            return alias, "ERROR", str(e)
        
        # Detect dead models (404/410) and mark for future calls
        if ans == "ERROR" and raw and any(code in raw for code in ["HTTP 404", "HTTP 410"]):
            _mark_dead(effective_alias)
            sub = _get_substitute(effective_alias)
            if sub:
                try:
                    ans, raw = call_model(question, sub, effective_system, max_tokens)
                except Exception:
                    return alias, "ERROR", "Substitute also failed"
                if answer_patterns and ans != "ERROR":
                    ans = parse_answer(raw, patterns=answer_patterns)
                return sub, ans, raw
        
        if answer_patterns and ans != "ERROR":
            ans = parse_answer(raw, patterns=answer_patterns)
        return effective_alias, ans, raw
    
    with ThreadPoolExecutor(max_workers=effective_k) as pool:
        futures = {pool.submit(_call, alias): alias for alias in selected}
        for fut in as_completed(futures):
            alias, ans, raw = fut.result()
            calls += 1
            if ans != "ERROR":
                all_votes.append((alias, ans, 1.0))
    
    answer, confidence = _weighted_majority(all_votes)
    
    # --- Online learning: shadow challenger + ELO update + feedback log ---
    try:
        from . import elo as _elo
        from .feedback import log_result as _log_fb
        
        # 1. Log panel votes to ELO
        _elo.update_from_votes(all_votes, answer)
        
        # 2. Shadow challenger: run 1 extra model not in panel (if available)
        panel_aliases = {v[0] for v in all_votes}
        challenger = _elo.get_challenger(exclude=list(panel_aliases))
        if not challenger:
            challenger = _elo.get_explore_model(exclude=list(panel_aliases))
        
        if challenger:
            try:
                c_ans, c_raw = call_model(question, challenger, effective_system, max_tokens)
                if answer_patterns and c_ans != "ERROR":
                    c_ans = parse_answer(c_raw, patterns=answer_patterns)
                if c_ans != "ERROR":
                    # Score challenger against panel consensus
                    challenger_votes = [(challenger, c_ans, 1.0)]
                    _elo.update_from_votes(challenger_votes, answer)
                    calls += 1
            except Exception:
                pass  # Shadow failure never affects main result
        
        # 3. Log result for user feedback resolution
        _log_fb(question=question, answer=answer, votes=all_votes,
                tag=tag, message_id=message_id)
    except Exception:
        pass  # ELO/feedback tracking is best-effort
    
    return CascadeResult(
        answer=answer,
        confidence=confidence,
        task_type="general",
        stage=f"scale-{effective_k}",
        calls_made=calls,
        models_used=[v[0] for v in all_votes],
        votes=all_votes,
        elapsed_s=time.time() - t0,
        reasoning=f"Scaled to {effective_k} models{f' (capped from k={k})' if effective_k < k else ''}: {answer} ({confidence:.0%} agreement).",
    )
