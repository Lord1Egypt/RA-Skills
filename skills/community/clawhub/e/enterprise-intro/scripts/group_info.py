#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
集团信息一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from collections import Counter
from .base import call_api, debug_print


# ============ 映射表 ============

FIELD_NAME_MAPPING = {
    'entname': '企业名称',
    'regcap': '注册资本(万)',
    'regcapcur_desc': '注册资本币种',
    'province_desc': '省份',
    'esdate': '成立日期',
    'final_cgzb': '最终持股比例',
    'layer': '层级',
    'islist': '是否上市',
    'path': '母公司到查询企业的控制链路',
    'from': '起始节点名称',
    'to': '终止节点名称',
    'radio': '投资比例',
    'type': '关系类型',
}

RELATION_TYPE_MAPPING = {
    1: '投资关系',
    13: '公开披露',
    2: '任职关系'
}

MODULE_NAME_MAPPING = {
    'parent': '母公司',
    'members': '子公司',
}


# ============ 辅助函数 ============

def _format_percentage(value: Any) -> str:
    """格式化百分比字段"""
    if value is None or value == '':
        return ""
    try:
        if isinstance(value, str):
            value = float(value)
        return f"{value * 100:.2f}%"
    except (ValueError, TypeError):
        return ""


def _format_islist(value: Any) -> str:
    """格式化上市状态"""
    if value == 1 or value == '1':
        return "上市"
    elif value == 0 or value == '0':
        return "非上市"
    return str(value) if value else ""


def _sort_members(members_list: List[Dict]) -> List[Dict]:
    """对子公司进行排序：层级升序 > 注册资本降序 > 企业名称升序"""
    return sorted(
        members_list,
        key=lambda x: (
            x.get('layer', float('inf')),
            -float(x.get('regcap', 0) or 0),
            x.get('entname', '')
        )
    )


def _process_control_path(path_data: Dict) -> List[Dict]:
    """处理控制链路数据"""
    if not path_data:
        return []

    try:
        nodes = path_data.get('nodes', [])
        links = path_data.get('links', [])

        id_to_name = {node.get('id'): node.get('name') for node in nodes}

        processed_links = []
        for link in links:
            link_type = link.get('type')
            properties = link.get('properties', {})

            if link_type == 2 and not properties.get('legal'):
                continue

            from_id = link.get('from')
            to_id = link.get('to')

            radio = ""
            if properties.get('holderrto'):
                radio = f"{properties['holderrto']}%"
            elif properties.get('conprop'):
                try:
                    conprop_value = float(properties['conprop'])
                    radio = f"{conprop_value * 100:.2f}%"
                except (ValueError, TypeError):
                    pass

            if link_type == 2 and properties.get('legal'):
                relation_type = "执行事务合伙人"
            else:
                relation_type = RELATION_TYPE_MAPPING.get(link_type, str(link_type))

            processed_link = {
                'from': id_to_name.get(from_id, from_id),
                'to': id_to_name.get(to_id, to_id),
                'radio': radio,
                'type': relation_type
            }
            processed_links.append(processed_link)

        return processed_links

    except Exception:
        return []


def _format_enterprise_info(enterprise_list: List[Dict], limit: int = 100) -> List[Dict]:
    """格式化企业信息列表"""
    if not enterprise_list or not isinstance(enterprise_list, list):
        return []

    if limit and len(enterprise_list) > limit:
        enterprise_list = enterprise_list[:limit]

    formatted_list = []
    for enterprise in enterprise_list:
        if not isinstance(enterprise, dict):
            continue

        formatted_enterprise = {
            '企业名称': enterprise.get('entname'),
            '注册资本(万)': enterprise.get('regcap'),
            '注册资本币种': enterprise.get('regcapcur_desc'),
            '是否上市': _format_islist(enterprise.get('islist')),
            '省份': enterprise.get('province_desc'),
            '成立日期': enterprise.get('esdate'),
        }

        if 'layer' in enterprise:
            formatted_enterprise['层级'] = enterprise.get('layer')
        if 'final_cgzb' in enterprise:
            formatted_enterprise['最终持股比例'] = _format_percentage(enterprise.get('final_cgzb'))

        formatted_list.append(formatted_enterprise)

    return formatted_list


# ============ API 调用 ============

def _call_entinfo_api(entname: str) -> Dict[str, Any]:
    """调用企业基本信息 API（检查是否分公司）"""
    response = call_api('/entinfo', {'name': entname}, method='GET')
    return response


