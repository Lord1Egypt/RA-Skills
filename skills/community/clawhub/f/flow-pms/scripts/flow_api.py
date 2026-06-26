#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "httpx>=0.27.0",
# ]
# ///
"""
Interact with FlowDeck REST API (Project Management: projects, cycles, tasks).

Usage:
    uv run flow_api.py list projects [--limit 50] [--offset 0] [--status in_progress]
    uv run flow_api.py get projects --id <uuid>
    uv run flow_api.py create projects --data '{"name":"Novo Projeto","prefix":"NP"}'
    uv run flow_api.py update projects --id <uuid> --data '{"status":"in_progress"}'
    uv run flow_api.py delete projects --id <uuid>
    uv run flow_api.py archive projects --id <uuid>
    uv run flow_api.py unarchive projects --id <uuid>

Resources: projects, cycles, tasks, comments

Use --api-key or set FLOWBOARD_API_KEY env var.
Use --base-url or set FLOWBOARD_BASE_URL env var.
"""

import argparse
import json
import os
import sys

import httpx


SUPPORTED_RESOURCES = {
    "projects": {"base": "/projects", "supports_archive": True},
    "cycles": {"base": "/cycles/{id}", "path_param": True, "parent_base": "/projects/{projectId}/cycles"},
    "tasks": {"base": "/tasks/{id}", "path_param": True, "parent_base": "/projects/{projectId}/tasks"},
    "comments": {"base": "/comments/{id}", "path_param": True, "parent_base": "/tasks/{taskId}/comments"},
}


def get_api_key(provided: str | None) -> str:
    if provided:
        return provided
    key = os.environ.get("FLOWBOARD_API_KEY")
    if not key:
        print("Error: No API key provided.", file=sys.stderr)
        print("  Set FLOWBOARD_API_KEY env var or pass --api-key", file=sys.stderr)
        sys.exit(1)
    return key


def get_base_url(provided: str | None) -> str:
    if provided:
        return provided.rstrip("/")
    val = os.environ.get(
        "FLOWBOARD_BASE_URL",
        "https://mycivgjuujlnyoycuwrz.supabase.co/functions/v1/api-gateway",
    )
    return val.rstrip("/")


def parse_query_params(args: argparse.Namespace) -> dict:
    """Extract known query parameters from CLI args."""
    params = {}
    for key in ("limit", "offset", "status", "priority", "cycle_id",
                 "assignee_id", "type"):
        val = getattr(args, key, None)
        if val is not None:
            params[key] = str(val)
    return params


def build_url(resource: str, action: str, resource_id: str | None,
              parent_project_id: str | None) -> str:
    info = SUPPORTED_RESOURCES.get(resource)
    if not info:
        print(f"Error: Unknown resource '{resource}'.", file=sys.stderr)
        print(f"Supported: {', '.join(SUPPORTED_RESOURCES.keys())}", file=sys.stderr)
        sys.exit(1)

    if action == "list":
        if resource == "cycles" and parent_project_id:
            return f"/projects/{parent_project_id}/cycles"
        if resource == "tasks" and parent_project_id:
            return f"/projects/{parent_project_id}/tasks"
        if resource == "comments" and parent_project_id:
            return f"/tasks/{parent_project_id}/comments"
        return info["base"]

    if action == "create":
        if resource == "cycles" and parent_project_id:
            return f"/projects/{parent_project_id}/cycles"
        if resource == "tasks" and parent_project_id:
            return f"/projects/{parent_project_id}/tasks"
        if resource == "comments" and parent_project_id:
            return f"/tasks/{parent_project_id}/comments"
        return info.get("parent_base", info["base"]) \
                   .replace("{projectId}", str(parent_project_id or "")) \
                   .replace("{taskId}", str(parent_project_id or ""))

    if action in ("archive", "unarchive"):
        if not resource_id:
            print("Error: --id is required for archive/unarchive.", file=sys.stderr)
            sys.exit(1)
        return f"/projects/{resource_id}/{action}"

    # get/update/delete
    if resource_id:
        base = info["base"]
        if "{id}" in base:
            return base.replace("{id}", resource_id)
        return f"{base}/{resource_id}"

    return info["base"]


