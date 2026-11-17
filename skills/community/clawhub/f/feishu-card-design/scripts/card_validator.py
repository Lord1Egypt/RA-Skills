#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
feishu-card-design 卡片 JSON 验证工具

验证一份飞书卡片 JSON 是否符合 feishu-card-design Skill 的 11 项铁律:
  1. schema 必须 = "2.0"
  2. 必须有 header.template (turquoise/blue/green/indigo/violet/red/yellow/wheat/grey)
  3. 必须有 body.elements (至少 1 个)
  4. body.elements 中所有 column 必须有 background_style (若 column_set 有, column 也要有, 双重保险)
  5. 不允许使用 lark_md 元素 (用 markdown 代替)
  6. button 必须用 behaviors 字段 (不允许 url 字段)
  7. 不允许使用 action 包装 button (Card 2.0 直接用 button)
  8. 邻近色环: header.template + 所有 background_style 不超过 3 种主色系
  9. 背景色块必须是 5 种语义色之一: blue-50/yellow-50/grey-50/green-50/red-50/turquoise-50/indigo-50/violet-50
 10. 标题建议格式 YYYYMMDD-类型-关键信息 (warning, 非强制)
 11. 必须有 footer 来源标识 (warning, 非强制，建议用 markdown + > 引用样式)
 12. note 元素废弃警告 (warning, Card 2.0 V2 已废弃，改用 markdown + > 引用)
 13. column_set/column padding 禁止 (warning, 飞书 API 报 230099，用 body.padding 统一控制)

