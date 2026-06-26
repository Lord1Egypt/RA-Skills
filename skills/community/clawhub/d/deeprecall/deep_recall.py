"""
DeepRecall — Recursive Memory for Persistent AI Agents (Pure-Python RLM)

Implements a manager→workers→synthesis loop entirely in Python.
No Deno, no fast-rlm subprocess — just HTTP calls to any OpenAI-compatible
LLM endpoint via httpx (with requests as fallback).

Part of the Anamnesis Architecture:
"The soul stays small, the mind scales forever."

Usage:
    from deep_recall import recall

    # Simple memory query
    result = recall("What did we decide about the budget?")

    # With options
    result = recall(
        "Summarize all project decisions from March",
        scope="memory",
        verbose=True,
        config_overrides={"max_files": 3},
    )
"""

from __future__ import annotations

import json
import logging
import os
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any, Optional

# ---------------------------------------------------------------------------
# Package imports — prefer relative (package), fall back for direct script use
# ---------------------------------------------------------------------------
try:
    from .provider_bridge import resolve_provider, ProviderConfig
    from .model_pairs import get_model_pair
    from .memory_scanner import MemoryScanner
    from .memory_indexer import build_memory_index, update_memory_index
except ImportError:
    # Fallback: running as a standalone script (python skill/deep_recall.py)
    _SKILL_DIR = Path(__file__).parent
    if str(_SKILL_DIR) not in sys.path:
        sys.path.insert(0, str(_SKILL_DIR))
    from provider_bridge import resolve_provider, ProviderConfig  # type: ignore[no-redef]
    from model_pairs import get_model_pair  # type: ignore[no-redef]
    from memory_scanner import MemoryScanner  # type: ignore[no-redef]
    from memory_indexer import build_memory_index, update_memory_index  # type: ignore[no-redef]

logger = logging.getLogger("deep_recall")

# Maximum number of manager→workers→synthesis rounds.
# Kept at 1 to prevent runaway recursion; raise only with explicit intent.
_MAX_TOOL_ROUNDS: int = 1

# ---------------------------------------------------------------------------
# HTTP client — prefer httpx, fall back to requests
# ---------------------------------------------------------------------------

_HTTP_CLIENT: Optional[str] = None


def _get_http_client() -> str:
    """Return 'httpx' or 'requests' depending on what is installed."""
    global _HTTP_CLIENT
    if _HTTP_CLIENT is not None:
        return _HTTP_CLIENT
    try:
        import httpx  # noqa: F401
        _HTTP_CLIENT = "httpx"
    except ImportError:
        try:
            import requests  # noqa: F401
            _HTTP_CLIENT = "requests"
        except ImportError:
            raise ImportError(
                "DeepRecall requires either 'httpx' or 'requests'. "
                "Install one with: pip install httpx"
            )
    return _HTTP_CLIENT


