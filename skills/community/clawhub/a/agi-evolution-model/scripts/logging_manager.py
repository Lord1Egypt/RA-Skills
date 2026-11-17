"""
统一日志管理模块

提供统一的日志记录接口，支持结构化日志和trace_id追踪。

版本: 1.0.0
作者: AGI Evolution Team
"""

__version__ = '1.0.0'
__author__ = 'AGI Evolution Team'

import logging
import json
import os
from typing import Any, Dict, Optional
from datetime import datetime
import uuid
from interfaces import TraceContext, ValidationResult, create_trace_context


class StructuredLogger:
    """结构化日志记录器"""
    
    def __init__(
        self,
        name: str,
        level: int = logging.INFO,
        log_dir: str = './agi_memory/logs',
        enable_file_log: bool = True,
        enable_console_log: bool = True
    ):
        """
        初始化日志记录器
        
        Args:
            name: 日志记录器名称
            level: 日志级别
            log_dir: 日志文件目录
            enable_file_log: 是否启用文件日志
            enable_console_log: 是否启用控制台日志
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        self.logger.propagate = False
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 控制台handler
            if enable_console_log:
                console_handler = logging.StreamHandler()
                console_handler.setLevel(level)
                console_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                console_handler.setFormatter(console_formatter)
                self.logger.addHandler(console_handler)
            
            # 文件handler
            if enable_file_log:
                os.makedirs(log_dir, exist_ok=True)
                log_file = os.path.join(log_dir, f'{name}.log')
                file_handler = logging.FileHandler(log_file, encoding='utf-8')
                file_handler.setLevel(level)
                file_formatter = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - [%(trace_id)s] - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
                file_handler.setFormatter(file_formatter)
                self.logger.addHandler(file_handler)
    
    def _log(self, level: int, message: str, trace_id: Optional[str] = None, **kwargs):
        """
        记录日志
        
        Args:
            level: 日志级别
            message: 日志消息
            trace_id: 追踪ID
            **kwargs: 额外的上下文信息
        """
        if trace_id is None:
            trace_id = str(uuid.uuid4())
        
        # 构建额外上下文
        extra = {'trace_id': trace_id}
        if kwargs:
            extra['context'] = kwargs
        
        # 记录日志
        self.logger.log(level, message, extra=extra)
    
    def debug(self, message: str, trace_id: Optional[str] = None, **kwargs):
        """记录DEBUG级别日志"""
        self._log(logging.DEBUG, message, trace_id, **kwargs)
    
    def info(self, message: str, trace_id: Optional[str] = None, **kwargs):
        """记录INFO级别日志"""
        self._log(logging.INFO, message, trace_id, **kwargs)
    
    def warning(self, message: str, trace_id: Optional[str] = None, **kwargs):
        """记录WARNING级别日志"""
        self._log(logging.WARNING, message, trace_id, **kwargs)
    
    def error(self, message: str, trace_id: Optional[str] = None, **kwargs):
        """记录ERROR级别日志"""
        self._log(logging.ERROR, message, trace_id, **kwargs)
    
    def critical(self, message: str, trace_id: Optional[str] = None, **kwargs):
        """记录CRITICAL级别日志"""
        self._log(logging.CRITICAL, message, trace_id, **kwargs)


class TraceManager:
    """Trace ID管理器"""
    
    _instance = None
    _trace_stack = {}
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def generate_trace_id(self) -> str:
        """生成新的trace_id"""
        return str(uuid.uuid4())
    
    def set_trace_id(self, trace_id: str):
        """设置当前trace_id"""
        import threading
        thread_id = threading.get_ident()
        if thread_id not in self._trace_stack:
            self._trace_stack[thread_id] = []
        self._trace_stack[thread_id].append(trace_id)
    
    def get_trace_id(self) -> Optional[str]:
        """获取当前trace_id"""
        import threading
        thread_id = threading.get_ident()
        if thread_id in self._trace_stack and self._trace_stack[thread_id]:
            return self._trace_stack[thread_id][-1]
        return None
    
    def clear_trace_id(self):
        """清除当前trace_id"""
        import threading
        thread_id = threading.get_ident()
        if thread_id in self._trace_stack and self._trace_stack[thread_id]:
            self._trace_stack[thread_id].pop()


# 全局日志记录器
def get_logger(name: str, **kwargs) -> StructuredLogger:
    """
    获取日志记录器
    
    Args:
        name: 日志记录器名称
        **kwargs: 传递给StructuredLogger的参数
    
    Returns:
        StructuredLogger实例
    """
    return StructuredLogger(name, **kwargs)


# 全局trace管理器
trace_manager = TraceManager()


def with_trace(func):
    """
    装饰器：自动为函数添加trace_id
    
    使用示例:
        @with_trace
        def my_function():
            logger.info("处理中")
    """
    def wrapper(*args, **kwargs):
        # 生成或获取trace_id
        trace_id = trace_manager.get_trace_id()
        if trace_id is None:
            trace_id = trace_manager.generate_trace_id()
            trace_manager.set_trace_id(trace_id)
            should_clear = True
        else:
            should_clear = False
        
        try:
            return func(*args, **kwargs)
        finally:
            if should_clear:
                trace_manager.clear_trace_id()
    
    return wrapper


if __name__ == '__main__':
    # 测试日志记录
    logger = get_logger('test_logger')
    
    # 测试基本日志
    logger.info('这是一条测试日志')
    
    # 测试带trace_id的日志
    trace_id = trace_manager.generate_trace_id()
    logger.info('这是一条带trace_id的日志', trace_id=trace_id)
    
    # 测试装饰器
    @with_trace
    def test_function():
        logger.info('在装饰器函数中')
    
    test_function()
    
    print('日志模块测试完成')
