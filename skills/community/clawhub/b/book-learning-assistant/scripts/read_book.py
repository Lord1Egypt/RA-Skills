#!/usr/bin/env python3
"""
EPUB / PDF 电子书章节读取工具
返回清理后的纯文本，供 AI 直接用。

核心策略：搜全部 HTML 文件 → 按文本长度排序 → 最长者 = 章节正文
（目录页文字极少，绝不可能是最长匹配）

用法（CLI）：
  python3 read_book.py <书路径> [章节关键词] [--limit 8000]
  python3 read_book.py <书路径> --list        # 列出所有章节标题

返回 JSON：
  {"file": "text/part0007.html", "chars": 15234, "text": "..."}
"""

import sys
import os
import json
import re
import html as html_lib
import zipfile
import io


# ── 工具函数 ──────────────────────────────────────────────────

def _clean_html(raw: str) -> str:
    """去除 HTML 标签，保留纯文本（保留段落间隔）"""
    # 把块级标签换成换行
    step = re.sub(r'</(p|div|h[1-6]|li|blockquote|tr)>', '\n', raw, flags=re.IGNORECASE)
    step = re.sub(r'<(br|hr|tr)[^>]*/?>', '\n', step, flags=re.IGNORECASE)
    # 去掉所有标签
    step = re.sub(r'<[^>]+>', ' ', step)
    # HTML 实体解码
    step = html_lib.unescape(step)
    # 合并多余空白，但保留换行
    step = re.sub(r'[ \t]+', ' ', step)
    step = re.sub(r'\n{3,}', '\n\n', step)
    return step.strip()


def _read_file(z, fpath: str) -> str:
    """从 zip 中读取文件，尝试 UTF-8，失败则用 lax 模式"""
    raw = z.read(fpath)
    for enc in ('utf-8', 'utf-8-sig', 'gbk', 'latin-1'):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    return raw.decode('utf-8', errors='ignore')


# ── EPUB 核心 ────────────────────────────────────────────────

def _find_chapter_in_epub(epub_path: str, keyword: str):
    """
    在 EPUB 内搜索包含 keyword 的章节正文。
    评分策略：关键词密度 = keyword 出现次数 / 文件字符数
    （正文章节密度高，索引/目录页密度极低）
    """
    matches = []  # (file_path, text_length, keyword_count, raw_html)

    with zipfile.ZipFile(epub_path, 'r') as z:
        html_files = [f for f in z.namelist()
                      if f.endswith(('.html', '.xhtml', '.htm'))]

        print(f"[search] 共 {len(html_files)} 个 HTML 文件，搜索关键词：「{keyword}」",
              file=sys.stderr)

        for f in html_files:
            try:
                content = _read_file(z, f)
                if keyword not in content:
                    continue
                text_len = len(re.sub(r'<[^>]+>', ' ', content))
                # [关键] 排除太短的文件（< 2000 字 = 目录/索引页）
                if text_len < 2000:
                    print(f"[skip]   {f}  →  仅 {text_len} 字（疑似目录页，跳过）",
                          file=sys.stderr)
                    continue
                # 计算关键词出现次数
                kw_count = content.count(keyword)
                # 关键词密度评分（每千字出现次数）
                density = kw_count * 1000 / max(text_len, 1)
                matches.append((f, text_len, kw_count, density, content))
                print(f"[match]  {f}  →  {text_len} 字，关键词出现 {kw_count} 次，密度 {density:.1f}",
                      file=sys.stderr)
            except Exception as e:
                print(f"[error]  {f}: {e}", file=sys.stderr)
                continue

    if not matches:
        return None, None

    # 按「关键词密度」降序排列，密度最高者 = 章节正文
    matches.sort(key=lambda x: x[3], reverse=True)
    best = matches[0]
    print(f"[best]   选择 {best[0]}（{best[1]} 字，密度 {best[3]:.1f}，共 {len(matches)} 个匹配）",
          file=sys.stderr)
    return best[0], best[4]


