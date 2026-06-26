"""
策略基类模块 - 定义策略接口和通用功能
"""
from abc import ABC, abstractmethod
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class StrategyResult:
    """策略执行结果数据类"""
    strategy_name: str
    strategy_description: str
    status: str  # 'passed', 'warning', 'failed'
    findings: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    details: Dict[str, Any] = field(default_factory=dict)
    executed_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            'strategy_name': self.strategy_name,
            'strategy_description': self.strategy_description,
            'status': self.status,
            'findings': self.findings,
            'recommendations': self.recommendations,
            'details': self.details,
            'executed_at': self.executed_at
        }
    
    def add_finding(self, finding_type: str, description: str, 
                    severity: str = 'medium', amount: float = None,
                    tax_type: str = None, regulation: str = None):
        """添加发现的问题"""
        finding = {
            'type': finding_type,
            'description': description,
            'severity': severity,  # 'high', 'medium', 'low'
            'tax_type': tax_type,
            'regulation': regulation
        }
        if amount is not None:
            finding['amount'] = amount
        self.findings.append(finding)
        
        # 根据严重程度更新状态
        if severity == 'high' and self.status != 'failed':
            self.status = 'failed'
        elif severity == 'medium' and self.status == 'passed':
            self.status = 'warning'
    
    def add_recommendation(self, recommendation: str):
        """添加改进建议"""
        self.recommendations.append(recommendation)


class BaseStrategy(ABC):
    """
    策略基类
    
    所有审查策略应继承此类，并实现 execute 方法。
    """
    
    # 策略元数据
    name: str = "base_strategy"
    description: str = "策略基类"
    version: str = "1.0.0"
    author: str = ""
    applicable_tax_types: List[str] = []  # 适用的税种
    required_data_fields: List[str] = []  # 必需的数据字段
    
    def __init__(self, config: Dict[str, Any] = None):
        """
        初始化策略
        
        Args:
            config: 策略配置参数
        """
        self.config = config or {}
        self.enabled = self.config.get('enabled', True)
        self.priority = self.config.get('priority', 50)  # 执行优先级，数字越小优先级越高
    
    @abstractmethod
    def execute(self, data: Dict[str, Any]) -> StrategyResult:
        """
        执行策略
        
        Args:
            data: 审查所需数据，包括财务报表、税务申报表等
            
        Returns:
            StrategyResult: 策略执行结果
        """
        pass
    
    def validate_data(self, data: Dict[str, Any]) -> tuple[bool, str]:
        """
        验证输入数据是否满足策略执行要求
        
        Args:
            data: 输入数据
            
        Returns:
            (是否有效, 错误信息)
        """
        missing_fields = []
        for field in self.required_data_fields:
            if field not in data or data[field] is None:
                missing_fields.append(field)
        
        if missing_fields:
            return False, f"缺少必需字段: {', '.join(missing_fields)}"
        return True, ""
    
    def pre_execute(self, data: Dict[str, Any]) -> StrategyResult:
        """
        执行前处理，包括数据验证
        
        Returns:
            如果验证失败返回错误结果，否则返回 None
        """
        is_valid, error_msg = self.validate_data(data)
        if not is_valid:
            result = StrategyResult(
                strategy_name=self.name,
                strategy_description=self.description,
                status='failed'
            )
            result.add_finding('数据验证失败', error_msg, 'high')
            return result
        return None
    
    def run(self, data: Dict[str, Any]) -> StrategyResult:
        """
        运行策略（包含前置处理和执行）
        
        Args:
            data: 审查数据
            
        Returns:
            StrategyResult: 执行结果
        """
        # 检查策略是否启用
        if not self.enabled:
            return StrategyResult(
                strategy_name=self.name,
                strategy_description=self.description,
                status='passed',
                details={'message': '策略已禁用'}
            )
        
        # 前置验证
        pre_result = self.pre_execute(data)
        if pre_result is not None:
            return pre_result
        
        # 执行策略
        try:
            result = self.execute(data)
            return result
        except Exception as e:
            result = StrategyResult(
                strategy_name=self.name,
                strategy_description=self.description,
                status='failed'
            )
            result.add_finding('执行异常', f'策略执行过程中发生错误: {str(e)}', 'high')
            return result
    
    def get_info(self) -> Dict[str, Any]:
        """获取策略信息"""
        return {
            'name': self.name,
            'description': self.description,
            'version': self.version,
            'author': self.author,
            'applicable_tax_types': self.applicable_tax_types,
            'required_data_fields': self.required_data_fields,
            'enabled': self.enabled,
            'priority': self.priority
        }
