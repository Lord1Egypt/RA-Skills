#!/usr/bin/env python3
"""客户详细档案 CLI入口"""

import os
import sys
import json
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from _i18n import tr, deep_parse
from _buyer_ids import parse_buyer_id_list
from capabilities.get_customer_profile.service import get_customer_profile

COMMAND_NAME = "get_customer_profile"
COMMAND_DESC = "客户详细资料档案(基础信息、采购习惯、采购决策、跨店询盘)"

# 会触发"数值→程度"模糊化的字段名关键字
RISK_SCORE_KEY_PATTERNS = [
    "流失风险分", "风险分", "风险评分", "lostScore", "riskScore", "流失分值"
]


def _safe(val) -> str:
    if val is None or val == "":
        return "—"
    return str(val)





def _risk_level_from_score(score) -> str:
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
    if isinstance(data, dict):
        new_d = {}
        for k, v in data.items():
            # 只处理风险分字段
            if isinstance(k, str) and any(p in k for p in RISK_SCORE_KEY_PATTERNS):
                new_d[k] = _risk_level_from_score(v) if v is not None else v
            else:
                new_d[k] = _fuzzify_risk_fields(v)
        return new_d
    if isinstance(data, list):
        return [_fuzzify_risk_fields(x) for x in data]
    return data


# ============================================================
# 通用渲染：表格 / 区块（绝不 json.dumps，不包"内容："字段名）
# ============================================================
def _render_value_inline(v) -> str:
    """表格单元格内的 value：降级为分号分隔，避免二次嵌表"""
    if v is None or v == "":
        return "—"
    if isinstance(v, list):
        if not v:
            return "—"
        if all(isinstance(x, dict) for x in v):
            return "；".join(
                "，".join(f"{tr(k)}={_safe(vv)}" for k, vv in x.items())
                for x in v
            )
        return "；".join(_safe(x) for x in v)
    if isinstance(v, dict):
        return "，".join(f"{tr(k)}={_render_value_inline(vv)}" for k, vv in v.items())
    return _safe(v)


def _render_table(items: list) -> str:
    """[{k:v}, ...] → HTML 表格，表头用中文译名"""
    if not items:
        return ""
    if all(isinstance(x, dict) for x in items):
        keys = []
        for it in items:
            for k in it.keys():
                if k not in keys:
                    keys.append(k)
        if not keys:
            return ""
        th = "".join(
            f'<th style="padding:6px 10px;border-bottom:2px solid #cbd5e1;text-align:left;color:#0f172a;background:#f8fafc;">{tr(k)}</th>'
            for k in keys
        )
        rows = []
        for it in items:
            tds = "".join(
                f'<td style="padding:6px 10px;border-bottom:1px solid #e2e8f0;color:#0f172a;vertical-align:top;">{_render_value_inline(it.get(k))}</td>'
                for k in keys
            )
            rows.append(f"<tr>{tds}</tr>")
        return (
            f'<table style="width:100%;border-collapse:collapse;margin:6px 0;font-size:13px;background:#fff;border-radius:6px;overflow:hidden;">'
            f'<thead><tr>{th}</tr></thead><tbody>{"".join(rows)}</tbody></table>'
        )
    li = "".join(f"<li>{_safe(x)}</li>" for x in items)
    return f'<ol style="margin:6px 0 6px 20px;padding:0;">{li}</ol>'


def _render_value_block(v) -> str:
    """区块正文 value：保留表格/列表/多行键值，绝不 json.dumps"""
    if v is None or v == "":
        return "—"
    if isinstance(v, list):
        return _render_table(v)
    if isinstance(v, dict):
        parts = []
        for k, vv in v.items():
            rv = _render_value_block(vv)
            if rv.startswith(("<table", "<ol", "<ul")):
                parts.append(f'<div style="margin-top:6px;"><b>{tr(k)}</b></div>{rv}')
            else:
                parts.append(f"<b>{tr(k)}</b>：{rv}")
        return "<br>".join(parts)
    return _safe(v)


def _render_json_block(title: str, data, color: str, emoji: str, border_color: str, intro: str = "") -> str:
    """带颜色的区块。data 可以是 dict / list / 已解析对象 / 纯字符串。"""
    if data is None or data == "" or data == [] or data == {}:
        return ""

    # 宽松解析（兼容 JSON / Python repr 字符串）
    data = deep_parse(data)
    data = _fuzzify_risk_fields(data)

    # 纯字符串：直接作为正文输出，绝不包装成 {"内容": ...}
    if isinstance(data, str):
        content_html = _safe(data)
    else:
        content_html = _render_value_block(data)

    intro_html = (
        f'<div style="font-size:13px;color:#64748b;margin-bottom:8px;">{intro}</div>'
        if intro else ""
    )
    return (
        f'<div style="background-color: {color}; padding: 14px; margin: 12px 0; border-radius: 10px; border-left: 5px solid {border_color};">'
        f'<div style="font-size: 16px; font-weight: bold; margin-bottom: 10px;">{emoji} {title}</div>'
        f'{intro_html}'
        f'<div style="font-size: 14px; line-height: 1.7;">{content_html}</div>'
        f'</div>'
    )


