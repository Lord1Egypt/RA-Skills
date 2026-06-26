"""
Project member and budget management via Bohrium API.

Usage:
    python project_manager.py list
    python project_manager.py members --project_id 154
    python project_manager.py add_member --project_id 154 --email user@example.com
    python project_manager.py remove_member --project_id 154 --user_id 12345
    python project_manager.py set_budget --project_id 154 --limit 10000
    python project_manager.py promote --project_id 154 --user_id 12345
    python project_manager.py demote --project_id 154 --user_id 12345
"""

import argparse
import json
import os
import sys

import requests

AK = os.environ.get("ACCESS_KEY", "")
BASE = "https://openapi.dp.tech/openapi/v1/project"
HEADERS = {"accessKey": AK}
HEADERS_JSON = {**HEADERS, "Content-Type": "application/json"}

ROLE_MAP = {1: "Creator/Admin", 3: "Member"}


def list_projects():
    """List all projects with details (cost, member count)."""
    r = requests.get(f"{BASE}/list", headers=HEADERS)
    items = r.json().get("data", {}).get("items", [])

    print(f"{'ID':<8} {'Name':<25} {'Role':<15} {'Members':<8} {'Total Cost':<12} {'Month Cost'}")
    print("-" * 85)
    for p in items:
        role = ROLE_MAP.get(p.get("projectRole"), "?")
        print(
            f"{p.get('id', '?'):<8} "
            f"{p.get('name', '?')[:24]:<25} "
            f"{role:<15} "
            f"{p.get('userCount', '?'):<8} "
            f"¥{p.get('totalCost', 0):<11} "
            f"¥{p.get('monthCost', 0)}"
        )


def list_members(project_id: int):
    """List members of a project."""
    r = requests.get(f"{BASE}/{project_id}/users", headers=HEADERS)
    items = r.json().get("data", {}).get("items", [])

    if not items:
        print(f"No members found for project {project_id}")
        return

    print(f"Members of project {project_id}:\n")
    print(f"{'UserID':<10} {'Name':<20} {'Email':<30} {'Role':<15} {'Cost'}")
    print("-" * 85)
    for u in items:
        role = ROLE_MAP.get(u.get("projectRole"), "?")
        print(
            f"{u.get('userId', '?'):<10} "
            f"{u.get('userName', '?')[:19]:<20} "
            f"{u.get('email', '?')[:29]:<30} "
            f"{role:<15} "
            f"¥{u.get('cost', 0)}"
        )


def add_member(project_id: int, email: str):
    """Add a member to the project by email."""
    r = requests.post(
        f"{BASE}/add_user",
        headers=HEADERS_JSON,
        json={"projectId": project_id, "email": email},
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"Added {email} to project {project_id}")
    else:
        print(f"Failed: {result.get('message', result)}")


def remove_member(project_id: int, user_id: int):
    """Remove a member from the project."""
    r = requests.post(
        f"{BASE}/del_user",
        headers=HEADERS_JSON,
        json={"projectId": project_id, "userId": user_id},
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"Removed user {user_id} from project {project_id}")
    else:
        print(f"Failed: {result.get('message', result)}")


def set_budget(project_id: int, cost_limit: float):
    """Set project cost limit."""
    r = requests.post(
        f"{BASE}/set_cost_limit",
        headers=HEADERS_JSON,
        json={"projectId": project_id, "costLimit": cost_limit},
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"Project {project_id} budget set to ¥{cost_limit}")
    else:
        print(f"Failed: {result.get('message', result)}")


def promote_admin(project_id: int, user_id: int):
    """Promote a member to admin."""
    r = requests.post(
        f"{BASE}/manager/add",
        headers=HEADERS_JSON,
        json={"projectId": project_id, "userId": user_id},
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"User {user_id} promoted to admin in project {project_id}")
    else:
        print(f"Failed: {result.get('message', result)}")


def demote_admin(project_id: int, user_id: int):
    """Demote an admin to member."""
    r = requests.post(
        f"{BASE}/manager/del",
        headers=HEADERS_JSON,
        json={"projectId": project_id, "userId": user_id},
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"User {user_id} demoted to member in project {project_id}")
    else:
        print(f"Failed: {result.get('message', result)}")


def rename_project(project_id: int, name: str):
    """Rename a project."""
    r = requests.post(
        f"{BASE}/set_name",
        headers=HEADERS_JSON,
        json={"projectId": project_id, "name": name},
    )
    result = r.json()
    if result.get("code") == 0:
        print(f"Project {project_id} renamed to '{name}'")
    else:
        print(f"Failed: {result.get('message', result)}")


def main():
    parser = argparse.ArgumentParser(description="Bohrium project manager")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("list", help="List all projects with details")

    p_members = sub.add_parser("members", help="List project members")
    p_members.add_argument("--project_id", type=int, required=True)

    p_add = sub.add_parser("add_member", help="Add member by email")
    p_add.add_argument("--project_id", type=int, required=True)
    p_add.add_argument("--email", type=str, required=True)

    p_rm = sub.add_parser("remove_member", help="Remove member")
    p_rm.add_argument("--project_id", type=int, required=True)
    p_rm.add_argument("--user_id", type=int, required=True)

    p_budget = sub.add_parser("set_budget", help="Set project cost limit")
    p_budget.add_argument("--project_id", type=int, required=True)
    p_budget.add_argument("--limit", type=float, required=True)

    p_promote = sub.add_parser("promote", help="Promote member to admin")
    p_promote.add_argument("--project_id", type=int, required=True)
    p_promote.add_argument("--user_id", type=int, required=True)

    p_demote = sub.add_parser("demote", help="Demote admin to member")
    p_demote.add_argument("--project_id", type=int, required=True)
    p_demote.add_argument("--user_id", type=int, required=True)

    p_rename = sub.add_parser("rename", help="Rename project")
    p_rename.add_argument("--project_id", type=int, required=True)
    p_rename.add_argument("--name", type=str, required=True)

    args = parser.parse_args()

    if not AK:
        print("ERROR: ACCESS_KEY environment variable not set")
        sys.exit(1)

    handlers = {
        "list": lambda: list_projects(),
        "members": lambda: list_members(args.project_id),
        "add_member": lambda: add_member(args.project_id, args.email),
        "remove_member": lambda: remove_member(args.project_id, args.user_id),
        "set_budget": lambda: set_budget(args.project_id, args.limit),
        "promote": lambda: promote_admin(args.project_id, args.user_id),
        "demote": lambda: demote_admin(args.project_id, args.user_id),
        "rename": lambda: rename_project(args.project_id, args.name),
    }

    handler = handlers.get(args.cmd)
    if handler:
        handler()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
