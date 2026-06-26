#!/usr/bin/env python3
"""
将 Markdown 文件转换为 PDF，嵌入本地图片，正确渲染中文。

使用 PyMuPDF (pymupdf) 的 TextWriter + Font 对象实现中文渲染。

用法:
    python md_to_pdf.py <article.md路径> [--output <输出PDF路径>]

示例:
    python md_to_pdf.py cursor-third-era/article.md
    python md_to_pdf.py cursor-third-era/article.md --output cursor-third-era/article.pdf
"""

import argparse
import os
import re
import sys

try:
    import pymupdf
except ImportError:
    print("错误：需要安装 pymupdf 库")
    print("运行: pip3 install pymupdf")
    sys.exit(1)


# 页面配置
PAGE_WIDTH = 595.28   # A4 宽度 (pt)
PAGE_HEIGHT = 841.89  # A4 高度 (pt)
MARGIN_LEFT = 56.69   # 20mm
MARGIN_RIGHT = 56.69
MARGIN_TOP = 56.69
MARGIN_BOTTOM = 56.69
CONTENT_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT

# 字体大小
FONT_SIZE_H1 = 20
FONT_SIZE_H2 = 16
FONT_SIZE_H3 = 14
FONT_SIZE_BODY = 11
FONT_SIZE_CAPTION = 9
FONT_SIZE_BLOCKQUOTE = 10

LINE_HEIGHT_FACTOR = 1.6


def parse_markdown(md_text: str) -> list:
    """解析 Markdown 为结构化块列表。"""
    blocks = []
    lines = md_text.split('\n')
    i = 0

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            blocks.append({'type': 'blank'})
            i += 1
            continue

        if re.match(r'^-{3,}$|^\*{3,}$|^_{3,}$', stripped):
            blocks.append({'type': 'hr'})
            i += 1
            continue

        h_match = re.match(r'^(#{1,3})\s+(.*)', stripped)
        if h_match:
            level = len(h_match.group(1))
            text = h_match.group(2).strip()
            # 处理 "### #\n实际标题文字" 被拆行的情况
            if text == '#' or not text:
                # 下一行可能是标题的实际文字
                if i + 1 < len(lines) and lines[i + 1].strip() and not lines[i + 1].strip().startswith('#'):
                    next_text = lines[i + 1].strip()
                    if next_text and not re.match(r'^!\[', next_text) and not re.match(r'^>\s', next_text):
                        blocks.append({'type': f'h{level}', 'text': next_text})
                        i += 2
                        continue
                # 单独的 "### #" 且下一行不是标题文字，跳过
                i += 1
                continue
            blocks.append({'type': f'h{level}', 'text': text})
            i += 1
            continue

        img_match = re.match(r'^!\[([^\]]*)\]\(([^)]+)\)', stripped)
        if img_match:
            blocks.append({'type': 'image', 'alt': img_match.group(1), 'src': img_match.group(2)})
            i += 1
            continue

        if stripped.startswith('*') and stripped.endswith('*') and not stripped.startswith('**'):
            blocks.append({'type': 'caption', 'text': stripped.strip('*')})
            i += 1
            continue

        if stripped.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].strip().startswith('>'):
                quote_lines.append(lines[i].strip().lstrip('>').strip())
                i += 1
            blocks.append({'type': 'blockquote', 'text': ' '.join(quote_lines)})
            continue

        ol_match = re.match(r'^(\d+)\.\s+(.*)', stripped)
        if ol_match:
            blocks.append({'type': 'list_item', 'number': ol_match.group(1), 'text': ol_match.group(2)})
            i += 1
            continue

        if stripped.startswith('- ') or stripped.startswith('* '):
            blocks.append({'type': 'list_item', 'number': '•', 'text': stripped[2:]})
            i += 1
            continue

        # 导航链接行跳过
        if re.match(r'^\[.+\]\(.+\)\s*/\s*\[.+\]\(.+\)', stripped):
            i += 1
            continue

        # 普通段落
        para_lines = [stripped]
        i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].strip().startswith('#') \
                and not lines[i].strip().startswith('![') and not lines[i].strip().startswith('>') \
                and not re.match(r'^-{3,}$', lines[i].strip()) \
                and not re.match(r'^\d+\.\s+', lines[i].strip()):
            para_lines.append(lines[i].strip())
            i += 1
        blocks.append({'type': 'paragraph', 'text': ' '.join(para_lines)})

    return blocks


def clean_text(text: str) -> str:
    """清理 Markdown 行内格式。"""
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'\*\*(.+?)\*\*', r'\1', text)
    text = re.sub(r'\*(.+?)\*', r'\1', text)
    text = re.sub(r'`(.+?)`', r'\1', text)
    return text


