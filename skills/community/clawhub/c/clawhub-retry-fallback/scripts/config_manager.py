"""
Configuration Manager - 配置管理器
管理重试策略、异常规则等配置
"""

import os
import yaml
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field


@dataclass
class RetryPolicy:
    """重试策略配置"""
    max_attempts: int = 3
    backoff_strategy: str = 'exponential'  # exponential, fixed, custom
    delays: List[float] = field(default_factory=lambda: [1.0, 3.0, 5.0])
    fixed_delay: float = 3.0
    max_total_duration: float = 300.0  # 最大总重试时长(秒)


@dataclass
class ExceptionRule:
    """异常分类规则"""
    retryable: List[str] = field(default_factory=list)
    non_retryable: List[str] = field(default_factory=list)


class ConfigManager:
    """
    配置管理器 - 管理所有重试和降级相关的配置
    
    Features:
    - 加载和管理重试策略配置
    - 管理异常分类规则
    - 支持热更新配置
    - 企业级策略组管理
    """
    
    # 平台默认重试策略 (遵循PRD 4.1节)
    DEFAULT_POLICIES = {
        'network_timeout': RetryPolicy(
            max_attempts=3,
            backoff_strategy='exponential',
            delays=[1.0, 3.0, 5.0]
        ),
        'rate_limit': RetryPolicy(
            max_attempts=5,
            backoff_strategy='exponential',
            delays=[2.0, 5.0, 10.0, 30.0, 60.0]
        ),
        'server_error': RetryPolicy(
            max_attempts=3,
            backoff_strategy='fixed',
            fixed_delay=3.0
        )
    }
    
    # 默认异常分类规则 (遵循PRD 4.2节)
    DEFAULT_EXCEPTION_RULES = ExceptionRule(
        retryable=[
            'ConnectionError',
            'TimeoutError', 
            'ConnectionTimeout',
            'RateLimitError',
            'ServiceUnavailableError',
            '429',
            '503',
            '5xx'
        ],
        non_retryable=[
            'ValueError',
            'TypeError',
            'KeyError',
            'PermissionError',
            'ComplianceError',
            'AccountBannedError',
            '400',
            '401',
            '403',
            '404'
        ]
    )
    
    # 平台强制限制
    PLATFORM_LIMITS = {
        'max_retry_attempts': 10,  # 最高重试次数上限
        'max_switch_attempts': 2,  # 备用工具切换次数上限
        'min_delay': 0.5,  # 最小重试间隔
        'max_delay': 300.0  # 最大重试间隔
    }
    
    def __init__(self, config_path: Optional[str] = None):
        """
        初始化配置管理器
        
        Args:
            config_path: 配置文件路径，默认使用内置配置
        """
        self.config_path = config_path or self._get_default_config_path()
        self._policies = {}
        self._exception_rules = None
        self._user_policies = {}
        self._load_config()
    
    def _get_default_config_path(self) -> str:
        """获取默认配置文件路径"""
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_dir, 'config', 'retry_policies.yaml')
    
    def _load_config(self):
        """加载配置文件"""
        # 先加载默认配置
        self._policies = self.DEFAULT_POLICIES.copy()
        self._exception_rules = self.DEFAULT_EXCEPTION_RULES
        
        # 尝试加载用户自定义配置
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    user_config = yaml.safe_load(f)
                
                if user_config:
                    # 加载用户策略
                    if 'user_policies' in user_config:
                        for name, policy_data in user_config['user_policies'].items():
                            self._user_policies[name] = self._parse_policy(policy_data)
                    
                    # 加载异常规则
                    if 'exception_rules' in user_config:
                        rules = user_config['exception_rules']
                        if 'retryable' in rules:
                            self._exception_rules.retryable.extend(rules['retryable'])
                        if 'non_retryable' in rules:
                            self._exception_rules.non_retryable.extend(rules['non_retryable'])
                            
            except Exception as e:
                print(f"Warning: Failed to load config from {self.config_path}: {e}")
                print("Using default configuration.")
    
    def _parse_policy(self, data: Dict[str, Any]) -> RetryPolicy:
        """解析策略配置数据"""
        # 应用平台强制限制
        max_attempts = min(
            data.get('max_attempts', 3),
            self.PLATFORM_LIMITS['max_retry_attempts']
        )
        
        policy = RetryPolicy(
            max_attempts=max_attempts,
            backoff_strategy=data.get('backoff_strategy', 'exponential'),
            delays=data.get('delays', [1.0, 3.0, 5.0]),
            fixed_delay=data.get('delay', 3.0),
            max_total_duration=data.get('max_total_duration', 300.0)
        )
        return policy
    
    def get_policy(self, exception_type: str) -> RetryPolicy:
        """
        获取指定异常类型的重试策略
        
        Args:
            exception_type: 异常类型名称
            
        Returns:
            RetryPolicy: 对应的重试策略
        """
        # 优先匹配特定策略
        if exception_type in self._policies:
            return self._policies[exception_type]
        
        # 默认返回网络超时策略
        return self.DEFAULT_POLICIES['network_timeout']
    
    def get_user_policy(self, policy_name: str) -> Optional[RetryPolicy]:
        """
        获取用户自定义策略
        
        Args:
            policy_name: 策略名称
            
        Returns:
            RetryPolicy or None
        """
        return self._user_policies.get(policy_name)
    
    def get_exception_rules(self) -> ExceptionRule:
        """获取异常分类规则"""
        return self._exception_rules
    
    def is_retryable_exception(self, exception_name: str) -> bool:
        """
        判断异常是否可重试
        
        Args:
            exception_name: 异常名称或错误码
            
        Returns:
            bool: 是否可重试
        """
        # 检查是否在不可重试列表
        if exception_name in self._exception_rules.non_retryable:
            return False
        
        # 检查是否在可重试列表
        if exception_name in self._exception_rules.retryable:
            return True
        
        # 检查通配符匹配 (如 '5xx' 匹配 '500', '502' 等)
        for pattern in self._exception_rules.retryable:
            if 'x' in pattern.lower():
                import re
                regex = pattern.lower().replace('x', r'\d')
                if re.match(f'^{regex}$', str(exception_name).lower()):
                    return True
        
        # 未知异常默认谨慎重试 (PRD 4.2节)
        return True
    
    def get_platform_limits(self) -> Dict[str, float]:
        """获取平台强制限制"""
        return self.PLATFORM_LIMITS.copy()
    
    def reload_config(self):
        """热更新配置"""
        self._load_config()
    
    def save_config(self, filepath: Optional[str] = None):
        """
        保存当前配置到文件
        
        Args:
            filepath: 保存路径，默认覆盖原配置
        """
        save_path = filepath or self.config_path
        
        config = {
            'user_policies': {},
            'exception_rules': {
                'retryable': self._exception_rules.retryable,
                'non_retryable': self._exception_rules.non_retryable
            }
        }
        
        for name, policy in self._user_policies.items():
            config['user_policies'][name] = {
                'max_attempts': policy.max_attempts,
                'backoff_strategy': policy.backoff_strategy,
                'delays': policy.delays,
                'max_total_duration': policy.max_total_duration
            }
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        with open(save_path, 'w', encoding='utf-8') as f:
            yaml.dump(config, f, allow_unicode=True, default_flow_style=False)