import os
import sys
import logging
from logging.handlers import RotatingFileHandler

class StreamToLogger(object):
    """Fake file-like stream object that redirects writes to a logger instance."""
    def __init__(self, logger, level):
       self.logger = logger
       self.level = level
       self.linebuf = ''

    def write(self, buf):
       for line in buf.rstrip().splitlines():
          self.logger.log(self.level, line.rstrip())

    def flush(self):
        pass

def setup_rotating_logger(name: str, log_file: str, max_bytes: int = 5*1024*1024, backup_count: int = 5):
    """
    Sets up a rotating logger that redirects stdout and stderr to the log file.
    Args:
        name: Name of the logger.
        log_file: Path to the log file (e.g., 'logs/live_trader.log').
        max_bytes: Maximum size of the log file before rotating (default 5MB).
        backup_count: Number of backup log files to keep (default 5).
    """
    os.makedirs(os.path.dirname(log_file), exist_ok=True)

    # 핸들러 설정 (Rolling File)
    file_handler = RotatingFileHandler(
        log_file, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
    )
    
    # 포맷 설정
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    file_handler.setFormatter(formatter)

    # 로거 생성
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    
    # 기존 핸들러 초기화 방지 (이미 추가된 경우)
    if not any(isinstance(h, RotatingFileHandler) and h.baseFilename == file_handler.baseFilename for h in logger.handlers):
        logger.addHandler(file_handler)

    # 콘솔 출력 (sys.stdout.isatty() 일때만)
    if sys.stdout.isatty():
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    # sys.stdout, sys.stderr 리다이렉트 (nohup 등으로 실행될 때 stdout/err가 파일에 계속 쌓이는 것 방지)
    # isatty()가 아닐때만 리다이렉트하여 콘솔 중복 방지
    if not sys.stdout.isatty():
        sys.stdout = StreamToLogger(logger, logging.INFO)
        sys.stderr = StreamToLogger(logger, logging.ERROR)

    return logging.getLogger(name)

