import json
import os
import sys
import argparse

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error
from capabilities.list_customer_details.service import list_customer_details

COMMAND_NAME = "list_customer_details"
COMMAND_DESC = "按筛选条件查询客户列表，或指定买家 ID 列表查询其客群信息"

DATE_TYPE_CN = {
    "RECENT_1": "近1天",
    "RECENT_7": "近7天",
    "RECENT_30": "近30天",
}


def _parse_json_list(value, param_name):
    """解析 JSON 字符串数组参数，失败则 print_output 并返回 None。"""
    try:
        parsed = json.loads(value)
        if not isinstance(parsed, list):
            raise ValueError(f"{param_name} 必须是 JSON 数组")
        return [str(x) for x in parsed]
    except json.JSONDecodeError as e:
        print_output(False, f"❌ {param_name} JSON 解析失败：{e}", {"data": {}})
        return None


def _render_list(data: dict) -> str:
    crowd_type = data.get("crowd_type", "")
    date_type = data.get("date_type", "")
    stat_date = data.get("stat_date", "")
    page_no = data.get("page_no", 1)
    page_size = data.get("page_size", 10)
    has_next = data.get("has_next", False)
    items = data.get("list", [])

    lines = [
        f"# 客户机会挖掘 — {crowd_type or '高价值买家筛选'}",
        "",
        "<!-- MODULE: customer_list -->",
        f"<!-- CROWD_TYPE: {crowd_type} -->",
        f"<!-- DATE_TYPE: {date_type} -->",
        f"<!-- STAT_DATE: {stat_date} -->",
        f"<!-- PAGE_COUNT: {len(items)} -->",
        f"<!-- HAS_NEXT: {str(has_next).lower()} -->",
    ]

    if not items:
        lines += [
            "<!-- STATUS: EMPTY -->",
            "",
            f"> 数据日期：{stat_date} | 时间范围：{DATE_TYPE_CN.get(date_type, date_type)}",
            "",
            "当前筛选条件暂无客户数据。",
            "",
            "<!-- /MODULE: customer_list -->",
        ]
        return "\n".join(lines)

    lines += [
        "<!-- STATUS: NORMAL -->",
        "",
        f"> 数据日期：{stat_date} | 时间范围：{DATE_TYPE_CN.get(date_type, date_type)} | 第 {page_no} 页（每页 {page_size} 条）",
        "",
        "| 客户 | 关系 | 月采购频率 | 月采购金额 | 最后询盘 | 重点客户 |",
        "|------|------|-----------|-----------|---------|---------|",
    ]
    for item in items:
        nick = item.get("nick") or "-"
        login_id = item.get("buyer_login_id") or "-"
        inq_rel = item.get("inq_relation") or "-"
        ord_cnt = item.get("ord_cnt_1m_level") or "-"
        gmv = item.get("gmv_1m_level") or "-"
        lst_inq = item.get("lst_inq_time") or "-"
        if_ka = "✅" if item.get("if_ka") == "Y" else "—"
        lines.append(f"| {nick}（{login_id}） | {inq_rel} | {ord_cnt} | {gmv} | {lst_inq} | {if_ka} |")

    lines += [
        "",
        f"> 共 {len(items)} 条，{'有' if has_next else '无'}下一页。"
        " 需要分析单个客户的跟进方案，可使用 `customer_crowd_analysis`。",
        "",
        "<!-- /MODULE: customer_list -->",
    ]
    return "\n".join(lines)


