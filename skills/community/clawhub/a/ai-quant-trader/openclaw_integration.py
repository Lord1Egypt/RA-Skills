#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OpenClaw集成模块 - 让AI量化交易助手可以直接在OpenClaw中使用
"""

import sys
import os
import json
from datetime import datetime

# 添加当前目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def openclaw_handler(message, context=None):
    """
    OpenClaw消息处理器
    
    Args:
        message: 用户消息
        context: OpenClaw上下文（可选）
    
    Returns:
        处理结果字符串
    """
    try:
        # 导入主处理器
        from main import handle_command
        
        # 处理命令
        result = handle_command(message)
        
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 格式化返回结果
        response = f"🤖 AI量化交易助手 ({timestamp})\n"
        response += "=" * 40 + "\n"
        response += result
        
        return response
        
    except Exception as e:
        # 错误处理
        error_msg = f"❌ 处理命令时出错: {str(e)}"
        print(f"错误详情: {e}")
        import traceback
        traceback.print_exc()
        
        return error_msg

def get_skill_info():
    """获取技能信息"""
    return {
        "name": "AI量化交易助手",
        "version": "1.0.0",
        "description": "基于AKShare的AI驱动量化交易模拟系统",
        "author": "小火马",
        "commands": {
            "交易": "模拟交易操作（设置本金、买入、卖出、持仓）",
            "策略": "AI策略生成和管理",
            "自动": "自动交易设置",
            "风控": "风险控制设置（止盈止损）",
            "选股": "股票筛选和推荐",
            "统计": "策略统计分析",
            "数据": "数据查询和技术分析",
            "帮助": "显示帮助信息"
        },
        "examples": [
            "/交易 设置本金 100000",
            "/选股 今日推荐",
            "/策略 生成 'MACD金叉策略'",
            "/数据 分析 600519",
            "/持仓"
        ]
    }

# 测试函数
def test_integration():
    """测试集成"""
    print("🧪 测试OpenClaw集成...")
    
    test_commands = [
        "/帮助",
        "/交易 设置本金 50000",
        "/选股 筛选 沪深A股 非ST"
    ]
    
    for cmd in test_commands:
        print(f"\n📨 测试命令: {cmd}")
        print("-" * 40)
        try:
            result = openclaw_handler(cmd)
            print(result[:200] + "..." if len(result) > 200 else result)
        except Exception as e:
            print(f"❌ 测试失败: {e}")
    
    print("\n✅ 集成测试完成")

if __name__ == "__main__":
    # 直接运行测试
    test_integration()