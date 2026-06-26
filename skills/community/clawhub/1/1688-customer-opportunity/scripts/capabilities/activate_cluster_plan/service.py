# scripts/capabilities/activate_cluster_plan/service.py
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _http import api_post
from _errors import ServiceError

REQUIRED_FIELDS = [
    "planId", "planDs", "clusterMainTag", "buyerType", "saleDescription",
]


def activate_cluster_plan(plan_data: dict) -> dict:
    for field in REQUIRED_FIELDS:
        val = plan_data.get(field)
        if val is None or val == "":
            raise ValueError(f"{field} 不能为空")
    plan_id = plan_data.get("planId", "")
    crm_url = f"https://air.1688.com/app/CSBC-modules/csbc-ai-component-loader/crm.html?rapidTab=old&showPlanId={plan_id}"

    try:
        result = api_post("/api/activate_cluster_plan/1.0.0", plan_data)
        result["crm_url"] = crm_url
        return result
    except ServiceError as e:
        if "已生成" in str(e) or "重复配置" in str(e):
            return {"already_exists": True, "crm_url": crm_url}
        raise
