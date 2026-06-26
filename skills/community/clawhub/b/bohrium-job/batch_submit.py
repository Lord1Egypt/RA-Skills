"""
Batch submit jobs to Bohrium with the same config but different input directories.

Usage:
    python batch_submit.py --project_id 154 --input_dirs exp1/ exp2/ exp3/
    python batch_submit.py --project_id 154 --input_dirs exp*/ --group "batch-run"
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def create_job_group(name: str, project_id: int) -> str | None:
    """Create a job group and return the group ID."""
    result = subprocess.run(
        ["bohr", "job_group", "create", "-n", name, "-p", str(project_id)],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(f"[WARN] Failed to create job group: {result.stderr.strip()}")
        return None
    # Parse group ID from output
    for line in result.stdout.strip().splitlines():
        if "JobGroupId" in line or "job_group_id" in line:
            return line.split(":")[-1].strip()
    print(f"[INFO] Job group output: {result.stdout.strip()}")
    return None


def submit_job(
    job_json: Path,
    input_dir: Path,
    job_name: str | None = None,
    group_id: str | None = None,
    result_path: str | None = None,
) -> bool:
    """Submit a single job."""
    cmd = ["bohr", "job", "submit", "-i", str(job_json), "-p", str(input_dir)]
    if job_name:
        cmd.extend(["-n", job_name])
    if group_id:
        cmd.extend(["-g", group_id])
    if result_path:
        cmd.extend(["-r", result_path])

    print(f"[SUBMIT] {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"  -> {result.stdout.strip()}")
        return True
    else:
        print(f"  -> FAILED: {result.stderr.strip()}")
        return False


def main():
    parser = argparse.ArgumentParser(description="Batch submit Bohrium jobs")
    parser.add_argument(
        "--job_json",
        type=Path,
        default=Path("job.json"),
        help="Path to job.json template (default: job.json)",
    )
    parser.add_argument(
        "--project_id",
        type=int,
        required=True,
        help="Project ID",
    )
    parser.add_argument(
        "--input_dirs",
        type=Path,
        nargs="+",
        required=True,
        help="Input directories, one job per directory",
    )
    parser.add_argument(
        "--group",
        type=str,
        default=None,
        help="Create a job group with this name and add all jobs to it",
    )
    parser.add_argument(
        "--result_path",
        type=str,
        default=None,
        help="Auto-download results to this path (e.g. /personal/results)",
    )
    args = parser.parse_args()

    if not args.job_json.exists():
        print(f"[ERROR] job.json not found: {args.job_json}")
        sys.exit(1)

    # Update project_id in job.json
    with open(args.job_json) as f:
        config = json.load(f)
    config["project_id"] = args.project_id
    tmp_json = Path("/tmp/bohrium_batch_job.json")
    with open(tmp_json, "w") as f:
        json.dump(config, f, indent=2)

    # Create job group if requested
    group_id = None
    if args.group:
        group_id = create_job_group(args.group, args.project_id)

    # Submit jobs
    success, failed = 0, 0
    for input_dir in args.input_dirs:
        if not input_dir.is_dir():
            print(f"[SKIP] Not a directory: {input_dir}")
            continue
        job_name = f"{config.get('job_name', 'job')}-{input_dir.name}"
        ok = submit_job(tmp_json, input_dir, job_name, group_id, args.result_path)
        if ok:
            success += 1
        else:
            failed += 1

    print(f"\n[DONE] {success} submitted, {failed} failed")
    if group_id:
        print(f"[INFO] Job group ID: {group_id}")


if __name__ == "__main__":
    main()
