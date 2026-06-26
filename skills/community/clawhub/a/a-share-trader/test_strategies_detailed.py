#!/usr/bin/env python3
"""详细测试各策略的筛选逻辑"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import logging
from strategies import *
from core.data_interface import AShareDataInterface

logging.basicConfig(level=logging.INFO)

def test_strategy_filtering():
    """测试策略筛选逻辑"""
    print("测试策略筛选逻辑")
    print("=" * 80)
    
    # 获取数据
    data_interface = AShareDataInterface()
    market_data = data_interface.get_market_data()
    fundamental_data = data_interface.get_fundamental_data()
    
    print(f"市场数据: {len(market_data)} 只股票")
    print(f"基本面数据: {len(fundamental_data)} 只股票")
    
    # 测试各策略
    strategies_to_test = [
        ("fundamental", FundamentalStrategy),
        ("defensive", DefensiveStrategy),
        ("swing_trading", SwingTradingStrategy),
        ("small_cap", SmallCapStrategy),
        ("quality_small_cap", QualitySmallCapStrategy),
        ("small_cap_growth", SmallCapGrowthStrategy),
        ("revenue_profit", RevenueProfitStrategy),
        ("chip_concentration", ChipConcentrationStrategy),
        ("social_security", SocialSecurityStrategy),
        ("oversold_rebound", OversoldReboundStrategy),
        ("resonance", ResonanceStrategy)
    ]
    
    for name, strategy_class in strategies_to_test:
        if strategy_class is None:
            print(f"\n{name}: 策略类未找到")
            continue
            
        print(f"\n{name}:")
        print("-" * 40)
        
        try:
            # 创建策略实例
            strategy = strategy_class()
            
            # 生成信号
            signals = strategy.generate_signals(
                market_data=market_data,
                fundamental_data=fundamental_data
            )
            
            print(f"  生成信号数: {len(signals)}")
            
            # 分析信号类型
            buy_count = sum(1 for s in signals if s.get('side') == 'BUY')
            sell_count = sum(1 for s in signals if s.get('side') == 'SELL')
            hold_count = sum(1 for s in signals if s.get('side') == 'HOLD')
            
            print(f"  BUY: {buy_count}, SELL: {sell_count}, HOLD: {hold_count}")
            
            if signals:
                # 显示前几个信号
                for i, signal in enumerate(signals[:3]):
                    print(f"  信号{i+1}: {signal.get('symbol')} {signal.get('side')} "
                          f"@{signal.get('price', 0):.2f} - {signal.get('reason', '')[:50]}")
            
            # 检查策略参数
            if hasattr(strategy, 'parameters'):
                param_count = len(strategy.parameters)
                print(f"  参数数量: {param_count}")
                
                # 显示关键参数
                key_params = ['holding_count', 'rebalance_days', 'min_market_cap', 'max_pe']
                for param in key_params:
                    if param in strategy.parameters:
                        print(f"  {param}: {strategy.parameters[param]}")
            
        except Exception as e:
            print(f"  测试失败: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_strategy_filtering()