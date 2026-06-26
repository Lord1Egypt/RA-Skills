#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import re
import sys
from datetime import datetime
from html import unescape
from pathlib import Path
from urllib.error import URLError, HTTPError
from urllib.request import Request, urlopen

BOC_URL = "https://www.boc.cn/sourcedb/whpj/"
DEFAULT_HISTORY = Path(__file__).resolve().parents[1] / "data" / "boc_fx_history.csv"
THRESH_GBP = 0.50
THRESH_HKD = 0.20
THRESH_JPY = 0.05
ROW_KEYS = {
    "英镑": "GBP",
    "港币": "HKD",
    "日元": "JPY",
}
FIELDNAMES = [
    "captured_at",
    "page_publish_time",
    "gbp_spot_sell",
    "hkd_spot_buy",
    "jpy_spot_sell",
]


def fetch_html(url: str) -> str:
    req = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0 Safari/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
        },
    )
    with urlopen(req, timeout=20) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, errors="replace")


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def parse_rows(html: str) -> list[list[str]]:
    rows = []
    for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", html, flags=re.I | re.S):
        cells = re.findall(r"<(?:td|th)[^>]*>(.*?)</(?:td|th)>", tr, flags=re.I | re.S)
        cleaned = [strip_tags(c) for c in cells]
        if cleaned:
            rows.append(cleaned)
    return rows


def parse_snapshot(html: str) -> dict[str, str]:
    rows = parse_rows(html)
    found: dict[str, dict[str, str]] = {}

    for row in rows:
        if len(row) < 8:
            continue
        currency = row[0]
        if currency not in ROW_KEYS:
            continue
        found[ROW_KEYS[currency]] = {
            "spot_buy": row[1],
            "spot_sell": row[3],
            "publish_time": row[7],
        }

    missing = [name for name in ("GBP", "HKD", "JPY") if name not in found]
    if missing:
        raise ValueError(f"页面解析失败，缺少币种: {', '.join(missing)}")

    publish_time = found["GBP"]["publish_time"] or found["HKD"]["publish_time"] or found["JPY"]["publish_time"]
    return {
        "captured_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "page_publish_time": publish_time,
        "gbp_spot_sell": normalize_num(found["GBP"]["spot_sell"]),
        "hkd_spot_buy": normalize_num(found["HKD"]["spot_buy"]),
        "jpy_spot_sell": normalize_num(found["JPY"]["spot_sell"]),
    }


def normalize_num(text: str) -> str:
    match = re.search(r"-?\d+(?:\.\d+)?", text.replace(",", ""))
    if not match:
        raise ValueError(f"数值解析失败: {text!r}")
    return f"{float(match.group(0)):.2f}"


def load_history(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def append_history(path: Path, snapshot: dict[str, str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    exists = path.exists()
    with path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if not exists:
            writer.writeheader()
        writer.writerow(snapshot)


def same_snapshot(latest: dict[str, str] | None, current: dict[str, str]) -> bool:
    if not latest:
        return False
    return all(latest.get(k, "") == current.get(k, "") for k in ("page_publish_time", "gbp_spot_sell", "hkd_spot_buy", "jpy_spot_sell"))


def emit(status: str, **pairs: str) -> None:
    print(f"STATUS={status}")
    for k, v in pairs.items():
        print(f"{k}={v}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Check Bank of China FX changes and emit key=value output.")
    parser.add_argument("--history", default=str(DEFAULT_HISTORY), help="CSV path for historical snapshots")
    parser.add_argument("--url", default=BOC_URL, help="Bank of China FX page URL")
    args = parser.parse_args()

    history_path = Path(args.history).expanduser()

    try:
        html = fetch_html(args.url)
        current = parse_snapshot(html)
        rows = load_history(history_path)
    except (HTTPError, URLError) as e:
        emit("ERROR", MESSAGE=f"抓取中国银行汇率页面失败: {e}")
        return 0
    except Exception as e:
        emit("ERROR", MESSAGE=str(e))
        return 0

    latest = rows[-1] if rows else None
    if not same_snapshot(latest, current):
        append_history(history_path, current)
        rows.append(current)

    if len(rows) < 2:
        emit(
            "NO_ALERT",
            MESSAGE="历史记录不足，已写入当前快照",
            PAGE_TIME=current["page_publish_time"],
            GBP_CURR=current["gbp_spot_sell"],
            HKD_CURR=current["hkd_spot_buy"],
            JPY_CURR=current["jpy_spot_sell"],
        )
        return 0

    prev = rows[-2]
    curr = rows[-1]
    prev_gbp = float(prev["gbp_spot_sell"])
    curr_gbp = float(curr["gbp_spot_sell"])
    prev_hkd = float(prev["hkd_spot_buy"])
    curr_hkd = float(curr["hkd_spot_buy"])
    prev_jpy = float(prev["jpy_spot_sell"])
    curr_jpy = float(curr["jpy_spot_sell"])

    gbp_drop = prev_gbp - curr_gbp
    hkd_rise = curr_hkd - prev_hkd
    jpy_drop = prev_jpy - curr_jpy

    alerts = []
    if gbp_drop >= THRESH_GBP:
        alerts.append(f"英镑现汇卖出价下跌 {gbp_drop:.2f}（{prev_gbp:.2f} → {curr_gbp:.2f}）")
    if hkd_rise >= THRESH_HKD:
        alerts.append(f"港币现汇买入价上涨 {hkd_rise:.2f}（{prev_hkd:.2f} → {curr_hkd:.2f}）")
    if jpy_drop >= THRESH_JPY:
        alerts.append(f"日元现汇卖出价下跌 {jpy_drop:.2f}（{prev_jpy:.2f} → {curr_jpy:.2f}）")

    emit(
        "ALERT" if alerts else "NO_ALERT",
        PAGE_TIME=curr["page_publish_time"],
        GBP_PREV=f"{prev_gbp:.2f}",
        GBP_CURR=f"{curr_gbp:.2f}",
        HKD_PREV=f"{prev_hkd:.2f}",
        HKD_CURR=f"{curr_hkd:.2f}",
        JPY_PREV=f"{prev_jpy:.2f}",
        JPY_CURR=f"{curr_jpy:.2f}",
        GBP_DROP=f"{gbp_drop:.2f}",
        HKD_RISE=f"{hkd_rise:.2f}",
        JPY_DROP=f"{jpy_drop:.2f}",
        MESSAGE="；".join(alerts) if alerts else "未达到告警阈值",
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
