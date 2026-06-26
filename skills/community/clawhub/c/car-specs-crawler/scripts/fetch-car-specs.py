#!/usr/bin/env python3
"""
Car Specs Crawler - Fetch vehicle specifications from Chinese auto websites.
Supports 懂车帝 (dongchedi.com) and 汽车之家 (autohome.com.cn).
"""

import argparse
import json
import re
import sys
import time
from urllib.parse import quote_plus, urljoin

try:
    import requests
    from lxml import html
except ImportError:
    print("ERROR: requests and lxml are required. Install: pip install requests lxml", file=sys.stderr)
    sys.exit(1)

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
HEADERS = {"User-Agent": USER_AGENT}


def clean_text(text):
    """Remove extra whitespace and normalize text."""
    if not text:
        return ""
    return " ".join(str(text).split())


def search_dongchedi(car_name):
    """Search 懂车帝 for the car model page."""
    query = quote_plus(car_name)
    search_url = f"https://www.dongchedi.com/search?keyword={query}"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        doc = html.fromstring(r.content)
        # Find first car detail link
        links = doc.xpath('//a[contains(@href, "/auto/series/")]/@href')
        if links:
            return urljoin("https://www.dongchedi.com", links[0])
        links = doc.xpath('//a[contains(@href, "/auto/")]/@href')
        if links:
            return urljoin("https://www.dongchedi.com", links[0])
    except Exception as e:
        print(f"懂车帝搜索失败: {e}", file=sys.stderr)
    return None


def search_autohome(car_name):
    """Search 汽车之家 for the car model page."""
    query = quote_plus(car_name)
    search_url = f"https://car.autohome.com.cn/price/search-0-0-0-0-0-0-0-0-0-0-0-0-0-0-0-1.html?keyword={query}"
    try:
        r = requests.get(search_url, headers=HEADERS, timeout=15)
        r.raise_for_status()
        doc = html.fromstring(r.content)
        links = doc.xpath('//div[@class="interval-slide"]//a/@href')
        if links:
            return urljoin("https://car.autohome.com.cn", links[0])
        links = doc.xpath('//dl[@class="search-pic"]//a/@href')
        if links:
            return urljoin("https://car.autohome.com.cn", links[0])
    except Exception as e:
        print(f"汽车之家搜索失败: {e}", file=sys.stderr)
    return None


def parse_dongchedi_spec(url):
    """Parse car specs from 懂车帝 detail page."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        doc = html.fromstring(r.content)

        specs = {}

        # Look for spec tables or parameter lists
        spec_rows = doc.xpath('//div[contains(@class, "spec-item")]')
        if not spec_rows:
            spec_rows = doc.xpath('//tr[contains(@class, "spec")]')
        if not spec_rows:
            spec_rows = doc.xpath('//div[contains(@class, "parameter")]')

        field_patterns = {
            "价格": ["指导价", "售价", "价格", "厂商指导价", "官方售价"],
            "能源类型": ["能源类型", "动力类型", "燃料形式", "能源"],
            "车身尺寸": ["车身尺寸", "长*宽*高", "长x宽x高", "外形尺寸", "长×宽×高"],
            "轴距": ["轴距"],
            "最高车速": ["最高车速", "最高时速", "最高速度"],
            "电池容量": ["电池容量", "电池能量", "电池电量"],
            "续航": ["CLTC", "NEDC", "WLTP", "续航里程", "纯电续航", "续航"],
            "座位": ["座位数", "座椅布局", "座位布局", "座椅数"],
            "电机功率": ["电动机总功率", "电机功率", "最大功率", "总功率"],
            "扭矩": ["最大扭矩", "扭矩", "总扭矩"],
            "百公里加速": ["百公里加速", "0-100", "加速时间", "0-100km/h"],
            "充电时间": ["快充时间", "慢充时间", "充电时间"],
        }

        for row in spec_rows:
            label = None
            value = None

            label_xpaths = [
                './/div[contains(@class, "name")]/text()',
                './/td[1]//text()',
                './/span[contains(@class, "label")]/text()',
                './/dt/text()',
                './/div[contains(@class, "title")]/text()',
            ]
            value_xpaths = [
                './/div[contains(@class, "value")]/text()',
                './/td[2]//text()',
                './/span[contains(@class, "value")]/text()',
                './/dd/text()',
                './/div[contains(@class, "content")]/text()',
            ]

            for lx in label_xpaths:
                labels = row.xpath(lx)
                if labels:
                    label = clean_text(labels[0])
                    break

            for vx in value_xpaths:
                values = row.xpath(vx)
                if values:
                    value = clean_text(values[0])
                    break

            if label and value:
                mapped = False
                for std_name, patterns in field_patterns.items():
                    for pat in patterns:
                        if pat in label:
                            specs[std_name] = value
                            mapped = True
                            break
                    if mapped:
                        break
                if not mapped:
                    specs[label] = value

        # Extract title for car name
        if not specs.get("车型名称"):
            title = doc.xpath('//title/text()')
            if title:
                t = clean_text(title[0])
                specs["车型名称"] = t.split("_")[0].split("-")[0].split("|")[0].strip()

        return specs

    except Exception as e:
        print(f"解析懂车帝页面失败: {e}", file=sys.stderr)
        return {}


def parse_autohome_spec(url):
    """Parse car specs from 汽车之家 spec page."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()
        doc = html.fromstring(r.content)

        specs = {}

        # Try spec list structure
        spec_groups = doc.xpath('//div[@class="spec-list"]')
        if not spec_groups:
            rows = doc.xpath('//div[@class="spec-box"]//tr')
            for row in rows:
                th = row.xpath('.//th/text()')
                td = row.xpath('.//td//text()')
                if th and td:
                    label = clean_text(th[0])
                    value = clean_text(" ".join(td))
                    specs[label] = value

        # Get price
        price_elem = doc.xpath('//span[@class="price"]/text()')
        if price_elem and not specs.get("价格"):
            specs["价格"] = clean_text(price_elem[0])

        if not specs.get("车型名称"):
            title = doc.xpath('//title/text()')
            if title:
                t = clean_text(title[0])
                specs["车型名称"] = t.split("_")[0].split("-")[0].split("|")[0].strip()

        return specs

    except Exception as e:
        print(f"解析汽车之家页面失败: {e}", file=sys.stderr)
        return {}


