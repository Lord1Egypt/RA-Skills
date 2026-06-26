#!/usr/bin/env python3
"""Dump a BP anchor map for one node.

This script solidifies the data-fetching step of the skill so the BP skeleton
does not depend on ad hoc code written during each run.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import requests


BASE_URL = "https://sg-al-cwork-web.mediportal.com.cn/open-api"


def api_get(app_key: str, endpoint: str, params: dict) -> dict:
    resp = requests.get(
        f"{BASE_URL}{endpoint}",
        params=params,
        headers={"appKey": app_key, "Content-Type": "application/json"},
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()


def build_anchor_map(app_key: str, period_id: str, group_id: str) -> list[dict]:
    tree = api_get(
        app_key,
        "/bp/task/v2/getSimpleTree",
        {"periodId": period_id, "groupId": group_id},
    )
    goals = tree.get("data") or []
    out = []
    for goal in goals:
        goal_id = str(goal["id"])
        detail = api_get(app_key, "/bp/task/v2/getGoalAndKeyResult", {"id": goal_id}).get(
            "data", {}
        )
        owners = extract_owner_names(detail)
        item = {
            "goal_id": goal_id,
            "goal_name": strip_html(detail.get("name") or goal.get("name") or ""),
            "owners": owners,
            "key_results": [],
        }
        for kr in detail.get("keyResultList") or detail.get("keyResults") or []:
            actions = []
            for action in kr.get("children") or kr.get("actionList") or kr.get("actions") or []:
                actions.append(
                    {
                        "action_id": str(action["id"]),
                        "action_name": strip_html(action.get("name") or ""),
                        "assignees": extract_owner_names(action),
                    }
                )
            item["key_results"].append(
                {
                    "result_id": str(kr["id"]),
                    "result_name": strip_html(kr.get("name") or ""),
                    "measure_standard": strip_html(kr.get("measureStandard") or ""),
                    "owners": extract_owner_names(kr),
                    "action_assignees": sorted(
                        {
                            assignee
                            for action in actions
                            for assignee in action.get("assignees", [])
                        }
                    ),
                    "actions": actions,
                }
            )
        out.append(item)
    return out


def strip_html(text: str) -> str:
    return (
        text.replace("<p>", "")
        .replace("</p>", "")
        .replace("<strong>", "")
        .replace("</strong>", "")
        .replace("<br>", " ")
        .replace("<br/>", " ")
        .replace("<br />", " ")
    )


def extract_owner_names(task_obj: dict) -> list[str]:
    users = task_obj.get("taskUsers") or []
    names = []
    for user in users:
        for emp in user.get("empList") or []:
            name = emp.get("name")
            if name:
                names.append(name)
    return names


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--app-key", required=True)
    parser.add_argument("--period-id", required=True)
    parser.add_argument("--group-id", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = build_anchor_map(args.app_key, args.period_id, args.group_id)
    output = Path(args.output)
    output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)


if __name__ == "__main__":
    main()
