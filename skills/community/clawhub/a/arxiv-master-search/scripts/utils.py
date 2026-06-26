"""
utils.py - 工具函数模块
提供通用辅助函数、日志设置等
"""

import os
import re
import time
import logging
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from urllib.parse import urlparse

# 可选依赖
try:
    import colorlog
    HAS_COLORLOG = True
except ImportError:
    HAS_COLORLOG = False


def setup_logging(level: str = "INFO", log_file: str = None) -> logging.Logger:
    """
    设置日志配置

    Args:
        level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
        log_file: 日志文件路径，如 None 则不记录到文件

    Returns:
        配置好的 logger 实例
    """
    log_format = "[%(levelname)s] %(asctime)s - %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    logger = logging.getLogger("arxiv_search")
    logger.setLevel(getattr(logging, level.upper()))
    logger.propagate = False

    if logger.handlers:
        logger.handlers.clear()

    # 控制台输出
    if HAS_COLORLOG:
        console_formatter = colorlog.ColoredFormatter(
            "%(log_color)s" + log_format,
            datefmt=date_format,
            log_colors={
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "red,bg_white",
            }
        )
    else:
        console_formatter = logging.Formatter(log_format, datefmt=date_format)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # 文件输出
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_formatter = logging.Formatter(log_format, datefmt=date_format)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger() -> logging.Logger:
    """
    获取全局 logger，如果未配置则使用默认配置

    Returns:
        logger 实例
    """
    logger = logging.getLogger("arxiv_search")
    if not logger.handlers:
        setup_logging()
    return logger


def deep_update(base_dict: Dict[str, Any], update_dict: Dict[str, Any]) -> None:
    """
    深度更新字典

    Args:
        base_dict: 基础字典
        update_dict: 更新字典
    """
    for key, value in update_dict.items():
        if key in base_dict and isinstance(base_dict[key], dict) and isinstance(value, dict):
            deep_update(base_dict[key], value)
        else:
            base_dict[key] = value


def slugify(text: str, max_length: int = 80) -> str:
    """
    将文本转换为 URL 友好的 slug

    Args:
        text: 输入文本
        max_length: 最大长度

    Returns:
        slug 化的文本
    """
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    text = re.sub(r"[\s_-]+", "-", text)
    text = text.strip("-")
    return text[:max_length]


def sanitize_filename(filename: str) -> str:
    """
    清理文件名，移除非法字符

    Args:
        filename: 原始文件名

    Returns:
        清理后的文件名
    """
    invalid_chars = '<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, "_")
    filename = filename.strip()
    filename = filename[:200]
    return filename


def ensure_dir(path: str) -> Path:
    """
    确保目录存在，不存在则创建

    Args:
        path: 目录路径

    Returns:
        Path 对象
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def parse_arxiv_id(arxiv_id: str) -> str:
    """
    解析 arXiv ID，支持多种格式

    Args:
        arxiv_id: arXiv ID 或 URL

    Returns:
        标准化的 arXiv ID

    Examples:
        >>> parse_arxiv_id("2301.01234")
        "2301.01234"
        >>> parse_arxiv_id("https://arxiv.org/abs/2301.01234v1")
        "2301.01234"
    """
    # 如果是 URL，提取 ID
    if arxiv_id.startswith(("http://", "https://")):
        parsed = urlparse(arxiv_id)
        path = parsed.path
        # 匹配 /abs/xxx 或 /pdf/xxx.pdf - 支持带点和斜杠的旧式 ID
        # 新模式: 2301.01234, 旧式: hep-th/9901001
        match = re.search(r"/(?:abs|pdf)/([^?#]+?)(?:v\d+)?(?:\.pdf)?$", path)
        if match:
            arxiv_id = match.group(1)

    # 移除版本号 (v1, v2 等) - 只在末尾匹配
    arxiv_id = re.sub(r"v\d+$", "", arxiv_id)

    return arxiv_id


def save_json(data: Any, filepath: str, indent: int = 2, ensure_ascii: bool = False) -> None:
    """
    保存数据为 JSON 文件

    Args:
        data: 要保存的数据
        filepath: 文件路径
        indent: 缩进空格数
        ensure_ascii: 是否确保 ASCII
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=indent, ensure_ascii=ensure_ascii, default=str)


def load_json(filepath: str) -> Any:
    """
    从 JSON 文件加载数据

    Args:
        filepath: 文件路径

    Returns:
        加载的数据
    """
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_jsonl(filepath: str) -> List[Any]:
    """
    从 JSONL 文件加载数据

    Args:
        filepath: 文件路径

    Returns:
        数据列表
    """
    results = []
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                results.append(json.loads(line))
    return results


class RateLimiter:
    """
    简单的速率限制器
    """

    def __init__(self, requests_per_second: float = 2.0, min_delay: float = 0.5):
        """
        初始化速率限制器

        Args:
            requests_per_second: 每秒请求数
            min_delay: 最小延迟（秒）
        """
        self.min_interval = 1.0 / requests_per_second if requests_per_second > 0 else 0
        self.min_interval = max(self.min_interval, min_delay)
        self.last_request_time = 0.0

    def wait(self) -> None:
        """等待直到可以发送下一个请求"""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)
        self.last_request_time = time.time()
