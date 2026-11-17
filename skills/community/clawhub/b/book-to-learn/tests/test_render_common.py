#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render_common 自检 —— 跨平台可用性验证。

用法：
    python3 tests/test_render_common.py            # 全量自检
    python3 tests/test_render_common.py --quick    # 跳过需要 weasyprint 的渲染检查

退出码：0 = 全部通过；1 = 有失败项（详情见输出）。
任何环境（含未装 weasyprint / 无网络的机器）都能跑 --quick。
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import render_common as rc


def check(name, got, want, mode='eq'):
    ok = (got == want) if mode == 'eq' else (want in (got or ''))
    return {'check': name, 'ok': ok, 'got': (got if isinstance(got, str) else repr(got))[:200],
            'want': want if isinstance(want, str) else repr(want)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--quick', action='store_true', help='跳过需要 weasyprint 的渲染检查')
    args = ap.parse_args()

    results = []

    # 1) 转义：markdown 行内
    results.append(check('md_inline/加粗+代码+链接文字化',
                         rc.md_inline('**a** and `b` and [t](http://x/1)'),
                         '<strong>a</strong> and <code>b</code> and t'))

    # 2) 卡片正面文字必须转义尖括号（本次踩过的坑：<plugin-spec> 被 HTML 吞掉）
    results.append(check('render_inline_text/尖括号占位符不被吞',
                         rc.render_inline_text('运行 install <plugin-spec> 即可'),
                         '&lt;plugin-spec&gt;', mode='in'))

    # 3) MDX/JSX 标签：title 提升为加粗引子，其余剥离
    mdx = '<Steps>\n<Step title="设置模式">\n- 第一步\n</Step>\n</Steps>'
    cleaned = rc.clean_mdx(mdx)
    results.append(check('clean_mdx/title 提升', cleaned, '**设置模式**', mode='in'))
    results.append({'check': 'clean_mdx/无标签残留',
                    'ok': ('<Step' not in cleaned and '<Steps>' not in cleaned),
                    'got': cleaned[:120], 'want': '无 <> 标签'})

    # 4) markdown 表格 → HTML 表格
    tbl = '| A | B |\n|---|---|\n| 1 | 2 |'
    results.append(check('md_table/渲染为 HTML 表', rc.md_table(tbl), '<table class="mdtable">', mode='in'))
    results.append({'check': 'md_table/非表格返回 None', 'ok': rc.md_table('普通段落') is None,
                    'got': repr(rc.md_table('普通段落')), 'want': 'None'})

    # 5) 图片解析：三种命名约定
    import tempfile
    tdir = tempfile.mkdtemp()
    flat = os.path.join(tdir, '_assets_a_b.png')
    open(flat, 'wb').write(b'\x89PNG\r\n\x1a\n')
    resolver = rc.make_img_resolver([tdir])
    results.append(check('make_img_resolver/扁平命名命中',
                         resolver('/assets/a/b.png'), flat))

    # 6) 占位符 → <img>
    ph = rc.clean_mdx('文字\n<img src="/assets/a/b.png" alt="x" />\n', resolve_img=resolver)
    html_with_img = rc.apply_images(rc.md_inline(ph))
    results.append(check('apply_images/占位符替换为 img',
                         html_with_img, 'file://' + flat, mode='in'))

    # 7) 破折号兜底 CSS（有字体则必须含 unicode-range）
    dash = rc.dash_fix_css()
    results.append({'check': 'dash_fix_css/存在或按缺失跳过',
                    'ok': (dash == '') or ('U+2014' in dash),
                    'got': (dash[:80] if dash else '(未找到 TrueType 字体，已跳过)'),
                    'want': '含 U+2014 或空串'})

    # 8) 环境体检
    rep = rc.runtime_report()
    print(json.dumps({'runtime': rep}, ensure_ascii=False, indent=2))
    results.append({'check': 'runtime_report/可运行', 'ok': 'platform' in rep, 'got': 'ok', 'want': 'ok'})

    # 9) 端到端：HTML → PNG（需要 weasyprint + 一个光栅化器）
    if args.quick:
        results.append({'check': 'html_to_png/已跳过(--quick)', 'ok': True, 'got': '-', 'want': '-'})
    elif not rep['deps'].get('weasyprint') or not rep['rasterizer_available']:
        results.append({'check': 'html_to_png/依赖缺失(跳过)',
                        'ok': True, 'got': 'weasyprint=%s rasterizer=%s' % (
                            rep['deps'].get('weasyprint'), rep['rasterizer_available']),
                        'want': '跳过'})
    else:
        out = os.path.join(tdir, 'card.png')
        html = ('<!doctype html><html><head><meta charset="utf-8"><style>'
                '@page{size:750px 1200px;margin:0}body{font-family:%s}'
                '%s</style></head><body><h1>自检 标题</h1>'
                '<p>破折号测试 —— 中文</p></body></html>' % (rc.body_font_family(), rc.dash_fix_css()))
        r = rc.html_to_png(html, out, crop=True)
        results.append({'check': 'html_to_png/端到端',
                        'ok': bool(r['verification'].get('ok')),
                        'got': json.dumps({'rasterizer': r['rasterizer'], 'size': r['size'],
                                           'verification': r['verification']}, ensure_ascii=False),
                        'want': 'verification.ok = True'})

    failed = [r for r in results if not r['ok']]
    print(json.dumps({'passed': len(results) - len(failed), 'failed': len(failed),
                      'results': results}, ensure_ascii=False, indent=2))
    sys.exit(1 if failed else 0)


if __name__ == '__main__':
    main()
