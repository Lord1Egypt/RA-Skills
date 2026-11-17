#!/usr/bin/env python3
"""
Generate a supplementary image (flashcard style) — auto-height.
Used as a visual supplement to Feishu card messages — NOT for standalone push.

Design: BIG fonts, MINIMAL content. Like a physical flashcard.
  - Title: huge (36-56px auto-sized)
  - Quote: large (28-32px)
  - Terms: large (22-26px)
  - NO core idea, NO explanation, NO links — just the essentials
  - Width fixed at 800px (rasterized at dpi=150 → 1250px wide); height auto-adapts to content (no fixed aspect ratio)
  - Card-style design with borders, section dividers, tag/badge elements

Usage:
  python gen_image.py --payload <payload.json> [--zh <zh.json>] --out <output.png> [--format <1:1|1:4|auto>] [--language <zh|en>]

Image generation: HTML → weasyprint PDF → pdf2image PNG → crop whitespace
Design inspired by react-paper-memo (github.com/JustinChia/react-paper-memo) large-font card concept.

NOTE: No emoji/special symbols in HTML output — weasyprint cannot render them.
NOTE: After generation, the script auto-verifies the PNG is valid and non-empty.
"""
import json, sys, os, argparse, datetime, re, html as html_mod
from weasyprint import HTML
from normalize_quotes import normalize_all

def esc(s):
    return html_mod.escape(s or '', quote=False)

def esc_attr(s):
    return html_mod.escape(s or '', quote=False)

def estimate_title_size(topic, fmt='auto'):
    """Auto-size title: shorter = bigger. Min 36px."""
    length = len(topic)
    base = 56 if fmt == '1:1' else 48
    if length <= 6:
        return base
    elif length <= 10:
        return base - 8
    elif length <= 16:
        return base - 16
    else:
        return max(36, base - 24)

