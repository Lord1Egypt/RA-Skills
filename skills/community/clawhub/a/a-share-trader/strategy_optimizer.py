#!/usr/bin/env python3
"""
策略优化器 - 调整策略参数以适配模拟数据
"""
import logging
from typing import Dict, List, Any
import json

logger = logging.getLogger(__name__)


class StrategyOptimizer:
    """策略优化器"""
    
    @staticmethod
    def get_optimized_config_for_mock_data() -> Dict[str, Dict[str, Any]]:
        """
        获取针对模拟数据优化的策略配置
        
        模拟数据的特点是：
        1. 数值范围有限
        2. 分布可能不均匀
        3. 缺少真实数据的复杂特征
        
        返回: 策略配置字典
        """
        config = {
            "fundamental": {
                "enabled": True,
                "weight": 0.15,
                "min_market_cap": 100000000,  # 降低市值要求
                "min_profit_growth": 0.10,    # 降低增长要求
                "min_revenue_growth": 0.10,   # 降低增长要求
                "pe_max": 80.0,               # 放宽PE限制
                "pb_max": 8.0,                # 放宽PB限制
                "holding_count": 5,           # 减少持仓数
                "rebalance_days": 5
            },
            "defensive": {
                "enabled": True,
                "weight": 0.12,
                "min_dividend_yield": 0.02,   # 降低股息率要求
                "max_price": 50.0,            # 提高价格上限
                "holding_count": 3,
                "rebalance_days": 5
            },
            "swing_trading": {
                "enabled": True,
                "weight": 0.10,
                "buy_threshold": 30,          # 提高买入阈值
                "sell_threshold": 70,         # 降低卖出阈值
                "initial_position": 0.8,
                "rebalance_freq": "daily"
            },
            "small_cap": {
                "enabled": True,
                "weight": 0.08,
                "min_market_cap": 50000000,   # 降低市值要求
                "initial_screen": 15,         # 减少初始筛选
                "final_screen": 8,            # 减少最终筛选
                "rebalance_days": 5
            },
            "quality_small_cap": {
                "enabled": True,
                "weight": 0.08,
                "min_dividend_yield": 0.01,   # 大幅降低股息率要求
                "min_profit_growth": 0.05,    # 大幅降低增长要求
                "min_roe": 0.08,              # 大幅降低ROE要求
                "min_gross_margin": 0.15,     # 大幅降低毛利率要求
                "max_pe_ttm": 40.0,           # 放宽PE限制
                "holding_count": 5,
                "rebalance_days": 14
            },
            "small_cap_growth": {
                "enabled": True,
                "weight": 0.08,
                "max_market_cap": 50000000000, # 大幅提高市值上限
                "min_listing_days": 180,       # 降低上市天数要求
                "min_pe_ttm": 0.01,            # 极低PE要求
                "holding_count": 8,            # 减少持仓数
                "rebalance_days": 3
            },
            "revenue_profit": {
                "enabled": True,
                "weight": 0.10,
                "min_profit_growth": 0.10,     # 大幅降低增长要求
                "min_revenue_growth": 0.10,    # 大幅降低增长要求
                "pe_max": 80.0,                # 放宽PE限制
                "pb_max": 10.0,                # 放宽PB限制
                "holding_count": 8,            # 减少持仓数
                "rebalance_days": 5
            },
            "chip_concentration": {
                "enabled": True,
                "weight": 0.07,
                "max_chip_concentration": 0.20, # 提高筹码集中度上限
                "max_stocks": 15,               # 减少股票数
                "rebalance_days": 5
            },
            "social_security": {
                "enabled": True,
                "weight": 0.07,
                "min_market_cap": 500000000,    # 降低市值要求
                "holding_count": 6,             # 减少持仓数
                "rebalance_days": 10
            },
            "oversold_rebound": {
                "enabled": True,
                "weight": 0.08,
                "min_profit_growth": 0.30,      # 降低增长要求
                "holding_count": 4,             # 减少持仓数
                "rebalance_days": 1
            },
            "resonance": {
                "enabled": True,
                "weight": 0.07,
                "holding_count": 10,            # 减少持仓数
                "rebalance_days": 10
            }
        }
        
        return config
    
    @staticmethod
    def optimize_strategy_instance(strategy, strategy_name: str):
        """
        优化策略实例参数
        
        Args:
            strategy: 策略实例
            strategy_name: 策略名称
        """
        if not hasattr(strategy, 'parameters'):
            return
        
        optimized_config = StrategyOptimizer.get_optimized_config_for_mock_data()
        strategy_config = optimized_config.get(strategy_name, {})
        
        if strategy_config:
            # 更新策略参数
            for key, value in strategy_config.items():
                if key in strategy.parameters:
                    old_value = strategy.parameters[key]
                    strategy.parameters[key] = value
                    logger.debug(f"策略 {strategy_name}: {key} = {old_value} -> {value}")
    
    @staticmethod
    def create_optimized_strategy(strategy_class, strategy_name: str, **kwargs):
        """
        创建优化后的策略实例
        
        Args:
            strategy_class: 策略类
            strategy_name: 策略名称
            **kwargs: 其他参数
            
        Returns:
            策略实例
        """
        optimized_config = StrategyOptimizer.get_optimized_config_for_mock_data()
        strategy_config = optimized_config.get(strategy_name, {})
        
        # 合并配置
        merged_config = {**strategy_config, **kwargs}
        
        try:
            strategy = strategy_class(**merged_config)
            logger.info(f"创建优化策略: {strategy_name}")
            return strategy
        except Exception as e:
            logger.error(f"创建策略 {strategy_name} 失败: {e}")
            # 使用默认参数
            return strategy_class(**kwargs)
    
    @staticmethod
    def test_strategy_with_optimization(strategy_name: str, strategy_class, 
                                      market_data: Dict, fundamental_data: Dict) -> Dict[str, Any]:
        """
        测试优化后的策略
        
        Returns:
            测试结果
        """
        result = {
            "strategy": strategy_name,
            "original_signals": 0,
            "optimized_signals": 0,
            "improvement": 0,
            "success": False
        }
        
        try:
            # 创建原始策略
            original_strategy = strategy_class()
            original_signals = original_strategy.generate_signals(
                market_data=market_data,
                fundamental_data=fundamental_data
            )
            result["original_signals"] = len(original_signals)
            
            # 创建优化策略
            optimized_strategy = StrategyOptimizer.create_optimized_strategy(
                strategy_class, strategy_name
            )
            optimized_signals = optimized_strategy.generate_signals(
                market_data=market_data,
                fundamental_data=fundamental_data
            )
            result["optimized_signals"] = len(optimized_signals)
            
            # 计算改进
            if result["original_signals"] > 0:
                improvement = ((result["optimized_signals"] - result["original_signals"]) / 
                             result["original_signals"]) * 100
            else:
                improvement = 100 if result["optimized_signals"] > 0 else 0
            
            result["improvement"] = round(improvement, 1)
            result["success"] = True
            
            # 记录信号详情
            if optimized_signals:
                result["sample_signals"] = [
                    {"symbol": s.get("symbol"), "side": s.get("side")} 
                    for s in optimized_signals[:3]
                ]
            
        except Exception as e:
            result["error"] = str(e)
        
        return result


if __name__ == "__main__":
    # 测试优化器
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("策略优化配置:")
    config = StrategyOptimizer.get_optimized_config_for_mock_data()
    
    for strategy_name, params in config.items():
        print(f"\n{strategy_name}:")
        for key, value in params.items():
            if isinstance(value, (int, float)):
                print(f"  {key}: {value}")
            elif isinstance(value, bool):
                print(f"  {key}: {value}")
    
    print("\n优化完成!")