from __future__ import annotations

import argparse
import json

import system_config as sc
from utils import json_fail, now_str


def out(data: dict) -> None:
    print(json.dumps(data, ensure_ascii=False))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job_id", required=True)
    parser.add_argument("--child_session_key", default="")
    parser.add_argument("--run_id", default="")
    parser.add_argument("--task_name", default="")
    parser.add_argument("--spawn_status", default="")
    args = parser.parse_args()

    jobs = sc.jobs()
    job = jobs.get(args.job_id)
    if not job:
        out(json_fail("job_not_found", "找不到批量编译 job。"))
        return

    worker_spawn = job.setdefault("worker_spawn", {})
    if args.child_session_key:
        worker_spawn["child_session_key"] = args.child_session_key
    if args.run_id:
        worker_spawn["run_id"] = args.run_id
    if args.task_name:
        worker_spawn["task_name"] = args.task_name
    if args.spawn_status:
        worker_spawn["spawn_status"] = args.spawn_status
    worker_spawn["updated_at"] = now_str()
    job["execution_mode"] = "background_worker"
    job["updated_at"] = now_str()

    sc.update_json("jobs.json", lambda current: {**current, args.job_id: job}, default={})
    out({"success": True, "job_id": args.job_id, "worker_spawn": worker_spawn})


if __name__ == "__main__":
    main()
