#!/usr/bin/env python3
"""多店铺日报批量查询 CLI 入口"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta

sys.path.insert(0, os.path.normpath(os.path.join(os.path.dirname(__file__), '..', '..')))

from _auth import get_ak_from_env
from _output import print_output, print_error, make_output
from capabilities.get_multi_shop_report.service import get_multi_shop_report

COMMAND_NAME = "get_multi_shop_report"
COMMAND_DESC = "批量并行查询多店铺日报数据（交易+流量+用户），含前一天环比数据"

# 【首屏白名单】基础日报真正会用到的当日字段，与 SKILL.md「报告生成规范·报告模板」逐项对应。
# 未列入的字段（uvCtr / adExposure / 新老买家等）留在落盘的完整 JSON 里，供【深度补充分析】
# 阶段按需读取；首屏不返回。白名单与首屏模板必须保持一致：模板里不提的字段才能砍，
# 否则模型拿不到数据又被要求展示，就可能凭现有指标推算出一个看似合理的数字。
_SUMMARY_SHOP_FIELDS = (
    "gmv", "gmvDayOnDay", "gmvWeekOnWeek",
    "orderCount", "orderDayOnDay", "orderWeekOnWeek",
    "uv", "uvDayOnDay", "uvWeekOnWeek",
    "pv", "pvDayOnDay",
    "searchUv", "searchUvDayOnDay", "searchExposure",
    "payConversionRate", "avgPrice", "avgPriceWeekOnWeek", "bounceRate",
    "inquiryCount", "inquiryDayOnDay", "inquiryWeekOnWeek",
)

# 【交叉校验基数】保留这几项前一天原始值，供 Agent 在环比异常或为 null 时自行比对两天数值
# （SKILL.md「输出格式·特殊值处理规则」依赖这条兜底路径）；完整 prevDay 不进首屏。
# 去掉基数等于把环比从「可校验」变成「错了也看不出」，因此这几个字段不得精简。
_SUMMARY_PREV_FIELDS = ("gmv", "orderCount", "uv", "payConversionRate", "bounceRate")
# 上周同日校验基数：转化率等不算周环比的指标，需要时用这里的原值直接比对
_SUMMARY_WEEK_FIELDS = ("gmv", "orderCount", "uv", "payConversionRate")

_SUMMARY_AD_TODAY = ("spend", "exposure", "clicks", "ctr", "inquiries", "deals", "deal_amount", "roi")
_SUMMARY_AD_PREV = ("spend", "deals", "deal_amount", "roi")
_SUMMARY_AD_PLAN = ("name", "spend", "deals", "deal_amount", "roi")
_SUMMARY_REVIEW = ("total", "good", "neutral", "bad", "goodRate", "badRate", "goodReasons", "badReasons")
_SUMMARY_REVIEW_PRODUCT = ("name", "total", "bad", "goodRate")


def _pick(src, keys):
    """按白名单投影字段。

    一律用 `.get(k)` 保留 None，**绝不可写成 `.get(k, 0)`**：查询失败店铺的 today 为 None、
    环比无基数时也为 None，一旦被填成 0，就会把「数据获取失败」伪装成「零成交」，直接制造假数据。
    """
    if not isinstance(src, dict):
        return None
    return {k: src.get(k) for k in keys}


def _summarize_shop(shop: dict) -> dict:
    """单店投影：店铺标识 + 首屏当日指标 + 前一天校验基数"""
    item = {
        "companyName": shop.get("companyName"),
        # loginId 不展示给用户，但【深度补充】阶段筛选活跃店铺、发起补充查询时需要它
        "loginId": shop.get("loginId"),
        "error": shop.get("error"),
    }
    today = _pick(shop.get("today"), _SUMMARY_SHOP_FIELDS)
    # today 为 None（该店查询失败）时，字段仍全部置 null 并保留 error，不能退化为 0
    item.update(today if today is not None else {k: None for k in _SUMMARY_SHOP_FIELDS})
    item["prev"] = _pick(shop.get("prevDay"), _SUMMARY_PREV_FIELDS)
    item["weekAgo"] = _pick(shop.get("weekAgo"), _SUMMARY_WEEK_FIELDS)
    return item


def _summarize_ad(ad) -> dict:
    """广告投影；hasData=False 或查询失败时返回 None（SKILL.md 规定此时省略广告板块）"""
    if not isinstance(ad, dict) or not ad.get("hasData"):
        return None
    return {
        "today": _pick(ad.get("today"), _SUMMARY_AD_TODAY),
        "prevDay": _pick(ad.get("prevDay"), _SUMMARY_AD_PREV),
        "changes": ad.get("changes"),
        "topPlans": [_pick(p, _SUMMARY_AD_PLAN) for p in (ad.get("topPlans") or [])],
    }


def _summarize_review(review) -> dict:
    """评价投影；hasData=False 或查询失败时返回 None

    好/差评原因原文保留不截断——它们是评价板块与行动建议的主要依据，截断会丢掉关键事实
    （如“一个月未发货”这类履约问题）。商品维度只留有差评的前 3 款用于定位风险款，
    完整 topProducts 清单在落盘文件里。
    """
    if not isinstance(review, dict) or not review.get("hasData"):
        return None
    summary = review.get("summary") or {}
    result = _pick(summary, _SUMMARY_REVIEW) or {}
    result["riskProducts"] = [
        _pick(p, _SUMMARY_REVIEW_PRODUCT)
        for p in (summary.get("topProducts") or [])
        if isinstance(p, dict) and (p.get("bad") or 0) > 0
    ][:3]
    return result


def build_summary(result: dict) -> dict:
    """从完整结果提取首屏所需的精简结构（体积约为完整结果的 1/4，可直接读 stdout）"""
    return {
        "query_date": result.get("query_date"),
        "prev_date": result.get("prev_date"),
        "week_date": result.get("week_date"),
        "shops": [_summarize_shop(s) for s in (result.get("shops") or [])],
        "adReport": _summarize_ad(result.get("adReport")),
        "reviewData": _summarize_review(result.get("reviewData")),
    }


def _calc_prev_date(date_str: str) -> str:
    """计算前一天日期"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    prev = date_obj - timedelta(days=1)
    return prev.strftime("%Y-%m-%d")


