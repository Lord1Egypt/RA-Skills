#!/usr/bin/env python3
"""
collectors/adapters/extraction/spawait.py - SPA动态等待策略

提供智能动态等待能力:
1. 网络idle检测（NetworkIdle）
2. DOM变化稳定检测（MutationObserver）
3. 关键元素出现检测
4. 站点级配置（spa_sites.json 扩展）
5. 超时兜底

Usage:
    from collectors.adapters.extraction.spawait import SPAWaitStrategy, wait_for_page_ready

    strategy = SPAWaitStrategy()
    result = strategy.wait_until_ready(page, url)
    print(f"等待成功: {result.success}, 策略: {result.wait_strategy}")
"""

import asyncio
import time
import json
import re
from typing import Optional, Dict, Any, List
from pathlib import Path
from dataclasses import dataclass


@dataclass
class SPAConfig:
    """SPA站点配置"""
    render_strategy: str = "networkidle"  # networkidle | dom_stable | selector | fixed
    wait_for_selector: Optional[str] = None
    stable_check: bool = True
    timeout: float = 30.0
    wait_time: float = 0  # 固定等待时间（秒），0表示不等待


@dataclass
class WaitResult:
    """等待结果"""
    success: bool
    reason: str
    elapsed_time: float
    wait_strategy: str


