#!/usr/bin/env python3
"""
run_flow.py —— 运行通用任务流转

支持：
1. 串行流转
2. 多方并行流转
3. 最终汇总
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
import uuid
from pathlib import Path


OFFICE_DIR = Path(os.environ.get("HERMES_OFFICE_DIR", Path.home() / ".hermes" / "office"))
STATE_FILE = OFFICE_DIR / "state" / "office_state.json"
FLOW_RUN_DIR = OFFICE_DIR / "flow_runs"
FLOW_DIR = Path(__file__).resolve().parent.parent / "flows"

FLOW_ALIASES = {
    "流转": "handoff-review",
    "handoff": "handoff-review",
    "handoff-review": "handoff-review",
    "并行综合": "fanout-synthesis",
    "fanout": "fanout-synthesis",
    "fanout-synthesis": "fanout-synthesis",
}


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())


def load_state() -> dict:
    if not STATE_FILE.exists():
        raise FileNotFoundError(f"找不到办公室状态文件：{STATE_FILE}")
    with open(STATE_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_flow_run(run_data: dict) -> Path:
    FLOW_RUN_DIR.mkdir(parents=True, exist_ok=True)
    run_path = FLOW_RUN_DIR / f"{run_data['run_id']}.json"
    with open(run_path, "w", encoding="utf-8") as f:
        json.dump(run_data, f, ensure_ascii=False, indent=2)
    return run_path


def list_flows() -> list[dict]:
    flows = []
    for path in sorted(FLOW_DIR.glob("*.json")):
        with open(path, encoding="utf-8") as f:
            flows.append(json.load(f))
    return flows


def resolve_flow_name(name: str) -> str:
    key = (name or "").strip()
    return FLOW_ALIASES.get(key, key)


def load_flow(name: str) -> dict:
    flow_name = resolve_flow_name(name)
    path = FLOW_DIR / f"{flow_name}.json"
    if not path.exists():
        raise FileNotFoundError(f"找不到 flow：{name}")
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def deep_get(data, path: str):
    current = data
    for part in path.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return ""
    return current if current is not None else ""


def render_template(text: str, context: dict) -> str:
    if not text:
        return ""

    def replace(match):
        expr = match.group(1).strip()
        value = deep_get(context, expr)
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False, indent=2)
        return str(value)

    return re.sub(r"\{\{\s*([^{}]+)\s*\}\}", replace, text)


def resolve_worker(identifier: str, state: dict) -> dict:
    workers = state.get("workers", {})
    if identifier in workers:
        worker = workers[identifier]
        return {"worker_id": identifier, **worker}
    for worker_id, worker in workers.items():
        if worker.get("name") == identifier:
            return {"worker_id": worker_id, **worker}
    raise KeyError(f"找不到员工：{identifier}")


def post_task(port: int, payload: dict) -> dict:
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
    request = urllib.request.Request(
        f"http://127.0.0.1:{port}/tasks",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def get_task(port: int, task_id: str) -> dict:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/tasks/{task_id}", timeout=10) as resp:
        return json.loads(resp.read().decode("utf-8"))


def wait_task(port: int, task_id: str, timeout_seconds: int = 180, interval_seconds: float = 1.0) -> dict:
    started = time.time()
    while time.time() - started <= timeout_seconds:
        task = get_task(port, task_id)
        status = task.get("status")
        if status in {"done", "error"}:
            return task
        time.sleep(interval_seconds)
    raise TimeoutError(f"任务超时：{task_id}")


def normalize_result(step_id: str, worker: dict, task_payload: dict, task_result: dict) -> dict:
    result = task_result.get("result", {}) if isinstance(task_result.get("result"), dict) else {}
    return {
        "step_id": step_id,
        "worker_id": worker["worker_id"],
        "worker_name": worker.get("name", worker["worker_id"]),
        "status": task_result.get("status", "unknown"),
        "title": task_payload.get("title", ""),
        "summary": task_result.get("summary", ""),
        "result": result,
        "content": result.get("content", ""),
        "raw": task_result,
    }


def build_combined_content(results: list[dict]) -> str:
    blocks = []
    for item in results:
        blocks.append(
            f"[{item['worker_name']}/{item['worker_id']}]\n"
            f"状态: {item['status']}\n"
            f"摘要: {item['summary']}\n"
            f"内容:\n{item['content']}"
        )
    return "\n\n".join(blocks)


def parse_slot_assignments(values: list[str]) -> dict:
    slots = {}
    for item in values or []:
        if "=" not in item:
            raise ValueError(f"无效 slot 参数：{item}，应为 slot=name")
        key, value = item.split("=", 1)
        slots[key.strip()] = value.strip()
    return slots


def execute_single_step(step: dict, state: dict, context: dict) -> dict:
    worker_name = context["slot_values"][step["worker_slot"]]
    worker = resolve_worker(worker_name, state)
    payload = {
        "title": render_template(step.get("title", context["input"]["title"]), context),
        "description": render_template(step.get("description", context["input"]["description"]), context),
    }
    task_meta = post_task(worker["port"], payload)
    task_result = wait_task(worker["port"], task_meta["task_id"], timeout_seconds=step.get("timeout", 180))
    return normalize_result(step["id"], worker, payload, task_result)


def execute_parallel_step(step: dict, state: dict, context: dict) -> dict:
    submitted = []
    for branch in step.get("branches", []):
        worker_name = context["slot_values"][branch["worker_slot"]]
        worker = resolve_worker(worker_name, state)
        payload = {
            "title": render_template(branch.get("title", context["input"]["title"]), context),
            "description": render_template(branch.get("description", context["input"]["description"]), context),
        }
        task_meta = post_task(worker["port"], payload)
        submitted.append((branch, worker, payload, task_meta["task_id"]))

    results = []
    for branch, worker, payload, task_id in submitted:
        task_result = wait_task(worker["port"], task_id, timeout_seconds=branch.get("timeout", step.get("timeout", 180)))
        results.append(normalize_result(branch["id"], worker, payload, task_result))

    combined = build_combined_content(results)
    return {
        "step_id": step["id"],
        "type": "parallel",
        "status": "done" if all(item["status"] == "done" for item in results) else "partial",
        "branches": results,
        "combined_content": combined,
        "summary": " / ".join(item["summary"] for item in results if item.get("summary")),
    }


def validate_slots(flow: dict, slot_values: dict) -> None:
    required = set(flow.get("slots", {}).keys())
    missing = sorted(required - set(slot_values.keys()))
    if missing:
        raise ValueError(f"缺少 slot 绑定：{', '.join(missing)}")


def run_flow(flow: dict, title: str, description: str, slot_values: dict) -> dict:
    state = load_state()
    validate_slots(flow, slot_values)

    run_data = {
        "run_id": str(uuid.uuid4()),
        "flow_name": flow["name"],
        "flow_display_name": flow.get("display_name", flow["name"]),
        "started_at": now(),
        "status": "running",
        "input": {
            "title": title,
            "description": description,
        },
        "slot_values": slot_values,
        "steps": {}
    }
    run_path = save_flow_run(run_data)

    context = {
        "input": run_data["input"],
        "steps": run_data["steps"],
        "slot_values": slot_values,
        "run": {
            "id": run_data["run_id"],
            "path": str(run_path),
        },
    }

    for step in flow.get("steps", []):
        if step["type"] == "single":
            result = execute_single_step(step, state, context)
        elif step["type"] == "parallel":
            result = execute_parallel_step(step, state, context)
        else:
            raise ValueError(f"未知 step 类型：{step['type']}")

        run_data["steps"][step["id"]] = result
        save_flow_run(run_data)

    run_data["status"] = "done"
    run_data["finished_at"] = now()
    save_flow_run(run_data)
    return run_data


def print_flow_list() -> None:
    print("可用流转模板：")
    for flow in list_flows():
        print(f"- {flow['display_name']} ({flow['name']})")
        print(f"  {flow.get('description', '')}")
        if flow.get("slots"):
            print(f"  需要岗位: {', '.join(flow['slots'].keys())}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Agent Office flows")
    parser.add_argument("flow", nargs="?", help="flow 名称，如 handoff-review")
    parser.add_argument("--title", default="未命名流转任务", help="任务标题")
    parser.add_argument("--description", default="", help="任务描述")
    parser.add_argument("--slot", action="append", default=[], help="绑定岗位，如 planner=产品")
    parser.add_argument("--list", action="store_true", help="列出可用流转模板")
    args = parser.parse_args()

    if args.list:
        print_flow_list()
        return

    if not args.flow:
        print("❌ 用法: python3 run_flow.py <flow> --slot planner=产品 ...")
        print("   先看列表: python3 run_flow.py --list")
        sys.exit(1)

    try:
        flow = load_flow(args.flow)
        slot_values = parse_slot_assignments(args.slot)
        result = run_flow(flow, args.title, args.description, slot_values)
    except (FileNotFoundError, KeyError, ValueError, TimeoutError, urllib.error.URLError) as e:
        print(f"❌ {e}")
        sys.exit(1)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"✅ 流转完成：{result['flow_display_name']}")
    print(f"   run_id: {result['run_id']}")
    print(f"   结果文件: {FLOW_RUN_DIR / (result['run_id'] + '.json')}")
    print(f"   最后一步: {list(result['steps'].keys())[-1] if result['steps'] else '-'}")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")


if __name__ == "__main__":
    main()
