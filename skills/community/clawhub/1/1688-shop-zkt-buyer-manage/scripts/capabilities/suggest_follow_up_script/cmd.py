#!/usr/bin/env python3
"""客户跟进话术建议 CLI入口"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from _i18n import tr, deep_parse, parse_loose
from _buyer_ids import parse_buyer_id_list
from capabilities.suggest_follow_up_script.service import suggest_follow_up_script

COMMAND_NAME = "suggest_follow_up_script"
COMMAND_DESC = "客户跟进话术建议（二次跟进、挽留、唤醒）"

# 常见话术字段对应的 emoji
SCRIPT_FIELD_EMOJI = {
    "开场白": "👋",
    "核心话术": "💡",
    "促单话术": "🎯",
    "场景": "📌",
    "挽留话术": "🛡️",
    "唤醒话术": "🔥",
    "跟进话术": "💬",
    "对话": "💬",
    "建议": "💡",
}


def _safe(val) -> str:
    if val is None or val == "":
        return "—"
    return str(val)


def _flatten_scripts(scripts):
    """把任意嵌套结构（list of list / 字符串 dict 字面量）扁平化为 [dict|str, ...]

    1688 接口可能返回：
      - [{开场白:..., 核心话术:...}, ...]                    （正常）
      - "[{'开场白':...},{'开场白':...}]"                     （Python repr 整体一坨字符串）
      - ["{'开场白':...}", "{'开场白':...}"]                  （list 内每元素都是 repr 字符串）
      - [[{...},{...}]]                                       （多嵌一层 list）
      - {"speech_script": [{...}, {...}]}                     （包含 speech_script 字段的 dict）
    全部统一为顶层 list of dict。
    """
    if scripts is None:
        return []
    
    # 字符串：先尝试解析
    if isinstance(scripts, str):
        parsed = parse_loose(scripts)
        if parsed is scripts:
            return [scripts]  # 当作纯文本话术处理
        scripts = parsed
    
    # dict：检查是否有 speech_script 字段
    if isinstance(scripts, dict):
        # 如果包含 speech_script 字段，提取其值并递归处理
        if "speech_script" in scripts:
            return _flatten_scripts(scripts["speech_script"])
        # 否则当作单套话术处理
        return [scripts]
    
    # list：递归展开
    if isinstance(scripts, list):
        out = []
        for s in scripts:
            if isinstance(s, str):
                p = parse_loose(s)
                if isinstance(p, list):
                    out.extend(_flatten_scripts(p))
                elif isinstance(p, dict):
                    out.append(p)
                else:
                    out.append(s)
            elif isinstance(s, list):
                out.extend(_flatten_scripts(s))
            else:
                out.append(s)
        return out
    return [scripts]


def _render_script_card(idx: int, script, border_color: str) -> str:
    """把单套话术渲染为可读卡片（dict → 字段表，list → 序号列表，str → 纯文本）"""
    if script is None or script == "":
        return ""

    # 深度解析（处理嵌套字符串）
    script = deep_parse(script)

    rows = []
    if isinstance(script, dict):
        for k, v in script.items():
            if v is None or v == "":
                continue
            label = tr(k) if not isinstance(k, str) or k not in SCRIPT_FIELD_EMOJI else k
            emoji = SCRIPT_FIELD_EMOJI.get(label, SCRIPT_FIELD_EMOJI.get(str(k), "✨"))
            v_text = _render_inline(v)
            rows.append(
                f'<div style="margin:8px 0;display:flex;gap:8px;align-items:flex-start;">'
                f'<span style="display:inline-block;min-width:80px;font-weight:bold;color:#475569;flex-shrink:0;">{emoji} {label}</span>'
                f'<span style="color:#0f172a;line-height:1.7;flex:1;">{v_text}</span>'
                f'</div>'
            )
    elif isinstance(script, list):
        # 子元素如果是 dict，直接展开成字段表（不要 "1. {...}"）
        dict_items = [x for x in script if isinstance(x, dict)]
        if dict_items and len(dict_items) == len(script):
            # 当作多套话术展开（合并为一个表格）
            return _render_scripts_table(script, border_color, idx)
        for i, line in enumerate(script, 1):
            if isinstance(line, (dict, list)):
                rows.append(f'<div style="margin:6px 0;">{i}. {_render_inline(line)}</div>')
            else:
                rows.append(f'<div style="margin:6px 0;">{i}. {_safe(line)}</div>')
    else:
        rows.append(f'<div style="margin:6px 0;">{_safe(script)}</div>')

    if not rows:
        return ""

    content_html = "".join(rows)
    return (
        f'<div style="background:#ffffff; padding:14px 16px; margin:10px 0; border-radius:10px; '
        f'border-left:5px solid {border_color}; box-shadow:0 1px 3px rgba(0,0,0,0.06);">'
        f'<div style="font-size:14px;font-weight:bold;color:{border_color};margin-bottom:6px;">方案 {idx}</div>'
        f'{content_html}'
        f'</div>'
    )


def _render_inline(v) -> str:
    """value 内联渲染：dict → 「键：值，键：值」；list → 「a；b；c」；str → 原样"""
    if v is None or v == "":
        return "—"
    if isinstance(v, dict):
        return "，".join(f"<b>{tr(k)}</b>：{_render_inline(vv)}" for k, vv in v.items())
    if isinstance(v, list):
        if all(isinstance(x, dict) for x in v):
            return "；".join(_render_inline(x) for x in v)
        return "；".join(_safe(x) for x in v)
    return _safe(v)


def _render_scripts_table(scripts: list, border_color: str, idx: int) -> str:
    """多套同结构的话术 → HTML 表格"""
    # 收集所有 key
    keys = []
    for s in scripts:
        if isinstance(s, dict):
            for k in s.keys():
                if k not in keys:
                    keys.append(k)
    if not keys:
        return ""
    th = "".join(
        f'<th style="padding:6px 10px;border-bottom:2px solid #cbd5e1;text-align:left;color:#0f172a;background:#f8fafc;">'
        f'{SCRIPT_FIELD_EMOJI.get(tr(k), SCRIPT_FIELD_EMOJI.get(str(k), "✨"))} {tr(k)}'
        f'</th>'
        for k in keys
    )
    rows = []
    for i, s in enumerate(scripts, 1):
        tds = "".join(
            f'<td style="padding:8px 10px;border-bottom:1px solid #e2e8f0;color:#0f172a;vertical-align:top;line-height:1.7;">{_render_inline(s.get(k)) if isinstance(s, dict) else _safe(s)}</td>'
            for k in keys
        )
        rows.append(f"<tr>{tds}</tr>")
    table = (
        f'<table style="width:100%;border-collapse:collapse;margin:6px 0;font-size:13px;background:#fff;border-radius:6px;overflow:hidden;">'
        f'<thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table>'
    )
    return (
        f'<div style="background:#ffffff; padding:14px 16px; margin:10px 0; border-radius:10px; '
        f'border-left:5px solid {border_color}; box-shadow:0 1px 3px rgba(0,0,0,0.06);">'
        f'<div style="font-size:14px;font-weight:bold;color:{border_color};margin-bottom:8px;">📋 话术总览（共 {len(scripts)} 套）</div>'
        f'{table}'
        f'</div>'
    )


def _render_script_group(title: str, scripts, bg_color: str, border_color: str, emoji: str) -> str:
    """把一组话术（最多取 3 套）渲染为同色系卡片组"""
    scripts = _flatten_scripts(scripts)
    if not scripts:
        return ""
    scripts = scripts[:3]

    # 全部是 dict 且字段一致 → 用表格汇总
    if len(scripts) >= 2 and all(isinstance(s, dict) for s in scripts):
        keysets = [tuple(sorted(s.keys())) for s in scripts]
        if len(set(keysets)) == 1:
            table_html = _render_scripts_table(scripts, border_color, 0)
            return (
                f'<div style="background-color: {bg_color}; padding: 14px 16px; margin: 12px 0; border-radius: 10px; border-left: 5px solid {border_color};">'
                f'<div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color:#0f172a;">{emoji} {title}（共 {len(scripts)} 套可选）</div>'
                f'<div style="font-size: 13px; color:#64748b; margin-bottom: 8px;">下列话术按适配度排序，可挑选最贴合当前客户沟通节奏的一套直接使用：</div>'
                f'{table_html}'
                f'</div>'
            )

    cards = []
    for i, s in enumerate(scripts, 1):
        card = _render_script_card(i, s, border_color)
        if card:
            cards.append(card)
    if not cards:
        return ""
    cards_html = "".join(cards)
    return (
        f'<div style="background-color: {bg_color}; padding: 14px 16px; margin: 12px 0; border-radius: 10px; border-left: 5px solid {border_color};">'
        f'<div style="font-size: 16px; font-weight: bold; margin-bottom: 8px; color:#0f172a;">{emoji} {title}（共 {len(cards)} 套可选）</div>'
        f'<div style="font-size: 13px; color:#64748b; margin-bottom: 8px;">下列话术按适配度排序，可挑选最贴合当前客户沟通节奏的一套直接使用：</div>'
        f'{cards_html}'
        f'</div>'
    )


def _pick_scripts_by_priority(item: dict, buyer_type: str = None):
    """按优先级选一组话术：wakenAdvice > retentionAdvice > followUpScript
    
    如果指定了 buyer_type：
    - lostRiskType: 只展示 retentionAdvice（挽留话术）
    - wakeUpType: 只展示 wakenAdvice（唤醒话术）
    - 未指定: 按原有优先级逻辑
    """
    # 如果指定了 buyer_type，按类型展示对应话术
    if buyer_type == "lostRiskType":
        retention = item.get("retentionAdvice")
        if retention:
            return "🛡️ 挽留话术建议", retention, "#fee2e2", "#dc2626"
        # 如果没有挽留话术，降级到 followUpScript
        follow = item.get("followUpScript")
        if follow:
            return "💬 跟进话术建议", follow, "#f3e8ff", "#a855f7"
        return None, None, None, None
    
    elif buyer_type == "wakeUpType":
        waken = item.get("wakenAdvice")
        if waken:
            return "🔥 唤醒话术建议", waken, "#dcfce7", "#16a34a"
        # 如果没有唤醒话术，降级到 followUpScript
        follow = item.get("followUpScript")
        if follow:
            return "💬 跟进话术建议", follow, "#f3e8ff", "#a855f7"
        return None, None, None, None
    
    # 未指定 buyer_type，按原有优先级逻辑
    waken = item.get("wakenAdvice")
    if waken:
        return "🔥 唤醒话术建议", waken, "#dcfce7", "#16a34a"
    retention = item.get("retentionAdvice")
    if retention:
        return "🛡️ 挽留话术建议", retention, "#fee2e2", "#dc2626"
    follow = item.get("followUpScript")
    if follow:
        return "💬 跟进话术建议", follow, "#f3e8ff", "#a855f7"
    return None, None, None, None


def _render_one_customer(item: dict, buyer_type: str = None) -> str:
    """单个客户的话术建议卡片（不含顶部总起，供批量拼接使用）"""
    nick = _safe(item.get("nickName"))
    title, scripts, bg_color, border_color = _pick_scripts_by_priority(item, buyer_type)

    parts = [
        f"## 💬 {nick} 的跟进话术建议",
        "",
        f"> 已结合 **{nick}** 最近的沟通节奏挑选出可直接使用的一组话术，按适配度从高到低排列 👇",
        "",
    ]

    if title and scripts:
        emoji = title.split(" ", 1)[0]
        clean_title = title.split(" ", 1)[1] if " " in title else title
        parts.append(_render_script_group(clean_title, scripts, bg_color, border_color, emoji))
    else:
        parts.append("> 该客户暂无话术建议数据。")

    return "\n".join(parts)


def _render_markdown(data: dict, buyer_type: str = None) -> str:
    result = data.get("data") or []
    if not result:
        return "# 💬 跟进话术建议\n\n> 未找到匹配客户，请确认客户信息是否正确。"

    # 单客户：保持原样式
    if len(result) == 1:
        item = result[0]
        nick = _safe(item.get("nickName"))
        title, scripts, bg_color, border_color = _pick_scripts_by_priority(item, buyer_type)
        lines = [
            f"# 💬 {nick} 的跟进话术建议",
            "",
            f"> 我已经结合 **{nick}** 的最近沟通节奏挑选好可直接使用的一组话术，按适配度从高到低排列，你可以挑一套最顺手的发出去 👇",
            "",
        ]
        if title and scripts:
            emoji = title.split(" ", 1)[0]
            clean_title = title.split(" ", 1)[1] if " " in title else title
            lines.append(_render_script_group(clean_title, scripts, bg_color, border_color, emoji))
        else:
            lines.append("> 该客户暂无话术建议数据。")
        return "\n".join(lines)

    # 多客户批量：总起 + 各客户独立卡片串联
    blocks = [
        f"# 💬 跟进话术建议（共 {len(result)} 位客户）",
        "",
        "> 已为以下客户依次生成可直接使用的跟进话术，你可以逐位拷贝使用 👇",
    ]
    sections = [_render_one_customer(it, buyer_type) for it in result]
    return blocks[0] + "\n" + blocks[1] + "\n" + blocks[2] + "\n\n---\n\n" + "\n\n---\n\n".join(sections)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未配置，无法获取话术建议。\n\n运行: `cli.py configure YOUR_AK`", {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--nick-name", help="买家昵称（单查兜底）")
    parser.add_argument("--buyer-id-list",
                        help="客户 ID 数组，推荐多客户批量一次查询，如 '[\"id1\",\"id2\"]'")
    parser.add_argument("--buyer-type", choices=["lostRiskType", "wakeUpType"],
                        help="客户类型：lostRiskType-流失风险（挽留话术）, wakeUpType-商机唤醒（唤醒话术）")
    args = parser.parse_args()
    
    buyer_id_list = None
    if args.buyer_id_list:
        buyer_id_list, err = parse_buyer_id_list(args.buyer_id_list)
        if err:
            print_output(False, err, {"data": {}})
            return
    
    try:
        result = suggest_follow_up_script(nick_name=args.nick_name, buyer_id_list=buyer_id_list, buyer_type=args.buyer_type)
        print_output(True, _render_markdown(result, args.buyer_type), {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
