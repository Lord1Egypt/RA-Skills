"""Generic collector for any web page."""

from __future__ import annotations

import logging
import os
import re
import ssl

import certifi
import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter

from datapulse.core.models import SourceType
from datapulse.core.security import get_secret, has_secret
from datapulse.core.utils import clean_text, generate_excerpt, validate_external_url

from .base import BaseCollector, ParseResult

logger = logging.getLogger("datapulse.parsers.generic")

CHINESE_NEWS_BACKEND_PROFILE = "general_news_extractor"
GENERIC_FALLBACK_POLICY = (
    "general_news_extractor_then_trafilatura_then_beautifulsoup_then_firecrawl_then_jina"
)
_MIN_EXTRACTED_CONTENT_LENGTH = 50
_MIN_CHINESE_CHARACTER_COUNT = 20
_CHINESE_CHARACTER_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")


class _SSLContextAdapter(HTTPAdapter):
    """Bind an explicit SSL context so requests can use system trust roots."""

    def __init__(self, ssl_context: ssl.SSLContext):
        self._ssl_context = ssl_context
        super().__init__()

    def init_poolmanager(self, connections, maxsize, block=False, **pool_kwargs):
        pool_kwargs["ssl_context"] = self._ssl_context
        return super().init_poolmanager(connections, maxsize, block=block, **pool_kwargs)

    def proxy_manager_for(self, proxy, **proxy_kwargs):
        proxy_kwargs["ssl_context"] = self._ssl_context
        return super().proxy_manager_for(proxy, **proxy_kwargs)


