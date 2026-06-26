"""
get_current_user.py - Get current user info

Get tenant and project information for current logged-in user.
API: GET /nephele/currentUser
"""

import argparse
import json
import sys

from common import client


def get_current_user() -> dict:
    """
    Get tenant and project information for current user.

    Returns:
        Dictionary containing user, tenant, project info
    """
    return client.get("/nephele/currentUser")


def extract_tenant_project_list(data: dict) -> list:
    """
    Extract tenant-project list from response data.

    Args:
        data: API response data
    Returns:
        Tenant-project list, format: [{"tenant": "xxx", "project": "yyy", "namespace": "xxx-yyy"}]
    """
    result = []
    tenant_mapping = data.get("data", {}).get("tenantMapping", [])

    for tenant_info in tenant_mapping:
        tenant_name = tenant_info.get("name", "")
        k8s_namespaces = tenant_info.get("k8sNamespaces", [])

        for ns in k8s_namespaces:
            namespace = ns.get("namespace", "")
            # namespace format: tenant-project
            # Tenant name itself may contain "-", so use tenant name length to split
            if namespace.startswith(tenant_name + "-"):
                project = namespace[len(tenant_name) + 1:]  # +1 to skip "-"
            else:
                # If namespace doesn't start with tenant name, try splitting by last "-"
                parts = namespace.rsplit("-", 1)
                if len(parts) == 2:
                    project = parts[1]
                else:
                    project = namespace

            result.append({
                "tenant": tenant_name,
                "project": project,
                "namespace": namespace,
                "roles": ns.get("roles", [])
            })

    return result


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(
        description="Get tenant and project info for current user"
    )
    parser.add_argument(
        "--extract",
        action="store_true",
        help="Output simplified tenant-project list only"
    )
    args = parser.parse_args()

    try:
        result = get_current_user()

        if args.extract and result.get("success"):
            # Output simplified tenant-project list
            extracted = extract_tenant_project_list(result)
            output = {
                "username": result.get("data", {}).get("username", ""),
                "userId": result.get("data", {}).get("userId", ""),
                "tenantProjects": extracted
            }
            print(json.dumps(output, ensure_ascii=False, indent=2))
        else:
            # Output full response
            print(json.dumps(result, ensure_ascii=False, indent=2))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
