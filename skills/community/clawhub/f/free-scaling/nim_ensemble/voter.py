"""Core voting engine — parallel NIM API calls with majority vote."""

from __future__ import annotations

import json
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field

from .models import MODELS, PANELS, NIM_ENDPOINT, get_model, get_panel, is_thinking
from .parser import extract_content, parse_answer


@dataclass
class VoteResult:
    """Result of an ensemble vote."""
    answer: str
    confidence: str          # "3/3", "2/3", etc.
    votes: list[str]         # individual model answers
    raw_responses: list[str] # full model outputs
    models_used: list[str]
    unanimous: bool = False
    elapsed_s: float = 0.0
    errors: list[str] = field(default_factory=list)


def _get_nim_key() -> str:
    """Load NIM API key from environment."""
    key = os.environ.get("NVIDIA_API_KEY", "")
    if not key:
        raise RuntimeError(
            "NVIDIA_API_KEY not set. Get a free key at https://build.nvidia.com"
        )
    return key


# Copilot API support
COPILOT_ENDPOINT = "https://api.individual.githubcopilot.com/chat/completions"
COPILOT_MODELS = {
    "cp-4.1": "gpt-4.1",
    "cp-mini": "gpt-5-mini",
    "cp-4o": "gpt-4o",
    "cp-flash": "gemini-3-flash-preview",
    "cp-haiku": "claude-haiku-4.5",
    "cp-sonnet": "claude-sonnet-4.5",
}


def _refresh_copilot_token() -> bool:
    """Refresh the Copilot session token using GitHub OAuth token.
    
    Uses the stored GitHub user token (ghu_*) to request a fresh
    Copilot session token from api.github.com/copilot_internal/v2/token.
    """
    import urllib.request
    import urllib.error
    import glob
    
    token_path = os.path.expanduser("~/.openclaw/credentials/github-copilot.token.json")
    
    # Find GitHub OAuth token from auth-profiles
    oauth_token = None
    for profile_path in glob.glob(os.path.expanduser("~/.openclaw/agents/*/agent/auth-profiles.json")):
        try:
            with open(profile_path) as f:
                data = json.load(f)
            # Profiles may be nested under "profiles" key
            profiles = data.get("profiles", data)
            for profile_name, profile_data in profiles.items():
                if isinstance(profile_data, dict):
                    tok = profile_data.get("token", "")
                    if isinstance(tok, str) and tok.startswith("ghu_"):
                        oauth_token = tok
                        break
            if oauth_token:
                break
        except Exception:
            continue
    
    if not oauth_token:
        return False
    
    try:
        req = urllib.request.Request(
            "https://api.github.com/copilot_internal/v2/token",
            headers={
                "Authorization": f"token {oauth_token}",
                "Editor-Version": "vscode/1.96.0",
                "Editor-Plugin-Version": "copilot/1.250.0",
                "User-Agent": "GithubCopilot/1.250.0",
            },
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        
        if "token" not in data:
            return False
        
        # Save refreshed token
        with open(token_path, "w") as f:
            json.dump({
                "token": data["token"],
                "expiresAt": int(data.get("expires_at", 0)),
                "updatedAt": int(time.time() * 1000),
            }, f, indent=2)
        
        return True
    except Exception:
        return False


def _get_copilot_token() -> str:
    """Load Copilot session token from cached file, auto-refreshing if expired."""
    token_path = os.path.expanduser("~/.openclaw/credentials/github-copilot.token.json")
    if not os.path.exists(token_path):
        raise RuntimeError(f"Copilot token not found at {token_path}")
    
    with open(token_path) as f:
        data = json.load(f)
    
    token = data.get("token", "")
    expires_raw = data.get("expiresAt", 0)
    # Handle both seconds and milliseconds format
    expires = expires_raw / 1000 if expires_raw > 1e12 else expires_raw
    
    # Proactive refresh: if <5min remaining, refresh before it expires
    if time.time() > expires - 300:
        if _refresh_copilot_token():
            with open(token_path) as f:
                data = json.load(f)
            token = data.get("token", "")
            expires_raw = data.get("expiresAt", 0)
            expires = expires_raw / 1000 if expires_raw > 1e12 else expires_raw
            if time.time() > expires:
                raise RuntimeError("Copilot token expired — auto-refresh failed")
        elif time.time() > expires:
            raise RuntimeError("Copilot token expired — no OAuth token found")
        # else: refresh failed but token still valid, continue
    
    return token


def call_copilot(
    prompt: str,
    model_alias: str = "cp-4.1",
    system_prompt: str = None,
    max_tokens: int = 300,
    temperature: float = 0.1,
) -> tuple[str, str]:
    """Call a Copilot model directly. Auto-refreshes token via GitHub OAuth."""
    api_model = COPILOT_MODELS.get(model_alias, model_alias)
    try:
        from .models import MODELS
        if model_alias in MODELS and MODELS[model_alias].get("backend") == "copilot":
            api_model = MODELS[model_alias]["id"]
    except (ImportError, KeyError):
        pass
    
    token = _get_copilot_token()
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    payload = {
        "model": api_model,
        "messages": messages,
        "max_tokens": max_tokens,
        "temperature": temperature,
    }
    
    try:
        import urllib.request
        import urllib.error
        
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            COPILOT_ENDPOINT,
            data=req_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
                "Editor-Version": "vscode/1.96.0",
                "Copilot-Integration-Id": "vscode-chat",
            },
        )
        
        with urllib.request.urlopen(req, timeout=45) as resp:
            raw = resp.read().decode("utf-8")
        
        if not raw or not raw.startswith("{"):
            return "ERROR", f"Bad response: {(raw or '')[:100]}"
        
        data = json.loads(raw)
        msg = data.get("choices", [{}])[0].get("message", {})
        content = msg.get("content", "")
        
        return parse_answer(content), content
    
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        return "ERROR", f"HTTP {e.code}: {body[:200]}"
    except Exception as e:
        return "ERROR", str(e)


