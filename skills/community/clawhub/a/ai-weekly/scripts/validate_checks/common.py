# validate_checks/common.py — 通用/共享检查 + helpers
import re
from pathlib import Path

def _detect_format(html_content: str) -> str:
    if 'news-card' in html_content or 'NEWS_DATA' in html_content or 'news-grid' in html_content:
        return 'v3'
    if 'kpi-section' in html_content or 'kpi-grid' in html_content:
        return 'v2'
    return 'v3'  # 默认按 v3 检查


def check_file_exists(html_path: Path) -> dict:
    if not html_path.exists():
        return {"ok": False, "msg": f"文件不存在：{html_path}"}
    size = html_path.stat().st_size
    if size < 1024:
        return {"ok": False, "msg": f"文件过小（{size} bytes），可能不完整"}
    return {"ok": True, "msg": f"文件存在，{size//1024} KB"}


def check_data_sources(html_content: str) -> dict:
    """
    检查数据来源，从文件末尾搜索"数据来源"/"来源"/"Sources"字样。
    """
    pattern = re.compile(r'数据来源|数据说明|新闻数据来自', re.IGNORECASE)
    last_match = None
    for m in pattern.finditer(html_content):
        last_match = m

    if not last_match:
        return {"ok": False, "msg": "未找到数据来源说明"}

    start = last_match.start()
    file_len = len(html_content)

    # 如果匹配在文件前 70%，尝试从尾部找
    if start < file_len * 0.6:
        tail = html_content[int(file_len * 0.6):]
        tail_match = pattern.search(tail)
        if tail_match:
            start = int(file_len * 0.6) + tail_match.start()

    source_section = html_content[start:start + 800]
    urls = re.findall(r'https?://[^\s<>"\'()]+', source_section)

    if len(urls) >= 2:
        return {"ok": True, "msg": f"数据来源已填写，含 {len(urls)} 个链接"}
    elif len(urls) >= 1:
        return {"ok": True, "msg": f"数据来源已填写，含 {len(urls)} 个链接"}
    return {"ok": False, "msg": "数据来源可能不完整（未找到 URL 链接）"}


def _extract_js_var(name: str, html_content: str):
    """从 HTML 抽取 const NAME = [...] / {...} 字面量（支持嵌套括号）。失败返回 None。"""
    m = re.search(r'const %s\s*=\s*([\[{])' % re.escape(name), html_content)
    if not m:
        return None
    start = m.start(1)
    opener = html_content[start]
    closer = "}" if opener == "{" else "]"
    depth = 0
    i = start
    n = len(html_content)
    while i < n:
        ch = html_content[i]
        if ch in "[{":
            depth += 1
        elif ch in "]}":
            depth -= 1
            if depth == 0 and ch == closer:
                return html_content[start:i + 1]
        i += 1
    return None