def build_html(payload, zh, date_str, language='en', fmt='auto'):
    idx = payload.get('cardIndex', '?')
    total = payload.get('totalCards', '?')
    topic = esc(payload.get('topic', ''))
    chapter = esc(payload.get('chapter', ''))
    bilingual = language == 'en' and zh
    topic_zh = (zh or {}).get('topicZh', '')
    main_title = esc(topic_zh) if (bilingual and topic_zh) else topic
    en_subtitle = topic if (bilingual and topic_zh) else ''

    page_w = '800px'

    if fmt == '1:1':
        page_h = '800px'
        padding = '24px'
    elif fmt == '1:4':
        page_h = '3200px'
        padding = '32px'
    else:
        page_h = '4000px'
        padding = '32px'

    title_size = estimate_title_size(main_title, fmt)

    sections = []

    # Terms section with card-style design
    terms_zh = (zh or {}).get('terminologyZh', {})
    if bilingual and terms_zh:
        term_items = ''
        for en, cn in list(terms_zh.items())[:5]:
            term_items += f'''<div class="term-card">
                <span class="term-en">{esc(en)}</span>
                <span class="term-arrow">→</span>
                <span class="term-cn">{esc(cn)}</span>
            </div>'''
        sections.append(f'''<div class="section">
            <div class="section-header">
                <span class="section-tag tag-red">术语</span>
                <div class="section-line"></div>
            </div>
            <div class="term-list">{term_items}</div>
        </div>''')

    # Quote section with card-style design
    quote_zh = (zh or {}).get('quoteZh', '') if bilingual else payload.get('quote', '')
    if quote_zh:
        sections.append(f'''<div class="section">
            <div class="section-header">
                <span class="section-tag tag-purple">金句</span>
                <div class="section-line"></div>
            </div>
            <div class="quote-card">{esc(quote_zh)}</div>
        </div>''')

    # image
    img_html = ''
    if payload.get('image'):
        img_html = '<div class="img-wrap"><img src="%s"></div>' % esc_attr(payload['image'])

    body = ''.join(sections)

    # font sizes
    quote_fs = '32px' if fmt == '1:4' else '28px'
    term_fs = '26px' if fmt == '1:4' else '24px'
    sec_tag_fs = '20px' if fmt == '1:4' else '18px'

    html_str = f'''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">
<style>
@page {{ size: {page_w} {page_h}; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{
    font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Hiragino Sans GB",
                 "Noto Sans CJK SC", "SimSun", "宋体", sans-serif;
    color: #1f2328;
    width: {page_w};
    background: #eef2f7;
}}
/* Outer card frame */
.card {{
    background: #fff;
    margin: 0;
    display: flex;
    flex-direction: column;
    border-left: 6px solid #0969da;
    border-right: 1px solid #e1e4e8;
    border-bottom: 1px solid #e1e4e8;
    min-height: 400px;
}}
/* Header — gradient blue with progress bar */
.card-head {{
    background: linear-gradient(135deg, #1cb0f6, #0969da);
    color: #fff;
    padding: {padding};
    text-align: center;
    position: relative;
    border-bottom: 4px solid #1a7f37;
}}
.card-head .progress {{
    font-size: 18px;
    opacity: .85;
    margin-bottom: 12px;
    display: inline-block;
    background: rgba(255,255,255,.18);
    padding: 4px 16px;
    border-radius: 99px;
}}
.card-head .topic {{
    font-size: {title_size}px;
    font-weight: 900;
    line-height: 1.2;
    word-break: keep-all;
    text-shadow: 0 2px 4px rgba(0,0,0,.1);
}}
.card-head .topic-en {{
    font-size: 20px;
    font-weight: 500;
    margin-top: 8px;
    opacity: .8;
    font-style: italic;
}}
.card-head .chapter-badge {{
    display: inline-block;
    font-size: 14px;
    background: rgba(255,255,255,.25);
    padding: 3px 14px;
    border-radius: 99px;
    margin-top: 12px;
    font-weight: 600;
}}
/* Card body */
.card-body {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    padding: {padding};
    gap: 20px;
}}
/* Section with tag header */
.section {{
    margin-bottom: 8px;
}}
.section-header {{
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}}
.section-tag {{
    font-size: {sec_tag_fs};
    font-weight: 800;
    padding: 4px 14px;
    border-radius: 6px;
    color: #fff;
    white-space: nowrap;
    letter-spacing: 1px;
}}
.tag-red {{ background: #cf222e; }}
.tag-purple {{ background: #8250df; }}
.tag-green {{ background: #1a7f37; }}
.tag-blue {{ background: #0969da; }}
.tag-orange {{ background: #bf8700; }}
.section-line {{
    flex: 1;
    height: 2px;
    background: linear-gradient(90deg, #e1e4e8, transparent);
}}
/* Term cards — individual bordered cards */
.term-list {{
    display: flex;
    flex-direction: column;
    gap: 8px;
}}
.term-card {{
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: {term_fs};
    padding: 10px 16px;
    background: #fff7e0;
    border: 1px solid #ffe08a;
    border-left: 4px solid #bf8700;
    border-radius: 8px;
    line-height: 1.5;
}}
.term-en {{
    color: #8a5a00;
    font-weight: 700;
}}
.term-arrow {{
    color: #999;
    flex-shrink: 0;
}}
.term-cn {{
    color: #1f2328;
    font-weight: 500;
}}
/* Quote card — purple tinted with left border */
.quote-card {{
    font-size: {quote_fs};
    font-style: italic;
    color: #5b3b8c;
    line-height: 1.6;
    text-align: center;
    padding: 20px 24px;
    background: #f6f0fb;
    border: 1px solid #d8c8ed;
    border-left: 4px solid #8250df;
    border-radius: 8px;
}}
/* Image */
.img-wrap {{
    text-align: center;
    margin-bottom: 8px;
}}
.img-wrap img {{
    max-width: 85%;
    border-radius: 12px;
    border: 2px solid #e1e4e8;
}}
/* Footer with top border */
.footer {{
    padding: 14px {padding};
    font-size: 14px;
    color: #8c959f;
    text-align: center;
    border-top: 1px solid #e1e4e8;
    background: #f9fafb;
}}
</style></head><body>
<div class="card">
    <div class="card-head">
        <div class="progress">第 {esc(str(idx))} / {esc(str(total))} 张</div>
        <div class="topic">{main_title}</div>
        {('<div class="topic-en">' + en_subtitle + '</div>') if en_subtitle else ''}
        {('<span class="chapter-badge">' + chapter + '</span>') if chapter else ''}
    </div>
    <div class="card-body">
        {img_html}
        {body}
    </div>
    <div class="footer">{esc(date_str)}</div>
</div>
</body></html>'''
    return html_str