def _render_buyer_ids(data: dict) -> str:
    buyer_ids = data.get("buyer_login_id_list", data.get("buyer_user_id_list", []))
    stat_date = data.get("stat_date", "")
    order_list = data.get("order_list", [])
    inquiry_list = data.get("inquiry_list", [])

    lines = [
        f"# 买家客群信息（共 {len(buyer_ids)} 人）",
        "",
        "<!-- MODULE: buyer_crowd_info -->",
        f"<!-- BUYER_COUNT: {len(buyer_ids)} -->",
        f"<!-- STAT_DATE: {stat_date} -->",
        "",
    ]

    if order_list:
        lines += [
            "## 订单维度客群信息",
            "",
            "| 客户 | 关系 | 月采购频率 | 月采购金额 | 最后询盘 | 重点客户 |",
            "|------|------|-----------|-----------|---------|---------|",
        ]
        for item in order_list:
            nick = item.get("nick") or "-"
            login_id = item.get("buyer_login_id") or "-"
            inq_rel = item.get("inq_relation") or "-"
            ord_cnt = item.get("ord_cnt_1m_level") or "-"
            gmv = item.get("gmv_1m_level") or "-"
            lst_inq = item.get("lst_inq_time") or "-"
            if_ka = "✅" if item.get("if_ka") == "Y" else "—"
            lines.append(f"| {nick}（{login_id}） | {inq_rel} | {ord_cnt} | {gmv} | {lst_inq} | {if_ka} |")
        lines.append("")
    else:
        lines += ["## 订单维度客群信息", "", "> 暂无数据", ""]

    if inquiry_list:
        lines += [
            "## 询盘维度客群信息",
            "",
            "| 客户 | 关系 | 月采购频率 | 月采购金额 | 最后询盘 | 重点客户 |",
            "|------|------|-----------|-----------|---------|---------|",
        ]
        for item in inquiry_list:
            nick = item.get("nick") or "-"
            login_id = item.get("buyer_login_id") or "-"
            inq_rel = item.get("inq_relation") or "-"
            ord_cnt = item.get("ord_cnt_1m_level") or "-"
            gmv = item.get("gmv_1m_level") or "-"
            lst_inq = item.get("lst_inq_time") or "-"
            if_ka = "✅" if item.get("if_ka") == "Y" else "—"
            lines.append(f"| {nick}（{login_id}） | {inq_rel} | {ord_cnt} | {gmv} | {lst_inq} | {if_ka} |")
        lines.append("")
    else:
        lines += ["## 询盘维度客群信息", "", "> 暂无数据", ""]

    lines.append("<!-- /MODULE: buyer_crowd_info -->")
    return "\n".join(lines)


def _fetch_all(crowd_type=None, date_type="RECENT_30", stat_date=None,
               user_label_list=None, buyer_credit_level_list=None,
               ord_cnt_1m_level=None, gmv_1m_level=None, if_ka=None):
    """
    循环调用 list_customer_details 拉取全量数据。

    - page_size 强制 50（API 上限）
    - page_no 从 1 递增直到 has_next=false
    - 软保护上限：SOFT_LIMIT_PAGES=50（最多 2500 条），防上游异常死循环
    - 合并 list 后重写元信息：page_no=1, page_size=len(list), has_next=false
    """
    all_items = []
    page_no = 1
    last_result = None
    SOFT_LIMIT_PAGES = 50

    while True:
        result = list_customer_details(
            crowd_type=crowd_type,
            date_type=date_type,
            page_no=page_no,
            page_size=50,
            stat_date=stat_date,
            user_label_list=user_label_list,
            buyer_credit_level_list=buyer_credit_level_list,
            ord_cnt_1m_level=ord_cnt_1m_level,
            gmv_1m_level=gmv_1m_level,
            if_ka=if_ka,
        )
        all_items.extend(result.get("list", []))
        last_result = result
        if not result.get("has_next"):
            break
        page_no += 1
        if page_no > SOFT_LIMIT_PAGES:
            break

    last_result["list"] = all_items
    last_result["page_no"] = 1
    last_result["page_size"] = len(all_items)
    last_result["has_next"] = False
    return last_result


