#!/usr/bin/env python3
"""
Generate a card-style PDF from a knowledge point payload.
Supports both bilingual (en→zh) and Chinese-only (no translation) modes.

Usage:
  python gen_card_pdf.py --payload <payload.json> [--zh <zh.json>] --out <output.pdf> [--language <zh|en>]

For English books: --language en --zh <translation.json> (bilingual card)
For Chinese books: --language zh (no --zh needed, single-language card)
"""
import json, sys, os, argparse, datetime, re, html as html_mod
from weasyprint import HTML
from normalize_quotes import normalize_all

def esc(s):
    return html_mod.escape(s or '', quote=False)

def md_links_to_text(text):
    """Convert markdown [text](url) to 'text (url)' plain text — IMA cannot click links."""
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)',
                  lambda m: '%s (%s)' % (m.group(1), m.group(2)), text)

def paras(text, md=False):
    out = []
    for ln in (text or '').split('\n'):
        ln = ln.strip()
        if ln:
            p = esc(ln)
            if md:
                p = md_links_to_text(p)
            out.append(p)
    return out

def build_html(payload, zh, date_str, language='en'):
    idx = payload.get('cardIndex', '?')
    total = payload.get('totalCards', '?')
    chapter = esc(payload.get('chapter', ''))
    topic = esc(payload.get('topic', ''))
    src = esc(payload.get('source', ''))
    book_title = esc(payload.get('bookTitle', ''))
    bilingual = language == 'en' and zh  # English book with translation

    sections = []
    # Terminology table
    terms_zh = (zh or {}).get('terminologyZh', {})
    terms_en = payload.get('terminology', [])
    if bilingual and terms_zh:
        rows = ''.join('<tr><td class="term-en">%s</td><td class="term-cn">%s</td></tr>' % (esc(en), esc(cn))
                       for en, cn in terms_zh.items())
        sections.append('<div class="sec"><div class="sec-h term-h">术语对照 · Terminology</div><table class="term-tbl">%s</table></div>' % rows)
    elif terms_en:
        chips = ''.join('<span class="term-chip">%s</span>' % esc(t) for t in terms_en)
        sections.append('<div class="sec"><div class="sec-h term-h">关键术语 · Key Terms</div><div class="terms">%s</div></div>' % chips)

    # Content blocks
    def block(title_cn, title_en, zh_text, en_text, color, md=False):
        zh_ps = ''.join('<p>%s</p>' % p for p in paras(zh_text, md=md)) if zh_text else ''
        en_ps = ''.join('<p class="en">%s</p>' % p for p in paras(en_text, md=md)) if en_text else ''
        if not zh_ps and not en_ps:
            return ''
        if bilingual:
            return ('<div class="sec"><div class="sec-h" style="color:%s">%s · %s</div>'
                    '<div class="zh">%s</div><div class="en-wrap">%s</div></div>'
                    ) % (color, title_cn, title_en, zh_ps, en_ps)
        else:
            # single language: show whichever content is available
            content = zh_ps or en_ps
            cls = 'zh' if zh_ps else 'en-wrap'
            return ('<div class="sec"><div class="sec-h" style="color:%s">%s</div>'
                    '<div class="%s">%s</div></div>') % (color, title_cn if zh_ps else title_en, cls, content)

    if bilingual:
        sections.append(block('核心观点', 'Core Idea', zh.get('coreIdeaZh',''), payload.get('coreIdea',''), '#1a7f37'))
        sections.append(block('详细解释', 'Explanation', zh.get('explanationZh',''), payload.get('explanation',''), '#0969da', md=True))
        sections.append(block('金句', 'Key Quote', zh.get('quoteZh',''), payload.get('quote',''), '#8250df'))
        sections.append(block('应用场景', 'Application', zh.get('applicationZh',''), payload.get('application',''), '#bf8700', md=True))
    else:
        # Chinese book: content is in payload directly, no translation needed
        label = '核心观点' if language == 'zh' else 'Core Idea'
        sections.append(block(label, label, payload.get('coreIdea',''), '', '#1a7f37'))
        label2 = '详细解释' if language == 'zh' else 'Explanation'
        sections.append(block(label2, label2, payload.get('explanation',''), '', '#0969da', md=True))
        label3 = '金句' if language == 'zh' else 'Key Quote'
        sections.append(block(label3, label3, payload.get('quote',''), '', '#8250df'))
        label4 = '应用场景' if language == 'zh' else 'Application'
        sections.append(block(label4, label4, payload.get('application',''), '', '#bf8700', md=True))

    # image (base64 data URI or URL)
    img_html = ''
    if payload.get('image'):
        img_html = '<div class="img-wrap"><img src="%s"></div>' % esc(payload['image'])

    # related links — plain text URLs (IMA can't click)
    links_html = ''
    rl = payload.get('relatedLinks', [])
    rl_zh = (zh or {}).get('relatedLinksZh', []) if bilingual else []
    zh_map = {item['href']: item.get('textZh', '') for item in rl_zh if isinstance(item, dict) and item.get('href')}
    if rl:
        link_items = []
        for l in rl:
            if isinstance(l, dict):
                href = l.get('href',''); text_en = l.get('text','')
            else:
                href = str(l); text_en = ''
            text_zh = zh_map.get(href, '')
            if text_zh and text_en:
                label = '%s / %s' % (text_zh, text_en)
            elif text_zh:
                label = text_zh
            elif text_en:
                label = text_en
            else:
                label = ''
            is_ext = '【延展资源】' in text_en or '【扩展】' in text_en
            mark = ' <span class="ext-tag">延展</span>' if is_ext else ''
            if label:
                link_items.append('<div class="link-item">%s%s<br><span class="link-url">%s</span></div>' % (esc(label), mark, esc(href)))
            else:
                link_items.append('<div class="link-item"><span class="link-url">%s</span></div>' % esc(href))
        links_html = '<div class="sec"><div class="sec-h" style="color:#0969da">相关链接 · Related Links</div><div class="links">%s</div></div>' % ''.join(link_items)

    note_html = ''
    if (zh or {}).get('note'):
        note_html = '<div class="note">译注：%s</div>' % esc(zh['note'])

    body = ''.join(sections)

    html_str = f'''<!DOCTYPE html><html lang="zh"><head><meta charset="UTF-8">
<style>
@page {{ size: 210mm 297mm; margin: 14mm 12mm; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: "Microsoft YaHei", "微软雅黑", "PingFang SC", "Hiragino Sans GB", "Heiti SC", "Noto Sans CJK SC", "Source Han Sans SC", "WenQuanYi Micro Hei", "SimSun", "宋体", sans-serif; color: #1f2328; line-height: 1.7; }}
.card {{ border: 2px solid #e1e4e8; border-radius: 18px; overflow: hidden; }}
.card-head {{ background: linear-gradient(135deg,#1cb0f6,#0969da); color: #fff; padding: 16px 22px; }}
.card-head .progress {{ font-size: 17px; font-weight: 700; opacity: .92; }}
.card-head .topic {{ font-size: 25px; font-weight: 800; margin-top: 6px; line-height: 1.3; }}
.card-head .chapter {{ display:inline-block; font-size: 13px; background: rgba(255,255,255,.22); padding: 3px 12px; border-radius: 99px; margin-top: 8px; }}
.sec {{ padding: 14px 22px; border-bottom: 1px solid #f0f1f3; }}
.sec:last-child {{ border-bottom: none; }}
.sec-h {{ font-size: 15px; font-weight: 800; margin-bottom: 10px; letter-spacing: .5px; }}
.term-h {{ color: #cf222e; }}
.term-tbl {{ width: 100%; border-collapse: collapse; }}
.term-tbl td {{ padding: 6px 10px; border-bottom: 1px solid #f0f1f3; font-size: 16px; }}
.term-en {{ color: #8a5a00; font-weight: 600; width: 38%; white-space: nowrap; }}
.term-cn {{ color: #1f2328; }}
.terms {{ display:flex; flex-wrap:wrap; gap:7px; }}
.term-chip {{ font-size:14px; background:#fff7e0; color:#8a5a00; border:1px solid #ffe08a; padding:4px 11px; border-radius:99px; }}
.zh p {{ font-size: 18px; margin-bottom: 9px; color: #1f2328; }}
.en-wrap {{ margin-top: 8px; padding-top: 8px; border-top: 1px dashed #d8dee4; }}
.en-wrap p.en {{ font-size: 15px; color: #57606a; margin-bottom: 6px; font-style: italic; }}
.en-wrap p {{ font-size: 18px; margin-bottom: 9px; color: #1f2328; }}
.img-wrap {{ padding: 10px 22px; }}
.img-wrap img {{ max-width: 100%; border-radius: 10px; border: 1px solid #eee; }}
.links {{ }}
.link-item {{ font-size: 14px; margin-bottom: 8px; word-break: break-all; }}
.link-url {{ font-size: 13px; color: #6e7781; word-break: break-all; }}
.ext-tag {{ display:inline-block; font-size:11px; background:#8250df; color:#fff; padding:1px 6px; border-radius:4px; margin-left:4px; vertical-align: middle; }}
.note {{ padding: 12px 22px 16px; font-size: 13.5px; color: #6e7781; border-top: 1px solid #f0f1f3; background: #fafbfc; }}
.footer {{ padding: 8px 22px 14px; font-size: 12px; color: #8c959f; text-align: center; word-break: break-all; }}
</style></head><body>
<div class="card">
  <div class="card-head">
    <div class="progress">第 {idx} / {total} 张 · {esc(date_str)}</div>
    <div class="topic">{topic}</div>
    <span class="chapter">{chapter}</span>
  </div>
  {img_html}
  {body}
  {links_html}
  {note_html}
  <div class="footer">来源 / Source: {src}</div>
</div>
</body></html>'''
    return html_str

def main():
    ap = argparse.ArgumentParser()
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
    html_str = build_html(payload, zh, date_str, language=language)
    HTML(string=html_str).write_pdf(args.out)
    print(json.dumps({'ok': True, 'pdf': args.out, 'date': date_str,
                      'size': os.path.getsize(args.out), 'language': language}, ensure_ascii=False))

if __name__ == '__main__':
    main()
