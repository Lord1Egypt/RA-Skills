#!/usr/bin/env python3
"""
获取 Teambition 项目自定义字段配置
用法: uv run scripts/get_custom_fields.py <projectId> [选项]

调用 /v3/project/{projectId}/customfield/search 接口
"""

import json
import sys

import call_api


def get_custom_fields(
    project_id: str,
    cf_ids: str | None = None,
    sfc_id: str | None = None,
) -> None:
    params = {}
    if cf_ids:
        params["cfIds"] = cf_ids
    if sfc_id:
        params["sfcId"] = sfc_id

    data = call_api.get(f"v3/project/{project_id}/customfield/search", params=params)
    fields = data.get("result", [])
    # 为每个字段添加 customfieldId 字段，方便后续更新操作使用
    # API 返回的 id 字段在更新时需要作为 customfieldId 使用
    for field in fields:
        if "id" in field and "customfieldId" not in field:
            field["customfieldId"] = field["id"]
    print(json.dumps(fields, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("""用法: uv run scripts/get_custom_fields.py <projectId> [选项]

参数:
  projectId           项目 ID（必需）

选项:
  --cf-ids <IDs>      自定义字段 ID 列表，逗号分隔（可选）
  --sfc-id <ID>       任务类型 ID，过滤该类型相关的字段（可选）

示例:
  # 获取项目所有自定义字段
  uv run scripts/get_custom_fields.py 67ec9b8c3c6130ac88605c3e

  # 获取指定字段
  uv run scripts/get_custom_fields.py 67ec9b8c3c6130ac88605c3e \\
    --cf-ids 67ec9b8c3c6130ac88605c3f,67ec9b8c3c6130ac88605c40

  # 获取特定任务类型的字段
  uv run scripts/get_custom_fields.py 67ec9b8c3c6130ac88605c3e \\
    --sfc-id 67ec9b8c3c6130ac88605c3f

提示: projectId 可从项目列表获取：
  uv run scripts/query_projects.py --tql "creatorId = me()" """)
        sys.exit(0 if "--help" in sys.argv else 1)

    project_id = sys.argv[1]
    cf_ids = None
    sfc_id = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--cf-ids" and i + 1 < len(sys.argv):
            cf_ids = sys.argv[i + 1]
            i += 2
        elif arg == "--sfc-id" and i + 1 < len(sys.argv):
            sfc_id = sys.argv[i + 1]
            i += 2
        else:
            print(f"错误: 未知参数 {arg}", file=sys.stderr)
            sys.exit(1)

    get_custom_fields(project_id, cf_ids, sfc_id)


if __name__ == "__main__":
    main()
