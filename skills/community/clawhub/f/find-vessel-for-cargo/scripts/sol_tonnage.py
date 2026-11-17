from __future__ import annotations

import html
import json
import re
import urllib.parse
from concurrent.futures import ThreadPoolExecutor, as_completed
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


BASE_URL = "https://chartering.sol.com.cn"
TONNAGE_TTL_SECONDS = 12 * 60 * 60


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


def _decode_page(data: bytes) -> str:
    return data.decode("gb18030", "replace")


def _list_url(trade_code: str, page: int) -> str:
    return (
        f"{BASE_URL}/open_tonnage.asp?"
        + urllib.parse.urlencode({"typeclass": trade_code, "pageno": page})
    )


def _parse_list_page(page_html: str, trade_code: str) -> tuple[list[dict], int]:
    parser = TableRowParser()
    parser.feed(page_html)
    records: list[dict] = []
    for cells, links in parser.rows:
        if len(cells) < 9 or not re.fullmatch(r"T\d+", cells[1] or ""):
            continue
        solid = ""
        for link in links:
            match = re.search(r"open_msg\.asp\?solid=([A-Za-z0-9]+)", link, re.I)
            if match:
                solid = match.group(1)
                break
        if not solid:
            continue
        records.append(
            {
                "vessel_id": cells[1],
                "company_name": cells[2],
                "vessel_name": cells[3],
                "vessel_type": cells[4],
                "capacity_raw": cells[5],
                "open_port_raw": cells[6],
                "open_date_raw": cells[7],
                "updated_date": cells[8],
                "solid": solid,
                "trade_code": trade_code,
            }
        )
    pages_match = re.search(r"当前第\s*\d+\s*/\s*(\d+)\s*页", page_html)
    return records, int(pages_match.group(1)) if pages_match else 1


def _cache_path(trade_code: str) -> Path:
    return cache_dir() / f"tonnage_{trade_code}.json"


