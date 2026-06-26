#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
URL 去重模块（混合去重）

功能：检查 URL 是否已存在于知识库，避免重复处理
支持：URL 标准化 + 内容指纹双重去重

注意：此模块需要配合 OpenClaw 环境使用，或独立运行时配置数据目录
"""

import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs, urlunparse

# 缓存文件路径（使用相对路径，安全）
SKILL_DIR = Path(__file__).parent.parent.resolve()
CACHE_FILE = SKILL_DIR / "data" / "url_cache.json"


def validate_path_safety(path: Path, base_dir: Path = None) -> bool:
    """
    验证路径是否在 Skill 目录内（安全边界检查）
    
    Args:
        path: 要验证的路径
        base_dir: 基准目录（默认 SKILL_DIR）
    
    Returns:
        bool: True=安全，False=超出边界
    
    Raises:
        SecurityError: 路径超出 Skill 目录范围
    """
    if base_dir is None:
        base_dir = SKILL_DIR
    
    try:
        path.resolve().relative_to(base_dir)
        return True
    except ValueError:
        raise SecurityError(
            f"安全错误：路径超出 Skill 目录范围\n"
            f"  基准目录：{base_dir}\n"
            f"  目标路径：{path.resolve()}"
        )


class SecurityError(Exception):
    """安全边界错误"""
    pass


# 初始化时验证数据目录
try:
    validate_path_safety(CACHE_FILE.parent)
except SecurityError as e:
    print(f"⚠️  警告：{e}")
    print("   请确保数据目录在 Skill 目录内")


def normalize_url(url: str) -> str:
    """
    标准化 URL（去除追踪参数）
    
    支持的 platform：
    - 微信：保留 __biz, mid, idx, sn
    - 其他：返回原 URL
    
    Args:
        url: 原始 URL
    
    Returns:
        str: 标准化后的 URL
    """
    # 微信文章特殊处理
    if "mp.weixin.qq.com" in url:
        try:
            parsed = urlparse(url)
            query_params = parse_qs(parsed.query)
            
            # 保留关键参数（文章唯一标识）
            keep_params = ['__biz', 'mid', 'idx', 'sn']
            normalized_params = {
                k: v[0] for k, v in query_params.items() 
                if k in keep_params
            }
            
            # 重建 URL
            normalized = parsed._replace(query='&'.join(
                f"{k}={v}" for k, v in sorted(normalized_params.items())
            ))
            
            return urlunparse(normalized)
        except Exception as e:
            print(f"⚠️ URL 标准化失败：{e}")
            return url
    
    # 其他平台返回原 URL
    return url


def get_url_hash(url: str) -> str:
    """生成 URL 的哈希值"""
    # 先标准化 URL
    normalized_url = normalize_url(url)
    return hashlib.md5(normalized_url.encode()).hexdigest()


def get_content_fingerprint(title: str, content: str) -> str:
    """
    生成内容指纹
    
    Args:
        title: 文章标题
        content: 文章内容
    
    Returns:
        str: 内容指纹（MD5，32 字符）
    
    Note:
        - 标题会标准化（小写、去多余空格）
        - 内容只取前 1000 字
        - 相同文章即使标题格式不同也能识别
    """
    # 标准化标题（小写、去多余空格）
    normalized_title = ' '.join(title.lower().split())
    
    # 取标题 + 前 1000 字
    fingerprint_text = f"{normalized_title}:{content[:1000].strip()}"
    return hashlib.md5(fingerprint_text.encode()).hexdigest()


def load_cache() -> dict:
    """加载缓存"""
    if CACHE_FILE.exists():
        with open(CACHE_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "urls": {},
        "fingerprints": {},
        "metadata": {
            "last_updated": None,
            "total": 0,
            "fingerprint_total": 0
        }
    }


def save_cache(cache: dict):
    """保存缓存"""
    CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_FILE, 'w', encoding='utf-8') as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)


def check_url_duplicate(url: str) -> dict:
    """
    检查 URL 是否已存在（仅 URL 维度）
    
    Args:
        url: 文章 URL
    
    Returns:
        dict: {
            "is_duplicate": bool,
            "record": dict|None,
            "check_type": "url"
        }
    """
    cache = load_cache()
    url_hash = get_url_hash(url)
    
    if url_hash in cache["urls"]:
        return {
            "is_duplicate": True,
            "record": cache["urls"][url_hash],
            "check_type": "url"
        }
    
    return {
        "is_duplicate": False,
        "record": None,
        "check_type": "url"
    }


def check_content_duplicate(title: str, content: str) -> dict:
    """
    检查内容是否重复（内容指纹维度）
    
    Args:
        title: 文章标题
        content: 文章内容
    
    Returns:
        dict: {
            "is_duplicate": bool,
            "record": dict|None,
            "check_type": "fingerprint",
            "fingerprint": str
        }
    """
    cache = load_cache()
    fingerprint = get_content_fingerprint(title, content)
    
    if fingerprint in cache.get("fingerprints", {}):
        return {
            "is_duplicate": True,
            "record": cache["fingerprints"][fingerprint],
            "check_type": "fingerprint",
            "fingerprint": fingerprint
        }
    
    return {
        "is_duplicate": False,
        "record": None,
        "check_type": "fingerprint",
        "fingerprint": fingerprint
    }


def check_duplicate(url: str, title: str = None, content: str = None) -> dict:
    """
    混合去重检查（URL 标准化 + 内容指纹）
    
    Args:
        url: 文章 URL
        title: 文章标题（可选，用于内容指纹）
        content: 文章内容（可选，用于内容指纹）
    
    Returns:
        dict: {
            "is_duplicate": bool,
            "record": dict|None,
            "check_type": "url" | "fingerprint" | None,
            "normalized_url": str,
            "fingerprint": str|None
        }
    """
    # 1. URL 标准化检查
    url_result = check_url_duplicate(url)
    if url_result["is_duplicate"]:
        return {
            "is_duplicate": True,
            "record": url_result["record"],
            "check_type": "url",
            "normalized_url": normalize_url(url),
            "fingerprint": None
        }
    
    # 2. 内容指纹检查（如果有标题和内容）
    if title and content:
        fingerprint_result = check_content_duplicate(title, content)
        if fingerprint_result["is_duplicate"]:
            return {
                "is_duplicate": True,
                "record": fingerprint_result["record"],
                "check_type": "fingerprint",
                "normalized_url": normalize_url(url),
                "fingerprint": fingerprint_result.get("fingerprint")
            }
    
    # 3. 不重复
    return {
        "is_duplicate": False,
        "record": None,
        "check_type": None,
        "normalized_url": normalize_url(url),
        "fingerprint": get_content_fingerprint(title, content) if title and content else None
    }


def add_url_to_cache(url: str, title: str, record_id: str, doc_url: str, content: str = None):
    """
    添加 URL 到缓存（同时记录 URL 和内容指纹）
    
    Args:
        url: 文章 URL
        title: 文章标题
        record_id: Bitable 记录 ID
        doc_url: 详细报告文档链接
        content: 文章内容（用于生成指纹）
    """
    cache = load_cache()
    
    # 1. URL 缓存
    url_hash = get_url_hash(url)
    normalized_url = normalize_url(url)
    
    cache["urls"][url_hash] = {
        "url": url,
        "normalized_url": normalized_url,
        "title": title,
        "record_id": record_id,
        "doc_url": doc_url,
        "added_at": datetime.now().isoformat()
    }
    
    # 2. 内容指纹缓存（如果有内容）
    if content:
        fingerprint = get_content_fingerprint(title, content)
        cache["fingerprints"][fingerprint] = {
            "url": url,
            "normalized_url": normalized_url,
            "title": title,
            "record_id": record_id,
            "doc_url": doc_url,
            "added_at": datetime.now().isoformat()
        }
        cache["metadata"]["fingerprint_total"] = len(cache["fingerprints"])
    
    # 3. 更新元数据
    cache["metadata"]["last_updated"] = datetime.now().isoformat()
    cache["metadata"]["total"] = len(cache["urls"])
    
    save_cache(cache)
