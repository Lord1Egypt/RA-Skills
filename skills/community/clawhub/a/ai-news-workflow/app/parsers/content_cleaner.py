from __future__ import annotations

import html
import re
from typing import Optional

from bs4 import BeautifulSoup


class ContentCleaner:
    """
    内容清洗器。
    适用于 RSS summary、网页正文摘要等。
    """

    def __init__(self) -> None:
        self.noise_patterns = [
            r"click here to read more",
            r"read more\.?",
            r"continue reading\.?",
            r"本文来自.*",
            r"责任编辑[:：].*",
            r"来源[:：].*",
        ]

    def clean_text(self, text: Optional[str]) -> str:
        if not text:
            return ""

        text = str(text)

        # 1. HTML实体解码
        text = html.unescape(text)

        # 2. 去HTML标签
        text = self._strip_html(text)

        # 3. 去噪音
        text = self._remove_noise(text)

        # 4. 统一空白
        text = self._normalize_whitespace(text)

        return text.strip()

    def clean_summary(self, text: Optional[str], max_length: int = 300) -> str:
        """
        清理摘要并按最大长度截断。
        """
        text = self.clean_text(text)
        if len(text) > max_length:
            return text[: max_length - 1].rstrip() + "…"
        return text

    @staticmethod
    def _strip_html(text: str) -> str:
        soup = BeautifulSoup(text, "lxml")
        return soup.get_text(separator=" ", strip=True)

    def _remove_noise(self, text: str) -> str:
        cleaned = text
        for pattern in self.noise_patterns:
            cleaned = re.sub(pattern, "", cleaned, flags=re.IGNORECASE)
        return cleaned

    @staticmethod
    def _normalize_whitespace(text: str) -> str:
        # 把各种空白统一为单个空格
        text = re.sub(r"\s+", " ", text)
        # 去掉中英文标点前多余空格
        text = re.sub(r"\s+([,.;:!?，。；：！？])", r"\1", text)
        return text