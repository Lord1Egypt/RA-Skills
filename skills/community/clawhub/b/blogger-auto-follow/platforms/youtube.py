# -*- coding: utf-8 -*-
"""
YouTube 平台自动化关注/订阅适配器 (支持频道直达链接抓取)
"""

import urllib.parse
from typing import Tuple, Dict
from .base import BasePlatform


class YouTubePlatform(BasePlatform):
    name = "youtube"
    display_name = "YouTube"
    home_url = "https://www.youtube.com/"

    def get_search_url(self, blogger_name: str) -> str:
        return f"https://www.youtube.com/results?search_query={urllib.parse.quote(blogger_name)}&sp=EgIQAg%253D%253D"

    def dismiss_popups(self, page):
        close_selectors = [
            'button[aria-label="关闭"]',
            'button[aria-label="Close"]',
            'button:has-text("暂不")',
            'button:has-text("No thanks")'
        ]
        for sel in close_selectors:
            try:
                for b in page.locator(sel).all():
                    if b.is_visible():
                        b.click(timeout=800)
            except Exception:
                pass

    def check_captcha(self, page) -> bool:
        return False

    def handle_follow(self, page, blogger_name: str) -> Tuple[str, str, Dict]:
        self.dismiss_popups(page)

        meta = {
            "profile_url": "",
            "unique_id": "",
            "bio": ""
        }

        # 1. 查找频道卡片
        card_selectors = [
            'ytd-channel-renderer',
            'ytd-video-renderer',
            'div#channel'
        ]
        cards = []
        for sel in card_selectors:
            try:
                found = page.locator(sel).all()
                if found:
                    cards = found
                    break
            except Exception:
                pass

        target_card = None
        if cards:
            for c in cards[:4]:
                try:
                    text = c.inner_text()
                    if blogger_name.lower() in text.lower():
                        target_card = c
                        break
                except Exception:
                    pass
        if not target_card:
            return "NOT_FOUND", "未找到与名单名称匹配的频道，未执行订阅", meta
        scope = target_card

        # 提取频道主页链接
        if target_card:
            try:
                link_elem = target_card.locator('a#main-link, a[href^="/@"], a[href*="/channel/"]').first
                if link_elem and link_elem.count() > 0:
                    href = link_elem.get_attribute("href") or ""
                    if href.startswith("/"):
                        meta["profile_url"] = "https://www.youtube.com" + href
                    elif href.startswith("http"):
                        meta["profile_url"] = href
                    if "/@" in href:
                        meta["unique_id"] = "@" + href.split("/@")[-1]
            except Exception:
                pass

        # 2. 检查是否已订阅
        already_selectors = [
            'button:has-text("已订阅")',
            'button:has-text("Subscribed")',
            'yt-button-shape:has-text("已订阅")',
            'yt-button-shape:has-text("Subscribed")'
        ]
        for sel in already_selectors:
            try:
                for m in scope.locator(sel).all():
                    if m.is_visible():
                        status_text = m.inner_text().strip()
                        return "ALREADY_FOLLOWED", f"已处于订阅状态 ({status_text})", meta
            except Exception:
                pass

        # 3. 查找“订阅/Subscribe”按钮
        subscribe_selectors = [
            'button:has-text("订阅")',
            'button:has-text("Subscribe")',
            'yt-button-shape:has-text("订阅")',
            'yt-button-shape:has-text("Subscribe")'
        ]
        for sel in subscribe_selectors:
            try:
                for btn in scope.locator(sel).all():
                    if btn.is_visible():
                        txt = btn.inner_text().strip()
                        if "已" not in txt and ("订阅" in txt or "Subscribe" in txt):
                            btn.scroll_into_view_if_needed()
                            btn.click()
                            try:
                                new_text = btn.inner_text().strip()
                                return "SUCCESS", f"订阅成功 ({new_text})", meta
                            except Exception:
                                return "SUCCESS", "已点击订阅", meta
            except Exception:
                pass

        return "NOT_FOUND", "未找到匹配频道或订阅按钮", meta