def _list_chapters(epub_path: str) -> list:
    """
    列出 EPUB 的章节目录。
    优先解析 toc.ncx；失败则扫描 HTML 中的 <h1>/<title> 标签。
    """
    chapters = []

    with zipfile.ZipFile(epub_path, 'r') as z:
        # 策略1：解析 toc.ncx
        for f in z.namelist():
            if f.endswith('toc.ncx'):
                try:
                    raw = _read_file(z, f)
                    # 提取所有 <navLabel><text>...</text>
                    texts = re.findall(r'<navLabel>\s*<text>(.*?)</text>', raw)
                    hrefs = re.findall(r'<content src="([^"]+)"', raw)
                    for i, t in enumerate(texts):
                        href = hrefs[i] if i < len(hrefs) else ''
                        chapters.append({'title': t.strip(), 'href': href})
                    if chapters:
                        return chapters
                except Exception as e:
                    print(f"[toc.ncx] 解析失败：{e}", file=sys.stderr)

        # 策略2：扫描 HTML 文件的 <title>/<h1>
        for f in z.namelist():
            if not f.endswith(('.html', '.xhtml')):
                continue
            try:
                content = _read_file(z, f)
                titles = re.findall(r'<title>(.*?)</title>', content)
                h1s = re.findall(r'<h1[^>]*>(.*?)</h1>', content, re.DOTALL)
                if titles or h1s:
                    t = titles[0].strip() if titles else h1s[0][:50].strip()
                    chapters.append({'title': t, 'file': f})
            except Exception:
                pass

    return chapters


def read_epub(epub_path: str, chapter_keyword: str, limit: int = 8000) -> dict:
    """读取 EPUB 章节，返回 dict"""
    rel_path, raw_html = _find_chapter_in_epub(epub_path, chapter_keyword)
    if raw_html is None:
        return {'error': f'未找到包含关键词「{chapter_keyword}」的章节',
                'epub': epub_path}

    text = _clean_html(raw_html)
    total = len(text)
    snippet = text[:limit] + (
        f'\n\n...（共 {total} 字符，已截断）' if total > limit else '')
    return {'file': rel_path,
            'chars': total,
            'text': snippet,
            'epub': epub_path}


# ── PDF 读取（备用）────────────────────────────────────

def read_pdf(pdf_path: str, chapter_keyword: str = '', limit: int = 8000) -> dict:
    try:
        from pypdf import PdfReader
    except ImportError:
        return {'error': 'pypdf 未安装，请运行 pip install pypdf'}

    reader = PdfReader(pdf_path)
    full_text = ''
    for i, page in enumerate(reader.pages):
        full_text += (page.extract_text() or '')
        full_text += f'\n--- 第{i + 1}页 ---\n'

    if chapter_keyword:
        idx = full_text.find(chapter_keyword)
        if idx == -1:
            return {'error': f'PDF 中未找到关键词「{chapter_keyword}」'}
        start = max(0, idx - 3000)
        end = min(len(full_text), idx + limit)
        snippet = full_text[start:end]
    else:
        snippet = full_text[:limit]

    return {'file': pdf_path,
            'chars': len(full_text),
            'text': snippet + ('...（已截断）' if len(full_text) > limit else ''),
            'pdf': pdf_path}


# ── CLI 入口 ─────────────────────────────────────────────────

def main():
    # 强制 UTF-8 输出（Windows 兼容）
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

    if len(sys.argv) < 2:
        print(json.dumps(
            {'error': '用法: python3 read_book.py <书路径> [章节关键词|--list] [--limit N]'},
            ensure_ascii=False))
        sys.exit(1)

    book_path = sys.argv[1]

    # --list 模式：列出所有章节
    if '--list' in sys.argv:
        if not os.path.exists(book_path):
            print(json.dumps({'error': f'文件不存在：{book_path}'}, ensure_ascii=False))
            sys.exit(1)
        chapters = _list_chapters(book_path)
        print(json.dumps({'chapters': chapters, 'count': len(chapters)},
                         ensure_ascii=False, indent=2))
        return

    # 正常模式：读取章节
    if len(sys.argv) < 3:
        print(json.dumps(
            {'error': '请提供章节关键词，或用 --list 列出所有章节'},
            ensure_ascii=False))
        sys.exit(1)

    keyword = sys.argv[2]
    limit = 8000
    if '--limit' in sys.argv:
        try:
            limit = int(sys.argv[sys.argv.index('--limit') + 1])
        except Exception:
            pass

    if not os.path.exists(book_path):
        print(json.dumps({'error': f'文件不存在：{book_path}'}, ensure_ascii=False))
        sys.exit(1)

    print(f"[read_book] 读取：{book_path}", file=sys.stderr)
    print(f"[read_book] 关键词：{keyword}", file=sys.stderr)
    print(f"[read_book] 限制：{limit} 字符", file=sys.stderr)

    if book_path.lower().endswith('.epub'):
        result = read_epub(book_path, keyword, limit=limit)
    elif book_path.lower().endswith('.pdf'):
        result = read_pdf(book_path, keyword, limit=limit)
    else:
        print(json.dumps({'error': f'不支持的文件格式，仅支持 .epub / .pdf'},
                         ensure_ascii=False))
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
