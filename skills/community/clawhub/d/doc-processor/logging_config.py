#!/usr/bin/env python3
"""日志配置模块 - v2.4.0"""

import logging
import sys
import os
from pathlib import Path
from typing import Optional

LOG_LEVELS = {'debug': logging.DEBUG, 'info': logging.INFO, 'warning': logging.WARNING, 'error': logging.ERROR, 'critical': logging.CRITICAL}

def setup_logger(name: str = 'doc_processor', log_file: str = None, level: str = None) -> logging.Logger:
    if level is None:
        level = os.getenv('DOC_PROCESSOR_LOG_LEVEL', 'info')
    logger = logging.getLogger(name)
    logger.setLevel(LOG_LEVELS.get(level.lower(), logging.INFO))
    if not logger.handlers:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logger.level)
        console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%H:%M:%S'))
        logger.addHandler(console_handler)
        if log_file is None:
            log_file = os.getenv('DOC_PROCESSOR_LOG_FILE')
        if log_file:
            log_path = Path(log_file)
            log_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(log_path, encoding='utf-8')
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'))
            logger.addHandler(file_handler)
    logger.info(f"日志级别：{level.upper()}")
    return logger

def configure_logging(level: str = None, log_file: Optional[str] = None, log_format: str = 'standard') -> logging.Logger:
    if level is None:
        level = os.getenv('DOC_PROCESSOR_LOG_LEVEL', 'info')
    if log_file is None:
        log_file = os.getenv('DOC_PROCESSOR_LOG_FILE')
    logger = logging.getLogger('doc_processor')
    logger.setLevel(LOG_LEVELS.get(level.lower(), logging.INFO))
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logger.level)
    if log_format == 'detailed':
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    else:
        formatter = logging.Formatter('%(levelname)s - %(message)s', datefmt='%H:%M:%S')
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_path, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'))
        logger.addHandler(file_handler)
    logger.info(f"日志级别：{level.upper()}")
    return logger

logger = setup_logger()
