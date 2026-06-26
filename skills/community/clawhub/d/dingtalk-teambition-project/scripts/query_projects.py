#!/usr/bin/env python3
"""
查询 Teambition 项目列表（TQL）
用法: uv run scripts/query_projects.py [--tql <TQL>] [--page-size N] [--no-details] [--include-template]
"""

import json
import sys
from typing import Any, Dict, List, Optional

import call_api


def query_projects(
    tql: Optional[str] = None,
    page_size: Optional[int] = None,
    page_token: Optional[str] = None,
    fetch_details: bool = True,
    include_template: bool = False,
) -> None:
    params: Dict[str, Any] = {}
    if tql:
        # 自动追加排除模板条件（除非用户明确要求包含）
        if not include_template and "isTemplate" not in tql:
            tql = f"({tql}) AND isTemplate = false"
        params["tql"] = tql
    else:
        if not include_template:
            params["tql"] = "isTemplate = false"
    if page_size:
        params["pageSize"] = page_size
    if page_token:
        params["pageToken"] = page_token

    data = call_api.get("project/search", params=params)
    project_ids: List[str] = data.get("result", [])
    next_page_token = data.get("nextPageToken")
    total = data.get("count", len(project_ids))

    print(f"共找到 {total} 个项目，本页 {len(project_ids)} 个。", file=sys.stderr)

    if not project_ids:
        print(json.dumps([], ensure_ascii=False, indent=2))
        return

    if not fetch_details:
        print(json.dumps(project_ids, ensure_ascii=False, indent=2))
        if next_page_token:
            print(f"nextPageToken: {next_page_token}", file=sys.stderr)
        return

    # 批量查询项目详情（使用 projectIds 参数）
    ids_str = ",".join(project_ids)
    detail_data = call_api.get("v3/project/query", params={"projectIds": ids_str})
    projects: List[Dict[str, Any]] = detail_data.get("result", [])

    output = {
        "projects": projects,
        "count": len(projects),
        "total": total,
    }
    if next_page_token:
        output["nextPageToken"] = next_page_token

    print(json.dumps(output, ensure_ascii=False, indent=2))


def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/query_projects.py [选项]

选项:
  --tql <TQL>            项目查询语言（可选）
  --page-size <N>        每页大小
  --page-token <T>       分页令牌
  --no-details           只返回项目 ID 列表
  --include-template     包含模板项目（默认排除）
  --help                 显示帮助

TQL 常用示例:
  "involveMembers = me()"              我参与的项目
  "creatorId = me()"                   我创建的项目
  "nameText ~ '电商'"                  名称包含"电商"
  "isSuspended = false"                未归档项目

完整 TQL 语法: references/project-tql.md""")
        sys.exit(0)

    tql = None
    page_size = None
    page_token = None
    fetch_details = True
    include_template = False

    i = 1
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--tql" and i + 1 < len(sys.argv):
            tql = sys.argv[i + 1]; i += 2
        elif arg == "--page-size" and i + 1 < len(sys.argv):
            page_size = int(sys.argv[i + 1]); i += 2
        elif arg == "--page-token" and i + 1 < len(sys.argv):
            page_token = sys.argv[i + 1]; i += 2
        elif arg == "--no-details":
            fetch_details = False; i += 1
        elif arg == "--include-template":
            include_template = True; i += 1
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    query_projects(tql, page_size, page_token, fetch_details, include_template)


if __name__ == "__main__":
    main()
