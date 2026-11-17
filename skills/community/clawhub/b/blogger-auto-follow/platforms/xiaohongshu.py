# -*- coding: utf-8 -*-
"""
小红书 (RED) 平台自动化关注适配器 (支持主页直达链接抓取)
"""

import urllib.parse
import time
from typing import Tuple, Dict
from .base import BasePlatform


class XiaohongshuPlatform(BasePlatform):
    name = "xiaohongshu"
    display_name = "小红书 (Xiaohongshu)"
    home_url = "https://www.xiaohongshu.com/"
    # Search-result cards currently expose the profile URL on their primary anchor.
    # Do not use this selector for a generic page-ready check: the sidebar's "我"
    # link uses the same URL pattern and can be present before search results render.
    profile_link_selector = 'div.onebox a[href*="/user/profile/"]'
    result_wait_seconds = 17.5
    result_poll_seconds = 0.5

    def get_search_url(self, blogger_name: str) -> str:
        return f"https://www.xiaohongshu.com/search_result?keyword={urllib.parse.quote(blogger_name)}&type=user"

    def dismiss_popups(self, page):
        close_selectors = [
            '.close-button',
            'div[class*="close"]',
            'svg[class*="close"]',
            'button:has-text("我知道了")'
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
            return page.locator('.captcha-modal, div[class*="captcha"]').count() > 0
        except Exception:
            return False

    def _find_matching_card(self, page, blogger_name: str):
        """Wait for a rendered search-result card matching ``blogger_name``.

        Small Red Book renders its search results after ``domcontentloaded``.  In
        particular, waiting for any profile link is unsafe because the persistent
        sidebar contains the current user's profile link.  Limit the query to a
        ``div.onebox`` result card and poll for at most 17.5 seconds.
        """
        name_parts = [part for part in blogger_name.split() if len(part) > 1]
        deadline = time.monotonic() + self.result_wait_seconds

        while True:
            try:
                for link in page.locator(self.profile_link_selector).all():
                    card = link.locator('xpath=ancestor::div[contains(concat(" ", normalize-space(@class), " "), " onebox ")][1]')
                    text = card.inner_text()
                    if blogger_name in text or any(part in text for part in name_parts):
                        return card, link
            except Exception:
                # The result grid may be replaced while the SPA is rendering.
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

        # 1. 等待并查找当前搜索页的用户卡片（排除侧边栏个人资料链接）。
        target_card, profile_link = self._find_matching_card(page, blogger_name)
        if not target_card:
            return "NOT_FOUND", "未找到与名单名称匹配的博主，未执行关注", meta
        scope = target_card

        # 提取个人主页链接
        try:
            href = profile_link.get_attribute("href") or ""
            if href.startswith("/"):
                meta["profile_url"] = "https://www.xiaohongshu.com" + href
            elif href.startswith("http"):
                meta["profile_url"] = href
            # 提取 user id
            meta["unique_id"] = href.split("/user/profile/")[-1].split("?")[0]
        except Exception:
            pass

        # 2. 检查是否已关注
        already_selectors = [
            'button:has-text("已关注")',
            'button:has-text("互相关注")',
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

        # 3. 查找“关注”按钮
        all_btns = scope.locator('button, div[role="button"]').all()
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

        return "NOT_FOUND", "未找到匹配博主或关注按钮", meta
