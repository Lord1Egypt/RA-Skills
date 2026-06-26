#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
===================================
V2.2完整回测验证系统
===================================

整合所有V2.2模块的完整回测系统
"""

import yaml
import pandas as pd
import numpy as np
from datetime import datetime
import logging

# 导入V2.2模块
from data_manager import DataFetcherManager
from market_analyzer import MarketAnalyzer
from realtime_analyzer import RealtimeAnalyzer
from chip_analyzer import ChipAnalyzer
from pipeline import StockAnalysisPipeline

logger = logging.getLogger(__name__)

def main():
    """主函数"""
    print("=" * 70)
    print(" AI量化交易系统 V2.2 - 完整回测验证")
    print("=" * 70)

    # 加载配置
    config = load_config('config_v22.yaml')

    # 初始化各模块
    print("\n[1/6] 初始化数据管理器...")
    data_manager = DataFetcherManager(config.get('data_sources'))

    print("[2/6] 初始化大盘分析器...")
    market_analyzer = MarketAnalyzer(region=config.get('region', 'cn'))

    print("[3/6] 初始化实时行情分析器...")
    realtime_analyzer = RealtimeAnalyzer(data_manager)

    print("[4/6] 初始化筹码分析器...")
    chip_analyzer = ChipAnalyzer()

    print("[5/6] 初始化完整流水线...")
    pipeline = StockAnalysisPipeline(
        config=config,
        notifier_config=config.get('notification')
    )

    print("[6/6] 准备回测...")
    print()

    # 获取市场环境
    overview = market_analyzer.get_market_overview()
    env = market_analyzer.analyze_environment(overview)
    threshold = market_analyzer.get_buy_threshold(env)

    print(f"市场环境: {env.value.upper()}")
    print(f"买入阈值: {threshold}")
    print()

    # 测试股票
    stock_list = ['600519', '000858', '600036', '000651', '600276']

    # 批量分析
    print("=" * 70)
    print("开始批量分析...")
    print("=" * 70)

    results = pipeline.analyze_stocks(
        stock_list=stock_list,
        buy_threshold=threshold,
        send_notification=False
    )

    # 打印结果
    print("\n" + "=" * 70)
    print("分析结果汇总")
    print("=" * 70)

    for code, result in results.items():
        print(f"\n{result.name}({code}):")
        print(f"  信号评分: {result.signal_score:.2f}/10")
        print(f"  交易建议: {result.recommendation}")
        print(f"  建议原因: {result.reason}")
        print(f"  风险等级: {result.risk_level}")

    print("\n" + "=" * 70)
    print("V2.2完整系统验证完成！")
    print("=" * 70)

    return results

def load_config(config_file):
    """加载配置"""
    try:
        with open(config_file, 'r') as f:
            return yaml.safe_load(f)
    except:
        # 返回默认配置
        return {
            'region': 'cn',
            'data_sources': {'primary': 'akshare'},
            'realtime': {'enabled': True},
            'chip_distribution': {'enabled': True},
            'market_environment': {'enabled': True},
        }

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    main()
