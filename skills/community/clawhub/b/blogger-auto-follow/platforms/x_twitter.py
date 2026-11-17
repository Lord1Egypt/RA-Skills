# -*- coding: utf-8 -*-
"""
X (Twitter) 平台自动化关注适配器 (支持主页直达链接抓取)
"""

import urllib.parse
from typing import Tuple, Dict
from .base import BasePlatform


class XPlatform(BasePlatform):
    name = "x"
    display_name = "X (Twitter)"
    home_url = "https://x.com/"

    def get_search_url(self, blogger_name: str) -> str:
        return f"https://x.com/search?q={urllib.parse.quote(blogger_name)}&f=user"

    def dismiss_popups(self, page):
        close_selectors = [
            'button[data-testid="app-bar-close"]',
            'button[aria-label="Close"]',
            'button[aria-label="关闭"]'
        ]
        for sel in close_selectors:
            try:
                for b in page.locator(sel).all():
                    if b.is_visible():
                        b.click(timeout=800)
            except Exception:
                pass

    def check_captcha(self, page) -> bool:
        try:
            return page.locator('iframe[src*="arkoselabs"], #arkose').count() > 0
        except Exception:
            return False

    def handle_follow(self, page, blogger_name: str) -> Tuple[str, str, Dict]:
        self.dismiss_popups(page)

        meta = {
            "profile_url": "",
            "unique_id": "",
            "bio": ""
        }

        # 1. 查找用户卡片
        card_selectors = [
            'div[data-testid="UserCell"]',
            'div[data-testid="cellInnerDiv"]'
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
                    if blogger_name in text or any(k in text for k in blogger_name.split() if len(k) > 1):
                        target_card = c
                        break
                except Exception:
                    pass
        if not target_card:
            return "NOT_FOUND", "未找到与名单名称匹配的用户，未执行关注", meta
        scope = target_card

        # 提取 X 个人主页与 handle
        if target_card:
            try:
                link_elem = target_card.locator('a[role="link"][href^="/"]').first
                if link_elem and link_elem.count() > 0:
                    href = link_elem.get_attribute("href") or ""
                    if href and not any(p in href for p in ["/home", "/explore", "/notifications", "/messages"]):
                        meta["profile_url"] = "https://x.com" + href
                        meta["unique_id"] = href.replace("/", "@")
            except Exception:
                pass

        # 2. 检查是否已关注
        already_selectors = [
            'button[data-testid$="-unfollow"]',
            'button:has-text("Following")',
            'button:has-text("正在关注")',
            'button:has-text("已关注")'
        ]
        for sel in already_selectors:
            try:
                for m in scope.locator(sel).all():
                    if m.is_visible():
                        status_text = m.inner_text().strip()
                        return "ALREADY_FOLLOWED", f"已处于关注状态 ({status_text})", meta
            except Exception:
                pass

        # 3. 查找“关注/Follow”按钮
        follow_selectors = [
            'button[data-testid$="-follow"]',
            'button:text-is("Follow")',
            'button:text-is("关注")'
        ]
        for sel in follow_selectors:
            try:
                for btn in scope.locator(sel).all():
                    if btn.is_visible():
                        txt = btn.inner_text().strip()
                        if "Follow" in txt or "关注" in txt:
                            btn.scroll_into_view_if_needed()
                            btn.click()
                            try:
                                new_text = btn.inner_text().strip()
                                return "SUCCESS", f"关注成功 ({new_text})", meta
                            except Exception:
                                return "SUCCESS", "已点击关注", meta
            except Exception:
                pass

        return "NOT_FOUND", "未找到匹配用户或 Follow 按钮", meta
