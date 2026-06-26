#!/usr/bin/env python3
"""
获取 Teambition 项目任务类型（场景类型）列表
用法: uv run scripts/get_scenario_types.py <projectId> [选项]

调用 /v3/project/{projectId}/scenariofieldconfig/search 接口
任务类型 ID（sfcId）可用于创建任务时指定类型，或过滤自定义字段
"""

import json
import sys

import call_api


def get_scenario_types(
    project_id: str,
    sfc_ids: str | None = None,
    q: str | None = None,
) -> None:
    params = {}
    if sfc_ids:
        params["sfcIds"] = sfc_ids
    if q:
        params["q"] = q

    data = call_api.get(f"v3/project/{project_id}/scenariofieldconfig/search", params=params)
    scenario_types = data.get("result", [])
    print(json.dumps(scenario_types, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("""用法: uv run scripts/get_scenario_types.py <projectId> [选项]

参数:
  projectId           项目 ID（必需）

选项:
  --sfc-ids <IDs>     任务类型 ID 列表，逗号分隔（可选）
  --q <关键词>        按名称模糊搜索任务类型（可选）

示例:
  # 获取项目所有任务类型
  uv run scripts/get_scenario_types.py 67ec9b8c3c6130ac88605c3e

  # 按名称搜索任务类型
  uv run scripts/get_scenario_types.py 67ec9b8c3c6130ac88605c3e --q 需求
  uv run scripts/get_scenario_types.py 67ec9b8c3c6130ac88605c3e --q 缺陷

  # 获取指定 ID 的任务类型
  uv run scripts/get_scenario_types.py 67ec9b8c3c6130ac88605c3e \\
    --sfc-ids 67ec9b8c3c6130ac88605c3f

提示:
  - 返回的 id 字段即为 sfcId，可用于 get_custom_fields.py --sfc-id 过滤字段
  - 创建任务时可通过 sfcId 指定任务类型""")
        sys.exit(0 if "--help" in sys.argv else 1)

    project_id = sys.argv[1]
    sfc_ids = None
    q = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--sfc-ids" and i + 1 < len(sys.argv):
            sfc_ids = sys.argv[i + 1]
            i += 2
        elif arg == "--q" and i + 1 < len(sys.argv):
            q = sys.argv[i + 1]
            i += 2
        else:
            print(f"错误: 未知参数 {arg}", file=sys.stderr)
            sys.exit(1)

    get_scenario_types(project_id, sfc_ids, q)


if __name__ == "__main__":
    main()
