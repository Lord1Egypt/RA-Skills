#!/usr/bin/env python3
"""简单测试优化系统"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 测试真实数据接口
print("测试真实数据接口...")
try:
    from core.real_data_interface import RealAShareDataInterface
    data_interface = RealAShareDataInterface(use_xtquant=True, use_tushare=False)
    
    # 测试连接
    test_result = data_interface.test_connection()
    print(f"连接测试: {test_result.get('market_data_test', {}).get('success', '未知')}")
    print(f"xtquant可用: {test_result.get('xtquant_available', False)}")
    
    # 获取数据
    symbols = ["000001.SZ", "600036.SH"]
    market_data = data_interface.get_market_data(symbols)
    print(f"获取 {len(market_data)} 只股票数据")
    
    for symbol, data in market_data.items():
        print(f"  {symbol}: 价格={data.get('price')}, 涨跌幅={data.get('change_percent')}%")
    
except Exception as e:
    print(f"数据接口测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)

# 测试策略优化器
print("\n测试策略优化器...")
try:
    from strategy_optimizer import StrategyOptimizer
    
    config = StrategyOptimizer.get_optimized_config_for_mock_data()
    print(f"优化配置: {len(config)} 种策略")
    
    # 显示几个策略的配置
    strategies_to_show = ["fundamental", "quality_small_cap", "small_cap_growth"]
    for strategy_name in strategies_to_show:
        if strategy_name in config:
            params = config[strategy_name]
            print(f"  {strategy_name}:")
            for key, value in list(params.items())[:3]:  # 只显示前3个参数
                print(f"    {key}: {value}")
    
except Exception as e:
    print(f"策略优化器测试失败: {e}")

print("\n" + "=" * 60)

# 测试策略生成
print("\n测试策略信号生成...")
try:
    from core.real_data_interface import RealAShareDataInterface
    from strategy_optimizer import StrategyOptimizer
    from strategies import FundamentalStrategy, QualitySmallCapStrategy
    
    # 获取数据
    data_interface = RealAShareDataInterface()
    symbols = ["000001.SZ", "000002.SZ", "600036.SH", "601318.SH"]
    market_data = data_interface.get_market_data(symbols)
    fundamental_data = data_interface.get_fundamental_data(symbols)
    
    # 测试基本面策略
    fundamental_strategy = StrategyOptimizer.create_optimized_strategy(
        FundamentalStrategy, "fundamental"
    )
    fundamental_signals = fundamental_strategy.generate_signals(
        market_data=market_data,
        fundamental_data=fundamental_data
    )
    print(f"基本面策略信号: {len(fundamental_signals)} 个")
    
    # 测试质量小市值策略
    quality_small_cap_strategy = StrategyOptimizer.create_optimized_strategy(
        QualitySmallCapStrategy, "quality_small_cap"
    )
    quality_signals = quality_small_cap_strategy.generate_signals(
        market_data=market_data,
        fundamental_data=fundamental_data
    )
    print(f"质量小市值策略信号: {len(quality_signals)} 个")
    
    # 显示信号
    if fundamental_signals or quality_signals:
        print("\n生成的信号:")
        all_signals = fundamental_signals + quality_signals
        for i, signal in enumerate(all_signals[:5]):  # 显示前5个
            print(f"  {i+1}. {signal.get('symbol')} {signal.get('side')} "
                  f"@{signal.get('price', 0):.2f}")
    
except Exception as e:
    print(f"策略测试失败: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("测试完成!")