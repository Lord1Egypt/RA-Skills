#!/usr/bin/env python3
import argparse
import csv
import json
import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
NORMALIZE = SCRIPT_DIR / "normalize_bills.py"
PRECHECK = SCRIPT_DIR / "import_precheck.py"
EXPORT = SCRIPT_DIR / "export_feishu_import_csv.py"
WRITE = SCRIPT_DIR / "write_feishu_records.py"
DEFAULT_APP_TOKEN = os.getenv("FAMILY_BOOKKEEPING_APP_TOKEN", "")
DEFAULT_TABLE_ID = os.getenv("FAMILY_BOOKKEEPING_TABLE_ID", "")


def run(cmd, env=None):
    proc = subprocess.run(cmd, text=True, capture_output=True, env=env)
    if proc.returncode != 0:
        sys.stderr.write(proc.stderr or proc.stdout)
        raise SystemExit(proc.returncode)
    return proc.stdout


def count_csv_rows(path: Path) -> int:
    if not path.exists():
        return 0
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    return max(len(rows) - 1, 0)


def main():
    parser = argparse.ArgumentParser(description="End-to-end family bookkeeping bill import pipeline.")
    parser.add_argument("input", help="Path to exported WeChat/Alipay bill file (.csv/.xlsx) or normalized .json/.csv")
    parser.add_argument("--bookkeeper", default="", help="Default 记账人 for normalization stage")
    parser.add_argument("--platform", choices=["wechat", "alipay"], help="Override platform detection during normalization")
    parser.add_argument("--normalized-input", action="store_true", help="Treat input as already normalized .json/.csv and skip normalize step")
    parser.add_argument("--app-token", default=DEFAULT_APP_TOKEN, help="Feishu Bitable app token")
    parser.add_argument("--table-id", default=DEFAULT_TABLE_ID, help="Feishu Bitable table id")
    parser.add_argument("--app-id", default=os.getenv("FEISHU_APP_ID", ""), help="Feishu app id (or FEISHU_APP_ID env)")
    parser.add_argument("--app-secret", default=os.getenv("FEISHU_APP_SECRET", ""), help="Feishu app secret (or FEISHU_APP_SECRET env)")
    parser.add_argument("--workdir", help="Output working directory. Default: ./family-import-<input-stem>")
    parser.add_argument("--write", action="store_true", help="After precheck, directly write new rows into Feishu Bitable")
    parser.add_argument("--write-limit", type=int, help="Only write first N new rows")
    args = parser.parse_args()

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        raise SystemExit(f"Input file not found: {input_path}")

    workdir = Path(args.workdir).resolve() if args.workdir else (Path.cwd() / f"family-import-{input_path.stem}").resolve()
    workdir.mkdir(parents=True, exist_ok=True)

    normalized_path = workdir / ("normalized.json" if not args.normalized_input else input_path.name)
    precheck_dir = workdir / "precheck"
    precheck_dir.mkdir(parents=True, exist_ok=True)
    final_import_csv = workdir / "feishu-import-new-records.csv"

    env = os.environ.copy()
    if args.app_id:
        env["FEISHU_APP_ID"] = args.app_id
    if args.app_secret:
        env["FEISHU_APP_SECRET"] = args.app_secret

    steps = []

    if args.normalized_input:
        if input_path.suffix.lower() not in {".json", ".csv"}:
            raise SystemExit("--normalized-input requires .json or .csv input")
        if input_path.resolve() != normalized_path.resolve():
            normalized_path.write_bytes(input_path.read_bytes())
        steps.append({"step": "normalize", "status": "skipped", "reason": "normalized input supplied"})
    else:
        cmd = [sys.executable, str(NORMALIZE), str(input_path), "--format", "json", "--output", str(normalized_path)]
        if args.bookkeeper:
            cmd.extend(["--bookkeeper", args.bookkeeper])
        if args.platform:
            cmd.extend(["--platform", args.platform])
        out = run(cmd, env=env)
        steps.append({"step": "normalize", "status": "ok", "stdout": out.strip()})

    cmd = [
        sys.executable,
        str(PRECHECK),
        str(normalized_path),
        "--app-token", args.app_token,
        "--table-id", args.table_id,
        "--output-dir", str(precheck_dir),
    ]
    if args.app_id:
        cmd.extend(["--app-id", args.app_id])
    if args.app_secret:
        cmd.extend(["--app-secret", args.app_secret])
    precheck_out = run(cmd, env=env)
    steps.append({"step": "precheck", "status": "ok", "stdout": precheck_out.strip()})

    new_records_csv = precheck_dir / "new_records.csv"
    export_out = run([sys.executable, str(EXPORT), str(new_records_csv), "--output", str(final_import_csv)], env=env)
    steps.append({"step": "export_feishu_csv", "status": "ok", "stdout": export_out.strip()})

    if args.write:
        cmd = [
            sys.executable,
            str(WRITE),
            str(new_records_csv),
            "--app-token", args.app_token,
            "--table-id", args.table_id,
        ]
        if args.app_id:
            cmd.extend(["--app-id", args.app_id])
        if args.app_secret:
            cmd.extend(["--app-secret", args.app_secret])
        if args.write_limit:
            cmd.extend(["--limit", str(args.write_limit)])
        write_out = run(cmd, env=env)
        steps.append({"step": "write_feishu_records", "status": "ok", "stdout": write_out.strip()})

    summary_path = precheck_dir / "import_summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8")) if summary_path.exists() else {}
    result = {
        "input": str(input_path),
        "workdir": str(workdir),
        "normalized": str(normalized_path),
        "precheck_dir": str(precheck_dir),
        "new_records_csv": str(new_records_csv),
        "duplicate_records_csv": str(precheck_dir / "duplicate_records.csv"),
        "feishu_import_csv": str(final_import_csv),
        "new_records_count": count_csv_rows(new_records_csv),
        "duplicate_records_count": count_csv_rows(precheck_dir / "duplicate_records.csv"),
        "write_enabled": args.write,
        "summary": summary,
        "steps": steps,
    }

    (workdir / "pipeline_result.json").write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
