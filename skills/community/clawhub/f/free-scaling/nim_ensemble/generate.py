"""Generation via ensemble — best-of-k with cross-evaluation.

Pattern:
  Round 1: k models generate independently (parallel)
  Round 2: k models vote on which output is best (scale())
  Return the winner.

Usage:
    from nim_ensemble import generate, generate_batch

    result = generate("Summarize this paper.", context=paper_text, k=3)
    print(result.output)       # best summary
    print(result.all_outputs)  # all k summaries
    print(result.winner_idx)   # which was picked
"""

from __future__ import annotations

import re
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from .models import MODELS
from .voter import call_model
from .health import _is_dead, _get_substitute, _mark_dead
from .parser import parse_answer


@dataclass
class GenerateResult:
    """Result of an ensemble generation."""
    output: str               # winning output text
    all_outputs: list[str]    # all k outputs
    models_used: list[str]    # which models generated
    winner_idx: int           # index of winning output
    winner_model: str         # which model won
    judge_votes: list[str]    # how judges voted (e.g. ["1", "1", "2"])
    judge_confidence: float   # agreement ratio
    gen_elapsed_s: float      # time for generation round
    judge_elapsed_s: float    # time for judging round
    total_elapsed_s: float    # total time
    total_calls: int          # total API calls (gen + judge)
    errors: list[str] = field(default_factory=list)


def _pick_diverse_models(k: int, exclude: list[str] = None) -> list[str]:
    """Pick k models maximizing family diversity, skipping dead ones."""
    exclude = set(exclude or [])
    families_seen = set()
    selected = []

    preference = [
        "mistral-large", "llama-3.3", "gemma-27b",
        "nemotron-super-49b", "kimi-k2", "llama-405b", "qwen-397b",
        "jamba-mini", "dracarys-70b", "mistral-medium",
    ]

    for alias in preference:
        if len(selected) >= k:
            break
        if alias in exclude or alias not in MODELS:
            continue
        if _is_dead(alias):
            sub = _get_substitute(alias)
            if sub and sub not in exclude and sub not in selected:
                alias = sub
            else:
                continue

        fam = MODELS[alias]["family"]
        if fam not in families_seen:
            selected.append(alias)
            families_seen.add(fam)
        elif len(selected) < k:
            selected.append(alias)

    return selected[:k]


