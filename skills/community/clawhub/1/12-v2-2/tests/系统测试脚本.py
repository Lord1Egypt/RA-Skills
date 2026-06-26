#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
V2.2系统测试和验证脚本
"""

import sys
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

print("=" * 70)
print(" V2.2系统测试和验证")
print("=" * 70)

tests_passed = 0
tests_total = 7

# 测试1: 导入所有模块
print("\n[测试1/7] 模块导入测试...")
try:
    from data_manager import DataFetcherManager
    from market_analyzer import MarketAnalyzer
    from realtime_analyzer import RealtimeAnalyzer
    from chip_analyzer import ChipAnalyzer
    from email_notifier import EmailNotifier
    from pipeline import StockAnalysisPipeline
    print("✓ 所有模块导入成功")
    tests_passed += 1
except Exception as e:
    print(f"✗ 模块导入失败: {e}")

# 测试2: 数据管理器
print("\n[测试2/7] 数据管理器测试...")
try:
    manager = DataFetcherManager()
    print("✓ 数据管理器初始化成功")
    tests_passed += 1
except Exception as e:
    print(f"✗ 数据管理器测试失败: {e}")

# 测试3: 大盘分析器
print("\n[测试3/7] 大盘分析器测试...")
try:
    analyzer = MarketAnalyzer()
    print("✓ 大盘分析器初始化成功")
    tests_passed += 1
except Exception as e:
    print(f"✗ 大盘分析器测试失败: {e}")

# 测试4: 实时行情分析器
print("\n[测试4/7] 实时行情分析器测试...")
try:
    realtime = RealtimeAnalyzer()
    print("✓ 实时行情分析器初始化成功")
    tests_passed += 1
except Exception as e:
    print(f"✗ 实时行情分析器测试失败: {e}")

# 测试5: 筹码分析器
print("\n[测试5/7] 筹码分析器测试...")
try:
    chip = ChipAnalyzer()
    print("✓ 筹码分析器初始化成功")
    tests_passed += 1
except Exception as e:
    print(f"✗ 筹码分析器测试失败: {e}")

# 测试6: 完整流水线
print("\n[测试6/7] 完整流水线测试...")
try:
    pipeline = StockAnalysisPipeline(config={})
    print("✓ 完整流水线初始化成功")
    tests_passed += 1
except Exception as e:
    print(f"✗ 完整流水线测试失败: {e}")

# 测试7: 配置文件
print("\n[测试7/7] 配置文件测试...")
try:
    import yaml
    with open('/tmp/config_v22.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print(f"✓ 配置文件读取成功 (包含{len(config)}个顶级配置)")
    tests_passed += 1
except Exception as e:
    print(f"✗ 配置文件测试失败: {e}")

# 总结
print("\n" + "=" * 70)
print(f"测试完成: {tests_passed}/{tests_total} 通过")
print("=" * 70)

if tests_passed == tests_total:
    print("\n✅ 所有测试通过！V2.2系统可以正常使用")
    sys.exit(0)
else:
    print(f"\n⚠️  有{tests_total - tests_passed}个测试失败，请检查")
    sys.exit(1)
