#!/usr/bin/env python3
"""Safe Seedance task client: dry-run, explicit paid submit, poll, download."""
from __future__ import annotations

import argparse
import json
import os
import base64
import time
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

DEFAULT_API = "https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks"


def load_tasks(path: Path) -> list[dict]:
    tasks = []
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            tasks.append(json.loads(line))
        except json.JSONDecodeError as e:
            raise SystemExit(f"invalid JSONL at line {i}: {e}")
    return tasks


def load_state(path: Path) -> dict:
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    return {"api": DEFAULT_API, "tasks": {}}


def save_state(path: Path, state: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def task_summary(task: dict) -> dict:
    refs = sum(1 for x in task.get("content", []) if x.get("type") == "image_url")
    local_refs = task.get("meta", {}).get("reference_paths", [])
    return {
        "custom_id": task.get("custom_id"),
        "model": task.get("model"),
        "duration": task.get("duration"),
        "ratio": task.get("ratio"),
        "resolution": task.get("resolution"),
        "generate_audio": task.get("generate_audio"),
        "references": refs,
        "local_reference_paths": len(local_refs) if isinstance(local_refs, list) else 0,
        "meta": task.get("meta", {}),
    }


def dry_run(tasks: list[dict]) -> dict:
    durations = Counter(t.get("duration") for t in tasks)
    refs = Counter(task_summary(t)["references"] for t in tasks)
    models = Counter(t.get("model") for t in tasks)
    invalid = []
    warnings = []
    for t in tasks:
        cid = t.get("custom_id") or "<missing>"
        summary = task_summary(t)
        if summary["references"] == 0 and summary["local_reference_paths"] > 0:
            warnings.append(f"{cid}: local reference paths present; submit with --embed-local-refs")
        elif summary["references"] == 0:
            warnings.append(f"{cid}: no image reference; character consistency may drift")
        if not t.get("content") or not any(x.get("type") == "text" and x.get("text") for x in t["content"]):
            invalid.append(f"{cid}: missing text prompt")
        d = t.get("duration")
        if not isinstance(d, (int, float)) or not (4 <= d <= 30):
            invalid.append(f"{cid}: duration must be 4-30")
    total_seconds = sum(float(t.get("duration") or 0) for t in tasks)
    return {
        "tasks": len(tasks),
        "total_video_seconds": total_seconds,
        "durations": {str(k): v for k, v in durations.items()},
        "reference_counts": {str(k): v for k, v in refs.items()},
        "models": dict(models),
        "invalid": invalid,
        "warnings": warnings,
    }


def http_json(url: str, api_key: str, method="GET", body=None, timeout=120):
    data = json.dumps(body, ensure_ascii=False).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}, method=method)
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8", "replace"))


def cmd_dry_run(args):
    tasks = load_tasks(Path(args.tasks))
    result = dry_run(tasks)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if result["invalid"]:
        raise SystemExit(1)


def embed_local_refs(task: dict) -> dict:
    task = dict(task)
    task["content"] = list(task.get("content", []))
    for path_str in task.get("meta", {}).get("reference_paths", []) or []:
        path = Path(path_str)
        if not path.exists():
            print("reference_missing", path_str)
            continue
        if path.stat().st_size > 30 * 1024 * 1024:
            print("reference_too_large", path_str)
            continue
        suffix = path.suffix.lower()
        mime = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}.get(suffix)
        if not mime:
            print("reference_unsupported", path_str)
            continue
        data = base64.b64encode(path.read_bytes()).decode("ascii")
        task["content"].append({"type": "image_url", "image_url": {"url": f"data:{mime};base64,{data}"}, "role": "reference_image"})
        print("embedded_reference", path_str)
    return task


