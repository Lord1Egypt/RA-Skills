#!/usr/bin/env python
"""Query chinadrugtrials.org.cn through browser automation.

The site uses anti-bot scripts and list rows with JavaScript detail links.
This script follows the fast path documented in SKILL.md:
homepage search -> result table -> constructed official detail URLs.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

from playwright.sync_api import sync_playwright


BASE_URL = "https://www.chinadrugtrials.org.cn"
DEFAULT_UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def normalize_keyword(raw: str) -> str:
    if "\\u" in raw:
        try:
            return raw.encode("utf-8").decode("unicode_escape")
        except UnicodeDecodeError:
            return raw
    return raw


def field_after_label(text: str, label: str) -> str:
    for line in text.replace("\u00a0", " ").splitlines():
        cells = [cell.strip() for cell in line.split("\t") if cell.strip()]
        for index, cell in enumerate(cells):
            if cell == label and index + 1 < len(cells):
                return cells[index + 1]

    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for index, line in enumerate(lines):
        if line == label and index + 1 < len(lines):
            return lines[index + 1]

    match = re.search(re.escape(label) + r"\s*[：:]?\s*([^\n\t]+)", text)
    return match.group(1).strip() if match else ""


def parse_count(text: str) -> str:
    match = re.search(r"当前第\s*\d+\s*页，共\s*\d+\s*页，共\s*(\d+)\s*条记录", text)
    return match.group(1) if match else ""


def markdown_table(rows: list[dict[str, Any]], count: str) -> str:
    header = "| 序号 | 登记号 | 试验状态 | 药物名称 | 适应症 | 试验通俗题目 | 公司 | 首次公示日期 | 链接 |"
    sep = "|---:|---|---|---|---|---|---|---|---|"
    lines = []
    if count:
        lines.append(f"官网查询结果：共 {count} 条记录。")
        lines.append("")
    lines.extend([header, sep])
    for row in rows:
        link = f"[详情]({row['link']})"
        lines.append(
            "| {seq} | {reg} | {status} | {drug} | {indication} | {title} | "
            "{company} | {date} | {link} |".format(
                seq=row.get("seq", ""),
                reg=row.get("reg", ""),
                status=row.get("status", ""),
                drug=row.get("drug", ""),
                indication=row.get("indication", ""),
                title=row.get("title", ""),
                company=row.get("company") or "未核实",
                date=row.get("date") or "未核实",
                link=link,
            )
        )
    return "\n".join(lines)


def query(keyword: str, browser_path: str | None, delay_ms: int) -> dict[str, Any]:
    with sync_playwright() as playwright:
        executable_path = browser_path or playwright.chromium.executable_path
        browser = playwright.chromium.launch(
            headless=True,
            executable_path=executable_path,
            args=["--disable-blink-features=AutomationControlled"],
        )
        context = browser.new_context(user_agent=DEFAULT_UA)
        page = context.new_page()
        page.goto(BASE_URL + "/", wait_until="commit", timeout=60000)
        page.wait_for_selector('input[name="keywords"]', timeout=30000)
        page.locator('input[name="keywords"]').fill(keyword)
        page.locator('button[type="submit"]').click(timeout=10000)
        page.wait_for_url("**/clinicaltrials.searchlist.dhtml", wait_until="commit", timeout=60000)
        page.wait_for_timeout(delay_ms)

        body = page.locator("body").inner_text(timeout=10000).replace("\u00a0", " ")
        rows = page.evaluate(
            """() => Array.from(document.querySelectorAll('table tr')).map(tr => {
              const tds = Array.from(tr.querySelectorAll('td')).map(td => td.innerText.trim().replace(/\u00a0/g, ' '));
              const a = tr.querySelector('a[onclick*=getDetail]');
              return tds.length >= 6 ? {
                seq: tds[0], reg: tds[1], status: tds[2], drug: tds[3],
                indication: tds[4], title: tds[5], id: a && a.id, idx: a && a.name
              } : null;
            }).filter(Boolean)"""
        )

        results: list[dict[str, Any]] = []
        for row in rows:
            link = f"{BASE_URL}/clinicaltrials.searchlistdetail.dhtml?id={row['id']}&ckm_index={row['idx']}"
            detail = context.new_page()
            detail.goto(link, wait_until="commit", timeout=60000)
            detail.wait_for_timeout(max(1500, min(delay_ms, 3000)))
            text = detail.locator("body").inner_text(timeout=10000).replace("\u00a0", " ")
            row["company"] = field_after_label(text, "申请人名称")
            row["date"] = field_after_label(text, "首次公示信息日期")
            row["link"] = link
            results.append(row)
            detail.close()

        browser.close()
        return {"keyword": keyword, "count": parse_count(body), "rows": results}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("keyword", help="Search keyword. Backslash-u escapes are accepted.")
    parser.add_argument("--browser-path", help="Explicit Chromium/Chrome executable path.")
    parser.add_argument("--delay-ms", type=int, default=5000)
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    args = parser.parse_args()

    sys.stdout.reconfigure(encoding="utf-8")
    data = query(normalize_keyword(args.keyword), args.browser_path, args.delay_ms)
    if args.format == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
    else:
        print(markdown_table(data["rows"], data["count"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
