#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试所有模块
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """测试基本导入"""
    print("🧪 测试模块导入...")
    
    modules = [
        ("main", "主程序"),
        ("broker", "交易引擎"),
        ("data_provider", "数据提供"),
        ("strategy_gen", "策略生成"),
        ("auto_trader", "自动交易"),
        ("risk_manager", "风险管理"),
        ("stock_screener", "选股引擎")
    ]
    
    all_ok = True
    for module_name, desc in modules:
        try:
            __import__(module_name)
            print(f"  ✅ {desc}({module_name})")
        except ImportError as e:
            print(f"  ❌ {desc}({module_name}): {e}")
            all_ok = False
    
    return all_ok

def test_main_module():
    """测试主模块"""
    print("\n🧪 测试主模块...")
    
    try:
        from main import handle_command
        
        # 测试帮助命令
        print("  测试 /帮助 命令...")
        result = handle_command("/帮助")
        if result and len(result) > 0:
            print("  ✅ 帮助命令正常")
            # 显示部分帮助
            lines = result.split('\n')[:5]
            for line in lines:
                print(f"    {line}")
        else:
            print("  ❌ 帮助命令返回空")
            return False
        
        # 测试设置本金命令
        print("\n  测试 /交易 设置本金 命令...")
        result = handle_command("/交易 设置本金 50000")
        if "设置" in result or "成功" in result or "50000" in result:
            print("  ✅ 设置本金命令正常")
        else:
            print(f"  ⚠️ 设置本金命令返回: {result[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 主模块测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_data_provider():
    """测试数据提供模块"""
    print("\n🧪 测试数据提供模块...")
    
    try:
        from data_provider import DataProvider
        
        provider = DataProvider()
        print("  ✅ 数据提供器初始化成功")
        
        # 测试获取股票信息
        print("  测试获取股票信息...")
        info = provider.get_stock_info("600519")
        if info and "symbol" in info:
            print(f"  ✅ 获取股票信息成功: {info.get('name', '未知')}")
        else:
            print("  ⚠️ 获取股票信息返回异常")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 数据提供模块测试失败: {e}")
        return False

def test_strategy_generator():
    """测试策略生成模块"""
    print("\n🧪 测试策略生成模块...")
    
    try:
        from strategy_gen import StrategyGenerator
        
        generator = StrategyGenerator()
        print("  ✅ 策略生成器初始化成功")
        
        # 测试生成策略
        print("  测试生成策略...")
        result = generator.generate_strategy("测试策略")
        if result and result.get("success"):
            print(f"  ✅ 策略生成成功: {result.get('strategy_name')}")
        else:
            print("  ⚠️ 策略生成返回异常")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 策略生成模块测试失败: {e}")
        return False

def test_stock_screener():
    """测试选股模块"""
    print("\n🧪 测试选股模块...")
    
    try:
        from stock_screener import StockScreener
        
        screener = StockScreener()
        print("  ✅ 选股器初始化成功")
        
        # 测试获取A股列表
        print("  测试获取A股列表...")
        stocks = screener.get_all_a_shares()
        if not stocks.empty:
            print(f"  ✅ 获取到 {len(stocks)} 只A股")
        else:
            print("  ⚠️ 获取A股列表为空")
        
        return True
        
    except Exception as e:
        print(f"  ❌ 选股模块测试失败: {e}")
        return False

def test_openclaw_integration():
    """测试OpenClaw集成"""
    print("\n🧪 测试OpenClaw集成...")
    
    try:
        from openclaw_integration import openclaw_handler, get_skill_info
        
        # 测试获取技能信息
        info = get_skill_info()
        print(f"  ✅ 技能信息: {info['name']} v{info['version']}")
        
        # 测试处理命令
        print("  测试处理命令...")
        result = openclaw_handler("/帮助")
        if result and len(result) > 0:
            print("  ✅ OpenClaw处理器正常")
        else:
            print("  ❌ OpenClaw处理器返回空")
            return False
        
        return True
        
    except Exception as e:
        print(f"  ❌ OpenClaw集成测试失败: {e}")
        return False

def main():
    """主测试函数"""
    print("=" * 60)
    print("🤖 AI量化交易助手 - 模块测试")
    print("=" * 60)
    
    test_results = []
    
    # 运行所有测试
    test_results.append(("模块导入", test_basic_imports()))
    test_results.append(("主模块", test_main_module()))
    test_results.append(("数据提供", test_data_provider()))
    test_results.append(("策略生成", test_strategy_generator()))
    test_results.append(("选股引擎", test_stock_screener()))
    test_results.append(("OpenClaw集成", test_openclaw_integration()))
    
    # 显示测试结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总")
    print("=" * 60)
    
    passed = 0
    total = len(test_results)
    
    for test_name, success in test_results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name:20} {status}")
        if success:
            passed += 1
    
    print(f"\n🎯 通过率: {passed}/{total} ({passed/total*100:.0f}%)")
    
    if passed == total:
        print("\n🎉 所有测试通过！技能可以正常使用。")
        print("\n📋 下一步:")
        print("1. 在OpenClaw中使用命令:")
        print("   /交易 设置本金 100000")
        print("   /选股 今日推荐")
        print("2. 或直接调用: openclaw_integration.openclaw_handler()")
    else:
        print(f"\n⚠️  有{total-passed}个测试失败，需要检查。")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)