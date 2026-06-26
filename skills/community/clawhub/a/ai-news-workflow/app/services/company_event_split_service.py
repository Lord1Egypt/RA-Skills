from __future__ import annotations

import copy
import re
from typing import Dict, List

from app.models.company import Company
from app.models.news_item import NewsItem


class CompanyEventSplitService:
    """
    企业级事件拆分服务。

    目标：
    - 一条资讯只讲一家企业
    - 如果原资讯命中多家企业，则按企业拆分成多条子事件
    - 每条子事件仅保留与该企业直接相关的句子
    """

    def __init__(self, companies: List[Company]) -> None:
        self.companies = companies
        self.company_map: Dict[str, Company] = {c.company_cn: c for c in companies}

    def split_items(self, items: List[NewsItem]) -> List[NewsItem]:
        result: List[NewsItem] = []

        for item in items:
            split_result = self.split_item(item)
            result.extend(split_result)

        return result

    def split_item(self, item: NewsItem) -> List[NewsItem]:
        matched_companies = item.related_companies or []

        # 只命中 0/1 家企业，不拆
        if len(matched_companies) <= 1:
            return [item]

        split_items: List[NewsItem] = []

        for company_name in matched_companies:
            company = self.company_map.get(company_name)
            if not company:
                continue

            sub_item = self._build_company_sub_item(item, company)

            # 若拆不出该企业明确相关的内容，则不生成子项
            if not sub_item:
                continue

            split_items.append(sub_item)

        # 如果一个都没拆出来，回退保留原记录，避免误丢
        if not split_items:
            return [item]

        return split_items

    def _build_company_sub_item(self, item: NewsItem, company: Company) -> NewsItem | None:
        keywords = self._build_company_keywords(company)

        title_source = item.title_zh or item.title or ""
        summary_source = item.summary_zh or item.summary or ""
        content_source = item.cleaned_content_zh or item.cleaned_content or ""

        title_parts = self._split_text_to_segments(title_source, is_title=True)
        summary_sentences = self._split_text_to_segments(summary_source, is_title=False)
        content_sentences = self._split_text_to_segments(content_source, is_title=False)

        matched_title_parts = self._extract_related_segments(title_parts, keywords)
        matched_summary_sentences = self._extract_related_segments(summary_sentences, keywords)
        matched_content_sentences = self._extract_related_segments(content_sentences, keywords)

        # 如果摘要和正文都没有明确提及该企业，不拆这一家
        if not matched_summary_sentences and not matched_content_sentences and not matched_title_parts:
            return None

        new_item = copy.deepcopy(item)

        # 只保留当前企业
        new_item.related_companies = [company.company_cn]

        # 按企业名单国家/地区重新写一级类别和地区
        if self._is_china_company(company):
            new_item.country_region = "中国"
            new_item.category_level_1 = "名单企业动态"
        else:
            new_item.country_region = "国际"
            new_item.category_level_1 = "全球AI产业动态"

        # 重写标题
        new_title = self._build_title(
            company_name=company.company_cn,
            matched_title_parts=matched_title_parts,
            matched_summary_sentences=matched_summary_sentences,
            matched_content_sentences=matched_content_sentences,
        )

        # 重写摘要
        new_summary = self._build_summary(
            matched_summary_sentences=matched_summary_sentences,
            matched_content_sentences=matched_content_sentences,
        )

        # 没有摘要时，用标题兜底
        if not new_summary:
            new_summary = new_title

        new_item.title = new_title
        new_item.summary = new_summary
        new_item.cleaned_content = new_summary

        # 中文字段同步
        new_item.title_zh = new_title
        new_item.summary_zh = new_summary
        new_item.cleaned_content_zh = new_summary

        # 原文标题/摘要不改，便于追溯
        new_item.normalized_title = self._normalize_simple(new_title)

        # 给备注加标记，方便排查
        new_item.remarks = self._append_remark(new_item.remarks, f"已按企业拆分：{company.company_cn}")

        return new_item

    def _build_title(
        self,
        company_name: str,
        matched_title_parts: List[str],
        matched_summary_sentences: List[str],
        matched_content_sentences: List[str],
    ) -> str:
        # 1. 优先用原标题中命中的片段
        if matched_title_parts:
            candidate = self._clean_segment(matched_title_parts[0])
            if candidate:
                # 若片段里没公司名，则补上
                if company_name not in candidate:
                    return f"{company_name}{candidate}"
                return candidate

        # 2. 其次用摘要中第一句
        if matched_summary_sentences:
            sentence = self._clean_segment(matched_summary_sentences[0])
            if sentence:
                return self._compress_to_title(sentence, company_name)

        # 3. 再次用正文中第一句
        if matched_content_sentences:
            sentence = self._clean_segment(matched_content_sentences[0])
            if sentence:
                return self._compress_to_title(sentence, company_name)

        # 4. 最后兜底
        return f"{company_name}相关动态"

    def _build_summary(
        self,
        matched_summary_sentences: List[str],
        matched_content_sentences: List[str],
    ) -> str:
        collected: List[str] = []

        for s in matched_summary_sentences:
            s = self._clean_segment(s)
            if s and s not in collected:
                collected.append(s)

        for s in matched_content_sentences:
            s = self._clean_segment(s)
            if s and s not in collected:
                collected.append(s)

        # 最多保留前2句
        collected = collected[:2]

        if not collected:
            return ""

        summary = " ".join(collected).strip()
        if len(summary) > 220:
            summary = summary[:219].rstrip() + "…"
        return summary

    @staticmethod
    def _split_text_to_segments(text: str, is_title: bool = False) -> List[str]:
        if not text:
            return []

        text = str(text).strip()
        if not text:
            return []

        if is_title:
            # 标题允许按中文顿号/逗号/分号/破折号等切
            parts = re.split(r"[；;｜|/、，,：:]", text)
        else:
            parts = re.split(r"[。！？!?；;\n]", text)

        return [p.strip() for p in parts if p and p.strip()]

    @staticmethod
    def _extract_related_segments(segments: List[str], keywords: List[str]) -> List[str]:
        matched = []

        for seg in segments:
            seg_lower = seg.lower()
            for kw in keywords:
                if kw and kw.lower() in seg_lower:
                    matched.append(seg)
                    break

        return matched

    def _build_company_keywords(self, company: Company) -> List[str]:
        keywords = []

        # 强关键词优先
        if company.company_cn:
            keywords.append(company.company_cn.strip())
        if company.company_en:
            keywords.append(company.company_en.strip())

        # 安全简称 / 别名
        candidates = [company.short_name, *company.aliases]
        for kw in candidates:
            kw = (kw or "").strip()
            if not kw:
                continue

            if self._contains_chinese(kw):
                if len(kw) >= 3:
                    keywords.append(kw)
            else:
                if len(kw) >= 4:
                    keywords.append(kw)

        # 去重
        return list(dict.fromkeys(keywords))

    @staticmethod
    def _contains_chinese(text: str) -> bool:
        return any("\u4e00" <= ch <= "\u9fff" for ch in text)

    @staticmethod
    def _compress_to_title(sentence: str, company_name: str) -> str:
        sentence = sentence.strip()
        if not sentence:
            return f"{company_name}相关动态"

        # 去尾部句号
        sentence = re.sub(r"[。；;,.，]+$", "", sentence)

        if company_name not in sentence:
            sentence = f"{company_name}{sentence}"

        # 标题太长时截断
        if len(sentence) > 60:
            sentence = sentence[:59].rstrip() + "…"

        return sentence

    @staticmethod
    def _clean_segment(text: str) -> str:
        text = (text or "").strip()
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"^[：:；;，,、\-\|]+", "", text)
        text = re.sub(r"[：:；;，,、\-\|]+$", "", text)
        return text.strip()

    @staticmethod
    def _normalize_simple(text: str) -> str:
        return " ".join((text or "").strip().lower().split())

    @staticmethod
    def _is_china_company(company: Company) -> bool:
        value = (company.country_region or "").strip().lower()
        return value in {"中国", "china", "cn", "中国大陆"}

    @staticmethod
    def _append_remark(existing: str | None, new_text: str) -> str:
        if not existing:
            return new_text
        return f"{existing}；{new_text}"