def _call_parent_identification_api(entname: str) -> Dict[str, Any]:
    """调用集团母公司识别 API"""
    response = call_api('/relation/parent_company_identification', {'entname': entname}, method='GET')
    return response


def _call_parent_member_api(entname: str) -> Dict[str, Any]:
    """调用集团成员识别 API"""
    response = call_api('/relation/parent_company_member', {'entname': entname}, method='GET')
    return response


# ============ 数据处理 ============

def _fetch_group_data(entname: str) -> Optional[Dict[str, Any]]:
    """获取集团数据"""
    # 先判断是否为分公司
    fen_out = _call_entinfo_api(entname)

    if fen_out.get('CODE') == 404:
        return None

    query_entname = entname
    try:
        test_fen = fen_out.get('ENT_INFO', {}).get('HEADQUARTERS', {})
        if test_fen and len(test_fen) > 0:
            entname_c = test_fen.get('ENTNAME', '')
            if entname_c:
                query_entname = entname_c
    except Exception:
        pass

    # 调用集团母公司识别接口
    parent_company_result = _call_parent_identification_api(query_entname)

    if parent_company_result.get('code') == 404:
        return None

    if parent_company_result.get('code') != 200:
        return None

    parent_info = parent_company_result.get('result', {}).get('parent', {})
    if not parent_info:
        return None

    # 调用集团成员识别接口
    parent_entname = parent_info.get('entname')
    if not parent_entname:
        return None

    member_result = _call_parent_member_api(parent_entname)

    if not member_result or member_result.get('code') != 200:
        return None

    # 格式化输出数据
    result_data = {}

    # 格式化母公司信息
    formatted_parent = {
        '企业名称': parent_info.get('entname'),
        '注册资本(万)': parent_info.get('regcap'),
        '注册资本币种': parent_info.get('regcapcur_desc'),
        '省份': parent_info.get('province_desc'),
        '成立日期': parent_info.get('esdate'),
        '最终持股比例': _format_percentage(parent_info.get('final_cgzb')),
        '层级': parent_info.get('layer')
    }

    if parent_info.get('path'):
        formatted_parent['控制链路'] = _process_control_path(parent_info.get('path'))

    result_data['母公司'] = formatted_parent

    # 获取成员信息
    members_data = {}
    if isinstance(member_result, dict):
        result_section = member_result.get('result', {})
        if isinstance(result_section, dict):
            members_data = result_section.get('members', {})
            if isinstance(members_data, list):
                members_data = {'members': members_data}

    # 格式化子公司信息
    if isinstance(members_data, dict):
        raw_members = members_data.get('members', [])
        sorted_members = _sort_members(raw_members)
        limited_sorted_members = sorted_members[:100]
        result_data['子公司'] = _format_enterprise_info(limited_sorted_members, limit=None)
    else:
        result_data['子公司'] = []

    return result_data


# ============ Markdown 格式化 ============

def _extract_business_fields(subsidiaries: List[Dict]) -> str:
    """从子公司名称中提取业务领域关键词"""
    field_keywords = {
        '金融租赁': 0,
        '金融资产投资': 0,
        '理财': 0,
        '人寿保险': 0,
        '村镇银行': 0,
        '资产管理': 0,
        '媒体': 0
    }

    for sub in subsidiaries:
        name = sub.get('企业名称', '')
        if '金融租赁' in name or '租赁' in name:
            field_keywords['金融租赁'] += 1
        if '金融资产投资' in name or '资产投资' in name:
            field_keywords['金融资产投资'] += 1
        if '理财' in name:
            field_keywords['理财'] += 1
        if '人寿保险' in name or '保险' in name:
            field_keywords['人寿保险'] += 1
        if '村镇银行' in name:
            field_keywords['村镇银行'] += 1
        if '资产管理' in name or '资本管理' in name:
            field_keywords['资产管理'] += 1
        if '杂志' in name or '媒体' in name or '传媒' in name:
            field_keywords['媒体'] += 1

    result = [field for field, count in field_keywords.items() if count > 0]
    return '、'.join(result)


