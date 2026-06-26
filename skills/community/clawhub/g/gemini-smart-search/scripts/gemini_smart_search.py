#!/usr/bin/env python3
"""Gemini Smart Search.

Minimal Gemini-only smart search worker with model routing and fallback.

Features:
- accepts --query / --mode / --json
- resolves API key from SMART_SEARCH_GEMINI_API_KEY then GEMINI_API_KEY
- tries a model chain based on mode
- uses Google Search grounding via the Gemini API
- falls back on quota / unavailable model / transient upstream errors
- returns standardized JSON for orchestration
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any

DISPLAY_MODEL_CHAINS = {
    "cheap": ["gemini-2.5-flash-lite", "gemini-3.1-flash-lite", "gemini-2.5-flash"],
    "balanced": ["gemini-2.5-flash", "gemini-3-flash", "gemini-2.5-flash-lite"],
    "deep": ["gemini-3-flash", "gemini-2.5-flash", "gemini-3.1-flash-lite"],
}

MODEL_CANDIDATES = {
    "gemini-2.5-flash-lite": ["gemini-2.5-flash-lite"],
    "gemini-2.5-flash": ["gemini-2.5-flash"],
    "gemini-3-flash": ["gemini-3-flash-preview", "gemini-3-flash"],
    "gemini-3.1-flash-lite": ["gemini-3.1-flash-lite-preview", "gemini-3.1-flash-lite"],
}

API_BASE = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
DEFAULT_TIMEOUT_SECONDS = 45
ISSUE_URL = "https://github.com/jas0n1ee/gemini-smart-search/issues/new"


@dataclass
class SearchError(Exception):
    type: str
    message: str
    status: int | None = None
    retryable: bool = False
    raw_status: str | None = None

    def to_dict(self) -> dict[str, Any]:
        data: dict[str, Any] = {
            "type": self.type,
            "message": self.message,
        }
        if self.status is not None:
            data["status"] = self.status
        if self.raw_status:
            data["raw_status"] = self.raw_status
        return data


def load_repo_local_env() -> None:
    if os.environ.get("GEMINI_SMART_SEARCH_SKIP_LOCAL_ENV") == "1":
        return
    script_dir = Path(__file__).resolve().parent
    env_path = script_dir.parent / ".env.local"
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip()
        if not key or key in os.environ:
            continue
        if value and len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
            value = value[1:-1]
        os.environ[key] = value


def resolve_api_key() -> str | None:
    return os.environ.get("SMART_SEARCH_GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")


class JsonArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        wants_json = "--json" in sys.argv[1:]
        if wants_json:
            mode = "balanced"
            argv = sys.argv[1:]
            for idx, token in enumerate(argv):
                if token == "--mode" and idx + 1 < len(argv):
                    mode = argv[idx + 1]
                elif token.startswith("--mode="):
                    mode = token.split("=", 1)[1]
            display_chain = DISPLAY_MODEL_CHAINS.get(mode, DISPLAY_MODEL_CHAINS["balanced"])
            fallback_chain = []
            for display_name in display_chain:
                fallback_chain.extend(MODEL_CANDIDATES.get(display_name, [display_name]))
            result = {
                "ok": False,
                "query": None,
                "mode": mode,
                "model_used": None,
                "fallback_chain": fallback_chain,
                "display_chain": display_chain,
                "answer": None,
                "citations": [],
                "usage": {"provider": "gemini", "grounding": True, "attempted_models": []},
                "error": {
                    "type": "invalid_arguments",
                    "message": message,
                },
                "escalation": default_escalation(),
            }
            print(json.dumps(result, ensure_ascii=False, indent=2), file=sys.stderr)
            raise SystemExit(2)
        super().error(message)


def parse_args() -> argparse.Namespace:
    p = JsonArgumentParser(description="Gemini smart search")
    p.add_argument("--query", required=True, help="Search query")
    p.add_argument("--mode", choices=sorted(DISPLAY_MODEL_CHAINS), default="balanced")
    p.add_argument("--json", action="store_true", help="Print JSON output")
    return p.parse_args()


def build_request(query: str) -> dict[str, Any]:
    return {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": (
                            "Answer the user's query using Google Search grounding when helpful. "
                            "Provide a concise synthesis and cite relevant sources in grounding metadata.\n\n"
                            f"Query: {query}"
                        )
                    }
                ],
            }
        ],
        "tools": [{"google_search": {}}],
        "generationConfig": {
            "temperature": 0.2,
            "topP": 0.95,
            "maxOutputTokens": 1024,
        },
    }


def classify_api_error(status: int | None, payload: dict[str, Any] | None, fallback_message: str) -> SearchError:
    error_obj = (payload or {}).get("error") or {}
    raw_status = error_obj.get("status")
    message = error_obj.get("message") or fallback_message

    text_blob = " ".join(
        str(x)
        for x in [message, raw_status]
        if x
    ).lower()

    retryable_statuses = {429, 500, 502, 503, 504}
    retryable_raw_statuses = {
        "resource_exhausted",
        "unavailable",
        "deadline_exceeded",
        "aborted",
        "internal",
    }

    is_model_unavailable = (
        (status in {400, 404})
        and any(token in text_blob for token in ["model", "not found", "unsupported", "not available", "not supported"])
    )

    if is_model_unavailable:
        return SearchError(
            type="model_unavailable",
            message=message,
            status=status,
            retryable=True,
            raw_status=raw_status,
        )

    if status in retryable_statuses or (raw_status or "").lower() in retryable_raw_statuses:
        err_type = "quota_exceeded" if status == 429 or "resource_exhausted" in text_blob else "transient_upstream"
        return SearchError(
            type=err_type,
            message=message,
            status=status,
            retryable=True,
            raw_status=raw_status,
        )

    return SearchError(
        type="api_error",
        message=message,
        status=status,
        retryable=False,
        raw_status=raw_status,
    )


def extract_text(candidate: dict[str, Any]) -> str:
    parts = (((candidate.get("content") or {}).get("parts")) or [])
    texts = [part.get("text", "") for part in parts if isinstance(part, dict) and part.get("text")]
    return "\n".join(texts).strip()


def extract_citations(data: dict[str, Any]) -> list[dict[str, str]]:
    citations: list[dict[str, str]] = []
    seen: set[tuple[str, str]] = set()

    candidates = data.get("candidates") or []
    for candidate in candidates:
        grounding = candidate.get("groundingMetadata") or candidate.get("grounding_metadata") or {}
        chunks = grounding.get("groundingChunks") or grounding.get("grounding_chunks") or []
        for chunk in chunks:
            web = chunk.get("web") or {}
            title = (web.get("title") or "").strip()
            url = (web.get("uri") or web.get("url") or "").strip()
            if not url:
                continue
            key = (title, url)
            if key in seen:
                continue
            seen.add(key)
            citations.append({"title": title or url, "url": url})
    return citations


def call_gemini(model: str, query: str, api_key: str) -> dict[str, Any]:
    url = API_BASE.format(model=urllib.parse.quote(model, safe=""))

    body = json.dumps(build_request(query)).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=DEFAULT_TIMEOUT_SECONDS) as response:
            payload = response.read().decode("utf-8")
            return json.loads(payload)
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        payload = None
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = None
        raise classify_api_error(exc.code, payload, raw or f"HTTP {exc.code}") from None
    except urllib.error.URLError as exc:
        raise SearchError(
            type="network_error",
            message=str(exc.reason),
            retryable=True,
        ) from None
    except TimeoutError:
        raise SearchError(
            type="network_timeout",
            message="Request timed out",
            retryable=True,
        ) from None


def expand_model_chain(mode: str) -> list[str]:
    chain: list[str] = []
    for display_name in DISPLAY_MODEL_CHAINS[mode]:
        chain.extend(MODEL_CANDIDATES.get(display_name, [display_name]))
    return chain


def default_escalation() -> dict[str, Any]:
    return {
        "should_open_issue": False,
        "issue_url": None,
        "reason": None,
        "kind": None,
        "recommended_details": [],
    }


def build_escalation(error_type: str, reason: str | None = None) -> dict[str, Any]:
    mapping = {
        "schema_mismatch": "api-compat",
        "unexpected_response_shape": "api-compat",
        "all_models_failed": "model-routing",
        "model_unavailable": "model-routing",
        "internal_error": "bug",
        "contract_drift": "docs-mismatch",
    }
    kind = mapping.get(error_type)
    if not kind:
        return default_escalation()
    return {
        "should_open_issue": True,
        "issue_url": ISSUE_URL,
        "reason": reason or error_type,
        "kind": kind,
        "recommended_details": [
            "query",
            "mode",
            "display_chain",
            "fallback_chain",
            "model_used",
            "usage.attempted_models",
            "error.type",
            "error.message",
        ],
    }


def run_search(query: str, mode: str, api_key: str) -> dict[str, Any]:
    display_chain = DISPLAY_MODEL_CHAINS[mode]
    fallback_chain = expand_model_chain(mode)
    errors: list[dict[str, Any]] = []

    for model in fallback_chain:
        try:
            data = call_gemini(model=model, query=query, api_key=api_key)
            candidates = data.get("candidates") or []
            answer = extract_text(candidates[0]) if candidates else ""
            citations = extract_citations(data)
            if not answer:
                raise SearchError(
                    type="empty_response",
                    message="Gemini returned no answer text.",
                    retryable=False,
                )
            return {
                "ok": True,
                "query": query,
                "mode": mode,
                "model_used": model,
                "fallback_chain": fallback_chain,
                "display_chain": display_chain,
                "answer": answer,
                "citations": citations,
                "usage": {
                    "provider": "gemini",
                    "grounding": True,
                    "attempted_models": [entry["model"] for entry in errors] + [model],
                },
                "error": None,
                "escalation": default_escalation(),
            }
        except SearchError as exc:
            errors.append({"model": model, **exc.to_dict()})
            if exc.retryable:
                continue
            return {
                "ok": False,
                "query": query,
                "mode": mode,
                "model_used": None,
                "fallback_chain": fallback_chain,
                "display_chain": display_chain,
                "answer": None,
                "citations": [],
                "usage": {
                    "provider": "gemini",
                    "grounding": True,
                    "attempted_models": [entry["model"] for entry in errors],
                },
                "error": {
                    **exc.to_dict(),
                    "attempts": errors,
                },
                "escalation": build_escalation(exc.type, exc.message),
            }

    final_error = SearchError(
        type="all_models_failed",
        message="All models in the fallback chain failed.",
        retryable=True,
    )
    return {
        "ok": False,
        "query": query,
        "mode": mode,
        "model_used": None,
        "fallback_chain": fallback_chain,
        "display_chain": display_chain,
        "answer": None,
        "citations": [],
        "usage": {
            "provider": "gemini",
            "grounding": True,
            "attempted_models": [entry["model"] for entry in errors],
        },
        "error": {
            **final_error.to_dict(),
            "attempts": errors,
        },
        "escalation": build_escalation(final_error.type, final_error.message),
    }


def print_human(result: dict[str, Any]) -> None:
    if result["ok"]:
        print(result["answer"])
        if result["citations"]:
            print("\nSources:")
            for citation in result["citations"]:
                print(f"- {citation['title']}: {citation['url']}")
    else:
        error = result.get("error") or {}
        print(error.get("message") or "Search failed")


def main() -> int:
    args = parse_args()
    load_repo_local_env()
    api_key = resolve_api_key()

    if not api_key:
        result = {
            "ok": False,
            "query": args.query,
            "mode": args.mode,
            "model_used": None,
            "fallback_chain": expand_model_chain(args.mode),
            "display_chain": DISPLAY_MODEL_CHAINS[args.mode],
            "answer": None,
            "citations": [],
            "usage": {"provider": "gemini", "grounding": True, "attempted_models": []},
            "error": {
                "type": "missing_api_key",
                "message": "Missing Gemini API key. Set SMART_SEARCH_GEMINI_API_KEY or GEMINI_API_KEY.",
            },
            "escalation": default_escalation(),
        }
        if args.json:
            print(json.dumps(result, ensure_ascii=False, indent=2))
        else:
            print(result["error"]["message"], file=sys.stderr)
        return 1

    try:
        result = run_search(query=args.query, mode=args.mode, api_key=api_key)
    except Exception as exc:  # defensive final boundary
        result = {
            "ok": False,
            "query": args.query,
            "mode": args.mode,
            "model_used": None,
            "fallback_chain": expand_model_chain(args.mode),
            "display_chain": DISPLAY_MODEL_CHAINS[args.mode],
            "answer": None,
            "citations": [],
            "usage": {"provider": "gemini", "grounding": True, "attempted_models": []},
            "error": {
                "type": "internal_error",
                "message": str(exc) or exc.__class__.__name__,
            },
            "escalation": build_escalation("internal_error", str(exc) or exc.__class__.__name__),
        }
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_human(result)
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
