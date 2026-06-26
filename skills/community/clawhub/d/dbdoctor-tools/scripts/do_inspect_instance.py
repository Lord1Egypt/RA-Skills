"""
do_inspect_instance.py - Execute instance inspection

Trigger inspection task for database instance.
Two-step call: first get inspection template ID, then execute inspection.
"""

import argparse
import json
import sys

from common import client
from common.config import config


def do_inspect_instance(instance_id: str, tenant: str = "", project: str = "") -> dict:
    """
    Execute instance inspection.

    Steps:
    1. Get inspection template ID
    2. Execute inspection task using template ID

    Args:
        instance_id: Instance ID
        tenant: Tenant name (optional, used to generate jump link)
        project: Project name (optional, used to generate jump link)
    Returns:
        Inspection execution result
    """
    # Step 1: Get inspection template ID
    template_resp = client.get(
        "/inspect/QueryTemplatePolicysByInstance",
        params={
            "InstanceId": instance_id,
            "UserId": config.user_id,
        },
    )

    # Check if template exists
    template_data = template_resp.get("Data", []) or template_resp.get("data", [])
    if not template_data or len(template_data) == 0:
        return {"error": "No associated template found for current instance. Please associate a template before inspection."}

    # Get first template ID
    temp_info = template_data[0]
    if temp_info is None:
        return {"error": "No associated template found for current instance. Please associate a template before inspection."}

    template_id = temp_info.get("id") or temp_info.get("Id") or temp_info.get("templateId") or temp_info.get("TemplateId", "")
    if not template_id:
        return {"error": "Unable to get template ID"}

    # Step 2: Execute inspection
    response = client.get(
        "/inspect/ExecuteInspectTaskByInstance",
        params={
            "InstanceIds": instance_id,
            "TemplateIds": template_id,
            "UserId": config.user_id,
        },
    )

    # Check execution result
    if response.get("Code") != 200 and response.get("code") != 200:
        message = response.get("Message") or response.get("message", "Unknown error")
        return {"error": f"Inspection failed. Please verify DBDoctor server is running or instance ID is correct. Message: {message}"}

    # Generate return info
    result = {
        "message": "Inspection operation completed",
        "instanceId": instance_id,
        "templateId": template_id,
    }

    # If tenant and project info exist, add jump link
    if tenant and project:
        inspection_route_path = f"{config.base_url}/#/dbDoctor/{tenant}/{project}/{config.role}/index/instance-diagnosis/{instance_id}/dbdoctor-inspect-list?cluster=idc"
        result["inspectionRoutePath"] = inspection_route_path
        result["suggestion"] = f"Click to jump to inspection console: {inspection_route_path}"

    return result


def main():
    """Command line entry"""
    parser = argparse.ArgumentParser(description="Execute database instance inspection")
    parser.add_argument("--instance-id", required=True, help="Instance ID")
    parser.add_argument("--tenant", default="", help="Tenant name (optional, used to generate jump link)")
    parser.add_argument("--project", default="", help="Project name (optional, used to generate jump link)")
    args = parser.parse_args()

    try:
        result = do_inspect_instance(args.instance_id, args.tenant, args.project)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
