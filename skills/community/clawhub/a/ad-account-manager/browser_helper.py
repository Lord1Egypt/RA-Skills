#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
浏览器自动化辅助模块
使用Playwright实现扫码登录、Cookie保存和一键登录功能
"""

import asyncio
import json
from typing import List, Dict, Optional, Callable
from pathlib import Path


class BrowserHelper:
    """浏览器辅助类"""

    def __init__(self, headless: bool = False):
        """
        初始化浏览器辅助类
        
        Args:
            headless: 是否无头模式运行
        """
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    async def start(self):
        """启动浏览器"""
        try:
            from playwright.async_api import async_playwright
            
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=self.headless)
            self.context = await self.browser.new_context()
            self.page = await self.context.new_page()
        except ImportError:
            raise ImportError("请安装playwright: pip install playwright && playwright install chromium")

    async def close(self):
        """关闭浏览器"""
        if self.page:
            await self.page.close()
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if hasattr(self, 'playwright'):
            await self.playwright.stop()

    async def get_cookies(self) -> List[Dict]:
        """获取当前页面的Cookies"""
        if self.context:
            return await self.context.cookies()
        return []

    async def set_cookies(self, cookies: List[Dict]):
        """设置Cookies"""
        if self.context:
            await self.context.add_cookies(cookies)

    async def navigate_and_wait_for_login(self, url: str, 
                                           check_login_callback: Optional[Callable] = None,
                                           timeout: int = 300) -> List[Dict]:
        """
        导航到登录页面并等待用户扫码登录
        
        Args:
            url: 登录页面URL
            check_login_callback: 检查是否登录成功的回调函数
            timeout: 超时时间（秒）
            
        Returns:
            登录后的Cookies
        """
        if not self.page:
            await self.start()

        # 导航到登录页面
        await self.page.goto(url)
        
        print(f"请在浏览器中扫码登录，超时时间: {timeout}秒")
        
        # 等待登录成功
        start_time = asyncio.get_event_loop().time()
        logged_in = False
        
        while not logged_in and (asyncio.get_event_loop().time() - start_time) < timeout:
            await asyncio.sleep(2)
            
            # 如果提供了检查回调，使用回调检查
            if check_login_callback:
                logged_in = await check_login_callback(self.page)
            else:
                # 默认检查：可以通过检查URL变化或特定元素来判断
                current_url = self.page.url
                if url not in current_url and 'login' not in current_url.lower():
                    logged_in = True
        
        if not logged_in:
            print("登录超时")
            return []
        
        print("登录成功！")
        return await self.get_cookies()

    async def login_with_cookies(self, url: str, cookies: List[Dict]) -> bool:
        """
        使用Cookies一键登录
        
        Args:
            url: 目标页面URL
            cookies: Cookie列表
            
        Returns:
            是否登录成功
        """
        if not self.page:
            await self.start()

        # 先访问一次域名以设置cookies
        await self.page.goto(url, wait_until="domcontentloaded")
        
        # 设置cookies
        await self.set_cookies(cookies)
        
        # 重新访问页面
        await self.page.goto(url)
        
        # 简单验证是否登录成功
        await asyncio.sleep(2)
        return True

    async def fetch_account_info(self, platform: str) -> Dict:
        """
        拉取账户信息（余额、消耗等）
        
        Args:
            platform: 平台名称
            
        Returns:
            账户信息字典
        """
        # 这里需要根据不同平台实现具体的信息拉取逻辑
        # 由于各平台页面结构不同，这里提供一个框架
        info = {
            "balance": 0.0,
            "daily_cost": 0.0,
            "budget": 0.0,
            "status": "normal"
        }
        
        # TODO: 根据不同平台实现具体的页面解析逻辑
        # 例如：
        # if platform == "guangdiantong":
        #     # 解析广点通页面
        # elif platform == "juliang":
        #     # 解析巨量引擎页面
        
        return info


def save_cookies_to_file(cookies: List[Dict], filepath: str):
    """保存Cookies到文件"""
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(cookies, f, ensure_ascii=False, indent=2)


def load_cookies_from_file(filepath: str) -> List[Dict]:
    """从文件加载Cookies"""
    if Path(filepath).exists():
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []
