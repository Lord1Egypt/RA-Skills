#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业经营动态一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List
from collections import defaultdict
from .base import call_api, debug_print


# ============ 映射表 ============

FIELD_MAPPING = {
    'yearcount': '按年份统计经营事件信息',
    'totalcount': '经营事件总数量',
    'clueinfo': '经营事件信息',
    'cluetype': '经营事件类型名称',
    'cluedesc': '经营事件内容',
    'datasource': '经营事件来源',
    'date': '经营事件发生日期',
    'year': '经营事件统计年份',
    'year_clue_count': '经营事件每年数量统计'
}

FIELDS_TO_REMOVE = ['cluecode', 'demandcode', 'demandname', 'businesscode',
                   'businesstype', 'prodcode', 'prodtype', 'clueid', 'updatetime', 'cluelevel']


# ============ API 调用 ============

def _call_operations_api(entname: str) -> Dict[str, Any]:
    """调用企业经营事件 API"""
    response = call_api('/businessOpportunityQuery', {'entname': entname, 'size': 100}, method='POST')
    return response


# ============ 数据处理 ============

def _process_api_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理 API 返回的数据"""
    import copy
    processed_data = copy.deepcopy(response)

    # 移除不需要的顶级字段
    for field in ['totalpage', 'page', 'size', 'code', 'msg']:
        processed_data.pop(field, None)

    # 处理顶级字段映射
    for old_key, new_key in FIELD_MAPPING.items():
        if old_key in processed_data:
            processed_data[new_key] = processed_data.pop(old_key)

    # 如果存在经营事件信息列表，处理每个条目
    if '经营事件信息' in processed_data and isinstance(processed_data['经营事件信息'], list):
        for clue_item in processed_data['经营事件信息']:
            # 移除不需要的字段
            for field in FIELDS_TO_REMOVE:
                clue_item.pop(field, None)

            # 映射字段名为中文
            clue_mapping = {}
            for old_key, value in list(clue_item.items()):
                if old_key in FIELD_MAPPING:
                    clue_mapping[FIELD_MAPPING[old_key]] = value
                else:
                    clue_mapping[old_key] = value

            clue_item.clear()
            clue_item.update(clue_mapping)

    # 处理按年份统计信息
    if '按年份统计经营事件信息' in processed_data and isinstance(processed_data['按年份统计经营事件信息'], list):
        for year_item in processed_data['按年份统计经营事件信息']:
            if isinstance(year_item, dict):
                year_mapping = {}
                for old_key, value in list(year_item.items()):
                    if old_key in FIELD_MAPPING:
                        year_mapping[FIELD_MAPPING[old_key]] = value
                    else:
                        year_mapping[old_key] = value
                year_item.clear()
                year_item.update(year_mapping)

    return processed_data


# ============ Markdown 格式化 ============

def _extract_enterprise_history(events: List[Dict[str, Any]]) -> str:
    """企业历程 - 按时间排序的重大事件清单"""
    if not events:
        return ""

    lines = ["### 企业历程"]

    # 按日期分组事件
    events_by_date = defaultdict(list)
    for event in events:
        date = event.get('经营事件发生日期', '')
        if date:
            events_by_date[date].append(event)

    # 按时间排序
    sorted_dates = sorted(events_by_date.keys())

    event_descriptions = []
    for date in sorted_dates:
        date_events = events_by_date[date]
        event_parts = []
        for event in date_events:
            content = event.get('经营事件内容', '').strip()
            event_type = event.get('经营事件类型名称', '')

            # 简化事件描述
            simplified = ""
            if event_type == "债券发行披露":
                if "债券名称：" in content:
                    bond_name = content.split("债券名称：")[1].split(",")[0].strip()
                    simplified = f"{bond_name}发行披露"
            elif event_type == "债券即将到期":
                if "债券名称：" in content:
                    bond_name = content.split("债券名称：")[1].split(",")[0].strip()
                    simplified = f"{bond_name}即将到期"
            elif event_type in ["新增中标", "中标政府项目"]:
                if "项目名称为" in content and "招标方为" in content:
                    try:
                        project_name = content.split("项目名称为")[1].split(",")[0].strip()
                        bidder_part = content.split("招标方为")[1].split(",")[0].strip()
                        simplified = f"{bidder_part}{project_name}中标"
                    except (IndexError, ValueError):
                        simplified = content[:100]
            else:
                simplified = content[:150]

            if simplified:
                event_parts.append(simplified)

        if event_parts:
            event_descriptions.append(f"{date}{'，'.join(event_parts)}")

    if event_descriptions:
        event_list = "按时间排序的重大事件清单：" + "；".join(event_descriptions[:10]) + "..."
        lines.append(event_list)

    # 提取事件类型分类
    event_types = set()
    for event in events:
        event_type = event.get('经营事件类型名称', '')
        if event_type:
            event_types.add(event_type)

    if event_types:
        type_list = "事件类型分类：" + "、".join(sorted(event_types))
        lines.append(type_list)

    # 提取事件来源
    sources = set()
    for event in events:
        source = event.get('经营事件来源', '')
        if source:
            sources.add(source)

    if sources:
        source_list = "事件来源标注：" + "、".join(sorted(sources))
        lines.append(source_list)

    return '\n'.join(lines)


def _extract_main_business(events: List[Dict[str, Any]]) -> str:
    """主营业务"""
    if not events:
        return ""

    lines = ["### 主营业务"]

    # 事件类型统计
    event_types = set()
    for event in events:
        event_type = event.get('经营事件类型名称', '')
        if event_type:
            event_types.add(event_type)

    if event_types:
        lines.append("主营业务事件类型统计：" + "、".join(sorted(event_types)))

    # 经营模式关键词
    business_keywords = []
    if "债券发行披露" in event_types or "债券即将到期" in event_types:
        business_keywords.append("债券发行与到期管理")
    if "中标政府项目" in event_types or "新增中标" in event_types:
        business_keywords.append("项目中标")

    if business_keywords:
        lines.append("经营模式关键词：" + "、".join(business_keywords))

    return '\n'.join(lines)


def _extract_operation_capital(events: List[Dict[str, Any]], year_stats: List[Dict[str, Any]]) -> str:
    """经营与资本"""
    lines = ["### 经营与资本"]

    # 经营事件年度趋势
    if year_stats:
        sorted_stats = sorted(year_stats, key=lambda x: x.get('经营事件统计年份', ''))
        year_trends = []
        for stat in sorted_stats:
            year = stat.get('经营事件统计年份', '')
            count = stat.get('经营事件每年数量统计', 0)
            year_trends.append(f"{year}年{count}件")

        lines.append("经营事件年度趋势：" + "，".join(year_trends))

    # 资本运作事件类型
    capital_types = set()
    for event in events:
        event_type = event.get('经营事件类型名称', '')
        if event_type and ("债券" in event_type or "资本" in event_type):
            capital_types.add(event_type)

    if capital_types:
        lines.append("资本运作事件类型：" + "、".join(sorted(capital_types)))

    return '\n'.join(lines)


def _extract_value_growth(events: List[Dict[str, Any]]) -> str:
    """价值与成长"""
    lines = ["### 价值与成长"]

    # 市场拓展事件
    market_expansion = set()
    regions = ['重庆', '三亚', '舟山', '扬州', '天津', '浙江', '云南', '江西', '诸暨', '成都', '厦门']

    for event in events:
        event_type = event.get('经营事件类型名称', '')
        content = event.get('经营事件内容', '')

        if event_type in ['中标政府项目', '新增中标'] and content:
            for region in regions:
                if region in content:
                    market_expansion.add(region)

    if market_expansion:
        lines.append(f"市场拓展事件：{'、'.join(sorted(market_expansion))}等多地项目新增中标")

    return '\n'.join(lines)


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    events = data.get('经营事件信息', [])
    year_stats = data.get('按年份统计经营事件信息', [])
    total_count = data.get('经营事件总数量', 0)

    sections = ["# 企业经营动态提炼"]
    sections.append("")
    sections.append(f"经营事件总数量：{total_count}")

    # 企业历程
    history = _extract_enterprise_history(events)
    if history:
        sections.append("")
        sections.append(history)

    # 主营业务
    business = _extract_main_business(events)
    if business:
        sections.append("")
        sections.append(business)

    # 经营与资本
    capital = _extract_operation_capital(events, year_stats)
    if capital:
        sections.append("")
        sections.append(capital)

    # 价值与成长
    value = _extract_value_growth(events)
    if value:
        sections.append("")
        sections.append(value)

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业经营动态信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的企业经营动态信息
    """
    # 1. 调用 API
    response = _call_operations_api(entname)

    # API 返回的 code 是字符串
    if response.get('code') != '200':
        return "# 企业经营动态\n\n未查询到企业经营事件信息"

    # 2. 处理数据
    processed_data = _process_api_data(response)

    if not processed_data or not processed_data.get('经营事件信息'):
        return "# 企业经营动态\n\n暂无经营动态数据"

    # 3. 生成 Markdown
    return _format_markdown(processed_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s11_operations <企业名称>")
