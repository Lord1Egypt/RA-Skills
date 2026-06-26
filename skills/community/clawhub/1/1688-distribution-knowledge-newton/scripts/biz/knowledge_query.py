#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
分销知识库查询业务模块

功能：
1. 查询分销知识库
2. 渠道/工具名称验证
3. 支持单渠道单工具查询

"""

import sys
import os
from typing import Dict, List, Optional, Tuple

# 导入系统模块
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from _http import api_post
from _auth import get_ak_from_env
from biz.const import (
    DEFAULT_USER_ID,
    VALID_CHANNELS,
    VALID_BUSINESSES,
)

def check_ak_config(show_guide: bool = True) -> Tuple[bool, str]:
    """
    检查 AK 配置状态
    
    参数：
    - show_guide: 是否显示配置指南（默认 True）
    
    返回：
    (是否已配置，AK 值或错误信息)
    """
    ak_id, ak_secret = get_ak_from_env()
    
    if not ak_id or not ak_secret:
        if show_guide:
            print("=" * 80)
            print("⚠️  检测到 AK 未配置")
            print("=" * 80)
            print()
            print("📋 配置 AK：")
            print("   1. 获取 AK：打开 https://clawhub.1688.com")
            print("   2. 执行配置：python3 scripts/capabilities/configure/cmd.py YOUR_AK")
            print()
        return False, "AK 未配置"
    
    return True, ak_id

def is_valid_channel(name: str) -> bool:
    """
    验证渠道名称是否有效
    
    参数：
    - name: 中文渠道名，如 "抖音"，或 "default" 表示使用默认知识库
    
    返回：
    True 如果是有效渠道名称，否则 False
    """
    return name == "default" or name in VALID_CHANNELS

def is_valid_business(name: str) -> bool:
    """
    验证工具名称是否有效
    
    参数：
    - name: 中文工具名，如 "自动分销"，或 "default" 表示使用默认知识库
    
    返回：
    True 如果是有效工具名称，否则 False
    """
    return name == "default" or name in VALID_BUSINESSES

def list_channels() -> List[str]:
    """返回所有支持的渠道名称列表"""
    return VALID_CHANNELS.copy()

def list_businesses() -> List[str]:
    """返回所有支持的工具名称列表"""
    return VALID_BUSINESSES.copy()

def query_knowledge(
    query: str,
    channel: str = "default",
    business: str = "default",
) -> Dict:
    """
    查询分销知识库
    
    参数：
    - query: 用户的查询问题（必填）
    - channel: 渠道中文名（如 "抖音"），未指定时传 "default"
    - business: 工具中文名（如 "逸淘分销铺货"），未指定时传 "default"
    
    返回：
    {
        "success": bool,
        "data": [...],  # 文档数组，每条包含 score, chunking_val, source_url
        "error": str  # 错误时返回
    }
    """
    # 检查 AK 配置
    ak_configured, ak_message = check_ak_config(show_guide=True)
    if not ak_configured:
        return {
            "success": False,
            "data": None,
            "error": f"调用失败：{ak_message}",
            "errorCode": "AK_NOT_CONFIGURED"
        }
    
    # 参数校验
    if not query or not query.strip():
        return {
            "success": False,
            "data": None,
            "error": "查询问题不能为空",
            "errorCode": "PARAM_ERROR"
        }
    
    # 验证 channel
    if not is_valid_channel(channel):
        return {
            "success": False,
            "data": None,
            "error": f"无效的渠道名称：{channel}",
            "errorCode": "PARAM_ERROR"
        }
    
    # 验证 business
    if not is_valid_business(business):
        return {
            "success": False,
            "data": None,
            "error": f"无效的工具名称：{business}",
            "errorCode": "PARAM_ERROR"
        }
    
    # 构建请求体（新格式：直接传中文名称字符串）
    arguments = {
        "__userId__": DEFAULT_USER_ID,
        "query": query.strip(),
        "channel": channel,
        "business": business,
    }
    
    try:
        # 调用知识库 API
        # tool_name 为源舟平台注册的工具 code
        result = api_post(tool_name="distribution_knowledge_tool", body=arguments)
        
        # 处理返回数据
        # 注意：API 返回的 data 字段可能是 JSON 字符串，需要解析
        if isinstance(result, str):
            import json
            try:
                result = json.loads(result)
            except json.JSONDecodeError:
                result = []
        
        return {
            "success": True,
            "data": result if isinstance(result, list) else []
        }
        
    except Exception as e:
        return {
            "success": False,
            "data": None,
            "error": f"调用失败：{str(e)}",
            "errorCode": "API_ERROR"
        }

# ==================== 命令行入口 ====================

if __name__ == "__main__":
    print("=" * 80)
    print("分销知识库查询 - 测试示例")
    print("=" * 80)
    
    # 测试查询（新格式：直接传中文名称）
    result = query_knowledge(
        query="铺货",
        channel="淘宝",
        business="逸淘分销铺货"
    )
    
    if result.get("success"):
        doc_list = result.get("data", [])
        print(f"✅ 查询成功，返回 {len(doc_list)} 条结果")
        for i, doc in enumerate(doc_list[:3], 1):
            print(f"\n{i}. 相关度: {doc.get('score', 0)}")
            content = doc.get('chunking_val', '')[:100]
            print(f"   内容: {content}...")
    else:
        print(f"❌ 调用失败：{result.get('error')}")
