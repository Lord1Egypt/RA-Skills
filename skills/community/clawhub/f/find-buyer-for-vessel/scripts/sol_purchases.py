from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.parse
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

try:
    from .common import (
        cache_dir,
        fetch_bytes,
        normalize_space,
        read_json_cache,
        utc_now_iso,
        write_json_atomic,
    )
except ImportError:
    from common import (
        cache_dir,
        fetch_bytes,
        normalize_space,
        read_json_cache,
        utc_now_iso,
        write_json_atomic,
    )


BASE_URL = "https://sp.sol.com.cn"
MAX_PAGES = 250


class TableRowParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.rows: list[tuple[list[str], list[str]]] = []
        self.current_cells: list[str] | None = None
        self.current_links: list[str] | None = None
        self.cell_parts: list[str] | None = None

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag == "tr":
            self.current_cells = []
            self.current_links = []
        elif tag in {"td", "th"} and self.current_cells is not None:
            self.cell_parts = []
        elif tag == "br" and self.cell_parts is not None:
            self.cell_parts.append("\n")
        elif tag == "a" and self.current_links is not None:
            href = dict(attrs).get("href")
            if href:
                self.current_links.append(href)

    def handle_data(self, data: str) -> None:
        if self.cell_parts is not None:
            self.cell_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in {"td", "th"} and self.cell_parts is not None:
            value = normalize_space("".join(self.cell_parts).replace("\xa0", " "))
            if self.current_cells is not None:
                self.current_cells.append(value)
            self.cell_parts = None
        elif tag == "tr" and self.current_cells is not None:
            self.rows.append((self.current_cells, self.current_links or []))
            self.current_cells = None
            self.current_links = None
            self.cell_parts = None


def _decode(data: bytes) -> str:
    return data.decode("gb18030", "replace")


def _list_url(filters: dict[str, str], page: int) -> str:
    params = {"pageno": str(page), **filters, "uid": ""}
    return f"{BASE_URL}/purchase.asp?" + urllib.parse.urlencode(
        params,
        encoding="gb18030",
        errors="strict",
    )


def _parse_list_page(page_html: str) -> tuple[list[dict[str, Any]], bool]:
    parser = TableRowParser()
    parser.feed(page_html)
    records: list[dict[str, Any]] = []
    for original_cells, links in parser.rows:
        cells = list(original_cells)
        while cells and not cells[0]:
            cells.pop(0)
        if len(cells) < 7 or not re.fullmatch(r"P\d+", cells[0] or ""):
            continue
        solid = ""
        for link in links:
            match = re.search(r"purchase_msg\.asp\?solid=([A-Za-z0-9]+)", link, re.I)
            if match:
                solid = match.group(1)
                break
        if not solid:
            continue
        if len(cells) >= 8:
            company_name, status, updated_date = cells[5], cells[6], cells[7]
        else:
            company_name, status, updated_date = "", cells[5], cells[6]
        records.append(
            {
                "purchase_id": cells[0],
                "vessel_type": cells[1],
                "capacity_raw": cells[2],
                "age_range_raw": cells[3],
                "flag": cells[4],
                "company_name": company_name,
                "status": status,
                "updated_date": updated_date,
                "solid": solid,
            }
        )
    has_next = bool(
        re.search(
            r"<li[^>]*class=[\"']next[\"'][^>]*>\s*<a[^>]+href=",
            page_html,
            re.I,
        )
    )
    return records, has_next


def _cache_path(filters: dict[str, str]) -> Path:
    key = json.dumps(filters, ensure_ascii=False, sort_keys=True).encode("utf-8")
    return cache_dir() / "lists" / f"{hashlib.sha256(key).hexdigest()[:24]}.json"


