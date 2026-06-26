#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
客户/供应商一体化脚本
整合 API 调用和数据后处理
"""

from typing import Dict, Any, List
from .base import call_api, debug_print


# ============ 映射表 ============

MODULE_MAPPING = {
    'supplier_page': '供应商统计信息',
    'cust_page': '客户统计信息',
    'year_supplier_count': '按年份统计供应商信息',
    'supplier_qual_count': '供应商属性统计信息',
    'year_cust_count': '按年份统计客户信息',
    'merchant_qual_count': '客户属性统计信息',
    'supplier_list': '供应商信息',
    'cust_list': '客户信息'
}

FIELD_MAPPING = {
    'totalcount': '总数',
    'year': '年份',
    'amount': '合作金额（万元）',
    'relation_date': '关联日期',
    'earliest_date': '最早合作日期',
    'source': '来源',
    'coop_count': '合作次数',
    'tprop': '占总额比例',
    'max_coop_duration': '最长合作时长（年）',
    'year_supplier_amount': '按年份统计供应商合作金额（万元）',
    'year_cust_amount': '按年份统计客户合作金额（万元）',
    'supplier_name': '供应商名称',
    'supplier_type': '供应商类型',
    'supplier_num': '不同类型下供应商数量',
    'explain': '说明',
    'source_desc': '数据来源描述',
    'relation_year': '合作年份',
    'cust_name': '客户名称',
    'customer_type': '客户类型',
    'customer_num': '不同类型下客户数量',
    'main_purchased_products': '销售给该客户的主要产品'
}


# ============ 辅助函数 ============

def _format_percentage(value: Any) -> str:
    """格式化百分比值"""
    if value is None:
        return ''

    if isinstance(value, str) and value.strip() == '':
        return ''

    try:
        if isinstance(value, (int, float)):
            if value == int(value):
                return f"{int(value)}%"
            else:
                formatted = f"{value:.2f}".rstrip('0').rstrip('.')
                return f"{formatted}%"
        elif isinstance(value, str):
            if not value.endswith('%'):
                num_value = float(value)
                if num_value == int(num_value):
                    return f"{int(num_value)}%"
                else:
                    formatted = f"{num_value:.2f}".rstrip('0').rstrip('.')
                    return f"{formatted}%"
            return value
    except (ValueError, TypeError):
        return str(value) if value else ''

    return str(value)


def _map_fields_to_chinese(obj: Any, parent_key: str = '', is_in_array: bool = False) -> Any:
    """递归地将数据结构中的英文字段名映射为中文字段名"""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if key in MODULE_MAPPING and not is_in_array:
                chinese_key = MODULE_MAPPING[key]
            elif key in FIELD_MAPPING:
                chinese_key = FIELD_MAPPING[key]
                if key == 'totalcount':
                    if parent_key == 'supplier_page' or 'supplier' in parent_key:
                        chinese_key = '供应商总数'
                    elif parent_key == 'cust_page' or 'cust' in parent_key:
                        chinese_key = '客户总数'
            else:
                chinese_key = key

            result[chinese_key] = _map_fields_to_chinese(value, key, False)
        return result
    elif isinstance(obj, list):
        return [_map_fields_to_chinese(item, parent_key, True) for item in obj]
    else:
        return obj


def _process_supplier_type_values(obj: Any) -> Any:
    """处理供应商类型值的转换，将"公开发债企业"改为"发债企业"""
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            if key in ['供应商类型', 'supplier_type', '客户类型']:
                if isinstance(value, list):
                    result[key] = ['发债企业' if item == '公开发债企业' else item for item in value]
                elif value == '公开发债企业':
                    result[key] = '发债企业'
                else:
                    result[key] = value
            else:
                result[key] = _process_supplier_type_values(value)
        return result
    elif isinstance(obj, list):
        return [_process_supplier_type_values(item) for item in obj]
    else:
        return obj


# ============ API 调用 ============

def _call_customer_supplier_api(entname: str) -> Dict[str, Any]:
    """调用客户供应商 API"""
    response = call_api('/customerSupplierRelation', {'entname': entname}, method='GET')
    return response


# ============ 数据处理 ============

