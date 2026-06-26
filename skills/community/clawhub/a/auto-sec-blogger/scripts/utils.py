"""
Utilities Module
로깅, 공통 헬퍼 함수 등을 제공합니다.
"""

import logging
import sys
from logging.handlers import RotatingFileHandler
from modules.intelligence.config import LOG_DIR

def setup_logger(name: str, log_file: str = None, level=logging.INFO) -> logging.Logger:
    """
    로거 설정 및 반환

    Args:
        name: 로거 이름 (__name__)
        log_file: 로그 파일명 (예: 'pipeline.log'). None이면 파일 로깅 안함.
        level: 로그 레벨

    Returns:
        설정된 Logger 인스턴스
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    # 핸들러가 이미 있다면 추가하지 않음 (중복 로그 방지)
    if logger.handlers:
        return logger

    # 포맷터
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # 1. 콘솔 핸들러
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 2. 파일 핸들러 (옵션)
    if log_file:
        log_path = LOG_DIR / log_file
        # RotatingFileHandler: 10MB 단위로 최대 5개 파일 유지
        file_handler = RotatingFileHandler(
            log_path, maxBytes=10*1024*1024, backupCount=5, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
