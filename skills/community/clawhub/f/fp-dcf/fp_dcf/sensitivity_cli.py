from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .cli import _load_payload
from .normalize import normalize_payload
from .plotting import render_wacc_terminal_growth_heatmap
from .sensitivity import build_wacc_terminal_growth_sensitivity


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a WACC x terminal growth sensitivity heatmap from FP-DCF input."
    )
    parser.add_argument("--input", default="-", help="Path to the input JSON file. Use - to read from stdin.")
    parser.add_argument(
        "--output",
        default=None,
        help="Optional chart output path. Use .svg or .png for a rendered heatmap artifact.",
    )
    parser.add_argument(
        "--json-output",
        default="-",
        help="Path to write the structured sensitivity JSON summary. Use - to write to stdout.",
    )
    parser.add_argument(
        "--provider",
        choices=["yahoo", "akshare_baostock"],
        default=None,
        help="Optionally enrich missing inputs using a provider before valuation.",
    )
    parser.add_argument(
        "--cache-dir",
        default=None,
        help="Override the provider cache directory. Defaults to the local user cache path.",
    )
    parser.add_argument(
        "--refresh-provider",
        action="store_true",
        help="Force a fresh provider fetch and overwrite the cached snapshot for this request.",
    )
    parser.add_argument(
        "--metric",
        choices=["per_share_value", "equity_value", "enterprise_value"],
        default="per_share_value",
        help="Metric to visualize in the sensitivity heatmap.",
    )
    parser.add_argument(
        "--wacc-range-bps",
        type=int,
        default=200,
        help="Basis-point range above and below the base WACC to include in the heatmap.",
    )
    parser.add_argument(
        "--wacc-step-bps",
        type=int,
        default=100,
        help="Basis-point step size for the WACC axis.",
    )
    parser.add_argument(
        "--growth-range-bps",
        type=int,
        default=100,
        help="Basis-point range above and below the base terminal growth rate to include in the heatmap.",
    )
    parser.add_argument(
        "--growth-step-bps",
        type=int,
        default=50,
        help="Basis-point step size for the terminal growth axis.",
    )
    parser.add_argument("--title", default=None, help="Optional chart title override.")
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the JSON output.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        payload = _load_payload(args.input)
        payload = normalize_payload(
            payload,
            provider_override=args.provider,
            cache_dir=args.cache_dir,
            force_refresh=args.refresh_provider,
        )
        heatmap = build_wacc_terminal_growth_sensitivity(
            payload,
            metric=args.metric,
            wacc_range_bps=args.wacc_range_bps,
            wacc_step_bps=args.wacc_step_bps,
            growth_range_bps=args.growth_range_bps,
            growth_step_bps=args.growth_step_bps,
        )
        if args.output:
            render_wacc_terminal_growth_heatmap(heatmap, args.output, title=args.title)

        text = json.dumps(heatmap.to_dict(), indent=2 if args.pretty else None, ensure_ascii=False)
        if args.json_output == "-":
            sys.stdout.write(text + ("\n" if not text.endswith("\n") else ""))
        else:
            Path(args.json_output).write_text(text + "\n", encoding="utf-8")
    except Exception as exc:  # pragma: no cover - exercised via CLI tests and runtime smoke paths
        sys.stderr.write(f"fp-dcf sensitivity error: {exc}\n")
        return 2

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