def _process_api_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """处理 API 返回的数据"""
    if not isinstance(data, dict):
        return {}

    pagination_fields = ['page', 'size', 'totalpage']
    filtered_fields = ['supplier_entname', 'cust_entname', 'frname', 'entitytype', 'source_id', 'entstatus', 'enttype']
    processed_data = {}

    # 处理供应商列表
    if 'supplier_list' in data and isinstance(data['supplier_list'], list):
        supplier_list = data['supplier_list'][:100]
        for supplier in supplier_list:
            if isinstance(supplier, dict):
                for field in filtered_fields:
                    supplier.pop(field, None)
                if 'tprop' in supplier:
                    supplier['tprop'] = _format_percentage(supplier['tprop'])
        processed_data['supplier_list'] = supplier_list

    # 处理客户列表
    if 'cust_list' in data and isinstance(data['cust_list'], list):
        cust_list = data['cust_list'][:100]
        for customer in cust_list:
            if isinstance(customer, dict):
                for field in filtered_fields:
                    customer.pop(field, None)
                if 'tprop' in customer:
                    customer['tprop'] = _format_percentage(customer['tprop'])
        processed_data['cust_list'] = cust_list

    # 保留其他数据
    for key in data:
        if key not in ['supplier_list', 'cust_list']:
            if key in ['supplier_page', 'cust_page'] and isinstance(data[key], dict):
                filtered_data = {k: v for k, v in data[key].items() if k not in pagination_fields}
                processed_data[key] = filtered_data
            else:
                processed_data[key] = data[key]

    # 映射字段名为中文
    chinese_data = _map_fields_to_chinese(processed_data)
    final_data = _process_supplier_type_values(chinese_data)

    return final_data


# ============ Markdown 格式化 ============

def _extract_supplier_stats(data: Dict[str, Any]) -> List[str]:
    """提取供应商统计信息"""
    lines = []

    supplier_stats = data.get('供应商统计信息', {})
    if supplier_stats:
        total = supplier_stats.get('供应商总数', 0)
        lines.append("### 供应商统计摘要")
        lines.append(f"供应商总数：{total}")

    year_stats = data.get('按年份统计供应商信息', [])
    if year_stats:
        lines.append("")
        lines.append("### 按年份统计供应商")
        for item in year_stats:
            year = item.get('年份', '')
            count = item.get('按年份统计供应商数量', 0)
            amount = item.get('按年份统计供应商合作金额（万元）', 0)
            lines.append(f"- 年份: {year}, 当年供应商数量: {count}, 当年合作金额（万元）: {amount}")

    type_stats = data.get('供应商属性统计信息', [])
    if type_stats:
        lines.append("")
        lines.append("### 供应商类型分布")
        for item in type_stats:
            supplier_type = item.get('供应商类型', '')
            count = item.get('不同类型下供应商数量', 0)
            duration = item.get('最长合作时长（年）', 0)
            lines.append(f"- 供应商类型: {supplier_type}, 该类型供应商数量: {count}, 最长合作时长（年）: {duration}")

    return lines


def _extract_customer_stats(data: Dict[str, Any]) -> List[str]:
    """提取客户统计信息"""
    lines = []

    customer_stats = data.get('客户统计信息', {})
    if customer_stats:
        total = customer_stats.get('客户总数', 0)
        lines.append("### 客户统计摘要")
        lines.append(f"客户总数：{total}")

    year_stats = data.get('按年份统计客户信息', [])
    if year_stats:
        lines.append("")
        lines.append("### 按年份统计客户")
        for item in year_stats:
            year = item.get('年份', '')
            count = item.get('按年份统计客户数量', 0)
            amount = item.get('按年份统计客户合作金额（万元）', 0)
            lines.append(f"- 年份: {year}, 当年客户数量: {count}, 当年合作金额（万元）: {amount}")

    type_stats = data.get('客户属性统计信息', [])
    if type_stats:
        lines.append("")
        lines.append("### 客户类型分布")
        for item in type_stats:
            customer_type = item.get('客户类型', '')
            count = item.get('不同类型下客户数量', 0)
            duration = item.get('最长合作时长（年）', 0)
            lines.append(f"- 客户类型: {customer_type}, 该类型客户数量: {count}, 最长合作时长（年）: {duration}")

    return lines