def _load_stale(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None


def _fetch_page(trade_code: str, page: int) -> list[dict]:
    records, _ = _parse_list_page(
        _decode_page(fetch_bytes(_list_url(trade_code, page))),
        trade_code,
    )
    return records


def get_tonnage_list(trade_code: str, force_refresh: bool = False) -> dict:
    if trade_code not in {"A", "B"}:
        raise ValueError("trade_code 必须是 A 或 B")
    path = _cache_path(trade_code)
    if not force_refresh:
        cached = read_json_cache(path, TONNAGE_TTL_SECONDS)
        if cached:
            cached["cache_status"] = "fresh"
            return cached
    try:
        first_html = _decode_page(fetch_bytes(_list_url(trade_code, 1)))
        first_records, page_count = _parse_list_page(first_html, trade_code)
        records_by_page: dict[int, list[dict]] = {1: first_records}
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {
                executor.submit(_fetch_page, trade_code, page): page
                for page in range(2, page_count + 1)
            }
            for future in as_completed(futures):
                records_by_page[futures[future]] = future.result()
        records = [
            record
            for page in sorted(records_by_page)
            for record in records_by_page[page]
        ]
        payload = {
            "trade_code": trade_code,
            "fetched_at": utc_now_iso(),
            "page_count": page_count,
            "record_count": len(records),
            "records": records,
            "cache_status": "fresh",
        }
        write_json_atomic(path, payload)
        return payload
    except Exception as exc:
        stale = _load_stale(path)
        if stale:
            stale["cache_status"] = "stale"
            stale["cache_warning"] = str(exc)
            return stale
        raise


def _scaled(number: str, unit: str | None) -> float:
    amount = float(number.replace(",", ""))
    label = (unit or "").casefold()
    if label in {"万", "w"}:
        amount *= 10000
    elif label in {"k", "千"}:
        amount *= 1000
    return amount


def parse_capacity_tons(raw: str) -> dict[str, Any]:
    value = html.unescape(normalize_space(raw)).casefold()
    if (
        not value
        or re.search(r"\d+\s*[*×x]\s*\d+", value)
        or (
            re.search(r"(m3|m³|cbm|立方|方)", value)
            and not re.search(r"(载重吨|吨|dwt|dwcc|mt\b|mts\b)", value)
        )
    ):
        return {
            "status": "manual_confirmation",
            "min_tons": None,
            "max_tons": None,
        }
    normalized = (
        value.replace("，", ",")
        .replace("～", "-")
        .replace("—", "-")
        .replace("–", "-")
        .replace("--", "-")
    )
    range_match = re.search(
        r"(\d[\d,]*(?:\.\d+)?)\s*(万|w|k|千)?\s*-\s*"
        r"(\d[\d,]*(?:\.\d+)?)\s*(万|w|k|千)?",
        normalized,
    )
    if range_match:
        left_unit = range_match.group(2) or range_match.group(4)
        right_unit = range_match.group(4) or range_match.group(2)
        left = _scaled(range_match.group(1), left_unit)
        right = _scaled(range_match.group(3), right_unit)
        return {
            "status": "parsed",
            "min_tons": min(left, right),
            "max_tons": max(left, right),
        }
    number_match = re.search(
        r"(\d[\d,]*(?:\.\d+)?)\s*(万|w|k|千)?\s*"
        r"(?:载重吨|吨|dwt|dwcc|mt|mts|t\b)?",
        normalized,
    )
    if not number_match:
        return {
            "status": "manual_confirmation",
            "min_tons": None,
            "max_tons": None,
        }
    amount = _scaled(number_match.group(1), number_match.group(2))
    if amount <= 0:
        return {
            "status": "manual_confirmation",
            "min_tons": None,
            "max_tons": None,
        }
    return {"status": "parsed", "min_tons": amount, "max_tons": amount}


DETAIL_LABELS = {
    "船名": "vessel_name",
    "船型": "vessel_type",
    "船舶容量": "capacity",
    "空船港口": "open_port",
    "空船日期": "open_date",
    "船舶详细规范": "specifications",
    "发布日期": "published_date",
    "更新日期": "updated_date",
    "发布公司": "company_name",
    "手机号码": "mobile",
    "联系电话": "telephone",
    "会员类型": "membership_type",
    "微信/QQ": "wechat_qq",
    "联系人": "contact_name",
    "邮件": "email",
    "在线联系": "online_contact",
    "公司网站": "company_website",
}
CONTACT_FIELDS = {
    "mobile", "telephone", "wechat_qq", "contact_name", "email", "online_contact",
}


def _normalize_label(value: str) -> str:
    return re.sub(r"\s+", "", value.replace("\xa0", "")).strip(":：;；")


def _visible_value(value: str, contact_field: bool) -> str:
    cleaned = normalize_space(value)
    if not cleaned:
        return ""
    if contact_field and (
        re.search(r"(付费|支付|购买|登录后|会员可见|联系网站|未开通)", cleaned)
        or re.search(r"[*＊•·xX]{3,}", cleaned)
    ):
        return ""
    if cleaned.casefold() in {"http://", "https://", "-", "无", "暂无"}:
        return ""
    return cleaned


def _detail_cache_path(solid: str) -> Path:
    return cache_dir() / "details" / f"{solid}.json"


def get_vessel_detail(solid: str, force_refresh: bool = False) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9]+", solid or ""):
        raise ValueError("solid 格式无效")
    path = _detail_cache_path(solid)
    if not force_refresh:
        cached = read_json_cache(path, TONNAGE_TTL_SECONDS)
        if cached:
            cached["cache_status"] = "fresh"
            return cached
    url = f"{BASE_URL}/open_msg.asp?" + urllib.parse.urlencode({"solid": solid})
    page_html = _decode_page(fetch_bytes(url))
    parser = TableRowParser()
    parser.feed(page_html)
    detail: dict[str, Any] = {
        "solid": solid,
        "vessel_id": "",
        "title": "",
    }
    id_match = re.search(r"空船编号[：:\s]*(T\d+)", page_html)
    if id_match:
        detail["vessel_id"] = id_match.group(1)
    title_match = re.search(r"<h3[^>]*>(.*?)</h3>", page_html, re.I | re.S)
    if title_match:
        detail["title"] = normalize_space(
            re.sub(r"<[^>]+>", " ", html.unescape(title_match.group(1)))
        )
    for cells, _ in parser.rows:
        index = 0
        while index + 1 < len(cells):
            field = DETAIL_LABELS.get(_normalize_label(cells[index]))
            if not field:
                index += 1
                continue
            next_label = _normalize_label(cells[index + 1])
            value = ""
            if next_label not in DETAIL_LABELS:
                value = _visible_value(
                    cells[index + 1],
                    contact_field=field in CONTACT_FIELDS,
                )
            if value and not detail.get(field):
                detail[field] = value
            index += 2
    for field in DETAIL_LABELS.values():
        detail.setdefault(field, "")
    detail["contact_access"] = (
        "visible"
        if any(detail.get(field) for field in CONTACT_FIELDS)
        else "empty_or_paid"
    )
    detail["fetched_at"] = utc_now_iso()
    detail["cache_status"] = "fresh"
    write_json_atomic(path, detail)
    return detail
