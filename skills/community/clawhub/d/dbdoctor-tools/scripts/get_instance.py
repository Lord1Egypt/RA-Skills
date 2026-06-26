"""
get_instance.py - Get instance basic info

Get database instance list under tenant/project.
"""

import argparse
import json
import sys

from common import client


def get_instance(tenant_name: str, project_name: str) -> dict:
    """
    Get instance basic info.

    Args:
        tenant_name: Tenant name, optional
        project_name: Project name, optional
    Returns:
        API JSON response
    """
    params = {}
    if tenant_name:
        params["TenantName"] = tenant_name
    if project_name:
        params["ProjectName"] = project_name
    return client.get("/drapi/ai/instanceMessage", params=params)


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Get database instance list under tenant/project")
    parser.add_argument("--tenant", default=None, help="Tenant name")
    parser.add_argument("--project", default=None, help="Project name")
    args = parser.parse_args()

    try:
        result = get_instance(args.tenant, args.project)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
