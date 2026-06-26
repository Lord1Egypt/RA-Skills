#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
关联方信息一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from .base import call_api, debug_print


# ============ 映射关系 ============

RELATION_TYPE_MAPPING = {
    1: '投资关系',
    13: '公开披露',
    2: '任职关系'
}


# ============ 辅助函数 ============

def _map_islist(value: int) -> str:
    """映射是否上市状态"""
    return "上市" if value == 1 else "非上市"


def _format_percentage(value: Any) -> str:
    """格式化持股比例"""
    if value is None:
        return ""
    try:
        return f"{float(value) * 100}%"
    except (ValueError, TypeError):
        return str(value)


def _map_rel_type(value: int) -> str:
    """映射关系类型"""
    if value == 1:
        return "共同控制"
    elif value == 2:
        return "施加重大影响"
    return ""


def _safe_int_convert(value: Any) -> int:
    """安全地将值转换为整数"""
    if value is None or value == '':
        return 0
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0


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

            # 处理投资比例
            radio = ""
            if properties.get('holderrto'):
                radio = f"{properties['holderrto']}%"
            elif properties.get('conprop'):
                try:
                    conprop_value = float(properties['conprop'])
                    radio = f"{conprop_value * 100:.2f}%"
                except (ValueError, TypeError):
                    pass

            # 处理关系类型
            if link_type == 2 and properties.get('legal'):
                relation_type = "执行事务合伙人"
            else:
                relation_type = RELATION_TYPE_MAPPING.get(link_type, str(link_type))

            processed_links.append({
                '起始节点名称': id_to_name.get(from_id, from_id),
                '终止节点名称': id_to_name.get(to_id, to_id),
                '投资比例': radio,
                '关系类型': relation_type
            })

        return processed_links

    except Exception as e:
        debug_print(f"处理控制链路数据异常: {e}")
        return []


def _process_enterprise_info(items: Any, limit: int = 100, filter_layer: bool = True) -> List[Dict]:
    """处理企业信息的通用函数"""
    if not items:
        return []

    items_list = items[:limit] if isinstance(items, list) else [items]
    processed_items = []

    for enterprise in items_list:
        if not enterprise:
            continue

        if filter_layer:
            layer_value = _safe_int_convert(enterprise.get('layer'))
            if 'layer' in enterprise and layer_value != 1:
                continue

        processed_items.append({
            '企业名称': enterprise.get('entname', '').strip(),
            '是否上市': _map_islist(enterprise.get('islist', 0)),
            '严重违法数量': _safe_int_convert(enterprise.get('break_law_count')),
            '失信被执行人数量': _safe_int_convert(enterprise.get('punish_break_count')),
            '被执行人数量': _safe_int_convert(enterprise.get('punished_count')),
            '经营异常数量': _safe_int_convert(enterprise.get('abnormity_count')),
            '行政处罚数量': _safe_int_convert(enterprise.get('caseinfo_count')),
            '最终持股比例': _format_percentage(enterprise.get('final_cgzb')),
            '层级': _safe_int_convert(enterprise.get('layer'))
        })

    return processed_items


# ============ API 调用 ============

def _call_related_party_api(entname: str) -> Dict[str, Any]:
    """调用关联方信息 API"""
    response = call_api('/relation/related_party', {'entname': entname}, method='GET')
    return response


# ============ 数据处理 ============