def _http_post(url: str, *, headers: dict, json_body: dict, timeout: float = 120) -> dict:
    """POST JSON and return the parsed response body."""
    client = _get_http_client()
    if client == "httpx":
        import httpx
        resp = httpx.post(url, headers=headers, json=json_body, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    else:
        import requests
        resp = requests.post(url, headers=headers, json=json_body, timeout=timeout)
        resp.raise_for_status()
        return resp.json()


# ---------------------------------------------------------------------------
# Anti-hallucination system prompts
# ---------------------------------------------------------------------------

_WORKER_SYSTEM = (
    "You are a quote extractor. Your job is to find EXACT quotes from "
    "the provided document that are relevant to the user's query.\n\n"
    "RULES — follow these EXACTLY:\n"
    "1. Return ONLY text that appears verbatim in the document.\n"
    "2. Do not paraphrase, summarize, or invent text.\n"
    "3. Copy each relevant passage EXACTLY as it appears, character for character.\n"
    "4. For each quote include the approximate line number.\n"
    "5. If nothing relevant is found, return an empty quotes list.\n\n"
    'Respond with JSON: {"quotes": [{"text": "...", "line": N}, ...]}'
)

_SYNTHESIS_SYSTEM = (
    "You are a memory-recall synthesis agent. You receive exact quotes "
    "extracted from the user's memory files and must compose a clear, "
    "accurate answer to the user's query.\n\n"
    "RULES:\n"
    "1. Base your answer ONLY on the provided quotes. Do not add information "
    "that is not supported by the quotes.\n"
    "2. Cite your sources using the format (filename:line).\n"
    "3. If quotes are contradictory, note the discrepancy.\n"
    "4. Prefer detailed answers from LONG_TERM.md over summaries from MEMORY.md. "
    "Include the full story - decisions, reasoning, timestamps. "
    "Don't give the Wikipedia summary, give the diary entry.\n"
    "4. If the quotes do not answer the question, say so honestly.\n"
)

_MANAGER_SYSTEM = (
    "You are a memory-file selector. You receive a Memory Index that "
    "describes the user's memory files and a query. Your job is to select "
    "the files most likely to contain the answer.\n\n"
    "PRIORITY RULE: ALWAYS include memory/LONG_TERM.md if it exists in the index. "
    "LONG_TERM.md contains detailed memories with full context, decisions, "
    "and reasoning. MEMORY.md is just a summary index. The devil is in the "
    "details — prefer LONG_TERM.md for complete answers.\n\n"
    "Respond with JSON: {\"files\": [\"path/to/file1.md\", ...]}\n"
    "Select only the most relevant files. Return at most {max_files} files.\n"
    "If no files seem relevant, return {\"files\": []}."
)


# ---------------------------------------------------------------------------
# Core LLM call
# ---------------------------------------------------------------------------

def _chat(
    messages: list[dict[str, str]],
    provider: ProviderConfig,
    json_mode: bool = False,
) -> str:
    """Send a chat-completion request and return the assistant text.

    Works with any OpenAI-compatible API endpoint.
    """
    url = provider.base_url.rstrip("/") + "/chat/completions"

    headers = {
        "Authorization": f"Bearer {provider.api_key}",
        "Content-Type": "application/json",
        **provider.default_headers,
    }

    model = provider.primary_model
    if "/" in model:
        model = model.split("/", 1)[1]

    body: dict[str, Any] = {
        "model": model,
        "messages": messages,
    }
    if json_mode:
        body["response_format"] = {"type": "json_object"}

    data = _http_post(url, headers=headers, json_body=body, timeout=120.0)

    choices = data.get("choices", [])
    if not choices:
        raise RuntimeError("LLM returned no choices")
    return choices[0]["message"]["content"]


# ---------------------------------------------------------------------------
# Path safety and sandboxed file reading (path-traversal protection)
# ---------------------------------------------------------------------------

def _safe_path(relative_path: str, workspace: Path) -> Optional[Path]:
    """Resolve *relative_path* inside *workspace*.

    Returns the resolved ``Path`` when it is strictly contained within
    *workspace*, or ``None`` if the path would escape the workspace
    (directory traversal, symlink escape, or absolute path injection).
    """
    try:
        target = (workspace / relative_path).resolve()
        ws_resolved = workspace.resolve()
        # target must be either exactly the workspace root or a child of it
        if not str(target).startswith(str(ws_resolved) + os.sep) and target != ws_resolved:
            return None
        return target
    except Exception:
        return None


def _read_file(relative_path: str, workspace: Path) -> Optional[str]:
    """Read a file safely within *workspace*; returns None on failure."""
    path = _safe_path(relative_path, workspace)
    if path is None or not path.is_file():
        return None
    try:
        return path.read_text(errors="replace")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Tool-code sandbox (execution guard)
# ---------------------------------------------------------------------------

def _execute_tool_code(code: str, sandbox: dict) -> str:
    """Sandbox boundary for any tool-code execution requests.

    Arbitrary code execution is **not** permitted.  This function exists as
    an explicit security boundary so that any future call-site is forced to
    go through a named choke-point rather than using ``eval``/``exec``
    directly.

    Args:
        code: The code string that was requested to run.
        sandbox: Any contextual bindings that would have been available.

    Returns:
        A refusal message — execution never proceeds.
    """
    logger.warning(
        "_execute_tool_code called; code execution is disabled (sandbox). "
        "code_snippet=%r", code[:120]
    )
    return "[sandbox] Code execution is not permitted in this environment."


# ---------------------------------------------------------------------------
# RLM loop: manager → workers → synthesis
# ---------------------------------------------------------------------------

def _manager_call(
    query: str,
    memory_index: str,
    max_files: int,
    provider: ProviderConfig,
) -> list[str]:
    """Ask the LLM to pick the most relevant files from the memory index.

    Raises on API/network errors so that ``recall()`` can report them.
    Returns ``[]`` only when the LLM responds with unparseable or empty JSON.
    """
    system = _MANAGER_SYSTEM.replace("{max_files}", str(max_files))
    messages = [
        {"role": "system", "content": system},
        {"role": "user", "content": (
            f"QUERY: {query}\n\n"
            f"=== MEMORY INDEX ===\n{memory_index}"
        )},
    ]
    raw = _chat(messages, provider, json_mode=True)

    try:
        data = json.loads(raw)
        files = data.get("files", [])
        if not isinstance(files, list):
            return []
        return [str(f) for f in files[:max_files]]
    except (json.JSONDecodeError, TypeError):
        return []


def _worker_call(
    query: str,
    filepath: str,
    content: str,
    provider: ProviderConfig,
) -> dict:
    """Extract exact quotes from a single file relevant to the query."""
    messages = [
        {"role": "system", "content": _WORKER_SYSTEM},
        {"role": "user", "content": (
            f"QUERY: {query}\n\n"
            f"=== FILE: {filepath} ===\n{content}"
        )},
    ]
    try:
        raw = _chat(messages, provider, json_mode=True)
        data = json.loads(raw)
        quotes = data.get("quotes", [])
        if not isinstance(quotes, list):
            quotes = []
    except Exception:
        quotes = []

    return {"file": filepath, "quotes": quotes}


def _synthesis_call(
    query: str,
    worker_results: list[dict],
    provider: ProviderConfig,
) -> str:
    """Synthesize worker quotes into a coherent answer."""
    # Gather all quotes
    all_quotes: list[str] = []
    for wr in worker_results:
        for q in wr.get("quotes", []):
            text = q.get("text", "")
            line = q.get("line", "?")
            all_quotes.append(f'[{wr["file"]}:{line}] "{text}"')

    if not all_quotes:
        return "I don't have memories that answer this query."

    messages = [
        {"role": "system", "content": _SYNTHESIS_SYSTEM},
        {"role": "user", "content": (
            f"QUERY: {query}\n\n"
            f"=== EXTRACTED QUOTES ===\n" + "\n".join(all_quotes)
        )},
    ]
    try:
        return _chat(messages, provider)
    except Exception as exc:
        return f"Synthesis failed: {exc}"


# ---------------------------------------------------------------------------
# Workspace helpers
# ---------------------------------------------------------------------------

def _find_workspace() -> Path:
    """Find the OpenClaw workspace directory."""
    ws = os.environ.get("OPENCLAW_WORKSPACE")
    if ws:
        return Path(ws)

    config_file = Path(os.path.expanduser("~/.openclaw/openclaw.json"))
    if config_file.exists():
        try:
            with open(config_file) as f:
                config = json.load(f)
            ws = config.get("agents", {}).get("defaults", {}).get("workspace")
            if ws:
                return Path(ws)
        except Exception:
            pass

    return Path(os.path.expanduser("~/.openclaw/workspace"))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

_DEFAULT_MAX_FILES = 3


def recall(
    query: str,
    scope: str = "memory",
    workspace: Optional[Path] = None,
    verbose: bool = False,
    config_overrides: Optional[dict] = None,
    max_depth: int = 1,
) -> str:
    """
    Recursively query the agent's memory using a pure-Python RLM loop.

    Flow:
        1. Resolve LLM provider from OpenClaw config
        2. Scan workspace for memory files
        3. Build memory index
        4. **Manager** selects relevant files from the index
        5. **Workers** (parallel) extract exact quotes from each file
        6. **Synthesis** combines quotes into a coherent answer

    Args:
        query: What to recall / search for / analyse.
        scope: ``"memory"`` | ``"identity"`` | ``"project"`` | ``"all"``.
        workspace: Override workspace path (default: auto-detect).
        verbose: Print progress to stdout.
        config_overrides: Override settings (``max_files``, etc.).
        max_depth: Number of manager→workers→synthesis rounds to run.
            Must be >= 1; capped at ``_MAX_TOOL_ROUNDS`` (currently 1).
            Default is 1 (single pass).

    Returns:
        The recalled information as a string.
    """
    overrides = config_overrides or {}
    max_files = overrides.get("max_files", _DEFAULT_MAX_FILES)
    # Enforce depth bounds: minimum 1, never exceed _MAX_TOOL_ROUNDS.
    max_depth = max(1, min(max_depth, _MAX_TOOL_ROUNDS))

    # 1. Resolve provider
    try:
        provider = resolve_provider()
    except RuntimeError as e:
        raise RuntimeError(f"DeepRecall cannot resolve LLM provider: {e}")

    # 2. Scan memory files
    ws = Path(workspace) if workspace else _find_workspace()
    scanner = MemoryScanner(workspace=ws)
    scanner.scan(scope=scope)

    if not scanner.files:
        return "[DeepRecall] No memory files found in workspace."

    # 3. Build memory index
    memory_index = build_memory_index(workspace=ws)

    if verbose:
        pair = get_model_pair(provider.primary_model)
        print(f"🧠 DeepRecall running (pure-Python RLM)...")
        print(f"   Provider : {provider.provider}")
        print(f"   Model    : {pair['primary']} (workers: {pair['sub_agent']})")
        print(f"   Scope    : {scope}")
        print(f"   Files    : {len(scanner.files)}")
        print(f"   Max pick : {max_files}")

    # 4. Manager: pick the relevant files
    try:
        selected_files = _manager_call(query, memory_index, max_files, provider)
    except Exception as exc:
        return f"[DeepRecall] Manager call failed: {exc}"

    if not selected_files:
        return "[DeepRecall] No relevant memory files identified for this query."

    if verbose:
        print(f"   Selected : {selected_files}")

    # 5. Workers: extract quotes in parallel
    worker_results: list[dict] = []
    with ThreadPoolExecutor(max_workers=min(len(selected_files), 4)) as pool:
        futures = {}
        for fpath in selected_files:
            content = _read_file(fpath, ws)
            if content is None:
                continue
            fut = pool.submit(_worker_call, query, fpath, content, provider)
            futures[fut] = fpath

        for fut in as_completed(futures):
            try:
                worker_results.append(fut.result())
            except Exception:
                worker_results.append({"file": futures[fut], "quotes": []})

    # 6. Synthesis
    answer = _synthesis_call(query, worker_results, provider)

    if verbose:
        total_quotes = sum(len(wr.get("quotes", [])) for wr in worker_results)
        print(f"   Quotes   : {total_quotes}")
        print()

    return answer


def recall_quick(query: str, verbose: bool = False) -> str:
    """Quick recall — identity scope, max 2 files."""
    return recall(
        query,
        scope="identity",
        verbose=verbose,
        config_overrides={"max_files": 2},
    )


def recall_deep(query: str, verbose: bool = False) -> str:
    """Deep recall — all scope, max 5 files."""
    return recall(
        query,
        scope="all",
        verbose=verbose,
        config_overrides={"max_files": 5},
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deep_recall.py <query> [scope]")
        print("Scopes: memory (default), identity, project, all")
        sys.exit(1)

    query = sys.argv[1]
    scope = sys.argv[2] if len(sys.argv) > 2 else "memory"

    print(f"🧠 DeepRecall: querying memory (scope={scope})...")
    print(f"   Query: {query}\n")

    try:
        result = recall(query, scope=scope, verbose=True)
        print(f"\n📝 Result:\n{result}")
    except RuntimeError as e:
        print(f"❌ Error: {e}")
