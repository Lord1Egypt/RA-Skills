#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_card_long.py — 学习长图引擎（移动端竖版，卡片类型 `long-study`）

版式（来自实战多轮迭代，固定不变）：
    标题区（蓝色渐变，**顶部留白 >= 80px**，避开手机刘海/灵动岛）
    → 金句 → 专业术语 → 核心观点 → 要点 → 来源（一行灰字）

为什么这样排：手机上单列阅读，「金句」先给情绪价值，「术语」解决生词，
「核心观点」给一句话总结，「要点」才是细节。**不放「相关链接」**（移动端保持清爽，
链接只进 PDF）。

其它要点：
  * 宽度 800px（竖版单列，可用 --width 调整）；dpi=96 时与 CSS 像素 1:1，产物宽即 800px
    字号偏大（正文 22px、金句 24px、标题 35px）
  * 所有文字走 render_common.render_inline_text：HTML 转义 + MDX 清理 + 行内 markdown
    （否则 `<plugin-spec>` 这类占位符会被 HTML 吞掉，卡片缺字）
  * 生成后自动裁掉底部空白，并保留底部留白 >= 60px

用法：
    python gen_card_long.py --payload p.json [--zh z.json] --out card.png
        [--language zh|en] [--width 800] [--top-pad 80] [--dpi 96] [--no-crop]
