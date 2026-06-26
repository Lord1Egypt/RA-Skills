#!/usr/bin/env python3
"""CodeGenerator — 数据处理代码自动生成器"""

import argparse
import json
import sys


TEMPLATES = {
    "requests_bs4": '''"""Auto-generated processor: {name}"""
import requests
from bs4 import BeautifulSoup
import json
import time
import random

class {class_name}:
    def __init__(self):
        self.base_url = "{url}"
        self.headers = {{
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }}
        self.results = []
        self.fields = {fields}

    def fetch_page(self, url):
        """获取页面内容"""
        try:
            resp = requests.get(url, headers=self.headers, timeout=15)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            print(f"请求失败: {{e}}")
            return None

    def parse_item(self, soup):
        """解析单条数据 - 请根据实际页面结构调整选择器"""
        item = {{}}
        {field_parsers}
        return item

    def process(self, max_pages=1):
        """执行数据处理"""
        for page in range(1, max_pages + 1):
            url = self.base_url if page == 1 else f"{{self.base_url}}?page={{page}}"
            html = self.fetch_page(url)
            if not html:
                continue
            soup = BeautifulSoup(html, "html.parser")
            items = soup.select("{item_selector}")
            for el in items:
                parsed = self.parse_item(el)
                if parsed:
                    self.results.append(parsed)
            delay = random.uniform(1, 3)
            print(f"第{{page}}页完成, 等待{{delay:.1f}}s...")
            time.sleep(delay)
        return self.results

    def save(self, filename="{output_file}"):
        """保存结果"""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"已保存{{len(self.results)}}条到{{filename}}")


if __name__ == "__main__":
    processor = {class_name}()
    results = processor.process(max_pages=5)
    processor.save()
''',

    "playwright": '''"""Auto-generated dynamic processor: {name}"""
from playwright.sync_api import sync_playwright
import json
import time
import random

class {class_name}:
    def __init__(self):
        self.base_url = "{url}"
        self.results = []
        self.fields = {fields}

    def parse_item(self, page, selector="{item_selector}"):
        """解析列表项"""
        items = page.query_selector_all(selector)
        parsed_list = []
        for item in items:
            data = {{}}
            {field_parsers}
            parsed_list.append(data)
        return parsed_list

    def process(self, max_pages=1):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            for pg in range(1, max_pages + 1):
                url = self.base_url if pg == 1 else f"{{self.base_url}}?page={{pg}}"
                page.goto(url, wait_until="networkidle")
                time.sleep(random.uniform(1, 2))
                items = self.parse_item(page)
                self.results.extend(items)
                # 翻页
                next_btn = page.query_selector("a.next, li.next a, [aria-label='Next']")
                if next_btn and pg < max_pages:
                    next_btn.click()
                    time.sleep(2)
            browser.close()
        return self.results

    def save(self, filename="{output_file}"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"已保存{{len(self.results)}}条到{{filename}}")


if __name__ == "__main__":
    processor = {class_name}()
    results = processor.process(max_pages=5)
    processor.save()
''',

    "api_client": '''"""Auto-generated API client: {name}"""
import requests
import json
import time

class {class_name}:
    def __init__(self):
        self.base_url = "{url}"
        self.headers = {{
            "Content-Type": "application/json",
            "User-Agent": "DataProcessBot/1.0"
        }}
        self.results = []
        self.fields = {fields}

    def fetch_data(self, params=None, page=1):
        """请求数据接口"""
        if params is None:
            params = {{}}
        params["page"] = page
        try:
            resp = requests.get(self.base_url, headers=self.headers, params=params, timeout=15)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"请求失败: {{e}}")
            return None

    def parse_response(self, data):
        """解析API响应 - 请根据实际接口结构调整"""
        if not data:
            return []
        items = data.get("data", data.get("results", data.get("items", [])))
        parsed = []
        for item in items:
            record = {{}}
            {field_parsers}
            parsed.append(record)
        return parsed

    def process(self, max_pages=5):
        for page in range(1, max_pages + 1):
            data = self.fetch_data(page=page)
            if not data:
                break
            items = self.parse_response(data)
            if not items:
                break
            self.results.extend(items)
            time.sleep(1)
        return self.results

    def save(self, filename="{output_file}"):
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.results, f, ensure_ascii=False, indent=2)
        print(f"已保存{{len(self.results)}}条到{{filename}}")


if __name__ == "__main__":
    client = {class_name}()
    results = client.process()
    client.save()
''',
}


