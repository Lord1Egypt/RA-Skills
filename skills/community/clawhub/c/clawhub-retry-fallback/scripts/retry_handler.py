"""
Retry Handler - 全局重试策略配置中心
遵循PRD 4.1节要求
"""

import time
import random
import functools
from typing import Callable, Optional, Any, Type, Tuple, List, Dict
from dataclasses import dataclass, field

from .exception_classifier import ExceptionClassifier, ExceptionCategory
from .config_manager import ConfigManager, RetryPolicy


@dataclass
class RetryResult:
    """重试执行结果"""
    success: bool
    result: Any = None
    exception: Optional[Exception] = None
    attempts: int = 0
    total_duration: float = 0.0
    retry_history: List[Dict] = field(default_factory=list)


class RetryHandler:
    """
    全局重试策略配置中心 - 核心重试处理器
    
    Features:
    - 支持指数退避、固定间隔、自定义间隔策略
    - 自动识别可重试/不可重试异常
    - 支持装饰器和上下文管理器两种使用方式
    - 完整的重试历史记录
    """
    
    def __init__(self, config_manager: Optional[ConfigManager] = None):
        """
        初始化重试处理器
        
        Args:
            config_manager: 配置管理器实例
        """
        self.config = config_manager or ConfigManager()
        self.classifier = ExceptionClassifier(self.config)
        self._retry_stats = {
            'total_attempts': 0,
            'successful_retries': 0,
            'failed_retries': 0
        }
    
    def with_retry(
        self,
        max_attempts: Optional[int] = None,
        backoff_strategy: str = 'exponential',
        delays: Optional[List[float]] = None,
        fixed_delay: float = 3.0,
        max_total_duration: float = 300.0,
        retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
        on_retry: Optional[Callable] = None,
        on_failure: Optional[Callable] = None
    ):
        """
        装饰器：为函数添加重试能力
        
        Args:
            max_attempts: 最大重试次数，默认从配置读取
            backoff_strategy: 退避策略 (exponential/fixed/custom)
            delays: 自定义重试间隔列表
            fixed_delay: 固定间隔时长(秒)
            max_total_duration: 最大总重试时长(秒)
            retryable_exceptions: 指定可重试的异常类型
            on_retry: 每次重试时的回调函数
            on_failure: 最终失败时的回调函数
            
        Returns:
            Callable: 装饰后的函数
        """
        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return self.execute_with_retry(
                    func=func,
                    args=args,
                    kwargs=kwargs,
                    max_attempts=max_attempts,
                    backoff_strategy=backoff_strategy,
                    delays=delays,
                    fixed_delay=fixed_delay,
                    max_total_duration=max_total_duration,
                    retryable_exceptions=retryable_exceptions,
                    on_retry=on_retry,
                    on_failure=on_failure
                )
            return wrapper
        return decorator
    
    def execute_with_retry(
        self,
        func: Callable,
        args: Optional[tuple] = None,
        kwargs: Optional[dict] = None,
        max_attempts: Optional[int] = None,
        backoff_strategy: str = 'exponential',
        delays: Optional[List[float]] = None,
        fixed_delay: float = 3.0,
        max_total_duration: float = 300.0,
        retryable_exceptions: Optional[Tuple[Type[Exception], ...]] = None,
        on_retry: Optional[Callable] = None,
        on_failure: Optional[Callable] = None
    ) -> RetryResult:
        """
        执行函数并在失败时自动重试
        
        Args:
            func: 要执行的函数
            args: 函数位置参数
            kwargs: 函数关键字参数
            max_attempts: 最大重试次数
            backoff_strategy: 退避策略
            delays: 自定义重试间隔
            fixed_delay: 固定间隔时长
            max_total_duration: 最大总重试时长
            retryable_exceptions: 指定可重试的异常类型
            on_retry: 重试回调
            on_failure: 失败回调
            
        Returns:
            RetryResult: 包含执行结果和重试历史
        """
        args = args or ()
        kwargs = kwargs or {}
        
        # 使用默认值
        if max_attempts is None:
            max_attempts = 3
        
        # 应用平台限制
        max_attempts = min(max_attempts, self.config.PLATFORM_LIMITS['max_retry_attempts'])
        
        start_time = time.time()
        retry_history = []
        last_exception = None
        
        for attempt in range(1, max_attempts + 1):
            try:
                result = func(*args, **kwargs)
                
                # 成功
                total_duration = time.time() - start_time
                self._retry_stats['total_attempts'] += attempt
                self._retry_stats['successful_retries'] += attempt - 1
                
                return RetryResult(
                    success=True,
                    result=result,
                    attempts=attempt,
                    total_duration=total_duration,
                    retry_history=retry_history
                )
                
            except Exception as e:
                last_exception = e
                total_duration = time.time() - start_time
                
                # 检查是否超过总时长限制
                if total_duration >= max_total_duration:
                    break
                
                # 分类异常
                category = self.classifier.classify(e)
                
                # 不可重试异常直接终止
                if category == ExceptionCategory.NON_RETRYABLE:
                    if on_failure:
                        on_failure(e, attempt, max_attempts)
                    break
                
                # 记录重试历史
                retry_record = {
                    'attempt': attempt,
                    'exception_type': e.__class__.__name__,
                    'exception_message': str(e),
                    'timestamp': time.time(),
                    'category': category.value
                }
                retry_history.append(retry_record)
                
                # 最后一次尝试，不再重试
                if attempt >= max_attempts:
                    break
                
                # 计算重试间隔
                delay = self._calculate_delay(
                    attempt=attempt,
                    strategy=backoff_strategy,
                    delays=delays,
                    fixed_delay=fixed_delay
                )
                
                # 执行回调
                if on_retry:
                    on_retry(e, attempt, delay)
                
                # 等待后重试
                time.sleep(delay)
        
        # 最终失败
        self._retry_stats['total_attempts'] += len(retry_history)
        self._retry_stats['failed_retries'] += len(retry_history)
        
        if on_failure and last_exception:
            on_failure(last_exception, len(retry_history) + 1, max_attempts)
        
        total_duration = time.time() - start_time
        
        return RetryResult(
            success=False,
            exception=last_exception,
            attempts=len(retry_history) + 1,
            total_duration=total_duration,
            retry_history=retry_history
        )
    
    def _calculate_delay(
        self,
        attempt: int,
        strategy: str,
        delays: Optional[List[float]],
        fixed_delay: float
    ) -> float:
        """
        计算重试间隔
        
        Args:
            attempt: 当前尝试次数(从1开始)
            strategy: 退避策略
            delays: 自定义间隔列表
            fixed_delay: 固定间隔
            
        Returns:
            float: 等待时长(秒)
        """
        if strategy == 'custom' and delays:
            # 使用自定义间隔
            idx = min(attempt - 1, len(delays) - 1)
            delay = delays[idx]
        elif strategy == 'exponential':
            # 指数退避: 2^(attempt-1) + jitter
            base = 2 ** (attempt - 1)
            jitter = random.uniform(0, 0.5)
            delay = base + jitter
        else:
            # 固定间隔
            delay = fixed_delay
        
        # 应用平台限制
        delay = max(delay, self.config.PLATFORM_LIMITS['min_delay'])
        delay = min(delay, self.config.PLATFORM_LIMITS['max_delay'])
        
        return delay
    
    def get_stats(self) -> Dict[str, int]:
        """获取重试统计信息"""
        return self._retry_stats.copy()
    
    def reset_stats(self):
        """重置统计信息"""
        self._retry_stats = {
            'total_attempts': 0,
            'successful_retries': 0,
            'failed_retries': 0
        }