#!/usr/bin/env python3
"""
collectors/proxy_pool.py - 免费代理池模块
从公开源抓取代理 → 验证 → 评分 → 按需分配

使用场景：
1. 大规模采集时轮换IP防封禁
2. 突破单IP请求频率限制
3. 特定地区内容访问

注意：免费代理成功率通常 <20%，关键业务不建议依赖

Usage:
    pool = ProxyPool()
    proxy = pool.get_working_proxy()  # 获取最优代理
    pool.remove_bad_proxy(proxy.url)  # 标记失败代理
"""

import asyncio
import time
import hashlib
import random
import re
from dataclasses import dataclass, field
from typing import Optional, List, Dict
from urllib.parse import urlparse

import aiohttp
from playwright.sync_api import sync_playwright

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))


# ==================== 代理源 ====================

FREE_PROXY_SOURCES = {
    'github_1': 'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'github_2': 'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'github_3': 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'proxyscan': 'https://www.proxyscan.io/api/proxy?limit=20&type=http',
    # 实时代理网站（格式解析较复杂，放后面）
    'free-proxy-list': 'https://free-proxy-list.net/',
    'ssl-proxy': 'https://sslproxies.org/',
}

GITHUB_PROXY_LISTS = [
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.list',
]


# ==================== 数据结构 ====================

@dataclass
class ProxyInfo:
    """代理信息"""
    host: str
    port: int
    protocol: str = 'http'
    latency: float = 0.0        # 毫秒
    success_count: int = 0
    fail_count: int = 0
    last_checked: float = 0.0
    country: Optional[str] = None
    anonymity: Optional[str] = None  # elite / anonymous / transparent

    @property
    def url(self) -> str:
        return f"{self.protocol}://{self.host}:{self.port}"

    @property
    def success_rate(self) -> float:
        total = self.success_count + self.fail_count
        return self.success_count / total if total > 0 else 0.0

    @property
    def is_working(self) -> bool:
        return self.success_count > 0 and self.fail_count < 3

    @property
    def score(self) -> float:
        """综合评分（0-1）"""
        rate = self.success_rate
        latency_score = max(0, 1 - self.latency / 5000)  # 5000ms=0分
        stability = max(0, 1 - self.fail_count / 10)
        return rate * 0.5 + latency_score * 0.3 + stability * 0.2


# ==================== ProxyPool 主类 ====================

