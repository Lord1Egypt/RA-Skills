#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业简介 Skill Scripts 统一入口

提供21个一体化脚本的统一访问接口
每个脚本都有统一的 fetch(entname: str) -> str 接口
"""

from .entity_info import fetch as fetch_entity_info
from .listed_info import fetch as fetch_listed_info
from .financial_info import fetch as fetch_financial_info
from .debt_financing import fetch as fetch_debt_financing
from .risk_data import fetch as fetch_risk_data
from .sentiment import fetch as fetch_sentiment
from .controller import fetch as fetch_controller
from .related_parties import fetch as fetch_related_parties
from .customers import fetch as fetch_customers
from .operations import fetch as fetch_operations
from .investment import fetch as fetch_investment
from .history import fetch as fetch_history
from .bidding import fetch as fetch_bidding
from .group_info import fetch as fetch_group_info
from .portrait import fetch as fetch_portrait
from .ip import fetch as fetch_ip
from .innovation import fetch as fetch_innovation
from .shell_company import fetch as fetch_shell_company
from .risk_assessment import fetch as fetch_risk_assessment
from .investment_query import fetch as fetch_investment_query


# 脚本映射表
SCRIPTS = {
    'entity_info': fetch_entity_info,           # 01 主体信息
    'listed_info': fetch_listed_info,           # 02 上市信息
    'financial_info': fetch_financial_info,     # 03 财务信息
    'debt_financing': fetch_debt_financing,     # 04 债权融资
    'risk_data': fetch_risk_data,               # 05 风险大数据
    'sentiment': fetch_sentiment,               # 06 舆情信息
    'controller': fetch_controller,             # 08 实际控制人
    'related_parties': fetch_related_parties,   # 09 关联方信息
    'customers': fetch_customers,               # 10 客户/供应商
    'operations': fetch_operations,             # 11 企业经营动态
    'investment': fetch_investment,             # 12 投融资事件
    'history': fetch_history,                   # 13 历史大数据
    'bidding': fetch_bidding,                   # 14 招投标活动
    'group_info': fetch_group_info,             # 15 集团信息
    'portrait': fetch_portrait,                 # 16 综合画像
    'ip': fetch_ip,                             # 17 知识产权
    'innovation': fetch_innovation,             # 18 科创能力评估
    'shell_company': fetch_shell_company,       # 19 空壳公司识别
    'risk_assessment': fetch_risk_assessment,   # 20 风险评测
    'investment_query': fetch_investment_query, # 21 投资任职查询
}


# 脚本中文名称映射
SCRIPT_NAMES = {
    'entity_info': '主体信息',
    'listed_info': '上市信息',
    'financial_info': '财务信息',
    'debt_financing': '债权融资',
    'risk_data': '风险大数据',
    'sentiment': '舆情信息',
    'controller': '实际控制人',
    'related_parties': '关联方信息',
    'customers': '客户/供应商',
    'operations': '企业经营动态',
    'investment': '投融资事件',
    'history': '历史大数据',
    'bidding': '招投标活动',
    'group_info': '集团信息',
    'portrait': '综合画像',
    'ip': '知识产权',
    'innovation': '科创能力评估',
    'shell_company': '空壳公司识别',
    'risk_assessment': '风险评测',
    'investment_query': '投资任职查询',
}


def fetch_single(script_name: str, entname: str) -> str:
    """
    获取单个维度的数据

    Args:
        script_name: 脚本名称（如 'entity_info', 'listed_info' 等）
        entname: 企业名称

    Returns:
        Markdown 格式的处理结果
    """
    if script_name not in SCRIPTS:
        return f"未知的脚本名称: {script_name}"

    return SCRIPTS[script_name](entname)


def fetch_multiple(script_names: list, entname: str) -> dict:
    """
    获取多个维度的数据

    Args:
        script_names: 脚本名称列表
        entname: 企业名称

    Returns:
        字典，键为脚本名称，值为 Markdown 格式的处理结果
    """
    results = {}
    for name in script_names:
        if name in SCRIPTS:
            results[name] = SCRIPTS[name](entname)
    return results


def fetch_all(entname: str) -> dict:
    """
    获取所有维度的数据

    Args:
        entname: 企业名称

    Returns:
        字典，键为脚本名称，值为 Markdown 格式的处理结果
    """
    return {name: func(entname) for name, func in SCRIPTS.items()}


def list_scripts() -> list:
    """
    列出所有可用的脚本

    Returns:
        脚本名称列表
    """
    return list(SCRIPTS.keys())


def get_script_name(script_key: str) -> str:
    """
    获取脚本的中文名称

    Args:
        script_key: 脚本键名

    Returns:
        中文名称
    """
    return SCRIPT_NAMES.get(script_key, script_key)


# 版本信息
__version__ = '1.0.0'
__all__ = [
    # 单个脚本导出
    'fetch_entity_info',
    'fetch_listed_info',
    'fetch_financial_info',
    'fetch_debt_financing',
    'fetch_risk_data',
    'fetch_sentiment',
    'fetch_controller',
    'fetch_related_parties',
    'fetch_customers',
    'fetch_operations',
    'fetch_investment',
    'fetch_history',
    'fetch_bidding',
    'fetch_group_info',
    'fetch_portrait',
    'fetch_ip',
    'fetch_innovation',
    'fetch_shell_company',
    'fetch_risk_assessment',
    'fetch_investment_query',
    # 工具函数
    'fetch_single',
    'fetch_multiple',
    'fetch_all',
    'list_scripts',
    'get_script_name',
    # 映射表
    'SCRIPTS',
    'SCRIPT_NAMES',
]