def _process_related_party_data(response: Dict[str, Any]) -> Dict[str, Any]:
    """处理关联方数据"""
    if response.get('code') != 200:
        return {}

    result_data = response.get('result', {})
    if not result_data:
        return {}

    processed_result = {}

    # 1. 该企业的母公司
    if result_data.get('parent'):
        parent_data = result_data['parent']
        processed_result['该企业的母公司'] = _process_enterprise_info([parent_data], 100, filter_layer=False)

        # 母公司到该企业的路径
        if isinstance(parent_data, dict) and 'path' in parent_data and parent_data['path']:
            control_path = _process_control_path(parent_data['path'])
            processed_result['母公司到该企业的路径'] = control_path

    # 2. 该企业的子公司
    if result_data.get('member'):
        member_data = result_data['member']
        if isinstance(member_data, dict) and 'members' in member_data:
            processed_result['该企业的子公司'] = _process_enterprise_info(member_data['members'], 100, filter_layer=False)
        else:
            processed_result['该企业的子公司'] = _process_enterprise_info(member_data, 100, filter_layer=False)

    # 3. 与该企业受同一母公司控制的其他企业
    if result_data.get('parent_other_member'):
        processed_result['与该企业受同一母公司控制的其他企业'] = _process_enterprise_info(result_data['parent_other_member'], 100)

    # 4. 对该企业实施共同控制的投资方
    if result_data.get('common_shareholder'):
        processed_result['对该企业实施共同控制的投资方'] = _process_enterprise_info(result_data['common_shareholder'], 100)

    # 5. 对该企业施加重大影响的投资方
    if result_data.get('major_ent_inv'):
        processed_result['对该企业施加重大影响的投资方'] = _process_enterprise_info(result_data['major_ent_inv'], 100)

    # 6. 该企业的合营或联营企业
    if result_data.get('joint_venture_ent_inv'):
        processed_result['该企业的合营或联营企业'] = _process_enterprise_info(result_data['joint_venture_ent_inv'], 100)

    # 7. 该企业关键管理人员
    if result_data.get('staff_and_relation_person'):
        staff_items = []
        for item in result_data['staff_and_relation_person'][:100]:
            staff_items.append({
                '关键管理人员姓名': item.get('name', ''),
                '职位': item.get('position_desc', '')
            })
        processed_result['该企业关键管理人员'] = staff_items

    # 8. 该企业关键管理人员对外控制的企业
    if result_data.get('staff_out_ctrl'):
        staff_ctrl_items = []
        for item in result_data['staff_out_ctrl'][:100]:
            staff_ctrl_items.append({
                '关键管理人员姓名': item.get('name', ''),
                '关键管理人员职位': item.get('position_desc', ''),
                '企业名称': item.get('entname', ''),
                '是否上市': _map_islist(item.get('islist', 0)),
                '最终持股比例': _format_percentage(item.get('final_cgzb'))
            })
        processed_result['该企业关键管理人员对外控制的企业'] = staff_ctrl_items

    # 9. 该企业主要投资者个人
    if result_data.get('major_person_inv_and_relation_person'):
        major_person_items = []
        for item in result_data['major_person_inv_and_relation_person'][:100]:
            major_person_items.append({
                '主要投资者个人姓名': item.get('name', ''),
                '最终持股比例': _format_percentage(item.get('conprop'))
            })
        processed_result['该企业主要投资者个人'] = major_person_items

    # 10. 该企业最终控股股东
    if result_data.get('final_person_and_relation_person'):
        final_person_items = []
        for item in result_data['final_person_and_relation_person'][:100]:
            final_person_items.append({
                '最终控股股东名称': item.get('name', ''),
                '最终持股比例': _format_percentage(item.get('final_cgzb'))
            })
        processed_result['该企业最终控股股东'] = final_person_items

    # 11. 该企业最终控股自然人对外控制的企业
    if result_data.get('final_person_out_ctrl'):
        final_ctrl_items = []
        for item in result_data['final_person_out_ctrl'][:100]:
            final_ctrl_items.append({
                '企业名称': item.get('entname', ''),
                '实控人姓名': item.get('name', ''),
                '是否上市': _map_islist(item.get('islist', 0)),
                '最终持股比例': _format_percentage(item.get('final_cgzb'))
            })
        processed_result['该企业最终控股自然人对外控制的企业'] = final_ctrl_items

    # 统计结果
    def count_data(data):
        if not data:
            return 0
        return len(data) if isinstance(data, list) else 1

    def count_member_data(member_data):
        if not member_data:
            return 0
        if isinstance(member_data, dict) and 'members' in member_data:
            members = member_data['members']
            return len(members) if isinstance(members, list) else 1
        return len(member_data) if isinstance(member_data, list) else 1

    processed_result['统计结果'] = {
        '该企业子公司数量': count_member_data(result_data.get('member')),
        '与该企业受同一母公司控制的其他企业数量': count_data(result_data.get('parent_other_member')),
        '对该企业实施共同控制的投资方数量': count_data(result_data.get('common_shareholder')),
        '对该企业施加重大影响的投资方数量': count_data(result_data.get('major_ent_inv')),
        '该企业的合营或联营企业数量': count_data(result_data.get('joint_venture_ent_inv')),
        '该企业母公司关键管理人员数量': count_data(result_data.get('parent_staff_and_relation_person')),
        '该企业主要投资者个人数量': count_data(result_data.get('major_person_inv_and_relation_person')),
        '该企业主要投资者个人对外控制的企业数量': count_data(result_data.get('major_person_out_ctrl')),
        '该企业关键管理人员数量': count_data(result_data.get('staff_and_relation_person')),
        '该企业关键管理人员对外控制的企业数量': count_data(result_data.get('staff_out_ctrl')),
        '该企业最终控股自然人对外控制的企业数量': count_data(result_data.get('final_person_out_ctrl')),
    }

    return processed_result