def crop_whitespace(img_path, out_path=None):
    """Crop trailing whitespace from bottom of image for auto-height mode.
    Uses a tolerance threshold so near-white colors are treated as background."""
    from PIL import Image
    import numpy as np
    if out_path is None:
        out_path = img_path
    img = Image.open(img_path).convert('RGB')
    arr = np.array(img)
    # Background is #eef2f7 = (238,242,247). Threshold at 235.
    is_content = (arr[:, :, 0] < 235) | (arr[:, :, 1] < 235) | (arr[:, :, 2] < 235)
    rows_with_content = np.any(is_content, axis=1)
    if rows_with_content.any():
        last_content_row = np.where(rows_with_content)[0][-1]
        bottom = min(last_content_row + 21, img.height)
        cropped = img.crop((0, 0, img.width, bottom))
        cropped.save(out_path, 'PNG')
        return cropped.size
    return img.size


def verify_image(img_path):
    """Verify the generated PNG is valid and non-empty."""
    from PIL import Image
    try:
        img = Image.open(img_path)
        w, h = img.size
        if w < 10 or h < 10:
            return {'ok': False, 'error': f'Image too small: {w}x{h}'}
        pixels = list(img.convert('RGB').getdata())
        unique_colors = set(pixels[:1000])
        if len(unique_colors) <= 1:
            return {'ok': False, 'error': 'Image appears to be blank (single color)'}
        return {'ok': True, 'width': w, 'height': h, 'mode': img.mode}
    except Exception as e:
        return {'ok': False, 'error': str(e)}


def main():
    ap = argparse.ArgumentParser(description='Generate flashcard image (auto-height)')
    ap.add_argument('--payload', required=True)
    ap.add_argument('--zh', help='translation JSON (for English books)')
    ap.add_argument('--out', required=True, help='output PNG path')
    ap.add_argument('--format', default='auto', choices=['1:1', '1:4', 'auto'],
                    help='1:1=800x800, 1:4=800x3200, auto=height adapts to content')
    ap.add_argument('--language', default='en', choices=['zh', 'en'])
    args = ap.parse_args()
    payload = json.load(open(args.payload, encoding='utf-8'))
    zh = json.load(open(args.zh, encoding='utf-8')) if args.zh else None
    language = args.language if '--language' in sys.argv else payload.get('language', 'en')
    zh, payload = normalize_all(zh, payload, language)
    date_str = datetime.date.today().isoformat()

    html_str = build_html(payload, zh, date_str, language=language, fmt=args.format)
    import render_common as _rc
    try:
        # 统一走 render_common：破折号兜底 CSS + 光栅化（PyMuPDF 优先，poppler 回退）
        # + 裁白（阈值/留白与 1.4.1 一致）+ 产物校验
        rendered = _rc.html_to_png(_rc.patch_style(html_str), args.out, dpi=150,
                                   crop=(args.format == 'auto'))
    except ImportError as e:
        print(json.dumps({'ok': False, 'error': 'html_to_png 依赖缺失: %s；请 '
                          'pip install weasyprint pymupdf（或保留 pdf2image + 系统 poppler）' % e},
                         ensure_ascii=False))
        sys.exit(1)
    verification = rendered['verification']
    if args.format in ('1:1', '1:4') and rendered.get('pages', 1) != 1:
        # 固定画布比例：多页会被纵向拼接成超比例长图，必须显式失败而不是静默交付
        print(json.dumps({'ok': False, 'error': '内容溢出固定画布（PDF %d 页 > 1）：%s 模式下应精简内容'
                          % (rendered['pages'], args.format)}, ensure_ascii=False))
        sys.exit(2)
    result = {'ok': True, 'image': args.out, 'format': args.format,
              'size': os.path.getsize(args.out), 'dimensions': rendered['size'],
              'date': date_str, 'pages': rendered['pages'],
              'rasterizer': rendered['rasterizer'], 'verification': verification}
    print(json.dumps(result, ensure_ascii=False))
    if not verification.get('ok'):
        sys.exit(2)

if __name__ == '__main__':
    main()
