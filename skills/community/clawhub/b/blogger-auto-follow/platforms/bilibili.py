# -*- coding: utf-8 -*-
"""
Bilibili (B站) 平台自动化关注适配器 (支持主页直达链接抓取)
"""

import urllib.parse
from typing import Tuple, Dict
from .base import BasePlatform


class BilibiliPlatform(BasePlatform):
    name = "bilibili"
    display_name = "哔哩哔哩 (Bilibili)"
    home_url = "https://www.bilibili.com/"

    def get_search_url(self, blogger_name: str) -> str:
        return f"https://search.bilibili.com/upuser?keyword={urllib.parse.quote(blogger_name)}"

    def dismiss_popups(self, page):
        close_selectors = [
            '.bili-mini-mask',
            '.bili-dialog-m-close',
            'button:has-text("我知道了")',
            '.close-btn'
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
            return page.locator('.geetest_slider, .geetest_holder, #geetest-wrap').count() > 0
        except Exception:
            return False

    def handle_follow(self, page, blogger_name: str) -> Tuple[str, str, Dict]:
        self.dismiss_popups(page)

        meta = {
            "profile_url": "",
            "unique_id": "",
            "bio": ""
        }

        # 1. 查找 UP 主卡片
        card_selectors = [
            'li.user-item',
            'div.user-item',
            'div[class*="user-item"]',
            '.up-item'
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
            return "NOT_FOUND", "未找到与名单名称匹配的 UP 主，未执行关注", meta
        scope = target_card

        # 提取空间主页链接
        if target_card:
            try:
                link_elem = target_card.locator('a[href*="space.bilibili.com"]').first
                if link_elem and link_elem.count() > 0:
                    href = link_elem.get_attribute("href") or ""
                    if href.startswith("//"):
                        meta["profile_url"] = "https:" + href
                    elif href.startswith("http"):
                        meta["profile_url"] = href
                    # 提取 UID
                    for part in href.split("/"):
                        if part.isdigit():
                            meta["unique_id"] = part
                            break
            except Exception:
                pass

        # 2. 检查是否已关注
        already_selectors = [
            'button:has-text("已关注")',
            'button:has-text("已互粉")',
            'span:text-is("已关注")',
            'span:text-is("已互粉")'
        ]
        for sel in already_selectors:
            try:
                for m in scope.locator(sel).all():
                    if m.is_visible():
                        status_text = m.inner_text().strip()
                        return "ALREADY_FOLLOWED", f"已处于关注状态 ({status_text})", meta
            except Exception:
                pass

        # 3. 查找“关注”按钮并点击
        follow_selectors = [
            'button:has-text("关注")',
            'button:has-text("+ 关注")',
            'button:has-text("+关注")',
            'div[class*="follow-btn"]'
        ]
        for sel in follow_selectors:
            try:
                for btn in scope.locator(sel).all():
                    if btn.is_visible():
                        txt = btn.inner_text().strip()
                        if "关注" in txt and "已" not in txt:
                            btn.scroll_into_view_if_needed()
                            btn.click()
                            try:
                                new_text = btn.inner_text().strip()
                                return "SUCCESS", f"关注成功 ({new_text})", meta
                            except Exception:
                                return "SUCCESS", "已点击关注", meta
            except Exception:
                pass

        return "NOT_FOUND", "未找到匹配 UP 主或关注按钮", meta
