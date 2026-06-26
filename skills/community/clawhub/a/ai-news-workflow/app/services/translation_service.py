from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from app.models.news_item import NewsItem
from app.parsers.content_cleaner import ContentCleaner
from app.utils.hash_utils import build_content_hash
from app.utils.text_utils import normalize_title


@dataclass
class TranslationResult:
    text: str
    translated: bool
    backend: str


class BaseTranslatorBackend:
    """
    翻译后端抽象类。
    """

    name = "base"

    def translate_to_zh(self, text: str) -> TranslationResult:
        raise NotImplementedError


class PassthroughTranslatorBackend(BaseTranslatorBackend):
    """
    占位后端：
    - 中文原样返回
    - 非中文也原样返回
    适合在未接入真实翻译服务时保证流程可运行。
    """

    name = "passthrough"

    def translate_to_zh(self, text: str) -> TranslationResult:
        return TranslationResult(text=text, translated=False, backend=self.name)


class DeepTranslatorBackend(BaseTranslatorBackend):
    """
    可选翻译后端。
    依赖:
        pip install deep-translator

    说明：
    - 若环境中未安装 deep_translator，会在初始化时报错
    - 这里只做 en -> zh-CN / auto -> zh-CN 的简单调用
    """

    name = "deep_translator"

    def __init__(self, source: str = "auto", target: str = "zh-CN") -> None:
        from deep_translator import GoogleTranslator  # type: ignore
        self._translator = GoogleTranslator(source=source, target=target)

    def translate_to_zh(self, text: str) -> TranslationResult:
        if not text or not text.strip():
            return TranslationResult(text="", translated=False, backend=self.name)

        translated_text = self._translator.translate(text)
        return TranslationResult(
            text=(translated_text or "").strip(),
            translated=True,
            backend=self.name,
        )


class TranslationService:
    """
    统一翻译服务。

    处理策略：
    - 保留原文字段
    - 生成中文字段
    - 再把 item.title / item.summary / item.cleaned_content 覆盖为中文版本
      以兼容当前已有的匹配、分类、去重逻辑
    """

    def __init__(
        self,
        backend: Optional[BaseTranslatorBackend] = None,
    ) -> None:
        self.backend = backend or self._build_default_backend()
        self.cleaner = ContentCleaner()

    def process_items(self, items: List[NewsItem]) -> List[NewsItem]:
        for item in items:
            self.process_item(item)
        return items

    def process_item(self, item: NewsItem) -> NewsItem:
        # 1. 先保留原文
        item.original_title = item.title or ""
        item.original_summary = item.summary or ""
        item.original_cleaned_content = item.cleaned_content or item.raw_content or ""

        # 2. 识别语言（优先看标题+摘要）
        language_sample = " ".join([
            item.original_title or "",
            item.original_summary or "",
        ]).strip()

        item.original_language = self.detect_language(language_sample)

        # 3. 生成中文字段
        if item.original_language == "zh":
            item.title_zh = self.cleaner.clean_text(item.original_title)
            item.summary_zh = self.cleaner.clean_summary(item.original_summary, max_length=300)
            item.cleaned_content_zh = self.cleaner.clean_text(item.original_cleaned_content)
            item.is_machine_translated = False
            item.translation_backend = "none"
        else:
            item.title_zh = self._translate_text(item.original_title, max_length=None)
            item.summary_zh = self._translate_text(item.original_summary, max_length=300)
            item.cleaned_content_zh = self._translate_text(item.original_cleaned_content, max_length=None)
            item.is_machine_translated = True
            item.translation_backend = self.backend.name

        # 4. 中文字段兜底
        item.title_zh = item.title_zh or self.cleaner.clean_text(item.original_title)
        item.summary_zh = item.summary_zh or self.cleaner.clean_summary(item.original_summary, max_length=300)
        item.cleaned_content_zh = item.cleaned_content_zh or self.cleaner.clean_text(item.original_cleaned_content)

        # 5. 为兼容现有链路，把当前主字段覆盖为中文
        item.title = item.title_zh or item.title or ""
        item.summary = item.summary_zh or item.summary or ""
        item.cleaned_content = item.cleaned_content_zh or item.cleaned_content or ""

        # 6. 生成中文去重字段
        item.normalized_title = normalize_title(item.title_zh or item.title or "")
        item.content_hash = build_content_hash(
            title=item.title_zh or item.title,
            summary=item.summary_zh or item.summary,
            content=item.cleaned_content_zh or item.cleaned_content,
        )

        return item

    def _translate_text(self, text: str, max_length: Optional[int] = None) -> str:
        cleaned = self.cleaner.clean_text(text)
        if not cleaned:
            return ""

        try:
            result = self.backend.translate_to_zh(cleaned)
            translated = self.cleaner.clean_text(result.text)
        except Exception:
            translated = cleaned

        if max_length and len(translated) > max_length:
            translated = translated[: max_length - 1].rstrip() + "…"

        return translated

    @staticmethod
    def detect_language(text: str) -> str:
        """
        简单语言识别：
        - 中文字符占比高 -> zh
        - 英文字母占比高 -> en
        - 否则 unknown
        """
        if not text or not text.strip():
            return "unknown"

        text = text.strip()

        zh_count = sum(1 for ch in text if "\u4e00" <= ch <= "\u9fff")
        en_count = sum(1 for ch in text if ("a" <= ch.lower() <= "z"))

        if zh_count >= 2 and zh_count >= en_count:
            return "zh"
        if en_count >= 3:
            return "en"
        return "unknown"

    @staticmethod
    def _build_default_backend() -> BaseTranslatorBackend:
        """
        默认后端：
        - 优先尝试 deep_translator
        - 不可用则回退为 passthrough
        """
        try:
            return DeepTranslatorBackend()
        except Exception:
            return PassthroughTranslatorBackend()