def call_model(
    prompt: str,
    model_alias: str,
    system_prompt: str = None,
    max_tokens: int = 150,
    temperature: float = 0.1,
) -> tuple[str, str]:
    """Call a single model. Routes Copilot aliases (cp-*) automatically."""
    # Route Copilot models to call_copilot()
    if model_alias in COPILOT_MODELS:
        return call_copilot(prompt, model_alias, system_prompt, max_tokens, temperature)
    # Also route models with backend=copilot from registry
    try:
        model_check = get_model(model_alias)
        if model_check.get("backend") == "copilot":
            return call_copilot(prompt, model_alias, system_prompt, max_tokens, temperature)
    except KeyError:
        pass
    model_info = get_model(model_alias)
    api_model = model_info["id"]
    key = _get_nim_key()
    
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})
    
    # Thinking models need more tokens and time
    effective_max_tokens = max_tokens
    curl_timeout = 30
    if model_info.get("thinking"):
        effective_max_tokens = max(max_tokens * 4, 600)
        curl_timeout = 45
    
    payload = {
        "model": api_model,
        "messages": messages,
        "max_tokens": effective_max_tokens,
        "temperature": temperature,
    }
    
    try:
        # Use urllib instead of curl to avoid leaking API key in process args
        import urllib.request
        import urllib.error
        
        req_data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            NIM_ENDPOINT,
            data=req_data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {key}",
            },
        )
        
        try:
            with urllib.request.urlopen(req, timeout=curl_timeout) as resp:
                raw = resp.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", errors="replace")
            return "ERROR", f"HTTP {e.code}: {body[:200]}"
        except urllib.error.URLError as e:
            return "ERROR", f"URL error: {e.reason}"
        
        if not raw:
            return "ERROR", "Empty response"
        
        if not raw.startswith("{"):
            return "ERROR", f"Non-JSON: {raw[:100]}"
        
        resp = json.loads(raw)
        
        if "error" in resp or resp.get("status") in (404, 410):
            err = resp.get("error", {})
            detail = resp.get("detail", "")
            msg = err.get("message", str(err)) if isinstance(err, dict) else str(err)
            return "ERROR", f"API error: {msg or detail}"
        
        msg = resp.get("choices", [{}])[0].get("message", {})
        content = extract_content(msg)
        
        return parse_answer(content), content
    
    except TimeoutError:
        return "ERROR", f"Timeout after {curl_timeout}s"
    except Exception as e:
        return "ERROR", str(e)