def main():
    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，请运行：`python cli.py configure YOUR_AK`",
                     {"data": {}})
        return

    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("-t", "--crowd-type",
                        help="人群类型：流失买家/周期采购/询盘未成交/老客促活（可与其他筛选条件组合）")
    parser.add_argument("-d", "--date-type", default="RECENT_7",
                        help="时间范围：RECENT_1/RECENT_7/RECENT_30（默认 RECENT_7）")
    parser.add_argument("-p", "--page-no", type=int, default=1, help="页码（默认 1）")
    parser.add_argument("-s", "--page-size", type=int, default=10, help="每页条数，最大 50（默认 10）")
    parser.add_argument("--stat-date", help="统计日期 YYYYMMDD（默认昨日）")
    parser.add_argument("--buyer-login-ids",
                        help='买家 loginId JSON 数组，例：\'["alice","bob"]\'')
    parser.add_argument("--user-label-list",
                        help='买家标签 JSON 数组，例：\'["B类买家"]\'')
    parser.add_argument("--buyer-credit-level-list",
                        help='买家等级 JSON 数组，例：\'["金牌","银牌"]\'')
    parser.add_argument("--ord-cnt-1m-level",
                        help="月采购频率水平：高/中/低")
    parser.add_argument("--gmv-1m-level",
                        help="月采购金额水平：高/中/低")
    parser.add_argument("--if-ka",
                        help="是否重点客户：Y/N")
    parser.add_argument("--fetch-all", action="store_true",
                        help="自动循环翻页（page_size=50）直到 has_next=false，合并所有结果。"
                             "与 --buyer-login-ids 互斥；--page-no/--page-size 由内部控制")
    args = parser.parse_args()

    has_filter = any([
        args.crowd_type, args.buyer_login_ids, args.user_label_list,
        args.buyer_credit_level_list, args.ord_cnt_1m_level,
        args.gmv_1m_level, args.if_ka,
    ])
    if not has_filter:
        print_output(False,
                     "❌ 参数错误：至少需要传一个筛选条件（--crowd-type / --buyer-login-ids / "
                     "--user-label-list / --buyer-credit-level-list / "
                     "--ord-cnt-1m-level / --gmv-1m-level / --if-ka）",
                     {"data": {}})
        return

    if args.fetch_all and args.buyer_login_ids:
        print_output(False,
                     "❌ 参数错误：--fetch-all 与 --buyer-login-ids 互斥（按买家 ID 查询本身不分页）",
                     {"data": {}})
        return

    try:
        if args.buyer_login_ids:
            buyer_list = _parse_json_list(args.buyer_login_ids, "--buyer-login-ids")
            if buyer_list is None:
                return
            result = list_customer_details(
                date_type=args.date_type,
                page_no=args.page_no,
                page_size=args.page_size,
                stat_date=args.stat_date,
                buyer_login_ids=buyer_list,
            )
            print_output(True, _render_buyer_ids(result), {"data": result})
        else:
            user_label_list = None
            if args.user_label_list:
                user_label_list = _parse_json_list(args.user_label_list, "--user-label-list")
                if user_label_list is None:
                    return

            buyer_credit_level_list = None
            if args.buyer_credit_level_list:
                buyer_credit_level_list = _parse_json_list(args.buyer_credit_level_list, "--buyer-credit-level-list")
                if buyer_credit_level_list is None:
                    return

            if args.fetch_all:
                result = _fetch_all(
                    crowd_type=args.crowd_type,
                    date_type=args.date_type,
                    stat_date=args.stat_date,
                    user_label_list=user_label_list,
                    buyer_credit_level_list=buyer_credit_level_list,
                    ord_cnt_1m_level=args.ord_cnt_1m_level,
                    gmv_1m_level=args.gmv_1m_level,
                    if_ka=args.if_ka,
                )
            else:
                result = list_customer_details(
                    crowd_type=args.crowd_type,
                    date_type=args.date_type,
                    page_no=args.page_no,
                    page_size=args.page_size,
                    stat_date=args.stat_date,
                    user_label_list=user_label_list,
                    buyer_credit_level_list=buyer_credit_level_list,
                    ord_cnt_1m_level=args.ord_cnt_1m_level,
                    gmv_1m_level=args.gmv_1m_level,
                    if_ka=args.if_ka,
                )
            print_output(True, _render_list(result), {"data": result})

    except ValueError as e:
        print_output(False, f"❌ 参数错误：{e}", {"data": {}})
    except Exception as e:
        print_error(e, {"data": {}})


if __name__ == "__main__":
    main()