class GenericCollector(BaseCollector):
    name = "generic"
    source_type = SourceType.GENERIC
    reliability = 0.72
    tier = 1
    setup_hint = "pip install trafilatura gne for best results"
    allowed_content_types = ("text/html", "application/xhtml+xml", "text/plain", "application/xml")
    max_response_bytes = 5_000_000

    def check(self) -> dict[str, str | bool]:
        backends = ["beautifulsoup"]
        has_gne = False
        try:
            from gne import GeneralNewsExtractor  # noqa: F401

            has_gne = True
            backends.append(CHINESE_NEWS_BACKEND_PROFILE)
        except ImportError:
            pass
        has_trafilatura = False
        try:
            import trafilatura  # noqa: F401

            has_trafilatura = True
            backends.append("trafilatura")
        except ImportError:
            pass
        if has_secret("FIRECRAWL_API_KEY"):
            backends.append("firecrawl")
        msg = f"backends: {', '.join(backends)}"
        if not has_gne and not has_trafilatura:
            return {"status": "warn", "message": f"gne and trafilatura missing; {msg}", "available": True}
        return {"status": "ok", "message": msg, "available": True}

    def can_handle(self, url: str) -> bool:
        return True

    def parse(self, url: str) -> ParseResult:
        last_error = ""
        try:
            safe, reason = validate_external_url(url)
            if not safe:
                return ParseResult.failure(url, reason)

            html = self._fetch_html(url)
            extracted = ""
            chinese_news_payload = self._extract_with_general_news_extractor(html, url)
            title, author = self._extract_metadata(html, url)

            if chinese_news_payload:
                content = chinese_news_payload["content"]
                return self._build_result(
                    url=url,
                    title=title,
                    author=author,
                    content=content,
                    extracted_title=chinese_news_payload.get("title", ""),
                    extracted_author=chinese_news_payload.get("author", ""),
                    tags=["generic", CHINESE_NEWS_BACKEND_PROFILE, "chinese-news-body"],
                    confidence_flags=[CHINESE_NEWS_BACKEND_PROFILE],
                    bridge_profile=CHINESE_NEWS_BACKEND_PROFILE,
                    collector_family="native_library",
                    transport="in_process",
                )

            try:
                import trafilatura  # type: ignore[import-not-found]

                extracted = trafilatura.extract(
                    html,
                    url=url,
                    include_comments=False,
                    include_tables=True,
                    include_links=True,
                    output_format="txt",
                    favor_precision=True,
                ) or ""
            except Exception as exc:
                logger.info("GenericCollector trafilatura unavailable for %s: %s", url, exc)

            if self._is_meaningful_text(extracted):
                return self._build_result(
                    url=url,
                    title=title,
                    author=author,
                    content=extracted,
                    tags=["generic", "trafilatura"],
                    confidence_flags=["trafilatura"],
                    bridge_profile="trafilatura",
                    collector_family="html_parser",
                    transport="in_process",
                )

            bs_content = self._extract_with_bs(html)
            if bs_content:
                return self._build_result(
                    url=url,
                    title=title,
                    author=author,
                    content=bs_content,
                    tags=["generic", "beautifulsoup"],
                    confidence_flags=["fallback_bs4"],
                    bridge_profile="beautifulsoup",
                    collector_family="html_parser",
                    transport="in_process",
                )
            last_error = "Could not extract meaningful text."
        except Exception as exc:  # noqa: BLE001
            last_error = str(exc)
            logger.warning("GenericCollector failed for %s: %s", url, last_error)

        # Optional firecrawl fallback
        fc_result = self._extract_with_firecrawl(url)
        if fc_result:
            return fc_result

        # Jina Reader fallback (last resort)
        jina_result = self._extract_with_jina(url)
        if jina_result:
            return jina_result

        return ParseResult.failure(url, last_error or "Generic parse failed")

    def _build_result(
        self,
        *,
        url: str,
        title: str,
        author: str,
        content: str,
        tags: list[str],
        confidence_flags: list[str],
        bridge_profile: str,
        collector_family: str,
        transport: str,
        extracted_title: str = "",
        extracted_author: str = "",
        extra: dict | None = None,
        raw_source_type: str = "generic",
    ) -> ParseResult:
        normalized_content = clean_text(content)
        return ParseResult(
            url=url,
            title=self._normalize_scalar(extracted_title or title),
            author=self._normalize_scalar(extracted_author or author),
            content=normalized_content,
            excerpt=self._safe_excerpt(normalized_content),
            source_type=self.source_type,
            tags=self._merge_unique(tags),
            confidence_flags=self._merge_unique(confidence_flags),
            extra=self._with_collector_provenance(
                extra,
                bridge_profile=bridge_profile,
                collector_family=collector_family,
                transport=transport,
                raw_source_type=raw_source_type,
                url=url,
            ),
        )

    @staticmethod
    def _merge_unique(values: list[str] | None, *required: str) -> list[str]:
        merged: list[str] = []
        for item in [*(values or []), *required]:
            text = str(item).strip()
            if text and text not in merged:
                merged.append(text)
        return merged

    @staticmethod
    def _normalize_scalar(value: object) -> str:
        if value is None:
            return ""
        if isinstance(value, (list, tuple, set)):
            return ", ".join(
                text for item in value if (text := str(item).strip())
            )
        return str(value).strip()

    @staticmethod
    def _with_collector_provenance(
        extra: dict | None,
        *,
        bridge_profile: str,
        collector_family: str,
        transport: str,
        raw_source_type: str,
        url: str,
    ) -> dict:
        payload = dict(extra) if isinstance(extra, dict) else {}
        payload.setdefault("url", url)
        payload["collector"] = "generic"
        payload["collector_provenance"] = {
            "collector_family": collector_family,
            "bridge_profile": bridge_profile,
            "transport": transport,
            "session_key": "",
            "session_mode": "none",
            "raw_source_type": raw_source_type,
            "fallback_policy": GENERIC_FALLBACK_POLICY,
        }
        return payload

    @staticmethod
    def _is_meaningful_text(text: str) -> bool:
        return len(clean_text(text or "")) > _MIN_EXTRACTED_CONTENT_LENGTH

    @staticmethod
    def _looks_like_chinese_text(text: str) -> bool:
        return len(_CHINESE_CHARACTER_RE.findall(text or "")) >= _MIN_CHINESE_CHARACTER_COUNT

    def _extract_with_general_news_extractor(self, html: str, url: str) -> dict[str, str] | None:
        try:
            from gne import GeneralNewsExtractor  # type: ignore[import-not-found]
        except Exception as exc:
            logger.info("GenericCollector gne unavailable for %s: %s", url, exc)
            return None

        try:
            payload = GeneralNewsExtractor().extract(html) or {}
        except Exception as exc:
            logger.info("GenericCollector gne extraction failed for %s: %s", url, exc)
            return None

        content = clean_text(self._normalize_scalar(payload.get("content", "")))
        if not self._is_meaningful_text(content):
            return None

        sample = html[:20_000].lower()
        if not self._looks_like_chinese_text(content) and not any(
            marker in sample for marker in ('lang="zh', "lang='zh", "zh-cn", "zh-hans", "zh-hant")
        ):
            return None

        return {
            "content": content,
            "title": self._normalize_scalar(payload.get("title", "")),
            "author": self._normalize_scalar(payload.get("author", "")),
        }

    def _build_ssl_context(self) -> ssl.SSLContext:
        context = ssl.create_default_context()
        context.load_default_certs()

        requests_bundle = certifi.where()
        if requests_bundle and os.path.exists(requests_bundle):
            context.load_verify_locations(cafile=requests_bundle)

        custom_bundle = os.getenv("DATAPULSE_CA_BUNDLE", "").strip()
        if custom_bundle:
            if os.path.exists(custom_bundle):
                context.load_verify_locations(cafile=custom_bundle)
            else:
                logger.warning(
                    "DATAPULSE_CA_BUNDLE not found at %s; falling back to default trust roots",
                    custom_bundle,
                )
        return context

    def _build_http_session(self) -> requests.Session:
        session = requests.Session()
        adapter = _SSLContextAdapter(self._build_ssl_context())
        session.mount("https://", adapter)
        session.mount("http://", adapter)
        return session

    def _fetch_html(self, url: str) -> str:
        session = self._build_http_session()
        try:
            with session.get(
                url,
                timeout=self.timeout,
                allow_redirects=True,
                stream=True,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "text/html,application/xhtml+xml;q=0.9,*/*;q=0.8",
                },
            ) as resp:
                resp.raise_for_status()
                safe, reason = validate_external_url(resp.url)
                if not safe:
                    raise ValueError(f"Blocked redirect target: {reason}")

                content_type = (resp.headers.get("Content-Type") or "").lower()
                if content_type and not any(ct in content_type for ct in self.allowed_content_types):
                    raise ValueError(f"Unsupported content type: {content_type}")

                body = bytearray()
                for chunk in resp.iter_content(chunk_size=8192):
                    if not chunk:
                        continue
                    body.extend(chunk)
                    if len(body) > self.max_response_bytes:
                        raise ValueError(f"Response too large: > {self.max_response_bytes}")
                encoding = resp.encoding or resp.apparent_encoding or "utf-8"
                return body.decode(encoding, errors="replace")
        finally:
            session.close()

    @staticmethod
    def _extract_metadata(html: str, url: str) -> tuple[str, str]:
        soup = BeautifulSoup(html, "lxml")
        title = ""
        title_tag = soup.find("title")
        if title_tag:
            title = title_tag.get_text(strip=True)
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):  # type: ignore[union-attr]
            title = str(og_title.get("content"))  # type: ignore[union-attr]
        author = ""
        meta_author = soup.find("meta", attrs={"name": "author"})
        if meta_author:
            author = str(meta_author.get("content", ""))  # type: ignore[union-attr]
        return title, author

    @staticmethod
    def _extract_with_bs(html: str) -> str:
        soup = BeautifulSoup(html, "lxml")
        for node in soup.find_all(["script", "style", "header", "footer", "nav", "aside"]):
            node.decompose()

        main = soup.find("article") or soup.find("main") or soup.find("div", attrs={"role": "main"})
        if not main:
            main = soup.body
        if not main:
            return ""
        content = main.get_text("\n", strip=True)
        return clean_text(content)

    def _extract_with_firecrawl(self, url: str) -> ParseResult | None:
        api_key = get_secret("FIRECRAWL_API_KEY")
        if not api_key:
            return None

        try:
            resp = requests.post(
                "https://api.firecrawl.dev/v1/scrape",
                json={"url": url, "formats": ["markdown"]},
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
                timeout=self.timeout * 2,
            )
            resp.raise_for_status()
            payload = resp.json()
            if not payload.get("success"):
                return None
            data = payload.get("data", {})
            markdown = clean_text(data.get("markdown", ""))
            if len(markdown) < 200:
                return None
            return ParseResult(
                url=url,
                title=data.get("metadata", {}).get("title", ""),
                author=data.get("metadata", {}).get("author", ""),
                content=markdown,
                excerpt=generate_excerpt(markdown),
                source_type=self.source_type,
                tags=["generic", "firecrawl"],
                confidence_flags=["firecrawl"],
                extra=self._with_collector_provenance(
                    {"firecrawl": True},
                    bridge_profile="firecrawl",
                    collector_family="remote_api",
                    transport="https_api",
                    raw_source_type="generic",
                    url=url,
                ),
            )
        except Exception:
            return None

    def _extract_with_jina(self, url: str) -> ParseResult | None:
        try:
            from datapulse.core.jina_client import JinaAPIClient

            client = JinaAPIClient()
            result = client.read(url)
            content = clean_text(result.content or "")
            if len(content) < 200:
                return None
            lines = [ln for ln in content.splitlines() if ln.strip()]
            title = ""
            if lines:
                title = lines[0].lstrip("#").strip()[:200]
                body = "\n".join(lines[1:]).strip()
            else:
                body = content
            return ParseResult(
                url=url,
                title=title,
                content=body,
                excerpt=generate_excerpt(body),
                source_type=self.source_type,
                tags=["generic", "jina_fallback"],
                confidence_flags=["jina"],
                extra=self._with_collector_provenance(
                    {"jina_fallback": True},
                    bridge_profile="jina",
                    collector_family="jina_fallback",
                    transport="jina_reader",
                    raw_source_type="generic",
                    url=url,
                ),
            )
        except Exception:
            return None
