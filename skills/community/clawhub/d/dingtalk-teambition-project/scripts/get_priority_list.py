#!/usr/bin/env python3
"""
获取 Teambition 企业优先级配置列表
用法: uv run scripts/get_priority_list.py <organizationId>

组织 ID 可从项目详情的 organizationId 字段获取：
  uv run scripts/query_project_detail.py <projectId> --extra-fields organizationId
"""

import json
import sys

import call_api


def get_priority_list(organization_id: str) -> None:
    data = call_api.get("v3/project/priority/list", params={"organizationId": organization_id})
    priorities = data.get("result", [])
    print(json.dumps(priorities, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("""用法: uv run scripts/get_priority_list.py <organizationId>

参数:
  organizationId    企业/组织 ID

示例:
  uv run scripts/get_priority_list.py 67ec9b8c3c6130ac88605c3e

提示: 组织 ID 可从项目详情获取：
  uv run scripts/query_project_detail.py <projectId> --extra-fields organizationId""")
        sys.exit(0 if "--help" in sys.argv else 1)

    get_priority_list(sys.argv[1])


if __name__ == "__main__":
    main()
