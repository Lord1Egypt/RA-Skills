#!/usr/bin/env python3
"""Locate and process one registered official China CDC health report."""

from __future__ import annotations

import argparse
import base64
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urljoin, urlsplit


SKILL_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_ARTIFACT_ROOT = SKILL_ROOT / "artifacts"
OFFICIAL_HOST = "www.chinacdc.cn"


def require_pdf_dependencies() -> None:
    """Fail before transferring a PDF when the extraction backend is unavailable."""
    if importlib.util.find_spec("pdfplumber") is not None:
        return
    requirements = SKILL_ROOT / "requirements.txt"
    command = f'"{sys.executable}" -m pip install -r "{requirements}"'
    raise PipelineError(
        "tool_environment_error",
        f"PDF extraction requires pdfplumber. Install it with: {command}",
    )

ADAPTERS: dict[str, dict[str, Any]] = {
    "influenza_weekly": {
        "index_url": "https://www.chinacdc.cn/jksj/jksj04_14249/",
        "allowed_path_prefix": "/jksj/jksj04_14249/",
        "period_type": "week",
        "content_mode": "html_with_pdf",
        "title_pattern": (
            r"^(?P<year>\d{4})年第(?P<week>\d{1,2})周"
            r"第(?P<issue>\d{1,4})期中国流感监测周报$"
        ),
        "index_marker": "流感监测周报",
        "allowed_url_patterns": (
            r"^https://www\.chinacdc\.cn/jksj/jksj04_14249/"
            r"(?:index(?:_\d+)?\.html)?$",
            r"^https://www\.chinacdc\.cn/jksj/jksj04_14249/"
            r"\d{6}/t\d+_\d+\.html$",
            r"^https://www\.chinacdc\.cn/jksj/jksj04_14249/\d{6}/P\d+\.pdf$",
        ),
    },
    "respiratory_weekly": {
        "index_url": "https://www.chinacdc.cn/jksj/jksj04_14275/",
        "allowed_path_prefix": "/jksj/jksj04_14275/",
        "period_type": "week",
        "content_mode": "html",
        "title_pattern": (
            r"^(?P<year>\d{4})年第(?P<week>\d{1,2})周"
            r"全国急性呼吸道传染病哨点监测情况$"
        ),
        "index_marker": "全国急性呼吸道传染病哨点监测情况",
        "allowed_url_patterns": (
            r"^https://www\.chinacdc\.cn/jksj/jksj04_14275/"
            r"(?:index(?:_\d+)?\.html)?$",
            r"^https://www\.chinacdc\.cn/jksj/jksj04_14275/"
            r"\d{6}/t\d+_\d+\.html$",
        ),
    },
    "covid_monthly": {
        "index_url": "https://www.chinacdc.cn/jksj/xgbdyq/",
        "allowed_path_prefix": "/jksj/xgbdyq/",
        "period_type": "month",
        "content_mode": "html",
        "title_pattern": (
            r"^全国新型冠状病毒感染疫情情况[（(]"
            r"(?P<year>\d{4})年(?P<month>\d{1,2})月[）)]$"
        ),
        "index_marker": "全国新型冠状病毒感染疫情情况",
        "allowed_url_patterns": (
            r"^https://www\.chinacdc\.cn/jksj/xgbdyq/"
            r"(?:index(?:_\d+)?\.html)?$",
            r"^https://www\.chinacdc\.cn/jksj/xgbdyq/"
            r"\d{6}/t\d+_\d+\.html$",
        ),
    },
    "global_infectious_risk_monthly": {
        "index_url": "https://www.chinacdc.cn/jksj/jksj03/",
        "allowed_path_prefix": "/jksj/jksj03/",
        "period_type": "month",
        "content_mode": "pdf",
        "title_pattern": (
            r"^(?P<year>\d{4})\s*年\s*(?P<month>\d{1,2})\s*月"
            r"全球传染病事件风险评估(?:报告)?$"
        ),
        "index_marker": "全球传染病事件风险评估报告",
        "allowed_url_patterns": (
            r"^https://www\.chinacdc\.cn/jksj/jksj03/"
            r"(?:index(?:_\d+)?\.html)?$",
            r"^https://www\.chinacdc\.cn/jksj/jksj03/\d{6}/P\d+\.pdf$",
        ),
    },
    "china_public_health_risk_monthly": {
        "index_url": "https://www.chinacdc.cn/jksj/jksj02/",
        "allowed_path_prefix": "/jksj/jksj02/",
        "period_type": "month",
        "content_mode": "pdf",
        "title_pattern": (
            r"^(?P<year>\d{4})\s*年\s*(?P<month>\d{1,2})\s*月"
            r"中国需关注的突发公共卫生事件风险评估(?:报告)?$"
        ),
        "index_marker": "重点传染病和突发公共卫生事件风险评估报告",
        "allowed_url_patterns": (
            r"^https://www\.chinacdc\.cn/jksj/jksj02/"
            r"(?:index(?:_\d+)?\.html)?$",
            r"^https://www\.chinacdc\.cn/jksj/jksj02/\d{6}/P\d+\.pdf$",
        ),
    },
}

LIST_PAGE_SCRIPT = r"""
(() => ({
  url: location.href,
  text: document.body?.innerText || "",
  links: Array.from(document.querySelectorAll("a")).map(a => ({
    text: (a.innerText || a.textContent || "").replace(/\s+/g, " ").trim(),
    href: a.href || "",
    context: (a.parentElement?.innerText || "").replace(/\s+/g, " ").trim()
  }))
}))()
"""

DETAIL_PAGE_SCRIPT = r"""
(() => {
  const selectors = [
    ".TRS_Editor", ".article-content", ".article_content", ".content-main",
    ".detail-content", ".zw", "article", "main"
  ];
  const candidates = selectors.flatMap(s => Array.from(document.querySelectorAll(s)));
  const main = candidates.sort((a, b) =>
    (b.innerText || "").length - (a.innerText || "").length
  )[0] || document.body;
  return {
    url: location.href,
    headings: Array.from(document.querySelectorAll("h1,h2,h3,h4,h5,h6"))
      .map(h => (h.innerText || "").replace(/\s+/g, " ").trim()),
    text: (main?.innerText || "").trim(),
    tables: Array.from(main?.querySelectorAll("table") || []).map(table => ({
      rows: Array.from(table.rows).map(row =>
        Array.from(row.cells).map(cell => (cell.innerText || "").trim())
      )
    })),
    images: Array.from(main?.querySelectorAll("img") || []).map(img => ({
      title: img.title || img.alt || "",
      url: img.src || ""
    })),
    links: Array.from(document.querySelectorAll("a")).map(a => ({
      text: (a.innerText || a.textContent || "").replace(/\s+/g, " ").trim(),
      href: a.href || ""
    })),
    bodyText: document.body?.innerText || ""
  };
})()
"""


class PipelineError(RuntimeError):
    def __init__(self, status: str, message: str) -> None:
        super().__init__(message)
        self.status = status


class AgentBrowser:
    def __init__(self, executable: str = "agent-browser") -> None:
        self.executable = executable
        self.session = f"cdc-report-{uuid.uuid4().hex[:10]}"

    def _run(self, *arguments: str) -> str:
        command = [self.executable, "--session", self.session, *arguments]
        try:
            result = subprocess.run(
                command,
                check=True,
                capture_output=True,
                text=True,
                timeout=45,
            )
        except FileNotFoundError as exc:
            raise PipelineError("browser_unavailable", "agent-browser is not installed") from exc
        except subprocess.TimeoutExpired as exc:
            raise PipelineError("source_unavailable", "browser navigation timed out") from exc
        except subprocess.CalledProcessError as exc:
            message = (exc.stderr or exc.stdout or "agent-browser failed").strip()
            raise PipelineError("browser_unavailable", message) from exc
        return result.stdout.strip()

    def open(self, url: str) -> None:
        self._run("open", url)

    def evaluate(self, script: str) -> dict[str, Any]:
        encoded = base64.b64encode(script.encode("utf-8")).decode("ascii")
        output = self._run("eval", "-b", encoded)
        try:
            value = json.loads(output)
        except json.JSONDecodeError as exc:
            raise PipelineError("source_unavailable", "browser returned invalid JSON") from exc
        if not isinstance(value, dict):
            raise PipelineError("source_unavailable", "browser returned an unexpected value")
        return value

    def close(self) -> None:
        try:
            self._run("close")
        except PipelineError:
            pass


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def validate_scoped_url(url: str, adapter: dict[str, Any]) -> str:
    parsed = urlsplit(url)
    if parsed.scheme != "https" or parsed.hostname != OFFICIAL_HOST:
        raise PipelineError("detail_unverified", "URL is outside the official China CDC host")
    if not parsed.path.startswith(adapter["allowed_path_prefix"]):
        raise PipelineError("detail_unverified", "URL is outside the selected adapter path")
    if not any(re.fullmatch(pattern, url) for pattern in adapter["allowed_url_patterns"]):
        raise PipelineError("detail_unverified", "URL does not match the adapter boundary")
    return url


def validate_query(query: dict[str, Any], adapter: dict[str, Any]) -> None:
    if query["latest"] and any(query.get(key) is not None for key in ("year", "week", "month", "issue")):
        raise PipelineError("invalid_query", "latest cannot be combined with a period or issue")
    if not query["latest"] and query.get("year") is None:
        raise PipelineError("invalid_query", "year is required unless --latest is used")
    if adapter["period_type"] == "week":
        if query.get("month") is not None:
            raise PipelineError("invalid_query", "month is not valid for a weekly report")
        if not query["latest"] and query.get("week") is None:
            raise PipelineError("invalid_query", "week is required for a weekly report")
        if query.get("week") is not None and not 1 <= query["week"] <= 53:
            raise PipelineError("invalid_query", "week must be 1-53")
    else:
        if query.get("week") is not None or query.get("issue") is not None:
            raise PipelineError("invalid_query", "week and issue are not valid for a monthly report")
        if not query["latest"] and query.get("month") is None:
            raise PipelineError("invalid_query", "month is required for a monthly report")
        if query.get("month") is not None and not 1 <= query["month"] <= 12:
            raise PipelineError("invalid_query", "month must be 1-12")
    if query.get("issue") is not None:
        if query["report_type"] != "influenza_weekly" or query["issue"] <= 0:
            raise PipelineError("invalid_query", "issue is supported only for influenza and must be positive")


def parse_records(page: dict[str, Any], adapter: dict[str, Any]) -> list[dict[str, Any]]:
    pattern = re.compile(adapter["title_pattern"])
    records: list[dict[str, Any]] = []
    for link in page.get("links", []):
        display_text = normalize_space(str(link.get("text", "")))
        title = re.sub(r"\s+20\d{2}-\d{2}-\d{2}$", "", display_text)
        match = pattern.fullmatch(title)
        if not match:
            continue
        href = urljoin(str(page["url"]), str(link.get("href", "")))
        validate_scoped_url(href, adapter)
        groups = match.groupdict()
        context = normalize_space(f"{display_text} {link.get('context', '')}")
        date_match = re.search(r"(?<!\d)(20\d{2})-(\d{2})-(\d{2})(?!\d)", context)
        records.append(
            {
                "title": title,
                "href": href,
                "year": int(groups["year"]),
                "week": int(groups["week"]) if groups.get("week") else None,
                "month": int(groups["month"]) if groups.get("month") else None,
                "issue": int(groups["issue"]) if groups.get("issue") else None,
                "publish_date": date_match.group(0) if date_match else None,
                "source_page_url": page["url"],
            }
        )
    return records


def choose_record(
    records: list[dict[str, Any]], query: dict[str, Any], adapter: dict[str, Any]
) -> dict[str, Any] | None:
    if query["latest"]:
        if not records:
            return None
        if query["report_type"] == "influenza_weekly":
            return max(records, key=lambda row: (row["issue"] or 0, row["year"], row["week"] or 0))
        period_key = "week" if adapter["period_type"] == "week" else "month"
        return max(
            records,
            key=lambda row: (row["year"], row[period_key] or 0, row["publish_date"] or ""),
        )
    for record in records:
        period_matches = (
            record["year"] == query["year"]
            and record.get(adapter["period_type"]) == query[adapter["period_type"]]
        )
        issue_matches = query.get("issue") is None or record["issue"] == query["issue"]
        if period_matches and issue_matches:
            return record
    return None


def pagination_urls(page: dict[str, Any], adapter: dict[str, Any]) -> list[str]:
    result: list[str] = []
    for link in page.get("links", []):
        label = normalize_space(str(link.get("text", "")))
        if label not in {"下一页", "尾页"} and not label.isdigit():
            continue
        href = urljoin(str(page["url"]), str(link.get("href", "")))
        try:
            validate_scoped_url(href, adapter)
        except PipelineError:
            continue
        if href not in result:
            result.append(href)
    return result


def report_id(report_type: str, record: dict[str, Any]) -> str:
    if record["week"] is not None:
        issue = record["issue"] if record["issue"] is not None else "NA"
        return f"{report_type}-{record['year']}-W{record['week']:02d}-I{issue}"
    return f"{report_type}-{record['year']}-M{record['month']:02d}-INA"


def build_report(
    query: dict[str, Any],
    adapter: dict[str, Any],
    record: dict[str, Any],
    detail: dict[str, Any] | None,
) -> dict[str, Any]:
    content_mode = adapter["content_mode"]
    detail_url = record["href"] if content_mode != "pdf" else None
    document_url = record["href"] if content_mode == "pdf" else None
    if content_mode == "html_with_pdf":
        assert detail is not None
        pdf_links = [
            urljoin(detail["url"], link.get("href", ""))
            for link in detail.get("links", [])
            if urlsplit(urljoin(detail["url"], link.get("href", ""))).path.lower().endswith(".pdf")
        ]
        verified = []
        for url in pdf_links:
            try:
                verified.append(validate_scoped_url(url, adapter))
            except PipelineError:
                continue
        if not verified:
            raise PipelineError("detail_unverified", "matching detail page has no allowed official PDF")
        document_url = verified[0]
    return {
        "report_id": report_id(query["report_type"], record),
        "report_type": query["report_type"],
        "title": record["title"],
        "reporting_period": {
            "year": record["year"],
            "week": record["week"],
            "month": record["month"],
        },
        "issue_number": record["issue"],
        "publish_date": record["publish_date"],
        "content_mode": content_mode,
        "detail_url": detail_url,
        "document_url": document_url,
        "source_page_url": record["source_page_url"],
    }


def locate_report(
    query: dict[str, Any],
    browser_factory: Callable[[], AgentBrowser] = AgentBrowser,
) -> tuple[dict[str, Any], dict[str, Any] | None]:
    adapter = ADAPTERS[query["report_type"]]
    validate_query(query, adapter)
    browser = browser_factory()
    try:
        next_urls = [adapter["index_url"]]
        visited: set[str] = set()
        record = None
        for page_number in range(8):
            if not next_urls:
                break
            page_url = next_urls.pop(0)
            if page_url in visited:
                continue
            visited.add(page_url)
            browser.open(page_url)
            page = browser.evaluate(LIST_PAGE_SCRIPT)
            validate_scoped_url(str(page.get("url", "")), adapter)
            if adapter["index_marker"] not in str(page.get("text", "")):
                raise PipelineError("source_unavailable", "index marker is missing")
            records = parse_records(page, adapter)
            record = choose_record(records, query, adapter)
            if record is not None:
                break
            if query["latest"]:
                break
            for candidate in pagination_urls(page, adapter):
                if candidate not in visited and candidate not in next_urls:
                    next_urls.append(candidate)
            if page_number == 7 and next_urls:
                raise PipelineError("search_budget_exceeded", "search exceeded eight list pages")
        if record is None:
            raise PipelineError("not_found", "no matching official report was found")

        detail = None
        if adapter["content_mode"] in {"html", "html_with_pdf"}:
            browser.open(record["href"])
            detail = browser.evaluate(DETAIL_PAGE_SCRIPT)
            validate_scoped_url(str(detail.get("url", "")), adapter)
            headings = {normalize_space(str(value)) for value in detail.get("headings", [])}
            if record["title"] not in headings:
                raise PipelineError("detail_unverified", "detail heading does not match the list title")
        return build_report(query, adapter, record, detail), detail
    finally:
        browser.close()


def html_extraction(report: dict[str, Any], detail: dict[str, Any]) -> dict[str, Any]:
    tables = []
    for table in detail.get("tables", []):
        rows = table.get("rows", [])
        tables.append(
            {
                "title": None,
                "headers": rows[0] if rows else [],
                "rows": rows[1:] if len(rows) > 1 else [],
                "footnotes": [],
                "units": None,
            }
        )
    return {
        "schema_version": "2.0",
        "report": report,
        "pages": [],
        "content": {
            "text": str(detail.get("text", "")),
            "tables": tables,
            "images": detail.get("images", []),
        },
        "vision_pages": [],
        "warnings": [],
    }


def pdf_extraction(report: dict[str, Any], pdf_path: Path) -> dict[str, Any]:
    require_pdf_dependencies()
    try:
        import pdfplumber
    except ImportError as exc:
        raise PipelineError("tool_environment_error", "pdfplumber is required for PDF extraction") from exc
    pages = []
    vision_pages = []
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for number, page in enumerate(pdf.pages, 1):
                text = page.extract_text(x_tolerance=2, y_tolerance=3) or ""
                native_tables = []
                for table in page.extract_tables() or []:
                    rows = [["" if cell is None else cell for cell in row] for row in table]
                    native_tables.append(
                        {
                            "title": None,
                            "headers": rows[0] if rows else [],
                            "rows": rows[1:] if len(rows) > 1 else [],
                            "footnotes": [],
                            "units": None,
                        }
                    )
                requires_vision = bool(page.images) and (
                    not text.strip() or bool(re.search(r"图\s*\d+", text))
                )
                if requires_vision:
                    vision_pages.append(number)
                pages.append(
                    {
                        "page": number,
                        "text": text,
                        "tables": native_tables,
                        "visuals": [],
                        "requires_vision": requires_vision,
                    }
                )
    except Exception as exc:
        raise PipelineError("extraction_partial", f"PDF extraction failed: {exc}") from exc
    warnings = []
    if vision_pages:
        warnings.append("图表未做视觉解读；相关页面已列入 vision_pages。")
    return {
        "schema_version": "2.0",
        "report": report,
        "pages": pages,
        "content": None,
        "vision_pages": vision_pages,
        "warnings": warnings,
    }


def validate_extraction(payload: dict[str, Any]) -> None:
    if payload.get("schema_version") != "2.0":
        raise PipelineError("internal_error", "unexpected extraction schema")
    pages = payload.get("pages")
    if not isinstance(pages, list):
        raise PipelineError("internal_error", "pages must be a list")
    if [page.get("page") for page in pages] != list(range(1, len(pages) + 1)):
        raise PipelineError("internal_error", "PDF pages are not complete and ordered")
    expected = [page["page"] for page in pages if page.get("requires_vision")]
    if payload.get("vision_pages") != expected:
        raise PipelineError("internal_error", "vision_pages is inconsistent")
    if pages and payload.get("content") is not None:
        raise PipelineError("internal_error", "PDF extraction cannot contain HTML content")
    if not pages and not isinstance(payload.get("content"), dict):
        raise PipelineError("internal_error", "HTML extraction content is missing")


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".json.tmp")
    try:
        temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        os.replace(temporary, path)
    except OSError as exc:
        temporary.unlink(missing_ok=True)
        raise PipelineError("artifact_store_unavailable", str(exc)) from exc


def cached_artifact(path: Path, expected_report_id: str) -> bool:
    if not path.is_file():
        return False
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        validate_extraction(payload)
        return payload.get("report", {}).get("report_id") == expected_report_id
    except (OSError, ValueError, PipelineError):
        return False


def default_downloader(
    report: dict[str, Any], adapter: dict[str, Any], output_dir: Path
) -> dict[str, Any]:
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    try:
        import download_official_document
    finally:
        sys.path.pop(0)
    arguments = argparse.Namespace(
        url=report["document_url"],
        referer=report["detail_url"] or report["source_page_url"],
        allowed_path_prefix=adapter["allowed_path_prefix"],
        output_dir=output_dir,
        report_type=report["report_type"],
        year=report["reporting_period"]["year"],
        week=report["reporting_period"]["week"],
        month=report["reporting_period"]["month"],
        issue=report["issue_number"],
        timeout=60.0,
        max_bytes=100 * 1024 * 1024,
        user_agent=download_official_document.DEFAULT_USER_AGENT,
    )
    try:
        return download_official_document.download(arguments)
    except download_official_document.DownloadError as exc:
        raise PipelineError("download_failed", str(exc)) from exc


def run_pipeline(
    query: dict[str, Any],
    artifact_root: Path = DEFAULT_ARTIFACT_ROOT,
    locator: Callable[[dict[str, Any]], tuple[dict[str, Any], dict[str, Any] | None]] = locate_report,
    downloader: Callable[[dict[str, Any], dict[str, Any], Path], dict[str, Any]] = default_downloader,
    html_extract: Callable[[dict[str, Any], dict[str, Any]], dict[str, Any]] = html_extraction,
    pdf_extract: Callable[[dict[str, Any], Path], dict[str, Any]] = pdf_extraction,
    pdf_dependency_check: Callable[[], None] = require_pdf_dependencies,
) -> dict[str, Any]:
    report, detail = locator(query)
    action = query["action"]
    result: dict[str, Any] = {"status": "success", "report": report, "cache_hit": False}
    if action == "locate":
        return result

    report_dir = artifact_root.resolve() / report["report_id"]
    extracted_path = report_dir / "extracted.json"
    if action == "extract" and cached_artifact(extracted_path, report["report_id"]):
        result.update({"cache_hit": True, "artifact": str(extracted_path)})
        return result

    adapter = ADAPTERS[report["report_type"]]
    if action == "download":
        if report["document_url"] is None:
            raise PipelineError("invalid_query", "this HTML-only report has no PDF")
        download_result = downloader(report, adapter, report_dir)
        result["document_path"] = download_result["path"]
        result["reused"] = bool(download_result.get("reused", False))
        return result

    if report["content_mode"] == "html":
        if detail is None:
            raise PipelineError("detail_unverified", "verified HTML content is missing")
        extraction = html_extract(report, detail)
    else:
        if report["document_url"] is None:
            raise PipelineError("detail_unverified", "verified PDF URL is missing")
        pdf_dependency_check()
        with tempfile.TemporaryDirectory(prefix="china-cdc-report-") as directory:
            download_result = downloader(report, adapter, Path(directory))
            extraction = pdf_extract(report, Path(download_result["path"]))
    validate_extraction(extraction)
    atomic_write_json(extracted_path, extraction)
    result["artifact"] = str(extracted_path)
    result["warnings"] = extraction["warnings"]
    return result


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report-type", required=True, choices=sorted(ADAPTERS))
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--year", type=int)
    parser.add_argument("--week", type=int)
    parser.add_argument("--month", type=int)
    parser.add_argument("--issue", type=int)
    parser.add_argument("--action", choices=("locate", "download", "extract"), default="locate")
    parser.add_argument("--artifact-root", type=Path, default=DEFAULT_ARTIFACT_ROOT)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    arguments = parse_args(argv)
    query = vars(arguments).copy()
    query.pop("artifact_root")
    try:
        result = run_pipeline(query, artifact_root=arguments.artifact_root)
    except PipelineError as exc:
        print(
            json.dumps({"status": exc.status, "message": str(exc)}, ensure_ascii=False),
            file=sys.stderr,
        )
        return 1
    except Exception as exc:
        print(
            json.dumps({"status": "internal_error", "message": str(exc)}, ensure_ascii=False),
            file=sys.stderr,
        )
        return 1
    print(json.dumps(result, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
