#!/usr/bin/env python3
import argparse
import subprocess
from pathlib import Path


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", help="Input inbox JSONL")
    ap.add_argument("--work-dir", default=".learnings", help="Working directory for pipeline outputs")
    ap.add_argument("--base-dir", help="Base dir for apply step")
    ap.add_argument("--dry-run", action="store_true", help="Use dry-run for apply step")
    ap.add_argument("--apply", action="store_true", help="Run apply step after draft/review state exists")
    ap.add_argument("--archive-input", action="store_true", help="Archive input inbox after pipeline completes")
    args = ap.parse_args()

    script_dir = Path(__file__).resolve().parent
    work_dir = Path(args.work_dir)
    work_dir.mkdir(parents=True, exist_ok=True)

    scored = work_dir / "scored.jsonl"
    merge = work_dir / "merge.json"
    consolidated = work_dir / "consolidated.jsonl"
    backlog = work_dir / "backlog.json"
    backlog_aged = work_dir / "backlog-aged.json"
    patches = work_dir / "patches.json"
    conflicts = work_dir / "conflicts.json"
    promotions = work_dir / "existing-promotions.json"
    report = work_dir / "apply-report.json"

    run(["python3", str(script_dir / "score_learnings.py"), args.input, "-o", str(scored)])
    run(["python3", str(script_dir / "merge_candidates.py"), str(scored), "-o", str(merge)])
    run(["python3", str(script_dir / "consolidate_learnings.py"), str(scored), str(merge), "-o", str(consolidated)])
    run(["python3", str(script_dir / "build_backlog.py"), str(consolidated), "-o", str(backlog)])
    run(["python3", str(script_dir / "age_backlog.py"), str(backlog), str(consolidated), "-o", str(backlog_aged)])
    run(["python3", str(script_dir / "draft_patches.py"), str(consolidated), "-o", str(patches)])
    run(["python3", str(script_dir / "detect_patch_conflicts.py"), str(patches), "-o", str(conflicts)])

    if args.base_dir:
        run(["python3", str(script_dir / "check_existing_promotions.py"), str(patches), "--base-dir", args.base_dir, "-o", str(promotions)])

    if args.apply:
        if not args.base_dir:
            raise SystemExit("--base-dir is required with --apply")
        cmd = [
            "python3", str(script_dir / "apply_approved_patches.py"),
            str(patches), "--base-dir", args.base_dir, "-o", str(report)
        ]
        if args.dry_run:
            cmd.append("--dry-run")
        run(cmd)

    if args.archive_input:
        run([
            "python3", str(script_dir / "archive_batch.py"),
            args.input, "--archive-dir", str(work_dir / "archive")
        ])

    print(f"Pipeline complete. Outputs in {work_dir}")


if __name__ == "__main__":
    main()
