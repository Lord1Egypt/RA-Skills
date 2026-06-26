
"""
日志工具模块
提供统一的日志记录功能
"""

import os
import logging
from logging.handlers import RotatingFileHandler

# 日志根目录
LOG_ROOT = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
    'logs'
)

# 全局logger缓存
_loggers = {}


def get_logger(
    name='a_share_daily_report',
    log_file=None,
    level=logging.INFO,
    max_bytes=10 * 1024 * 1024,  # 10MB
    backup_count=5
):
    """
    获取或创建logger

    Args:
        name: logger名称
        log_file: 日志文件名，如果为None则使用默认名称
        level: 日志级别
        max_bytes: 单个日志文件最大字节数
        backup_count: 保留的备份文件数量

    Returns:
        配置好的logger实例
    """
    # 如果logger已存在，直接返回
    if name in _loggers:
        return _loggers[name]

    # 确保日志目录存在
    os.makedirs(LOG_ROOT, exist_ok=True)

    # 确定日志文件路径
    if log_file is None:
        log_file = f'{name}.log'
    log_path = os.path.join(LOG_ROOT, log_file)

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 避免重复添加handler
    if logger.handlers:
        _loggers[name] = logger
        return logger

    # 日志格式
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # 文件handler（带轮转）
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(level)
    logger.addHandler(file_handler)

    # 控制台handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)
    logger.addHandler(console_handler)

    # 缓存logger
    _loggers[name] = logger

    return logger

