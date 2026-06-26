#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI量化交易助手 - OpenClaw技能入口
"""

from .main import handle_command

__all__ = ['handle_command']

# 技能信息
SKILL_INFO = {
    "name": "AI量化交易助手",
    "version": "1.0.0",
    "description": "基于AKShare的AI驱动量化交易模拟系统",
    "author": "小火马",
    "commands": [
        "/交易 - 模拟交易操作",
        "/策略 - AI策略生成和管理",
        "/自动 - 自动交易设置",
        "/风控 - 风险控制设置",
        "/选股 - 股票筛选和推荐",
        "/统计 - 策略统计分析",
        "/数据 - 数据查询和技术分析",
        "/帮助 - 显示帮助信息"
    ]
}