def fetch_car_info(car_name, sources=None):
    """Main function to fetch car info from multiple sources."""
    if sources is None:
        sources = ["dongchedi", "autohome"]

    results = {
        "查询车型": car_name,
        "来源": {},
        "合并结果": {}
    }

    for source in sources:
        if source == "dongchedi":
            url = search_dongchedi(car_name)
            if url:
                specs = parse_dongchedi_spec(url)
                results["来源"]["懂车帝"] = {"url": url, "参数": specs}
        elif source == "autohome":
            url = search_autohome(car_name)
            if url:
                specs = parse_autohome_spec(url)
                results["来源"]["汽车之家"] = {"url": url, "参数": specs}

    # Merge results
    merged = {}
    for source_name, source_data in results["来源"].items():
        for key, value in source_data["参数"].items():
            if key not in merged or not merged[key]:
                merged[key] = value
    results["合并结果"] = merged

    return results


def output_as_table(results_list):
    """Output results as markdown table."""
    if not results_list:
        print("未找到任何车型信息")
        return None

    all_keys = set()
    for r in results_list:
        all_keys.update(r["合并结果"].keys())

    priority = [
        "车型名称", "价格", "能源类型", "座位", "车身尺寸", "轴距",
        "最高车速", "电池容量", "续航", "电机功率", "扭矩",
        "百公里加速", "充电时间"
    ]

    ordered_keys = [k for k in priority if k in all_keys]
    ordered_keys += sorted([k for k in all_keys if k not in priority])

    car_names = [r["查询车型"] for r in results_list]
    header = "| 参数 | " + " | ".join(car_names) + " |"
    separator = "|------|" + "|".join(["------"] * len(car_names)) + "|"

    lines = [header, separator]
    for key in ordered_keys:
        row = f"| {key} |"
        for r in results_list:
            value = r["合并结果"].get(key, "-")
            row += f" {value} |"
        lines.append(row)

    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Fetch car specs from Chinese auto websites")
    parser.add_argument("cars", nargs="+", help="Car model names to search")
    parser.add_argument("--source", "-s", choices=["dongchedi", "autohome", "all"],
                        default="all", help="Data source")
    parser.add_argument("--format", "-f", choices=["json", "table"],
                        default="table", help="Output format")
    parser.add_argument("--output", "-o", help="Output file path")

    args = parser.parse_args()

    if args.source == "all":
        sources = ["dongchedi", "autohome"]
    else:
        sources = [args.source]

    all_results = []
    for car in args.cars:
        print(f"正在查询: {car} ...", file=sys.stderr)
        result = fetch_car_info(car, sources=sources)
        all_results.append(result)
        time.sleep(0.5)

    if args.format == "json":
        output = json.dumps(all_results, ensure_ascii=False, indent=2)
        print(output)
    elif args.format == "table":
        table = output_as_table(all_results)
        if table:
            print(table)

    if args.output and args.format == "json":
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(json.dumps(all_results, ensure_ascii=False, indent=2))
        print(f"\n结果已保存到: {args.output}", file=sys.stderr)


if __name__ == "__main__":
    main()