class ProxyPool:
    """
    免费代理池

    功能：
    1. 从多个公开源抓取代理（GitHub列表 + 代理网站）
    2. 异步验证可用性 + 测延迟
    3. 按评分排序，按需分配
    4. 自动剔除连续失败的代理
    5. 后台定期刷新

    Usage:
        pool = ProxyPool()

        # 单次使用
        proxy = pool.get_working_proxy()
        if proxy:
            page.set_proxy(proxy={'server': proxy.url})

        # 持续维护
        asyncio.run(pool.auto_maintain(interval_seconds=300))
    """

    def __init__(self,
                 min_success_rate: float = 0.3,
                 max_fail_streak: int = 3,
                 test_url: str = 'http://httpbin.org/ip',
                 test_urls: Optional[List[str]] = None):
        self.proxies: Dict[str, ProxyInfo] = {}
        self.min_success_rate = min_success_rate
        self.max_fail_streak = max_fail_streak
        self.test_urls = test_urls or [
            'http://httpbin.org/ip',
            'http://www.google.com/generate_204',
        ]
        self._lock = asyncio.Lock()

    PRIVATE_IP_PATTERNS = [
        '10.', '192.168.', '172.16.', '172.17.', '172.18.', '172.19.',
        '172.20.', '172.21.', '172.22.', '172.23.', '172.24.', '172.25.',
        '172.26.', '172.27.', '172.28.', '172.29.', '172.30.', '172.31.',
        '127.', 'localhost', '0.0.0.0', '::1'
    ]

    def _is_private_proxy(self, proxy_url: str) -> bool:
        """检查代理是否指向内网IP"""
        from urllib.parse import urlparse
        host = urlparse(proxy_url).hostname or ''
        return any(host.startswith(p) for p in self.PRIVATE_IP_PATTERNS)

    # ---- 抓取 ----

    async def fetch_from_source(self, url: str, session: aiohttp.ClientSession) -> List[ProxyInfo]:
        """从单个源抓取代理列表"""
        proxies = []

        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=15)) as resp:
                if resp.status != 200:
                    return proxies

                text = await resp.text()

                # 纯文本格式（每行 host:port）
                if 'github.com' in url or 'raw.githubusercontent' in url:
                    for line in text.strip().split('\n'):
                        line = line.strip()
                        if not line or line.startswith('#'):
                            continue
                        parts = line.split(':')
                        if len(parts) == 2:
                            try:
                                proxies.append(ProxyInfo(
                                    host=parts[0].strip(),
                                    port=int(parts[1].strip()),
                                    protocol='http',
                                    last_checked=time.time()
                                ))
                            except ValueError:
                                continue

                # HTML格式（free-proxy-list.net）
                elif 'free-proxy-list' in url or 'sslproxies' in url:
                    rows = re.findall(r'<tr>(.*?)</tr>', text, re.DOTALL)
                    for row in rows:
                        cols = re.findall(r'<td>(.*?)</td>', row)
                        if len(cols) >= 2:
                            try:
                                host = cols[0].strip()
                                port = int(cols[1].strip())
                                protocol = 'https' if 'yes' in cols[6].lower() else 'http'
                                country = cols[2].strip() if len(cols) > 2 else None
                                anonymity = cols[4].strip() if len(cols) > 4 else None
                                proxies.append(ProxyInfo(
                                    host=host, port=port, protocol=protocol,
                                    country=country, anonymity=anonymity,
                                    last_checked=time.time()
                                ))
                            except (ValueError, IndexError):
                                continue

        except Exception as e:
            print(f"[ProxyPool] Fetch failed from {url}: {e}")

        return proxies

    async def fetch_all(self) -> int:
        """从所有源抓取代理，返回新增数量"""
        async with aiohttp.ClientSession() as session:
            all_proxies = []

            tasks = [self.fetch_from_source(url, session)
                     for url in FREE_PROXY_SOURCES.values()]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, list):
                    all_proxies.extend(result)

            # 去重
            seen = set()
            unique = []
            for p in all_proxies:
                key = f"{p.host}:{p.port}"
                if key not in seen:
                    seen.add(key)
                    unique.append(p)

            async with self._lock:
                added = 0
                for p in unique:
                    key = f"{p.host}:{p.port}"
                    if key not in self.proxies:
                        self.proxies[key] = p
                        added += 1
                return added

    # ---- 验证 ----

    async def verify_proxy(self, proxy: ProxyInfo,
                           session: aiohttp.ClientSession) -> bool:
        """验证单个代理是否可用，返回成功/失败"""
        # 跳过内网代理，防SSRF
        if self._is_private_proxy(proxy.url):
            return False

        start = time.time()

        for url in self.test_urls:
            try:
                async with session.get(
                    url,
                    proxy=proxy.url,
                    timeout=aiohttp.ClientTimeout(total=10)
                ) as resp:
                    if resp.status in (200, 204):
                        proxy.latency = (time.time() - start) * 1000
                        proxy.success_count += 1
                        proxy.last_checked = time.time()
                        return True
            except:
                continue

        proxy.fail_count += 1
        proxy.last_checked = time.time()
        return False

    async def verify_all(self) -> int:
        """验证所有代理，返回成功数量"""
        async with aiohttp.ClientSession() as session:
            verify_tasks = [self.verify_proxy(p, session)
                           for p in list(self.proxies.values())]
            results = await asyncio.gather(*verify_tasks, return_exceptions=True)
            return sum(1 for r in results if r is True)

    # ---- 管理 ----

    def get_working_proxy(self,
                          protocol: Optional[str] = None,
                          country: Optional[str] = None) -> Optional[ProxyInfo]:
        """
        获取一个可用的代理

        Args:
            protocol: 协议过滤（http/https）
            country: 国家过滤

        Returns:
            ProxyInfo 或 None
        """
        candidates = [
            p for p in self.proxies.values()
            if p.success_rate >= self.min_success_rate
            and p.fail_count <= self.max_fail_streak
        ]

        if protocol:
            candidates = [p for p in candidates if p.protocol == protocol]
        if country:
            candidates = [p for p in candidates if p.country == country]

        if not candidates:
            return None

        # 按评分降序
        candidates.sort(key=lambda x: -x.score)
        return candidates[0]

    def remove_bad_proxy(self, proxy_url: str):
        """移除连续失败的代理"""
        key = proxy_url.replace('http://', '').replace('https://', '')
        if key in self.proxies:
            del self.proxies[key]

    async def refresh_and_verify(self) -> Dict[str, int]:
        """
        完整刷新流程：抓取 → 去重 → 验证

        Returns:
            {'added': int, 'working': int, 'total': int}
        """
        added = await self.fetch_all()
        working = await self.verify_all()

        # 清理不合格的
        async with self._lock:
            bad_keys = [
                k for k, p in self.proxies.items()
                if p.fail_count >= self.max_fail_streak
            ]
            for k in bad_keys:
                del self.proxies[k]

        return {
            'added': added,
            'working': working,
            'total': len(self.proxies)
        }

    async def auto_maintain(self, interval_seconds: int = 300):
        """
        后台维护循环

        定期：抓取新代理 → 验证所有代理 → 清理坏的
        """
        while True:
            stats = await self.refresh_and_verify()
            print(f"[ProxyPool] refresh: added={stats['added']}, "
                  f"working={stats['working']}, total={stats['total']}")
            await asyncio.sleep(interval_seconds)

    def get_statistics(self) -> Dict:
        """获取统计信息"""
        all_p = list(self.proxies.values())
        working = [p for p in all_p if p.is_working]
        return {
            'total': len(all_p),
            'working': len(working),
            'success_rate_avg': sum(p.success_rate for p in working) / max(len(working), 1),
        }

    # ---- 同步封装（用于Playwright同步API）----

    def get_sync(self) -> Optional[ProxyInfo]:
        """同步版本的 get_working_proxy（用于Playwright）"""
        try:
            loop = asyncio.get_running_loop()
            # 已在loop中，用 run_in_executor
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor() as pool:
                future = pool.submit(asyncio.run, self.get_working_proxy())
                return future.result()
        except RuntimeError:
            # 没有running loop，用asyncio.run
            return asyncio.run(self.get_working_proxy())


