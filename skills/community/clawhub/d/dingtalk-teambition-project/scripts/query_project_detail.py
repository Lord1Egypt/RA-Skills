#!/usr/bin/env python3
"""
查询 Teambition 项目详情（支持逗号分隔批量查询）
用法: uv run scripts/query_project_detail.py <projectId[,projectId,...]> [--detail-level simple|detailed] [--extra-fields f1,f2]
"""

import json
import sys
from typing import Any, Dict, List, Optional

import call_api

SIMPLE_FIELDS = {
    "id", "name", "description", "visibility", "isTemplate",
    "creatorId", "isArchived", "isSuspended", "created", "updated",
}


def format_simple(project: Dict[str, Any], extra_fields: Optional[List[str]] = None) -> Dict[str, Any]:
    result = {k: project.get(k) for k in SIMPLE_FIELDS}
    if extra_fields:
        for f in extra_fields:
            result[f] = project.get(f)
    return result


def query_project_detail(
    project_ids: str,
    detail_level: str = "simple",
    extra_fields: Optional[List[str]] = None,
) -> None:
    data = call_api.get("v3/project/query", params={"projectId": project_ids})
    projects: List[Dict[str, Any]] = data.get("result", [])

    if not projects:
        print(json.dumps([], ensure_ascii=False, indent=2))
        return

    if detail_level == "simple":
        projects = [format_simple(p, extra_fields) for p in projects]

    print(json.dumps(projects, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("""用法: uv run scripts/query_project_detail.py <projectId[,projectId,...]> [选项]

参数:
  projectId            项目 ID，多个用逗号分隔

选项:
  --detail-level       simple（默认）或 detailed
  --extra-fields       额外字段，逗号分隔（如 logo,organizationId）
  --help               显示帮助

示例:
  uv run scripts/query_project_detail.py 67ec9b8c3c6130ac88605c3e
  uv run scripts/query_project_detail.py id1,id2 --detail-level detailed
  uv run scripts/query_project_detail.py id1 --extra-fields organizationId,startDate""")
        sys.exit(0 if "--help" in sys.argv else 1)

    project_ids = sys.argv[1]
    detail_level = "simple"
    extra_fields: Optional[List[str]] = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--detail-level" and i + 1 < len(sys.argv):
            detail_level = sys.argv[i + 1]; i += 2
        elif arg == "--extra-fields" and i + 1 < len(sys.argv):
            extra_fields = [f.strip() for f in sys.argv[i + 1].split(",")]; i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr); sys.exit(1)

    query_project_detail(project_ids, detail_level, extra_fields)


if __name__ == "__main__":
    main()
