#!/usr/bin/env python3
"""
查询 Teambition 任务列表（TQL）
用法: uv run scripts/query_tasks.py [--tql <TQL>] [--page-size N] [--page-token T] [--no-details]
"""

import json
import sys
from typing import Any, Dict, List, Optional

import call_api

# 系统默认优先级名称（兜底值，企业未配置时使用）
DEFAULT_PRIORITY_LABEL = {0: "紧急", 1: "高", 2: "中", 3: "低"}

# 缓存企业优先级配置，key 为 organizationId
_priority_label_cache: Dict[str, Dict[int, str]] = {}

# 文件下载链接有效期：7天（604800秒），API支持的最长有效期
FILE_URL_EXPIRE_SECONDS = 604800

# 默认请求的额外字段。
# v3/task/query 接口默认已返回：id、content、isDone、executorId、projectId、
# dueDate、priority、created、updated 等核心字段。
# 以下字段需要通过 fields 参数额外请求：
DEFAULT_EXTRA_FIELDS = [
    "note",        # 备注
    "sprintId",    # 所属迭代 ID
    "stageId",     # 所属任务列 ID
    "startDate",   # 开始时间
    "progress",    # 进度（0-100）
    "parentTaskId", # 父任务 ID（子任务场景）
]

def _extract_resource_id(meta_string: Optional[str]) -> Optional[str]:
    """从 metaString 中解析 resourceId"""
    if not meta_string:
        return None
    try:
        meta = json.loads(meta_string)
        return meta.get("resourceId")
    except json.JSONDecodeError:
        return None

def enrich_file_custom_fields(task: Dict[str, Any]) -> None:
    """
    为文件类型的自定义字段补齐下载链接。
    """
    customfields = task.get("customfields", [])
    if not customfields:
        return

    # 收集所有文件类型的 resourceId
    resource_ids = []
    file_entries = []  # 记录 (cf_index, value_index, entry) 用于回填

    for cf_idx, cf in enumerate(customfields):
        if cf.get("type") != "work":
            continue
        value = cf.get("value", [])
        if not isinstance(value, list):
            continue
        for val_idx, entry in enumerate(value):
            if not isinstance(entry, dict):
                continue
            resource_id = _extract_resource_id(entry.get("metaString"))
            if resource_id:
                resource_ids.append(resource_id)
                file_entries.append((cf_idx, val_idx, entry, resource_id))

    if not resource_ids:
        return

    # 批量查询文件详情
    try:
        resp = call_api.post(
            "v3/file/query/by-resource-ids",
            body={
                "needSign": True,
                "resourceIds": resource_ids,
                "expireAfterSeconds": FILE_URL_EXPIRE_SECONDS,
            },
            headers={"X-Canary": "prepub"}
        )
        file_details = {f.get("resourceId"): f for f in resp.get(
            "result", []) if f.get("resourceId")}
    except Exception:
        # 查询失败时静默处理，不中断主流程
        return

    # 回填 downloadUrl
    for cf_idx, val_idx, entry, resource_id in file_entries:
        detail = file_details.get(resource_id)
        if detail and detail.get("downloadUrl"):
            entry["downloadUrl"] = detail["downloadUrl"]

def get_priority_label_map(project_id: str) -> Dict[int, str]:
    """
    获取企业优先级名称映射。
    直接查询企业优先级配置，失败时静默返回默认映射，不中断主流程。
    """
    # 检查缓存
    if project_id in _priority_label_cache:
        return _priority_label_cache[project_id]

    try:
        # 获取企业优先级配置（无需传参）
        resp = call_api.get("v3/project/priority/list")
        priorities = resp.get("result", [])
        if priorities:
            label_map = {int(p["priority"]): p["name"] for p in priorities if "priority" in p and "name" in p}
            _priority_label_cache[project_id] = label_map
            return label_map
    except Exception:
        # 查询失败时静默处理，使用默认值
        pass

    return DEFAULT_PRIORITY_LABEL

# 缓存项目自定义字段配置，避免重复请求
_custom_field_cache: Dict[str, Dict[str, str]] = {}