def generate(
    question: str,
    context: str = None,
    k: int = 3,
    system_prompt: str = None,
    max_tokens: int = 500,
    judge_max_tokens: int = 100,
    models: list[str] = None,
    judge_models: list[str] = None,
) -> GenerateResult:
    """Generate with k models, pick the best output via cross-evaluation.

    Round 1: k models generate answers in parallel.
    Round 2: k (different) models vote on which output is best.

    Args:
        question: What to generate (e.g. "Summarize this paper.")
        context: Source material / input data
        k: Number of models for generation AND judging
        system_prompt: Optional system prompt (overrides context placement)
        max_tokens: Max tokens for generation (higher than scale's 150)
        judge_max_tokens: Max tokens for judging round
        models: Override generation model selection
        judge_models: Override judge model selection (defaults to different models)

    Returns:
        GenerateResult with winning output and metadata
    """
    t0 = time.time()

    # Build effective system prompt
    effective_system = system_prompt
    if context and not system_prompt:
        effective_system = f"Here is the material to work with:\n\n{context}"
    elif context and system_prompt:
        effective_system = f"{system_prompt}\n\nHere is the material to work with:\n\n{context}"

    # ── Round 1: Generate ──────────────────────────────────────────
    gen_models = list(models) if models else _pick_diverse_models(k)
    outputs = [None] * len(gen_models)
    gen_errors = []
    t1 = time.time()

    def _gen(idx, alias):
        effective_alias = alias
        if _is_dead(alias):
            sub = _get_substitute(alias)
            effective_alias = sub if sub else alias

        ans, raw = call_model(question, effective_alias, effective_system, max_tokens)

        if ans == "ERROR":
            if raw and any(code in raw for code in ["HTTP 404", "HTTP 410"]):
                _mark_dead(effective_alias)
            return idx, effective_alias, "", raw
        return idx, effective_alias, raw, ""

    with ThreadPoolExecutor(max_workers=len(gen_models)) as pool:
        futures = {pool.submit(_gen, i, m): i for i, m in enumerate(gen_models)}
        for fut in as_completed(futures):
            idx, model, output, error = fut.result()
            gen_models[idx] = model  # update with effective alias
            outputs[idx] = output
            if error:
                gen_errors.append(f"{model}: {error[:100]}")

    gen_elapsed = time.time() - t1

    # Filter out failed/empty outputs
    valid = [(i, out) for i, out in enumerate(outputs) if out and out.strip()]

    if not valid:
        return GenerateResult(
            output="",
            all_outputs=outputs,
            models_used=gen_models,
            winner_idx=-1,
            winner_model="",
            judge_votes=[],
            judge_confidence=0.0,
            gen_elapsed_s=gen_elapsed,
            judge_elapsed_s=0.0,
            total_elapsed_s=time.time() - t0,
            total_calls=len(gen_models),
            errors=gen_errors or ["All models failed to generate"],
        )

    if len(valid) == 1:
        # Only one output — no need to judge
        idx, output = valid[0]
        return GenerateResult(
            output=output,
            all_outputs=outputs,
            models_used=gen_models,
            winner_idx=idx,
            winner_model=gen_models[idx],
            judge_votes=[],
            judge_confidence=1.0,
            gen_elapsed_s=gen_elapsed,
            judge_elapsed_s=0.0,
            total_elapsed_s=time.time() - t0,
            total_calls=len(gen_models),
            errors=gen_errors,
        )

    # ── Round 2: Judge ─────────────────────────────────────────────
    # Build comparison prompt
    labeled_outputs = []
    idx_map = {}  # label number → original index
    for label_num, (orig_idx, output) in enumerate(valid, 1):
        # Truncate very long outputs for judging
        truncated = output[:2000] + ("..." if len(output) > 2000 else "")
        labeled_outputs.append(f"[Output {label_num}]:\n{truncated}")
        idx_map[label_num] = orig_idx

    comparison_text = "\n\n".join(labeled_outputs)
    answer_patterns = [str(i) for i in range(1, len(valid) + 1)]

    judge_question = (
        f"You are evaluating {len(valid)} responses to the same question.\n"
        f"Original question: \"{question}\"\n\n"
        f"Which output is the best? Consider accuracy, completeness, "
        f"and clarity. Answer with ONLY the number ({', '.join(answer_patterns)})."
    )

    # Pick different models for judging (avoid self-evaluation bias)
    jmodels = judge_models or _pick_diverse_models(k, exclude=gen_models)
    # If we can't get enough different models, allow overlap
    if len(jmodels) < k:
        jmodels = _pick_diverse_models(k)

    judge_votes = []
    t2 = time.time()

    def _judge(alias):
        effective_alias = alias
        if _is_dead(alias):
            sub = _get_substitute(alias)
            effective_alias = sub if sub else alias

        ans, raw = call_model(
            judge_question, effective_alias,
            f"Here are the outputs to evaluate:\n\n{comparison_text}",
            judge_max_tokens,
        )

        if ans == "ERROR":
            return effective_alias, "ERROR"

        # Parse: look for a number in the response
        parsed = parse_answer(raw, patterns=answer_patterns)
        if parsed == "UNCLEAR":
            # Try harder: find first digit in response
            nums = re.findall(r'\b([1-9])\b', raw)
            for n in nums:
                if n in answer_patterns:
                    return effective_alias, n
        return effective_alias, parsed

    with ThreadPoolExecutor(max_workers=len(jmodels)) as pool:
        futures = {pool.submit(_judge, m): m for m in jmodels}
        for fut in as_completed(futures):
            model, vote = fut.result()
            if vote != "ERROR":
                judge_votes.append(vote)

    judge_elapsed = time.time() - t2

    # Tally votes
    if not judge_votes:
        # No valid judge votes — return first valid output
        idx, output = valid[0]
        return GenerateResult(
            output=output,
            all_outputs=outputs,
            models_used=gen_models,
            winner_idx=idx,
            winner_model=gen_models[idx],
            judge_votes=[],
            judge_confidence=0.0,
            gen_elapsed_s=gen_elapsed,
            judge_elapsed_s=judge_elapsed,
            total_elapsed_s=time.time() - t0,
            total_calls=len(gen_models) + len(jmodels),
            errors=gen_errors + ["All judges failed"],
        )

    from collections import Counter
    counts = Counter(v for v in judge_votes if v in answer_patterns)

    if not counts:
        winner_label = 1
        confidence = 0.0
    else:
        winner_label_str, winner_count = counts.most_common(1)[0]
        winner_label = int(winner_label_str)
        confidence = winner_count / len(judge_votes)

    winner_orig_idx = idx_map.get(winner_label, valid[0][0])

    return GenerateResult(
        output=outputs[winner_orig_idx] or "",
        all_outputs=outputs,
        models_used=gen_models,
        winner_idx=winner_orig_idx,
        winner_model=gen_models[winner_orig_idx],
        judge_votes=judge_votes,
        judge_confidence=confidence,
        gen_elapsed_s=gen_elapsed,
        judge_elapsed_s=judge_elapsed,
        total_elapsed_s=time.time() - t0,
        total_calls=len(gen_models) + len(jmodels),
        errors=gen_errors,
    )


def generate_batch(
    items: list[dict],
    k: int = 3,
    max_parallel: int = 3,
) -> list[GenerateResult]:
    """Batch multiple generation tasks.

    Each item: {"question": "...", "context": "...", "max_tokens": 500}

    Returns list of GenerateResults in same order.
    """
    results = [None] * len(items)

    def _run(idx, item):
        return idx, generate(
            question=item.get("question", item.get("text", "")),
            context=item.get("context"),
            k=k,
            system_prompt=item.get("system_prompt"),
            max_tokens=item.get("max_tokens", 500),
            models=item.get("models"),
            judge_models=item.get("judge_models"),
        )

    # Lower parallelism for generate (each task does 2k calls)
    with ThreadPoolExecutor(max_workers=max_parallel) as pool:
        futures = {pool.submit(_run, i, item): i for i, item in enumerate(items)}
        for fut in as_completed(futures):
            try:
                idx, result = fut.result()
                results[idx] = result
            except Exception as e:
                idx = futures[fut]
                results[idx] = GenerateResult(
                    output="", all_outputs=[], models_used=[],
                    winner_idx=-1, winner_model="", judge_votes=[],
                    judge_confidence=0.0, gen_elapsed_s=0.0,
                    judge_elapsed_s=0.0, total_elapsed_s=0.0,
                    total_calls=0, errors=[f"Batch item error: {e}"],
                )

    return results