def get_image_path(src: str, md_dir: str):
    """解析图片路径。"""
    if src.startswith(('http://', 'https://')):
        return None
    abs_path = os.path.normpath(os.path.join(md_dir, src))
    return abs_path if os.path.isfile(abs_path) else None


class PdfWriter:
    """PDF 写入器，处理分页和中文字体。"""

    def __init__(self):
        self.doc = pymupdf.open()
        self.font = pymupdf.Font("china-s")  # 内置简体中文字体
        self.font_bold = pymupdf.Font("china-ss")  # 内置简体中文粗体
        self.page = None
        self.y = MARGIN_TOP
        self._new_page()

    def _new_page(self):
        self.page = self.doc.new_page(width=PAGE_WIDTH, height=PAGE_HEIGHT)
        self.y = MARGIN_TOP

    def _ensure_space(self, needed: float):
        """确保页面剩余空间足够，不够则换页。"""
        if self.y + needed > PAGE_HEIGHT - MARGIN_BOTTOM:
            self._new_page()

    def _text_width(self, text: str, font, fontsize: float) -> float:
        """计算文本宽度。"""
        return font.text_length(text, fontsize=fontsize)

    def _wrap_text(self, text: str, font, fontsize: float, max_width: float) -> list:
        """将文本按宽度限制分行。"""
        lines = []
        current = ""
        for ch in text:
            test = current + ch
            if self._text_width(test, font, fontsize) > max_width and current:
                lines.append(current)
                current = ch
            else:
                current = test
        if current:
            lines.append(current)
        return lines if lines else [""]

    def write_text(self, text: str, fontsize: float, bold: bool = False,
                   indent: float = 0, color: tuple = (0, 0, 0),
                   max_width: float = None) -> float:
        """写入文本，自动换行和分页。返回结束 y 坐标。"""
        font = self.font_bold if bold else self.font
        if max_width is None:
            max_width = CONTENT_WIDTH - indent
        x = MARGIN_LEFT + indent
        line_height = fontsize * LINE_HEIGHT_FACTOR

        wrapped = self._wrap_text(text, font, fontsize, max_width)

        for line_text in wrapped:
            self._ensure_space(line_height)
            tw = pymupdf.TextWriter(self.page.rect)
            tw.append(pymupdf.Point(x, self.y + fontsize), line_text, font=font, fontsize=fontsize)
            tw.write_text(self.page, color=color)
            self.y += line_height

        return self.y

    def draw_hr(self):
        """绘制水平分割线。"""
        self._ensure_space(15)
        self.y += 5
        self.page.draw_line(
            pymupdf.Point(MARGIN_LEFT, self.y),
            pymupdf.Point(PAGE_WIDTH - MARGIN_RIGHT, self.y),
            color=(0.7, 0.7, 0.7), width=0.5
        )
        self.y += 10

    def draw_blockquote_bar(self, start_y: float, end_y: float):
        """绘制引用条。"""
        self.page.draw_line(
            pymupdf.Point(MARGIN_LEFT + 5, start_y),
            pymupdf.Point(MARGIN_LEFT + 5, end_y),
            color=(0.6, 0.6, 0.6), width=2
        )

    def insert_image(self, img_path: str):
        """插入图片，自动处理缩放和分页。"""
        try:
            pix = pymupdf.Pixmap(img_path)
            img_w = pix.width
            img_h = pix.height
            pix = None

            max_h = PAGE_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM - 30
            scale = min(CONTENT_WIDTH / img_w, max_h / img_h, 1.0)
            display_w = img_w * scale
            display_h = img_h * scale

            remaining = PAGE_HEIGHT - MARGIN_BOTTOM - self.y
            if remaining < min(display_h, 100):
                self._new_page()

            x_offset = MARGIN_LEFT + (CONTENT_WIDTH - display_w) / 2
            rect = pymupdf.Rect(x_offset, self.y, x_offset + display_w, self.y + display_h)
            self.page.insert_image(rect, filename=img_path)
            self.y += display_h + 8
        except Exception as e:
            print(f"  ⚠️  插入图片失败 ({os.path.basename(img_path)}): {e}")
            # 回退：尝试直接用文件名插入
            try:
                img_rect = pymupdf.Rect(MARGIN_LEFT, self.y, PAGE_WIDTH - MARGIN_RIGHT, self.y + 200)
                self.page.insert_image(img_rect, filename=img_path)
                self.y += 208
            except Exception:
                pass

    def add_blank(self, height: float = None):
        if height is None:
            height = FONT_SIZE_BODY * 0.5
        self.y += height
        if self.y > PAGE_HEIGHT - MARGIN_BOTTOM:
            self._new_page()

    def save(self, output_path: str):
        self.doc.save(output_path)
        self.doc.close()
        size_kb = os.path.getsize(output_path) / 1024
        print(f"✅ PDF 已生成: {output_path} ({size_kb:.0f}KB)")


