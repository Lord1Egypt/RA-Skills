"""Playwright 网页截图"""

import asyncio
from pathlib import Path
from typing import Optional


class ScreenshotCapture:
    """网页截图工具"""

    def __init__(self):
        self._browser = None

    async def _get_browser(self):
        """懒加载 Playwright browser"""
        if self._browser is None:
            from playwright.async_api import async_playwright
            self._pw = await async_playwright().start()
            self._browser = await self._pw.chromium.launch(headless=True)
        return self._browser

    async def capture_github_page(
        self,
        repo_url: str,
        output_path: str,
        width: int = 1200,
        height: int = 1600,
    ) -> str:
        """截取 GitHub 项目首页"""
        browser = await self._get_browser()
        page = await browser.new_page(viewport={"width": width, "height": height})
        try:
            await page.goto(repo_url, wait_until="networkidle", timeout=30000)
            # 等待 README 加载
            await page.wait_for_selector("article", timeout=10000)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=output_path, full_page=False)
            return output_path
        except Exception as e:
            print(f"  ⚠ GitHub 截图失败: {e}")
            return ""
        finally:
            await page.close()

    async def capture_url(
        self,
        url: str,
        output_path: str,
        width: int = 1200,
        height: int = 1600,
        wait_selector: Optional[str] = None,
    ) -> str:
        """通用网页截图"""
        browser = await self._get_browser()
        page = await browser.new_page(viewport={"width": width, "height": height})
        try:
            await page.goto(url, wait_until="networkidle", timeout=30000)
            if wait_selector:
                await page.wait_for_selector(wait_selector, timeout=10000)
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            await page.screenshot(path=output_path, full_page=False)
            return output_path
        except Exception as e:
            print(f"  ⚠ 网页截图失败: {e}")
            return ""
        finally:
            await page.close()

    async def close(self):
        """关闭浏览器"""
        if self._browser:
            await self._browser.close()
            await self._pw.stop()
            self._browser = None
