"""
CLI entry-point for agent-bench-lite.

Usage::

    agent-bench-lite                     # Run with EchoAdapter (demo)
    agent-bench-lite --adapter echo      # Explicit EchoAdapter
    agent-bench-lite --adapter anthropic # Requires ANTHROPIC_API_KEY
    agent-bench-lite --adapter openai    # Requires OPENAI_API_KEY
    agent-bench-lite --output report.json
    agent-bench-lite --dimensions tool_calling,planning
"""

from __future__ import annotations

import argparse
import asyncio
import sys


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="agent-bench-lite",
        description="Lightweight AI Agent evaluation benchmark.",
    )
    p.add_argument(
        "--adapter",
        choices=["echo", "anthropic", "openai"],
        default="echo",
        help="LLM adapter to use (default: echo — runs without API keys).",
    )
    p.add_argument(
        "--model",
        default=None,
        help="Model name to pass to the adapter (e.g. gpt-4o, claude-sonnet-4-20250514).",
    )
    p.add_argument(
        "--output", "-o",
        default=None,
        help="Path to write the JSON report to.",
    )
    p.add_argument(
        "--dimensions",
        default=None,
        help="Comma-separated list of dimension names to run (default: all).",
    )
    p.add_argument(
        "--sequential",
        action="store_true",
        help="Run dimensions sequentially instead of in parallel.",
    )
    p.add_argument(
        "--details",
        action="store_true",
        help="Print per-task details after the summary.",
    )
    return p


def _make_adapter(name: str, model: str | None):
    """Instantiate the requested adapter."""
    if name == "echo":
        from agent_bench_lite.adapters.base import EchoAdapter
        return EchoAdapter()
    if name == "anthropic":
        from agent_bench_lite.adapters.anthropic_adapter import AnthropicAdapter
        return AnthropicAdapter(model=model) if model else AnthropicAdapter()
    if name == "openai":
        from agent_bench_lite.adapters.openai_adapter import OpenAIAdapter
        return OpenAIAdapter(model=model) if model else OpenAIAdapter()
    raise ValueError(f"Unknown adapter: {name}")


async def _async_main(args: argparse.Namespace) -> int:
    from agent_bench_lite.core.runner import BenchmarkRunner, RunConfig

    adapter = _make_adapter(args.adapter, args.model)

    dims = None
    if args.dimensions:
        dims = [d.strip() for d in args.dimensions.split(",")]

    config = RunConfig(
        parallel=not args.sequential,
        dimensions=dims,
        metadata={"adapter": args.adapter},
    )
    if args.model:
        config.metadata["model"] = args.model

    runner = BenchmarkRunner(adapter=adapter, config=config)
    report = await runner.run()

    report.print_summary()
    if args.details:
        report.print_details()

    if args.output:
        path = report.save_json(args.output)
        print(f"\nReport saved to: {path}")

    return 0


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    sys.exit(asyncio.run(_async_main(args)))


if __name__ == "__main__":
    main()
