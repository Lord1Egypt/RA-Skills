#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Collect public evidence for Codex to analyze an A-share stock move.

This script intentionally does not call any LLM service and does not read
credentials. It gathers quote data, Eastmoney guba posts/news-like rows,
announcements, market indexes, sector board ranks, and A-share breadth, then
prints a compact evidence brief for Codex to analyze.
"""

from __future__ import annotations

import argparse
import ast
import datetime as dt
import gzip
import html
import json
import random
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from typing import Any


CST = dt.timezone(dt.timedelta(hours=8), "CST")
EASTMONEY_QUOTE_API = "https://push2delay.eastmoney.com"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)

POSITIVE_WORDS = [
    "涨停",
    "封板",
    "反包",
    "龙头",
    "主线",
    "加速",
    "突破",
    "放量",
    "利好",
    "订单",
    "中标",
    "重组",
    "回购",
    "增持",
    "业绩增长",
    "超预期",
    "涨价",
    "国产替代",
]
NEGATIVE_WORDS = [
    "跌停",
    "炸板",
    "断板",
    "天地板",
    "核按钮",
    "退潮",
    "出货",
    "减持",
    "亏损",
    "不及预期",
    "下滑",
    "问询",
    "监管",
    "风险",
    "破位",
]
NEWS_KEYWORDS = [
    "公告",
    "业绩",
    "预告",
    "快报",
    "中报",
    "年报",
    "一季报",
    "合作",
    "签订",
    "订单",
    "中标",
    "回购",
    "增持",
    "减持",
    "重组",
    "并购",
    "定增",
    "涨价",
    "政策",
    "出口",
    "机器人",
    "AI",
    "芯片",
    "算力",
    "低空",
    "固态电池",
]


def now_cst() -> dt.datetime:
    return dt.datetime.now(CST).replace(tzinfo=None)


def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = re.sub(r"<!--.*?-->", "", value, flags=re.DOTALL)
    value = re.sub(r"<script.*?</script>", "", value, flags=re.DOTALL | re.IGNORECASE)
    value = re.sub(r"<style.*?</style>", "", value, flags=re.DOTALL | re.IGNORECASE)
    value = re.sub(r"<[^>]+>", "", value)
    value = re.sub(r"\s+", " ", value).strip()
    return value


def decode_response_body(body: bytes, charset: str | None = None) -> str:
    candidates: list[str] = []
    if charset:
        candidates.append(charset)
    head = body[:4096].decode("ascii", errors="ignore")
    match = re.search(r"charset=['\"]?([a-zA-Z0-9_\-]+)", head, flags=re.IGNORECASE)
    if match:
        candidates.append(match.group(1))
    candidates.extend(["utf-8", "gb18030", "gbk"])
    seen: set[str] = set()
    for encoding in candidates:
        normalized = encoding.lower()
        if normalized in seen:
            continue
        seen.add(normalized)
        try:
            return body.decode(encoding)
        except Exception:
            continue
    return body.decode("utf-8", errors="ignore")


def fetch_url(url: str, referer: str | None = None, timeout: int = 20, pause: bool = True) -> str:
    last_exc: Exception | None = None
    for attempt in range(3):
        if pause or attempt:
            time.sleep(random.uniform(0.35, 1.0) + attempt * 0.4)
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": USER_AGENT,
                "Accept": "text/html,application/xhtml+xml,application/json,*/*;q=0.8",
                "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.7",
                "Accept-Encoding": "gzip, deflate",
                "Referer": referer or "https://www.eastmoney.com/",
                "Cache-Control": "max-age=0",
                "Connection": "close",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=timeout) as response:
                body = response.read()
                encoding = response.info().get("Content-Encoding", "")
                if encoding == "gzip":
                    body = gzip.decompress(body)
                elif encoding == "deflate":
                    import zlib

                    body = zlib.decompress(body)
                return decode_response_body(body, response.headers.get_content_charset())
        except Exception as exc:
            last_exc = exc
    try:
        result = subprocess.run(
            ["curl", "-L", "--silent", "--show-error", "--max-time", str(timeout), url],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
        )
        return decode_response_body(result.stdout)
    except Exception:
        raise last_exc or RuntimeError("fetch failed")


def normalize_stock(raw: str) -> dict[str, str]:
    text = raw.strip().lower()
    if not text:
        raise ValueError("stock code is empty")
    match = re.search(r"(\d{6})", text)
    if not match:
        raise ValueError(f"cannot find 6-digit A-share code in {raw!r}")
    code = match.group(1)
    if text.startswith("sh") or code.startswith(("5", "6", "9")):
        market = "sh"
        secid = f"1.{code}"
    elif text.startswith("sz") or code.startswith(("0", "2", "3")):
        market = "sz"
        secid = f"0.{code}"
    elif text.startswith("bj") or code.startswith(("4", "8")):
        market = "bj"
        secid = f"0.{code}"
    else:
        market = "sh" if code.startswith("6") else "sz"
        secid = f"{'1' if market == 'sh' else '0'}.{code}"
    return {"code": code, "market": market, "secid": secid, "symbol": f"{market}{code}"}


def eastmoney_quote_url(secid: str) -> str:
    fields = ",".join(
        [
            "f43",
            "f44",
            "f45",
            "f46",
            "f47",
            "f48",
            "f57",
            "f58",
            "f60",
            "f116",
            "f162",
            "f167",
            "f168",
            "f170",
            "f171",
            "f172",
            "f173",
            "f292",
        ]
    )
    return f"{EASTMONEY_QUOTE_API}/api/qt/stock/get?secid={urllib.parse.quote(secid)}&fields={fields}"


def scaled(value: Any, divisor: float = 100.0) -> float | None:
    if value in [None, "-", ""]:
        return None
    try:
        return float(value) / divisor
    except (TypeError, ValueError):
        return None


def raw_num(value: Any) -> float | int | None:
    if value in [None, "-", ""]:
        return None
    try:
        num = float(value)
        return int(num) if num.is_integer() else num
    except (TypeError, ValueError):
        return None


def fetch_quote(stock: dict[str, str]) -> dict[str, Any]:
    url = eastmoney_quote_url(stock["secid"])
    payload = json.loads(fetch_url(url, pause=False))
    data = payload.get("data") or {}
    if not data:
        return {"url": url, "error": "empty quote data"}
    return {
        "url": url,
        "code": data.get("f57") or stock["code"],
        "name": data.get("f58") or "",
        "price": scaled(data.get("f43")),
        "high": scaled(data.get("f44")),
        "low": scaled(data.get("f45")),
        "open": scaled(data.get("f46")),
        "volume_lots": raw_num(data.get("f47")),
        "amount": raw_num(data.get("f48")),
        "previous_close": scaled(data.get("f60")),
        "market_cap": raw_num(data.get("f116")),
        "pe": scaled(data.get("f162")),
        "pb": scaled(data.get("f167")),
        "turnover_pct": scaled(data.get("f168")),
        "change_pct": scaled(data.get("f170")),
        "amplitude_pct": scaled(data.get("f171")),
        "roe_pct": raw_num(data.get("f173")),
        "status": data.get("f292"),
        "source": "Eastmoney quote",
    }


def parse_cst_datetime(value: str) -> dt.datetime | None:
    text = clean_text(value)
    current = now_cst()
    patterns = [
        (r"(\d{4})[-/](\d{1,2})[-/](\d{1,2})\s+(\d{1,2}):(\d{1,2})(?::\d{1,2})?", True),
        (r"(\d{1,2})[-/](\d{1,2})\s+(\d{1,2}):(\d{1,2})", False),
    ]
    for pattern, has_year in patterns:
        match = re.search(pattern, text)
        if not match:
            continue
        try:
            if has_year:
                year, month, day, hour, minute = [int(x) for x in match.groups()]
            else:
                month, day, hour, minute = [int(x) for x in match.groups()]
                year = current.year
            parsed = dt.datetime(year, month, day, hour, minute)
            if not has_year and parsed > current + dt.timedelta(days=1):
                parsed = parsed.replace(year=year - 1)
            return parsed
        except ValueError:
            continue
    return None


def within_hours(value: str, hours: int) -> bool:
    parsed = parse_cst_datetime(value)
    if not parsed:
        return True
    return now_cst() - dt.timedelta(hours=hours) <= parsed <= now_cst() + dt.timedelta(minutes=5)


def age_label(value: str) -> str:
    parsed = parse_cst_datetime(value)
    if not parsed:
        return ""
    hours = max(0.0, (now_cst() - parsed).total_seconds() / 3600)
    if hours < 1:
        return f"{int(hours * 60)}分钟前"
    if hours < 48:
        return f"{hours:.1f}小时前"
    return f"{hours / 24:.1f}天前"


class GubaTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[dict[str, str]] = []
        self.in_tr = False
        self.in_td = False
        self.in_anchor = False
        self.row_tds: list[str] = []
        self.current_td = ""
        self.current_href = ""
        self.current_title = ""
        self.row_link = ""
        self.td_index = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attrs_d = {k: v or "" for k, v in attrs}
        if tag == "tr" and "listitem" in attrs_d.get("class", ""):
            self.in_tr = True
            self.row_tds = []
            self.row_link = ""
            self.td_index = 0
        if self.in_tr and tag == "td":
            self.in_td = True
            self.current_td = ""
            self.td_index += 1
        if self.in_td and tag == "a":
            self.in_anchor = True
            self.current_href = attrs_d.get("href", "")
            self.current_title = attrs_d.get("title", "")
            if self.td_index == 3 and not self.row_link:
                self.row_link = urllib.parse.urljoin("https://guba.eastmoney.com/", self.current_href)

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self.in_anchor:
            self.in_anchor = False
        if tag == "td" and self.in_td:
            self.in_td = False
            self.row_tds.append(clean_text(self.current_td))
        if tag == "tr" and self.in_tr:
            self.in_tr = False
            if len(self.row_tds) >= 5:
                self.rows.append(
                    {
                        "read": self.row_tds[0],
                        "reply": self.row_tds[1],
                        "title": self.row_tds[2],
                        "author": self.row_tds[3],
                        "time": self.row_tds[4],
                        "link": self.row_link,
                    }
                )
            self.current_href = ""
            self.current_title = ""

    def handle_data(self, data: str) -> None:
        if self.in_td:
            self.current_td += data


class SimpleTableRowParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.rows: list[list[str]] = []
        self.in_tr = False
        self.in_cell = False
        self.current_row: list[str] = []
        self.current_cell = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "tr":
            self.in_tr = True
            self.current_row = []
        if self.in_tr and tag in ["td", "th"]:
            self.in_cell = True
            self.current_cell = ""

    def handle_endtag(self, tag: str) -> None:
        if tag in ["td", "th"] and self.in_cell:
            self.in_cell = False
            self.current_row.append(clean_text(self.current_cell))
        if tag == "tr" and self.in_tr:
            self.in_tr = False
            if self.current_row:
                self.rows.append(self.current_row)

    def handle_data(self, data: str) -> None:
        if self.in_cell:
            self.current_cell += data


def parse_int(value: Any) -> int:
    text = re.sub(r"[^\d]", "", str(value or ""))
    return int(text) if text else 0


def score_post(item: dict[str, Any]) -> tuple[int, dt.datetime, int]:
    title = str(item.get("title") or "")
    read = parse_int(item.get("read") or item.get("post_click_count"))
    reply = parse_int(item.get("reply") or item.get("post_comment_count"))
    likes = parse_int(item.get("post_like_count"))
    parsed = parse_cst_datetime(str(item.get("time") or item.get("post_last_time") or item.get("post_publish_time") or "")) or dt.datetime(1970, 1, 1)
    keyword_score = min(8, sum(1 for word in NEWS_KEYWORDS if word.lower() in title.lower()) * 2)
    activity_score = min(8, read // 2000 + reply // 20 + likes // 30)
    recency_score = 5 if (now_cst() - parsed).total_seconds() <= 6 * 3600 else 3
    return keyword_score + activity_score + recency_score, parsed, read


def fetch_guba(code: str, hours: int, limit: int) -> dict[str, Any]:
    url = f"https://guba.eastmoney.com/list,{urllib.parse.quote(code)}.html"
    try:
        page = fetch_url(url, referer="https://guba.eastmoney.com/")
        parser = GubaTableParser()
        parser.feed(page)
        rows = [row for row in parser.rows if within_hours(row.get("time", ""), hours)]

        # Newer pages also embed a JSON post_list. Use it when possible because it
        # includes read/comment/like counts and article text snippets.
        embedded: list[dict[str, Any]] = []
        match = re.search(r'"post_list"\s*:\s*(\[.*?\])\s*,\s*"ret"', page, flags=re.DOTALL)
        if match:
            try:
                for raw in json.loads(match.group(1)):
                    embedded.append(
                        {
                            "title": clean_text(raw.get("post_title", "")),
                            "time": raw.get("post_last_time") or raw.get("post_publish_time") or "",
                            "read": raw.get("post_click_count", 0),
                            "reply": raw.get("post_comment_count", 0),
                            "like": raw.get("post_like_count", 0),
                            "author": (raw.get("post_user") or {}).get("user_nickname", ""),
                            "content": clean_text(raw.get("post_content", ""))[:260],
                            "link": f"https://guba.eastmoney.com/news,{code},{raw.get('post_id')}.html",
                            "post_type": raw.get("post_type"),
                        }
                    )
            except Exception:
                embedded = []
        items = embedded or rows
        items = [item for item in items if item.get("title") and within_hours(str(item.get("time", "")), hours)]
        items.sort(key=score_post, reverse=True)
        return {"url": url, "posts": items[:limit], "count": len(items), "source": "东方财富股吧"}
    except Exception as exc:
        return {"url": url, "posts": [], "count": 0, "source": "东方财富股吧", "error": str(exc)}


def fetch_announcements(code: str, limit: int) -> dict[str, Any]:
    params = urllib.parse.urlencode(
        {
            "sr": "-1",
            "page_size": str(limit),
            "page_index": "1",
            "ann_type": "A",
            "client_source": "web",
            "stock_list": code,
        }
    )
    url = f"https://np-anotice-stock.eastmoney.com/api/security/ann?{params}"
    try:
        payload = json.loads(fetch_url(url))
        items = []
        for raw in ((payload.get("data") or {}).get("list") or []):
            columns = raw.get("columns") or []
            items.append(
                {
                    "title": clean_text(raw.get("title_ch") or raw.get("title") or ""),
                    "time": raw.get("display_time") or raw.get("notice_date") or "",
                    "columns": "、".join(clean_text(c.get("column_name", "")) for c in columns if c.get("column_name")),
                    "art_code": raw.get("art_code", ""),
                    "source": "东方财富公告",
                }
            )
        return {"url": url, "announcements": items, "source": "东方财富公告"}
    except Exception as exc:
        return {"url": url, "announcements": [], "source": "东方财富公告", "error": str(exc)}


def parse_sohu_peak_array(page: str) -> list[Any]:
    match = re.search(r"PEAK_ODIA\((\[.*?\])\)</script>", page, flags=re.DOTALL)
    if not match:
        raise ValueError("cannot find Sohu PEAK_ODIA payload")
    return ast.literal_eval(match.group(1))


def sohu_number(value: Any) -> float | None:
    text = str(value or "").replace("%", "").replace(",", "").strip()
    if text in ["", "--"]:
        return None
    try:
        return float(text)
    except ValueError:
        return None


def fetch_sohu_market_indexes() -> dict[str, Any]:
    url = "https://q.stock.sohu.com/zs/zs-2.html"
    target_codes = {"zs_000001", "zs_399001", "zs_399006", "zs_000300", "zs_000016", "zs_399905", "zs_000688", "zs_899050"}
    try:
        payload = parse_sohu_peak_array(fetch_url(url, referer="https://q.stock.sohu.com/cn/zs.shtml"))
        rows = []
        for row in payload[1:]:
            if not isinstance(row, list) or len(row) < 5 or row[0] not in target_codes:
                continue
            rows.append(
                {
                    "code": str(row[0]).replace("zs_", ""),
                    "name": row[1],
                    "price": sohu_number(row[2]),
                    "change": sohu_number(row[3]),
                    "change_pct": sohu_number(row[4]),
                    "amount": sohu_number(row[7]) if len(row) > 7 else None,
                    "link": f"https://q.stock.sohu.com/{row[13]}" if len(row) > 13 else "https://q.stock.sohu.com/cn/zs.shtml",
                }
            )
        return {
            "url": url,
            "reference_url": "https://q.stock.sohu.com/cn/zs.shtml",
            "indexes": rows,
            "source": "搜狐证券指数行情",
        }
    except Exception as exc:
        return {"url": url, "reference_url": "https://q.stock.sohu.com/cn/zs.shtml", "indexes": [], "source": "搜狐证券指数行情", "error": str(exc)}


def fetch_sohu_board_rank(name: str, plate_id: str, limit: int = 8) -> dict[str, Any]:
    url = f"https://q.stock.sohu.com/pl/pl-{plate_id}.html"
    try:
        payload = parse_sohu_peak_array(fetch_url(url, referer="https://q.stock.sohu.com/cn/bk.shtml"))
        boards = []
        for row in payload[1:]:
            if not isinstance(row, list) or len(row) < 13:
                continue
            boards.append(
                {
                    "code": row[0],
                    "name": row[1],
                    "stock_count": parse_int(row[2]),
                    "avg_price": sohu_number(row[3]),
                    "change": sohu_number(row[4]),
                    "change_pct": sohu_number(row[5]),
                    "amount": sohu_number(row[7]),
                    "leader_code": str(row[8]).replace("cn_", ""),
                    "leader_name": row[9],
                    "leader_price": sohu_number(row[10]),
                    "leader_change": sohu_number(row[11]),
                    "leader_change_pct": sohu_number(row[12]),
                    "link": f"https://q.stock.sohu.com/cn/bk_{row[0]}.shtml",
                }
            )
        boards.sort(key=lambda item: item.get("change_pct") if isinstance(item.get("change_pct"), float) else -9999, reverse=True)
        return {
            "url": url,
            "reference_url": "https://q.stock.sohu.com/cn/bk.shtml",
            "top_gain": boards[:limit],
            "top_loss": list(reversed(boards[-limit:])) if len(boards) > limit else [],
            "source": f"搜狐证券{name}板块行情",
        }
    except Exception as exc:
        return {
            "url": url,
            "reference_url": "https://q.stock.sohu.com/cn/bk.shtml",
            "top_gain": [],
            "top_loss": [],
            "source": f"搜狐证券{name}板块行情",
            "error": str(exc),
        }


def eastmoney_clist_url(fs: str, fields: str, *, pn: int = 1, pz: int = 100, po: int = 1, fid: str = "f3") -> str:
    params = urllib.parse.urlencode(
        {
            "pn": pn,
            "pz": pz,
            "po": po,
            "np": 1,
            "fltt": 2,
            "invt": 2,
            "fid": fid,
            "fs": fs,
            "fields": fields,
        }
    )
    return f"{EASTMONEY_QUOTE_API}/api/qt/clist/get?{params}"


def parse_eastmoney_rows(url: str) -> tuple[int, list[dict[str, Any]]]:
    payload = json.loads(fetch_url(url, pause=False))
    data = payload.get("data") or {}
    return int(data.get("total") or 0), data.get("diff") or []


def fetch_eastmoney_market_indexes() -> dict[str, Any]:
    fields = "f12,f14,f2,f3,f4,f6"
    secids = "1.000001,0.399001,0.399006,1.000688,1.000300,0.399905"
    url = f"{EASTMONEY_QUOTE_API}/api/qt/ulist.np/get?secids={urllib.parse.quote(secids)}&fields={fields}"
    try:
        _, rows = parse_eastmoney_rows(url)
        return {"url": url, "indexes": rows, "source": "Eastmoney index quotes"}
    except Exception as exc:
        return {"url": url, "indexes": [], "source": "Eastmoney index quotes", "error": str(exc)}


def fetch_board_rank(name: str, fs: str, limit: int = 8) -> dict[str, Any]:
    fields = "f12,f14,f2,f3,f4,f6,f62"
    gain_url = eastmoney_clist_url(fs, fields, pn=1, pz=limit, po=1, fid="f3")
    loss_url = eastmoney_clist_url(fs, fields, pn=1, pz=limit, po=0, fid="f3")
    try:
        _, top_gain = parse_eastmoney_rows(gain_url)
        _, top_loss = parse_eastmoney_rows(loss_url)
        return {
            "url": gain_url,
            "top_gain": top_gain[:limit],
            "top_loss": top_loss[:limit],
            "source": f"Eastmoney {name} board rank",
        }
    except Exception as exc:
        return {"url": gain_url, "top_gain": [], "top_loss": [], "source": f"Eastmoney {name} board rank", "error": str(exc)}


def fetch_eastmoney_intraday_breadth() -> dict[str, Any]:
    fields = "f12,f14,f2,f3,f104,f105,f106"
    secids = "1.000001,0.399001"
    url = f"{EASTMONEY_QUOTE_API}/api/qt/ulist.np/get?secids={urllib.parse.quote(secids)}&fields={fields}"
    try:
        _, rows = parse_eastmoney_rows(url)
        markets: list[dict[str, Any]] = []
        up = down = flat = 0
        for row in rows:
            market_up = parse_int(row.get("f104"))
            market_down = parse_int(row.get("f105"))
            market_flat = parse_int(row.get("f106"))
            up += market_up
            down += market_down
            flat += market_flat
            markets.append(
                {
                    "code": row.get("f12"),
                    "name": row.get("f14"),
                    "change_pct": row.get("f3"),
                    "up": market_up,
                    "down": market_down,
                    "flat": market_flat,
                }
            )
        if not markets or not (up or down or flat):
            raise ValueError("missing Eastmoney index breadth fields f104/f105/f106")
        return {
            "url": url,
            "reference_url": "https://quote.eastmoney.com/zs000001.html",
            "date": now_cst().strftime("%m/%d"),
            "total": up + down + flat if up or down or flat else None,
            "up": up,
            "down": down,
            "flat": flat,
            "markets": markets,
            "source": "东方财富指数页今日涨跌家数",
        }
    except Exception as exc:
        return {
            "url": url,
            "reference_url": "https://quote.eastmoney.com/zs000001.html",
            "error": str(exc),
            "source": "东方财富指数页今日涨跌家数",
        }


def fetch_sohu_zdt_history() -> dict[str, Any]:
    url = "https://q.stock.sohu.com/cn/zdt.shtml"
    try:
        page = fetch_url(url, referer="https://q.stock.sohu.com/")
        parser = SimpleTableRowParser()
        parser.feed(page)
        history: list[dict[str, Any]] = []
        for row in parser.rows:
            if len(row) < 14 or not re.match(r"\d{2}/\d{2}$", row[0]):
                continue
            sh_up, sh_flat, sh_down = parse_int(row[5]), parse_int(row[6]), parse_int(row[7])
            sz_up, sz_flat, sz_down = parse_int(row[8]), parse_int(row[9]), parse_int(row[10])
            bj_up, bj_flat, bj_down = parse_int(row[11]), parse_int(row[12]), parse_int(row[13])
            item = {
                "date": row[0],
                "limit_up": parse_int(row[1]),
                "limit_down": parse_int(row[2]),
                "halted": parse_int(row[3]),
                "amount_100m": sohu_number(row[4]),
                "up": sh_up + sz_up + bj_up,
                "flat": sh_flat + sz_flat + bj_flat,
                "down": sh_down + sz_down + bj_down,
                "sh_up": sh_up,
                "sh_flat": sh_flat,
                "sh_down": sh_down,
                "sz_up": sz_up,
                "sz_flat": sz_flat,
                "sz_down": sz_down,
                "bj_up": bj_up,
                "bj_flat": bj_flat,
                "bj_down": bj_down,
            }
            item["total"] = item["up"] + item["flat"] + item["down"]
            history.append(item)
        if not history:
            raise ValueError("cannot parse Sohu zdt table")
        latest = history[0]
        prev = history[1] if len(history) > 1 else {}
        return {
            "url": url,
            "reference_url": url,
            "sample_mode": "sohu_zdt_history",
            "date": latest.get("date", ""),
            "total": latest.get("total"),
            "up": latest.get("up"),
            "down": latest.get("down"),
            "flat": latest.get("flat"),
            "limit_up": latest.get("limit_up"),
            "limit_down": latest.get("limit_down"),
            "halted": latest.get("halted"),
            "amount_100m": latest.get("amount_100m"),
            "prev_up": prev.get("up"),
            "prev_down": prev.get("down"),
            "prev_limit_up": prev.get("limit_up"),
            "prev_limit_down": prev.get("limit_down"),
            "history": history[:10],
            "source": "搜狐证券涨跌停历史数据",
        }
    except Exception as exc:
        return {"url": url, "reference_url": url, "error": str(exc), "source": "搜狐证券涨跌停历史数据"}


def fetch_market_breadth() -> dict[str, Any]:
    intraday = fetch_eastmoney_intraday_breadth()
    history = fetch_sohu_zdt_history()
    history_latest = (history.get("history") or [{}])[0] if history.get("history") else {}
    source_parts = []
    if intraday.get("error"):
        source_parts.append(f"{intraday.get('source')}失败")
    else:
        source_parts.append(str(intraday.get("source")))
    if history.get("error"):
        source_parts.append(f"{history.get('source')}失败")
    else:
        source_parts.append(str(history.get("source")))
    base = intraday if not intraday.get("error") else (history if not history.get("error") else {})
    return {
        "url": intraday.get("url"),
        "reference_url": intraday.get("reference_url"),
        "history_reference_url": history.get("reference_url"),
        "sample_mode": "eastmoney_intraday_plus_sohu_history",
        "date": base.get("date", ""),
        "total": base.get("total"),
        "up": base.get("up"),
        "down": base.get("down"),
        "flat": base.get("flat"),
        "limit_up": base.get("limit_up") if base.get("limit_up") is not None else history_latest.get("limit_up"),
        "limit_down": base.get("limit_down") if base.get("limit_down") is not None else history_latest.get("limit_down"),
        "markets": intraday.get("markets", []),
        "history": history.get("history", []),
        "history_latest": history_latest,
        "intraday_error": intraday.get("error", ""),
        "history_error": history.get("error", ""),
        "error": intraday.get("error") if intraday.get("error") and history.get("error") else "",
        "source": " + ".join(source_parts),
    }


def qualitative_guba_sentiment(posts: list[dict[str, Any]]) -> dict[str, Any]:
    pos = neg = 0
    themes: dict[str, int] = {}
    for post in posts:
        text = f"{post.get('title', '')} {post.get('content', '')}"
        pos += sum(1 for word in POSITIVE_WORDS if word.lower() in text.lower())
        neg += sum(1 for word in NEGATIVE_WORDS if word.lower() in text.lower())
        for word in NEWS_KEYWORDS:
            if word.lower() in text.lower():
                themes[word] = themes.get(word, 0) + 1
    if pos >= neg * 1.6 and pos >= 2:
        label = "偏多"
    elif neg >= pos * 1.6 and neg >= 2:
        label = "偏空"
    elif pos + neg >= 2:
        label = "分歧"
    else:
        label = "低信息量"
    return {
        "label": label,
        "positive_hits": pos,
        "negative_hits": neg,
        "themes": sorted(themes.items(), key=lambda x: x[1], reverse=True)[:8],
    }


def infer_market_phase(breadth: dict[str, Any]) -> str:
    if breadth.get("error"):
        return "无法判断"
    today_missing = bool(breadth.get("intraday_error"))
    limit_up = int(breadth.get("limit_up") or 0)
    limit_down = int(breadth.get("limit_down") or 0)
    up = int(breadth.get("up") or 0)
    down = int(breadth.get("down") or 0)
    history = breadth.get("history") or []
    recent_limit_up = [int(row.get("limit_up") or 0) for row in history[:5]]
    avg_recent_limit_up = sum(recent_limit_up) / len(recent_limit_up) if recent_limit_up else 0
    prev = history[1] if len(history) > 1 else {}
    prev_limit_up = int(prev.get("limit_up") or 0)
    prev_limit_down = int(prev.get("limit_down") or 0)
    limit_up_falling = bool(prev_limit_up and limit_up < prev_limit_up * 0.8)
    limit_down_rising = bool(prev_limit_down and limit_down > prev_limit_down * 1.2)
    breadth_split = bool(up and down and up <= down * 1.25)
    if limit_up <= 20 and (limit_down >= 40 or down > up * 1.5):
        phase = "冰点期"
    elif limit_down > limit_up * 1.2 and down > up * 1.2:
        phase = "退潮期"
    elif (limit_up >= 80 or avg_recent_limit_up >= 90) and (breadth_split or limit_up_falling or limit_down_rising):
        phase = "高位分歧/分化期"
    elif limit_up >= 100 or (avg_recent_limit_up >= 100 and limit_up >= 80):
        phase = "高潮期"
    elif limit_up >= 60 and up > down * 1.3:
        phase = "加速期"
    elif limit_up >= 30:
        phase = "启动期"
    elif up > down * 1.3 and limit_down <= max(10, limit_up):
        phase = "修复期"
    elif down >= up * 1.1:
        phase = "退潮期"
    else:
        phase = "混沌/轮动期"
    if today_missing:
        return f"历史{phase}（今日盘中未确认）"
    return phase


def collect_sources(args: argparse.Namespace) -> dict[str, Any]:
    stock = normalize_stock(args.stock)
    errors: list[str] = []
    try:
        quote = fetch_quote(stock)
        if quote.get("error"):
            errors.append(f"Eastmoney quote: {quote['error']}")
    except Exception as exc:
        quote = {"error": str(exc), "source": "Eastmoney quote"}
        errors.append(f"Eastmoney quote: {exc}")
    guba = fetch_guba(stock["code"], args.hours, args.posts)
    if guba.get("error"):
        errors.append(f"Eastmoney guba: {guba['error']}")
    announcements = fetch_announcements(stock["code"], args.announcements)
    if announcements.get("error"):
        errors.append(f"Eastmoney announcements: {announcements['error']}")
    market_indexes: dict[str, Any] = {}
    board_ranks: dict[str, Any] = {}
    breadth: dict[str, Any] = {}
    if not args.skip_market_context:
        market_indexes = fetch_sohu_market_indexes()
        if market_indexes.get("error") or not market_indexes.get("indexes"):
            errors.append(f"Sohu indexes: {market_indexes.get('error') or 'empty index data'}")
            market_indexes = fetch_eastmoney_market_indexes()
        board_ranks = {
            "industry": fetch_sohu_board_rank("行业", "1631"),
            "concept": fetch_sohu_board_rank("概念", "1630"),
        }
        for key, value in board_ranks.items():
            if value.get("error"):
                errors.append(f"Sohu {key} boards: {value['error']}")
        breadth = fetch_market_breadth()
        if breadth.get("error"):
            errors.append(f"Market breadth: {breadth['error']}")

    posts = guba.get("posts", [])
    sentiment = qualitative_guba_sentiment(posts)
    phase = infer_market_phase(breadth) if breadth else "未采集：已按参数跳过市场背景"

    return {
        "generated_at_cst": now_cst().strftime("%Y-%m-%d %H:%M:%S"),
        "window_hours": args.hours,
        "stock": stock,
        "quote": quote,
        "guba": guba,
        "guba_sentiment": sentiment,
        "announcements": announcements,
        "market_indexes": market_indexes,
        "board_ranks": board_ranks,
        "market_breadth": breadth,
        "market_phase_hint": phase,
        "errors": errors,
    }


def fmt_num(value: Any, digits: int = 2) -> str:
    if isinstance(value, (int, float)):
        if abs(value) >= 100000000:
            return f"{value / 100000000:.2f}亿"
        if digits == 0:
            return f"{value:,.0f}"
        return f"{value:,.{digits}f}".rstrip("0").rstrip(".")
    if value is None or value == "":
        return "-"
    return str(value)


def quote_name(row: dict[str, Any]) -> str:
    return str(row.get("name") or row.get("f14") or "-")


def quote_pct(row: dict[str, Any]) -> str:
    value = row.get("change_pct")
    if value is None:
        value = row.get("f3")
    return fmt_num(value)


def quote_amount(row: dict[str, Any]) -> str:
    return fmt_num(row.get("amount") if row.get("amount") is not None else row.get("f6"))


def render_market_context(data: dict[str, Any], lines: list[str]) -> None:
    indexes = data.get("market_indexes", {})
    boards = data.get("board_ranks", {})
    breadth = data.get("market_breadth", {})
    if not indexes and not boards and not breadth:
        return
    lines.append("")
    lines.append("## 大盘・板块・涨跌家数")
    if indexes:
        lines.append(f"- 指数来源: {indexes.get('source', '-')} / 校验页: {indexes.get('reference_url', indexes.get('url', '-'))}")
        index_text = "、".join(
            f"{quote_name(row)} {quote_pct(row)}%" for row in indexes.get("indexes", [])[:8]
        )
        lines.append(f"- 主要指数: {index_text or '-'}")
    if breadth:
        lines.append(
            f"- 涨跌家数来源: {breadth.get('source', '-')} / 今日页: {breadth.get('reference_url', 'https://quote.eastmoney.com/zs000001.html')} / "
            f"历史页: {breadth.get('history_reference_url', 'https://q.stock.sohu.com/cn/zdt.shtml')}"
        )
        lines.append(
            f"- 阶段提示: {data.get('market_phase_hint')}；日期:{breadth.get('date', '-') or '-'}；"
            f"上涨:{breadth.get('up', '-')}，下跌:{breadth.get('down', '-')}，"
            f"平盘:{breadth.get('flat', '-')}，涨停附近:{breadth.get('limit_up', '-')}，跌停附近:{breadth.get('limit_down', '-')}"
        )
        market_text = "、".join(
            f"{row.get('name')} 涨{row.get('up')}/跌{row.get('down')}/平{row.get('flat')}"
            for row in breadth.get("markets", [])[:4]
        )
        if market_text:
            lines.append(f"- 分市场涨跌家数: {market_text}")
        history_text = "、".join(
            f"{row.get('date')} 涨停{row.get('limit_up')} 跌停{row.get('limit_down')} 涨{row.get('up')}/跌{row.get('down')}"
            for row in breadth.get("history", [])[:5]
        )
        lines.append(f"- 近几日情绪历史: {history_text or '-'}")
        notes = []
        if breadth.get("intraday_error"):
            notes.append(f"今日东方财富接口失败: {breadth.get('intraday_error')}")
        if breadth.get("history_error"):
            notes.append(f"搜狐历史页失败: {breadth.get('history_error')}")
        if notes:
            lines.append(f"- 涨跌家数备注: {'; '.join(notes)}")
    for key, title in [("industry", "行业板块"), ("concept", "概念板块")]:
        board = boards.get(key, {})
        if not board:
            continue
        gain = "、".join(
            f"{item.get('name')}({fmt_num(item.get('change_pct'))}%, 领涨:{item.get('leader_name')} {fmt_num(item.get('leader_change_pct'))}%)"
            for item in board.get("top_gain", [])[:6]
        )
        loss = "、".join(f"{item.get('name')}({fmt_num(item.get('change_pct'))}%)" for item in board.get("top_loss", [])[:4])
        lines.append(f"- {title}来源: {board.get('source', '-')} / 校验页: {board.get('reference_url', '-')}")
        lines.append(f"- {title}涨幅前列: {gain or '-'}")
        lines.append(f"- {title}跌幅前列: {loss or '-'}")


def render_posts(posts: list[dict[str, Any]], lines: list[str]) -> None:
    if not posts:
        lines.append("- 未取得股吧帖子/资讯")
        return
    for idx, item in enumerate(posts, 1):
        time_text = item.get("time") or "时间不明"
        age = age_label(str(time_text))
        age_suffix = f" / {age}" if age else ""
        read = item.get("read", 0)
        reply = item.get("reply", 0)
        like = item.get("like", item.get("post_like_count", 0))
        lines.append(f"{idx}. {time_text}{age_suffix} / 阅读{read} 评论{reply} 赞{like}")
        lines.append(f"   {item.get('title')}")
        content = clean_text(str(item.get("content") or ""))
        if content:
            lines.append(f"   摘要: {content}")
        if item.get("link"):
            lines.append(f"   {item.get('link')}")


def render_markdown(data: dict[str, Any], prompt_only: bool = False) -> str:
    quote = data.get("quote", {})
    stock = data.get("stock", {})
    guba = data.get("guba", {})
    sentiment = data.get("guba_sentiment", {})
    ann = data.get("announcements", {})
    name = quote.get("name") or "-"
    title = f"{stock.get('code')} {name} ({stock.get('symbol')})"
    lines: list[str] = []
    if not prompt_only:
        lines.append(f"# Codex分析材料: {title}")
        lines.append("")
        lines.append(f"- 生成时间(CST): {data.get('generated_at_cst')}")
        lines.append(f"- 目标窗口: 近{data.get('window_hours')}小时为主")
        lines.append(f"- 东方财富行情: https://quote.eastmoney.com/{stock.get('symbol')}.html")
        lines.append(f"- 东方财富股吧: {guba.get('url', '')}")
        lines.append("")
        lines.append("## 基本信息・当前行情")
        lines.append(f"- 现价: {fmt_num(quote.get('price'))}")
        lines.append(f"- 前收: {fmt_num(quote.get('previous_close'))}")
        lines.append(f"- 涨跌幅: {fmt_num(quote.get('change_pct'))}%")
        lines.append(f"- 振幅: {fmt_num(quote.get('amplitude_pct'))}%")
        lines.append(f"- 换手率: {fmt_num(quote.get('turnover_pct'))}%")
        lines.append(f"- 成交额: {fmt_num(quote.get('amount'))}")
        lines.append(f"- 市值: {fmt_num(quote.get('market_cap'))}")
        lines.append(f"- PE / PB: {fmt_num(quote.get('pe'))} / {fmt_num(quote.get('pb'))}")
        render_market_context(data, lines)
        lines.append("")
        lines.append("## 个股公告")
        items = ann.get("announcements", [])
        if items:
            for idx, item in enumerate(items, 1):
                lines.append(f"{idx}. {item.get('time') or '时间不明'} [{item.get('columns') or '公告'}] {item.get('title')}")
        else:
            lines.append("- 未取得公告")
        lines.append("")
        lines.append("## 股吧/资讯材料")
        lines.append(
            f"- 定性情绪: {sentiment.get('label', '-')} "
            f"(多头词:{sentiment.get('positive_hits', 0)}, 空头词:{sentiment.get('negative_hits', 0)}, "
            f"主题:{', '.join(f'{k}×{v}' for k, v in sentiment.get('themes', [])) or '-'})"
        )
        render_posts(guba.get("posts", []), lines)
        errors = data.get("errors") or []
        if errors:
            lines.append("")
            lines.append("## 取得错误")
            for err in errors:
                lines.append(f"- {err}")
        lines.append("")

    lines.append("## Codex分析指示")
    market_instruction = (
        "结合大盘指数、行业/概念板块和涨跌家数，判断异动是大盘共振、板块共振还是个股独立催化。"
        if data.get("market_indexes") or data.get("board_ranks") or data.get("market_breadth")
        else "本次未采集市场背景时，共振判断请明确写“未采集大盘/板块背景，无法确认”。"
    )
    lines.append(
        "请只基于上面的公开材料，用中文分析这只A股的直近异动理由。"
        "优先级为：公告/业绩/监管等确认材料 > 股吧资讯帖和高阅读材料 > 普通股吧观点。"
        "股吧只做情绪面和未确认思惑，不当作事实。"
        f"{market_instruction}"
        "情绪周期按七段判断：冰点期、修复/潜伏期、启动期、加速期、高潮期、高位分歧/分化期、退潮期；"
        "同时区分情绪票和趋势票。"
        "输出顺序：1) 最有力理由 2) 补助理由 3) 共振判断 4) 情绪面/周期位置 5) 确定度 6) 注意点。"
        "材料弱时要明确写“未确认”“思惑”“低信息量”，不要编造催化。"
    )
    return "\n".join(lines).strip() + "\n"


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Collect public A-share evidence for Codex stock-move analysis.")
    parser.add_argument("stock", help="A-share code or symbol, e.g. 600519, sh600519, 300750")
    parser.add_argument("--hours", type=int, default=24, help="Recent evidence window in hours")
    parser.add_argument("--posts", type=int, default=100, help="Max Eastmoney guba/news posts to print")
    parser.add_argument("--announcements", type=int, default=10, help="Max announcements to print")
    parser.add_argument("--skip-market-context", action="store_true", help="Skip market indexes, boards, and breadth context")
    parser.add_argument("--format", choices=["markdown", "json", "prompt"], default="markdown")
    parser.add_argument("--output", default="", help="Write output to this path instead of stdout")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_arg_parser().parse_args(argv)
    try:
        data = collect_sources(args)
    except KeyboardInterrupt:
        return 130
    except Exception as exc:
        print(f"fatal: {exc}", file=sys.stderr)
        return 1
    if args.format == "json":
        output = json.dumps(data, ensure_ascii=False, indent=2)
    elif args.format == "prompt":
        output = render_markdown(data, prompt_only=True)
    else:
        output = render_markdown(data)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(output)
    else:
        print(output, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
