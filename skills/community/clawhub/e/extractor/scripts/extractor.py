#!/usr/bin/env python3
"""
extractor.py - 结构化字段提取器

支持从 HTML 页面或文件中提取结构化字段：
- CSS Selector 提取
- XPath 提取
- 正则表达式提取
- LLM 提取（TODO）

用法：
    python extractor.py --url "https://example.com" --css '{"title": "h1", "price": ".price"}'
    python extractor.py --file "page.html" --xpath '{"links": "//a/@href"}'
    python extractor.py --url "https://example.com" --regex '{"email": "[\\w.]+@[\\w.]+"}'
"""

import argparse
import json
import os
import re
import sys
import urllib.request
import urllib.error
from pathlib import Path
from typing import Optional

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 not installed. Run: pip install beautifulsoup4 lxml", file=sys.stderr)
    sys.exit(1)

try:
    from lxml import etree
except ImportError:
    print("Error: lxml not installed. Run: pip install lxml", file=sys.stderr)
    sys.exit(1)


class PageExtractor:
    """结构化字段提取器，支持 CSS/XPath/Regex 三种提取方式。"""

    def __init__(self, html: str, parser: str = "lxml"):
        """
        初始化提取器。

        Args:
            html: HTML 内容字符串
            parser: BeautifulSoup 解析器，默认 lxml
        """
        self.html = html
        self.soup = BeautifulSoup(html, parser)
        # 为 XPath 准备 lxml tree
        self._tree = None

    @property
    def tree(self):
        """延迟构建 lxml tree（仅在 XPath 查询时需要）。"""
        if self._tree is None:
            self._tree = etree.HTML(self.html)
        return self._tree

    # ── CSS Selector 提取 ──────────────────────────────────────────

    def extract_by_css(self, selectors: dict) -> dict:
        """
        使用 CSS 选择器提取字段。

        Args:
            selectors: {字段名: CSS选择器} 映射。
                       选择器可以是字符串（单个选择器）或 dict（含 selector/attr/text 等配置）。

        Returns:
            {字段名: 提取值} 映射。单元素返回字符串，多元素返回列表。

        Examples:
            >>> ext = PageExtractor("<h1>Hello</h1><p class='price'>¥99</p>")
            >>> ext.extract_by_css({"title": "h1", "price": "p.price"})
            {'title': 'Hello', 'price': '¥99'}
        """
        results = {}
        for field, config in selectors.items():
            selector, attr, get_all, get_text = self._parse_config(config)
            elements = self.soup.select(selector)

            if not elements:
                results[field] = None
                continue

            values = []
            for el in elements:
                if attr:
                    val = el.get(attr)
                elif get_text:
                    val = el.get_text(strip=True)
                else:
                    val = el.get_text(strip=True)

                if val is not None:
                    values.append(val)

            if get_all:
                results[field] = values if values else None
            else:
                results[field] = values[0] if values else None

        return results

    # ── XPath 提取 ─────────────────────────────────────────────────

    def extract_by_xpath(self, xpaths: dict) -> dict:
        """
        使用 XPath 表达式提取字段。

        Args:
            xpaths: {字段名: XPath表达式} 映射。
                    值可以是字符串（单个 XPath）或 dict（含 xpath/get_all 等配置）。

        Returns:
            {字段名: 提取值} 映射。

        Examples:
            >>> ext = PageExtractor("<ul><li>A</li><li>B</li></ul>")
            >>> ext.extract_by_xpath({"items": "//li/text()"})
            {'items': ['A', 'B']}
        """
        results = {}
        for field, config in xpaths.items():
            xpath, get_all = self._parse_xpath_config(config)

            try:
                raw_results = self.tree.xpath(xpath)
            except etree.XPathError as e:
                results[field] = None
                print(f"Warning: XPath error for '{field}': {e}", file=sys.stderr)
                continue

            # 转换结果为字符串列表
            values = []
            for r in raw_results:
                if isinstance(r, etree._Element):
                    text = r.text_content() if hasattr(r, 'text_content') else (r.text or "")
                    text = text.strip()
                    if text:
                        values.append(text)
                else:
                    val = str(r).strip()
                    if val:
                        values.append(val)

            if get_all:
                results[field] = values if values else None
            else:
                results[field] = values[0] if values else None

        return results

    # ── 正则表达式提取 ─────────────────────────────────────────────

    def extract_by_regex(self, patterns: dict, flags: int = 0) -> dict:
        """
        使用正则表达式提取字段。

        Args:
            patterns: {字段名: 正则表达式} 映射。
                      值可以是字符串（单个正则）或 dict（含 pattern/get_all 等配置）。
            flags: 全局正则标志（如 re.IGNORECASE），可被单个配置覆盖。

        Returns:
            {字段名: 提取值} 映射。

        Examples:
            >>> ext = PageExtractor("Contact: test@example.com, admin@site.org")
            >>> ext.extract_by_regex({"emails": r"[\\w.]+@[\\w.]+"})
            {'emails': ['test@example.com', 'admin@site.org']}
        """
        # 先用 BeautifulSoup 提取纯文本用于正则匹配
        text = self.soup.get_text(separator=" ", strip=True)
        results = {}

        for field, config in patterns.items():
            pattern, get_all, f = self._parse_regex_config(config, flags)

            try:
                if get_all:
                    matches = re.findall(pattern, text, f)
                    # 如果有分组，findall 返回元组列表
                    if matches and isinstance(matches[0], tuple):
                        matches = [m[0] if len(m) == 1 else m for m in matches]
                    results[field] = matches if matches else None
                else:
                    match = re.search(pattern, text, f)
                    if match:
                        groups = match.groups()
                        if groups:
                            results[field] = groups[0] if len(groups) == 1 else list(groups)
                        else:
                            results[field] = match.group(0)
                    else:
                        results[field] = None
            except re.error as e:
                results[field] = None
                print(f"Warning: Regex error for '{field}': {e}", file=sys.stderr)

        return results

    # ── LLM 提取 ─────────────────────────────────────────────────

    # 默认 prompt 模板
    DEFAULT_LLM_PROMPT = """你是一个信息提取助手。请从以下 HTML 内容中提取指定的字段。

要求提取的字段：{fields}

HTML 内容：
```html
{html_content}
```

请以 JSON 格式返回提取结果，格式为：
{{"字段名": "提取值", ...}}

如果某个字段在内容中不存在，值设为 null。
只返回 JSON，不要其他解释文字。"""

    def extract_by_llm(
        self,
        fields: list,
        prompt_template: Optional[str] = None,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        max_html_chars: int = 12000,
    ) -> dict:
        """
        使用 LLM 提取字段（自然语言描述）。

        支持 OpenAI 兼容 API（OpenAI / Ollama / vLLM / OpenClaw 网关等）。

        配置方式（优先级从高到低）：
        1. 方法参数直接传入
        2. 环境变量：OPENAI_BASE_URL / OPENAI_API_KEY / OPENAI_MODEL
        3. 默认：Ollama 本地 (http://localhost:11434, model=qwen2.5)

        Args:
            fields: 要提取的字段名列表，如 ["产品名称", "价格", "规格"]
            prompt_template: 自定义 prompt 模板（含 {fields} 和 {html_content} 占位符）
            base_url: LLM API 地址
            api_key: API Key（Ollama 不需要）
            model: 模型名称
            max_html_chars: HTML 最大字符数（防止超出 token 限制）

        Returns:
            {字段名: 提取值} 映射
        """
        # 确定 API 配置
        base_url = base_url or os.environ.get("OPENAI_BASE_URL", "http://localhost:11434/v1")
        api_key = api_key or os.environ.get("OPENAI_API_KEY", "ollama")  # Ollama 不需要真实 key
        model = model or os.environ.get("OPENAI_MODEL", "qwen2.5")

        # 准备 HTML 内容（截断防止超长）
        html_content = self.html
        if len(html_content) > max_html_chars:
            html_content = html_content[:max_html_chars] + "\n... (truncated)"

        # 构建 prompt
        template = prompt_template or self.DEFAULT_LLM_PROMPT
        prompt = template.format(
            fields=", ".join(fields),
            html_content=html_content,
        )

        # 调用 LLM API（OpenAI 兼容格式）
        url = f"{base_url.rstrip('/')}/chat/completions"
        payload = json.dumps({
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个信息提取助手，只返回 JSON 格式结果。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
            "max_tokens": 1024,
        }).encode("utf-8")

        headers = {
            "Content-Type": "application/json",
        }
        if api_key and api_key != "ollama":
            headers["Authorization"] = f"Bearer {api_key}"

        try:
            req = urllib.request.Request(url, data=payload, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=60) as resp:
                result = json.loads(resp.read().decode("utf-8"))

            # 解析响应
            content = result["choices"][0]["message"]["content"].strip()

            # 提取 JSON（处理 markdown code block 包裹的情况）
            if content.startswith("```"):
                # 移除 ```json ... ``` 包裹
                content = re.sub(r"^```(?:json)?\s*", "", content)
                content = re.sub(r"\s*```$", "", content)

            extracted = json.loads(content)

            # 确保返回的是 dict
            if not isinstance(extracted, dict):
                print(f"Warning: LLM returned non-dict result: {type(extracted)}", file=sys.stderr)
                return {f: None for f in fields}

            return extracted

        except urllib.error.URLError as e:
            raise ConnectionError(
                f"Failed to connect to LLM API at {base_url}: {e}\n"
                f"Please ensure:\n"
                f"  1. Ollama is running: ollama serve\n"
                f"  2. Or set OPENAI_BASE_URL and OPENAI_API_KEY environment variables\n"
                f"  3. Or pass base_url and api_key parameters directly"
            ) from e
        except (json.JSONDecodeError, KeyError) as e:
            raise ValueError(f"Failed to parse LLM response: {e}\nRaw response: {content[:500]}") from e

    # ── 批量提取 ───────────────────────────────────────────────────

    def extract_all(
        self,
        css: Optional[dict] = None,
        xpath: Optional[dict] = None,
        regex: Optional[dict] = None,
    ) -> dict:
        """
        批量提取：同时使用多种方式进行提取。

        Args:
            css: CSS 选择器配置
            xpath: XPath 配置
            regex: 正则表达式配置

        Returns:
            合并后的 {字段名: 值} 映射
        """
        results = {}

        if css:
            results.update(self.extract_by_css(css))
        if xpath:
            results.update(self.extract_by_xpath(xpath))
        if regex:
            results.update(self.extract_by_regex(regex))

        return results

    # ── 内部工具方法 ───────────────────────────────────────────────

    @staticmethod
    def _parse_config(config):
        """解析 CSS 配置项，支持字符串和 dict 两种格式。"""
        if isinstance(config, str):
            return config, None, False, True
        elif isinstance(config, dict):
            selector = config.get("selector", config.get("css", ""))
            attr = config.get("attr")  # 提取属性值（如 href, src）
            get_all = config.get("all", False)
            get_text = config.get("text", True)
            return selector, attr, get_all, get_text
        else:
            raise ValueError(f"Invalid config type: {type(config)}")

    @staticmethod
    def _parse_xpath_config(config):
        """解析 XPath 配置项。"""
        if isinstance(config, str):
            return config, True  # XPath 默认返回所有匹配
        elif isinstance(config, dict):
            xpath = config.get("xpath", "")
            get_all = config.get("all", True)
            return xpath, get_all
        else:
            raise ValueError(f"Invalid xpath config type: {type(config)}")

    @staticmethod
    def _parse_regex_config(config, default_flags=0):
        """解析正则配置项。"""
        if isinstance(config, str):
            return config, True, default_flags
        elif isinstance(config, dict):
            pattern = config.get("pattern", config.get("regex", ""))
            get_all = config.get("all", True)
            flags = default_flags
            if config.get("ignorecase"):
                flags |= re.IGNORECASE
            if config.get("multiline"):
                flags |= re.MULTILINE
            if config.get("dotall"):
                flags |= re.DOTALL
            return pattern, get_all, flags
        else:
            raise ValueError(f"Invalid regex config type: {type(config)}")


