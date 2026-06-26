from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .engine import run_valuation
from .market_implied_growth import reject_removed_market_implied_blocks, resolve_market_inputs
from .normalize import normalize_payload
from .plotting import render_wacc_terminal_growth_heatmap
from .sensitivity import build_wacc_terminal_growth_sensitivity


def _load_payload(input_path: str) -> dict:
    if input_path == "-":
        raw = sys.stdin.read()
    else:
        raw = Path(input_path).read_text(encoding="utf-8")
    payload = json.loads(raw)
    if not isinstance(payload, dict):
        raise ValueError("Input JSON must decode to an object")
    return payload


def _truthy(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on"}
    return bool(value)


def _has_value(value) -> bool:
    return value not in (None, "")


def _emit_error(exc: Exception) -> int:
    sys.stderr.write(f"fp-dcf error: {exc}\n")
    return 2


def _default_chart_path(args: argparse.Namespace, payload: dict, result: dict) -> Path:
    if args.output != "-":
        output_path = Path(args.output).expanduser()
        return output_path.with_name(f"{output_path.stem}.sensitivity.svg")

    ticker = str(result.get("ticker") or payload.get("ticker") or "fp_dcf").strip().lower() or "fp_dcf"
    if args.input != "-":
        input_path = Path(args.input).expanduser()
        return Path.cwd() / f"{input_path.stem}.sensitivity.svg"
    return Path.cwd() / f"{ticker}_sensitivity.svg"


def _resolve_chart_paths(chart_path: str | Path) -> tuple[Path, Path]:
    path = Path(chart_path).expanduser()
    suffix = path.suffix.lower()

    if suffix == ".png":
        png_path = path
        svg_path = path.with_suffix(".svg")
    elif suffix == ".svg":
        svg_path = path
        png_path = path.with_suffix(".png")
    else:
        if suffix:
            path = path.with_suffix("")
        svg_path = path.with_suffix(".svg")
        png_path = path.with_suffix(".png")

    return svg_path, png_path


def _resolve_sensitivity_request(payload: dict, args: argparse.Namespace) -> dict | None:
    config = payload.get("sensitivity") or {}
    if not isinstance(config, dict):
        config = {}

    if args.no_sensitivity:
        return None

    cli_requested = any(
        [
            args.sensitivity,
            args.sensitivity_metric is not None,
            args.sensitivity_chart_output is not None,
            args.sensitivity_title is not None,
            args.sensitivity_wacc_range_bps is not None,
            args.sensitivity_wacc_step_bps is not None,
            args.sensitivity_growth_range_bps is not None,
            args.sensitivity_growth_step_bps is not None,
        ]
    )
    config_requested = any(
        [
            _has_value(config.get("enabled")),
            _has_value(config.get("metric")),
            _has_value(config.get("detail")),
            _has_value(config.get("include_grid")),
            _has_value(config.get("chart_path")),
            _has_value(config.get("title")),
            _has_value(config.get("wacc_range_bps")),
            _has_value(config.get("wacc_step_bps")),
            _has_value(config.get("growth_range_bps")),
            _has_value(config.get("growth_step_bps")),
        ]
    )

    enabled = True
    if cli_requested:
        enabled = True
    elif _has_value(config.get("enabled")):
        enabled = _truthy(config.get("enabled"))
    elif config_requested:
        enabled = True
    if not enabled:
        return None

    return {
        "metric": args.sensitivity_metric or config.get("metric"),
        "detail": _truthy(config.get("detail")) or _truthy(config.get("include_grid")),
        "chart_path": args.sensitivity_chart_output or config.get("chart_path"),
        "title": args.sensitivity_title or config.get("title"),
        "wacc_range_bps": args.sensitivity_wacc_range_bps
        if args.sensitivity_wacc_range_bps is not None
        else int(config.get("wacc_range_bps") or 200),
        "wacc_step_bps": args.sensitivity_wacc_step_bps
        if args.sensitivity_wacc_step_bps is not None
        else int(config.get("wacc_step_bps") or 100),
        "growth_range_bps": args.sensitivity_growth_range_bps
        if args.sensitivity_growth_range_bps is not None
        else int(config.get("growth_range_bps") or 100),
        "growth_step_bps": args.sensitivity_growth_step_bps
        if args.sensitivity_growth_step_bps is not None
        else int(config.get("growth_step_bps") or 50),
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run a first-principles DCF valuation from JSON input.")
    parser.add_argument("--input", default="-", help="Path to the input JSON file. Use - to read from stdin.")
    parser.add_argument("--output", default="-", help="Path to write output JSON. Use - to write to stdout.")
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
        "--sensitivity",
        action="store_true",
        help="Explicitly include a WACC x terminal growth sensitivity grid in the output JSON. This is enabled by default.",
    )
    parser.add_argument(
        "--no-sensitivity",
        action="store_true",
        help="Disable the default WACC x terminal growth sensitivity grid.",
    )
    parser.add_argument(
        "--sensitivity-metric",
        choices=["per_share_value", "equity_value", "enterprise_value"],
        default=None,
        help="Metric to use when generating the default sensitivity summary.",
    )
    parser.add_argument(
        "--sensitivity-chart-output",
        default=None,
        help=(
            "Override the default rendered sensitivity chart base path. "
            "By default FP-DCF writes a sibling *.sensitivity.svg next to --output, "
            "or a cwd-based fallback path when writing JSON to stdout. "
            "FP-DCF also writes a sibling PNG beside the SVG."
        ),
    )
    parser.add_argument(
        "--sensitivity-title",
        default=None,
        help="Optional chart title override for the rendered sensitivity heatmap.",
    )
    parser.add_argument(
        "--sensitivity-wacc-range-bps",
        type=int,
        default=None,
        help="Basis-point range above and below base WACC for the default sensitivity chart.",
    )
    parser.add_argument(
        "--sensitivity-wacc-step-bps",
        type=int,
        default=None,
        help="Basis-point step size for the default WACC sensitivity axis.",
    )
    parser.add_argument(
        "--sensitivity-growth-range-bps",
        type=int,
        default=None,
        help="Basis-point range above and below base terminal growth for the default sensitivity chart.",
    )
    parser.add_argument(
        "--sensitivity-growth-step-bps",
        type=int,
        default=None,
        help="Basis-point step size for the default terminal growth sensitivity axis.",
    )
    parser.add_argument("--pretty", action="store_true", help="Pretty-print the output JSON.")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        payload = _load_payload(args.input)
        reject_removed_market_implied_blocks(payload)
        payload = normalize_payload(
            payload,
            provider_override=args.provider,
            cache_dir=args.cache_dir,
            force_refresh=args.refresh_provider,
        )
        valuation_output = run_valuation(payload)
        result = valuation_output.to_dict()
        market_inputs = None
        if valuation_output.market_implied_growth is not None:
            market_inputs = resolve_market_inputs(payload)
            result["market_inputs"] = market_inputs.to_dict()

        sensitivity_request = _resolve_sensitivity_request(payload, args)
        if sensitivity_request is not None:
            requested_metric = sensitivity_request["metric"]
            metric_candidates = (
                [requested_metric]
                if requested_metric
                else ["per_share_value", "equity_value", "enterprise_value"]
            )
            market_price = None
            if market_inputs is not None and market_inputs.market_price is not None:
                market_price = market_inputs.market_price
            elif valuation_output.market_implied_growth is not None:
                market_price = valuation_output.market_implied_growth.market_price
            sensitivity = None
            last_exc: Exception | None = None
            for metric in metric_candidates:
                try:
                    sensitivity = build_wacc_terminal_growth_sensitivity(
                        payload,
                        metric=metric,
                        market_price=market_price,
                        wacc_range_bps=sensitivity_request["wacc_range_bps"],
                        wacc_step_bps=sensitivity_request["wacc_step_bps"],
                        growth_range_bps=sensitivity_request["growth_range_bps"],
                        growth_step_bps=sensitivity_request["growth_step_bps"],
                    )
                except ValueError as exc:
                    last_exc = exc
                    continue
                else:
                    if requested_metric is None and metric != "per_share_value":
                        sensitivity.diagnostics.append(f"sensitivity_metric_auto_fallback:{metric}")
                    break
            if sensitivity is None:
                raise last_exc or ValueError("Unable to build sensitivity output")
            result["sensitivity"] = sensitivity.to_summary_dict(
                include_grid=sensitivity_request["detail"],
                exclude_diagnostics=set(result.get("diagnostics") or []),
                exclude_warnings=set(result.get("warnings") or []),
            )

            chart_path = sensitivity_request["chart_path"] or _default_chart_path(args, payload, result)
            if chart_path:
                svg_path, png_path = _resolve_chart_paths(chart_path)
                rendered_svg_path = render_wacc_terminal_growth_heatmap(
                    sensitivity,
                    svg_path,
                    title=sensitivity_request["title"],
                )
                rendered_png_path = render_wacc_terminal_growth_heatmap(
                    sensitivity,
                    png_path,
                    title=sensitivity_request["title"],
                )
                artifacts = dict(result.get("artifacts") or {})
                artifacts["sensitivity_heatmap_path"] = str(rendered_png_path)
                artifacts["sensitivity_heatmap_svg_path"] = str(rendered_svg_path)
                result["artifacts"] = artifacts

        text = json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False)
        if args.output == "-":
            sys.stdout.write(text + ("\n" if not text.endswith("\n") else ""))
        else:
            Path(args.output).write_text(text + "\n", encoding="utf-8")
    except Exception as exc:  # pragma: no cover - exercised via CLI smoke test
        return _emit_error(exc)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
