#!/usr/bin/env python3
"""
Amber Url to Markdown - 工具函数模块
包含文件保存、图片下载、目录管理等辅助功能

作者：小文
时间：2026-03-24
版本：V3.0
"""

import os
import re
import requests
from datetime import datetime
from typing import Optional, Dict, Tuple
from pathlib import Path
from bs4 import BeautifulSoup

# 导入配置
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from config import get_output_config


# ============================================================================
# 常量定义
# ============================================================================

DEFAULT_OUTPUT_DIR = "/root/openclaw/urltomarkdown"
IMAGE_DOWNLOAD_TIMEOUT = 10
MAX_TITLE_LENGTH = 50


# ============================================================================
# 标题清理
# ============================================================================

def sanitize_title(title: str, max_length: int = None) -> str:
    """
    清理标题，生成安全的文件名
    
    Args:
        title: 原始标题
        max_length: 最大长度（默认从配置读取）
    
    Returns:
        str: 清理后的标题（适合用作文件名）
    """
    cfg = get_output_config()
    
    if max_length is None:
        max_length = cfg.MAX_TITLE_LENGTH
    
    # 去除首尾空格
    title = title.strip()
    
    # 替换非法文件名字符
    # Windows: < > : " / \ | ? *
    # Linux/Mac: 只限制 / 和 NULL
    title = re.sub(r'[<>:"/\\|?*]', '_', title)
    
    # 替换连续空格为单个下划线
    title = re.sub(r'\s+', '_', title)
    
    # 替换连续下划线为单个
    title = re.sub(r'_+', '_', title)
    
    # 去除首尾下划线
    title = title.strip('_')
    
    # 限制长度
    if len(title) > max_length:
        # 尽量在单词边界处截断
        truncated = title[:max_length]
        last_underscore = truncated.rfind('_')
        if last_underscore > max_length // 2:
            title = truncated[:last_underscore]
        else:
            title = truncated
    
    # 确保不为空
    if not title:
        title = "untitled"
    
    return title


def format_timestamp(fmt: str = None) -> str:
    """
    生成格式化的时间戳
    
    Args:
        fmt: 时间格式（默认从配置读取）
    
    Returns:
        str: 格式化时间戳
    """
    cfg = get_output_config()
    if fmt is None:
        fmt = cfg.TIMESTAMP_FORMAT
    return datetime.now().strftime(fmt)


def format_datetime(fmt: str = None) -> str:
    """
    生成格式化的日期时间字符串
    
    Args:
        fmt: 时间格式（默认从配置读取）
    
    Returns:
        str: 格式化日期时间
    """
    cfg = get_output_config()
    if fmt is None:
        fmt = cfg.DATETIME_FORMAT
    return datetime.now().strftime(fmt)


# ============================================================================
# 目录管理
# ============================================================================

def create_output_directories(
    output_dir: str = None,
    timestamp: Optional[str] = None,
    download_images: bool = None
) -> Tuple[str, Optional[str]]:
    """
    创建输出目录结构
    
    Args:
        output_dir: 输出目录根路径
        timestamp: 时间戳（用于图片目录命名）
        download_images: 是否下载图片
    
    Returns:
        Tuple[str, Optional[str]]: (输出目录，图片目录或 None)
    """
    cfg = get_output_config()
    
    if output_dir is None:
        output_dir = cfg.DEFAULT_OUTPUT_DIR
    if download_images is None:
        download_images = cfg.DOWNLOAD_IMAGES
    
    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成时间戳
    if not timestamp:
        timestamp = format_timestamp()
    
    # 图片目录
    images_dir = None
    if download_images:
        images_dir = os.path.join(output_dir, cfg.IMAGES_SUBDIR, f"{cfg.IMAGES_DIR_PREFIX}{timestamp}")
        os.makedirs(images_dir, exist_ok=True)
    
    return output_dir, images_dir


# ============================================================================
# 图片处理
# ============================================================================

def download_image(
    img_url: str,
    save_path: str,
    timeout: int = None,
    headers: Optional[Dict[str, str]] = None
) -> bool:
    """
    下载图片到本地
    
    Args:
        img_url: 图片 URL
        save_path: 保存路径
        timeout: 下载超时时间（秒）
        headers: 自定义请求头
    
    Returns:
        bool: 是否下载成功
    """
    cfg = get_output_config()
    
    if timeout is None:
        timeout = cfg.IMAGE_TIMEOUT
    
    # 默认请求头
    default_headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://mp.weixin.qq.com/",
    }
    
    if headers:
        default_headers.update(headers)
    
    try:
        response = requests.get(img_url, headers=default_headers, timeout=timeout)
        response.raise_for_status()
        
        # 确保目录存在
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        
        with open(save_path, 'wb') as f:
            f.write(response.content)
        
        return True
        
    except Exception as e:
        print(f"[WARN] ⚠️ 图片下载失败：{str(e)[:80]}")
        return False


