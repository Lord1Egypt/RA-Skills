#!/usr/bin/env python3
"""web_fetch — 网页抓取与文本提取（纯标准库，无 LLM 依赖）"""
import sys, os, json, re, urllib.request, urllib.error, urllib.parse
from html.parser import HTMLParser
sys.path.insert(0, os.path.dirname(__file__))
from common import *


class TextExtractor(HTMLParser):
    """从 HTML 中提取纯文本"""
    BLOCK_TAGS = {"p", "div", "br", "h1", "h2", "h3", "h4", "h5", "h6",
                  "li", "tr", "td", "th", "blockquote", "pre", "hr", "section",
                  "article", "header", "footer", "nav", "main", "aside"}

    def __init__(self):
        super().__init__()
        self._text = []
        self._skip = False
        self._in_script = False
        self._in_style = False

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag in ("script", "style", "noscript"):
            self._skip = True
            if tag == "script":
                self._in_script = True
            elif tag == "style":
                self._in_style = True
        if tag in self.BLOCK_TAGS:
            self._text.append("\n")
        if tag == "br":
            self._text.append("\n")
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6"):
            self._text.append("\n")

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag in ("script", "style", "noscript"):
            self._skip = False
            self._in_script = False
            self._in_style = False
        if tag in self.BLOCK_TAGS:
            self._text.append("\n")

    def handle_data(self, data):
        if not self._skip:
            text = data.strip()
            if text:
                self._text.append(text)

    def get_text(self):
        raw = "".join(self._text)
        # 清理多余空行
        lines = [l.strip() for l in raw.splitlines() if l.strip()]
        return "\n".join(lines)


class TitleExtractor(HTMLParser):
    """提取 <title> 标签内容"""
    def __init__(self):
        super().__init__()
        self.title = ""
        self._in_title = False

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self._in_title = True

    def handle_data(self, data):
        if self._in_title:
            self.title += data

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self._in_title = False


def fetch_url(url, timeout=30):
    """抓取 URL 内容"""
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; builtin-tools/1.0)",
            "Accept": "text/html,application/xhtml+xml,*/*",
        },
    )
    try:
        resp = urllib.request.urlopen(req, timeout=timeout)
        content_type = resp.headers.get("Content-Type", "")
        return resp.read(), resp.status, content_type, None
    except urllib.error.HTTPError as e:
        return None, e.code, None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, 0, None, f"URL 错误: {e.reason}"
    except Exception as e:
        return None, 0, None, str(e)


def html_to_text(html_bytes):
    """HTML 字节转纯文本"""
    # 检测编码
    content = None
    for enc in ("utf-8", "gbk", "gb2312", "latin-1"):
        try:
            content = html_bytes.decode(enc)
            break
        except (UnicodeDecodeError, LookupError):
            continue
    if content is None:
        content = html_bytes.decode("utf-8", errors="replace")

    # 提取标题
    te = TitleExtractor()
    try:
        te.feed(content)
    except Exception:
        pass

    # 提取文本
    ex = TextExtractor()
    try:
        ex.feed(content)
    except Exception:
        pass

    return ex.get_text(), te.title.strip()


def extract_section(text, section_name):
    """从文本中提取特定章节"""
    patterns = [
        rf"(?:##\s*{re.escape(section_name)}[^\n]*\n)(.*?)(?=\n##\s|\Z)",
        rf"(?:#{1,3}\s*{re.escape(section_name)}[^\n]*\n)(.*?)(?=\n#{1,3}\s|\Z)",
    ]
    for pattern in patterns:
        m = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if m:
            return m.group(1).strip()
    return None


def text_to_simple_markdown(text, title=""):
    """将纯文本转为简单 Markdown"""
    lines = text.splitlines()
    result = []
    if title:
        result.append(f"# {title}")
        result.append("")

    for line in lines:
        stripped = line.strip()
        if not stripped:
            result.append("")
        else:
            result.append(stripped)

    return "\n".join(result)


def main():
    params = parse_input()
    url = get_param(params, "url", required=True)
    extract = get_param(params, "extract")
    max_length = get_param(params, "max_length", 50000)
    timeout = get_param(params, "timeout", 30)
    as_markdown = get_param(params, "as_markdown", True)

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    # 抓取
    raw_bytes, status, content_type, error = fetch_url(url, timeout)
    if error:
        output_error(f"抓取失败: {error}", EXIT_EXEC_ERROR)

    # 检查是否是 HTML
    is_html = content_type and "text/html" in content_type.lower()
    if not is_html and raw_bytes:
        # 非 HTML，直接返回原始内容
        try:
            text = raw_bytes.decode("utf-8", errors="replace")
        except Exception:
            text = str(raw_bytes)
        output_ok({
            "url": url,
            "status": status,
            "type": "raw",
            "content": text[:max_length],
            "size": len(raw_bytes),
        })
        return

    if not raw_bytes:
        output_error("响应为空", EXIT_EXEC_ERROR)

    # HTML → 纯文本
    text, title = html_to_text(raw_bytes)

    # 提取特定章节
    result_text = text
    if extract:
        section = extract_section(text, extract)
        if section:
            result_text = section
        # 也尝试全文搜索关键词
        if not section and extract.lower() in text.lower():
            idx = text.lower().index(extract.lower())
            start = max(0, idx - 200)
            end = min(len(text), idx + len(extract) + 2000)
            result_text = text[start:end]

    # 截断
    truncated = len(result_text) > max_length
    result_text = result_text[:max_length]

    # 格式化输出
    if as_markdown:
        content = text_to_simple_markdown(result_text, title)
    else:
        content = result_text

    output_ok({
        "url": url,
        "title": title,
        "status": status,
        "type": "html",
        "content": content,
        "text_length": len(text),
        "truncated": truncated,
    })


if __name__ == "__main__":
    main()
