#!/usr/bin/env python3
"""
Generate a LARGE-FONT flashcard PDF (A4, minimal content, huge fonts).
Ideal for vocabulary / terminology / single-concept learning.

Design philosophy: LESS text, BIGGER fonts. A flashcard, not a document.
  - Title: 48-64px (auto-shrink to fit one line, minimum 48px)
  - Core content: 24-28px
  - Terms: 22-24px
  - NO English original text (bilingual mode shows Chinese only)
  - NO related links section
  - NO explanation section (keep it to core idea + quote + terms only)
  - Minimum body font: 18px (but typically much larger)

Usage:
  python gen_card_pdf_large.py --payload <payload.json> [--zh <zh.json>] --out <output.pdf> [--language <zh|en>]
"""
import json, sys, os, argparse, datetime, re, html as html_mod
from weasyprint import HTML
from normalize_quotes import normalize_all

def esc(s):
    return html_mod.escape(s or '', quote=False)

def md_links_to_text(text):
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: '%s (%s)' % (m.group(1), m.group(2)), text or '')

def paras(text, md=False):
    out = []
    for ln in (text or '').split('\n'):
        ln = ln.strip()
        if ln:
            p = esc(ln)
            if md: p = md_links_to_text(p)
            out.append(p)
    return out

def estimate_title_size(topic, max_chars_per_line=18):
    """Estimate a good font size for the title so it fits nicely.
    Longer titles get smaller fonts (but minimum 48px).
    Short titles get up to 64px."""
    length = len(topic)
    if length <= 8:
        return 64
    elif length <= 12:
        return 56
    elif length <= 18:
        return 48
    else:
        return 42  # long title, will wrap

