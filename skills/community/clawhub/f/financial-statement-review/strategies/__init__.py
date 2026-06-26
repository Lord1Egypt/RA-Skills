"""
策略库模块 - 财务报表审查策略集合

策略库用于存放各种专门的审查策略，每个策略实现特定的审查逻辑。
策略可以通过继承 BaseStrategy 基类来实现，并通过 StrategyManager 进行管理。

使用示例：
    from strategies import StrategyManager
    
    manager = StrategyManager()
    manager.load_all_strategies()
    
    # 执行特定策略
    result = manager.execute_strategy('tax_reconciliation', data)
    
    # 执行所有策略
    all_results = manager.execute_all(data)
"""

from .base_strategy import BaseStrategy, StrategyResult
from .strategy_manager import StrategyManager

__all__ = ['BaseStrategy', 'StrategyResult', 'StrategyManager']
