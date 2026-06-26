#!/usr/bin/env python3

import argparse
import hashlib
import json
import os
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

STATUS_LABELS = {
    1: "成功",
    2: "失败",
    3: "部分成功",
    4: "正在执行",
}

DEFAULT_SCRIPT_ID = 187
DEFAULT_TASK_NAME = "故障处理-脚本执行"
MAX_WAIT_SECONDS = 300
POLL_INTERVAL = 3


def load_env(env_path: Path) -> None:
    if not env_path.exists():
        return
    for raw_line in env_path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip("'").strip('"'))


def make_sign(data: dict, secret: str) -> str:
    parts = []
    for key in sorted(data):
        if key == "sign":
            continue
        value = data[key]
        if value in ("", None) or isinstance(value, (list, dict)):
            continue
        parts.append(f"{key}{value}")
    return hashlib.sha1(f"{secret}{''.join(parts)}".encode("utf-8")).hexdigest().lower()


def post_json(api_url: str, api_secret: str, route: str, params: dict, timeout: int = 30) -> dict:
    payload = dict(params)
    payload["timestamp"] = int(datetime.now().timestamp())
    payload["sign"] = make_sign(payload, api_secret)
    body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        api_url.rstrip("/") + route,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.loads(response.read().decode("utf-8"))


def parse_args():
    parser = argparse.ArgumentParser(description="Execute fault handling scripts on remote hosts")
    parser.add_argument("--hosts", help="Comma-separated host IPs (e.g. '192.168.3.76,192.168.3.75')")
    parser.add_argument("--organizes", help="Comma-separated organizes for each host (e.g. '普通用户,')")
    parser.add_argument("--script-id", dest="script_id", default="", help="Script ID (default: 187)")
    parser.add_argument("--script-type", dest="script_type", type=int, default=1, help="Script type: 1=shell, 2=python, 3=playbook, 4=powershell, 5=network")
    parser.add_argument("--script-content", dest="script_content", default="", help="Script content (if no script-id)")
    parser.add_argument("--task-name", dest="task_name", default=DEFAULT_TASK_NAME, help="Task name")
    parser.add_argument("--step-name", dest="step_name", default="步骤1", help="Step name")
    parser.add_argument("--timeout", type=int, default=3600, help="Script execution timeout in seconds")
    parser.add_argument("--no-wait", dest="no_wait", action="store_true", help="Submit task without waiting for result")
    parser.add_argument("--query", type=int, help="Query execution history by execution_id (skip run-script)")
    parser.add_argument("--max-wait", dest="max_wait", type=int, default=MAX_WAIT_SECONDS, help="Max seconds to wait for completion")
    parser.add_argument("--poll-interval", dest="poll_interval", type=int, default=POLL_INTERVAL, help="Seconds between status polls")
    return parser.parse_args()


def init_env():
    skill_dir = Path(__file__).resolve().parent
    load_env(skill_dir / ".env")

    api_url = os.environ.get("LWJK_API_URL", "")
    api_secret = os.environ.get("LWJK_API_SECRET", "")
    if not api_url or not api_secret:
        raise SystemExit(
            "LWJK_API_URL 和 LWJK_API_SECRET 未配置，"
            "请检查 skills/fault-handling/.env"
        )
    return api_url, api_secret


def build_hosts(hosts_str: str, organizes_str: str | None) -> list[dict]:
    ips = [ip.strip() for ip in hosts_str.split(",") if ip.strip()]
    if not ips:
        raise SystemExit("至少需要一个主机 IP（--hosts）")

    organizes = []
    if organizes_str:
        organizes = [o.strip() for o in organizes_str.split(",")]

    result = []
    for i, ip in enumerate(ips):
        organize = organizes[i] if i < len(organizes) else ""
        result.append({"ansible_host": ip, "organize": organize})
    return result


def run_script(api_url: str, api_secret: str, args) -> dict:
    hosts = build_hosts(args.hosts, args.organizes)

    step = {
        "step_name": args.step_name,
        "current_user": "",
        "proxy_ip": "",
        "timeout": args.timeout,
        "hosts": hosts,
        "script_type": args.script_type,
        "script_content": args.script_content,
        "script_id": args.script_id if args.script_id else "",
        "arguments": [],
        "error_result": [],
        "success_result": [],
    }

    data_payload = {
        "task_name": args.task_name,
        "steps": [step],
    }

    params = {"data": json.dumps(data_payload, ensure_ascii=False)}
    print(f"[run-script] 提交任务: {args.task_name}, 主机: {[h['ansible_host'] for h in hosts]}", file=sys.stderr)

    result = post_json(api_url, api_secret, "/api/v6/devops/run-script", params)

    if result.get("code") != 0:
        raise SystemExit(f"run-script API 返回错误: code={result.get('code')}, message={result.get('message')}")

    data = result.get("data", {})
    execution_id = data.get("execution_id")
    task_name = data.get("task_name", args.task_name)

    print(f"[run-script] 任务已提交: execution_id={execution_id}, task_name={task_name}", file=sys.stderr)
    return {"execution_id": execution_id, "task_name": task_name}