def build_html(payload, zh, date_str, language='en'):
    idx = payload.get('cardIndex', '?')
    total = payload.get('totalCards', '?')
    chapter = esc(payload.get('chapter', ''))
    topic = esc(payload.get('topic', ''))
    src = esc(payload.get('source', ''))
    book_title = esc(payload.get('bookTitle', ''))
    bilingual = language == 'en' and zh
    topic_zh = (zh or {}).get('topicZh', '')
    # For bilingual: show Chinese title as main, English as small subtitle
    main_title = esc(topic_zh) if (bilingual and topic_zh) else topic
    en_subtitle = topic if (bilingual and topic_zh) else ''

    # Auto-size title based on length
    title_size = estimate_title_size(main_title)

    sections = []

    # Terms only (no English original, no links)
    terms_zh = (zh or {}).get('terminologyZh', {})
    terms_en = payload.get('terminology', [])
    if bilingual and terms_zh:
        rows = ''.join('<tr><td class="term-en">%s</td><td class="term-arrow">→</td><td class="term-cn">%s</td></tr>'
                       % (esc(en), esc(cn)) for en, cn in terms_zh.items())
        sections.append('<div class="sec"><div class="sec-h term-h">术语 · Terms</div><table class="term-tbl">%s</table></div>' % rows)
    elif terms_en:
        chips = ''.join('<span class="term-chip">%s</span>' % esc(t) for t in terms_en)
        sections.append('<div class="sec"><div class="sec-h term-h">术语 · Terms</div><div class="terms">%s</div></div>' % chips)

    # Core idea (Chinese only for bilingual, no English)
    core_zh = (zh or {}).get('coreIdeaZh', '') if bilingual else payload.get('coreIdea', '')
    if core_zh:
        core_ps = ''.join('<p>%s</p>' % p for p in paras(core_zh))
        sections.append('<div class="sec"><div class="sec-h" style="color:#1a7f37">核心观点</div><div class="core">%s</div></div>' % core_ps)

    # Quote (Chinese only)
    quote_zh = (zh or {}).get('quoteZh', '') if bilingual else payload.get('quote', '')
    if quote_zh:
        sections.append('<div class="sec"><div class="sec-h" style="color:#8250df">金句</div><div class="quote">%s</div></div>' % esc(quote_zh))

    # image (if any)
    img_html = ''
    if payload.get('image'):
        img_html = '<div class="img-wrap"><img src="%s"></div>' % esc(payload['image'])

    body = ''.join(sections)

    html_str = f'''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">
<style>
@page {{ size: 210mm 297mm; margin: 22mm 20mm; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Hiragino Sans GB", "Heiti SC", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Micro Hei", "SimSun", "宋体", sans-serif; color: #1f2328; line-height: 1.6; }}
.card {{ border: 4px solid #e1e4e8; border-radius: 24px; overflow: hidden; min-height: 230mm; display: flex; flex-direction: column; }}
.card-head {{ background: linear-gradient(135deg,#1cb0f6,#0969da); color: #fff; padding: 28px 32px; text-align: center; }}
.card-head .progress {{ font-size: 22px; font-weight: 700; opacity: .9; margin-bottom: 16px; }}
.card-head .topic {{ font-size: {title_size}px; font-weight: 900; line-height: 1.2; word-break: keep-all; overflow-wrap: break-word; }}
.card-head .topic-en {{ font-size: 24px; font-weight: 500; margin-top: 10px; opacity: .8; font-style: italic; }}
.card-head .chapter {{ display:inline-block; font-size: 20px; background: rgba(255,255,255,.22); padding: 6px 20px; border-radius: 99px; margin-top: 16px; }}
.card-body {{ flex: 1; display: flex; flex-direction: column; justify-content: center; }}
.sec {{ padding: 24px 32px; border-bottom: 3px solid #f0f1f3; }}
.sec:last-child {{ border-bottom: none; }}
.sec-h {{ font-size: 24px; font-weight: 800; margin-bottom: 16px; letter-spacing: .5px; }}
.term-h {{ color: #cf222e; }}
.term-tbl {{ width: 100%; border-collapse: collapse; }}
.term-tbl td {{ padding: 12px 16px; border-bottom: 2px solid #f0f1f3; font-size: 24px; }}
.term-en {{ color: #8a5a00; font-weight: 700; white-space: nowrap; }}
.term-arrow {{ color: #ccc; font-size: 22px; text-align: center; width: 40px; }}
.term-cn {{ color: #1f2328; }}
.terms {{ display:flex; flex-wrap:wrap; gap:12px; }}
.term-chip {{ font-size: 22px; background:#fff7e0; color:#8a5a00; border:2px solid #ffe08a; padding:8px 20px; border-radius:99px; font-weight:700; }}
.core p {{ font-size: 28px; margin-bottom: 16px; color: #1f2328; line-height: 1.7; text-align: justify; }}
.core p:last-child {{ margin-bottom: 0; }}
.quote {{ font-size: 26px; font-style: italic; color: #5b3b8c; line-height: 1.6; padding: 8px 0; }}
.img-wrap {{ padding: 16px 32px; text-align: center; }}
.img-wrap img {{ max-width: 80%; border-radius: 16px; border: 2px solid #eee; }}
.footer {{ padding: 16px 32px 20px; font-size: 18px; color: #8c959f; text-align: center; border-top: 3px solid #f0f1f3; }}
</style></head><body>
<div class="card">
  <div class="card-head">
    <div class="progress">第 {idx} / {total} 张</div>
    <div class="topic">{main_title}</div>
    {('<div class="topic-en">' + en_subtitle + '</div>') if en_subtitle else ''}
    <span class="chapter">{chapter}</span>
  </div>
  <div class="card-body">
    {img_html}
    {body}
  </div>
  <div class="footer">{esc(date_str)} · {book_title}</div>
</div>
</body></html>'''
    return html_str

def main():
    ap = argparse.ArgumentParser(description='Generate LARGE-FONT flashcard PDF')
    ap.add_argument('--payload', required=True)
    ap.add_argument('--zh', help='translation JSON (for English books)')
    ap.add_argument('--out', required=True)
    ap.add_argument('--language', default='en', choices=['zh', 'en'])
    args = ap.parse_args()
    payload = json.load(open(args.payload, encoding='utf-8'))
    zh = json.load(open(args.zh, encoding='utf-8')) if args.zh else None
    language = args.language or payload.get('language', 'en')
    zh, payload = normalize_all(zh, payload, language)  # 规范化中文引号
    date_str = datetime.date.today().isoformat()
    card_id = payload.get('nextId', 'card')
    topic_zh = (zh or {}).get('topicZh', '')
    html_str = build_html(payload, zh, date_str, language=language)
    HTML(string=html_str).write_pdf(args.out)
    import re as _re
    safe_zh = _re.sub(r'[\\/:*?"<>|]', '_', topic_zh)[:40] if topic_zh else ''
    print(json.dumps({'ok': True, 'pdf': args.out, 'date': date_str,
                      'size': os.path.getsize(args.out), 'language': language,
                      'card_id': card_id, 'topicZh': topic_zh,
                      'template': 'pdf-large', 'suggestedSuffix': safe_zh}, ensure_ascii=False))

if __name__ == '__main__':
    main()
