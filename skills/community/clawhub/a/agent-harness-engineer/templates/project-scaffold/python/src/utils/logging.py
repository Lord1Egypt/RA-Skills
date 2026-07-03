#!/usr/bin/env python3
"""
# ============================================
# 类型: 核心框架
# 模块: utils.logging
# 说明: 日志配置
# 修改建议: 如需扩展，修改日志格式或添加新的handler
# ============================================

import os
import logging
from pathlib import Path


def setup_logging(level: str = None):
    """
    设置日志
    
    Args:
        level: 日志级别，默认从环境变量LOG_LEVEL读取
    """
    if level is None:
        level = os.getenv("LOG_LEVEL", "info").upper()
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 配置日志
    logging.basicConfig(
        level=getattr(logging, level, logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(log_dir / "agent.log")
        ]
    )


def get_logger(name: str) -> logging.Logger:
    """获取日志记录器"""
    return logging.getLogger(name)