def _build_buyer_information(item: dict) -> dict:
    """基础信息由多个独立字段组合而成（已用中文 key）"""
    return {
        "买家昵称": _safe(item.get("nickName")),
        "客户等级": _safe(item.get("lLevel")),
        "客户体质": _safe(item.get("buyerConstitution")),
        "主采类目": _safe(item.get("mainCate")),
        "近半年采购次数": _safe(item.get("payCnt180d")),
        "近半年同类目采购额": _safe(item.get("payAmt180d")),
    }


def _render_one_customer(item: dict) -> str:
    """单个客户的详细档案卡片（供批量拼接使用）"""
    nick = _safe(item.get("nickName"))
    parts = [
        f"## 📇 {nick} 的详细档案",
        "",
        f"> 将 **{nick}** 的身份信息、采购习惯、决策偏好、多店询盘整合在一张卡片 👇",
        "",
    ]
    info = _build_buyer_information(item)
    parts.append(_render_json_block(
        "客户基础信息", info, "#e0f2fe", "👤", "#3b82f6",
        intro="首先是客户的身份画像与近半年采购规模："
    ))
    habits = item.get("buyerPurchaseHabits")
    if habits:
        parts.append(_render_json_block(
            "客户采购习惯", habits, "#dcfce7", "🛒", "#16a34a",
            intro="接着看客户日常的采购节奏与偏好，帮你挑选最合适的沟通时机："
        ))
    decisions = item.get("purchaseDecisions")
    if decisions:
        parts.append(_render_json_block(
            "采购决策依据", decisions, "#fef3c7", "🟨", "#eab308",
            intro="然后看看客户下单前最在意的决策点，跟进时要优先回应这些："
        ))
    other = item.get("otherShopInqInfor")
    if other:
        parts.append(_render_json_block(
            "跨店询盘信息", other, "#f3e8ff", "🏪", "#a855f7",
            intro="最后看看客户在其他店铺的询盘动作，掌握外部对比信号："
        ))
    return "\n".join(parts)


def _render_markdown(data: dict) -> str:
    result = data.get("data") or []
    if not result:
        return "# 📇 客户详细档案\n\n> 未找到匹配客户，请确认客户信息是否正确。"

    # 单客户：保持原样式
    if len(result) == 1:
        item = result[0]
        nick = _safe(item.get("nickName"))

        lines = [
            f"# 📇 {nick} 的详细档案",
            "",
            f"> 这里把 **{nick}** 的身份信息、采购习惯、决策偏好、多店询盘整合在一张卡片，帮你在跟进前 30 秒快速抓住重点 👇",
            "",
        ]

        info = _build_buyer_information(item)
        lines.append(_render_json_block(
            "客户基础信息", info, "#e0f2fe", "👤", "#3b82f6",
            intro="首先是客户的身份画像与近半年采购规模："
        ))

        habits = item.get("buyerPurchaseHabits")
        if habits:
            lines.append(_render_json_block(
                "客户采购习惯", habits, "#dcfce7", "🛒", "#16a34a",
                intro="接着看客户日常的采购节奏与偏好，帮你挑选最合适的沟通时机："
            ))

        decisions = item.get("purchaseDecisions")
        if decisions:
            lines.append(_render_json_block(
                "采购决策依据", decisions, "#fef3c7", "🟨", "#eab308",
                intro="然后看看客户下单前最在意的决策点，跟进时要优先回应这些："
            ))

        other = item.get("otherShopInqInfor")
        if other:
            lines.append(_render_json_block(
                "跨店询盘信息", other, "#f3e8ff", "🏪", "#a855f7",
                intro="最后看看客户在其他店铺的询盘动作，掌握外部对比信号："
            ))

        return "\n".join(lines)

    # 多客户批量：总起 + 各客户独立卡片串联
    head = (
        f"# 📇 客户详细档案（共 {len(result)} 位客户）\n\n"
        f"> 已为以下客户依次汇总身份信息、采购习惯、决策偏好、多店询盘数据，可逐位查看 👇"
    )
    sections = [_render_one_customer(it) for it in result]
    return head + "\n\n---\n\n" + "\n\n---\n\n".join(sections)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False, "❌ AK 未配置，无法查询客户档案。\n\n运行: `cli.py configure YOUR_AK`", {"data": {}})
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
        result = get_customer_profile(nick_name=args.nick_name, buyer_id_list=buyer_id_list)
        print_output(True, _render_markdown(result), {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
