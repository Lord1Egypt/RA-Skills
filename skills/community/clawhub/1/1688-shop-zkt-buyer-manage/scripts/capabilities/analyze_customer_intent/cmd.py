#!/usr/bin/env python3
"""客户采购意图分析 CLI入口"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from _i18n import tr as _tr, deep_parse
from _buyer_ids import parse_buyer_id_list
from capabilities.analyze_customer_intent.service import analyze_customer_intent

COMMAND_NAME = "analyze_customer_intent"
COMMAND_DESC = "客户采购意图分析(采购需求、跨店对比、决策依据)"

# 会触发"数值→程度"模糊化的字段名关键字
RISK_SCORE_KEY_PATTERNS = [
    "流失风险分", "风险分", "风险评分", "lostScore", "riskScore", "流失分值"
]


def _safe(val) -> str:
    if val is None or val == "":
        return "—"
    return str(val)


def _risk_level_from_score(score) -> str:
    """把 0~100 或 0~1 的风险分数转为程度描述"""
    try:
        s = float(score)
    except Exception:
        return str(score)
    if s <= 1:
        s = s * 100
    if s >= 80:
        return "极高"
    if s >= 60:
        return "较高"
    if s >= 40:
        return "中等"
    if s >= 20:
        return "较低"
    return "很低"


def _fuzzify_risk_fields(data):
    """递归遍历 data，把"流失风险分/风险分"等字段的数值替换为程度描述"""
    if isinstance(data, dict):
        new_d = {}
        for k, v in data.items():
            if isinstance(k, str) and any(p in k for p in RISK_SCORE_KEY_PATTERNS):
                new_d[k] = _risk_level_from_score(v) if v is not None else v
            else:
                new_d[k] = _fuzzify_risk_fields(v)
        return new_d
    if isinstance(data, list):
        return [_fuzzify_risk_fields(x) for x in data]
    return data


def _render_table(items: list) -> str:
    """把 [{k:v}, ...] 渲染为 HTML 表格；非 dict 元素渲染为有序列表"""
    if not items:
        return ""

    # 如果元素都是 dict，按 key 并集出表格
    if all(isinstance(x, dict) for x in items):
        keys = []
        for it in items:
            for k in it.keys():
                if k not in keys:
                    keys.append(k)
        if not keys:
            return ""
        th = "".join(
            f'<th style="padding:6px 10px;background:#ffffff;border-bottom:2px solid #e5e7eb;text-align:left;font-weight:600;color:#334155;">{_tr(k)}</th>'
            for k in keys
        )
        rows = []
        for it in items:
            tds = "".join(
                f'<td style="padding:6px 10px;border-bottom:1px solid #f1f5f9;vertical-align:top;color:#1f2937;">{_render_value_inline(it.get(k))}</td>'
                for k in keys
            )
            rows.append(f'<tr>{tds}</tr>')
        return (
            f'<table style="border-collapse:collapse;width:100%;margin:6px 0 2px 0;background:#ffffff;border-radius:6px;overflow:hidden;font-size:13.5px;">'
            f'<thead><tr>{th}</tr></thead>'
            f'<tbody>{"".join(rows)}</tbody>'
            f'</table>'
        )

    # 混合/基础类型：有序列表
    li = "".join(f"<li style='margin:2px 0;'>{_safe(x)}</li>" for x in items)
    return f'<ol style="margin:6px 0 2px 20px;padding:0;">{li}</ol>'


def _render_value_inline(v) -> str:
    """表格单元格里的 value：尽量单行，避免二次嵌表格"""
    if v is None or v == "":
        return "—"
    if isinstance(v, list):
        # 单元格里不再嵌表格，降级为分号分隔
        parts = []
        for x in v:
            if isinstance(x, dict):
                parts.append("；".join(f"{_tr(k)}：{_safe(vv)}" for k, vv in x.items()))
            else:
                parts.append(_safe(x))
        return "<br>".join(parts)
    if isinstance(v, dict):
        return "；".join(f"{_tr(k)}：{_safe(vv)}" for k, vv in v.items())
    return _safe(v)


def _render_value_block(v) -> str:
    """区块正文里的 value：保留表格 / 列表 / 多行"""
    if v is None or v == "":
        return "—"
    if isinstance(v, list):
        return _render_table(v)
    if isinstance(v, dict):
        parts = []
        for k, vv in v.items():
            rv = _render_value_block(vv)
            # 如果子 value 是表格/列表，作为独立块
            if rv.startswith(("<table", "<ol", "<ul")):
                parts.append(
                    f'<div style="margin-top:6px;"><b>{_tr(k)}</b></div>{rv}'
                )
            else:
                parts.append(f"<b>{_tr(k)}</b>：{rv}")
        return "<br>".join(parts)
    return _safe(v)


def _render_json_block(title: str, data, color: str = "#e0f2fe", emoji: str = "🟦",
                      border_color: str = "#3b82f6", intro: str = "") -> str:
    """将 JSON 数据渲染为带颜色区块的 HTML（带可读串场语，**禁止**输出裸 JSON）"""
    if data is None or data == "":
        return ""

    # 宽松解析（兼容 JSON / Python repr 字符串）
    data = deep_parse(data)

    # 纯字符串：直接输出正文，不要包装"内容："字段名
    if isinstance(data, str):
        content_html = _safe(data)
        intro_html = (
            f'<div style="font-size:13px;color:#64748b;margin-bottom:8px;">{intro}</div>'
            if intro else ""
        )
        return (
            f'<div style="background-color: {color}; padding: 14px; margin: 12px 0; border-radius: 10px; border-left: 5px solid {border_color};">'
            f'<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">{emoji} {title}</div>'
            f'{intro_html}'
            f'<div style="font-size: 14px; line-height: 1.7;color:#1f2937;">{content_html}</div>'
            f'</div>'
        )

    # 流失风险分模糊化
    data = _fuzzify_risk_fields(data)

    # dict / list 统一由 _render_value_block 处理
    content_html = _render_value_block(data)

    intro_html = (
        f'<div style="font-size:13px;color:#64748b;margin-bottom:8px;">{intro}</div>'
        if intro else ""
    )

    return (
        f'<div style="background-color: {color}; padding: 14px; margin: 12px 0; border-radius: 10px; border-left: 5px solid {border_color};">'
        f'<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">{emoji} {title}</div>'
        f'{intro_html}'
        f'<div style="font-size: 14px; line-height: 1.7;color:#1f2937;">{content_html}</div>'
        f'</div>'
    )


def _render_one_customer(item: dict) -> str:
    """单个客户的意图分析卡片（供批量拼接使用）"""
    nick = _safe(item.get("nickName"))
    parts = [
        f"## 🔍 {nick} 的采购意图分析",
        "",
        f"> 先看「{nick} 最近在聊什么」，再看「决策关注点」，结合跟进阶段给出可参考的判断 👇",
        "",
    ]
    recent_chat = item.get("recentChatNeedsAna")
    if recent_chat:
        parts.append(_render_json_block(
            "近期沟通需求分析", recent_chat, "#e0f2fe", "🟦", "#3b82f6",
            intro="这部分来自最近聊天记录的结构化提炼，用来看客户目前关心的核心诉求："
        ))
    decisions = item.get("purchaseDecisions")
    if decisions:
        parts.append(_render_json_block(
            "采购决策依据", decisions, "#fef3c7", "🟨", "#eab308",
            intro="接下来看看客户下单前最在意的几个决策点，这些是跟进时优先回应的方向："
        ))
    awaken = item.get("awakenReason")
    lost = item.get("lostAnalysis")
    if awaken:
        parts.append(_render_json_block(
            "商机唤醒理由", awaken, "#dcfce7", "🟩", "#16a34a",
            intro="另外，这位客户在以下几个维度具备唤醒价值，可以作为主动触达的切入点："
        ))
    elif lost:
        parts.append(_render_json_block(
            "流失风险分析", lost, "#fee2e2", "🟥", "#ef4444",
            intro="系统识别到这位客户存在一些流失信号，我们一起看看背后的原因（风险程度已用等级描述，便于快速判断）："
        ))
    if len(parts) == 4:
        parts.append("> 该客户暂无采购意图分析数据。")
    return "\n".join(parts)


def _render_markdown(data: dict) -> str:
    # API 返回的数据可能在 data.data 或 data.result 中
    result = data.get("result") or data.get("data") or []
    if not result:
        return "# 🔍 客户采购意图分析\n\n> 未找到匹配客户，请确认客户信息是否正确。"

    # 单客户：保持原样式
    if len(result) == 1:
        item = result[0]
        nick = _safe(item.get("nickName"))

        lines = [
            f"# 🔍 {nick} 的采购意图分析",
            "",
            f"> 先带你从「最近在聊什么」入手，再看「决策关注点」，最后结合客户当前的跟进阶段，给出可参考的判断 👇",
            "",
        ]

        recent_chat = item.get("recentChatNeedsAna")
        if recent_chat:
            lines.append(_render_json_block(
                "近期沟通需求分析", recent_chat, "#e0f2fe", "🟦", "#3b82f6",
                intro="这部分来自最近聊天记录的结构化提炼，用来看客户目前关心的核心诉求："
            ))

        decisions = item.get("purchaseDecisions")
        if decisions:
            lines.append(_render_json_block(
                "采购决策依据", decisions, "#fef3c7", "🟨", "#eab308",
                intro="接下来看看客户下单前最在意的几个决策点，这些是跟进时优先回应的方向："
            ))

        awaken = item.get("awakenReason")
        lost = item.get("lostAnalysis")
        if awaken:
            lines.append(_render_json_block(
                "商机唤醒理由", awaken, "#dcfce7", "🟩", "#16a34a",
                intro="另外，这位客户在以下几个维度具备唤醒价值，可以作为主动触达的切入点："
            ))
        elif lost:
            lines.append(_render_json_block(
                "流失风险分析", lost, "#fee2e2", "🟥", "#ef4444",
                intro="系统识别到这位客户存在一些流失信号，我们一起看看背后的原因（风险程度已用等级描述，便于快速判断）："
            ))

        if len(lines) == 4:
            lines.append("> 该客户暂无采购意图分析数据。")
        else:
            lines.append("")
            lines.append("> 🎯 以上分析都来自最近一段时间的真实互动数据，建议结合客户当前跟进阶段选择最合适的动作。")

        return "\n".join(lines)

    # 多客户批量：总起 + 各客户独立卡片串联
    head = (
        f"# 🔍 采购意图分析（共 {len(result)} 位客户）\n\n"
        f"> 已为以下客户依次生成采购意图分析，可逐位查看 👇"
    )
    sections = [_render_one_customer(it) for it in result]
    return head + "\n\n---\n\n" + "\n\n---\n\n".join(sections)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未配置，无法分析客户意图。\n\n运行: `cli.py configure YOUR_AK`", {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--nick-name", help="买家昵称（单查兜底）")
    parser.add_argument("--buyer-id-list",
                        help='客户 ID 数组，推荐多客户批量一次查询，如 \'["id1","id2"]\'')
    args = parser.parse_args()

    buyer_id_list = None
    if args.buyer_id_list:
        buyer_id_list, err = parse_buyer_id_list(args.buyer_id_list)
        if err:
            print_output(False, err, {"data": {}})
            return

    try:
        result = analyze_customer_intent(nick_name=args.nick_name, buyer_id_list=buyer_id_list)
        print_output(True, _render_markdown(result), {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
