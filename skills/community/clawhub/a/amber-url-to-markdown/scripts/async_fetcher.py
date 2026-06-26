#!/usr/bin/env python3
"""
Amber Url to Markdown - 异步批量请求模块
使用 aiohttp 实现高效批量抓取

作者：小文
时间：2026-03-24
版本：V3.1
"""

import asyncio
import aiohttp
from aiohttp import ClientTimeout, ClientError
from typing import List, Optional, Dict, Tuple
import time

# 导入配置
import sys
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, script_dir)
from config import get_fetch_config


# ============================================================================
# 异步请求函数
# ============================================================================

async def async_fetch_url(
    session: aiohttp.ClientSession,
    url: str,
    timeout: int = None,
    semaphore: asyncio.Semaphore = None
) -> Optional[Tuple[str, str]]:
    """
    异步抓取单个 URL
    
    Args:
        session: aiohttp 会话
        url: 目标 URL
        timeout: 超时时间（秒）
        semaphore: 信号量（控制并发数）
    
    Returns:
        Tuple[str, str]: (url, html_content) 或 None
    """
    cfg = get_fetch_config()
    
    if timeout is None:
        timeout = cfg.TIMEOUT
    
    headers = {
        "User-Agent": cfg.USER_AGENT,
        "Accept": cfg.ACCEPT,
        "Accept-Language": cfg.ACCEPT_LANGUAGE,
    }
    
    async with semaphore or asyncio.Semaphore():
        try:
            async with session.get(
                url,
                headers=headers,
                timeout=ClientTimeout(total=timeout),
                allow_redirects=True
            ) as response:
                response.raise_for_status()
                content = await response.text()
                print(f"[INFO] ✅ 抓取成功：{url[:60]}...")
                return (url, content)
                
        except asyncio.TimeoutError:
            print(f"[ERROR] ❌ 超时：{url[:60]}...")
            return None
            
        except ClientError as e:
            print(f"[ERROR] ❌ 请求失败：{url[:60]}... - {str(e)[:50]}")
            return None
            
        except Exception as e:
            print(f"[ERROR] ❌ 未知错误：{url[:60]}... - {type(e).__name__}: {str(e)[:50]}")
            return None


async def async_batch_fetch(
    urls: List[str],
    timeout: int = None,
    max_concurrent: int = 5,
    check_robots: bool = False
) -> List[Tuple[str, str]]:
    """
    批量异步抓取 URL
    
    Args:
        urls: URL 列表
        timeout: 超时时间（秒）
        max_concurrent: 最大并发数
        check_robots: 是否检查 robots.txt
    
    Returns:
        List[Tuple[str, str]]: [(url, html_content), ...] 成功抓取的列表
    """
    from fetcher import is_allowed_by_robots
    
    # 过滤禁止爬取的 URL
    if check_robots:
        allowed_urls = []
        for url in urls:
            if is_allowed_by_robots(url):
                allowed_urls.append(url)
            else:
                print(f"[WARN] 🚫 跳过禁止爬取的 URL：{url}")
        urls = allowed_urls
    
    # 创建信号量（控制并发数）
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with aiohttp.ClientSession() as session:
        # 创建任务列表
        tasks = [
            async_fetch_url(session, url, timeout, semaphore)
            for url in urls
        ]
        
        # 并发执行
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # 过滤失败结果
        success_results = [
            (url, content) for url, content in results
            if url and content
        ]
        
        return success_results


def batch_fetch_async(
    urls: List[str],
    timeout: int = None,
    max_concurrent: int = 5
) -> List[Tuple[str, str]]:
    """
    同步入口：批量异步抓取 URL
    
    Args:
        urls: URL 列表
        timeout: 超时时间（秒）
        max_concurrent: 最大并发数
    
    Returns:
        List[Tuple[str, str]]: 成功抓取的列表
    """
    print(f"\n{'='*60}")
    print(f"异步批量抓取 - {len(urls)} 个 URL，最大并发：{max_concurrent}")
    print(f"{'='*60}\n")
    
    start_time = time.time()
    
    # 运行异步任务
    results = asyncio.run(async_batch_fetch(urls, timeout, max_concurrent))
    
    elapsed = time.time() - start_time
    
    print(f"\n{'='*60}")
    print(f"✅ 批量抓取完成")
    print(f"📊 成功：{len(results)}/{len(urls)}")
    print(f"⏱️ 耗时：{elapsed:.2f}秒")
    print(f"📈 平均速度：{elapsed/len(urls):.2f}秒/URL")
    print(f"{'='*60}\n")
    
    return results


# ============================================================================
# 带进度条的批量抓取
# ============================================================================

async def async_batch_fetch_with_progress(
    urls: List[str],
    timeout: int = None,
    max_concurrent: int = 5
) -> List[Tuple[str, str]]:
    """
    带进度条的批量异步抓取
    
    Args:
        urls: URL 列表
        timeout: 超时时间（秒）
        max_concurrent: 最大并发数
    
    Returns:
        List[Tuple[str, str]]: 成功抓取的列表
    """
    from fetcher import is_allowed_by_robots
    
    # 过滤禁止爬取的 URL
    allowed_urls = [url for url in urls if is_allowed_by_robots(url)]
    skipped = len(urls) - len(allowed_urls)
    
    if skipped > 0:
        print(f"[INFO] 跳过 {skipped} 个禁止爬取的 URL")
    
    semaphore = asyncio.Semaphore(max_concurrent)
    results = []
    completed = 0
    total = len(allowed_urls)
    
    async def fetch_with_progress(session: aiohttp.ClientSession, url: str):
        nonlocal completed
        result = await async_fetch_url(session, url, timeout, semaphore)
        completed += 1
        
        # 显示进度
        progress = completed / total * 100
        print(f"[INFO] 进度：{progress:.1f}% ({completed}/{total})")
        
        if result:
            results.append(result)
        
        return result
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_progress(session, url) for url in allowed_urls]
        await asyncio.gather(*tasks, return_exceptions=True)
    
    return results


# ============================================================================
# 测试入口
# ============================================================================

if __name__ == "__main__":
    # 简单测试
    test_urls = [
        "https://example.com",
        "https://example.org",
        "https://httpbin.org/html",
    ]
    
    print("测试异步批量抓取...")
    results = batch_fetch_async(test_urls, max_concurrent=3)
    
    print(f"\n抓取结果：")
    for url, content in results:
        print(f"  {url[:50]}... - {len(content)} 字节")