def enrich_custom_field_names(task: Dict[str, Any]) -> None:
    """
    为自定义字段补齐字段名称（cfName）。
    根据 projectId 获取项目自定义字段配置，构建 cfId -> name 映射。
    """
    customfields = task.get("customfields", [])
    if not customfields:
        return

    project_id = task.get("projectId")
    if not project_id:
        return

    # 检查缓存
    if project_id not in _custom_field_cache:
        try:
            resp = call_api.get(
                f"v3/project/{project_id}/customfield/search")
            fields = resp.get("result", [])
            # 构建 cfId -> name 映射（尝试 id 和 _id 两个字段）
            _custom_field_cache[project_id] = {}
            for f in fields:
                cf_id = f.get("id") or f.get("_id")
                if cf_id:
                    _custom_field_cache[project_id][cf_id] = f.get("name")
        except Exception:
            # 查询失败时静默处理，不中断主流程
            return

    name_map = _custom_field_cache.get(project_id, {})
    if not name_map:
        return

    # 为每个自定义字段添加 cfName
    for cf in customfields:
        cf_id = cf.get("cfId")
        if cf_id and cf_id in name_map:
            cf["cfName"] = name_map[cf_id]

def query_tasks(
    tql: Optional[str] = None,
    page_size: Optional[int] = 50,
    page_token: Optional[str] = None,
    fetch_details: bool = True,
    extra_fields: Optional[List[str]] = None,
) -> None:
    # Step 1: 查询任务 ID 列表
    params: Dict[str, Any] = {}
    if tql:
        params["tql"] = tql
    if page_size:
        params["pageSize"] = page_size
    else:
        params["pageSize"] = 50
    if page_token:
        params["pageToken"] = page_token

    data = call_api.get("v2/all-task/search", params=params)
    task_ids: List[str] = data.get("result", [])
    next_page_token = data.get("nextPageToken")
    total = data.get("count", len(task_ids))

    print(f"共找到 {total} 个任务，本页 {len(task_ids)} 个。", file=sys.stderr)

    if not task_ids:
        print(json.dumps([], ensure_ascii=False, indent=2))
        return

    if not fetch_details:
        print(json.dumps(task_ids, ensure_ascii=False, indent=2))
        if next_page_token:
            print(f"nextPageToken: {next_page_token}", file=sys.stderr)
        return

    # Step 2: 批量查询详情
    ids_str = ",".join(task_ids)
    detail_params: Dict[str, Any] = {"taskId": ids_str}
    # 合并默认字段和用户指定的额外字段
    fields = list(set(DEFAULT_EXTRA_FIELDS + (extra_fields or [])))
    detail_params["fields"] = ",".join(fields)
    detail_data = call_api.get("v3/task/query", params=detail_params)
    tasks: List[Dict[str, Any]] = detail_data.get("result", [])

    # 格式化输出：优先级转中文（自动获取企业配置），同时补齐文件下载链接和自定义字段名称
    for t in tasks:
        p = t.get("priority")
        if p is not None:
            project_id = t.get("projectId", "")
            label_map = get_priority_label_map(project_id) if project_id else DEFAULT_PRIORITY_LABEL
            t["priorityLabel"] = label_map.get(p, str(p))
        # 为文件类型的自定义字段补齐下载链接
        enrich_file_custom_fields(t)
        # 为自定义字段补齐字段名称
        enrich_custom_field_names(t)

    output = {
        "tasks": tasks,
        "count": len(tasks),
        "total": total,
    }
    if next_page_token:
        output["nextPageToken"] = next_page_token

    print(json.dumps(output, ensure_ascii=False, indent=2))

def main() -> None:
    if "--help" in sys.argv:
        print("""用法: uv run scripts/query_tasks.py [选项]

选项:
  --tql <TQL>              任务查询语言（可选）
  --page-size <N>          每页大小（可选）
  --page-token <T>         分页令牌（可选）
  --no-details             只返回任务 ID 列表，不查询详情
  --extra-fields <字段>    额外获取的字段，逗号分隔（如 sprintId,content）
                           注：note 字段默认已包含，无需额外指定
  --help                   显示帮助

TQL 常用示例:
  "executorId = me() AND isDone = false"                    我的待办任务
  "executorId = me() AND isDone = false AND dueDate < startOf(d)"  我的逾期任务
  "dueDate >= startOf(w) AND dueDate <= endOf(w)"           本周截止
  "dueDate >= startOf(d) AND dueDate <= endOf(d)"           今天截止
  "title ~ '关键词'"                                         标题模糊搜索
  "projectId = 'xxx'"                                       指定项目

完整 TQL 语法: references/tql.md""")
        sys.exit(0)

    tql = None
    page_size = None
    page_token = None
    fetch_details = True
    extra_fields: Optional[List[str]] = None

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
        elif arg == "--extra-fields" and i + 1 < len(sys.argv):
            extra_fields = [f.strip() for f in sys.argv[i + 1].split(",")]; i += 2
        else:
            print(f"❌ 未知参数: {arg}，使用 --help 查看帮助", file=sys.stderr)
            sys.exit(1)

    query_tasks(tql, page_size, page_token, fetch_details, extra_fields)

if __name__ == "__main__":
    main()