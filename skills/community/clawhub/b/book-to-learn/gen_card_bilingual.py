#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_card_bilingual.py — 中英对照文档引擎（A4，卡片类型 `pdf-bilingual`）

版式（来自实战定稿，固定顺序）：
    专业术语 → 核心观点（中 + 英） → 正文翻译（逐块「中文译文 + 英文原文」）
    → 相关链接（纯文本 URL） → 来源

要点：
  * **超链接一律纯文本**：知识库 / IM 里链接不可点击，正文中的 markdown 链接
    渲染为纯文本，完整 URL 统一列在「相关链接」区（可复制）。
  * 正文逐块对照：按空行切块，中英块数应一一对应（用 `book_setup.py validate` 校验）。
  * 正文里的 markdown 表格渲染为真表格；MDX 组件标签转为可读文本；
    `<img src="/assets/...">` 按 --assets 指定的目录映射本地文件并真实嵌入。
  * 破折号兜底 + CJK 字体自动探测（见 render_common）。

用法：
    python gen_card_bilingual.py --payload p.json [--zh z.json] --out card.pdf
        [--language zh|en] [--assets <图片目录>]...
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
body {{ font-family: {font}; color:#1f2328; }}
.card-head {{ background: linear-gradient(135deg,#1a73e8,#1557b0); color:#fff; padding:16px 22px; }}
.card-head .marker {{ font-size:15px; font-weight:700; opacity:.9; }}
.card-head .chapter {{ display:inline-block; font-size:12px; background:rgba(255,255,255,.22);
             padding:2px 10px; border-radius:99px; margin-left:8px; }}
.card-head .topic {{ font-size:25px; font-weight:800; margin-top:8px; line-height:1.3; }}
.card-head .topic-en {{ font-size:13px; opacity:.85; margin-top:4px; font-style:italic; }}
.sec {{ padding:12px 22px; border-bottom:1px solid #f0f1f3; }}
.sec-h {{ font-size:14px; font-weight:800; letter-spacing:.5px; margin-bottom:8px; }}
.c-idea {{ color:#1e8e3e; }} .c-point {{ color:#1a73e8; }}
.c-term {{ color:#d93025; }} .c-link {{ color:#f9ab00; }}
p {{ font-size:16px; line-height:1.75; margin:0 0 8px; }}
ul {{ margin:0; padding-left:22px; }} li {{ font-size:16px; line-height:1.75; margin-bottom:5px; }}
table.term {{ width:100%; border-collapse:collapse; }}
table.term td {{ padding:5px 8px; border-bottom:1px solid #f0f1f3; font-size:15px; }}
.term-en {{ color:#8a5a00; font-weight:600; width:40%; }}
table.mdtable {{ width:100%; border-collapse:collapse; font-size:12px; margin:6px 0 12px; }}
table.mdtable th, table.mdtable td {{ border:1px solid #98a1aa; padding:4px 6px; vertical-align:top; line-height:1.5; }}
table.mdtable th {{ background:#eef1f4; }}
table.mdtable tbody tr:nth-child(even) {{ background:#fafbfc; }}
.en {{ font-size:13px; color:#57606a; font-style:italic; margin-bottom:11px; }}
.link-item {{ font-size:14px; margin-bottom:7px; word-break:break-all; }}
.link-url {{ font-size:12.5px; color:#6e7781; word-break:break-all; }}
.fig img {{ max-width:100%; border:1px solid #d0d7de; border-radius:6px; margin:8px 0; }}
.footer {{ padding:10px 22px; font-size:12px; color:#8c959f; word-break:break-all; }}
code {{ font-family:"DejaVu Sans Mono",monospace; font-size:13px; background:#f4f5f7;
             padding:1px 4px; border-radius:3px; }}
pre {{ font-family:"DejaVu Sans Mono",monospace; font-size:12px; background:#f4f5f7;
             padding:10px; border-radius:6px; white-space:pre-wrap; word-break:break-all; margin:6px 0; }}
"""


def split_blocks(text):
    """按空行切块（与 book-to-learn 的 explanation 分段约定一致）。"""
    out, cur = [], []
    for line in (text or '').split('\n'):
        if line.strip() == '':
            if cur:
                out.append('\n'.join(cur))
                cur = []
        else:
            cur.append(line)
    if cur:
        out.append('\n'.join(cur))
    return [b for b in out if b.strip()]


def norm_terms(terms):
    out = []
    if isinstance(terms, dict):
        out = [{'en': k, 'zh': v} for k, v in terms.items()]
    elif isinstance(terms, list):
        for t in terms:
            if isinstance(t, dict):
                out.append({'en': t.get('en', ''), 'zh': t.get('zh', '')})
            elif isinstance(t, str):
                out.append({'en': t, 'zh': ''})
    return [t for t in out if t.get('en') or t.get('zh')]


def build_html(payload, zh, language='en', assets_dirs=None):
    zh = zh or {}
    bilingual = (language == 'en')
    assets_dirs = assets_dirs or []
    resolver = rc.make_img_resolver(assets_dirs) if assets_dirs else None

    topic_en = payload.get('topic', '')
    topic_zh = zh.get('topicZh', '') if bilingual else ''
    title = topic_zh or topic_en
    subtitle = topic_en if (bilingual and topic_zh) else ''

    marker = payload.get('marker') or ('%s / %s' % (payload.get('cardIndex', '?'),
                                                    payload.get('totalCards', '?')))
    chapter = payload.get('chapter', '')
    parts = ['<div class="card-head"><div><span class="marker">%s</span>%s</div>'
             '<div class="topic">%s</div>%s</div>' % (
                 rc.render_inline_text(marker),
                 ('<span class="chapter">%s</span>' % rc.render_inline_text(chapter)) if chapter else '',
                 rc.render_inline_text(title),
                 ('<div class="topic-en">%s</div>' % rc.render_inline_text(subtitle)) if subtitle else '')]

    # 1) 专业术语
    terms = norm_terms(zh.get('terminologyZh') if bilingual else None) or \
        norm_terms(payload.get('terminology'))
    if terms:
        rows = ''.join('<tr><td class="term-en">%s</td><td>%s</td></tr>'
                       % (rc.render_inline_text(t['en']), rc.render_inline_text(t['zh']))
                       for t in terms)
        parts.append('<div class="sec"><div class="sec-h c-term">专业术语 · Terms</div>'
                     '<table class="term">%s</table></div>' % rows)

    # 2) 核心观点（中 + 英）
    idea_zh = (zh.get('coreIdeaZh', '') if bilingual else '') or ''
    idea_en = payload.get('coreIdea', '') or ''
    if idea_zh or idea_en:
        inner = ''
        if idea_zh:
            inner += '<p>%s</p>' % rc.render_inline_text(idea_zh)
        if idea_en:
            inner += '<p class="en">%s</p>' % rc.render_inline_text(idea_en)
        parts.append('<div class="sec"><div class="sec-h c-idea">核心观点 · Summary</div>%s</div>' % inner)

    # 3) 正文翻译：逐块「中文 + 英文」
    en_blocks = split_blocks(payload.get('explanation', ''))
    zh_blocks = split_blocks(zh.get('explanationZh', '') if bilingual else '')
    body = []
    n_blocks = max(len(en_blocks), len(zh_blocks))
    if len(zh_blocks) > len(en_blocks):
        # 译文多分段：原实现只遍历 en_blocks，多出的译文块被静默丢弃
        print('[warn] 译文块数(%d)多于原文块数(%d)，多出的译文仍会输出（建议校验对齐）'
              % (len(zh_blocks), len(en_blocks)), file=sys.stderr)
    for i in range(n_blocks):
        en = en_blocks[i] if i < len(en_blocks) else ''
        cn = zh_blocks[i] if i < len(zh_blocks) else ''
        if en and en.strip().startswith('```'):
            body.append('<pre>%s</pre>' % rc.esc(en.strip()))
            continue
        tbl_en, tbl_cn = (rc.md_table(en) if en else None), (rc.md_table(cn) if cn else None)
        if tbl_en or tbl_cn:
            if tbl_cn:
                body.append('<div class="sec-h" style="font-size:12px;color:#57606a">中文对照</div>%s' % tbl_cn)
            if tbl_en:
                body.append(tbl_en)
            continue
        if cn:
            text = rc.clean_mdx(cn, resolve_img=resolver)
            body.append('<p>%s</p>' % rc.apply_images(rc.md_inline(text)))
        if en:
            text_en = rc.clean_mdx(en, resolve_img=resolver)
            body.append('<p class="en">%s</p>' % rc.apply_images(rc.md_inline(text_en)))
    if body:
        parts.append('<div class="sec"><div class="sec-h c-point">正文翻译 · Full Translation</div>'
                     '%s</div>' % ''.join(body))

    # 4) 相关链接（纯文本 URL）
    links = payload.get('relatedLinks') or []
    if links:
        items = ''
        for l in links:
            if isinstance(l, dict):
                t, h = l.get('text', ''), l.get('href', '')
            else:
                t, h = str(l), str(l)
            items += '<div class="link-item">%s<div class="link-url">%s</div></div>' % (
                rc.render_inline_text(t), rc.render_inline_text(h))
        parts.append('<div class="sec"><div class="sec-h c-link">相关链接 · Links</div>%s</div>' % items)

    source = payload.get('source') or payload.get('link') or ''
    if source:
        parts.append('<div class="footer">来源 · Source: %s</div>' % rc.render_inline_text(source))

    css = CSS_TMPL.format(font=rc.body_font_family())
    return ('<!doctype html><html lang="zh"><head><meta charset="utf-8"><style>'
            '@page { size: A4; margin: 13mm 12mm; }%s</style></head><body>%s</body></html>'
            % (css, ''.join(parts)))


def main():
    ap = argparse.ArgumentParser(description='生成中英对照 PDF')
    ap.add_argument('--payload', required=True)
    ap.add_argument('--zh', help='translation JSON (for English sources)')
    ap.add_argument('--out', required=True, help='output PDF path')
    ap.add_argument('--language', default='en', choices=['zh', 'en'])
    ap.add_argument('--assets', action='append', default=[], help='图片目录（可重复）')
    args = ap.parse_args()

    payload = json.load(open(args.payload, encoding='utf-8'))
    zh = json.load(open(args.zh, encoding='utf-8')) if args.zh else {}
    # 未显式传 --language 时优先用 payload 里的语言（argparse default 恒真值会吃掉回退）
    language = args.language if '--language' in sys.argv else payload.get('language', 'en')
    if language != 'en':
        # 本引擎是中英对照版式：中文书内容会被排成小号斜体英文样式，提示改用 pdf-standard
        print('[warn] pdf-bilingual 是中英对照引擎，中文书建议用 pdf-standard / long-study', file=sys.stderr)

    assets = list(args.assets)
    if payload.get('assetsDir'):
        assets.append(payload['assetsDir'])
    html_str = build_html(payload, zh, language=language, assets_dirs=assets)

    from weasyprint import HTML
    HTML(string=rc.patch_style(html_str)).write_pdf(args.out)
    # 产物校验：非空 + PDF 魔数
    try:
        size = os.path.getsize(args.out)
        with open(args.out, 'rb') as _f:
            magic = _f.read(4)
    except OSError:
        size, magic = 0, b''
    if size <= 0 or magic != b'%PDF':
        print(json.dumps({'ok': False, 'error': 'PDF 产物无效（空文件或魔数不符）: %s' % args.out},
                         ensure_ascii=False), file=sys.stderr)
        sys.exit(1)
    print(json.dumps({'ok': True, 'pdf': args.out, 'type': 'pdf-bilingual',
                      'size': size,
                      'date': datetime.date.today().isoformat()}, ensure_ascii=False))


if __name__ == '__main__':
    main()
