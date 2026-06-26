from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Dict, Optional


def _ensure_src_on_path() -> None:
    # 该脚本在 scripts/ 下，skill 根目录的 src 需要加入搜索路径。
    skill_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    src_dir = os.path.join(skill_root, "src")
    if src_dir not in sys.path:
        sys.path.insert(0, src_dir)


def _load_toml(path: str) -> Dict[str, Any]:
    try:
        import tomllib  # py3.11+
    except Exception:
        import tomli as tomllib  # type: ignore
    with open(path, "rb") as f:
        return tomllib.load(f)


def main() -> int:
    _ensure_src_on_path()
    from fluid_network.schema import parse_toml_network
    from fluid_network.solver import FluidNetworkSolver
    from fluid_network.path_analyzer import assess_connectivity_and_reliability

    parser = argparse.ArgumentParser(description="Solve fluid network scenarios and analyze reliability.")
    parser.add_argument("--input", "-i", required=True, help="Path to network TOML file.")
    parser.add_argument("--scenario", "-s", default="", help="Scenario id to run (default: all).")
    parser.add_argument("--format", "-f", default="markdown", choices=["markdown", "json"], help="Output format.")
    parser.add_argument("--output", "-o", default="", help="Optional output file path.")
    args = parser.parse_args()

    toml_data = _load_toml(args.input)
    network = parse_toml_network(toml_data)
    if not network.scenarios:
        # Allow a synthetic default scenario with empty variables.
        from fluid_network.schema import Scenario

        network.scenarios = [Scenario(id="default")]

    chosen = [sc for sc in network.scenarios if (not args.scenario) or sc.id == args.scenario]
    if not chosen:
        raise SystemExit(f"No scenario matched id={args.scenario!r}")

    solver = FluidNetworkSolver(network)
    reports_md = []
    reports_json: Dict[str, Any] = {"scenarios": {}}

    for sc in chosen:
        sol = solver.solve(sc)
        assessment = assess_connectivity_and_reliability(network, sc, sol)

        if args.format == "markdown":
            reports_md.append(f"## Scenario: {sc.id}")

            reachable = ", ".join(assessment.reachable_node_ids) if assessment.reachable_node_ids else "(none)"
            reports_md.append(f"### Connectivity")
            reports_md.append(f"- Reachable nodes from sources: {reachable}")

            reports_md.append("### Edge results")
            for eid, er in sol.edge_results.items():
                vel = f"{er.velocity_m_per_s:.6g} m/s" if er.velocity_m_per_s is not None else "n/a"
                reports_md.append(
                    f"- {eid}: enabled={er.enabled}, Q={er.flow_m3s:.6g} m3/s, "
                    f"v={vel}, dP={er.delta_p_pa:.6g} Pa, R_eff={er.effective_R:.6g}"
                )

            reports_md.append("### Function reliability")
            for fn in assessment.functions:
                status = "PASS" if fn.function_pass else "FAIL"
                reports_md.append(f"- {fn.function_id}: {status}")
                for load in fn.loads:
                    ok = "PASS" if (load.connected and load.pass_threshold) else "FAIL"
                    reports_md.append(
                        f"  - Load {load.load_node_id}: {ok}, connected={load.connected}, "
                        f"p={load.pressure_pa:.6g} Pa, flow={load.flow_m3s:.6g} m3/s"
                    )
        else:
            # JSON
            reports_json["scenarios"][sc.id] = {
                "node_pressures_pa": sol.node_pressures_pa,
                "edge_results": {
                    eid: {
                        "enabled": er.enabled,
                        "effective_R": er.effective_R,
                        "flow_m3s": er.flow_m3s,
                        "velocity_m_per_s": er.velocity_m_per_s,
                        "delta_p_pa": er.delta_p_pa,
                    }
                    for eid, er in sol.edge_results.items()
                },
                "reachable_node_ids": list(assessment.reachable_node_ids),
                "functions": [
                    {
                        "function_id": fn.function_id,
                        "function_pass": fn.function_pass,
                        "loads": [
                            {
                                "load_node_id": ld.load_node_id,
                                "connected": ld.connected,
                                "pass_threshold": ld.pass_threshold,
                                "pressure_pa": ld.pressure_pa,
                                "flow_m3s": ld.flow_m3s,
                            }
                            for ld in fn.loads
                        ],
                    }
                    for fn in assessment.functions
                ],
            }

    if args.format == "markdown":
        md = "# Fluid Network Scenario Report\n\n" + "\n".join(reports_md) + "\n"
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(md)
        print(md)
    else:
        payload = json.dumps(reports_json, ensure_ascii=False, indent=2)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f:
                f.write(payload)
        print(payload)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())