def vote(
    question: str,
    panel: str | list[str] = "general",
    system_prompt: str = None,
    answer_patterns: list[str] = None,
    short_circuit: bool = True,
    max_tokens: int = 150,
    parallel: bool = True,
) -> VoteResult:
    """Run a question through a model panel and return majority vote.
    
    Args:
        question: The question/prompt to vote on
        panel: Panel name (str) or list of model aliases
        system_prompt: Optional system prompt for all models
        answer_patterns: Custom answer patterns for parsing
        short_circuit: Stop early when first 2 models agree
        max_tokens: Max tokens per model call
        parallel: Run models in parallel (default True)
    
    Returns:
        VoteResult with majority answer and individual votes
    """
    t0 = time.time()
    
    # Resolve panel
    if isinstance(panel, str):
        model_aliases = get_panel(panel)
    else:
        model_aliases = panel
    
    votes = []
    raw_responses = []
    errors = []
    
    # Normalize answer patterns to uppercase
    if answer_patterns:
        answer_patterns = [p.strip().upper() for p in answer_patterns]
    
    def _call(alias):
        ans, raw = call_model(question, alias, system_prompt, max_tokens)
        # Re-parse with custom patterns if provided
        if answer_patterns and ans != "ERROR":
            ans = parse_answer(raw, patterns=answer_patterns)
        return alias, ans, raw
    
    models_used_ordered = []
    
    if parallel:
        # Parallel execution — submit all, optionally short-circuit on agreement
        with ThreadPoolExecutor(max_workers=len(model_aliases)) as pool:
            futures = {pool.submit(_call, alias): alias for alias in model_aliases}
            for fut in as_completed(futures):
                alias, ans, raw = fut.result()
                models_used_ordered.append(alias)
                votes.append(ans)
                raw_responses.append(raw)
                if ans == "ERROR":
                    errors.append(f"{alias}: {raw[:100]}")
                
                # Short-circuit: cancel remaining if first 2 non-error votes agree
                if short_circuit and len(votes) >= 2:
                    non_error = [v for v in votes if v != "ERROR"]
                    if len(non_error) >= 2 and len(set(non_error)) == 1:
                        # Cancel remaining futures
                        for f in futures:
                            f.cancel()
                        break
    
    else:
        # Sequential execution with optional short-circuit
        for i, alias in enumerate(model_aliases):
            _, ans, raw = _call(alias)
            models_used_ordered.append(alias)
            votes.append(ans)
            raw_responses.append(raw)
            if ans == "ERROR":
                errors.append(f"{alias}: {raw[:100]}")
            
            if short_circuit and i >= 1:
                non_error = [v for v in votes if v != "ERROR"]
                if len(non_error) >= 2 and len(set(non_error)) == 1:
                    break
    
    # Count votes (exclude errors)
    non_error_votes = [v for v in votes if v != "ERROR"]
    if not non_error_votes:
        return VoteResult(
            answer="ERROR",
            confidence=f"0/{len(votes)}",
            votes=votes,
            raw_responses=raw_responses,
            models_used=models_used_ordered if models_used_ordered else model_aliases[:len(votes)],
            errors=errors,
            elapsed_s=time.time() - t0,
        )
    
    # Majority vote
    from collections import Counter
    counts = Counter(non_error_votes)
    majority_answer, majority_count = counts.most_common(1)[0]
    total_valid = len(non_error_votes)
    
    sc_tag = " (short-circuit)" if len(votes) < len(model_aliases) else ""
    
    return VoteResult(
        answer=majority_answer,
        confidence=f"{majority_count}/{total_valid}{sc_tag}",
        votes=votes,
        raw_responses=raw_responses,
        models_used=models_used_ordered if models_used_ordered else model_aliases[:len(votes)],
        unanimous=majority_count == total_valid and total_valid >= 2,
        errors=errors,
        elapsed_s=time.time() - t0,
    )


def vote_batch(
    questions: list[dict],
    parallel_questions: int = 5,
    **vote_kwargs,
) -> list[VoteResult]:
    """Vote on multiple questions in parallel.
    
    Each question dict must have 'text' key, and optionally:
    - 'panel', 'system_prompt', 'answer_patterns', 'short_circuit'
    
    Returns list of VoteResults in same order as input.
    """
    results = [None] * len(questions)
    
    def _vote_one(idx, q):
        kwargs = {**vote_kwargs}
        kwargs.update({k: v for k, v in q.items() if k != "text" and k != "id"})
        text = q.get("text", q.get("question_text", ""))
        return idx, vote(text, **kwargs)
    
    with ThreadPoolExecutor(max_workers=parallel_questions) as pool:
        futures = {
            pool.submit(_vote_one, i, q): i
            for i, q in enumerate(questions)
        }
        for fut in as_completed(futures):
            try:
                idx, result = fut.result()
                results[idx] = result
            except Exception as e:
                idx = futures[fut]
                results[idx] = VoteResult(
                    answer="ERROR", confidence="0/0",
                    votes=[], raw_responses=[], models_used=[],
                    errors=[f"Batch item error: {e}"],
                )

    return results
