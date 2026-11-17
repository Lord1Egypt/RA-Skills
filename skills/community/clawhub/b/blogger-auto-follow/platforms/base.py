# -*- coding: utf-8 -*-
"""
多平台自动化关注基类 (支持博主主页链接与元数据捕获)
"""

from typing import Tuple, Dict

class BasePlatform:
    name = "base"
    display_name = "未知平台"
    home_url = ""

    def get_search_url(self, blogger_name: str) -> str:
        raise NotImplementedError

    def dismiss_popups(self, page):
        """关闭页面干扰弹窗"""
        pass

    def check_captcha(self, page) -> bool:
        """检查是否存在验证码"""
        return False

    def handle_follow(self, page, blogger_name: str) -> Tuple[str, str, Dict]:
        """
        执行搜索后的识别与关注
        返回: (status: str, message: str, meta: Dict)
        status: "SUCCESS" | "ALREADY_FOLLOWED" | "NOT_FOUND" | "FAILED"
        meta: { "profile_url": str, "unique_id": str, "bio": str }
        """
        raise NotImplementedError
