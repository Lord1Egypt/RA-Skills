from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path
from typing import Any

try:
    from .analyzer import analyze_solution
    from .models import AnalysisReport, apply_scenario, load_system_config
    from .solver import solve_system
except ImportError:  # pragma: no cover
    from analyzer import analyze_solution
    from models import AnalysisReport, apply_scenario, load_system_config
    from solver import solve_system


NETWORK_TEMPLATE = """[system]
name = "Template Cooling Network"
fluid_density = 998.2
description = "Closed-loop template with one supply source and one return sink."

[[nodes]]
id = "pump_1"
type = "source"
fixed_pressure = 500000.0

[[nodes]]
id = "manifold_1"
type = "junction"

[[nodes]]
id = "process_load_1"
type = "load"
min_pressure = 120000.0
min_flow = 0.0025

[[nodes]]
id = "return_header"
type = "sink"
fixed_pressure = 0.0

[[pipes]]
id = "supply_main"
source = "pump_1"
target = "manifold_1"
resistance = 1.2e10
diameter = 0.05
valve_open = true

[[pipes]]
id = "load_branch"
source = "manifold_1"
target = "process_load_1"
resistance = 1.8e10
diameter = 0.04
valve_open = true

[[pipes]]
id = "return_branch"
source = "process_load_1"
target = "return_header"
resistance = 1.4e10
diameter = 0.04
valve_open = true

[[scenarios]]
name = "Normal_Operation"
description = "Nominal operating condition."
[scenarios.overrides]

[[scenarios]]
name = "Pump_Degradation"
description = "Pump discharge pressure drops under wear."
[scenarios.overrides.nodes]
pump_1 = { fixed_pressure = 360000.0 }

[[scenarios]]
name = "Valve_Closed_Fault"
description = "The branch valve is unexpectedly closed."
[scenarios.overrides.pipes]
load_branch = { valve_open = false }
"""


def generate_network_template(filepath: str) -> str:
    """Generate a starter TOML network file that follows the documented schema.

    Args:
        filepath: Destination file path for the generated TOML template.

    Returns:
        The absolute path of the written template file.
    """

    output_path = Path(filepath).resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(NETWORK_TEMPLATE, encoding="utf-8")
    return str(output_path)


def execute_scenario_analysis(toml_filepath: str, scenario_name: str) -> dict[str, Any]:
    """Run parsing, scenario application, solving, and reliability analysis.

    Args:
        toml_filepath: Absolute or relative path to the network TOML file.
        scenario_name: Scenario name to analyze. Use ``base`` for the raw configuration.

    Returns:
        A JSON-serializable report dictionary.
    """

    report = _run_analysis(toml_filepath, scenario_name)
    return asdict(report)


def execute_all_scenarios_analysis(toml_filepath: str, include_base: bool = True) -> dict[str, Any]:
    """Run the analysis pipeline for every scenario in a TOML file.

    Args:
        toml_filepath: Absolute or relative path to the network TOML file.
        include_base: Whether to analyze the unmodified base configuration first.

    Returns:
        A JSON-serializable dictionary containing every scenario report.
    """

    config = load_system_config(toml_filepath)
    scenario_names = config.scenario_names(include_base=include_base)
    reports = [_run_analysis(toml_filepath, scenario_name) for scenario_name in scenario_names]
    return {
        "system_name": config.name,
        "scenario_count": len(reports),
        "reports": [asdict(report) for report in reports],
    }


def render_report_markdown(report_data: AnalysisReport | dict[str, Any]) -> str:
    """Render an analysis report as readable Markdown."""

    report = asdict(report_data) if isinstance(report_data, AnalysisReport) else dict(report_data)
    lines = [
        f"# {report['system_name']} - {report['scenario_name']}",
        "",
        f"- Scenario description: {report['scenario_description'] or 'N/A'}",
        f"- Solver method: {report['solver']['method']}",
        f"- Solver converged: {report['solver']['converged']}",
        f"- Residual norm: {report['solver']['residual_norm']:.6e}",
        f"- Connected components: {report['connectivity']['component_count']}",
        "",
        "## Load Assessments",
    ]

    for load in report["loads"]:
        lines.extend(
            [
                f"- `{load['node_id']}`: operational={load['operational']}, "
                f"pressure={load['pressure']:.6f}, inflow={load['inflow']:.6f}",
                f"  connected_sources={load['connected_sources']}, "
                f"path={load['topology_path_pipe_ids']}, alarms={load['alarms']}",
            ]
        )

    lines.extend(["", "## Pipe States"])
    for pipe_id, pipe_state in sorted(report["solver"]["pipe_states"].items()):
        velocity = pipe_state["velocity"]
        velocity_text = "None" if velocity is None else f"{velocity:.6f}"
        lines.append(
            f"- `{pipe_id}`: active={pipe_state['active']}, flow={pipe_state['flow']:.6f}, "
            f"velocity={velocity_text}, pressure_drop={pipe_state['pressure_drop']:.6f}"
        )

    if report["alarms"]:
        lines.extend(["", "## Alarms"])
        lines.extend(f"- {alarm}" for alarm in report["alarms"])

    return "\n".join(lines)


def _run_analysis(toml_filepath: str, scenario_name: str) -> AnalysisReport:
    base_config = load_system_config(toml_filepath)
    scoped_config = apply_scenario(base_config, scenario_name)
    scenario_description = ""
    if scenario_name != "base":
        scenario_description = base_config.scenarios[scenario_name].description
    solver_result = solve_system(scoped_config, scenario_name=scenario_name)
    return analyze_solution(
        scoped_config,
        solver_result,
        scenario_name=scenario_name,
        scenario_description=scenario_description,
    )


def _write_output(output_path: str | None, content: str) -> None:
    if output_path is None:
        print(content)
        return
    path = Path(output_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    """CLI entry point for template generation and scenario analysis."""

    parser = argparse.ArgumentParser(description="Fluid network solver skill tools.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    template_parser = subparsers.add_parser("template", help="Generate a TOML network template.")
    template_parser.add_argument("--output", required=True, help="Output TOML file path.")

    analyze_parser = subparsers.add_parser("analyze", help="Analyze a single scenario.")
    analyze_parser.add_argument("--toml", required=True, help="Path to the network TOML file.")
    analyze_parser.add_argument("--scenario", default="base", help="Scenario name to analyze.")
    analyze_parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    analyze_parser.add_argument("--output", help="Optional file to write the rendered result.")

    analyze_all_parser = subparsers.add_parser("analyze-all", help="Analyze every scenario.")
    analyze_all_parser.add_argument("--toml", required=True, help="Path to the network TOML file.")
    analyze_all_parser.add_argument(
        "--format",
        choices=("json", "markdown"),
        default="json",
        help="Output format.",
    )
    analyze_all_parser.add_argument("--output", help="Optional file to write the rendered result.")

    args = parser.parse_args()

    if args.command == "template":
        path = generate_network_template(args.output)
        print(path)
        return

    if args.command == "analyze":
        report = _run_analysis(args.toml, args.scenario)
        if args.format == "markdown":
            _write_output(args.output, render_report_markdown(report))
        else:
            _write_output(args.output, json.dumps(asdict(report), ensure_ascii=False, indent=2))
        return

    results = execute_all_scenarios_analysis(args.toml)
    if args.format == "markdown":
        markdown_blocks = [render_report_markdown(report) for report in results["reports"]]
        _write_output(args.output, "\n\n".join(markdown_blocks))
    else:
        _write_output(args.output, json.dumps(results, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