# ==================== 同步版本的 ProxyPool（用于Playwright） ====================

class SyncProxyPool:
    """
    同步版代理池（包装异步ProxyPool，提供同步API）

    用于 Playwright 等同步API场景
    """

    def __init__(self, **kwargs):
        self._async_pool = ProxyPool(**kwargs)
        self._working: Optional[ProxyInfo] = None
        self._last_refresh = 0.0
        self._refresh_interval = 300.0  # 5分钟刷新一次

    def _ensure_fresh(self):
        """确保缓存新鲜"""
        now = time.time()
        if now - self._last_refresh > self._refresh_interval:
            self.refresh()

    def refresh(self):
        """刷新代理列表"""
        try:
            stats = asyncio.run(self._async_pool.refresh_and_verify())
            self._last_refresh = time.time()
            print(f"[SyncProxyPool] refreshed: {stats}")
        except Exception as e:
            print(f"[SyncProxyPool] refresh failed: {e}")

    def get_proxy(self) -> Optional[ProxyInfo]:
        """获取一个可用代理"""
        self._ensure_fresh()
        return self._async_pool.get_working_proxy()

    def get_url(self) -> Optional[str]:
        """获取代理URL字符串"""
        p = self.get_proxy()
        return p.url if p else None

    def mark_success(self, proxy_url: str):
        """标记代理成功（增加计数）"""
        key = proxy_url.replace('http://', '').replace('https://', '')
        if key in self._async_pool.proxies:
            self._async_pool.proxies[key].success_count += 1

    def mark_failure(self, proxy_url: str):
        """标记代理失败"""
        self._async_pool.remove_bad_proxy(proxy_url)


# ---- CLI ----

def main():
    import argparse
    parser = argparse.ArgumentParser(description='Proxy Pool CLI')
    parser.add_argument('command', choices=['refresh', 'test', 'status'])
    parser.add_argument('--limit', type=int, default=10, help='测试代理数量')
    args = parser.parse_args()

    pool = ProxyPool()

    if args.command == 'refresh':
        print("Fetching and verifying proxies...")
        stats = asyncio.run(pool.refresh_and_verify())
        print(f"Done: added={stats['added']}, working={stats['working']}, total={stats['total']}")

        working = pool.get_working_proxy()
        if working:
            print(f"\nBest proxy: {working.url} (score={working.score:.3f})")
        else:
            print("\nNo working proxies found")

    elif args.command == 'test':
        asyncio.run(pool.fetch_all())
        print(f"Fetched {len(pool.proxies)} proxies, testing...")

        working = asyncio.run(pool.verify_all())
        print(f"Working: {working}/{len(pool.proxies)}")

        top = sorted(pool.proxies.values(), key=lambda x: -x.score)[:args.limit]
        for p in top:
            print(f"  {p.url} score={p.score:.3f} rate={p.success_rate:.2f} "
                  f"latency={p.latency:.0f}ms country={p.country}")

    elif args.command == 'status':
        stats = pool.get_statistics()
        print(f"Total proxies: {stats['total']}")
        print(f"Working: {stats['working']}")
        print(f"Avg success rate: {stats['success_rate_avg']:.2%}")


if __name__ == '__main__':
    import sys
    sys.exit(main())
