#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI量化交易助手功能演示
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import handle_command

def print_separator(title):
    """打印分隔符"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def demo_initialization():
    """演示初始化功能"""
    print_separator("1. 系统初始化")
    
    # 查看帮助
    print("📖 查看帮助命令:")
    help_text = handle_command("/帮助")
    # 只显示部分帮助内容
    lines = help_text.split('\n')[:15]
    print('\n'.join(lines))
    print("...")
    
    # 设置初始资金
    print("\n💰 设置初始资金:")
    result = handle_command("/交易 设置本金 100000")
    print(result)

def demo_data_queries():
    """演示数据查询功能"""
    print_separator("2. 数据查询功能")
    
    # 查看股票价格
    print("📊 查看贵州茅台当前价格:")
    result = handle_command("/数据 价格 600519")
    print(result)
    
    # 技术分析
    print("\n📈 贵州茅台技术分析:")
    result = handle_command("/数据 分析 600519")
    print(result)

def demo_stock_screening():
    """演示选股功能"""
    print_separator("3. AI选股功能")
    
    # 获取今日推荐
    print("🤖 AI今日推荐股票:")
    result = handle_command("/选股 今日推荐")
    print(result)
    
    # 条件筛选
    print("\n🔍 按条件筛选股票:")
    result = handle_command("/选股 筛选 MACD金叉")
    print(result)

def demo_strategy_generation():
    """演示策略生成功能"""
    print_separator("4. AI策略生成")
    
    # 生成MACD策略
    print("🧠 AI生成MACD交易策略:")
    result = handle_command("/策略 生成 一个基于MACD金叉的短线交易策略，当MACD金叉时买入，死叉时卖出")
    print(result)
    
    # 查看策略列表
    print("\n📋 查看策略列表:")
    result = handle_command("/策略 列表")
    print(result)

def demo_trading_operations():
    """演示交易操作"""
    print_separator("5. 模拟交易操作")
    
    # 买入操作
    print("🛒 模拟买入贵州茅台100股（假设价格1800元）:")
    # 注意：这里需要模拟价格，实际系统会从AKShare获取
    print("（实际系统会从AKShare获取实时价格）")
    
    # 查看持仓
    print("\n📊 查看当前持仓:")
    result = handle_command("/持仓")
    print(result)
    
    # 卖出操作
    print("\n💰 模拟卖出50股:")
    print("（实际系统会计算盈亏和手续费）")

def demo_auto_trading():
    """演示自动交易"""
    print_separator("6. 自动交易设置")
    
    # 启用自动交易
    print("⚡ 启用自动交易:")
    result = handle_command("/自动 启用 MACD策略 600519")
    print(result)
    
    # 查看自动交易状态
    print("\n📋 查看自动交易列表:")
    result = handle_command("/自动 列表")
    print(result)

def demo_risk_management():
    """演示风控功能"""
    print_separator("7. 风险控制设置")
    
    # 设置止损
    print("🛡️ 设置止损（亏损5%时自动卖出）:")
    result = handle_command("/风控 设置止损 600519 5%")
    print(result)
    
    # 设置止盈
    print("\n🎯 设置止盈（盈利10%时自动卖出）:")
    result = handle_command("/风控 设置止盈 600519 10%")
    print(result)
    
    # 设置移动止盈
    print("\n📈 设置移动止盈（从最高点回撤8%时卖出）:")
    result = handle_command("/风控 移动止盈 600519 8%")
    print(result)

def demo_statistics():
    """演示统计分析"""
    print_separator("8. 策略统计分析")
    
    # 查看策略统计
    print("📊 查看MACD策略统计:")
    result = handle_command("/统计 MACD策略")
    print(result)
    
    # 策略回测
    print("\n🔍 回测MACD策略:")
    result = handle_command("/策略 回测 MACD策略")
    print(result)

def demo_advanced_features():
    """演示高级功能"""
    print_separator("9. 高级功能演示")
    
    # 策略优化
    print("⚙️ AI优化策略参数:")
    result = handle_command("/策略 优化 MACD策略")
    print(result)
    
    # 多条件筛选
    print("\n🔍 多条件筛选股票:")
    result = handle_command("/选股 筛选 MACD金叉 RSI<30 放量上涨")
    print(result)

def demo_complete_workflow():
    """演示完整工作流程"""
    print_separator("10. 完整投资工作流程")
    
    steps = [
        "1. 📋 设置初始资金: /交易 设置本金 100000",
        "2. 🔍 研究市场: /选股 今日推荐",
        "3. 🧠 制定策略: /策略 生成 '价值投资策略'",
        "4. ⚡ 启用自动: /自动 启用 价值策略 600519",
        "5. 🛡️ 设置风控: /风控 设置止损 600519 5%",
        "6. 📊 监控持仓: /持仓",
        "7. 📈 分析表现: /统计 价值策略",
        "8. 🔄 优化调整: /策略 优化 价值策略"
    ]
    
    for step in steps:
        print(step)

def main():
    """主演示函数"""
    print("🎬 AI量化交易助手功能演示")
    print("="*60)
    
    try:
        # 执行各功能演示
        demo_initialization()
        demo_data_queries()
        demo_stock_screening()
        demo_strategy_generation()
        demo_trading_operations()
        demo_auto_trading()
        demo_risk_management()
        demo_statistics()
        demo_advanced_features()
        demo_complete_workflow()
        
        print_separator("演示完成")
        print("✅ 所有功能演示完成！")
        print("\n💡 现在你可以:")
        print("1. 使用 /帮助 查看所有命令")
        print("2. 使用 /交易 设置本金 开始模拟交易")
        print("3. 使用 /选股 今日推荐 获取AI推荐")
        print("4. 使用 /策略 生成 创建自己的策略")
        
    except Exception as e:
        print(f"❌ 演示过程中出现错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()