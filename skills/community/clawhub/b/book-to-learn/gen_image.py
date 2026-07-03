#!/usr/bin/env python3
"""
Generate a MINIMAL supplementary image (1:1 or 1:4) — flashcard style.
Used as a visual supplement to Feishu card messages — NOT for standalone push.

Design: BIG fonts, MINIMAL content. Like a physical flashcard.
  - Title: huge (40-56px auto-sized)
  - Quote: large (28-32px)
  - Terms: large (22-26px)
  - NO core idea, NO explanation, NO links — just the essentials
  - 1:1 = 750x750 (square card), 1:4 = 750x3000 (long card)

Usage:
  python gen_image.py --payload <payload.json> [--zh <zh.json>] --out <output.png> [--format <1:1|1:4>] [--language <zh|en>]

Image generation: HTML → weasyprint PDF → pdf2image PNG
Design inspired by react-paper-memo (github.com/JustinChia/react-paper-memo) large-font card concept.
"""
import json, sys, os, argparse, datetime, re, html as html_mod, tempfile
from weasyprint import HTML
from normalize_quotes import normalize_all

def esc(s):
    return html_mod.escape(s or '', quote=False)

def estimate_title_size(topic, fmt='1:1'):
    """Auto-size title: shorter = bigger. Min 40px."""
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

def build_html(payload, zh, date_str, language='en', fmt='1:1'):
    idx = payload.get('cardIndex', '?')
    total = payload.get('totalCards', '?')
    topic = esc(payload.get('topic', ''))
    chapter = esc(payload.get('chapter', ''))
    bilingual = language == 'en' and zh
    topic_zh = (zh or {}).get('topicZh', '')
    main_title = esc(topic_zh) if (bilingual and topic_zh) else topic
    en_subtitle = topic if (bilingual and topic_zh) else ''

    if fmt == '1:4':
        page_w, page_h = '750px', '3000px'
        padding = '32px'
    else:
        page_w, page_h = '750px', '750px'
        padding = '24px'

    title_size = estimate_title_size(main_title, fmt)

    sections = []

    # Terms (minimal, large)
    terms_zh = (zh or {}).get('terminologyZh', {})
    if bilingual and terms_zh:
        rows = ''.join('<div class="term-row"><span class="term-en">%s</span> <span class="term-arrow">→</span> <span class="term-cn">%s</span></div>'
                       % (esc(en), esc(cn)) for en, cn in list(terms_zh.items())[:5])
        sections.append('<div class="sec"><div class="sec-h" style="color:#cf222e">术语</div>%s</div>' % rows)

    # Quote only (NO core idea, NO explanation)
    quote_zh = (zh or {}).get('quoteZh', '') if bilingual else payload.get('quote', '')
    if quote_zh:
        sections.append('<div class="sec"><div class="quote-box">%s</div></div>' % esc(quote_zh))

    # image
    img_html = ''
    if payload.get('image'):
        img_html = '<div class="img-wrap"><img src="%s"></div>' % esc(payload['image'])

    body = ''.join(sections)

    # font sizes scale up for 1:4
    quote_fs = '32px' if fmt == '1:4' else '26px'
    term_fs = '26px' if fmt == '1:4' else '22px'
    sec_h_fs = '28px' if fmt == '1:4' else '22px'

    html_str = f'''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">
<style>
@page {{ size: {page_w} {page_h}; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Hiragino Sans GB", "Noto Sans CJK SC", "SimSun", "宋体", sans-serif; color: #1f2328; width: {page_w}; }}
.card {{ background: linear-gradient(180deg, #eef2f7 0%, #fff 30%, #fff 100%); min-height: {page_h}; display: flex; flex-direction: column; }}
.card-head {{ background: linear-gradient(135deg, #1cb0f6, #0969da); color: #fff; padding: {padding}; text-align: center; }}
.card-head .topic {{ font-size: {title_size}px; font-weight: 900; line-height: 1.2; word-break: keep-all; }}
.card-head .topic-en {{ font-size: 20px; font-weight: 500; margin-top: 8px; opacity: .8; font-style: italic; }}
.card-head .progress {{ font-size: 18px; opacity: .85; margin-bottom: 12px; }}
.card-body {{ flex: 1; display: flex; flex-direction: column; justify-content: center; padding: {padding}; }}
.sec {{ margin-bottom: 24px; }}
.sec-h {{ font-size: {sec_h_fs}; font-weight: 800; margin-bottom: 12px; }}
.term-row {{ font-size: {term_fs}; margin-bottom: 10px; line-height: 1.5; }}
.term-en {{ color: #8a5a00; font-weight: 700; }}
.term-arrow {{ color: #999; margin: 0 8px; }}
.term-cn {{ color: #1f2328; }}
.quote-box {{ font-size: {quote_fs}; font-style: italic; color: #5b3b8c; line-height: 1.5; text-align: center; padding: 16px 0; }}
.img-wrap {{ text-align: center; margin-bottom: 20px; }}
.img-wrap img {{ max-width: 85%; border-radius: 12px; border: 1px solid #eee; }}
.footer {{ padding: 16px {padding}; font-size: 16px; color: #8c959f; text-align: center; border-top: 1px solid #eee; }}
</style></head><body>
<div class="card">
  <div class="card-head">
    <div class="progress">第 {idx} / {total} 张</div>
    <div class="topic">{main_title}</div>
    {('<div class="topic-en">' + en_subtitle + '</div>') if en_subtitle else ''}
  </div>
  <div class="card-body">
    {img_html}
    {body}
  </div>
  <div class="footer">{esc(date_str)}</div>
</div>
</body></html>'''
    return html_str

def main():
    ap = argparse.ArgumentParser(description='Generate minimal flashcard image (1:1 or 1:4)')
    ap.add_argument('--payload', required=True)
    ap.add_argument('--zh', help='translation JSON (for English books)')
    ap.add_argument('--out', required=True, help='output PNG path')
    ap.add_argument('--format', default='1:1', choices=['1:1', '1:4'])
    ap.add_argument('--language', default='en', choices=['zh', 'en'])
    args = ap.parse_args()
    payload = json.load(open(args.payload, encoding='utf-8'))
    zh = json.load(open(args.zh, encoding='utf-8')) if args.zh else None
    language = args.language or payload.get('language', 'en')
    zh, payload = normalize_all(zh, payload, language)  # 规范化中文引号
    date_str = datetime.date.today().isoformat()

    html_str = build_html(payload, zh, date_str, language=language, fmt=args.format)
    tmp_pdf = tempfile.mktemp(suffix='.pdf')
    HTML(string=html_str).write_pdf(tmp_pdf)

    try:
        from pdf2image import convert_from_path
        images = convert_from_path(tmp_pdf, dpi=150)
        if images:
            images[0].save(args.out, 'PNG')
            print(json.dumps({'ok': True, 'image': args.out, 'format': args.format,
                              'size': os.path.getsize(args.out), 'date': date_str}, ensure_ascii=False))
        else:
            print(json.dumps({'ok': False, 'error': 'pdf2image returned no images'}, ensure_ascii=False))
            sys.exit(1)
    except ImportError:
        print(json.dumps({'ok': False, 'error': 'pdf2image not installed. Run: pip install pdf2image (also needs poppler)'}, ensure_ascii=False))
        sys.exit(1)
    finally:
        if os.path.exists(tmp_pdf):
            os.remove(tmp_pdf)

if __name__ == '__main__':
    main()
