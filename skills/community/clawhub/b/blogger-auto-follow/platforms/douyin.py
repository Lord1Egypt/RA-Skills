# -*- coding: utf-8 -*-
"""
抖音平台自动化关注适配器 (支持博主主页直达链接抓取)
"""

import urllib.parse
import time
from typing import Tuple, Dict
from .base import BasePlatform


class DouyinPlatform(BasePlatform):
    name = "douyin"
    display_name = "抖音 (Douyin)"
    home_url = "https://www.douyin.com/"
    # douyin.com may redirect to 抖音精选, whose SPA populates user results well
    # after ``domcontentloaded``.  Keep these selectors scoped to result cards;
    # the persistent navigation's “我的” link is not a search result.
    result_card_selectors = [
        'div[data-e2e="search-user-item"]',
        '[data-e2e*="search"] [class*="user-card"]',
        '[data-e2e*="search"] [class*="user-info-card"]',
        '[data-e2e*="search"] [class*="search-result-card"]',
        'main [class*="search"] [class*="user-card"]',
        'main [class*="search"] [class*="user-info-card"]',
        'main [class*="search"] [class*="search-result-card"]',
    ]
    result_wait_seconds = 22
    result_poll_seconds = 0.5

    def get_search_url(self, blogger_name: str) -> str:
        return f"https://www.douyin.com/search/{urllib.parse.quote(blogger_name)}?type=user"

    def dismiss_popups(self, page):
        close_selectors = [
            'div[class*="close"]',
            'svg[class*="close"]',
            'div[data-e2e="modal-close-icon"]',
            '.dy-account-close',
            'button:has-text("我知道了")',
            'button:has-text("稍后再说")'
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
            loc = page.locator(".secsdk-captcha-drag-icon, #captcha-verify-image, .captcha_verify_container, div[class*='captcha']")
            return loc.count() > 0
        except Exception:
            return False

    def _find_matching_card(self, page, blogger_name: str):
        """Wait for a matching user card in the asynchronously rendered results.

        The 抖音精选 redirect preserves the search as an SPA view.  Do not use a
        generic user/profile anchor as a readiness signal: navigation already
        contains one before the search results appear.
        """
        name_parts = [part for part in blogger_name.split() if len(part) > 1]
        deadline = time.monotonic() + self.result_wait_seconds

        while True:
            try:
                for selector in self.result_card_selectors:
                    for card in page.locator(selector).all():
                        if not card.is_visible():
                            continue
                        # A search user result must expose a user-profile link.
                        # This filters search-layout wrappers and sidebar entries.
                        profile_link = card.locator('a[href*="/user/"]').first
                        if profile_link.count() == 0:
                            continue
                        text = card.inner_text()
                        if blogger_name in text or any(part in text for part in name_parts):
                            return card, profile_link
            except Exception:
                # The result list can be replaced during SPA hydration.
                pass

            if time.monotonic() >= deadline:
                return None, None
            try:
                page.wait_for_timeout(int(self.result_poll_seconds * 1000))
            except Exception:
                time.sleep(self.result_poll_seconds)

    def handle_follow(self, page, blogger_name: str) -> Tuple[str, str, Dict]:
        self.dismiss_popups(page)

        meta = {
            "profile_url": "",
            "unique_id": "",
            "bio": ""
        }

        # 1. Wait for the current search view's user card.  A redirect to
        # 抖音精选 may leave this empty for 10–20 seconds after navigation.
        target_card, profile_link = self._find_matching_card(page, blogger_name)
        if not target_card:
            return "NOT_FOUND", "未找到与名单名称匹配的用户，未执行关注", meta
        scope = target_card

        # 提取主页链接与简介
        if target_card:
            try:
                if profile_link and profile_link.count() > 0:
                    href = profile_link.get_attribute("href") or ""
                    if href.startswith("//"):
                        meta["profile_url"] = "https:" + href
                    elif href.startswith("/"):
                        meta["profile_url"] = "https://www.douyin.com" + href
                    elif href.startswith("http"):
                        meta["profile_url"] = href
            except Exception:
                pass

            try:
                card_text = target_card.inner_text()
                # 尝试提取抖音号
                for line in card_text.split("\n"):
                    if "抖音号：" in line or "抖音号:" in line:
                        meta["unique_id"] = line.replace("抖音号：", "").replace("抖音号:", "").strip()
            except Exception:
                pass

        # 2. 检查是否已关注
        already_selectors = [
            'button:has-text("已关注")',
            'button:has-text("互相关注")',
            'button:has-text("特别关注")',
            'div[role="button"]:has-text("已关注")',
            'div[role="button"]:has-text("互相关注")',
            'span:text-is("已关注")',
            'span:text-is("互相关注")'
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
        all_btns = scope.locator('button, div[role="button"], span[class*="follow"]').all()
        for btn in all_btns:
            try:
                if btn.is_visible():
                    txt = btn.inner_text().strip()
                    if txt in ["关注", "+ 关注", "+关注", "加关注"]:
                        btn.scroll_into_view_if_needed()
                        btn.click()
                        try:
                            new_text = btn.inner_text().strip()
                            return "SUCCESS", f"关注成功 ({new_text})", meta
                        except Exception:
                            return "SUCCESS", "已点击关注", meta
            except Exception:
                pass

        return "NOT_FOUND", "未找到匹配用户或关注按钮", meta