def _extract_parent_company_info(parent_company: Dict[str, Any], subsidiaries: List[Dict]) -> str:
    """提取目标企业作为集团母公司的信息"""
    parts = []

    company_name = parent_company.get('企业名称', '')
    level = parent_company.get('层级', 0)
    capital = parent_company.get('注册资本(万)', '')
    currency = parent_company.get('注册资本币种', '')
    establish_date = parent_company.get('成立日期', '')

    if establish_date and '-' in establish_date:
        parts_date = establish_date.split('-')
        if len(parts_date) == 3:
            establish_date = f"{parts_date[0]}年{parts_date[1]}月{parts_date[2]}日"

    province = parent_company.get('省份', '')

    parts.append(f"{company_name}自身为集团母公司，层级为{level}，注册资本{capital}万{currency}，成立于{establish_date}，位于{province}。")
    parts.append("该集团架构模式为产业核心模式，母公司作为产业链核心角色，通过直接或间接持股控制子公司。")

    business_fields = _extract_business_fields(subsidiaries)
    if business_fields:
        parts.append(f"整体业务领域涵盖{business_fields}等。")

    level1_subs = [sub for sub in subsidiaries if sub.get('层级') == 1]
    level2_subs = [sub for sub in subsidiaries if sub.get('层级') == 2]

    board_parts = []
    if level1_subs:
        level1_sorted = sorted(level1_subs, key=lambda x: float(x.get('注册资本(万)', 0) or 0), reverse=True)[:4]
        level1_desc = []
        for sub in level1_sorted:
            sub_name = sub.get('企业名称', '')
            sub_capital = sub.get('注册资本(万)', '')
            sub_currency = sub.get('注册资本币种', '')
            sub_ratio = sub.get('最终持股比例', '')
            if sub_ratio and '.' in sub_ratio:
                try:
                    ratio_num = float(sub_ratio.replace('%', ''))
                    if ratio_num == int(ratio_num):
                        sub_ratio = f"{int(ratio_num)}%"
                except Exception:
                    pass
            level1_desc.append(f"{sub_name}（注册资本{sub_capital}万{sub_currency}，{sub_ratio}持股）")
        board_parts.append(f"一级子公司包括{'、'.join(level1_desc)}等")

    if level2_subs:
        level2_names = [sub.get('企业名称', '') for sub in level2_subs[:3]]
        level2_field_flags = {'租赁': False, '资产管理': False}
        for sub in level2_subs[:10]:
            name = sub.get('企业名称', '')
            if '租赁' in name:
                level2_field_flags['租赁'] = True
            if '资本' in name or '投资' in name or '资产管理' in name:
                level2_field_flags['资产管理'] = True
        level2_fields = [field for field, exists in level2_field_flags.items() if exists]
        fields_str = '、'.join(level2_fields) if level2_fields else '多个'
        board_parts.append(f"二级子公司包括{'、'.join(level2_names)}等，涉及{fields_str}等细分领域")

    if board_parts:
        parts.append(f"业务板块构成中，{'，'.join(board_parts)}。")

    province_counter = Counter([sub.get('省份', '') for sub in subsidiaries if sub.get('省份')])
    if province_counter:
        all_provinces = [prov for prov, _ in province_counter.most_common()]
        top_provinces = [prov for prov, _ in province_counter.most_common(3)]
        parts.append(f"行业地区分布方面，子公司分布在{'、'.join(all_provinces)}等多个省份，其中{'、'.join(top_provinces)}等地子公司数量相对较多。")

    total_subs = len(subsidiaries)
    parts.append(f"集团成员中，子公司数量为{total_subs}家。")

    return ''.join(parts)


def _extract_member_company_info(parent_company: Dict[str, Any], subsidiaries: List[Dict]) -> str:
    """提取目标企业作为集团成员的信息"""
    parts = []

    company_name = parent_company.get('企业名称', '')
    capital = parent_company.get('注册资本(万)', '')
    currency = parent_company.get('注册资本币种', '')
    establish_date = parent_company.get('成立日期', '')
    province = parent_company.get('省份', '')

    parts.append(f"目标企业为集团成员企业。集团母公司：{company_name}（成立于{establish_date}，注册资本{capital}万元{currency}，位于{province}）。")

    return ''.join(parts)


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    parent_company = data.get('母公司', {})
    subsidiaries = data.get('子公司', [])

    is_parent = parent_company.get('层级', -1) == 0

    sections = ["# 集团信息提炼"]

    if is_parent:
        result = _extract_parent_company_info(parent_company, subsidiaries)
    else:
        result = _extract_member_company_info(parent_company, subsidiaries)

    sections.append("")
    sections.append(result)

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业集团信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的集团信息
    """
    # 1. 获取集团数据
    data = _fetch_group_data(entname)

    if not data:
        return "# 集团信息\n\n该企业不属于集团客户或暂无集团信息数据"

    # 2. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s15_group_info <企业名称>")