def cmd_submit(args):
    if not (args.execute and args.confirm_paid):
        print("DRY RUN ONLY. Add --execute --confirm-paid to submit paid tasks.")
        cmd_dry_run(args)
        return
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        raise SystemExit("ARK_API_KEY is not set")
    tasks = load_tasks(Path(args.tasks))[: args.limit]
    if not tasks:
        raise SystemExit("no tasks to submit")
    state_path = Path(args.state)
    state = load_state(state_path)
    state.setdefault("api", args.api_url)
    state.setdefault("tasks", {})
    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    for raw_task in tasks:
        task = embed_local_refs(raw_task) if args.embed_local_refs else raw_task
        cid = task.get("custom_id") or f"task-{len(state['tasks'])+1}"
        if cid in state["tasks"] and state["tasks"][cid].get("provider_task_id"):
            print(f"skip already submitted: {cid}")
            continue
        try:
            resp = http_json(args.api_url, api_key, method="POST", body=task)
            state["tasks"][cid] = {"provider_task_id": resp.get("id"), "status": "queued", "request": task_summary(task), "create_response": resp}
            print("submitted", cid, resp.get("id"))
        except urllib.error.HTTPError as e:
            msg = e.read().decode("utf-8", "replace")
            state["tasks"][cid] = {"status": "submit_failed", "error": msg, "request": task_summary(task)}
            print("submit_failed", cid, e.code, msg[:500])
        except Exception as e:
            state["tasks"][cid] = {"status": "submit_failed", "error": str(e), "request": task_summary(task)}
            print("submit_failed", cid, type(e).__name__, e)
        save_state(state_path, state)
        time.sleep(args.interval)


def cmd_poll(args):
    api_key = os.environ.get("ARK_API_KEY")
    if not api_key:
        raise SystemExit("ARK_API_KEY is not set")
    state_path = Path(args.state)
    state = load_state(state_path)
    api = state.get("api") or args.api_url
    download_dir = Path(args.download_dir) if args.download_dir else None
    if download_dir: download_dir.mkdir(parents=True, exist_ok=True)
    deadline = time.time() + args.timeout_minutes * 60
    while True:
        pending = 0
        for cid, rec in state.get("tasks", {}).items():
            tid = rec.get("provider_task_id")
            if not tid or rec.get("status") in {"succeeded", "failed", "cancelled", "expired"}:
                continue
            pending += 1
            try:
                st = http_json(f"{api}/{tid}", api_key)
                rec["status"] = st.get("status")
                rec["last_response"] = st
                content = st.get("content") or {}
                video_url = content.get("video_url") if isinstance(content, dict) else None
                if video_url:
                    rec["video_url"] = video_url
                    if download_dir and not rec.get("video_path"):
                        target = download_dir / f"{cid}.mp4"
                        with urllib.request.urlopen(urllib.request.Request(video_url, headers={"User-Agent": "Mozilla/5.0"}), timeout=180) as r, open(target, "wb") as f:
                            while True:
                                chunk = r.read(1024 * 1024)
                                if not chunk: break
                                f.write(chunk)
                        rec["video_path"] = str(target)
                        print("downloaded", cid, target.stat().st_size)
                print("status", cid, rec["status"])
            except Exception as e:
                rec["poll_error"] = f"{type(e).__name__}: {e}"
                print("poll_error", cid, rec["poll_error"])
        save_state(state_path, state)
        if pending == 0 or time.time() >= deadline:
            break
        time.sleep(args.interval)
    print(json.dumps(status_summary(state), ensure_ascii=False, indent=2))


def status_summary(state: dict) -> dict:
    counts = Counter(v.get("status", "unknown") for v in state.get("tasks", {}).values())
    return {"tasks": len(state.get("tasks", {})), "status_counts": dict(counts), "state_api": state.get("api")}


def cmd_status(args):
    state = load_state(Path(args.state))
    print(json.dumps(status_summary(state), ensure_ascii=False, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--api-url", default=DEFAULT_API)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("dry-run")
    p.add_argument("--tasks", required=True)
    p.set_defaults(func=cmd_dry_run)

    p = sub.add_parser("submit")
    p.add_argument("--tasks", required=True)
    p.add_argument("--state", required=True)
    p.add_argument("--output-dir", required=True)
    p.add_argument("--limit", type=int, default=1)
    p.add_argument("--interval", type=float, default=2)
    p.add_argument("--execute", action="store_true")
    p.add_argument("--confirm-paid", action="store_true")
    p.add_argument("--embed-local-refs", action="store_true", help="Embed meta.reference_paths as Base64 image references")
    p.set_defaults(func=cmd_submit)

    p = sub.add_parser("poll")
    p.add_argument("--state", required=True)
    p.add_argument("--download-dir")
    p.add_argument("--interval", type=float, default=10)
    p.add_argument("--timeout-minutes", type=float, default=30)
    p.set_defaults(func=cmd_poll)

    p = sub.add_parser("status")
    p.add_argument("--state", required=True)
    p.set_defaults(func=cmd_status)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