"""
import argparse
import datetime
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import render_common as rc

CSS_TMPL = """
* {{ box-sizing: border-box; }}
body {{ font-family: {font}; color:#1f2328; margin:0; width:{width}px; }}
.card-head {{ background: linear-gradient(135deg,#1a73e8,#1557b0); color:#fff;
             padding:{top_pad}px 34px 40px; }}
.card-head .marker {{ font-size:22px; font-weight:700; opacity:.92; }}
.card-head .chapter {{ display:inline-block; font-size:17px; background:rgba(255,255,255,.22);
             padding:3px 14px; border-radius:99px; margin-left:10px; }}
.card-head .topic {{ font-size:35px; font-weight:800; margin-top:12px; line-height:1.32; }}
.card-head .topic-en {{ font-size:19px; opacity:.85; margin-top:6px; font-style:italic; }}
.sec {{ padding:20px 28px; border-bottom:1px solid #f0f1f3; }}
.sec-h {{ font-size:21px; font-weight:800; letter-spacing:.5px; margin-bottom:12px; }}
.c-idea {{ color:#1e8e3e; }} .c-point {{ color:#1a73e8; }}
.c-quote {{ color:#7b1fa2; }} .c-term {{ color:#d93025; }}
p {{ font-size:22px; line-height:1.8; margin:0; }}
ul {{ margin:0; padding-left:28px; }}
li {{ font-size:22px; line-height:1.8; margin-bottom:10px; }}
.quote {{ font-size:24px; line-height:1.75; padding:16px 20px; background:#faf5ff;
             border-left:6px solid #7b1fa2; border-radius:8px; font-weight:600; }}
table.term {{ width:100%; border-collapse:collapse; }}
table.term td {{ padding:10px; border-bottom:1px solid #f0f1f3; font-size:21px; }}
.term-en {{ color:#8a5a00; font-weight:700; width:42%; }}
.footer {{ padding:14px 28px 60px; font-size:15px; color:#8c959f; word-break:break-all; }}
code {{ font-family:"DejaVu Sans Mono",monospace; font-size:19px; background:#f4f5f7;
             padding:1px 5px; border-radius:3px; }}
"""


def norm_terms(terms):
    """术语兼容三种写法：dict{en:zh}、list[{en,zh}]、list[str]（items.json 标准格式，
    en 用原文、zh 置空——中文书模式下直接显示原文术语，不再静默丢弃）。"""
    out = []
    if isinstance(terms, dict):
        out = [{'en': k, 'zh': v or ''} for k, v in terms.items()]
    elif isinstance(terms, list):
        for t in terms:
            if isinstance(t, dict):
                out.append({'en': t.get('en', '') or '', 'zh': t.get('zh', '') or ''})
            elif isinstance(t, str) and t:
                out.append({'en': t, 'zh': ''})
    return [t for t in out if t.get('en') or t.get('zh')]


def build_html(payload, zh, width=800, top_pad=80, language='en'):
    zh = zh or {}
    bilingual = (language == 'en')
    topic_en = payload.get('topic', '')
    topic_zh = zh.get('topicZh', '') if bilingual else ''
    title = topic_zh or topic_en
    subtitle = topic_en if (bilingual and topic_zh) else ''

    marker = payload.get('marker') or ('序号 %s / %s' % (payload.get('cardIndex', '?'),
                                                         payload.get('totalCards', '?')))
    chapter = payload.get('chapter', '')

    def pick(zh_key, en_key):
        v = (zh.get(zh_key) if bilingual else '') or ''
        return v if v else (payload.get(en_key, '') or '')

    parts = ['<div class="card-head"><div><span class="marker">%s</span>%s</div>'
             '<div class="topic">%s</div>%s</div>' % (
                 rc.render_inline_text(marker),
                 ('<span class="chapter">%s</span>' % rc.render_inline_text(chapter)) if chapter else '',
                 rc.render_inline_text(title),
                 ('<div class="topic-en">%s</div>' % rc.render_inline_text(subtitle)) if subtitle else '')]

    quote = pick('quoteZh', 'quote')
    if quote:
        parts.append('<div class="sec"><div class="sec-h c-quote">金句</div>'
                     '<div class="quote">%s</div></div>' % rc.render_inline_text(quote))

    terms = norm_terms(zh.get('terminologyZh') if bilingual else None) or \
        norm_terms(payload.get('terminology'))
    if terms:
        shown = terms[:8]
        shown = terms[:8]
        rows = ''.join('<tr><td class="term-en">%s</td><td>%s</td></tr>'
                       % (rc.render_inline_text(t['en']), rc.render_inline_text(t['zh']))
                       for t in shown)
        if len(terms) > len(shown):
            rows += ('<tr><td colspan="2" style="color:#8c959f;font-size:16px;">'
                     '仅显示前 %d 条（共 %d 条）</td></tr>' % (len(shown), len(terms)))
        parts.append('<div class="sec"><div class="sec-h c-term">专业术语</div>'
                     '<table class="term">%s</table></div>' % rows)

    idea = pick('coreIdeaZh', 'coreIdea')
    if idea:
        parts.append('<div class="sec"><div class="sec-h c-idea">核心观点</div><p>%s</p></div>'
                     % rc.render_inline_text(idea))

    points = (zh.get('pointsZh') if bilingual else None) or payload.get('points') or []
    points = [p for p in points if isinstance(p, str) and p.strip()]
    if points:
        parts.append('<div class="sec"><div class="sec-h c-point">要点</div><ul>%s</ul></div>'
                     % ''.join('<li>%s</li>' % rc.render_inline_text(p) for p in points))

    source = payload.get('source') or payload.get('link') or ''
    if source:
        parts.append('<div class="footer">来源 · Source: %s</div>' % rc.render_inline_text(source))

    css = CSS_TMPL.format(font=rc.body_font_family(), width=width, top_pad=top_pad)
    dash = rc.dash_fix_css()
    if dash:
        css = dash + '\n' + css
    return ('<!doctype html><html lang="zh"><head><meta charset="utf-8"><style>'
            '@page { size: %dpx 20000px; margin: 0; }%s</style></head><body>%s</body></html>'
            % (width, css, ''.join(parts)))


def main():
    ap = argparse.ArgumentParser(description='生成学习长图 PNG（移动端竖版）')
    ap.add_argument('--payload', required=True)
    ap.add_argument('--zh', help='translation JSON (for English sources)')
    ap.add_argument('--out', required=True, help='output PNG path')
    ap.add_argument('--language', default='en', choices=['zh', 'en'])
    ap.add_argument('--width', type=int, default=800)
    ap.add_argument('--top-pad', type=int, default=80, help='标题区顶部留白（避开刘海屏）')
    ap.add_argument('--dpi', type=int, default=96, help='96 时与 CSS 像素 1:1')
    ap.add_argument('--no-crop', action='store_true', help='不裁底部空白')
    args = ap.parse_args()

    payload = json.load(open(args.payload, encoding='utf-8'))
    zh = json.load(open(args.zh, encoding='utf-8')) if args.zh else {}
    # 未显式传 --language 时优先用 payload 里的语言（argparse default 恒真值会吃掉回退）
    language = args.language if '--language' in sys.argv else payload.get('language', 'en')

    html_str = build_html(payload, zh, width=args.width, top_pad=args.top_pad, language=language)
    try:
        result = rc.html_to_png(html_str, args.out, dpi=args.dpi, crop=not args.no_crop,
                                crop_opts={'threshold': 250, 'pad': 64})
    except ImportError as e:
        # 依赖缺失（weasyprint/光栅化通道）时输出干净 JSON，不裸 traceback
        print(json.dumps({'ok': False, 'type': 'long-study', 'error': '缺少渲染依赖: %s' % e},
                         ensure_ascii=False))
        sys.exit(1)
    result.update({'ok': True, 'type': 'long-study', 'date': datetime.date.today().isoformat()})
    if not result['verification'].get('ok'):
        result['ok'] = False
    print(json.dumps(result, ensure_ascii=False))
    sys.exit(0 if result['ok'] else 2)


if __name__ == '__main__':
    main()
