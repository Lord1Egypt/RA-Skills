#!/usr/bin/env python3
"""客户筛选配置查询 CLI入口"""

import json
import os
import sys

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import JsonArgumentParser, print_output, print_error, unwrap_payload
from capabilities.customer_field_config.service import customer_field_config

COMMAND_NAME = "alibaba.1688.customer.attr.field.config"
COMMAND_DESC = "获取当前商家可用的筛选维度"

# 黑名单：data 输出时剔除的无效字段
_ATTR_BLACKLIST = {"class", "id", "source", "isSystem", "isFilterable"}
_TAG_BLACKLIST = {"class", "id", "isSystem", "sellerId"}

# 后端 activeAttrs 存在重复项与命名错位，统一在客户端归一：
# - merch_tags 与 tags 等价（实测两者筛选结果一致），统一声明为 tags，与返回字段名对齐
_ATTR_KEY_RENAME = {"merch_tags": "tags"}

# - buyer_nick 重复两次且元数据互相矛盾（买家昵称/客户信息、string/String），固定为单一口径
_ATTR_OVERRIDE = {
    "buyer_nick": {"attrLabel": "买家昵称", "attrType": "String"},
}

# - attrType 大小写混用（string / String），统一为首字母大写；
#   number 等属于真实类型差异，不做改写
_ATTR_TYPE_CANON = {"string": "String"}


def _normalize_active_attrs(attrs) -> list:
    """归一 activeAttrs：重命名别名 attrKey、统一 attrType 大小写、修正矛盾元数据、按 attrKey 去重（保留首次出现）"""
    normalized, seen = [], set()
    for attr in attrs or []:
        if not isinstance(attr, dict):
            continue
        item = dict(attr)
        key = _ATTR_KEY_RENAME.get(item.get("attrKey"), item.get("attrKey"))
        item["attrKey"] = key
        attr_type = item.get("attrType")
        if isinstance(attr_type, str):
            item["attrType"] = _ATTR_TYPE_CANON.get(attr_type, attr_type)
        item.update(_ATTR_OVERRIDE.get(key, {}))
        if key in seen:
            continue
        seen.add(key)
        normalized.append(item)
    return normalized


def _truncate(val, max_len=50):
    """截断过长字符串"""
    if val is None:
        return "—"
    s = str(val)
    if len(s) > max_len:
        return s[:max_len] + "..."
    return s


def _render_markdown(data: dict) -> str:
    lines = ["# 📋 筛选配置", ""]

    active_attrs = data.get("activeAttrs") or []
    filterable_tags = data.get("filterableTags") or []

    # 仅保留 isActive == 1 的记录
    active_attrs = [a for a in active_attrs if a.get("isActive") == 1]

    if active_attrs:
        lines.append("## 可筛选的属性列表")
        lines.append("")
        lines.append(f"共 **{len(active_attrs)}** 个属性：")
        lines.append("")
        lines.append("| 属性编码 | 显示名 | 类型 | 示例值 |")
        lines.append("|----------|--------|------|--------|")
        for attr in active_attrs:
            key = attr.get("attrKey", "—")
            label = attr.get("attrLabel", "—")
            t = attr.get("attrType", "string")
            example = _truncate(attr.get("example"))
            lines.append(f"| {key} | {label} | {t} | {example} |")
        lines.append("")

    if filterable_tags:
        lines.append("## 可用标签（tags列属性值）")
        lines.append("")
        lines.append(f"共 **{len(filterable_tags)}** 个标签：")
        lines.append("")
        for tag in filterable_tags:
            lines.append(f"- {tag.get('tag', '—')}")
        lines.append("")

    if not active_attrs and not filterable_tags:
        lines.append("> 暂无可用的筛选维度")

    return "\n".join(lines)


def _slim_data(data: dict) -> dict:
    """黑名单方式剔除 activeAttrs / filterableTags 中的无效字段"""
    result = {}
    if "activeAttrs" in data:
        result["activeAttrs"] = [
            {k: v for k, v in item.items() if k not in _ATTR_BLACKLIST}
            for item in (data["activeAttrs"] or [])
        ]
    if "filterableTags" in data:
        result["filterableTags"] = [
            {k: v for k, v in item.items() if k not in _TAG_BLACKLIST}
            for item in (data["filterableTags"] or [])
        ]
    # 保留其他顶层字段
    for k, v in data.items():
        if k not in ("activeAttrs", "filterableTags"):
            result[k] = v
    return result


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未注入，请检查框架环境变量 ALI_1688_AK 是否已配置", {})
        return 2

    parser = JsonArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--raw", action="store_true", default=False, help="输出完整 data 字段（默认仅输出 markdown）")
    args = parser.parse_args()

    try:
        result = customer_field_config()
        data = unwrap_payload(result)
        if not isinstance(data, dict):
            data = {}
        if "activeAttrs" in data:
            data["activeAttrs"] = _normalize_active_attrs(data.get("activeAttrs"))

        if args.raw:
            # --raw 模式：输出精简后的 data
            print(json.dumps({"success": True, "data": _slim_data(data)}, ensure_ascii=False, indent=2))
        else:
            # 默认模式：仅输出 markdown
            print(json.dumps({"success": True, "markdown": _render_markdown(data)}, ensure_ascii=False, indent=2))
        return 0
    except Exception as e:
        return print_error(e, {})


if __name__ == "__main__":
    sys.exit(main())
