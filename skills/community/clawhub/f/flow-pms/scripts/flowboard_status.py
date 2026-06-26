#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import flowboard_lookup  # noqa: E402


TASK_STATUSES = ["backlog", "todo", "in_progress", "in_review", "done", "cancelled"]
TASK_PRIORITIES = ["urgent", "high", "medium", "low", "none"]


def count_by(items, field, ordered_keys=None):
    counts = {}
    for item in items:
        key = item.get(field) or "unknown"
        counts[key] = counts.get(key, 0) + 1
    if ordered_keys:
        ordered = {key: counts[key] for key in ordered_keys if key in counts}
        remaining = {key: value for key, value in counts.items() if key not in ordered}
        ordered.update(dict(sorted(remaining.items())))
        return ordered
    return dict(sorted(counts.items()))


def top_priority_tasks(tasks, limit=5):
    priority_rank = {name: index for index, name in enumerate(TASK_PRIORITIES)}
    status_rank = {
        "in_progress": 0,
        "in_review": 1,
        "todo": 2,
        "backlog": 3,
        "done": 4,
        "cancelled": 5,
    }

    sorted_tasks = sorted(
        tasks,
        key=lambda task: (
            priority_rank.get(task.get("priority"), 99),
            status_rank.get(task.get("status"), 99),
            task.get("due_date") or "9999-12-31",
            task.get("identifier") or task.get("title") or "",
        ),
    )
    return sorted_tasks[:limit]


def compact_task(task):
    return {
        "id": task.get("id"),
        "identifier": task.get("identifier"),
        "title": task.get("title"),
        "status": task.get("status"),
        "priority": task.get("priority"),
        "type": task.get("type"),
        "due_date": task.get("due_date"),
        "cycle_id": task.get("cycle_id"),
    }


def summarize(project, cycle, tasks, mode):
    active_cycle = cycle if cycle and cycle.get("status") == "active" else None
    cycle_id = active_cycle.get("id") if active_cycle else None
    cycle_tasks = [task for task in tasks if cycle_id and task.get("cycle_id") == cycle_id]
    urgent_open = [
        compact_task(task)
        for task in tasks
        if task.get("priority") == "urgent" and task.get("status") not in {"done", "cancelled"}
    ]
    in_progress = [task for task in tasks if task.get("status") == "in_progress"]
    blocked_signals = [
        compact_task(task)
        for task in tasks
        if task.get("status") in {"backlog", "todo", "in_review"} and task.get("priority") in {"high", "urgent"}
    ][:5]

    return {
        "project": {
            "id": project.get("id"),
            "name": project.get("name"),
            "prefix": project.get("prefix"),
            "status": project.get("status"),
            "deadline": project.get("deadline"),
            "client_name": project.get("client_name"),
            "updated_at": project.get("updated_at"),
        },
        "active_cycle": cycle,
        "task_summary": {
            "total": len(tasks),
            "by_status": count_by(tasks, "status", TASK_STATUSES),
            "by_priority": count_by(tasks, "priority", TASK_PRIORITIES),
            "in_progress_count": len(in_progress),
            "urgent_open_count": len(urgent_open),
        },
        "active_cycle_task_summary": {
            "mode": "active_cycle" if active_cycle else mode,
            "total": len(cycle_tasks),
            "by_status": count_by(cycle_tasks, "status", TASK_STATUSES),
        },
        "highlights": {
            "top_priority_open_tasks": [compact_task(task) for task in top_priority_tasks([
                task for task in tasks if task.get("status") not in {"done", "cancelled"}
            ])],
            "urgent_open_tasks": urgent_open[:5],
            "potential_attention_items": blocked_signals,
        },
    }


