#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""render.py — 按「卡片类型 → 渲染引擎」调度

设计：**可复用的工具集中在一处（render_common.py），不可复用的版式各自独立成引擎**。
本调度器只做「选哪个引擎、传什么参数」，不掺和任何渲染细节。

用法：
    python render.py --list
    python render.py --type long-study --payload p.json [--zh z.json] --out card.png
    python render.py --type pdf-bilingual --payload p.json --out card.pdf --assets raw/imgs
    python render.py --type long-study --payload p.json --out x.png --dry-run
    python render.py --type long-study --payload p.json --out x.png --config books/<slug>/config.json

映射优先级：`--config` 里的 `renderer` > 内置默认。加一个自定义引擎不用改代码，
在 config.json 里补一条 `"my-type": "my_engine.py"` 即可。
"""
import argparse
import json
import os
import subprocess
import sys

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))

# 内置默认映射：卡片类型 → (引擎脚本, 传递的参数名列表)
DEFAULT_RENDERERS = {
    'pdf-standard':  ('gen_card_pdf.py',       ['payload', 'zh', 'out', 'language']),
    'pdf-large':     ('gen_card_pdf_large.py', ['payload', 'zh', 'out', 'language']),
    'long-image':    ('gen_image.py',          ['payload', 'zh', 'out', 'language', 'format']),
    'pdf-bilingual': ('gen_card_bilingual.py', ['payload', 'zh', 'out', 'language', 'assets']),
    'long-study':    ('gen_card_long.py',      ['payload', 'zh', 'out', 'language',
                                                 'width', 'top_pad', 'dpi', 'no_crop']),
}

# 属于「推送层」而不是渲染层的类型（避免误用）
PUSH_TYPES = {'feishu-card': 'send_feishu.py（推送层，请用推送流程）',
              'feishu-card+image': 'gen_image.py + send_feishu_api.py（推送层）'}

# 「资料拆卡」：竖版卡片长图，按画布比例分型；参数是 --cards/--outdir（不是 payload/out）
TILE_TYPES = {'tile-3x4': '3:4', 'tile-9x16': '9:16', 'tile-1x1': '1:1',
              'tile-4x3': '4:3', 'tile-16x9': '16:9'}


def load_mapping(config_path=None):
    mapping = {k: {'script': v[0], 'args': list(v[1])} for k, v in DEFAULT_RENDERERS.items()}
    if config_path and os.path.exists(config_path):
        cfg = json.load(open(config_path, encoding='utf-8'))
        for k, v in (cfg.get('renderer') or {}).items():
            if k in PUSH_TYPES:
                continue  # 旧 config 里混着推送类型，跳过
            mapping[k] = {'script': v, 'args': list(DEFAULT_RENDERERS.get(
                k, ('', ['payload', 'zh', 'out', 'language']))[1])}
    return mapping


def build_cmd(script, arg_names, a):
    cmd = [sys.executable, os.path.join(SKILL_DIR, script)]
    for name in arg_names:
        flag = '--' + name.replace('_', '-')
        val = getattr(a, name, None)
        if val is None or val is False or val == []:
            continue
        if name == 'no_crop':
            cmd.append(flag)
        elif isinstance(val, list):
            for v in val:
                cmd += [flag, str(v)]
        else:
            cmd += [flag, str(val)]
    return cmd


def main():
    ap = argparse.ArgumentParser(description='按卡片类型调度渲染引擎')
    ap.add_argument('--type', help='卡片类型，见 --list')
    ap.add_argument('--list', action='store_true', help='列出可用的类型与引擎')
    ap.add_argument('--config', help='config.json 路径（其中的 renderer 可覆盖默认映射）')
    ap.add_argument('--payload', help='载荷 JSON')
    ap.add_argument('--zh', help='翻译 JSON')
    ap.add_argument('--out', help='输出文件路径')
    ap.add_argument('--language', default=None, choices=[None, 'zh', 'en'])
    ap.add_argument('--assets', action='append', default=[], help='图片目录（可重复）')
    ap.add_argument('--format', default=None, help='图片引擎的版式参数')
    ap.add_argument('--width', type=int, default=None)
    ap.add_argument('--top-pad', dest='top_pad', type=int, default=None, help='长图顶部留白')
    ap.add_argument('--dpi', type=int, default=None)
    ap.add_argument('--no-crop', dest='no_crop', action='store_true')
    ap.add_argument('--cards', help='拆卡引擎的 cards.json 路径（--type tile-*）')
    ap.add_argument('--outdir', help='拆卡引擎的输出目录（--type tile-*）')
    ap.add_argument('--only', help='拆卡引擎：只渲染指定卡 id（逗号分隔）')
    ap.add_argument('--check-only', dest='check_only', action='store_true',
                    help='拆卡引擎：只校验既有产物')
    ap.add_argument('--dry-run', action='store_true', help='只打印将要执行的命令')
    args = ap.parse_args()

    mapping = load_mapping(args.config)

    if args.list or not args.type:
        print(json.dumps({'renderers': {k: v['script'] for k, v in mapping.items()},
                          'tile_types': TILE_TYPES,
                          'push_types': PUSH_TYPES}, ensure_ascii=False, indent=2))
        return 0

    # 「资料拆卡」引擎：参数是 --cards/--outdir（不是 payload/out），在这里单独分流
    if args.type in TILE_TYPES:
        ratio = TILE_TYPES[args.type]
        if not args.cards or not args.outdir:
            print(json.dumps({'ok': False, 'error': '--cards 与 --outdir 是 --type %s 的必填参数'
                              % args.type}, ensure_ascii=False))
            return 1
        cmd = [sys.executable, os.path.join(SKILL_DIR, 'gen_card_tile.py'),
               '--cards', args.cards, '--outdir', args.outdir, '--ratio', ratio]
        if args.dpi:
            cmd += ['--dpi', str(args.dpi)]
        if args.only:
            cmd += ['--only', args.only]
        if args.check_only:
            cmd += ['--check-only']
        if args.dry_run:
            print(json.dumps({'ok': True, 'dry_run': True, 'cmd': cmd}, ensure_ascii=False))
            return 0
        return subprocess.call(cmd, cwd=SKILL_DIR)

    if args.type in PUSH_TYPES:
        print(json.dumps({'ok': False, 'error': '%s 属于推送层：%s'
                          % (args.type, PUSH_TYPES[args.type])}, ensure_ascii=False))
        return 1

    if args.type not in mapping:
        print(json.dumps({'ok': False, 'error': 'unknown card type: %s（可用：%s）'
                          % (args.type, ', '.join(sorted(mapping)))}, ensure_ascii=False))
        return 1

    entry = mapping[args.type]
    script = os.path.join(SKILL_DIR, entry['script'])
    if not os.path.exists(script):
        print(json.dumps({'ok': False, 'error': 'engine not found: %s' % script}, ensure_ascii=False))
        return 1

    for req in ('payload', 'out'):
        if not getattr(args, req):
            print(json.dumps({'ok': False, 'error': '--%s is required for --type %s'
                              % (req, args.type)}, ensure_ascii=False))
            return 1

    cmd = build_cmd(entry['script'], entry['args'], args)
    if args.dry_run:
        print(json.dumps({'ok': True, 'dry_run': True, 'cmd': cmd}, ensure_ascii=False))
        return 0

    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              encoding='utf-8', errors='replace', cwd=SKILL_DIR, timeout=900)
    except subprocess.TimeoutExpired:
        print(json.dumps({'ok': False, 'error': 'engine timeout after 900s: %s' % script},
                         ensure_ascii=False))
        return 1
    out = (proc.stdout or '').strip()
    if out:
        print(out)
    if proc.returncode != 0 and (proc.stderr or '').strip():
        print(proc.stderr.strip(), file=sys.stderr)
    return proc.returncode


if __name__ == '__main__':
    sys.exit(main())
