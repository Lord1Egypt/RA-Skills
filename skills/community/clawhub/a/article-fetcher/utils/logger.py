"""
日志配置
"""
import logging
import sys
from pathlib import Path

log_dir = Path(__file__).resolve().parent.parent / 'logs'
log_dir.mkdir(parents=True, exist_ok=True)

formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

file_handler = logging.FileHandler(log_dir / 'article-fetcher.log', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger = logging.getLogger('article-fetcher')
logger.setLevel(logging.INFO)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
