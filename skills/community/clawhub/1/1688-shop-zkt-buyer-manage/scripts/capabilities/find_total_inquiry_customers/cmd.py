#!/usr/bin/env python3
"""总询盘客户查询 CLI入口"""

import json
import os
import sys
import argparse
from datetime import datetime

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.find_total_inquiry_customers.service import find_total_inquiry_customers

COMMAND_NAME = "find_total_inquiry_customers"
COMMAND_DESC = "查询总询盘客户列表（支持多维度筛选）"


def _fmt_ts(ts) -> str:
    if not ts:
        return "—"
    try:
        ms = int(ts)
        if ms > 10 ** 12:
            ms = ms // 1000
        return datetime.fromtimestamp(ms).strftime("%Y-%m-%d")
    except Exception:
        return str(ts)


def _safe(val) -> str:
    if val is None or val == "":
        return "—"
    return str(val)





def _risk_level(score) -> str:
    """把流失风险分(0~100 或 0~1)转为程度描述，不直接透出数值"""
    if score is None or score == "":
        return "—"
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


def _parse_json_list(val: str):
    """解析 JSON 数组字符串，失败返回 None"""
    if not val:
        return None
    try:
        result = json.loads(val)
        if isinstance(result, list):
            return result
    except Exception:
        pass
    return None


# ── 跟进状态语义归一化 ────────────────────────────────────────────────────────

FOLLOW_UP_STATE_SYNONYMS = {
    "初步沟通": [
        "初步沟通", "刚开始聊", "刚联系", "初次接触", "首次沟通",
        "刚开始", "刚加上", "新客", "新客户", "初步了解", "刚沟通", "初聊"
    ],
    "意向明确": [
        "意向明确", "有意向", "确定要买", "想下单", "准备成交",
        "高意向", "准客户", "意向强", "明确购买", "即将成交", "要买了"
    ],
    "历史成交": [
        "历史成交", "买过", "老客户", "已成交", "复购",
        "曾经买过", "下过单", "成交过", "老客", "既往成交", "回头客"
    ],
}
VALID_FOLLOW_UP_STATES = list(FOLLOW_UP_STATE_SYNONYMS.keys())


def _normalize_follow_up_state(raw: str) -> str:
    """将用户输入的跟进状态词归一化为标准值，取语义最相近的 top1"""
    if not raw:
        return None
    # 精确匹配标准值
    if raw in VALID_FOLLOW_UP_STATES:
        return raw
    # 精确匹配同义词
    for canonical, synonyms in FOLLOW_UP_STATE_SYNONYMS.items():
        if raw in synonyms:
            return canonical
    # difflib 模糊匹配所有同义词
    import difflib
    best_canonical = None
    best_ratio = 0.0
    for canonical, synonyms in FOLLOW_UP_STATE_SYNONYMS.items():
        for syn in synonyms:
            ratio = difflib.SequenceMatcher(None, raw, syn).ratio()
            if ratio > best_ratio:
                best_ratio = ratio
                best_canonical = canonical
    if best_ratio >= 0.3:
        return best_canonical
    return None