def get_purchase_list(filters: dict[str, str], force_refresh: bool = False) -> dict[str, Any]:
    path = _cache_path(filters)
    if not force_refresh:
        cached = read_json_cache(path)
        if cached:
            cached["cache_status"] = "fresh"
            return cached
    records: list[dict[str, Any]] = []
    seen: set[str] = set()
    page_count = 0
    try:
        for page in range(1, MAX_PAGES + 1):
            page_html = _decode(fetch_bytes(_list_url(filters, page)))
            page_records, has_next = _parse_list_page(page_html)
            page_count = page
            new_count = 0
            for record in page_records:
                if record["solid"] not in seen:
                    seen.add(record["solid"])
                    records.append(record)
                    new_count += 1
            if not has_next or not page_records or not new_count:
                break
        payload = {
            "filters": filters,
            "fetched_at": utc_now_iso(),
            "page_count": page_count,
            "record_count": len(records),
            "records": records,
            "cache_status": "fresh",
            "truncated": page_count >= MAX_PAGES,
        }
        write_json_atomic(path, payload)
        return payload
    except Exception as exc:
        try:
            stale = json.loads(path.read_text(encoding="utf-8"))
        except (FileNotFoundError, OSError, json.JSONDecodeError):
            raise
        stale["cache_status"] = "stale"
        stale["cache_warning"] = str(exc)
        return stale


DETAIL_LABELS = {
    "信息编号": "purchase_id",
    "船舶类型": "vessel_type",
    "载重/容量": "capacity",
    "船龄": "age_range",
    "船旗": "flag",
    "有效期限": "valid_until",
    "发布日期": "published_date",
    "备注": "remarks",
    "发布公司": "company_name",
    "联系人": "contact_name",
    "信用等级": "credit_rating",
    "所在部门": "department",
    "电话": "telephone",
    "微信/QQ": "wechat_qq",
    "手机": "mobile",
    "邮件": "email",
    "公司网站": "company_website",
}
CONTACT_FIELDS = {"contact_name", "telephone", "wechat_qq", "mobile", "email"}
REMOVED_DETAIL_FIELDS = {"membership_type", "membership_points"}


def _remove_membership_fields(detail: dict[str, Any]) -> bool:
    """Remove fields that must never be retained or returned."""
    changed = False
    for field in REMOVED_DETAIL_FIELDS:
        if field in detail:
            detail.pop(field, None)
            changed = True
    return changed


def _label(value: str) -> str:
    return re.sub(r"\s+", "", value.replace("\xa0", "")).strip(":：;；")


def _visible(value: str, contact_field: bool) -> str:
    cleaned = normalize_space(value)
    if not cleaned:
        return ""
    if contact_field and (
        re.search(r"(付费|支付|购买|登录后|会员可见|未开通)", cleaned)
        or re.search(r"[*＊•·xX]{2,}", cleaned)
    ):
        return ""
    if cleaned.casefold() in {"http://", "https://", "-", "无", "暂无"}:
        return ""
    return cleaned


def _detail_path(solid: str) -> Path:
    return cache_dir() / "details" / f"{solid}.json"


def get_purchase_detail(solid: str, force_refresh: bool = False) -> dict[str, Any]:
    if not re.fullmatch(r"[A-Za-z0-9]+", solid or ""):
        raise ValueError("solid格式无效")
    path = _detail_path(solid)
    if not force_refresh:
        cached = read_json_cache(path)
        if cached:
            if _remove_membership_fields(cached):
                write_json_atomic(path, cached)
            cached["cache_status"] = "fresh"
            return cached
    url = f"{BASE_URL}/purchase_msg.asp?" + urllib.parse.urlencode({"solid": solid})
    page_html = _decode(fetch_bytes(url))
    parser = TableRowParser()
    parser.feed(page_html)
    detail: dict[str, Any] = {"solid": solid}
    for cells, _ in parser.rows:
        index = 0
        while index + 1 < len(cells):
            field = DETAIL_LABELS.get(_label(cells[index]))
            if not field:
                index += 1
                continue
            next_label = _label(cells[index + 1])
            value = ""
            if next_label not in DETAIL_LABELS:
                value = _visible(cells[index + 1], field in CONTACT_FIELDS)
            if value and not detail.get(field):
                detail[field] = value
            index += 2
    for field in DETAIL_LABELS.values():
        detail.setdefault(field, "")
    detail["contact_access"] = (
        "visible" if any(detail.get(field) for field in CONTACT_FIELDS) else "empty_or_paid"
    )
    detail["fetched_at"] = utc_now_iso()
    detail["cache_status"] = "fresh"
    _remove_membership_fields(detail)
    write_json_atomic(path, detail)
    return detail