def format_brief(summary):
    project = summary["project"]
    cycle = summary.get("active_cycle")
    task_summary = summary["task_summary"]
    active_cycle_summary = summary["active_cycle_task_summary"]
    highlights = summary["highlights"]

    lines = []
    lines.append(f"Projeto: {project['name']} ({project['status']})")
    if project.get("deadline"):
        lines.append(f"Prazo: {project['deadline']}")
    if cycle:
        lines.append(
            "Cycle atual: "
            f"{cycle.get('name')} ({cycle.get('status')})"
            + (f", progresso {cycle.get('progress')}%" if cycle.get("progress") is not None else "")
        )
    else:
        lines.append("Cycle atual: nenhum cycle ativo encontrado")

    lines.append(f"Tasks totais: {task_summary['total']}")
    if task_summary["by_status"]:
        status_text = ", ".join(f"{k}: {v}" for k, v in task_summary["by_status"].items())
        lines.append(f"Por status: {status_text}")
    if active_cycle_summary["total"]:
        cycle_text = ", ".join(f"{k}: {v}" for k, v in active_cycle_summary["by_status"].items())
        lines.append(f"Tasks do cycle ativo: {active_cycle_summary['total']} ({cycle_text})")
    if highlights["urgent_open_tasks"]:
        urgent = "; ".join(
            f"{task.get('identifier') or task.get('id')}: {task.get('title')}"
            for task in highlights["urgent_open_tasks"][:3]
        )
        lines.append(f"Urgentes em aberto: {urgent}")
    elif highlights["top_priority_open_tasks"]:
        top = "; ".join(
            f"{task.get('identifier') or task.get('id')}: {task.get('title')}"
            for task in highlights["top_priority_open_tasks"][:3]
        )
        lines.append(f"Principais itens em aberto: {top}")

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="High-level project status summary for FlowBoard")
    parser.add_argument("project_query", help="Project name or close match")
    parser.add_argument("--api-key")
    parser.add_argument("--project-limit", type=int, default=100)
    parser.add_argument("--task-limit", type=int, default=200)
    parser.add_argument("--max-matches", type=int, default=5)
    parser.add_argument("--json-only", action="store_true")
    args = parser.parse_args()

    project_lookup = flowboard_lookup.lookup_project(
        argparse.Namespace(
            name=args.project_query,
            api_key=args.api_key,
            limit=args.project_limit,
            max_matches=args.max_matches,
        )
    )
    if not project_lookup.get("ok"):
        print(json.dumps(project_lookup, ensure_ascii=False, indent=2))
        sys.exit(1)

    matches = project_lookup.get("matches", [])
    if not matches:
        print(json.dumps({"ok": False, "error": f"No project match for '{args.project_query}'"}, ensure_ascii=False, indent=2))
        sys.exit(1)

    best = matches[0]
    project = best["item"]
    if len(matches) > 1 and matches[0]["score"] == matches[1]["score"] and matches[0]["score"] < 100:
        print(
            json.dumps(
                {
                    "ok": False,
                    "error": "Ambiguous project match",
                    "query": args.project_query,
                    "matches": matches,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        sys.exit(1)

    project_detail = flowboard_lookup.call_api("GET", f"/projects/{project['id']}", api_key=args.api_key)
    if not project_detail.get("ok"):
        print(json.dumps(project_detail, ensure_ascii=False, indent=2))
        sys.exit(1)
    project = project_detail["data"].get("data", project)

    cycle_lookup = flowboard_lookup.lookup_active_cycle(
        argparse.Namespace(project_id=project["id"], api_key=args.api_key, limit=100)
    )
    if not cycle_lookup.get("ok"):
        print(json.dumps(cycle_lookup, ensure_ascii=False, indent=2))
        sys.exit(1)
    cycle = cycle_lookup.get("data")

    task_result = flowboard_lookup.call_api(
        "GET",
        f"/projects/{project['id']}/tasks",
        query={"limit": args.task_limit, "offset": 0},
        api_key=args.api_key,
    )
    if not task_result.get("ok"):
        print(json.dumps(task_result, ensure_ascii=False, indent=2))
        sys.exit(1)
    tasks = flowboard_lookup.extract_data(task_result["data"])

    summary = summarize(project, cycle, tasks, cycle_lookup.get("mode"))
    response = {
        "ok": True,
        "query": args.project_query,
        "matched_project": {
            "score": best["score"],
            "matched_on": best["matched_on"],
            "id": project.get("id"),
            "name": project.get("name"),
        },
        "summary": summary,
        "brief": format_brief(summary),
    }
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