def extract_and_download_images(
    soup: BeautifulSoup,
    images_dir: str,
    timestamp: str,
    download_images: bool = True
) -> Tuple[str, int]:
    """
    从 BeautifulSoup 对象中提取并下载图片
    
    Args:
        soup: BeautifulSoup 对象
        images_dir: 图片保存目录
        timestamp: 时间戳（用于生成相对路径）
        download_images: 是否下载图片
    
    Returns:
        Tuple[str, int]: (处理后的 HTML 字符串，图片数量)
    """
    from bs4 import BeautifulSoup
    
    image_count = 0
    
    for img_tag in soup.find_all("img"):
        image_count += 1
        alt = img_tag.get("alt") or "图片"
        src = img_tag.get("data-src") or img_tag.get("src")
        
        # 跳过无效图片链接
        if not src or not src.startswith("http"):
            img_tag.decompose()
            continue
        
        # 生成文件名和路径
        filename = f"img_{image_count:03d}.jpg"
        save_path = os.path.join(images_dir, filename)
        # 相对路径用于 Markdown 引用
        relative_path = f"images/knowledge_{timestamp}/{filename}"
        
        print(f"[INFO]   ↓ 图片 {image_count}: {filename}")
        
        if download_images and download_image(src, save_path):
            img_tag.replace_with(f"![{alt}]({relative_path})\n\n")
        else:
            # 下载失败，保留原链接
            img_tag.replace_with(f"![{alt}]({src})\n\n")
    
    return str(soup), image_count


# ============================================================================
# 文件保存
# ============================================================================

def save_markdown_file(
    content: str,
    title: str,
    output_dir: str,
    metadata: Optional[Dict] = None
) -> str:
    """
    保存 Markdown 文件
    
    Args:
        content: Markdown 内容
        title: 文章标题（用于文件名）
        output_dir: 输出目录
        metadata: 元数据（链接、时间等）
    
    Returns:
        str: 保存的文件路径
    """
    # 生成安全的文件名
    safe_title = sanitize_title(title)
    output_file = os.path.join(output_dir, f"{safe_title}.md")
    
    # 构建完整内容（包含元数据）
    if metadata:
        header_lines = [
            f"# {title}",
            "",
        ]
        
        # 添加元数据
        if "url" in metadata:
            header_lines.append(f"> 链接：{metadata['url']}")
        if "timestamp" in metadata:
            header_lines.append(f"> 抓取时间：{metadata['timestamp']}")
        if "image_count" in metadata:
            header_lines.append(f"> 图片数量：{metadata['image_count']} 张")
        if "site_type" in metadata:
            header_lines.append(f"> 网站类型：{metadata['site_type']}")
        if "scheme" in metadata:
            header_lines.append(f"> 抓取方案：{metadata['scheme']}")
        
        header_lines.extend(["", "---", ""])
        full_content = "\n".join(header_lines) + content
    else:
        full_content = f"# {title}\n\n{content}"
    
    # 保存文件
    os.makedirs(os.path.dirname(output_file) if os.path.dirname(output_file) else ".", exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(full_content)
    
    print(f"[INFO] 📝 文件保存成功：{output_file}")
    return output_file


# ============================================================================
# 日志工具
# ============================================================================

def create_logger(prefix: str = "AMBER") -> callable:
    """
    创建日志记录函数
    
    Args:
        prefix: 日志前缀
    
    Returns:
        callable: log(msg, level="INFO") 函数
    """
    def log(msg: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        print(f"[{timestamp}] [{level}] {prefix}: {msg}")
    
    return log


# ============================================================================
# 测试入口
# ============================================================================

if __name__ == "__main__":
    # 测试标题清理
    test_titles = [
        "测试文章：如何学习 Python？",
        "Hello <World> 测试/文件名",
        "这是一篇非常非常非常非常非常长的文章标题需要截断",
    ]
    
    print("标题清理测试:")
    for title in test_titles:
        print(f"  原始：{title}")
        print(f"  清理：{sanitize_title(title)}")
        print()
    
    # 测试时间戳
    print(f"时间戳：{format_timestamp()}")
    print(f"日期时间：{format_datetime()}")
