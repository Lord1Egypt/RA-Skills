"""
Binary eval suite for the Dialogflow CX → CES migration skill.
Each eval returns True (pass) or False (fail).
Used by autoresearch loop.

Run standalone:
    python evals.py --output-dir ./migration_output
"""

import json
import csv
import argparse
import sys
from pathlib import Path


def eval_flows(output_dir: Path) -> tuple[bool, str]:
    """EVAL_FLOWS: All non-default flows appear as sub-agents."""
    ces = output_dir / "ces_agent.json"
    if not ces.exists():
        return False, "ces_agent.json not found"
    data = json.loads(ces.read_text(encoding="utf-8"))
    agents = data.get("agents", [])
    if len(agents) == 0:
        return False, f"No sub-agents found in ces_agent.json (expected ≥1)"
    return True, f"{len(agents)} sub-agents found"


def eval_tools(output_dir: Path) -> tuple[bool, str]:
    """EVAL_TOOLS: All webhooks appear as tools with OpenAPI schemas."""
    ces = output_dir / "ces_agent.json"
    if not ces.exists():
        return False, "ces_agent.json not found"
    data = json.loads(ces.read_text(encoding="utf-8"))
    tools = data.get("tools", [])
    if len(tools) == 0:
        return False, "No tools found in ces_agent.json"
    for t in tools:
        if "openapiTool" not in t:
            return False, f"Tool '{t.get('displayName')}' missing openapiTool schema"
        if "textSchema" not in t["openapiTool"]:
            return False, f"Tool '{t.get('displayName')}' missing textSchema"
    return True, f"{len(tools)} tools with OpenAPI schemas found"


def eval_entities(output_dir: Path) -> tuple[bool, str]:
    """EVAL_ENTITIES: Entity types exported to entity_types.json."""
    et = output_dir / "entity_types.json"
    if not et.exists():
        return False, "entity_types.json not found"
    data = json.loads(et.read_text(encoding="utf-8"))
    if len(data) == 0:
        return False, "entity_types.json is empty"
    for e in data:
        if "name" not in e or "entities" not in e:
            return False, f"Entity type missing 'name' or 'entities' field: {e}"
    return True, f"{len(data)} entity types exported"


def eval_evals_csv(output_dir: Path) -> tuple[bool, str]:
    """EVAL_EVALS_CSV: golden_evals.csv has correct header + ≥1 eval row."""
    csv_path = output_dir / "golden_evals.csv"
    if not csv_path.exists():
        return False, "golden_evals.csv not found"
    with open(csv_path, encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required_headers = {"display_name", "turn_index", "action_type"}
        actual = set(reader.fieldnames or [])
        missing = required_headers - actual
        if missing:
            return False, f"golden_evals.csv missing required columns: {missing}"
        rows = list(reader)
        eval_rows = [r for r in rows if r.get("display_name", "").strip()]
        if len(eval_rows) == 0:
            return False, "golden_evals.csv has header but no evaluation rows"
    return True, f"{len(eval_rows)} evaluation(s) found in CSV"


def eval_instructions(output_dir: Path) -> tuple[bool, str]:
    """EVAL_INSTRUCTIONS: Each sub-agent has non-empty instructions."""
    ces = output_dir / "ces_agent.json"
    if not ces.exists():
        return False, "ces_agent.json not found"
    data = json.loads(ces.read_text(encoding="utf-8"))
    agents = data.get("agents", [])
    if not agents:
        return False, "No sub-agents to check"
    empty = [a["displayName"] for a in agents if not a.get("instruction", "").strip()]
    if empty:
        return False, f"Sub-agents with empty instructions: {empty}"
    return True, f"All {len(agents)} sub-agents have instructions"


def eval_report(output_dir: Path) -> tuple[bool, str]:
    """EVAL_REPORT: migration_report.md exists with stats table."""
    report = output_dir / "migration_report.md"
    if not report.exists():
        return False, "migration_report.md not found"
    content = report.read_text(encoding="utf-8")
    if "Migration Stats" not in content:
        return False, "migration_report.md missing 'Migration Stats' section"
    if "Next Steps" not in content:
        return False, "migration_report.md missing 'Next Steps' section"
    return True, "migration_report.md complete"


EVALS = [
    ("EVAL_FLOWS",        eval_flows),
    ("EVAL_TOOLS",        eval_tools),
    ("EVAL_ENTITIES",     eval_entities),
    ("EVAL_EVALS_CSV",    eval_evals_csv),
    ("EVAL_INSTRUCTIONS", eval_instructions),
    ("EVAL_REPORT",       eval_report),
]


def run_all(output_dir: Path) -> dict:
    results = {}
    passed = 0
    print(f"\n{'='*60}")
    print(f"Eval Suite: {output_dir}")
    print(f"{'='*60}")
    for name, fn in EVALS:
        ok, msg = fn(output_dir)
        results[name] = {"pass": ok, "msg": msg}
        status = "PASS" if ok else "FAIL"
        print(f"{status}  {name}: {msg}")
        if ok:
            passed += 1
    score = passed / len(EVALS)
    print(f"{'='*60}")
    print(f"Score: {passed}/{len(EVALS)} = {score:.0%}")
    print(f"{'='*60}\n")
    results["_score"] = {"passed": passed, "total": len(EVALS), "pct": score}
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run binary evals on migration output")
    parser.add_argument("--output-dir", default="./migration_output", help="Migration output directory")
    args = parser.parse_args()

    results = run_all(Path(args.output_dir))
    sys.exit(0 if results["_score"]["passed"] == results["_score"]["total"] else 1)
