from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Iterable, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from .fiscal_parser import DocumentMeta, build_period_label, normalize_text, parse_period_from_title, previous_month


BASE_URL = "https://www.mof.gov.cn/gkml/caizhengshuju/"
USER_AGENT = "Mozilla/5.0 (compatible; FinancialDataCollection/1.0)"


@dataclass(frozen=True)
class CrawlScope:
    start_month: Optional[str] = None
    end_month: Optional[str] = None

    def normalized_start_month(self) -> Optional[str]:
        if not self.start_month:
            return None
        year, month = self.start_month.split("-")
        if month in {"01", "02"}:
            return f"{year}-02"
        return self.start_month

    def normalized_end_month(self) -> Optional[str]:
        if not self.end_month:
            return None
        year, month = self.end_month.split("-")
        if month in {"01", "02"}:
            return f"{year}-02"
        return self.end_month

    def requested_period_range_key(self) -> Optional[str]:
        start = self.normalized_start_month()
        end = self.normalized_end_month()
        if not start or not end:
            return None
        start_year, start_mon = start.split("-")
        end_year, end_mon = end.split("-")
        if start_mon == "02" and self.start_month and self.start_month.endswith(("-01", "-02")):
            start_key = f"{start_year}01"
        else:
            start_key = f"{start_year}{start_mon}"
        if end_mon == "02" and self.end_month and self.end_month.endswith(("-01", "-02")):
            end_key = f"{end_year}02"
        else:
            end_key = f"{end_year}{end_mon}"
        return f"{start_key}-{end_key}"

    def fetch_start_month(self) -> Optional[str]:
        start = self.normalized_start_month()
        if not start:
            return None
        prev = previous_month(start)
        if prev is None:
            return start
        if self.start_month and self.start_month.endswith(("-01", "-02")):
            return start
        return prev

    def should_fetch(self, cutoff_month: str) -> bool:
        start = self.fetch_start_month()
        end = self.normalized_end_month()
        if start and end:
            return start <= cutoff_month <= end
        return True

    def should_output(self, month_value: str, period_label: Optional[str] = None) -> bool:
        start = self.normalized_start_month()
        end = self.normalized_end_month()
        if start and end:
            return start <= month_value <= end
        return True


class FiscalCrawler:
    def __init__(self, timeout: int = 30) -> None:
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": USER_AGENT})
        self.timeout = timeout

    def _fetch_html(self, url: str) -> str:
        response = self.session.get(url, timeout=self.timeout)
        response.raise_for_status()
        response.encoding = response.apparent_encoding or response.encoding
        return response.text

    def iter_document_entries(self) -> Iterable[Dict[str, str]]:
        yielded = set()
        for page_url in self.iter_listing_pages():
            soup = BeautifulSoup(self._fetch_html(page_url), "html.parser")
            for anchor in soup.select("a[href]"):
                href = anchor.get("href", "").strip()
                if not href:
                    continue
                absolute_url = urljoin(page_url, href)
                title = normalize_text(anchor.get_text(" ", strip=True))
                if "财政收支情况" not in title:
                    continue
                if absolute_url in yielded:
                    continue
                yielded.add(absolute_url)
                yield {"title": title, "url": absolute_url}

    def iter_document_links(self) -> Iterable[str]:
        for entry in self.iter_document_entries():
            yield entry["url"]

    def iter_listing_pages(self) -> Iterable[str]:
        first_page_html = self._fetch_html(BASE_URL)
        yield BASE_URL
        match = re.search(r"countPage\s*=\s*(\d+)", first_page_html)
        if not match:
            return
        count_page = int(match.group(1))
        for index in range(1, count_page):
            yield urljoin(BASE_URL, f"index_{index}.htm")

    def fetch_documents(self, scope: CrawlScope) -> List[dict]:
        documents: List[dict] = []
        seen = set()
        for entry in self.iter_document_entries():
            url = entry["url"]
            if url in seen:
                continue
            seen.add(url)
            try:
                period_text, cutoff_month = parse_period_from_title(entry["title"])
            except Exception:
                continue
            if not scope.should_fetch(cutoff_month):
                continue
            try:
                meta = self.fetch_document(url)
            except Exception:
                continue
            if scope.should_fetch(meta.cutoff_month):
                documents.append(self._meta_to_record(meta))
        documents.sort(key=lambda item: item["publish_date"])
        return documents

    def fetch_document(self, url: str) -> DocumentMeta:
        soup = BeautifulSoup(self._fetch_html(url), "html.parser")
        self._ensure_valid_page(soup)
        title = normalize_text(
            soup.find("h1").get_text(" ", strip=True) if soup.find("h1") else soup.title.get_text(" ", strip=True)
        )
        publish_date = self._extract_publish_date(soup)
        page_text = normalize_text(soup.get_text("\n", strip=True))
        source_department = self._extract_source_department(page_text)
        content = self._extract_content(soup)
        period_text, cutoff_month = parse_period_from_title(title)
        return DocumentMeta(
            title=title,
            url=url,
            publish_date=publish_date,
            source_department=source_department,
            content=content,
            period_text=period_text,
            cutoff_month=cutoff_month,
        )

    def _extract_publish_date(self, soup: BeautifulSoup) -> datetime.date:
        selectors = [
            ".laiyuan",
            ".source",
            ".article-source",
            ".info",
        ]
        for selector in selectors:
            node = soup.select_one(selector)
            if not node:
                continue
            match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", node.get_text(" ", strip=True))
            if match:
                year, month, day = map(int, match.groups())
                return datetime(year, month, day).date()

        text = normalize_text(soup.get_text("\n", strip=True))
        if "温馨提示：您访问的页面不存在或已删除" in text:
            raise ValueError("页面不存在或已删除")
        match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日\s*来源[:：]", text)
        if not match:
            match = re.search(r"(\d{4})年(\d{1,2})月(\d{1,2})日", text)
        if not match:
            raise ValueError("未找到发布日期")
        year, month, day = map(int, match.groups())
        return datetime(year, month, day).date()

    def _extract_source_department(self, text: str) -> str:
        match = re.search(r"来源[:：]\s*([^\s]+)", text)
        return match.group(1) if match else ""

    def _extract_content(self, soup: BeautifulSoup) -> str:
        selectors = [
            ".TRS_Editor",
            ".content",
            ".article-content",
            "#zoom",
            ".xl-content",
        ]
        for selector in selectors:
            node = soup.select_one(selector)
            if node:
                return normalize_text(node.get_text("\n", strip=True))
        return normalize_text(soup.get_text("\n", strip=True))

    def _ensure_valid_page(self, soup: BeautifulSoup) -> None:
        text = normalize_text(soup.get_text("\n", strip=True))
        if "温馨提示：您访问的页面不存在或已删除" in text:
            raise ValueError("页面不存在或已删除")

    def _meta_to_record(self, meta: DocumentMeta) -> dict:
        doc_id = meta.title
        return {
            "document_id": doc_id,
            "title": meta.title,
            "url": meta.url,
            "publish_date": meta.publish_date.isoformat(),
            "source_department": meta.source_department,
            "content": meta.content,
            "period_text": meta.period_text,
            "cutoff_month": meta.cutoff_month,
            "period_label": build_period_label(meta.period_text, meta.cutoff_month),
        }