def _make_class_name(name: str) -> str:
    """生成类名"""
    parts = name.replace("-", " ").replace("_", " ").split()
    return "".join(p.capitalize() for p in parts) + "Processor"


def _make_field_parsers(fields: list, mode: str = "requests_bs4") -> str:
    """生成字段解析代码"""
    lines = []
    for f in fields:
        safe_name = f.replace(" ", "_").replace("-", "_").lower()
        if mode == "requests_bs4":
            lines.append(f'        data["{safe_name}"] = el.get_text(strip=True) if hasattr(el, "get_text") else ""')
            lines.append(f'        # TODO: 调整选择器 — soup.select_one(".{safe_name}") 或 el.select_one(".{safe_name}")')
        elif mode == "playwright":
            lines.append(f'        sub_el = item.query_selector(".{safe_name}")')
            lines.append(f'        data["{safe_name}"] = sub_el.inner_text().strip() if sub_el else ""')
        elif mode == "api_client":
            lines.append(f'        record["{safe_name}"] = item.get("{safe_name}", "")')
    return "\n".join(lines)


def generate_code(name: str, url: str, fields: list, mode: str = "requests_bs4",
                  item_selector: str = ".item", output_format: str = "json") -> dict:
    """生成数据处理代码"""
    if mode not in TEMPLATES:
        return {"error": f"不支持的模式: {mode}，可选: {list(TEMPLATES.keys())}"}

    class_name = _make_class_name(name)
    field_parsers = _make_field_parsers(fields, mode)
    output_file = f"{name}_output.{output_format}"

    code = TEMPLATES[mode].format(
        name=name,
        class_name=class_name,
        url=url,
        fields=fields,
        field_parsers=field_parsers,
        item_selector=item_selector,
        output_file=output_file,
    )

    dependencies = {
        "requests_bs4": ["requests", "beautifulsoup4", "lxml"],
        "playwright": ["playwright"],
        "api_client": ["requests"],
    }

    return {
        "name": name,
        "mode": mode,
        "class_name": class_name,
        "url": url,
        "fields": fields,
        "generated_code": code,
        "code_lines": len(code.split("\n")),
        "dependencies": dependencies.get(mode, []),
        "install_command": f"pip install {' '.join(dependencies.get(mode, []))}",
        "usage": f"python {name}_processor.py",
        "next_steps": [
            "1. 安装依赖: " + f"pip install {' '.join(dependencies.get(mode, []))}",
            "2. 根据实际页面调整选择器(item_selector和字段选择器)",
            "3. 运行: python " + f"{name}_processor.py",
            "4. 检查输出文件: " + output_file,
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="CodeGenerator - 数据处理代码自动生成")
    parser.add_argument("--name", type=str, required=True, help="项目名称")
    parser.add_argument("--url", type=str, required=True, help="目标URL")
    parser.add_argument("--fields", type=str, nargs="+", required=True, help="处理字段列表")
    parser.add_argument("--mode", type=str, default="requests_bs4",
                        choices=["requests_bs4", "playwright", "api_client"], help="处理模式")
    parser.add_argument("--selector", type=str, default=".item", help="列表项CSS选择器")
    parser.add_argument("--format", type=str, default="json", choices=["json", "csv"])

    args = parser.parse_args()
    result = generate_code(args.name, args.url, args.fields, args.mode, args.selector, args.format)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
