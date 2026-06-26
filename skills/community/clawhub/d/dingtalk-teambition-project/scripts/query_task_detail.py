#!/usr/bin/env python3
"""
查询 Teambition 任务详情（支持逗号分隔批量查询）
用法: uv run scripts/query_task_detail.py <taskId[,taskId,...]> [--detail-level simple|detailed] [--extra-fields f1,f2]
"""

import json
import sys
from typing import Any, Dict, List, Optional

import call_api

# 系统默认优先级名称（兜底值，企业未配置时使用）
DEFAULT_PRIORITY_LABEL = {0: "紧急", 1: "高", 2: "中", 3: "低"}

# 缓存优先级配置
_priority_label_cache: Optional[Dict[int, str]] = None

def get_priority_label_map() -> Dict[int, str]:
    """
    获取优先级名称映射。
    直接查询优先级配置，无需 organizationId。
    失败时静默返回默认映射，不中断主流程。
    """
    global _priority_label_cache
    if _priority_label_cache is not None:
        return _priority_label_cache

    try:
        resp = call_api.get("v3/project/priority/list")
        priorities = resp.get("result", [])
        if priorities:
            label_map = {int(p["priority"]): p["name"] for p in priorities if "priority" in p and "name" in p}
            _priority_label_cache = label_map
            return label_map
    except Exception:
        pass

    return DEFAULT_PRIORITY_LABEL

# 文件下载链接有效期：7天（604800秒），API支持的最长有效期
FILE_URL_EXPIRE_SECONDS = 604800

SIMPLE_FIELDS = {"id", "content", "isDone", "executorId", "projectId", "dueDate", "priority", "created", "updated", "note"}

def format_simple(task: Dict[str, Any], extra_fields: Optional[List[str]] = None) -> Dict[str, Any]:
    result = {k: task.get(k) for k in SIMPLE_FIELDS}
    if extra_fields:
        for f in extra_fields:
            result[f] = task.get(f)
    p = result.get("priority")
    if p is not None:
        label_map = get_priority_label_map()
        result["priorityLabel"] = label_map.get(p, str(p))
    return result


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
    仅在 detailed 模式下调用。
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


def query_task_detail(
    task_ids: str,
    detail_level: str = "detailed",
    extra_fields: Optional[List[str]] = None,
) -> None:
    data = call_api.get("v3/task/query", params={"taskId": task_ids})
    tasks: List[Dict[str, Any]] = data.get("result", [])

    if not tasks:
        print(json.dumps([], ensure_ascii=False, indent=2))
        return

    if detail_level == "simple":
        tasks = [format_simple(t, extra_fields) for t in tasks]
    else:
        # detailed: 补充 priorityLabel（自动获取企业优先级配置）
        for t in tasks:
            p = t.get("priority")
            if p is not None:
                label_map = get_priority_label_map()
                t["priorityLabel"] = label_map.get(p, str(p))
            # 为文件类型的自定义字段补齐下载链接
            enrich_file_custom_fields(t)
            # 为自定义字段补齐字段名称
            enrich_custom_field_names(t)

    print(json.dumps(tasks, ensure_ascii=False, indent=2))


def main() -> None:
    if len(sys.argv) < 2 or "--help" in sys.argv:
        print("""用法: uv run scripts/query_task_detail.py <taskId[,taskId,...]> [选项]

参数:
  taskId               任务 ID，多个用逗号分隔（批量查询，无需多次调用）

选项:
  --detail-level       detailed（默认）或 simple
  --extra-fields       简单模式下额外字段，逗号分隔（如 note,sprintId）
  --help               显示帮助

示例:
  uv run scripts/query_task_detail.py 67ec9b8c3c6130ac88605c3e
  uv run scripts/query_task_detail.py id1,id2,id3
  uv run scripts/query_task_detail.py id1 --detail-level detailed
  uv run scripts/query_task_detail.py id1 --extra-fields note,stageId""")
        sys.exit(0 if "--help" in sys.argv else 1)

    task_ids = sys.argv[1]
    detail_level = "detailed"
    extra_fields: Optional[List[str]] = None

    i = 2
    while i < len(sys.argv):
        arg = sys.argv[i]
        if arg == "--detail-level" and i + 1 < len(sys.argv):
            detail_level = sys.argv[i + 1]; i += 2
        elif arg == "--extra-fields" and i + 1 < len(sys.argv):
            extra_fields = [f.strip() for f in sys.argv[i + 1].split(",")]; i += 2
        else:
            print(f"❌ 未知参数: {arg}", file=sys.stderr)
            sys.exit(1)

    query_task_detail(task_ids, detail_level, extra_fields)


if __name__ == "__main__":
    main()