#!/usr/bin/env python3
"""CLI bridge between OpenClaw and the Agenter SDK.

Wraps AutonomousCodingAgent in a CLI that outputs structured JSON,
so OpenClaw can invoke it via bash and parse results.

Usage:
    python3 agenter_cli.py --prompt "Create a FastAPI app" --cwd /workspace
    python3 agenter_cli.py --prompt "Fix the bug" --cwd . --backend claude-code --stream
"""

from __future__ import annotations

import argparse
import asyncio
import json
import sys


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Agenter CLI for OpenClaw — run autonomous coding tasks",
    )
    parser.add_argument("--prompt", required=True, help="The coding task description")
    parser.add_argument("--cwd", required=True, help="Working directory for file operations")
    parser.add_argument(
        "--backend",
        default="anthropic-sdk",
        choices=["anthropic-sdk", "claude-code", "codex", "openhands"],
        help="Backend runtime (default: anthropic-sdk)",
    )
    parser.add_argument("--model", default=None, help="Model override (e.g. claude-sonnet-4-20250514)")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max validation/retry iterations")
    parser.add_argument("--max-cost-usd", type=float, default=None, help="Maximum spend in USD")
    parser.add_argument("--max-tokens", type=int, default=None, help="Maximum total tokens")
    parser.add_argument("--max-time-seconds", type=float, default=None, help="Maximum wall clock time")
    parser.add_argument("--allowed-write-paths", nargs="*", default=None, help="Glob patterns for allowed writes")
    parser.add_argument("--sandbox", action="store_true", default=True, help="Enable sandboxed execution (default)")
    parser.add_argument("--no-sandbox", dest="sandbox", action="store_false", help="Disable sandbox")
    parser.add_argument("--stream", action="store_true", default=False, help="Emit NDJSON progress events")
    return parser.parse_args()


def _result_to_dict(result) -> dict:
    """Convert a CodingResult to a JSON-serializable dict."""
    return {
        "status": result.status.value,
        "summary": result.summary,
        "files_modified": list(result.files.keys()),
        "files": result.files,
        "iterations": result.iterations,
        "total_tokens": result.total_tokens,
        "total_cost_usd": result.total_cost_usd,
        "total_duration_seconds": result.total_duration_seconds,
    }


async def run_blocking(args: argparse.Namespace) -> None:
    """Run agenter to completion and print final JSON result to stdout."""
    from agenter import AutonomousCodingAgent, Budget, CodingRequest, Verbosity

    agent = AutonomousCodingAgent(
        backend=args.backend,
        model=args.model,
        sandbox=args.sandbox,
    )

    budget = Budget(
        max_iterations=args.max_iterations,
        max_cost_usd=args.max_cost_usd,
        max_tokens=args.max_tokens,
        max_time_seconds=args.max_time_seconds,
    )

    request = CodingRequest(
        prompt=args.prompt,
        cwd=args.cwd,
        budget=budget,
        allowed_write_paths=args.allowed_write_paths,
    )

    result = await agent.execute(request, verbosity=Verbosity.QUIET)
    print(json.dumps(_result_to_dict(result), indent=2))


async def run_streaming(args: argparse.Namespace) -> None:
    """Run agenter with streaming, emit NDJSON events to stdout."""
    from agenter import AutonomousCodingAgent, Budget, CodingRequest

    agent = AutonomousCodingAgent(
        backend=args.backend,
        model=args.model,
        sandbox=args.sandbox,
    )

    budget = Budget(
        max_iterations=args.max_iterations,
        max_cost_usd=args.max_cost_usd,
        max_tokens=args.max_tokens,
        max_time_seconds=args.max_time_seconds,
    )

    request = CodingRequest(
        prompt=args.prompt,
        cwd=args.cwd,
        budget=budget,
        allowed_write_paths=args.allowed_write_paths,
    )

    async for event in agent.stream_execute(request):
        line: dict = {
            "event": event.type.value,
        }
        if event.data is not None:
            line["data"] = event.data.model_dump()
        if event.result is not None:
            line["result"] = _result_to_dict(event.result)
        print(json.dumps(line), flush=True)


def main() -> None:
    args = parse_args()
    try:
        if args.stream:
            asyncio.run(run_streaming(args))
        else:
            asyncio.run(run_blocking(args))
    except KeyboardInterrupt:
        sys.exit(130)
    except Exception as exc:
        error = {"status": "error", "error": str(exc)}
        print(json.dumps(error), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
