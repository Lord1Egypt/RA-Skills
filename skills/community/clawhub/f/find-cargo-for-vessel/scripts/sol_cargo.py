from __future__ import annotations

import html
import json
import re
import time
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
CARGO_TTL_SECONDS = 12 * 60 * 60


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
        f"{BASE_URL}/open_cargo.asp?"
        + urllib.parse.urlencode({"typeclass": trade_code, "pageno": page})
    )


def _parse_list_page(page_html: str, trade_code: str) -> tuple[list[dict], int]:
    parser = TableRowParser()
    parser.feed(page_html)
    records: list[dict] = []
    for cells, links in parser.rows:
        if len(cells) < 9 or not re.fullmatch(r"C\d+", cells[1] or ""):
            continue
        solid = ""
        for link in links:
            match = re.search(r"cargo_msg\.asp\?solid=([A-Za-z0-9]+)", link, re.I)
            if match:
                solid = match.group(1)
                break
        if not solid:
            continue
        records.append(
            {
                "cargo_id": cells[1],
                "company_name": cells[2],
                "cargo_name": cells[3],
                "quantity_raw": cells[4],
                "load_port_raw": cells[5],
                "discharge_port_raw": cells[6],
                "loading_time": cells[7],
                "updated_date": cells[8],
                "solid": solid,
                "trade_code": trade_code,
            }
        )
    pages_match = re.search(r"当前第\s*\d+\s*/\s*(\d+)\s*页", page_html)
    page_count = int(pages_match.group(1)) if pages_match else 1
    return records, page_count


def _cargo_cache_path(trade_code: str) -> Path:
    return cache_dir() / f"cargo_{trade_code}.json"


def _load_stale(path: Path) -> dict | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, OSError, json.JSONDecodeError):
        return None


def _fetch_page(trade_code: str, page: int) -> list[dict]:
    page_html = _decode_page(fetch_bytes(_list_url(trade_code, page)))
    records, _ = _parse_list_page(page_html, trade_code)
    return records


def get_cargo_list(trade_code: str, force_refresh: bool = False) -> dict:
    if trade_code not in {"A", "B"}:
        raise ValueError("trade_code 必须是 A 或 B")
    path = _cargo_cache_path(trade_code)
    if not force_refresh:
        cached = read_json_cache(path, CARGO_TTL_SECONDS)
        if cached:
            cached["cache_status"] = "fresh"
            return cached

    try:
        first_html = _decode_page(fetch_bytes(_list_url(trade_code, 1)))
        first_records, page_count = _parse_list_page(first_html, trade_code)
        records_by_page: dict[int, list[dict]] = {1: first_records}
        if page_count > 1:
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


def parse_quantity_tons(raw: str) -> dict:
    value = normalize_space(unicase(raw))
    if not value:
        return {"status": "manual_confirmation", "min_tons": None}
    if re.search(r"(teu|立方|m3|m³|方|桶|支|vlcc)", value) and not re.search(
        r"(吨|mt\b|mts\b|bdmt|dwt)", value
    ):
        return {"status": "manual_confirmation", "min_tons": None}
    if re.search(r"(详情|大量|一直有货|长期|合同)", value) and not re.search(
        r"\d", value
    ):
        return {"status": "manual_confirmation", "min_tons": None}

    normalized = (
        value.replace(",", "")
        .replace("，", "")
        .replace("～", "-")
        .replace("—", "-")
        .replace("–", "-")
        .replace("--", "-")
    )

    def scaled(number: str, unit: str | None) -> float:
        amount = float(number)
        label = (unit or "").lower()
        if label in {"万", "w"}:
            amount *= 10000
        elif label in {"k", "thousand", "thousands"}:
            amount *= 1000
        return amount

    range_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(万|w|k|thousand|thousands)?\s*-\s*"
        r"(\d+(?:\.\d+)?)\s*(万|w|k|thousand|thousands)?",
        normalized,
    )
    if range_match:
        left_unit = range_match.group(2) or range_match.group(4)
        right_unit = range_match.group(4) or range_match.group(2)
        left = scaled(range_match.group(1), left_unit)
        right = scaled(range_match.group(3), right_unit)
        if not left_unit and not right_unit:
            if left < 1000 <= right and left * 1000 <= right * 1.5:
                left *= 1000
            elif right < 1000 <= left and right * 1000 <= left * 1.5:
                right *= 1000
            elif max(left, right) < 1000 and not re.search(
                r"(吨|mt\b|mts\b|bdmt|dwt)",
                normalized,
            ):
                return {
                    "status": "manual_confirmation",
                    "min_tons": None,
                }
        return {
            "status": "parsed",
            "min_tons": min(left, right),
            "max_tons": max(left, right),
        }

    number_match = re.search(
        r"(\d+(?:\.\d+)?)\s*(万|w|k|thousand|thousands)?", normalized
    )
    if not number_match:
        return {"status": "manual_confirmation", "min_tons": None}
    amount = scaled(number_match.group(1), number_match.group(2))
    if (
        not number_match.group(2)
        and amount < 100
        and not re.search(r"(吨|mt\b|mts\b|bdmt|dwt)", normalized)
    ):
        return {"status": "manual_confirmation", "min_tons": None}
    tolerance_match = re.search(r"[±+/-]+\s*(\d+(?:\.\d+)?)\s*%", normalized)
    minimum = amount
    maximum = amount
    if tolerance_match:
        tolerance = float(tolerance_match.group(1)) / 100
        minimum = amount * (1 - tolerance)
        maximum = amount * (1 + tolerance)
    return {"status": "parsed", "min_tons": minimum, "max_tons": maximum}


def unicase(value: str) -> str:
    return html.unescape(value or "").casefold()


DETAIL_LABELS = {
    "货名": "cargo_name",
    "装港": "load_port",
    "货量": "quantity",
    "卸港": "discharge_port",
    "装货日期": "loading_date",
    "详细信息及其他要求": "requirements",
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
    "mobile",
    "telephone",
    "wechat_qq",
    "contact_name",
    "email",
    "online_contact",
}


def _normalize_label(value: str) -> str:
    value = value.replace("\xa0", "")
    value = re.sub(r"\s+", "", value)
    return value.strip(":：;；")


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


def get_cargo_detail(solid: str) -> dict:
    if not re.fullmatch(r"[A-Za-z0-9]+", solid or ""):
        raise ValueError("solid 格式无效")
    url = f"{BASE_URL}/cargo_msg.asp?" + urllib.parse.urlencode({"solid": solid})
    page_html = _decode_page(fetch_bytes(url))
    parser = TableRowParser()
    parser.feed(page_html)

    detail: dict[str, Any] = {
        "solid": solid,
        "cargo_id": "",
        "title": "",
    }
    cargo_id_match = re.search(r"货盘编号[：:\s]*(C\d+)", page_html)
    if cargo_id_match:
        detail["cargo_id"] = cargo_id_match.group(1)
    title_match = re.search(r"<h3[^>]*>(.*?)</h3>", page_html, re.I | re.S)
    if title_match:
        detail["title"] = normalize_space(
            re.sub(r"<[^>]+>", " ", html.unescape(title_match.group(1)))
        )

    for cells, _ in parser.rows:
        index = 0
        while index + 1 < len(cells):
            label = _normalize_label(cells[index])
            field = DETAIL_LABELS.get(label)
            if field:
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
            else:
                index += 1

    for field in DETAIL_LABELS.values():
        detail.setdefault(field, "")
    detail["contact_access"] = (
        "visible"
        if any(detail.get(field) for field in CONTACT_FIELDS)
        else "empty_or_paid"
    )
    return detail