def _calc_week_date(date_str: str) -> str:
    """计算上周同日（queryDate - 7 天），用于自算周环比"""
    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
    return (date_obj - timedelta(days=7)).strftime("%Y-%m-%d")


def _dump_full(path: str, markdown: str, data: dict) -> str:
    """将完整结果写入文件（自动创建父目录），返回绝对路径

    避免 Agent 端手动 `mkdir` + shell 重定向：目录不存在时由本函数创建，
    保证在任意部署目录下都能落盘成功。
    """
    abspath = os.path.abspath(os.path.expanduser(path))
    os.makedirs(os.path.dirname(abspath), exist_ok=True)
    # 以缩进多行格式写入（而非压缩单行）：多行 JSON 可被读文件工具按行范围分段读取，
    # 避免一条超长单行被从中间硬截断、进而迫使 Agent 改用临时脚本读取。
    with open(abspath, "w", encoding="utf-8") as f:
        json.dump(make_output(True, markdown, data), f, ensure_ascii=False, indent=2)
    return abspath


def _write_output_file(path: str, markdown: str, data: dict):
    """全量落盘模式：stdout 仅回执路径与摘要"""
    abspath = _dump_full(path, markdown, data)
    shop_count = len(data.get("shops", [])) if isinstance(data, dict) else 0
    print_output(
        True,
        f"多店铺日报已写入 {abspath}（{shop_count} 家店铺），请读取该文件解析完整 JSON",
        {"output_file": abspath, "shopCount": shop_count},
    )


def main():
    parser = argparse.ArgumentParser(description=COMMAND_DESC)
    parser.add_argument("--query_date", required=True, help="查询日期，格式 YYYY-MM-DD")
    parser.add_argument("--NEWTON_SHOP_LOGIN_ID", required=False, default=None,
                        help="可选，指定则仅查询该店铺（单店铺模式复用同一套并发管线）")
    parser.add_argument(
        "--output_file",
        help="将完整 JSON 结果写入该文件（自动创建目录，无需手动 mkdir）；stdout 仅打印摘要",
    )
    parser.add_argument(
        "--summary_only",
        action="store_true",
        help="stdout 直接输出首屏所需的精简结构（可一次读完，无需再读文件）；"
             "同时传 --output_file 时，完整数据仍会落盘供深度补充阶段按需读取",
    )
    parser.add_argument(
        "--no_week_on_week",
        action="store_true",
        help="不查上周同日数据（默认会查）。接口的周环比预计算字段除 GMV 外恒为 0，"
             "因此周环比只能多查一天自算；加本开关可省下 1/3 接口调用量（代价：无周环比）",
    )
    args = parser.parse_args()

    ak_id, _ = get_ak_from_env()
    if not ak_id:
        print_output(False,
                     "❌ AK 未配置，无法查询多店铺日报。\n\n请补充有效 AK 或检查鉴权配置后重试",
                     {"data": {}})
        return

    prev_date = _calc_prev_date(args.query_date)
    week_date = None if args.no_week_on_week else _calc_week_date(args.query_date)
    login_id = getattr(args, 'NEWTON_SHOP_LOGIN_ID', None)

    try:
        result = get_multi_shop_report(
            query_date=args.query_date,
            prev_date=prev_date,
            login_id=login_id,
            week_date=week_date,
        )
        if args.summary_only:
            summary = build_summary(result)
            shop_count = len(summary.get("shops") or [])
            markdown = f"多店铺日报精简数据（{shop_count} 家店铺），可直接解析本输出生成基础日报"
            if args.output_file:
                abspath = _dump_full(args.output_file, "多店铺日报查询成功", result)
                summary["full_data_file"] = abspath
                markdown += "；完整数据已落盘，深度补充阶段再按需读取"
            print_output(True, markdown, summary)
        elif args.output_file:
            _write_output_file(args.output_file, "多店铺日报查询成功", result)
        else:
            print_output(True, "多店铺日报查询成功", result)
    except Exception as exc:
        print_error(exc, {})


if __name__ == "__main__":
    main()