def main():
    parser = argparse.ArgumentParser(
        description="FlowDeck API CLI (Project Management)"
    )
    parser.add_argument("--api-key", help="Bearer API key")
    parser.add_argument("--base-url", dest="base_url",
                        help="Base URL for the API gateway")

    subparsers = parser.add_subparsers(dest="action", required=True)

    # list
    list_p = subparsers.add_parser("list", help="List resources")
    list_p.add_argument("resource", choices=SUPPORTED_RESOURCES.keys())
    list_p.add_argument("--limit", type=int)
    list_p.add_argument("--offset", type=int)
    list_p.add_argument("--status", type=str)
    list_p.add_argument("--priority", type=str)
    list_p.add_argument("--cycle-id", dest="cycle_id")
    list_p.add_argument("--assignee-id", dest="assignee_id")
    list_p.add_argument("--type", type=str)
    list_p.add_argument("--project-id", dest="parent_id")

    # get
    get_p = subparsers.add_parser("get", help="Get single resource")
    get_p.add_argument("resource", choices=SUPPORTED_RESOURCES.keys())
    get_p.add_argument("--id", required=True)

    # create
    create_p = subparsers.add_parser("create", help="Create resource")
    create_p.add_argument("resource", choices=SUPPORTED_RESOURCES.keys())
    create_p.add_argument("--data", required=True,
                          help='JSON body string')
    create_p.add_argument("--project-id", dest="parent_id",
                          help="Parent project ID for cycles, tasks, comments")

    # update
    update_p = subparsers.add_parser("update", help="Update resource")
    update_p.add_argument("resource", choices=SUPPORTED_RESOURCES.keys())
    update_p.add_argument("--id", required=True)
    update_p.add_argument("--data", required=True,
                          help='JSON body string')

    # delete
    delete_p = subparsers.add_parser("delete", help="Delete resource")
    delete_p.add_argument("resource", choices=SUPPORTED_RESOURCES.keys())
    delete_p.add_argument("--id", required=True)

    # archive
    archive_p = subparsers.add_parser("archive", help="Archive project")
    archive_p.add_argument("resource", choices=["projects"])
    archive_p.add_argument("--id", required=True)

    # unarchive
    unarchive_p = subparsers.add_parser("unarchive", help="Unarchive project")
    unarchive_p.add_argument("resource", choices=["projects"])
    unarchive_p.add_argument("--id", required=True)

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    base_url = get_base_url(args.base_url)

    query = parse_query_params(args)
    parent_id = getattr(args, "parent_id", None)
    resource_id = getattr(args, "id", None)

    http_method_map = {
        "list": "GET",
        "get": "GET",
        "create": "POST",
        "update": "PATCH",
        "delete": "DELETE",
        "archive": "POST",
        "unarchive": "POST",
    }

    url = base_url + build_url(args.resource, args.action,
                               resource_id, parent_id)

    try:
        if args.action in ("list", "get", "archive", "unarchive"):
            body = None
            params = query if args.action == "list" else None
            resp = httpx.request(
                http_method_map[args.action], url,
                headers={"Authorization": f"Bearer {api_key}",
                          "Content-Type": "application/json"},
                params=params, json=body, timeout=30,
            )
        elif args.action in ("create", "update"):
            body = json.loads(args.data)
            resp = httpx.request(
                http_method_map[args.action], url,
                headers={"Authorization": f"Bearer {api_key}",
                          "Content-Type": "application/json"},
                json=body, timeout=30,
            )
        else:
            resp = httpx.request(
                http_method_map[args.action], url,
                headers={"Authorization": f"Bearer {api_key}",
                          "Content-Type": "application/json"},
                timeout=30,
            )

        if resp.status_code >= 400:
            print(f"Error: HTTP {resp.status_code}", file=sys.stderr)
            try:
                detail = resp.json()
                print(json.dumps(detail, ensure_ascii=False, indent=2),
                      file=sys.stderr)
            except Exception:
                print(resp.text, file=sys.stderr)
            sys.exit(1)

        print(json.dumps(resp.json(), ensure_ascii=False, indent=2))

    except httpx.RequestError as e:
        print(f"Request failed: {e}", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Invalid JSON in --data: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
