"""
策略管理器 - 管理所有审查策略的加载和执行
"""
import os
import sys
import importlib
import inspect
from typing import Dict, List, Type, Any, Optional
from pathlib import Path

from .base_strategy import BaseStrategy, StrategyResult


class StrategyManager:
    """
    策略管理器
    
    负责策略的注册、加载、管理和执行。
    """
    
    def __init__(self, strategies_path: str = None):
        """
        初始化策略管理器
        
        Args:
            strategies_path: 策略文件所在路径，默认为当前目录
        """
        self.strategies: Dict[str, BaseStrategy] = {}
        self.strategy_classes: Dict[str, Type[BaseStrategy]] = {}
        
        if strategies_path is None:
            strategies_path = os.path.dirname(os.path.abspath(__file__))
        self.strategies_path = strategies_path
    
    def register_strategy(self, strategy_class: Type[BaseStrategy], config: Dict = None):
        """
        注册策略类
        
        Args:
            strategy_class: 策略类（继承自 BaseStrategy）
            config: 策略配置
        """
        if not issubclass(strategy_class, BaseStrategy):
            raise ValueError(f"策略类必须继承自 BaseStrategy: {strategy_class}")
        
        strategy_name = strategy_class.name
        self.strategy_classes[strategy_name] = strategy_class
        
        # 实例化策略
        self.strategies[strategy_name] = strategy_class(config)
    
    def unregister_strategy(self, strategy_name: str):
        """
        注销策略
        
        Args:
            strategy_name: 策略名称
        """
        if strategy_name in self.strategies:
            del self.strategies[strategy_name]
        if strategy_name in self.strategy_classes:
            del self.strategy_classes[strategy_name]
    
    def load_strategy_from_file(self, filename: str, config: Dict = None):
        """
        从文件加载策略
        
        Args:
            filename: 策略文件名（不含路径）
            config: 策略配置
        """
        # 移除 .py 后缀
        if filename.endswith('.py'):
            filename = filename[:-3]
        
        # 跳过非策略文件
        if filename.startswith('_'):
            return
        
        try:
            # 动态导入模块
            module_path = f"strategies.{filename}"
            if module_path in sys.modules:
                module = sys.modules[module_path]
                importlib.reload(module)
            else:
                module = importlib.import_module(module_path)
            
            # 查找模块中的策略类
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if (issubclass(obj, BaseStrategy) and 
                    obj is not BaseStrategy and 
                    hasattr(obj, 'name') and 
                    obj.name != 'base_strategy'):
                    self.register_strategy(obj, config)
                    print(f"  已加载策略: {obj.name} - {obj.description}")
                    
        except Exception as e:
            print(f"  加载策略文件 {filename} 失败: {e}")
    
    def load_all_strategies(self, config_map: Dict[str, Dict] = None):
        """
        加载所有策略
        
        Args:
            config_map: 策略配置映射，key为策略名，value为配置字典
        """
        print("开始加载策略...")
        config_map = config_map or {}
        
        # 扫描策略目录
        strategies_dir = Path(self.strategies_path)
        
        for file_path in strategies_dir.glob('*.py'):
            if file_path.name.startswith('_'):
                continue
            
            strategy_name = file_path.stem
            config = config_map.get(strategy_name, {})
            self.load_strategy_from_file(file_path.name, config)
        
        print(f"策略加载完成，共加载 {len(self.strategies)} 个策略")
    
    def get_strategy(self, strategy_name: str) -> Optional[BaseStrategy]:
        """
        获取策略实例
        
        Args:
            strategy_name: 策略名称
            
        Returns:
            策略实例或 None
        """
        return self.strategies.get(strategy_name)
    
    def get_all_strategies(self) -> Dict[str, BaseStrategy]:
        """
        获取所有策略
        
        Returns:
            策略名称到实例的映射
        """
        return self.strategies.copy()
    
    def list_strategies(self) -> List[Dict[str, Any]]:
        """
        列出所有策略信息
        
        Returns:
            策略信息列表
        """
        return [strategy.get_info() for strategy in self.strategies.values()]
    
    def execute_strategy(self, strategy_name: str, data: Dict[str, Any]) -> Optional[StrategyResult]:
        """
        执行指定策略
        
        Args:
            strategy_name: 策略名称
            data: 审查数据
            
        Returns:
            策略执行结果
        """
        strategy = self.get_strategy(strategy_name)
        if strategy is None:
            result = StrategyResult(
                strategy_name=strategy_name,
                strategy_description='未知策略',
                status='failed'
            )
            result.add_finding('策略不存在', f'未找到策略: {strategy_name}', 'high')
            return result
        
        return strategy.run(data)
    
    def execute_all(self, data: Dict[str, Any], 
                    tax_type_filter: str = None) -> Dict[str, StrategyResult]:
        """
        执行所有策略
        
        Args:
            data: 审查数据
            tax_type_filter: 按税种过滤，如 '增值税'、'企业所得税'等
            
        Returns:
            策略名称到执行结果的映射
        """
        results = {}
        
        # 按优先级排序
        sorted_strategies = sorted(
            self.strategies.items(),
            key=lambda x: x[1].priority
        )
        
        for name, strategy in sorted_strategies:
            # 税种过滤
            if tax_type_filter and tax_type_filter not in strategy.applicable_tax_types:
                continue
            
            print(f"  执行策略: {name}...")
            result = strategy.run(data)
            results[name] = result
        
        return results
    
    def execute_by_tax_type(self, data: Dict[str, Any], tax_type: str) -> Dict[str, StrategyResult]:
        """
        执行指定税种相关的所有策略
        
        Args:
            data: 审查数据
            tax_type: 税种名称
            
        Returns:
            策略名称到执行结果的映射
        """
        return self.execute_all(data, tax_type_filter=tax_type)
    
    def generate_summary_report(self, results: Dict[str, StrategyResult]) -> str:
        """
        生成策略执行汇总报告
        
        Args:
            results: 策略执行结果
            
        Returns:
            汇总报告文本
        """
        lines = []
        lines.append("=" * 70)
        lines.append("策略执行汇总报告")
        lines.append("=" * 70)
        
        # 统计
        total = len(results)
        passed = sum(1 for r in results.values() if r.status == 'passed')
        warnings = sum(1 for r in results.values() if r.status == 'warning')
        failed = sum(1 for r in results.values() if r.status == 'failed')
        
        lines.append(f"\n执行统计:")
        lines.append(f"  总策略数: {total}")
        lines.append(f"  通过: {passed}")
        lines.append(f"  警告: {warnings}")
        lines.append(f"  失败: {failed}")
        
        # 详细结果
        if failed > 0:
            lines.append(f"\n【失败策略】")
            for name, result in results.items():
                if result.status == 'failed':
                    lines.append(f"  - {name}: {result.strategy_description}")
                    for finding in result.findings:
                        lines.append(f"    * [{finding['severity']}] {finding['type']}: {finding['description']}")
        
        if warnings > 0:
            lines.append(f"\n【警告策略】")
            for name, result in results.items():
                if result.status == 'warning':
                    lines.append(f"  - {name}: {result.strategy_description}")
        
        # 发现汇总
        all_findings = []
        for result in results.values():
            all_findings.extend(result.findings)
        
        if all_findings:
            high_risk = [f for f in all_findings if f['severity'] == 'high']
            medium_risk = [f for f in all_findings if f['severity'] == 'medium']
            
            lines.append(f"\n【风险发现汇总】")
            lines.append(f"  高风险发现: {len(high_risk)}项")
            lines.append(f"  中风险发现: {len(medium_risk)}项")
            
            if high_risk:
                lines.append(f"\n  高风险详情:")
                for finding in high_risk[:5]:  # 只显示前5条
                    lines.append(f"    - [{finding.get('tax_type', '通用')}] {finding['type']}")
                    lines.append(f"      {finding['description']}")
        
        lines.append("\n" + "=" * 70)
        return "\n".join(lines)


# 全局策略管理器实例
_default_manager = None


def get_strategy_manager() -> StrategyManager:
    """获取默认策略管理器实例"""
    global _default_manager
    if _default_manager is None:
        _default_manager = StrategyManager()
    return _default_manager
