#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Create a fail-closed intervention packet with all observations unknown."""

from __future__ import annotations

import argparse
import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any


DIMENSIONS = (
    "provenance_integrity",
    "trust_quorum",
    "temporal_integrity",
    "structural_reachability",
    "causal_formation",
    "dimensional_consistency",
    "exact_self_maintenance",
    "finite_horizon_resource_persistence",
    "target_bound_generative_catalysis",
    "verification_capacity",
    "effective_independence",
    "coordination_protocol_integrity",
    "perturbation_robustness",
)
GATES = (
    "phase_readiness",
    "capability_reproduction",
    "residual_ratio",
    "verification_coverage",
    "resource_floor",
    "critical_unknowns",
    "hold_period",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a structurally valid, fail-closed packet. Every phase dimension "
            "and candidate gate begins unknown; no capability or ASI claim is implied."
        )
    )
    parser.add_argument("output", type=Path, help="Output JSON path.")
    parser.add_argument("--objective", required=True, help="Concrete intervention objective.")
    parser.add_argument(
        "--workspace",
        default=".",
        help="Declared workspace recorded in the packet (default: .).",
    )
    parser.add_argument(
        "--evaluation-horizon",
        default="Not yet declared.",
        help="Finite evaluation period or hold duration.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Replace an existing output file. Without this flag, overwrite is refused.",
    )
    parser.add_argument("--pretty", action="store_true", help="Indent status JSON.")
    return parser.parse_args()


def packet(args: argparse.Namespace) -> dict[str, Any]:
    unknown_assessment = {
        dimension: {
            "status": "unknown",
            "value": None,
            "evidence_refs": [],
            "rationale": "No admissible observation has been recorded.",
        }
        for dimension in DIMENSIONS
    }
    unknown_gates = {
        gate: {
            "status": "unknown",
            "criterion": "Declare a protocol-relative criterion before evaluation.",
            "evidence_refs": [],
            "rationale": "The criterion has not been evaluated.",
        }
        for gate in GATES
    }
    return {
        "schema_version": "1.0.0",
        "objective": args.objective,
        "scope": {
            "workspace": args.workspace,
            "systems": [],
            "in_scope": [],
            "out_of_scope": [
                "real-world ASI certification",
                "undeclared external systems",
            ],
            "evaluation_horizon": args.evaluation_horizon,
        },
        "authority_boundary": {
            "allowed_actions": [
                "inspect the declared workspace",
                "prepare a bounded local intervention",
                "run local validation",
            ],
            "approval_required": [
                "push",
                "release",
                "external communication",
                "destructive operation",
            ],
            "prohibited_actions": [
                "invent missing observations",
                "claim real ASI",
            ],
        },
        "phase_assessment": unknown_assessment,
        "candidate_gate": {
            "conditions": unknown_gates,
            "unknowns": [
                {
                    "id": "initial-evidence-boundary",
                    "description": "No phase evidence has been admitted.",
                    "critical": True,
                    "evidence_refs": [],
                }
            ],
            "candidate_regime": None,
        },
        "sources": {"papers": [], "repositories": []},
        "interventions": [],
        "execution": {"status": "not_executed", "actions": [], "artifacts": []},
        "rollback": {
            "available": False,
            "trigger": "No intervention has been selected.",
            "steps": [],
        },
        "validation": {"status": "not_run", "checks": []},
        "residuals": {
            "status": "unknown",
            "evidence_refs": [],
            "unresolved": ["All phase dimensions require evidence."],
        },
        "outcome_status": "planned",
        "next_binding_dimension": None,
        "non_claims": [
            "This packet is protocol-relative.",
            "It does not predict, detect, or certify real ASI.",
            "It does not prove a scientific phase transition or real-world causal effect.",
        ],
    }


def atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def emit(payload: Any, pretty: bool) -> None:
    json.dump(
        payload,
        sys.stdout,
        ensure_ascii=True,
        indent=2 if pretty else None,
        sort_keys=True,
    )
    sys.stdout.write("\n")


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def main() -> int:
    args = parse_args()
    if args.output.exists() and not args.force:
        message = (
            "output exists; use --force to replace it: "
            f"{display_path(args.output)}"
        )
        print(f"init_packet: {message}", file=sys.stderr)
        emit({"ok": False, "error": message}, args.pretty)
        return 2
    data = (
        json.dumps(packet(args), ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    try:
        atomic_write(args.output, data)
    except OSError as exc:
        message = type(exc).__name__
        print(f"init_packet: {message}", file=sys.stderr)
        emit({"ok": False, "error": message}, args.pretty)
        return 1
    emit(
        {
            "ok": True,
            "output": display_path(args.output),
            "candidate_regime": None,
            "phase_dimensions": len(DIMENSIONS),
            "next": "Replace unknowns only with evidence, then run validate_packet.py.",
        },
        args.pretty,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