def _extract_main_suppliers(data: Dict[str, Any]) -> List[str]:
    """提取主要供应商列表"""
    lines = []
    suppliers = data.get('供应商信息', [])

    if suppliers:
        lines.append("### 主要供应商列表")
        for supplier in suppliers[:20]:
            name = supplier.get('供应商名称', '')
            recent_date = supplier.get('关联日期', '')
            amount = supplier.get('合作金额（万元）', 0)
            count = supplier.get('合作次数', 0)
            earliest_date = supplier.get('最早合作日期', '')
            source = supplier.get('来源', '')

            supplier_types = supplier.get('供应商类型', [])
            type_str = ', '.join(supplier_types) if isinstance(supplier_types, list) else str(supplier_types or '')

            parts = [f"供应商名称: {name}"]
            if type_str:
                parts.append(f"类型: {type_str}")
            parts.append(f"最近合作日期: {recent_date}")
            parts.append(f"合作金额（万元）: {amount}")
            parts.append(f"合作次数: {count}")
            parts.append(f"最早合作日期: {earliest_date}")
            parts.append(f"数据来源: {source}")

            lines.append(f"- {', '.join(parts)}")

    return lines


def _extract_main_customers(data: Dict[str, Any]) -> List[str]:
    """提取主要客户列表"""
    lines = []
    customers = data.get('客户信息', [])

    if customers:
        lines.append("### 主要客户列表")
        for customer in customers[:20]:
            name = customer.get('客户名称', '')
            recent_date = customer.get('关联日期', '')
            amount = customer.get('合作金额（万元）', 0)
            count = customer.get('合作次数', 0)
            earliest_date = customer.get('最早合作日期', '')
            source = customer.get('来源', '')

            customer_types = customer.get('客户类型', [])
            type_str = ', '.join(customer_types) if isinstance(customer_types, list) else str(customer_types or '')

            products = customer.get('销售给该客户的主要产品', [])
            product_str = ', '.join(products[:10]) if isinstance(products, list) else str(products or '')

            parts = [f"客户名称: {name}"]
            if type_str:
                parts.append(f"类型: {type_str}")
            parts.append(f"最近合作日期: {recent_date}")
            parts.append(f"合作金额（万元）: {amount}")
            parts.append(f"合作次数: {count}")
            if product_str:
                parts.append(f"主要销售产品: {product_str}")
            parts.append(f"最早合作日期: {earliest_date}")
            parts.append(f"数据来源: {source}")

            lines.append(f"- {', '.join(parts)}")

    return lines


def _format_markdown(data: Dict[str, Any]) -> str:
    """将数据转换为 Markdown 格式"""
    sections = ["# 客户/供应商信息提炼"]
    sections.append("")
    sections.append("### 数据说明")
    sections.append("本数据仅源自企业外部公开交易活动（如招投标、公开披露等），不代表企业客户/供应商全貌，请谨慎评估单一合作伙伴重要性。")

    supplier_stats = _extract_supplier_stats(data)
    if supplier_stats:
        sections.append("")
        sections.extend(supplier_stats)

    customer_stats = _extract_customer_stats(data)
    if customer_stats:
        sections.append("")
        sections.extend(customer_stats)

    suppliers = _extract_main_suppliers(data)
    if suppliers:
        sections.append("")
        sections.extend(suppliers)

    customers = _extract_main_customers(data)
    if customers:
        sections.append("")
        sections.extend(customers)

    return '\n'.join(sections)


# ============ 主函数 ============

def fetch(entname: str) -> str:
    """
    获取并处理企业客户供应商信息

    Args:
        entname: 企业名称

    Returns:
        Markdown 格式的客户供应商信息
    """
    # 1. 调用 API
    response = _call_customer_supplier_api(entname)

    if response.get('code') != 200:
        return "# 客户/供应商信息\n\n未查询到客户供应商信息"

    # 2. 处理数据
    data = response.get('data', {})
    if not data:
        return "# 客户/供应商信息\n\n暂无客户供应商数据"

    processed_data = _process_api_data(data)

    # 3. 生成 Markdown
    return _format_markdown(processed_data)


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        print(fetch(sys.argv[1]))
    else:
        print("用法: python -m scripts.s10_customers <企业名称>")