# ============ Markdown 格式化 ============

def _extract_subsidiaries(data: Dict[str, Any]) -> str:
    """提取子公司信息"""
    stats = data.get('统计结果', {})
    subs = data.get('该企业的子公司', [])

    if not stats and not subs:
        return ""

    lines = ["### 子公司信息"]

    total = stats.get('该企业子公司数量', len(subs))
    lines.append(f"子公司总数：{total}")

    # 重要子公司（持股比例≥50%或上市）
    important_subs = []
    for sub in subs:
        ratio_str = sub.get('最终持股比例', '0%')
        try:
            ratio = float(ratio_str.rstrip('%'))
        except (ValueError, TypeError):
            ratio = 0

        is_listed = sub.get('是否上市', '非上市')

        if ratio >= 50:
            name = sub.get('企业名称', '')
            important_subs.append(f"{name}、{is_listed}、{ratio_str}")
            if len(important_subs) >= 3:
                break

    if important_subs:
        lines.append(f"重要子公司（持股比例≥50%）：{'；'.join(important_subs)}")

    return '\n'.join(lines)


def _extract_key_management(data: Dict[str, Any]) -> str:
    """提取关键管理人员"""
    stats = data.get('统计结果', {})
    mgmt = data.get('该企业关键管理人员', [])

    if not mgmt:
        return ""

    lines = ["### 关键管理人员"]

    total = stats.get('该企业关键管理人员数量', len(mgmt))
    lines.append(f"关键管理人员数量：{total}")

    mgmt_list = []
    for person in mgmt[:3]:
        name = person.get('关键管理人员姓名', '')
        positions = person.get('职位', [])
        if isinstance(positions, list) and positions:
            position = positions[0]
        else:
            position = str(positions) if positions else ''

        if name:
            mgmt_list.append(f"{name}、{position}")

    if mgmt_list:
        lines.append(f"名单与职位：{'；'.join(mgmt_list)}")

    return '\n'.join(lines)


def _extract_other_statistics(data: Dict[str, Any]) -> str:
    """提取其他关联方统计"""
    stats = data.get('统计结果', {})

    if not stats:
        return ""

    lines = ["### 其他关联方统计"]

    stat_items = []

    if stats.get('对该企业施加重大影响的投资方数量'):
        stat_items.append(f"重大影响投资方数量：{stats.get('对该企业施加重大影响的投资方数量')}")

    stat_items.append(f"实控人对外控制企业数量：{stats.get('该企业最终控股自然人对外控制的企业数量', 0)}")

    if stats.get('对该企业实施共同控制的投资方数量'):
        stat_items.append(f"共同控制投资方数量：{stats.get('对该企业实施共同控制的投资方数量')}")

    if stats.get('该企业的合营或联营企业数量'):
        stat_items.append(f"合营/联营企业数量：{stats.get('该企业的合营或联营企业数量')}")

    if stats.get('该企业关键管理人员对外控制的企业数量'):
        stat_items.append(f"关键管理人员对外控制企业数量：{stats.get('该企业关键管理人员对外控制的企业数量')}")

    if stats.get('该企业主要投资者个人数量'):
        stat_items.append(f"主要投资者个人数量：{stats.get('该企业主要投资者个人数量')}")

    if stats.get('与该企业受同一母公司控制的其他企业数量'):
        stat_items.append(f"同一母公司控制的其他企业数量：{stats.get('与该企业受同一母公司控制的其他企业数量')}")

    if stat_items:
        lines.extend(stat_items)

    return '\n'.join(lines)


def _format_markdown(data: Dict[str, Any]) -> str:
    """将关联方数据转换为 Markdown 格式"""
    sections = ["# 关联方信息提炼"]

    # 子公司信息
    subs = _extract_subsidiaries(data)
    if subs:
        sections.append("")
        sections.append(subs)

    # 关键管理人员
    mgmt = _extract_key_management(data)
    if mgmt:
        sections.append("")
        sections.append(mgmt)

    # 其他统计
    stats = _extract_other_statistics(data)
    if stats:
        sections.append("")
        sections.append(stats)

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业关联方信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的关联方信息
    """
    # 1. 调用 API
    response = _call_related_party_api(entname)

    if response.get('code') != 200:
        return "# 关联方信息\n\n未查询到关联方信息"

    # 2. 处理数据
    data = _process_related_party_data(response)

    if not data:
        return "# 关联方信息\n\n暂无关联方数据"

    # 3. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s09_related_parties <企业名称>")