class SPAWaitStrategy:
    """SPA动态等待策略"""

    def __init__(self, config_path: Optional[str] = None):
        """
        初始化SPA等待策略

        Args:
            config_path: spa_sites.json 路径
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent.parent.parent / "spa_sites.json"

        self.config_path = Path(config_path)
        self.site_configs: Dict[str, SPAConfig] = {}
        self._load_config()

    def _load_config(self) -> None:
        """加载站点配置"""
        if self.config_path.exists():
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    raw_config = json.load(f)

                # 转换旧格式到新格式
                for site, config in raw_config.items():
                    if isinstance(config, dict):
                        self.site_configs[site] = SPAConfig(
                            render_strategy=config.get('render_strategy', 'networkidle'),
                            wait_for_selector=config.get('wait_for_selector'),
                            stable_check=config.get('stable_check', True),
                            timeout=config.get('timeout', 30.0),
                            wait_time=config.get('wait_time', 0)
                        )
            except Exception as e:
                print(f"⚠️ 加载SPA配置失败: {e}")

        # 默认配置
        self.default_config = SPAConfig(
            render_strategy="networkidle",
            stable_check=True,
            timeout=30.0
        )

    def _get_site_config(self, url: str) -> SPAConfig:
        """获取站点的等待配置"""
        # 从URL提取域名
        domain_match = re.search(r'https?://([^/]+)', url)
        if not domain_match:
            return self.default_config

        domain = domain_match.group(1)

        # 精确匹配
        if domain in self.site_configs:
            return self.site_configs[domain]

        # 通配符匹配（如 *.aliyun.com）
        for site_pattern, config in self.site_configs.items():
            if site_pattern.startswith('*.'):
                base_domain = site_pattern[2:]
                if domain.endswith(base_domain):
                    return config

        return self.default_config

    async def wait_until_ready(
        self,
        page,
        url: str,
        timeout: Optional[float] = None
    ) -> WaitResult:
        """
        等待页面渲染完成

        Args:
            page: Playwright Page对象
            url: 页面URL
            timeout: 超时时间（秒）

        Returns:
            WaitResult: 等待结果
        """
        start_time = time.time()
        config = self._get_site_config(url)

        if timeout is None:
            timeout = config.timeout

        strategy = config.render_strategy

        try:
            if strategy == "networkidle":
                success = await self._wait_networkidle(page, timeout)
                reason = "network idle" if success else "timeout"
            elif strategy == "dom_stable":
                success = await self._wait_dom_stable(page, timeout)
                reason = "dom stable" if success else "timeout"
            elif strategy == "selector":
                success = await self._wait_selector(page, config.wait_for_selector, timeout)
                reason = f"selector {config.wait_for_selector}" if success else "timeout"
            elif strategy == "fixed":
                if config.wait_time > 0:
                    await asyncio.sleep(config.wait_time)
                success = True
                reason = f"fixed {config.wait_time}s"
            else:
                # 默认networkidle
                success = await self._wait_networkidle(page, timeout)
                reason = "network idle" if success else "timeout"

            elapsed = time.time() - start_time

            return WaitResult(
                success=success,
                reason=reason,
                elapsed_time=elapsed,
                wait_strategy=strategy
            )

        except Exception as e:
            elapsed = time.time() - start_time
            return WaitResult(
                success=False,
                reason=f"error: {str(e)[:50]}",
                elapsed_time=elapsed,
                wait_strategy=strategy
            )

    async def _wait_networkidle(self, page, timeout: float) -> bool:
        """等待网络空闲"""
        try:
            # 等待网络空闲（2秒内无新网络请求）
            await page.wait_for_load_state(
                state="networkidle",
                timeout=timeout * 1000  # Playwright用毫秒
            )
            return True
        except Exception:
            return False

    async def _wait_dom_stable(self, page, timeout: float) -> bool:
        """等待DOM内容稳定"""
        start = time.time()
        last_content = ""
        stable_count = 0
        check_interval = 0.5  # 0.5秒检查一次
        required_stable = 3   # 需要3次稳定才认为稳定

        while time.time() - start < timeout:
            try:
                # 获取当前页面内容长度
                content_length = await page.evaluate("""
                    document.body ? document.body.innerHTML.length : 0
                """)

                current_content = str(content_length)

                if current_content == last_content:
                    stable_count += 1
                    if stable_count >= required_stable:
                        return True
                else:
                    stable_count = 0
                    last_content = current_content

                await asyncio.sleep(check_interval)

            except Exception:
                await asyncio.sleep(check_interval)
                continue

        return False

    async def _wait_selector(
        self,
        page,
        selector: Optional[str],
        timeout: float
    ) -> bool:
        """等待关键选择器出现"""
        if not selector:
            return await self._wait_networkidle(page, timeout)

        try:
            await page.wait_for_selector(
                selector,
                timeout=timeout * 1000,
                state="visible"
            )
            return True
        except Exception:
            return False

    def is_content_stable(self, page, interval: float = 0.5, samples: int = 3) -> bool:
        """
        同步版本：检测内容是否稳定

        Args:
            page: Playwright Page对象
            interval: 检查间隔（秒）
            samples: 采样次数

        Returns:
            bool: 内容是否稳定
        """
        # 获取初始内容长度
        try:
            last_length = page.evaluate("document.body ? document.body.innerHTML.length : 0")
        except:
            return True

        for _ in range(samples - 1):
            time.sleep(interval)
            try:
                current_length = page.evaluate("document.body ? document.body.innerHTML.length : 0")
                if current_length != last_length:
                    return False
                last_length = current_length
            except:
                return True

        return True

    def get_config_for_url(self, url: str) -> SPAConfig:
        """获取URL对应的配置（供调试用）"""
        return self._get_site_config(url)


def wait_for_page_ready(
    page,
    url: str,
    config_path: Optional[str] = None,
    timeout: Optional[float] = None
) -> WaitResult:
    """
    同步入口函数，供 BrowserCollector 调用

    Args:
        page: Playwright Page对象
        url: 页面URL
        config_path: spa_sites.json 路径
        timeout: 超时时间（秒）

    Returns:
        WaitResult: 等待结果
    """
    strategy = SPAWaitStrategy(config_path)

    # 同步调用异步方法
    try:
        loop = asyncio.get_running_loop()
        # 如果已经有运行中的loop，使用线程池执行
        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future = executor.submit(
                asyncio.run,
                strategy.wait_until_ready(page, url, timeout)
            )
            return future.result()
    except RuntimeError:
        # 没有运行中的loop，可以安全创建
        return asyncio.run(strategy.wait_until_ready(page, url, timeout))