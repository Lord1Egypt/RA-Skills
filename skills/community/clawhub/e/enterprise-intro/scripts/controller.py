#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
实际控制人一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List, Optional
from .base import call_api, debug_print


# ============ 映射表 ============

# 疑似实控人判断规则映射
DISTINGUISH_MAP = {
    1: "公开披露", "1": "公开披露",
    2: "决策权最大", "2": "决策权最大",
    3: "表决权最大", "3": "表决权最大"
}

# 疑似实控人类型映射
CONTROLLER_TYPE_MAP = {
    2: "自然人", "2": "自然人",
    3: "境外企业", "3": "境外企业",
    4: "组织机构", "4": "组织机构",
    5: "其他社会组织", "5": "其他社会组织"
}


# ============ API 调用 ============

def _call_entinfo_api(entname: str) -> Dict[str, Any]:
    """调用企业基本信息 API（用于获取总公司信息）"""
    response = call_api('/entinfo', {'name': entname}, method='GET')
    return response


def _call_controller_api(entname: str) -> Dict[str, Any]:
    """调用实际控制人 API"""
    response = call_api('/actual_control_info', {'entname': entname}, method='POST')
    return response


# ============ 数据处理 ============

def _format_controller_result(data: Dict[str, Any]) -> Dict[str, Any]:
    """格式化实控人返回结果"""
    if not data or 'result' not in data:
        return {}

    result = data.get('result', [])
    if not result:
        return {}

    formatted_results = []

    for item in result:
        formatted_item = {}

        # 疑似实控人判断规则
        distinguish = item.get('distinguish')
        if distinguish is not None and distinguish in DISTINGUISH_MAP:
            formatted_item['疑似实控人判断规则'] = DISTINGUISH_MAP[distinguish]

        # 疑似实控人名称
        if item.get('controller_name'):
            formatted_item['疑似实控人名称'] = item.get('controller_name')

        # 疑似实控人类型
        controller_type = item.get('controller_type')
        if controller_type is not None and controller_type != '' and controller_type in CONTROLLER_TYPE_MAP:
            formatted_item['疑似实控人类型'] = CONTROLLER_TYPE_MAP[controller_type]

        # 决策权系数 - 乘以100加%
        control_power = item.get('control_power')
        if control_power is not None:
            try:
                percentage = float(control_power) * 100
                value = f"{percentage:.4f}%".rstrip('0').rstrip('.')
                if not value.endswith('%'):
                    value += '%'
                formatted_item['决策权系数'] = value
            except (ValueError, TypeError):
                formatted_item['决策权系数'] = str(control_power)

        # 控制路径
        if item.get('txt_path'):
            formatted_item['控制路径'] = item.get('txt_path')

        # 控制层级
        if item.get('layer'):
            formatted_item['控制层级'] = item.get('layer')

        formatted_results.append(formatted_item)

    return {"疑似实控人信息": formatted_results}


def _fetch_controller_data(entname: str) -> Dict[str, Any]:
    """
    获取实控人数据，支持分公司查询
    如果是分公司，会先获取总公司信息再查询实控人
    """
    # 先查询企业基本信息，检查是否是分公司
    ent_response = _call_entinfo_api(entname)

    if ent_response.get('CODE') == 404:
        debug_print("没有基础信息")
        return {}

    # 检查是否有总公司信息
    headquarters = None
    try:
        headquarters = ent_response.get('ENT_INFO', {}).get('HEADQUARTERS', {})
    except (AttributeError, TypeError):
        pass

    # 如果是分公司，使用总公司的名称查询
    if headquarters and len(headquarters) > 0:
        hq_name = headquarters.get('ENTNAME', '')
        if hq_name:
            debug_print(f"检测到分公司，使用总公司 {hq_name} 查询实控人")
            response = _call_controller_api(hq_name)
        else:
            response = _call_controller_api(entname)
    else:
        response = _call_controller_api(entname)

    # 检查响应
    code = response.get('code', 0)
    if code != 200:
        return {}

    return _format_controller_result(response)


# ============ Markdown 格式化 ============

def _format_markdown(data: Dict[str, Any]) -> str:
    """将实控人数据转换为 Markdown 格式"""
    controller_list = data.get('疑似实控人信息', [])

    if not controller_list:
        return "# 实际控制人\n\n暂无实际控制人数据"

    lines = ["# 实际控制人"]

    # 取第一个实控人信息
    controller = controller_list[0] if controller_list else {}

    if controller.get('疑似实控人判断规则'):
        lines.append(f"判断结果：{controller.get('疑似实控人判断规则')}")

    if controller.get('疑似实控人名称'):
        lines.append(f"实控人名称：{controller.get('疑似实控人名称')}")

    if controller.get('疑似实控人类型'):
        lines.append(f"实控人类型：{controller.get('疑似实控人类型')}")

    if controller.get('决策权系数'):
        lines.append(f"决策权系数：{controller.get('决策权系数')}")

    if controller.get('控制层级'):
        lines.append(f"控制层级：{controller.get('控制层级')}")

    if controller.get('控制路径'):
        lines.append(f"控制路径：{controller.get('控制路径')}")

    # 如果有多个实控人，显示其他实控人
    if len(controller_list) > 1:
        lines.append("")
        lines.append("### 其他疑似实控人")
        for i, ctrl in enumerate(controller_list[1:], 2):
            name = ctrl.get('疑似实控人名称', f'实控人{i}')
            ctrl_type = ctrl.get('疑似实控人类型', '')
            power = ctrl.get('决策权系数', '')
            info_parts = [name]
            if ctrl_type:
                info_parts.append(f"类型：{ctrl_type}")
            if power:
                info_parts.append(f"决策权系数：{power}")
            lines.append(f"- {', '.join(info_parts)}")

    return '\n'.join(lines)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业实际控制人信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的实际控制人信息
    """
    # 1. 获取数据
    data = _fetch_controller_data(entname)

    if not data:
        return "# 实际控制人\n\n未查询到实控人信息"

    # 2. 生成 Markdown
    return _format_markdown(data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s08_controller <企业名称>")
