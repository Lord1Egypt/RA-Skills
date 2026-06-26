"""
Exception Classifier - 异常类型智能识别与匹配引擎
遵循PRD 4.2节要求
"""

import re
import json
from typing import Optional, Dict, Any, Union
from enum import Enum


class ExceptionCategory(Enum):
    """异常分类枚举"""
    RETRYABLE = "retryable"          # 可重试异常
    NON_RETRYABLE = "non_retryable"  # 不可重试异常
    UNKNOWN = "unknown"              # 未知异常（谨慎重试）


class ExceptionClassifier:
    """
    异常类型智能识别与匹配引擎
    
    Features:
    - 自动识别可重试 vs 不可重试异常
    - 内置标准化异常分类规则库
    - 支持HTTP状态码识别
    - 支持自定义异常匹配规则
    """
    
    def __init__(self, config_manager=None):
        """
        初始化异常分类器
        
        Args:
            config_manager: 配置管理器实例
        """
        self.config = config_manager
        self._retryable_patterns = [
            r'connection.*error',
            r'timeout',
            r'rate.?limit',
            r'too.?many.?requests',
            r'service.?unavailable',
            r'temporaril(y|ily).?unavailable',
            r'internal.?server.?error',
            r'gateway.?timeout',
            r'dns.*error',
            r'network.*error',
            r'tcp.*error',
        ]
        
        self._non_retryable_patterns = [
            r'permission.*denied',
            r'unauthorized',
            r'forbidden',
            r'not.?found',
            r'bad.?request',
            r'invalid.*(param|argument)',
            r'missing.*(param|field)',
            r'account.*(banned|suspended|blocked)',
            r'compliance.*(violation|error)',
            r'quota.*exceeded',  # 配额超限通常不可重试
        ]
    
    def classify(self, exception: Union[Exception, str, Dict]) -> ExceptionCategory:
        """
        分类异常类型
        
        Args:
            exception: 异常对象、错误消息或错误信息字典
            
        Returns:
            ExceptionCategory: 异常分类
        """
        exception_info = self._extract_exception_info(exception)
        
        # 1. 检查配置规则
        if self.config:
            if self._match_config_rules(exception_info, 'non_retryable'):
                return ExceptionCategory.NON_RETRYABLE
            if self._match_config_rules(exception_info, 'retryable'):
                return ExceptionCategory.RETRYABLE
        
        # 2. 检查HTTP状态码
        status_code = exception_info.get('status_code')
        if status_code:
            category = self._classify_by_status_code(status_code)
            if category != ExceptionCategory.UNKNOWN:
                return category
        
        # 3. 检查错误码
        error_code = exception_info.get('error_code')
        if error_code:
            category = self._classify_by_error_code(str(error_code))
            if category != ExceptionCategory.UNKNOWN:
                return category
        
        # 4. 检查异常类型名称
        exception_type = exception_info.get('type', '')
        if self._is_retryable_type(exception_type):
            return ExceptionCategory.RETRYABLE
        if self._is_non_retryable_type(exception_type):
            return ExceptionCategory.NON_RETRYABLE
        
        # 5. 检查错误消息
        message = exception_info.get('message', '')
        if self._match_patterns(message, self._non_retryable_patterns):
            return ExceptionCategory.NON_RETRYABLE
        if self._match_patterns(message, self._retryable_patterns):
            return ExceptionCategory.RETRYABLE
        
        # 6. 未知异常 - 谨慎重试 (PRD 4.2节)
        return ExceptionCategory.UNKNOWN
    
    def is_retryable(self, exception: Union[Exception, str, Dict]) -> bool:
        """
        判断异常是否可重试
        
        Args:
            exception: 异常对象、错误消息或错误信息字典
            
        Returns:
            bool: 是否可重试
        """
        category = self.classify(exception)
        return category in (ExceptionCategory.RETRYABLE, ExceptionCategory.UNKNOWN)
    
    def is_non_retryable(self, exception: Union[Exception, str, Dict]) -> bool:
        """
        判断异常是否不可重试
        
        Args:
            exception: 异常对象、错误消息或错误信息字典
            
        Returns:
            bool: 是否不可重试
        """
        category = self.classify(exception)
        return category == ExceptionCategory.NON_RETRYABLE
    
    def _extract_exception_info(self, exception: Union[Exception, str, Dict]) -> Dict[str, Any]:
        """提取异常信息"""
        info = {
            'type': '',
            'message': '',
            'status_code': None,
            'error_code': None
        }
        
        if isinstance(exception, dict):
            info.update(exception)
        elif isinstance(exception, Exception):
            info['type'] = exception.__class__.__name__
            info['message'] = str(exception)
            
            # 尝试提取HTTP状态码
            if hasattr(exception, 'status_code'):
                info['status_code'] = exception.status_code
            elif hasattr(exception, 'code'):
                info['status_code'] = exception.code
            elif hasattr(exception, 'response') and hasattr(exception.response, 'status_code'):
                info['status_code'] = exception.response.status_code
                
        elif isinstance(exception, str):
            info['message'] = exception
            
        return info
    
    def _match_config_rules(self, exception_info: Dict, rule_type: str) -> bool:
        """匹配配置规则"""
        if not self.config:
            return False
            
        rules = self.config.get_exception_rules()
        rule_list = rules.retryable if rule_type == 'retryable' else rules.non_retryable
        
        # 检查异常类型名
        exc_type = exception_info.get('type', '')
        if exc_type in rule_list:
            return True
        
        # 检查状态码
        status_code = exception_info.get('status_code')
        if status_code and str(status_code) in rule_list:
            return True
        
        # 检查错误码
        error_code = exception_info.get('error_code')
        if error_code and str(error_code) in rule_list:
            return True
        
        return False
    
    def _classify_by_status_code(self, status_code: int) -> ExceptionCategory:
        """根据HTTP状态码分类"""
        # 可重试状态码
        if status_code in (429, 500, 502, 503, 504):
            return ExceptionCategory.RETRYABLE
        
        # 不可重试状态码
        if status_code in (400, 401, 403, 404, 405, 422):
            return ExceptionCategory.NON_RETRYABLE
        
        return ExceptionCategory.UNKNOWN
    
    def _classify_by_error_code(self, error_code: str) -> ExceptionCategory:
        """根据错误码分类"""
        # 可重试错误码
        retryable_codes = ['RATE_LIMIT', 'TIMEOUT', 'CONNECTION_ERROR', 'SERVER_ERROR']
        if any(code in error_code.upper() for code in retryable_codes):
            return ExceptionCategory.RETRYABLE
        
        # 不可重试错误码
        non_retryable_codes = ['INVALID_PARAM', 'PERMISSION_DENIED', 'NOT_FOUND', 'COMPLIANCE']
        if any(code in error_code.upper() for code in non_retryable_codes):
            return ExceptionCategory.NON_RETRYABLE
        
        return ExceptionCategory.UNKNOWN
    
    def _is_retryable_type(self, exception_type: str) -> bool:
        """检查异常类型是否可重试"""
        retryable_types = [
            'ConnectionError', 'TimeoutError', 'ConnectionTimeout',
            'RateLimitError', 'ServiceUnavailableError', 'ServerError',
            'DNSResolutionError', 'TCPConnectionError'
        ]
        return any(t.lower() in exception_type.lower() for t in retryable_types)
    
    def _is_non_retryable_type(self, exception_type: str) -> bool:
        """检查异常类型是否不可重试"""
        non_retryable_types = [
            'ValueError', 'TypeError', 'KeyError', 'PermissionError',
            'ComplianceError', 'AccountBannedError', 'ValidationError'
        ]
        return any(t.lower() in exception_type.lower() for t in non_retryable_types)
    
    def _match_patterns(self, text: str, patterns: list) -> bool:
        """检查文本是否匹配任一模式"""
        text_lower = text.lower()
        for pattern in patterns:
            if re.search(pattern, text_lower):
                return True
        return False
    
    def get_exception_details(self, exception: Union[Exception, str, Dict]) -> Dict[str, Any]:
        """
        获取异常的详细分析结果
        
        Args:
            exception: 异常对象、错误消息或错误信息字典
            
        Returns:
            Dict: 包含分类结果、处理建议等详细信息
        """
        info = self._extract_exception_info(exception)
        category = self.classify(exception)
        is_retryable = category in (ExceptionCategory.RETRYABLE, ExceptionCategory.UNKNOWN)
        
        details = {
            'exception_type': info.get('type', 'Unknown'),
            'message': info.get('message', ''),
            'status_code': info.get('status_code'),
            'category': category.value,
            'is_retryable': is_retryable,
            'is_non_retryable': category == ExceptionCategory.NON_RETRYABLE,
            'recommendation': self._get_recommendation(category)
        }
        
        return details
    
    def _get_recommendation(self, category: ExceptionCategory) -> str:
        """获取处理建议"""
        recommendations = {
            ExceptionCategory.RETRYABLE: "该异常为临时性问题，建议执行重试策略",
            ExceptionCategory.NON_RETRYABLE: "该异常无法通过重试解决，建议终止任务并检查参数/权限",
            ExceptionCategory.UNKNOWN: "异常类型未知，建议谨慎重试（最多2次）并记录异常特征"
        }
        return recommendations.get(category, "请人工检查异常原因")