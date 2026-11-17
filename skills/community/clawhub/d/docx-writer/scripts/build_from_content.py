#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
声明式内容 → docx（docx-writer 引擎 CLI）

用法
----
    python build_from_content.py --content content.yaml --out out.docx
    python build_from_content.py --content content.json --template push --out out.docx
    python build_from_content.py --content content.yaml        # --out 缺省=当前目录/content.docx

内容文件（YAML / JSON）
----------------------
    template: push              # 可选；也可用 --template 覆盖
    image_base: ./imgs          # 可选；image 相对路径的基准目录
    blocks:
      - { type: title,    text: "标题" }
      - { type: heading,  level: 1, text: "一、引言" }
      - { type: para,     style: body, text: "正文{F1}", fn: { F1: "注释" } }
      - { type: para,     style: body, text: "由 {X1} 可得", lx: { X1: "\\alpha_0=\\arctan(p_x/p_y)" } }
      - { type: formula,  latex: "E=mc^2", caption: "(1)" }
      - { type: caption,  text: "图1  示意" }
      - { type: image,    path: a.jpg, caption: "图1  示意", width: 14cm }
      - { type: table,    caption: "表1", headers: [a, b], rows: [[1, 2]], style: table }
      - { type: signature, lines: ["文案丨xx", "审核丨xx"] }
      - { type: blank }
      - { type: pagebreak }

输出：stdout 为 JSON 结果，进度写 stderr。
"""
import sys, os, json, argparse

sys.stdout.reconfigure(encoding='utf-8')
sys.stderr.reconfigure(encoding='utf-8')

from docx_engine import Template, Builder  # noqa: E402


def load_content(path):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    if path.endswith('.json'):
        return json.loads(text)
    import yaml
    return yaml.safe_load(text)


def render(content, template_ref, out_path, base_override=None):
    tpl = Template.load(template_ref)
    b = Builder(tpl)
    base = base_override or content.get('image_base') or '.'
    if not os.path.isabs(base):
        base = os.path.join(os.path.dirname(os.path.abspath(content.get('__path__', '.'))), base)

    def img_path(p):
        if os.path.isabs(p) or os.path.exists(p):
            return p
        return os.path.join(base, p)

    n = 0
    for blk in content.get('blocks', []):
        n += 1
        t = blk.get('type', 'para')
        if t == 'title':
            b.title(blk['text'])
        elif t == 'heading':
            b.heading(blk['text'], level=blk.get('level', 1), style=blk.get('style'))
        elif t == 'para':
            b.para(blk.get('text', ''), style=blk.get('style', 'body'),
                   fn_map=blk.get('fn'), lx_map=blk.get('lx'))
        elif t == 'formula':
            b.formula(blk['latex'], caption=blk.get('caption'),
                      width=blk.get('width'), style=blk.get('style', 'formula'),
                      scale=blk.get('scale'))
        elif t == 'caption':
            b.caption(blk['text'], style=blk.get('style', 'caption'))
        elif t == 'note':
            b.para(blk.get('text', ''), style=blk.get('style', 'note'))
        elif t == 'image':
            b.image(img_path(blk['path']), caption=blk.get('caption'),
                    width=blk.get('width'), style=blk.get('style', 'image'),
                    caption_style=blk.get('caption_style', 'caption'))
        elif t == 'table':
            b.table(blk.get('headers', []), blk.get('rows', []),
                    caption=blk.get('caption'), style=blk.get('style', 'table'))
        elif t == 'signature':
            for line in blk.get('lines', []):
                b.para(line, style=blk.get('style', 'signature'))
        elif t == 'blank':
            b.para('', style=blk.get('style', 'blank'))
        elif t == 'pagebreak':
            b.doc.add_page_break()
        else:
            raise ValueError('unknown block type: %s' % t)
    b.save(out_path)
    return n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--content', required=True, help='内容文件（YAML/JSON，输入）')
    ap.add_argument('--out', default=None,
                    help='输出 docx 路径（默认：当前工作目录/<content 文件名>.docx）')
    ap.add_argument('--template', default=None, help='覆盖内容文件里的 template')
    ap.add_argument('--image-base', default=None)
    a = ap.parse_args()
    a.out = a.out or os.path.join(
        os.getcwd(), os.path.splitext(os.path.basename(a.content))[0] + '.docx')
    try:
        content = load_content(a.content)
        content['__path__'] = os.path.abspath(a.content)
        tpl = a.template or content.get('template')
        if not tpl:
            raise ValueError('no template: set `template:` in content or pass --template')
        n = render(content, tpl, a.out, base_override=a.image_base)
        print(json.dumps({'status': 'ok', 'out': os.path.abspath(a.out),
                          'template': tpl, 'blocks': n}, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({'status': 'error', 'error': str(e)}, ensure_ascii=False))
        sys.exit(1)


if __name__ == '__main__':
    main()