def md_to_pdf(md_path: str, output_path: str = None) -> str:
    """将 Markdown 文件转换为 PDF。"""
    if not os.path.isfile(md_path):
        raise FileNotFoundError(f"文件不存在: {md_path}")

    md_dir = os.path.dirname(os.path.abspath(md_path))
    if output_path is None:
        output_path = os.path.splitext(md_path)[0] + '.pdf'

    with open(md_path, 'r', encoding='utf-8') as f:
        md_text = f.read()

    blocks = parse_markdown(md_text)
    writer = PdfWriter()
    seen_title = False

    # 检查 blocks 中是否有有效的 h1 标题
    has_h1 = any(b['type'] == 'h1' and b.get('text', '').strip() for b in blocks)

    # 如果没有 h1 标题，尝试从 article_meta.json 获取
    fallback_title = None
    if not has_h1:
        meta_path = os.path.join(md_dir, 'article_meta.json')
        if os.path.isfile(meta_path):
            try:
                import json
                with open(meta_path, 'r', encoding='utf-8') as f:
                    meta = json.load(f)
                fallback_title = meta.get('title', '').strip()
                if fallback_title:
                    print(f"  ℹ️  MD 中无有效标题，从 article_meta.json 补充: {fallback_title}")
            except Exception:
                pass

    # 如果需要补充标题，在开头插入 h1 块
    if fallback_title:
        blocks.insert(0, {'type': 'h1', 'text': fallback_title})

    for block in blocks:
        btype = block['type']

        if btype == 'blank':
            writer.add_blank()
            continue

        if btype == 'hr':
            writer.draw_hr()
            continue

        if btype in ('h1', 'h2', 'h3'):
            text = clean_text(block['text'])
            sizes = {'h1': FONT_SIZE_H1, 'h2': FONT_SIZE_H2, 'h3': FONT_SIZE_H3}
            fsize = sizes[btype]

            if btype == 'h1':
                if seen_title:
                    continue
                seen_title = True

            writer.add_blank(fsize * 0.5)
            writer._ensure_space(fsize * 2)
            writer.write_text(text, fsize, bold=True)
            writer.add_blank(fsize * 0.3)
            continue

        if btype == 'paragraph':
            text = clean_text(block['text'])
            if not text.strip():
                continue
            writer._ensure_space(FONT_SIZE_BODY * 2)
            writer.write_text(text, FONT_SIZE_BODY)
            writer.add_blank(FONT_SIZE_BODY * 0.4)
            continue

        if btype == 'blockquote':
            text = clean_text(block['text'])
            if not text.strip():
                continue
            writer._ensure_space(FONT_SIZE_BLOCKQUOTE * 2)
            start_y = writer.y
            writer.write_text(text, FONT_SIZE_BLOCKQUOTE, indent=15, color=(0.3, 0.3, 0.3))
            writer.draw_blockquote_bar(start_y, writer.y)
            writer.add_blank(FONT_SIZE_BLOCKQUOTE * 0.4)
            continue

        if btype == 'list_item':
            text = clean_text(block['text'])
            number = block.get('number', '•')
            prefix = f"{number}. " if number != '•' else "• "
            writer._ensure_space(FONT_SIZE_BODY * 2)

            indent = writer._text_width(prefix, writer.font, FONT_SIZE_BODY) + 4
            # 写前缀
            tw = pymupdf.TextWriter(writer.page.rect)
            tw.append(pymupdf.Point(MARGIN_LEFT, writer.y + FONT_SIZE_BODY),
                      prefix, font=writer.font, fontsize=FONT_SIZE_BODY)
            tw.write_text(writer.page, color=(0, 0, 0))
            # 写正文（带缩进）
            writer.write_text(text, FONT_SIZE_BODY, indent=indent)
            writer.add_blank(FONT_SIZE_BODY * 0.3)
            continue

        if btype == 'image':
            img_path = get_image_path(block['src'], md_dir)
            if img_path:
                writer.insert_image(img_path)
            continue

        if btype == 'caption':
            text = clean_text(block['text'])
            writer._ensure_space(FONT_SIZE_CAPTION * 2)
            writer.write_text(text, FONT_SIZE_CAPTION, color=(0.4, 0.4, 0.4))
            writer.add_blank(FONT_SIZE_CAPTION * 0.4)
            continue

    writer.save(output_path)
    return output_path


def main():
    parser = argparse.ArgumentParser(description='将 Markdown 文件转换为 PDF（嵌入本地图片）')
    parser.add_argument('md_path', help='Markdown 文件路径')
    parser.add_argument('--output', '-o', help='输出 PDF 路径（默认同目录同名 .pdf）')
    args = parser.parse_args()

    try:
        output = md_to_pdf(args.md_path, args.output)
        print(f"🎉 完成: {output}")
    except Exception as e:
        print(f"❌ 转换失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