def query_execution(api_url: str, api_secret: str, execution_id: int) -> dict:
    params = {"data": json.dumps({"execution_id": execution_id}, ensure_ascii=False)}
    result = post_json(api_url, api_secret, "/api/v6/devops/execution-history", params)

    if result.get("code") != 0:
        raise SystemExit(f"execution-history API 返回错误: code={result.get('code')}, message={result.get('message')}")

    return result.get("data", {})


def wait_for_completion(api_url: str, api_secret: str, execution_id: int, max_wait: int, poll_interval: int) -> dict:
    elapsed = 0
    while elapsed < max_wait:
        data = query_execution(api_url, api_secret, execution_id)
        is_running = data.get("is_running", True)
        detail = data.get("detail", {})
        status = detail.get("status", 4)

        print(f"[poll] elapsed={elapsed}s, is_running={is_running}, status={STATUS_LABELS.get(status, status)}", file=sys.stderr)

        if not is_running and status != 4:
            return data

        time.sleep(poll_interval)
        elapsed += poll_interval

    print(f"[poll] 超时({max_wait}s)，任务仍在执行中", file=sys.stderr)
    return query_execution(api_url, api_secret, execution_id)


def format_result(data: dict, execution_id: int) -> dict:
    detail = data.get("detail", {})
    status = detail.get("status", 4)
    output = detail.get("output", [])

    steps = []
    total_success = 0
    total_fail = 0

    for step_output in output:
        step_info = {
            "step_name": step_output.get("step_name", ""),
            "step_id": step_output.get("step_id", 0),
            "task": step_output.get("task", ""),
            "status": step_output.get("status", 0),
            "status_label": STATUS_LABELS.get(step_output.get("status", 0), "未知"),
            "consuming": step_output.get("consuming", 0),
            "hosts": [],
        }
        for host in step_output.get("hosts", []):
            host_status = host.get("status", 0)
            if host_status == 1:
                total_success += 1
            elif host_status == 2:
                total_fail += 1
            step_info["hosts"].append({
                "ansible_host": host.get("ansible_host", ""),
                "host_name": host.get("host_name", ""),
                "stdout": host.get("stdout", ""),
                "status": host_status,
                "status_label": STATUS_LABELS.get(host_status, "未知"),
                "os": host.get("os", ""),
            })
        steps.append(step_info)

    return {
        "execution_id": execution_id,
        "task_name": detail.get("task_name", ""),
        "status": status,
        "status_label": STATUS_LABELS.get(status, "未知"),
        "is_running": data.get("is_running", False),
        "begin_at": detail.get("begin_at", ""),
        "end_at": detail.get("end_at", ""),
        "consuming": detail.get("consuming", 0),
        "total_success": total_success,
        "total_fail": total_fail,
        "steps": steps,
    }


def main():
    args = parse_args()
    api_url, api_secret = init_env()

    # Query-only mode
    if args.query:
        print(f"[query] 查询任务 execution_id={args.query}", file=sys.stderr)
        data = query_execution(api_url, api_secret, args.query)
        result = format_result(data, args.query)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    # Run-script mode
    if not args.hosts:
        raise SystemExit("必须提供 --hosts 参数（主机 IP）")

    if not args.script_id and not args.script_content:
        args.script_id = str(DEFAULT_SCRIPT_ID)
        print(f"[run-script] 未指定脚本，使用默认脚本 ID={DEFAULT_SCRIPT_ID}", file=sys.stderr)

    submit_result = run_script(api_url, api_secret, args)
    execution_id = submit_result["execution_id"]

    if args.no_wait:
        print(json.dumps({
            "execution_id": execution_id,
            "task_name": submit_result["task_name"],
            "status": 4,
            "status_label": "已提交（未等待结果）",
            "is_running": True,
        }, ensure_ascii=False, indent=2))
        return

    # Poll for completion
    data = wait_for_completion(api_url, api_secret, execution_id, args.max_wait, args.poll_interval)
    result = format_result(data, execution_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
