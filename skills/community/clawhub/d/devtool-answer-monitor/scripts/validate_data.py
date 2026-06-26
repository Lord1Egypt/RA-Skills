#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

from jsonschema import validate


def fail(msg):
    print(msg, file=sys.stderr)
    raise SystemExit(1)


def load_json(path):
    try:
        return json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Invalid JSON: {path} ({exc})")


def validate_query_pools(root):
    schema = load_json(root / "schemas/query-pool.schema.json")
    for path in (root / "data/query-pools").glob("*.json"):
        validate(instance=load_json(path), schema=schema)


def validate_repair(root):
    schema = load_json(root / "schemas/repair-validation.schema.json")
    for path in (root / "data/repair-validations").glob("*.json"):
        validate(instance=load_json(path), schema=schema)


def validate_summary(root):
    schema = load_json(root / "schemas/run-results.schema.json")
    for rel in [
        "data/runs/sample-run/summary.json",
        "data/runs/sciverse-sample-run/summary.json",
        "data/runs/repair-t7-run/summary.json",
        "data/runs/repair-t14-run/summary.json",
        "data/runs/multi-model-demo/summary.json",
    ]:
        path = root / rel
        if path.exists():
            validate(instance=load_json(path), schema=schema)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo-root", default=".")
    args = ap.parse_args()

    root = Path(args.repo_root).resolve()
    required = [
        root / "README.md",
        root / "README.zh-CN.md",
        root / "docs/for-beginners.md",
        root / "requirements.txt",
        root / "data/query-pools/mineru-example.json",
        root / "data/query-pools/sciverse-api-integration-example.json",
        root / "data/models.sample.json",
        root / "data/models.multi.sample.json",
        root / "data/manual.sample.json",
        root / "data/manual.multi.sample.json",
        root / "data/runs/sample-run/summary.json",
        root / "data/runs/sciverse-sample-run/summary.json",
        root / "scripts/run_monitor.py",
        root / "scripts/build_leaderboard.py",
        root / "scripts/doctor.sh",
    ]
    missing = [str(p.relative_to(root)) for p in required if not p.exists()]
    if missing:
        fail("Missing required files: " + ", ".join(missing))

    query_pool = load_json(root / "data/query-pools/mineru-example.json")
    if "project" not in query_pool or not isinstance(query_pool.get("segments"), list) or not query_pool["segments"]:
        fail("Query pool must contain 'project' and non-empty 'segments'.")

    for cfg_name in ["data/models.sample.json", "data/models.multi.sample.json"]:
        cfg = load_json(root / cfg_name)
        models = cfg.get("models")
        if not isinstance(models, list) or not models:
            fail(f"{cfg_name} must contain a non-empty models array.")
        for row in models:
            for field in ["id", "provider", "api_model"]:
                if field not in row:
                    fail(f"{cfg_name} is missing '{field}' in one model row.")

    for manual_name in ["data/manual.sample.json", "data/manual.multi.sample.json"]:
        manual = load_json(root / manual_name)
        if not isinstance(manual, dict) or not manual:
            fail(f"{manual_name} must be a non-empty object keyed by model_id::query_id.")

    validate_query_pools(root)
    validate_repair(root)
    validate_summary(root)
    print("validation passed")


if __name__ == "__main__":
    sys.exit(main())
