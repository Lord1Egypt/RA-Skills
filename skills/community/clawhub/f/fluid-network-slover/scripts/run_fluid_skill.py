from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from skill_tools import (  # noqa: E402
    execute_all_scenarios_analysis,
    execute_scenario_analysis,
    generate_network_template,
    render_report_markdown,
)


def _build_summary_table(reports: list[dict[str, Any]]) -> str:
    lines = [
        "| Scenario | Converged | Method | Components | Operational Loads |",
        "|---|---:|---|---:|---:|",
    ]
    for report in reports:
        load_total = len(report["loads"])
        load_passed = sum(1 for load in report["loads"] if load["operational"])
        lines.append(
            f"| {report['scenario_name']} | {report['solver']['converged']} | "
            f"{report['solver']['method']} | {report['connectivity']['component_count']} | "
            f"{load_passed}/{load_total} |"
        )
    return "\n".join(lines)


def _render_report_template(
    template_path: Path,
    toml_path: Path,
    mode: str,
    reports: list[dict[str, Any]],
) -> str:
    template = template_path.read_text(encoding="utf-8")
    detail_sections = "\n\n".join(render_report_markdown(report) for report in reports)
    return (
        template.replace("{{generated_at_utc}}", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"))
        .replace("{{input_file}}", str(toml_path))
        .replace("{{scenario_mode}}", mode)
        .replace("{{scenario_count}}", str(len(reports)))
        .replace("{{summary_table}}", _build_summary_table(reports))
        .replace("{{detail_sections}}", detail_sections)
    )


def _write_output(path_text: str | None, content: str) -> None:
    if path_text is None:
        return
    path = Path(path_text).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Clawhub-ready entry point for the fluid network solver skill.")
    parser.add_argument("--toml", help="Path to the network TOML file.")
    parser.add_argument("--scenario", default="base", help="Scenario name when not using --all-scenarios.")
    parser.add_argument("--all-scenarios", action="store_true", help="Analyze base plus all named scenarios.")
    parser.add_argument(
        "--report-template",
        default=str((SCRIPT_DIR.parent / "assets" / "report_template.md").resolve()),
        help="Path to the report template markdown file.",
    )
    parser.add_argument("--report-out", help="Optional output path for the rendered markdown report.")
    parser.add_argument("--json-out", help="Optional output path for the JSON result.")
    parser.add_argument("--print-text", action="store_true", help="Print a readable markdown summary to stdout.")
    parser.add_argument("--generate-template", help="Write a starter TOML template and exit.")
    args = parser.parse_args()

    if args.generate_template:
        generated = generate_network_template(args.generate_template)
        print(generated)
        return

    if not args.toml:
        parser.error("--toml is required unless --generate-template is used.")

    toml_path = Path(args.toml).resolve()
    template_path = Path(args.report_template).resolve()

    if args.all_scenarios:
        result_payload = execute_all_scenarios_analysis(str(toml_path))
        reports = list(result_payload["reports"])
        mode = "all-scenarios"
    else:
        single_report = execute_scenario_analysis(str(toml_path), args.scenario)
        result_payload = single_report
        reports = [single_report]
        mode = f"single:{args.scenario}"

    if args.print_text:
        print("\n\n".join(render_report_markdown(report) for report in reports))

    if args.json_out:
        _write_output(args.json_out, json.dumps(result_payload, ensure_ascii=False, indent=2))

    if args.report_out:
        rendered_report = _render_report_template(template_path, toml_path, mode, reports)
        _write_output(args.report_out, rendered_report)


if __name__ == "__main__":
    main()
