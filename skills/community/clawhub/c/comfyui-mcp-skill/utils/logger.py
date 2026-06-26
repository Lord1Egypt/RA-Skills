"""
公共日志模块
"""

import logging


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    获取配置好的 logger

    Args:
        name: logger 名称（通常是 __name__）
        level: 日志级别

    Returns:
        配置好的 Logger 实例
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger


# 根 logger 配置
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# 设置 FastMCP 和 MCP 相关 logger 为 ERROR 级别
logging.getLogger('fastmcp').setLevel(logging.ERROR)
logging.getLogger('mcp').setLevel(logging.ERROR)
