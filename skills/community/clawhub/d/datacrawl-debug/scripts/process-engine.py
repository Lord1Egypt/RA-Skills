#!/usr/bin/env python3
"""ProcessEngine — 数据处理配置生成 + 结果解析器"""

import argparse
import json
import re
import sys
from html.parser import HTMLParser


class HTMLDataExtractor(HTMLParser):
    """从HTML中提取结构化数据的轻量解析器"""

    def __init__(self):
        super().__init__()
        self.tag_stack = []
        self.current_attrs = {}
        self.extracted = {"texts": [], "links": [], "images": [], "tables": [], "lists": []}
        self._in_table = False
        self._in_row = False
        self._in_list = False
        self._current_table = []
        self._current_row = []
        self._current_list = []

    def handle_starttag(self, tag, attrs):
        attr_dict = dict(attrs)
        self.tag_stack.append(tag)
        self.current_attrs = attr_dict
        if tag == "a" and "href" in attr_dict:
            self.extracted["links"].append({"href": attr_dict["href"], "text": ""})
        elif tag == "img":
            self.extracted["images"].append({
                "src": attr_dict.get("src", ""),
                "alt": attr_dict.get("alt", ""),
            })
        elif tag == "table":
            self._in_table = True
            self._current_table = []
        elif tag == "tr" and self._in_table:
            self._in_row = True
            self._current_row = []
        elif tag in ("ul", "ol"):
            self._in_list = True
            self._current_list = []
        elif tag in ("td", "th") and self._in_row:
            pass

    def handle_endtag(self, tag):
        if self.tag_stack and self.tag_stack[-1] == tag:
            self.tag_stack.pop()
        if tag == "tr" and self._in_row:
            self._in_row = False
            if self._current_row:
                self._current_table.append(self._current_row)
        elif tag == "table" and self._in_table:
            self._in_table = False
            if self._current_table:
                self.extracted["tables"].append(self._current_table)
        elif tag in ("ul", "ol") and self._in_list:
            self._in_list = False
            if self._current_list:
                self.extracted["lists"].append(self._current_list)

    def handle_data(self, data):
        text = data.strip()
        if not text:
            return
        self.extracted["texts"].append(text)
        if self.tag_stack:
            last = self.tag_stack[-1]
            if last == "a" and self.extracted["links"]:
                self.extracted["links"][-1]["text"] = text
            elif last in ("td", "th") and self._in_row:
                self._current_row.append(text)
            elif last == "li" and self._in_list:
                self._current_list.append(text)


def extract_from_html(html_content: str, fields: list = None) -> dict:
    """从HTML内容提取结构化数据"""
    parser = HTMLDataExtractor()
    try:
        parser.feed(html_content)
    except Exception as e:
        return {"error": f"HTML解析失败: {str(e)}"}

    result = {
        "summary": {
            "text_fragments": len(parser.extracted["texts"]),
            "links": len(parser.extracted["links"]),
            "images": len(parser.extracted["images"]),
            "tables": len(parser.extracted["tables"]),
            "lists": len(parser.extracted["lists"]),
        },
        "data": parser.extracted,
    }

    # 如果指定了字段，尝试正则匹配
    if fields:
        field_results = {}
        for field in fields:
            patterns = [
                re.compile(rf'{field}["\s:]+([^"<,\n]+)', re.IGNORECASE),
                re.compile(rf'<[^>]*class="[^"]*{field}[^"]*"[^>]*>(.*?)</', re.IGNORECASE | re.DOTALL),
                re.compile(rf'{field}.*?:\s*(.+?)(?:\n|<|$)', re.IGNORECASE),
            ]
            found = []
            for p in patterns:
                matches = p.findall(html_content)
                found.extend([m.strip() for m in matches if m.strip()])
            field_results[field] = found[:20]  # 限制每字段最多20条
        result["field_extraction"] = field_results

    return result


def generate_process_config(url: str, fields: list, mode: str = "static",
                          frequency: str = "once", output_format: str = "json") -> dict:
    """生成数据处理配置方案"""
    # 识别站点类型
    site_type = "unknown"
    if "amazon" in url.lower():
        site_type = "ecommerce"
    elif "linkedin" in url.lower():
        site_type = "social_professional"
    elif "alibaba" in url.lower():
        site_type = "b2b_marketplace"
    elif "twitter" in url.lower() or "x.com" in url.lower():
        site_type = "social_media"
    elif "news" in url.lower() or "blog" in url.lower():
        site_type = "content"
    elif "gov" in url.lower():
        site_type = "government"
    elif "github" in url.lower():
        site_type = "developer"

    # 根据模式推荐工具
    tool_recommendations = {
        "static": ["requests + BeautifulSoup", "lxml", "httpx"],
        "dynamic": ["Playwright", "Selenium", "Puppeteer"],
        "api": ["requests", "httpx", "aiohttp"],
    }

    # 生成选择器建议
    selector_suggestions = {}
    for field in fields:
        selector_suggestions[field] = {
            "css_candidates": [f"[class*='{field}']", f"[id*='{field}']", f"[data-field='{field}']"],
            "xpath_candidates": [f"//*[contains(@class,'{field}')]", f"//*[contains(text(),'{field}')]"],
            "regex_hint": f"{field}[\\s:]+([^\\n<]+)",
        }

    config = {
        "url": url,
        "site_type": site_type,
        "mode": mode,
        "fields": fields,
        "frequency": frequency,
        "output_format": output_format,
        "recommended_tools": tool_recommendations.get(mode, tool_recommendations["static"]),
        "selector_suggestions": selector_suggestions,
        "anti_detection": {
            "user_agent_rotation": True,
            "request_delay_range": [1, 3],
            "respect_robots_txt": True,
            "max_concurrent": 2,
        },
        "compliance_notes": [
            "请遵守目标网站robots.txt",
            "控制请求频率避免对服务器造成压力",
            "仅采集公开数据，不尝试绕过登录/付费墙",
            "注意数据使用需符合当地法律法规",
        ],
    }
    return config


def main():
    parser = argparse.ArgumentParser(description="ProcessEngine - 数据处理配置生成与结果解析")
    sub = parser.add_subparsers(dest="command")

    p_extract = sub.add_parser("extract", help="从HTML内容提取结构化数据")
    p_extract.add_argument("--html", type=str, required=True, help="HTML内容或文件路径")
    p_extract.add_argument("--fields", type=str, nargs="*", help="要提取的字段名列表")

    p_config = sub.add_parser("config", help="生成数据处理配置方案")
    p_config.add_argument("--url", type=str, required=True, help="目标URL")
    p_config.add_argument("--fields", type=str, nargs="+", required=True, help="处理字段列表")
    p_config.add_argument("--mode", type=str, default="static", choices=["static", "dynamic", "api"])
    p_config.add_argument("--frequency", type=str, default="once", choices=["once", "hourly", "daily", "weekly"])
    p_config.add_argument("--format", type=str, default="json", choices=["json", "csv", "both"])

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(1)

    result = {}
    if args.command == "extract":
        html_content = args.html
        if args.html.endswith(".html") or args.html.endswith(".htm"):
            try:
                with open(args.html, "r", encoding="utf-8") as f:
                    html_content = f.read()
            except Exception as e:
                result = {"error": f"文件读取失败: {str(e)}"}
                print(json.dumps(result, ensure_ascii=False, indent=2))
                return
        result = extract_from_html(html_content, args.fields)
    elif args.command == "config":
        result = generate_process_config(args.url, args.fields, args.mode, args.frequency, args.format)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
