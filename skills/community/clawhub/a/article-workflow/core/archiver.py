#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
归档模块

功能：将分析结果归档到飞书 Bitable 和文档

注意：
    此模块需要 OpenClaw 飞书插件支持：
    - feishu_bitable_app_table_record: 写入多维表格
    - feishu_create_doc: 创建飞书文档
    
    独立运行时这些功能不可用
"""

import json
from pathlib import Path
from datetime import datetime

# 配置文件路径（相对路径）
MODULE_DIR = Path(__file__).parent
SKILL_DIR = MODULE_DIR.parent
CONFIG_FILE = SKILL_DIR / "config.json"


def load_config() -> dict:
    """加载配置文件"""
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}


def archive_to_bitable(analysis_result: dict, doc_url: str) -> dict:
    """
    归档到 Bitable
    
    Args:
        analysis_result: 分析结果
            - title: 标题
            - url: URL
            - source: 来源
            - summary: 摘要
            - importance: 重要程度
            - quality_score: 质量评分
        doc_url: 详细报告文档链接
    
    Returns:
        dict: {
            "record_id": str,
            "success": bool
        }
    
    Note:
        实际实现需要调用飞书 Bitable API
        这里提供接口定义
    """
    config = load_config()
    bitable_token = config.get("bitable", {}).get("app_token")
    table_id = config.get("bitable", {}).get("table_id")
    
    # 准备字段
    fields = {
        "标题": analysis_result.get("title", ""),
        "URL 链接": analysis_result.get("url", ""),
        "来源": analysis_result.get("source", "其他"),
        "简短摘要": analysis_result.get("summary", ""),
        "详细报告链接": doc_url,
        "重要程度": analysis_result.get("importance", "中"),
        "阅读日期": int(datetime.now().timestamp() * 1000),
        "状态": "已完成",
        "创建方式": "手动触发"
    }
    
    # 添加质量评分（如果配置启用）
    if config.get("workflow", {}).get("enable_quality_score", True):
        quality = analysis_result.get("quality_score", {})
        fields["质量评分"] = quality.get("total", 0)
        fields["评分等级"] = quality.get("level", "C")
    
    # TODO: 调用飞书 Bitable API 创建记录
    # feishu_bitable_app_table_record(action="create", ...)
    
    return {
        "record_id": "",  # 实际 API 返回
        "success": True
    }


def create_feishu_doc(report_content: str, title: str) -> dict:
    """
    创建飞书文档
    
    Args:
        report_content: 报告内容（Markdown）
        title: 文档标题
    
    Returns:
        dict: {
            "doc_id": str,
            "doc_url": str
        }
    
    Note:
        实际实现需要调用飞书文档 API
    """
    # TODO: 调用飞书文档 API 创建文档
    # feishu_create_doc(markdown=report_content, title=title)
    
    return {
        "doc_id": "",  # 实际 API 返回
        "doc_url": ""
    }


def format_bitable_fields(analysis_result: dict, doc_url: str) -> dict:
    """
    格式化 Bitable 字段
    
    Args:
        analysis_result: 分析结果
        doc_url: 文档链接
    
    Returns:
        dict: 格式化的字段对象
    """
    fields = {
        "标题": analysis_result.get("title", ""),
        "URL 链接": analysis_result.get("url", ""),
        "来源": analysis_result.get("source", "其他"),
        "简短摘要": analysis_result.get("summary", ""),
        "详细报告链接": doc_url,
        "重要程度": analysis_result.get("importance", "中"),
        "阅读日期": int(datetime.now().timestamp() * 1000),
        "状态": "已完成",
        "创建方式": "手动触发"
    }
    
    # 质量评分
    quality = analysis_result.get("quality_score", {})
    if quality:
        fields["质量评分"] = quality.get("total", 0)
        fields["评分等级"] = quality.get("level", "C")
        fields["内容价值"] = quality.get("content_value", 0)
        fields["技术深度"] = quality.get("technical_depth", 0)
        fields["适配性"] = quality.get("relevance", 0)
        fields["可读性"] = quality.get("readability", 0)
    
    return fields
