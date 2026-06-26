#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
招投标活动一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List
from collections import Counter
from .base import call_api, debug_print


# ============ 辅助函数 ============

def _format_number(value: Any) -> str:
    """格式化数字，移除不必要的小数位"""
    if value is None or value == '':
        return ''

    try:
        num = float(value)
        if num == int(num):
            return str(int(num))
        return f"{num:.2f}"
    except (ValueError, TypeError):
        return str(value)


def _safe_float_convert(value: Any) -> float:
    """安全地将值转换为浮点数"""
    if value is None or value == "":
        return 0.0
    try:
        if isinstance(value, str):
            value = value.strip().replace("元", "").replace(",", "")
        return float(value)
    except (ValueError, TypeError):
        return 0.0


# ============ API 调用 ============

def _call_bidding_api(entname: str) -> Dict[str, Any]:
    """调用招投标 API"""
    params = {
        'entname': entname,
        'mask': '0000100',
        'enableaggregate': 'true',
        'page': 1,
        'size': 100
    }
    response = call_api('/bidNotice', params, method='POST')
    return response


# ============ 数据处理 ============

def _process_api_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理 API 返回的数据"""
    raw_data = response.get('data', {})
    total_count = response.get('totalcount', 0)
    party_role_count = response.get('PartyRoleCount', {})
    year_party_count = response.get('YearPartyCount', [])

    result = {
        "角色方数量统计": [],
        "年份角色方统计": [],
        "总数量": total_count,
        "数据": []
    }

    # 处理不同的数据结构
    notices = []
    if isinstance(raw_data, list):
        notices = raw_data[:500]
    elif isinstance(raw_data, dict):
        if 'notices' in raw_data:
            notices = raw_data.get('notices', [])[:500]
        elif 'data' in raw_data:
            data = raw_data.get('data', [])
            notices = data[:500] if isinstance(data, list) else []
        elif 'result' in raw_data:
            result_data = raw_data.get('result', [])
            notices = result_data[:500] if isinstance(result_data, list) else []
        elif 'list' in raw_data:
            list_data = raw_data.get('list', [])
            notices = list_data[:500] if isinstance(list_data, list) else []
        else:
            notices = [raw_data] if raw_data else []

    # 处理每条公告
    for notice in notices:
        notice_info = notice.get("noticeInfo", {})
        project_info = notice.get("projectInfo", {})

        notice_project_info = {
            "公告标题": notice_info.get("title", ""),
            "公告日期": notice_info.get("notice_date", ""),
            "信息来源": notice_info.get("information_source", ""),
            "采购系统": project_info.get("procurementsystem", ""),
            "信息类型一级中文": notice_info.get("notice_type_first_class", ""),
            "信息类型二级中文": notice_info.get("notice_type_second_class", ""),
            "项目编号": project_info.get("project_num", ""),
            "采购方式中文": project_info.get("purchase_way_cn", ""),
            "省份名称": project_info.get("province", ""),
            "地市名称": project_info.get("city", ""),
            "区县名称": project_info.get("county", ""),
            "资金来源": project_info.get("moneysource", ""),
            "采购类型": project_info.get("purchase_type", ""),
            "招投标一级行业": project_info.get("primaryindustry", ""),
            "招投标二级行业": project_info.get("secondaryindustry", ""),
            "服务期限": project_info.get("servicetime", ""),
            "预算总金额（元）": project_info.get("budget_amount_value", ""),
            "项目资质": project_info.get("project_qual", ""),
            "采购内容": project_info.get("purchase_content", "")
        }

        # 处理招标人列表
        current_tenderee_list = []
        for tenderee in notice.get("tendereeList", []):
            tenderee_name = tenderee.get("the_tenderee", "")
            if tenderee_name:
                current_tenderee_list.append({"招标人": tenderee_name})

        # 处理中标人列表
        current_win_tenderer_list = []
        for win_tenderer in notice.get("winTendererList", []):
            win_tenderer_name = win_tenderer.get("the_win_tenderer", "")
            win_bidding_amount = win_tenderer.get("win_bidding_amount", "")
            if win_tenderer_name:
                current_win_tenderer_list.append({
                    "中标人": win_tenderer_name,
                    "中标金额（元）": win_bidding_amount
                })

        # 处理中标候选人列表
        current_win_candidate_list = []
        for win_candidate in notice.get("winCandidateList", []):
            win_candidate_name = win_candidate.get("the_win_candidate", "")
            candidate_bidding_amount = win_candidate.get("candidate_bidding_amount", "")
            if win_candidate_name:
                candidate_item = {"中标候选人": win_candidate_name}
                if candidate_bidding_amount:
                    candidate_item["报价金额（元）"] = candidate_bidding_amount
                current_win_candidate_list.append(candidate_item)

        notice_data_item = {
            "招标项目信息": notice_project_info,
            "招标人列表": current_tenderee_list,
            "中标人列表": current_win_tenderer_list,
            "中标候选人列表": current_win_candidate_list
        }
        result["数据"].append(notice_data_item)

    # 设置统计结果
    if party_role_count:
        role_stats = {
            "企业招标的次数": party_role_count.get("the_tenderee_count_total", 0),
            "作为招标人的货物类采购次数": party_role_count.get("the_tenderee_goods_count", 0),
            "作为招标人的服务类采购次数": party_role_count.get("the_tenderee_services_count", 0),
            "作为招标人的工程类采购次数": party_role_count.get("the_tenderee_works_count", 0),
            "企业中标的次数": party_role_count.get("the_win_tenderer_count_total", 0),
            "作为中标人的货物类中标次数": party_role_count.get("the_win_tenderer_goods_count", 0),
            "作为中标人的服务类中标次数": party_role_count.get("the_win_tenderer_services_count", 0),
            "作为中标人的工程类中标次数": party_role_count.get("the_win_tenderer_works_count", 0)
        }
        result["角色方数量统计"] = [role_stats] if any(role_stats.values()) else []

    # 年份统计数据
    if year_party_count:
        year_stats = []
        for year_data in year_party_count:
            year_stat = {
                "年份": year_data.get("year", ""),
                "作为招标人数量": year_data.get("the_tenderee_count", 0),
                "作为招标人总金额（元）": year_data.get("the_tenderee_amount", 0),
                "作为中标人数量": year_data.get("the_win_tenderer_count", 0),
                "企业作为中标人的中标金额（元）": year_data.get("the_win_tenderer_win_bidding_amount", 0)
            }
            year_stats.append(year_stat)
        result["年份角色方统计"] = year_stats

    return result


# ============ Markdown 格式化 ============

def _extract_enterprise_journey(data_list: List[Dict]) -> str:
    """提取企业历程"""
    lines = ["### 企业历程"]

    dated_projects = []
    for item in data_list:
        info = item.get('招标项目信息', {})
        date = info.get('公告日期', '')
        title = info.get('公告标题', '')
        project_no = info.get('项目编号', '')
        if date and title:
            dated_projects.append((date, title, project_no))

    dated_projects.sort(reverse=True)

    if dated_projects:
        lines.append("重大招投标项目时间线")
        project_strs = []
        for date, title, project_no in dated_projects[:20]:
            date_str = date[:10] if len(date) >= 10 else date
            project_str = f"公告日期：{date_str}，公告标题：{title}"
            if project_no:
                project_str += f"，项目编号：{project_no}"
            project_strs.append(project_str)
        lines.append('；'.join(project_strs))

    return '\n'.join(lines)


def _extract_main_business(data_list: List[Dict]) -> str:
    """提取主营业务"""
    lines = ["### 主营业务"]

    # 采购类型分布
    purchase_types = []
    for item in data_list:
        info = item.get('招标项目信息', {})
        ptype = info.get('采购类型', '')
        if ptype:
            purchase_types.append(ptype)

    if purchase_types:
        type_counter = Counter(purchase_types)
        type_strs = [f"{k}（{v}次）" for k, v in type_counter.most_common()]
        lines.append(f"采购类型分布：{', '.join(type_strs)}")

    # 行业领域聚焦
    industries_1 = []
    industries_2 = []
    for item in data_list:
        info = item.get('招标项目信息', {})
        ind1 = info.get('招投标一级行业', '')
        ind2 = info.get('招投标二级行业', '')
        if ind1:
            industries_1.append(ind1)
        if ind2:
            industries_2.append(ind2)

    if industries_1:
        ind1_counter = Counter(industries_1)
        ind1_strs = [f"{k}（{v}次）" for k, v in ind1_counter.most_common(10)]
        lines.append(f"行业领域聚焦（一级）：{', '.join(ind1_strs)}")

    if industries_2:
        ind2_counter = Counter(industries_2)
        ind2_strs = [f"{k}（{v}次）" for k, v in ind2_counter.most_common(10)]
        lines.append(f"行业领域聚焦（二级）：{', '.join(ind2_strs)}")

    return '\n'.join(lines)


def _extract_market_competitiveness(role_stats: List[Dict], data_list: List[Dict]) -> str:
    """提取市场竞争力"""
    lines = ["### 市场竞争力"]

    if role_stats:
        stats = role_stats[0]

        win_count = stats.get('企业中标的次数', 0)
        lines.append(f"中标项目总数：{win_count}次")

        goods = stats.get('作为中标人的货物类中标次数', 0)
        service = stats.get('作为中标人的服务类中标次数', 0)
        engineering = stats.get('作为中标人的工程类中标次数', 0)
        lines.append(f"各类别中标数量：货物类{goods}次、服务类{service}次、工程类{engineering}次")

        total_amount = 0.0
        for item in data_list:
            winners = item.get('中标人列表', [])
            for winner in winners:
                amount = winner.get('中标金额（元）')
                if amount is not None:
                    total_amount += _safe_float_convert(amount)

        if total_amount > 0:
            total_formatted = _format_number(total_amount)
            total_wan = _format_number(total_amount / 10000)
            lines.append(f"中标金额统计：累计中标金额{total_formatted}元（约{total_wan}万元）")

        bid_count = stats.get('企业招标的次数', 0)
        if bid_count > 0:
            lines.append(f"市场拓展能力指标：企业作为招标人{bid_count}次，作为中标人{win_count}次")
        else:
            lines.append(f"市场拓展能力指标：企业主要作为中标人参与项目（{win_count}次）")

    return '\n'.join(lines)


def _extract_brand_influence(data_list: List[Dict]) -> str:
    """提取品牌影响力"""
    lines = ["### 品牌影响力"]

    sources = []
    for item in data_list:
        info = item.get('招标项目信息', {})
        source = info.get('信息来源', '')
        if source:
            sources.append(source)

    if sources:
        source_counter = Counter(sources)
        source_strs = [f"{k}（{v}次）" for k, v in source_counter.most_common(10)]
        lines.append(f"招标公告来源：{', '.join(source_strs)}")

    bidders = []
    for item in data_list:
        bidder_list = item.get('招标人列表', [])
        for bidder in bidder_list:
            name = bidder.get('招标人', '')
            if name:
                bidders.append(name)

    if bidders:
        bidder_counter = Counter(bidders)
        bidder_strs = [f"{k}（{v}次）" for k, v in bidder_counter.most_common(10)]
        lines.append(f"招标人背景分析：{', '.join(bidder_strs)}")

    return '\n'.join(lines)


def _extract_operation_capital(yearly_stats: List[Dict], data_list: List[Dict]) -> str:
    """提取经营与资本"""
    lines = ["### 经营与资本"]

    # 预算金额分析
    budgets = []
    for item in data_list:
        info = item.get('招标项目信息', {})
        budget = info.get('预算总金额（元）')
        if budget is not None:
            val = _safe_float_convert(budget)
            if val > 0:
                budgets.append(val)

    if budgets:
        total_budget = sum(budgets)
        avg_budget = total_budget / len(budgets)
        total_formatted = _format_number(total_budget)
        avg_formatted = _format_number(avg_budget)
        lines.append(f"预算金额分析：{len(budgets)}个项目有预算数据，合计{total_formatted}元，平均{avg_formatted}元")

    # 中标金额分析
    win_amounts = []
    for item in data_list:
        winners = item.get('中标人列表', [])
        for winner in winners:
            amount = winner.get('中标金额（元）')
            if amount is not None:
                val = _safe_float_convert(amount)
                if val > 0:
                    win_amounts.append(val)

    if win_amounts:
        total_win = sum(win_amounts)
        avg_win = total_win / len(win_amounts)
        total_formatted = _format_number(total_win)
        avg_formatted = _format_number(avg_win)
        lines.append(f"中标金额分析：{len(win_amounts)}个中标项目有金额数据，合计{total_formatted}元，平均{avg_formatted}元")

    lines.append(f"招标行为统计：企业参与{len(data_list)}个招投标项目")

    # 年度趋势数据
    if yearly_stats:
        sorted_stats = sorted(yearly_stats, key=lambda x: x.get('年份', 0))
        trend_strs = []

        for stat in sorted_stats[-10:]:
            year = stat.get('年份', '')
            bid_count = stat.get('作为招标人数量', 0)
            bid_amount = stat.get('作为招标人总金额（元）', 0)
            win_count = stat.get('作为中标人数量', 0)
            win_amount = stat.get('企业作为中标人的中标金额（元）', 0)

            if year and (bid_count > 0 or win_count > 0):
                year_info = f"{year}年"
                details = []
                if bid_count > 0:
                    bid_amt_str = _format_number(bid_amount)
                    details.append(f"招标{bid_count}次（{bid_amt_str}元）")
                if win_count > 0:
                    win_amt_str = _format_number(win_amount)
                    details.append(f"中标{win_count}次（{win_amt_str}元）")

                if details:
                    year_info += "：" + "、".join(details)
                    trend_strs.append(year_info)

        if trend_strs:
            lines.append(f"年度趋势数据：{'; '.join(trend_strs)}")

    return '\n'.join(lines)


def _extract_value_growth(data_list: List[Dict]) -> str:
    """提取价值与成长"""
    lines = ["### 价值与成长"]

    provinces = []
    cities = []

    for item in data_list:
        info = item.get('招标项目信息', {})
        province = info.get('省份名称', '')
        city = info.get('地市名称', '')

        if province:
            provinces.append(province)
        if city:
            cities.append(city)

    if provinces:
        province_counter = Counter(provinces)
        prov_strs = [f"{k}（{v}次）" for k, v in province_counter.most_common(10)]
        lines.append(f"地域分布特征（省份）：{', '.join(prov_strs)}")

    if cities:
        city_counter = Counter(cities)
        city_strs = [f"{k}（{v}次）" for k, v in city_counter.most_common(10)]
        lines.append(f"地域分布特征（城市）：{', '.join(city_strs)}")

    if provinces:
        province_count = len(set(provinces))
        city_count = len(set(cities)) if cities else 0
        lines.append(f"区域市场渗透情况：覆盖{province_count}个省份、{city_count}个城市")

    return '\n'.join(lines)


def _extract_enterprise_relations(data_list: List[Dict]) -> str:
    """提取企业关联分析"""
    lines = ["### 企业关联分析"]

    bidders = []
    for item in data_list:
        bidder_list = item.get('招标人列表', [])
        for bidder in bidder_list:
            name = bidder.get('招标人', '')
            if name:
                bidders.append(name)

    if bidders:
        bidder_counter = Counter(bidders)
        bidder_strs = [f"{k}（{v}次）" for k, v in bidder_counter.most_common(15)]
        lines.append(f"招标人关系网络：{', '.join(bidder_strs)}")

    winners = []
    for item in data_list:
        winner_list = item.get('中标人列表', [])
        for winner in winner_list:
            name = winner.get('中标人', '')
            if name:
                winners.append(name)

    if winners:
        winner_counter = Counter(winners)
        winner_strs = [f"{k}（{v}次）" for k, v in winner_counter.most_common(15)]
        lines.append(f"中标人合作图谱：{', '.join(winner_strs)}")

    return '\n'.join(lines)


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    data_list = data.get('数据', [])
    role_stats = data.get('角色方数量统计', [])
    yearly_stats = data.get('年份角色方统计', [])

    if not data_list:
        return "# 招投标活动\n\n暂无招投标数据"

    sections = ["# 招投标信息提炼"]

    # 企业历程
    sections.append("")
    sections.append(_extract_enterprise_journey(data_list))

    # 主营业务
    sections.append("")
    sections.append(_extract_main_business(data_list))

    # 市场竞争力
    if role_stats:
        sections.append("")
        sections.append(_extract_market_competitiveness(role_stats, data_list))

    # 品牌影响力
    sections.append("")
    sections.append(_extract_brand_influence(data_list))

    # 经营与资本
    sections.append("")
    sections.append(_extract_operation_capital(yearly_stats, data_list))

    # 价值与成长
    sections.append("")
    sections.append(_extract_value_growth(data_list))

    # 企业关联分析
    sections.append("")
    sections.append(_extract_enterprise_relations(data_list))

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业招投标信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的招投标信息
    """
    # 1. 调用 API
    response = _call_bidding_api(entname)

    # 检查响应状态
    if response.get('code') != 200:
        return "# 招投标活动\n\n未查询到招投标信息"

    # 2. 处理数据
    processed_data = _process_api_data(response)

    if not processed_data.get('数据'):
        return "# 招投标活动\n\n暂无招投标数据"

    # 3. 生成 Markdown
    return _format_markdown(processed_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s14_bidding <企业名称>")