用法:
    python card_validator.py <card.json>
    python card_validator.py <card.json> --strict   # 把 warning 也当 error
    python card_validator.py examples/*.json         # 批量验证
    python card_validator.py --stdin                 # 从 stdin 读 JSON

退出码:
    0 = 全部通过
    1 = 有 warning
    2 = 有 error
    3 = 文件读不到 / JSON 解析失败
"""
import sys
import json
import argparse
import re
from pathlib import Path

# ============================================================
# 11 项铁律
# ============================================================

ALLOWED_TEMPLATES = {
    "turquoise", "blue", "green", "indigo", "violet", "red",
    "yellow", "wheat", "grey"
}

ALLOWED_BG_COLORS = {
    "default",
    "blue-50", "yellow-50", "grey-50", "green-50", "red-50",
    "turquoise-50", "indigo-50", "violet-50", "wheat-50",
}

# 邻近色环映射: 起始色 -> 允许搭配的色系 (含自身)
ADJACENT_COLOR_GROUPS = {
    "turquoise": {"turquoise", "blue", "green"},
    "blue":      {"blue", "turquoise", "indigo", "violet"},
    "green":     {"green", "turquoise", "yellow"},
    "indigo":    {"indigo", "blue", "violet"},
    "violet":    {"violet", "indigo", "red", "blue"},
    "red":       {"red", "violet", "yellow"},
    "yellow":    {"yellow", "green", "red", "wheat"},
    "wheat":     {"wheat", "yellow"},
    "grey":      {"grey"},  # grey 是中性, 任何主色系都允许搭配
}

TITLE_REGEX = re.compile(r"^\d{8}-[^-]+-.+")


def validate_card(card: dict) -> tuple[list, list]:
    """验证一份卡片 JSON, 返回 (errors, warnings) 两个列表"""
    errors = []
    warnings = []

    # ============ Rule 1: schema = "2.0" ============
    schema = card.get("schema")
    if schema != "2.0":
        errors.append(f"R1: schema 必须 = '2.0', 当前 = {schema!r}")

    # ============ Rule 2: header.template 必填 ============
    header = card.get("header", {})
    if not header:
        errors.append("R2: 缺少 header 字段")
    else:
        template = header.get("template")
        if not template:
            errors.append("R2: header.template 缺失")
        elif template not in ALLOWED_TEMPLATES:
            errors.append(
                f"R2: header.template={template!r} 不在允许列表 {sorted(ALLOWED_TEMPLATES)}"
            )

    # ============ Rule 3: body.elements 至少 1 个 ============
    body = card.get("body", {})
    if not body:
        errors.append("R3: 缺少 body 字段")
    else:
        elements = body.get("elements", [])
        if not elements:
            errors.append("R3: body.elements 为空, 至少 1 个元素")

    # ============ Rule 4: column + column_set 双重保险 ============
    # 语义: 仅当 column_set 使用「非 default 背景色」时, column 也必须设 background_style.
    # default 是「无背景色」, 不触发双重保险.
    used_bg_colors = set()
    for i, el in enumerate(elements):
        if not isinstance(el, dict):
            continue
        tag = el.get("tag")
        if tag == "column_set":
            cs_bg = el.get("background_style")
            # 只有非 default 背景才需要双重保险
            if cs_bg and cs_bg != "default":
                columns = el.get("columns", [])
                for col in columns:
                    col_bg = col.get("background_style")
                    if not col_bg or col_bg == "default":
                        errors.append(
                            f"R4: elements[{i}].column_set 有 background_style={cs_bg!r} "
                            f"但 column 没设 background_style, 违反双重保险"
                        )
                    # 收集实际使用的色块
                    if col_bg and col_bg != "default":
                        used_bg_colors.add(col_bg)
                # column_set 自身的色也记入 (column 没设但 column_set 设了)
                used_bg_colors.add(cs_bg)
            else:
                # default 背景: 只收集 column 上设的非 default 色
                for col in el.get("columns", []):
                    col_bg = col.get("background_style") if isinstance(col, dict) else None
                    if col_bg and col_bg != "default":
                        used_bg_colors.add(col_bg)

    # ============ Rule 5: 禁用 lark_md, 用 markdown ============
    def walk_elements_for_lark_md(els, path="elements"):
        for i, el in enumerate(els):
            if not isinstance(el, dict):
                continue
            # 直接 text 字段
            text_obj = el.get("text", {})
            if isinstance(text_obj, dict) and text_obj.get("tag") == "lark_md":
                errors.append(
                    f"R5: {path}[{i}].text.tag='lark_md' 禁用, 改用 'markdown'"
                )
            # 嵌套 elements (column 内)
            for col in el.get("columns", []) or []:
                col_els = col.get("elements", []) or []
                walk_elements_for_lark_md(col_els, f"{path}[{i}].column.elements")
    walk_elements_for_lark_md(elements)

    # ============ Rule 6: button 必须用 behaviors ============
    for i, el in enumerate(elements):
        if not isinstance(el, dict):
            continue
        if el.get("tag") == "button":
            if "url" in el:
                errors.append(
                    f"R6: elements[{i}].button.url 字段已废弃, 改用 behaviors=[{{type:'open_url',default_url:...}}]"
                )
            if "behaviors" not in el:
                errors.append(
                    f"R6: elements[{i}].button 缺少 behaviors 字段"
                )

    # ============ Rule 7: 禁止 action 包装 button ============
    for i, el in enumerate(elements):
        if not isinstance(el, dict):
            continue
        if el.get("tag") == "action":
            errors.append(
                f"R7: elements[{i}].tag='action' 已废弃, Card 2.0 直接用 button"
            )

    # ============ Rule 8: 邻近色环 ≤ 3 种主色系 ============
    # 语义: yellow-50 / grey-50 是「语义中性色」, 与任何 header.template 搭配都不计入主色系.
    # 主色系 = turquoise/blue/green/indigo/violet/red/wheat (饱和色).
    if header and (template := header.get("template")):
        allowed_group = ADJACENT_COLOR_GROUPS.get(template, set())
        # 允许的 = 起始色 + grey (中性) + yellow (语义亮点) + 同组邻近色
        # yellow-50 作为「亮点」语义色块, 跨所有 header 模板允许搭配
        allowed_with_neutral = allowed_group | {"grey", "yellow"}
        # 收集所有色系 (从 background_style 提取主色, e.g. "blue-50" -> "blue")
        used_hues = set()
        for bg in used_bg_colors:
            if bg == "default":
                continue
            hue = bg.split("-")[0]
            used_hues.add(hue)
        # 加入 header.template 自己
        used_hues.add(template)
        # 中性色不计入 3 主色系限制
        NEUTRAL_HUES = {"grey", "yellow"}
        used_hues_no_neutral = {h for h in used_hues if h not in NEUTRAL_HUES}

        if len(used_hues_no_neutral) > 3:
            errors.append(
                f"R8: 邻近色环超过 3 种主色系, 当前 = {sorted(used_hues_no_neutral)} "
                f"(起始色 {template!r} 允许 = {sorted(allowed_with_neutral - NEUTRAL_HUES)} + grey/yellow)"
            )
        else:
            # 检查是否都在允许组内
            outside = used_hues_no_neutral - allowed_with_neutral
            if outside:
                errors.append(
                    f"R8: 色系 {sorted(outside)} 不在 {template!r} 的邻近色环内 "
                    f"(允许 = {sorted(allowed_with_neutral - NEUTRAL_HUES)} + grey/yellow)"
                )

    # ============ Rule 9: 背景色块必须合法 ============
    for bg in used_bg_colors:
        if bg not in ALLOWED_BG_COLORS:
            errors.append(
                f"R9: background_style={bg!r} 不在允许列表 {sorted(ALLOWED_BG_COLORS)}"
            )

    # ============ Rule 10: 标题格式建议 (warning) ============
    title = header.get("title", {}).get("content", "") if header else ""
    if title and not TITLE_REGEX.match(title):
        # 看是否包含 emoji 开头
        if not re.match(r"^[\U0001F300-\U0001FAFF]", title):
            warnings.append(
                f"R10: 标题 {title!r} 不符合 'YYYYMMDD-类型-关键信息' 格式"
            )

    # ============ Rule 11: footer 来源标识建议 (warning) ============
    # note 元素在 Card 2.0 V2 已废弃，接受 note 或 markdown 引用样式（> 开头）
    has_note = any(
        isinstance(el, dict) and el.get("tag") == "note"
        for el in elements
    )
    has_markdown_footer = any(
        isinstance(el, dict)
        and el.get("tag") == "markdown"
        and (el.get("content") or "").lstrip().startswith(">")
        for el in elements
    )
    if not has_note and not has_markdown_footer:
        warnings.append("R11: 缺少 footer 来源标识 (建议用 markdown > 引用样式，note 已废弃)")

    # ============ Rule 12: note 元素废弃警告 (warning) ============
    has_deprecated_note = any(
        isinstance(el, dict) and el.get("tag") == "note"
        for el in elements
    )
    if has_deprecated_note:
        warnings.append("R12: 检测到 note 元素 (Card 2.0 V2 已废弃，建议改用 markdown > 引用样式)")

    # ============ Rule 13: column_set/column padding 禁止 (warning) ============
    # 飞书 API 230099 错误: column_set 和 column 不支持 padding 属性
    # 只有 body 支持 padding, 内边距通过 body.padding 统一控制
    for el in elements:
        if isinstance(el, dict) and el.get("tag") == "column_set":
            if "padding" in el:
                warnings.append("R13: column_set 含 padding 属性 (飞书 API 报 230099，应删除，用 body.padding 统一控制)")
            for col in el.get("columns", []):
                if isinstance(col, dict) and "padding" in col:
                    warnings.append("R13: column 含 padding 属性 (飞书 API 报 230099，应删除，用 body.padding 统一控制)")

    return errors, warnings


# ============================================================
# CLI
# ============================================================

def validate_file(path: Path, strict: bool = False) -> tuple[int, list, list]:
    """验证单个文件, 返回 (exit_code, errors, warnings)"""
    try:
        text = path.read_text(encoding="utf-8")
    except Exception as e:
        return 3, [f"无法读取 {path}: {e}"], []
    try:
        card = json.loads(text)
    except json.JSONDecodeError as e:
        return 3, [f"JSON 解析失败 {path}: {e}"], []
    errors, warnings = validate_card(card)
    if errors:
        return 2, errors, warnings
    if warnings and strict:
        return 1, errors, warnings
    if warnings:
        return 1, errors, warnings
    return 0, errors, warnings


def format_result(path: str, exit_code: int, errors: list, warnings: list) -> str:
    """格式化单文件验证结果"""
    icon = {0: "✅", 1: "⚠️ ", 2: "❌", 3: "💀"}.get(exit_code, "?")
    lines = [f"{icon} {path}"]
    for e in errors:
        lines.append(f"   ERROR  {e}")
    for w in warnings:
        lines.append(f"   WARN   {w}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="feishu-card-design 卡片 JSON 验证工具"
    )
    parser.add_argument("files", nargs="*", help="待验证的 JSON 文件 (支持 glob)")
    parser.add_argument("--strict", action="store_true",
                        help="把 warning 也当 error (exit 1)")
    parser.add_argument("--stdin", action="store_true",
                        help="从 stdin 读 JSON")
    args = parser.parse_args()

    all_errors = []
    all_warnings = []
    final_code = 0

    if args.stdin:
        text = sys.stdin.read()
        try:
            card = json.loads(text)
        except json.JSONDecodeError as e:
            print(f"💀 JSON 解析失败: {e}")
            sys.exit(3)
        errors, warnings = validate_card(card)
        print(format_result("<stdin>", 2 if errors else (1 if warnings else 0),
                            errors, warnings))
        sys.exit(2 if errors else (1 if warnings and args.strict else 0))

    if not args.files:
        parser.print_help()
        sys.exit(0)

    # 展开 glob
    file_paths = []
    for pattern in args.files:
        p = Path(pattern)
        if p.exists() and p.is_file():
            file_paths.append(p)
        else:
            # glob 模式
            matched = sorted(Path(".").glob(pattern))
            if matched:
                file_paths.extend(matched)
            else:
                print(f"💀 文件不存在: {pattern}")
                final_code = max(final_code, 3)

    for fp in file_paths:
        code, errors, warnings = validate_file(fp, args.strict)
        print(format_result(str(fp), code, errors, warnings))
        all_errors.extend(errors)
        all_warnings.extend(warnings)
        final_code = max(final_code, code)

    print()
    print("=" * 60)
    print(f"总计: {len(file_paths)} 文件 / {len(all_errors)} 错误 / {len(all_warnings)} 警告")
    if args.strict:
        sys.exit(2 if all_errors else (1 if all_warnings else 0))
    sys.exit(2 if all_errors else 0)


if __name__ == "__main__":
    main()