# ── HTML 加载工具 ──────────────────────────────────────────────────


def load_html_from_file(file_path: str) -> str:
    """从本地文件加载 HTML。"""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    return path.read_text(encoding="utf-8")


def load_html_from_url(url: str, timeout: int = 30000) -> str:
    """
    使用 Playwright 从 URL 加载页面 HTML。

    Args:
        url: 页面 URL
        timeout: 超时时间（毫秒）

    Returns:
        页面 HTML 字符串
    """
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        raise ImportError(
            "Playwright not installed. Run: pip install playwright && playwright install chromium"
        )

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page()
            page.goto(url, timeout=timeout, wait_until="domcontentloaded")
            html = page.content()
            return html
        finally:
            browser.close()


def load_html(source: str) -> str:
    """
    自动检测来源并加载 HTML。

    Args:
        source: URL 或文件路径

    Returns:
        HTML 字符串
    """
    if source.startswith(("http://", "https://")):
        return load_html_from_url(source)
    else:
        return load_html_from_file(source)


# ── CLI 入口 ───────────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="结构化字段提取器 - 从 HTML 页面提取结构化数据",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  # 从 URL 用 CSS 提取
  python extractor.py --url "https://example.com" --css '{"title": "h1", "desc": "p"}'

  # 从文件用 XPath 提取
  python extractor.py --file page.html --xpath '{"links": "//a/@href"}'

  # 用正则提取
  python extractor.py --file page.html --regex '{"emails": "[\\\\w.]+@[\\\\w.]+"}'

  # 混合提取
  python extractor.py --file page.html --css '{"title": "h1"}' --regex '{"phone": "1[3-9]\\\\d{9}"}'
        """,
    )

    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--url", help="页面 URL")
    source_group.add_argument("--file", help="本地 HTML 文件路径")

    parser.add_argument("--css", help="CSS 选择器（JSON 格式）", type=json.loads)
    parser.add_argument("--xpath", help="XPath 表达式（JSON 格式）", type=json.loads)
    parser.add_argument("--regex", help="正则表达式（JSON 格式）", type=json.loads)
    parser.add_argument("--pretty", action="store_true", help="格式化 JSON 输出")
    parser.add_argument("--output", "-o", help="输出文件路径（默认输出到 stdout）")

    args = parser.parse_args()

    if not any([args.css, args.xpath, args.regex]):
        parser.error("至少需要指定 --css, --xpath, 或 --regex 之一")

    # 加载 HTML
    try:
        if args.url:
            print(f"Loading from URL: {args.url}", file=sys.stderr)
            html = load_html_from_url(args.url)
        else:
            print(f"Loading from file: {args.file}", file=sys.stderr)
            html = load_html_from_file(args.file)
    except Exception as e:
        print(f"Error loading HTML: {e}", file=sys.stderr)
        sys.exit(1)

    # 提取
    extractor = PageExtractor(html)
    results = extractor.extract_all(css=args.css, xpath=args.xpath, regex=args.regex)

    # 输出
    indent = 2 if args.pretty else None
    output = json.dumps(results, ensure_ascii=False, indent=indent)

    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Results saved to: {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