def _render_markdown(data: dict, page_size: int = 10) -> str:
    result = data.get("data") or []
    total = data.get("total") or len(result)
    if not result:

        return "# 📋 查询结果\n\n> 暂无匹配的询盘客户数据"


    lines = [
        "# 📋 查询结果",
        "",
        f"共到 **{total}** 位客户，其中top{page_size}信息如下：",
        "",
        "| 买家昵称 | 买家身份 | 跟进阶段 | 主采类目 | 近半年类目额 | 采购次数 |",
        "|----------|----------|----------|----------|--------------|----------|",
    ]

    for item in result:
        nick = _safe(item.get("nickName"))
        identity = _safe(item.get("identity"))
        follow_up_state = _safe(item.get("followUpState"))
        cate = _safe(item.get("mainCate"))
        pay_amt = _safe(item.get("payAmt180d"))
        pay_cnt = _safe(item.get("payCnt180d"))

        lines.append(
            f"| {nick} | {identity} | {follow_up_state} | {cate} | {pay_amt} | {pay_cnt} |"
        )

    lines.append("")
    lines.append("---")
    lines.append("")
    return "\n".join(lines)


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(
            False,
            "❌ AK 未配置，无法查询询盘客户。\n\n运行: `cli.py configure YOUR_AK`",
            {"data": {}}
        )
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--buyer-type", choices=["lostRiskType", "wakeUpType"],
                        help="客户类型筛选：lostRiskType-风险流失, wakeUpType-商机唤醒")
    parser.add_argument("--follow-up-state-list",
                        help='跟进状态 JSON 数组，如 \'["初步沟通","已报价"]\'（最多5个）')
    parser.add_argument("--nick-name",
                        help="买家昵称，支持模糊查询")
    parser.add_argument("--tag-list",
                        help='旺旺标签 JSON 数组，如 \'["标签A","标签B"]\'（最多5个）')
    parser.add_argument("--start-time",
                        help='询盘查询开始时间，格式：yyyyMMdd HH:mm:ss，如 "2026-03-01 00:00:00"')
    parser.add_argument("--end-time",
                        help='询盘查询截止时间，格式：yyyyMMdd HH:mm:ss，如 "2026-05-10 23:59:59"')
    parser.add_argument("--min-pay-amt-180d", type=int,
                        help="近半年店铺同类目采购金额最小值")
    parser.add_argument("--max-pay-amt-180d", type=int,
                        help="近半年店铺同类目采购金额最大值")
    parser.add_argument("--last-sales-name",
                        help="最近跟进业务员名称")
    parser.add_argument("--identity-list",
                        help='买家身份 JSON 数组，如 \'["超级买家","L3"]\'（最多5个）')
    parser.add_argument("--is-buyer-active", type=int, choices=[0, 1],
                        help="近30天活跃状态：1-活跃")
    parser.add_argument("--page-size", type=int, default=10,
                        help="查询客户数量，范围10~50，默认10")
    args = parser.parse_args()

    # 校验数组参数长度 + 跟进状态语义归一化
    raw_follow_up_state_list = _parse_json_list(args.follow_up_state_list)
    follow_up_state_list = None
    if raw_follow_up_state_list is not None:
        follow_up_state_list = []
        for raw in raw_follow_up_state_list:
            normalized = _normalize_follow_up_state(raw)
            if normalized:
                follow_up_state_list.append(normalized)
        if not follow_up_state_list:
            print_output(False, f"❌ 跟进状态仅支持：{'、'.join(VALID_FOLLOW_UP_STATES)}", {"data": {}})
            return

    tag_list = _parse_json_list(args.tag_list)
    identity_list = _parse_json_list(args.identity_list)

    if follow_up_state_list is not None and len(follow_up_state_list) > 5:
        print_output(False, "❌ followUpStateList 最多不能超过 5 个", {"data": {}})
        return
    if tag_list is not None and len(tag_list) > 5:
        print_output(False, "❌ tagList 最多不能超过 5 个", {"data": {}})
        return
    if identity_list is not None and len(identity_list) > 5:
        print_output(False, "❌ identityList 最多不能超过 5 个", {"data": {}})
        return

    # 校验 page_size 范围
    if args.page_size is not None:
        if args.page_size < 10 or args.page_size > 50:
            print_output(False, "❌ 查询数量必须在 10~50 之间", {"data": {}})
            return

    try:
        result = find_total_inquiry_customers(
            buyer_type=args.buyer_type,
            follow_up_state_list=follow_up_state_list,
            nick_name=args.nick_name,
            tag_list=tag_list,
            start_time=args.start_time,
            end_time=args.end_time,
            min_pay_amt_180d=args.min_pay_amt_180d,
            max_pay_amt_180d=args.max_pay_amt_180d,
            last_sales_name=args.last_sales_name,
            identity_list=identity_list,
            is_buyer_active=args.is_buyer_active,
            page_size=args.page_size,
        )
        print_output(True, _render_markdown(result, args.page_size), {"data": result})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
