#!/usr/bin/env python3
"""
优化版快速启动脚本 - 使用优化策略和真实数据
"""
import sys
import os
import logging
import json
from datetime import datetime

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def test_optimized_system():
    """测试优化后的系统"""
    print("=" * 60)
    print("A股核心交易框架 - 优化版测试")
    print("=" * 60)
    
    try:
        # 1. 初始化真实数据接口
        from core.real_data_interface import RealAShareDataInterface
        data_interface = RealAShareDataInterface(use_xtquant=True, use_tushare=False)
        
        # 测试连接
        connection_test = data_interface.test_connection()
        print(f"1. 数据接口连接测试: {connection_test.get('market_data_test', {}).get('success', False)}")
        
        # 2. 获取数据
        symbols = ["000001.SZ", "000002.SZ", "600036.SH", "601318.SH", "300750.SZ"]
        market_data = data_interface.get_market_data(symbols)
        fundamental_data = data_interface.get_fundamental_data(symbols)
        
        print(f"2. 数据获取: 市场数据={len(market_data)}只, 基本面数据={len(fundamental_data)}只")
        
        # 3. 初始化优化策略
        from strategy_optimizer import StrategyOptimizer
        from strategies import (
            FundamentalStrategy, DefensiveStrategy, SwingTradingStrategy,
            SmallCapStrategy, QualitySmallCapStrategy, SmallCapGrowthStrategy,
            RevenueProfitStrategy, ChipConcentrationStrategy, SocialSecurityStrategy,
            OversoldReboundStrategy, ResonanceStrategy
        )
        
        strategy_classes = [
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
        
        optimized_strategies = {}
        total_signals = 0
        
        print("3. 策略优化与测试:")
        print("-" * 40)
        
        for name, strategy_class in strategy_classes:
            if strategy_class is None:
                print(f"  {name}: 策略类未找到")
                continue
            
            try:
                # 创建优化策略
                strategy = StrategyOptimizer.create_optimized_strategy(strategy_class, name)
                
                # 生成信号
                signals = strategy.generate_signals(
                    market_data=market_data,
                    fundamental_data=fundamental_data
                )
                
                optimized_strategies[name] = strategy
                
                # 统计信号
                buy_signals = [s for s in signals if s.get('side') == 'BUY']
                sell_signals = [s for s in signals if s.get('side') == 'SELL']
                hold_signals = [s for s in signals if s.get('side') == 'HOLD']
                
                total_signals += len(signals)
                
                print(f"  {name}: 总信号={len(signals)}, "
                      f"买入={len(buy_signals)}, 卖出={len(sell_signals)}, 持有={len(hold_signals)}")
                
                # 显示前2个信号
                if signals:
                    for i, signal in enumerate(signals[:2]):
                        print(f"    {signal.get('symbol')} {signal.get('side')} "
                              f"@{signal.get('price', 0):.2f}")
            
            except Exception as e:
                print(f"  {name}: 初始化失败 - {e}")
        
        # 4. 测试自适应引擎
        print("\n4. 自适应引擎测试:")
        print("-" * 40)
        
        try:
            from core.adaptive_engine import AdaptiveEngine
            
            # 创建自适应引擎
            adaptive_engine = AdaptiveEngine()
            
            # 分析市场状态
            market_state = adaptive_engine.analyze_market_state(market_data)
            print(f"  市场状态: {market_state.get('state_name', '未知')}")
            print(f"  置信度: {market_state.get('confidence', 0):.2f}")
            print(f"  建议策略权重调整:")
            
            # 获取策略调整建议
            strategy_weights = adaptive_engine.get_strategy_weights(
                list(optimized_strategies.keys()),
                market_state
            )
            
            for strategy_name, weight in strategy_weights.items():
                if strategy_name in optimized_strategies:
                    old_weight = optimized_strategies[strategy_name].weight
                    print(f"    {strategy_name}: {old_weight:.2f} -> {weight:.2f}")
        
        except Exception as e:
            print(f"  自适应引擎测试失败: {e}")
        
        # 5. 总体统计
        print("\n5. 总体统计:")
        print("-" * 40)
        print(f"  总策略数: {len(optimized_strategies)}")
        print(f"  总信号数: {total_signals}")
        print(f"  测试股票: {len(market_data)}只")
        print(f"  数据更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # 6. 生成交易建议
        print("\n6. 综合交易建议:")
        print("-" * 40)
        
        # 收集所有买入信号
        all_signals = []
        for strategy_name, strategy in optimized_strategies.items():
            signals = strategy.generate_signals(market_data, fundamental_data)
            for signal in signals:
                if signal.get('side') == 'BUY':
                    signal['strategy'] = strategy_name
                    all_signals.append(signal)
        
        # 按置信度排序
        all_signals.sort(key=lambda x: x.get('confidence', 0), reverse=True)
        
        if all_signals:
            print(f"  推荐买入股票 (前5只):")
            for i, signal in enumerate(all_signals[:5]):
                print(f"    {i+1}. {signal.get('symbol')} @{signal.get('price', 0):.2f} "
                      f"({signal.get('strategy', '未知')}) - 置信度: {signal.get('confidence', 0):.2f}")
        else:
            print("  暂无推荐买入股票")
        
        return True
    
    except Exception as e:
        print(f"系统测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def simulate_trading(days: int = 30):
    """模拟交易"""
    print("\n" + "=" * 60)
    print(f"A股交易模拟 - {days}天")
    print("=" * 60)
    
    try:
        # 这里可以添加模拟交易逻辑
        print("模拟交易功能待实现...")
        print("将包括:")
        print("  1. 每日调仓")
        print("  2. 策略权重动态调整")
        print("  3. 绩效跟踪")
        print("  4. 风险监控")
        
        return True
    except Exception as e:
        print(f"模拟交易失败: {e}")
        return False


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='A股核心交易框架优化版')
    parser.add_argument('action', choices=['test', 'simulate', 'optimize'],
                       help='执行动作: test-测试系统, simulate-模拟交易, optimize-策略优化')
    parser.add_argument('--days', type=int, default=30, help='模拟交易天数')
    
    args = parser.parse_args()
    
    if args.action == 'test':
        success = test_optimized_system()
        if success:
            print("\n" + "=" * 60)
            print("✅ 优化版系统测试成功!")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ 优化版系统测试失败!")
            print("=" * 60)
            sys.exit(1)
    
    elif args.action == 'simulate':
        success = simulate_trading(args.days)
        if success:
            print("\n模拟交易完成!")
        else:
            print("\n模拟交易失败!")
            sys.exit(1)
    
    elif args.action == 'optimize':
        print("策略优化功能待实现...")
        # 可以添加策略参数优化功能


if __name__ == "__main__":
    main()