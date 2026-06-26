"""
Retry & Timeout Strategy
P0: Exponential backoff, circuit breaker pattern
"""
import time
import functools
from typing import Callable, Any, Optional, Type, Tuple
from datetime import datetime, timezone

# Configuration
REQUEST_TIMEOUT_SEC = 20
MAX_RETRY = 3
RETRY_BACKOFF_SEC = 0.5


class RetryStrategy:
    """重试策略"""
    
    @staticmethod
    def exponential_backoff(attempt: int, base_delay: float = RETRY_BACKOFF_SEC, max_delay: float = 30.0) -> float:
        """
        指数退避算法
        delay = base_delay * (2 ^ attempt) + random(0, 1)
        """
        import random
        delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
        return delay
    
    @staticmethod
    def should_retry(exception: Exception, retryable_exceptions: Tuple[Type, ...]) -> bool:
        """判断是否应该重试"""
        return isinstance(exception, retryable_exceptions)


def with_retry(
    max_attempts: int = MAX_RETRY,
    timeout: int = REQUEST_TIMEOUT_SEC,
    backoff_base: float = RETRY_BACKOFF_SEC,
    retryable: Tuple[Type, ...] = (ConnectionError, TimeoutError, OSError)
):
    """
    重试装饰器
    
    Args:
        max_attempts: 最大尝试次数
        timeout: 超时时间（秒）
        backoff_base: 退避基数
        retryable: 可重试的异常类型
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                    
                except RetryStrategy.should_retry(type(last_exception), retryable) if last_exception else True:
                    last_exception = e
                    
                    if attempt < max_attempts - 1:
                        delay = RetryStrategy.exponential_backoff(attempt, backoff_base)
                        time.sleep(delay)
                        
                        # 记录重试日志
                        from observability import get_logger, get_metrics
                        logger = get_logger()
                        metrics = get_metrics()
                        logger.warning(
                            f"Retrying {func.__name__} (attempt {attempt + 1}/{max_attempts}) after {delay:.2f}s",
                            attempt=attempt + 1,
                            max_attempts=max_attempts,
                            delay=delay,
                            error=str(e)
                        )
                        metrics.increment("retry.count", tags={"function": func.__name__, "attempt": str(attempt + 1)})
                    else:
                        # 最终失败
                        from observability import get_alerts
                        alerts = get_alerts()
                        alerts.send(
                            alert_name="retry_exhausted",
                            level="error",
                            message=f"Failed after {max_attempts} attempts: {func.__name__}",
                            cooldown_sec=300
                        )
            
            raise last_exception
                
        return wrapper
    return decorator


def with_timeout(seconds: int = REQUEST_TIMEOUT_SEC):
    """
    超时装饰器（基于 signal，不支持 Windows）
    """
    import signal
    
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            def timeout_handler(signum, frame):
                raise TimeoutError(f"Function {func.__name__} timed out after {seconds}s")
            
            # 设置超时
            old_handler = signal.signal(signal.SIGALRM, timeout_handler)
            signal.alarm(seconds)
            
            try:
                result = func(*args, **kwargs)
            finally:
                # 恢复原有 handler
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            
            return result
            
        return wrapper
    return decorator


class TimeoutContext:
    """超时上下文管理器（跨平台）"""
    
    def __init__(self, seconds: int = REQUEST_TIMEOUT_SEC):
        self.seconds = seconds
        self.start_time = None
    
    def __enter__(self):
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        if elapsed > self.seconds:
            raise TimeoutError(f"Operation took {elapsed:.2f}s, expected {self.seconds}s")
        return False
    
    def elapsed(self) -> float:
        return time.time() - self.start_time if self.start_time else 0


def retry_call(func: Callable, *args, 
               max_attempts: int = MAX_RETRY,
               timeout: int = REQUEST_TIMEOUT_SEC,
               **kwargs) -> Any:
    """
    带重试和超时的函数调用
    """
    last_exception = None
    
    for attempt in range(max_attempts):
        try:
            with TimeoutContext(seconds=timeout):
                return func(*args, **kwargs)
                
        except TimeoutError as e:
            last_exception = e
            if attempt < max_attempts - 1:
                delay = RetryStrategy.exponential_backoff(attempt)
                time.sleep(delay)
                
        except Exception as e:
            last_exception = e
            if not RetryStrategy.should_retry(e, (ConnectionError, TimeoutError, OSError, Exception)):
                raise
            
            if attempt < max_attempts - 1:
                delay = RetryStrategy.exponential_backoff(attempt)
                time.sleep(delay)
    
    raise last_exception
