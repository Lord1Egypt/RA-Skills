#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flowboard_api  # noqa: E402


def call_api(method, path, query=None, body=None, api_key=None):
    key = flowboard_api.resolve_api_key(api_key)
    url = flowboard_api.build_url(path, query)
    headers = {
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    }
    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = flowboard_api.Request(url, data=data, headers=headers, method=method.upper())

    try:
        with flowboard_api.urlopen(request) as response:
            raw = response.read().decode("utf-8")
            payload = json.loads(raw) if raw else {}
            return {"ok": True, "status": response.getcode(), "data": payload}
    except flowboard_api.HTTPError as exc:
        raw = exc.read().decode("utf-8", errors="replace")
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError:
            payload = raw
        return {"ok": False, "status": exc.code, "error": payload}
    except flowboard_api.URLError as exc:
        return {"ok": False, "error": str(exc.reason)}


def normalize(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def score_name(candidate, target):
    candidate_n = normalize(candidate)
    target_n = normalize(target)
    if not candidate_n or not target_n:
        return 0
    if candidate_n == target_n:
        return 100
    if candidate_n.startswith(target_n) or target_n.startswith(candidate_n):
        return 90
    if target_n in candidate_n:
        return 80
    candidate_words = set(candidate_n.split())
    target_words = set(target_n.split())
    overlap = len(candidate_words & target_words)
    if overlap:
        return min(70, overlap * 15)
    return 0


def extract_data(payload):
    if isinstance(payload, dict):
        data = payload.get("data")
        if isinstance(data, list):
            return data
        if isinstance(data, dict):
            return [data]
    return []


def pick_best(items, target, keys):
    scored = []
    for item in items:
        best = 0
        matched_key = None
        for key in keys:
            value = item.get(key)
            score = score_name(value, target) if isinstance(value, str) else 0
            if score > best:
                best = score
                matched_key = key
        if best > 0:
            scored.append({"score": best, "matched_on": matched_key, "item": item})
    scored.sort(key=lambda x: (-x["score"], str(x["item"].get("name") or x["item"].get("title") or "")))
    return scored


def lookup_project(args):
    result = call_api("GET", "/projects", query={"limit": args.limit, "offset": 0}, api_key=args.api_key)
    if not result["ok"]:
        return result
    matches = pick_best(extract_data(result["data"]), args.name, ["name", "prefix"])
    return {
        "ok": True,
        "resource": "project",
        "query": args.name,
        "matches": matches[: args.max_matches],
    }


def lookup_task(args):
    task_query = {"limit": args.limit, "offset": 0}
    if args.status:
        task_query["status"] = args.status
    if args.priority:
        task_query["priority"] = args.priority
    if args.cycle_id:
        task_query["cycle_id"] = args.cycle_id
    result = call_api("GET", f"/projects/{args.project_id}/tasks", query=task_query, api_key=args.api_key)
    if not result["ok"]:
        return result

    data = extract_data(result["data"])
    identifier = normalize(args.query)
    exact_identifier = [
        {"score": 100, "matched_on": "identifier", "item": item}
        for item in data
        if normalize(item.get("identifier")) == identifier
    ]
    if exact_identifier:
        matches = exact_identifier
    else:
        matches = pick_best(data, args.query, ["title", "identifier"])

    return {
        "ok": True,
        "resource": "task",
        "query": args.query,
        "project_id": args.project_id,
        "matches": matches[: args.max_matches],
    }


def lookup_active_cycle(args):
    result = call_api("GET", f"/projects/{args.project_id}/cycles", query={"limit": args.limit, "offset": 0}, api_key=args.api_key)
    if not result["ok"]:
        return result
    cycles = extract_data(result["data"])
    active = [cycle for cycle in cycles if cycle.get("status") == "active"]
    if active:
        active.sort(key=lambda c: c.get("start_date") or "", reverse=True)
        selected = active[0]
        return {
            "ok": True,
            "resource": "cycle",
            "mode": "active",
            "project_id": args.project_id,
            "data": selected,
        }
    cycles.sort(key=lambda c: (c.get("start_date") or "", c.get("created_at") or ""), reverse=True)
    return {
        "ok": True,
        "resource": "cycle",
        "mode": "fallback_latest",
        "project_id": args.project_id,
        "data": cycles[0] if cycles else None,
    }


def main():
    parser = argparse.ArgumentParser(description="Search helper for FlowBoard resources")
    subparsers = parser.add_subparsers(dest="command", required=True)

    project = subparsers.add_parser("project", help="Find a project by name")
    project.add_argument("name")
    project.add_argument("--api-key")
    project.add_argument("--limit", type=int, default=100)
    project.add_argument("--max-matches", type=int, default=5)
    project.set_defaults(func=lookup_project)

    task = subparsers.add_parser("task", help="Find a task by identifier or title inside a project")
    task.add_argument("project_id")
    task.add_argument("query")
    task.add_argument("--api-key")
    task.add_argument("--limit", type=int, default=200)
    task.add_argument("--max-matches", type=int, default=10)
    task.add_argument("--status")
    task.add_argument("--priority")
    task.add_argument("--cycle-id")
    task.set_defaults(func=lookup_task)

    cycle = subparsers.add_parser("active-cycle", help="Get the active cycle for a project")
    cycle.add_argument("project_id")
    cycle.add_argument("--api-key")
    cycle.add_argument("--limit", type=int, default=100)
    cycle.set_defaults(func=lookup_active_cycle)

    args = parser.parse_args()
    result = args.func(args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if not result.get("ok", False):
        sys.exit(1)


if __name__ == "__main__":
    main()
