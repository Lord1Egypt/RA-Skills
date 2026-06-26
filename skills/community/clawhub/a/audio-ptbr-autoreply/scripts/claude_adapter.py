#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from anthropic import Anthropic
except Exception:
    Anthropic = None  # type: ignore

DEFAULT_TIMEOUT = int(os.environ.get("RESPONSE_TIMEOUT", "30"))


class ResponseError(Exception):
    pass


def read_transcript(args: argparse.Namespace) -> str:
    if args.stdin:
        return sys.stdin.read().strip()
    if args.input_file:
        return Path(args.input_file).read_text(encoding="utf-8").strip()
    if args.transcript is not None:
        return args.transcript.strip()
    raise ResponseError("No transcript provided")


def get_anthropic_response(transcript: str, timeout: int) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ResponseError("ANTHROPIC_API_KEY not configured")
    if Anthropic is None:
        raise ResponseError("anthropic package not installed")

    client = Anthropic(api_key=api_key)
    msg = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=180,
        system=(
            "Você é um assistente de voz em português brasileiro. "
            "Responda de forma curta, natural e clara, em no máximo 2 frases. "
            "Sem listas, sem markdown, sem emojis."
        ),
        messages=[{"role": "user", "content": transcript}],
        timeout=timeout,
    )
    text = msg.content[0].text.strip()
    if not text:
        raise ResponseError("Empty Anthropic response")
    return text


def get_openclaw_response(transcript: str, timeout: int) -> str:
    try:
        result = subprocess.run(
            ["openclaw", "infer", "model", "run", "--prompt", transcript, "--json"],
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise ResponseError("openclaw command not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise ResponseError(f"openclaw timed out after {timeout}s") from exc

    if result.returncode != 0:
        raise ResponseError(result.stderr.strip() or f"openclaw exited with {result.returncode}")

    try:
        payload = json.loads(result.stdout)
        text = str(payload.get("response", "")).strip()
        if text:
            return text
    except json.JSONDecodeError:
        pass

    fallback = result.stdout.strip()
    if fallback:
        return fallback
    raise ResponseError("Empty local OpenClaw response")


def generate_response(transcript: str, timeout: int) -> dict[str, Any]:
    transcript = transcript.strip()
    if not transcript:
        raise ValueError("Transcript cannot be empty")

    errors: list[str] = []

    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            text = get_anthropic_response(transcript, timeout)
            return {"success": True, "response": text, "provider": "anthropic"}
        except Exception as exc:
            errors.append(f"anthropic: {exc}")

    try:
        text = get_openclaw_response(transcript, timeout)
        return {"success": True, "response": text, "provider": "openclaw"}
    except Exception as exc:
        errors.append(f"openclaw: {exc}")

    fallback = f"Entendi. Você disse: {transcript[:80]}"
    return {"success": True, "response": fallback, "provider": "fallback", "errors": errors}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("transcript", nargs="?")
    parser.add_argument("--stdin", action="store_true", help="Read transcript from stdin")
    parser.add_argument("--input-file", help="Read transcript from a UTF-8 text file")
    parser.add_argument("--text", action="store_true", help="Print only response text")
    parser.add_argument("--json", action="store_true", help="Print JSON payload")
    parser.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT)
    args = parser.parse_args()

    try:
        transcript = read_transcript(args)
        data = generate_response(transcript, args.timeout)
    except Exception as exc:
        payload = {"success": False, "error": str(exc)}
        print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
        return 1

    if args.text:
        print(data["response"])
    else:
        print(json.dumps(data, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
