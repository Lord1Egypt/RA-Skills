import os
import sys
import json
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.activate_cluster_plan.service import activate_cluster_plan

COMMAND_NAME = "activate_cluster_plan"
COMMAND_DESC = "开启 AI 客群运营计划"

REACH_TYPE_MAP = {1: "旺旺", 2: "短信", 3: "邮件"}

# snake_case → camelCase 字段映射（agent 误传时自动兜底）
_SNAKE_TO_CAMEL = {
    "plan_id": "planId",
    "plan_ds": "planDs",
    "cluster_main_tag": "clusterMainTag",
    "buyer_type": "buyerType",
    "sale_description": "saleDescription",
    "reach_type": "reachType",
    "reach_type_list": "reachTypeList",
}


def _normalize_keys(plan_data: dict) -> dict:
    """把 snake_case 字段名自动转为 camelCase（agent 误传兜底）。已是 camelCase 的字段保留。"""
    normalized = {}
    for k, v in plan_data.items():
        new_key = _SNAKE_TO_CAMEL.get(k, k)
        # 若 camelCase 版本已存在，保留 camelCase 的值（优先），避免覆盖
        if new_key in normalized:
            continue
        normalized[new_key] = v
    return normalized


def _render_markdown(plan_data: dict, result: dict, already_exists: bool = False) -> str:
    plan_id = plan_data.get("planId", "—")
    reach_label = "旺旺"
    status_text = "ℹ️ 运营计划已存在（无需重复创建）" if already_exists else "✅ 运营计划已开启"

    lines = [
        "<!-- MODULE: activate_cluster_plan -->",
        status_text,
        "",
        f"- **planId**: {plan_id}",
        f"- **触达方式**: {reach_label}",
        "",
        f"运营方案会智能进行，推送效果可以在 [CRM管理](https://air.1688.com/app/CSBC-modules/csbc-ai-component-loader/crm.html?rapidTab=old&showPlanId={plan_id}) 中查看。",
        "",
        "<!-- /MODULE: activate_cluster_plan -->",
    ]
    return "\n".join(lines)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，请运行：`python cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--plan-json", required=True,
                        help="运营计划 JSON 字符串（含 planId/planDs/clusterMainTag 等字段）")
    args = parser.parse_args()

    try:
        plan_data = json.loads(args.plan_json)
    except json.JSONDecodeError as e:
        print_output(False, f"❌ --plan-json 解析失败：{e}", {"data": {}})
        return

    # snake_case → camelCase 自动兜底（agent 误传时不会因字段名失败）
    plan_data = _normalize_keys(plan_data)

    try:
        result = activate_cluster_plan(plan_data)
        already_exists = result.get("already_exists", False)
        print_output(True, _render_markdown(plan_data, result, already_exists=already_exists), {"data": result})
    except ValueError as e:
        print_output(False, f"❌ 参数错误：{e}", {"data": {}})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
