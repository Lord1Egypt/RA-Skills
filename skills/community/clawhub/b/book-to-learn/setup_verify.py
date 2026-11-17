#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""setup_verify.py — 环境体检 / 依赖自检

在不同机器上第一次使用本 skill 前，先跑这个：
    python setup_verify.py            # 人类可读报告 + 缺失项的安装建议
    python setup_verify.py --json     # 机器可读
    python setup_verify.py --selftest # 顺带跑渲染自检 tests/test_render_common.py

检查项：Python 版本 / 渲染依赖 / 光栅化通道 / CJK 字体 / 破折号兜底字体 /
抓取与提取依赖 / 可选依赖。缺失项按平台给出可直接执行的安装命令。
"""
import argparse
import json
import os
import platform
import subprocess
import sys
import shutil

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, SKILL_DIR)

REQUIRED = {
    'weasyprint': ('HTML → PDF 渲染核心', 'pip install weasyprint'),
    'PIL': ('图片处理', 'pip install pillow'),
}
RASTERIZER = {
    'pymupdf': ('PDF → PNG 光栅化（首选，纯 wheel，无需系统库）', 'pip install pymupdf'),
    'pdf2image': ('PDF → PNG 光栅化（需系统 poppler / pdftoppm）',
                  'pip install pdf2image  # 另需安装 poppler'),
}
OPTIONAL = {
    'numpy': '自适应高度测量 / 精确裁白（拆卡引擎（tile-*）必需；缺失时走 PIL 近似）',
    'bs4': '书籍 HTML 提取',
    'docx': 'DOCX 提取',
    'pypdf': 'PDF 文本提取',
    'pdfminer': 'PDF 文本提取（备选）',
    'ebooklib': 'EPUB 提取',
    'striprtf': 'RTF 提取',
}


def has(mod):
    import importlib.util
    try:
        return importlib.util.find_spec(mod) is not None
    except Exception:
        return False


def poppler_ok():
    from shutil import which
    return bool(which('pdftoppm'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()

    import render_common as rc
    rep = rc.runtime_report()

    missing_required, missing_rasterizer = [], []
    for m, (desc, hint) in REQUIRED.items():
        if not rep['deps'].get(m):
            missing_required.append({'mod': m, 'desc': desc, 'hint': hint})
    if not (rep['deps'].get('pymupdf') or rep['deps'].get('fitz')):
        if rep['deps'].get('pdf2image') and poppler_ok():
            pass
        else:
            missing_rasterizer.append({
                'mod': 'pymupdf（或 pdf2image+poppler）',
                'desc': 'PDF → PNG 光栅化（长图类卡片必需）',
                'hint': 'pip install pymupdf',
            })
    elif rep['deps'].get('pdf2image') and not poppler_ok():
        if not a.json:
            print('  - 提示: 已装 pdf2image 但系统缺 poppler（pdftoppm）；光栅化优先走 pymupdf，缺失时 PDF→PNG 不可用')

    report = {
        'python': rep['python'],
        'python_ok': sys.version_info >= (3, 8),
        'platform': rep['platform'],
        'cjk_fonts_found': rep['cjk_fonts_found'],
        'cjk_font_ok': bool(rep['cjk_fonts_found']),
        'dash_font': rep['dash_font'],
        'dash_fallback_ok': bool(rep['dash_font']),
        'rasterizer': rep['rasterizer_available'],
        'poppler': poppler_ok(),
        'missing_required': missing_required,
        'missing_rasterizer': missing_rasterizer,
        'optional_missing': [m for m in OPTIONAL if not has(m)],
        'ok': (sys.version_info >= (3, 8) and not missing_required and not missing_rasterizer),
    }

    # 「资料拆卡」引擎（tile-*）的额外体检：weasyprint + numpy + 光栅化 + 中文字体
    tile_missing = []
    if not rep['deps'].get('weasyprint'):
        tile_missing.append('weasyprint（HTML→PDF）')
    if not (rep['deps'].get('numpy') or has('numpy')):
        tile_missing.append('numpy（内容高度测量，pip install numpy）')
    if missing_rasterizer:
        tile_missing.append('PDF→PNG 光栅化通道（pip install pymupdf）')
    if not report['cjk_font_ok']:
        tile_missing.append('中文字体（Linux: apt-get install -y fonts-noto-cjk）')
    report['tile_ready'] = not tile_missing
    report['tile_missing'] = tile_missing

    if a.selftest:
        t = os.path.join(SKILL_DIR, 'tests', 'test_render_common.py')
        if os.path.exists(t):
            proc = subprocess.run([sys.executable, t, '--quick'], capture_output=True, text=True)
            report['selftest_exit'] = proc.returncode
            report['ok'] = report['ok'] and proc.returncode == 0

    if a.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
        sys.exit(0 if report['ok'] else 1)

    print('== book-to-learn 环境体检 ==')
    print('Python %s（%s）%s' % (report['python'], report['platform'],
                                'OK' if report['python_ok'] else '需要 >= 3.8'))
    print('渲染核心 weasyprint: %s' % ('OK' if rep['deps'].get('weasyprint') else '缺失'))
    print('光栅化通道: %s%s' % (report['rasterizer'] or '无',
                              '' if report['poppler'] else '（未检测到 poppler，若用 pdf2image 需装）'))
    print('CJK 字体: %s' % (', '.join(report['cjk_fonts_found']) or '未探测到（中文会显示为方块）'))
    print('破折号兜底字体: %s' % (report['dash_font'] or '未找到（破折号可能在某些阅读器显示异常）'))
    print('拆卡引擎 (tile-*): %s' % ('就绪' if report['tile_ready']
                                  else '缺：' + '、'.join(report['tile_missing'])))
    if report['missing_required'] or report['missing_rasterizer']:
        print('\n需要安装：')
        for m in report['missing_required'] + report['missing_rasterizer']:
            print('  - %s  ← %s' % (m['desc'], m['hint']))
    if report['optional_missing']:
        print('\n可选（缺失只影响对应格式/精度）：%s' % ', '.join(report['optional_missing']))
    if not report['cjk_font_ok']:
        print('\n提示：本机没有探测到中文字体。Linux 可 `apt-get install -y fonts-noto-cjk`，'
              'macOS/Windows 一般自带（PingFang / Microsoft YaHei）。')
    if report['ok'] and not report['tile_ready']:
        print('\n注意: 基础流程可用，但拆卡引擎（tile-*）尚缺：%s' % '、'.join(report['tile_missing']))
    if not shutil.which('node'):
        print('  - 提示: 未找到 node（仅 pushMethod=ima 需要）')
    if not shutil.which('curl'):
        print('  - 提示: 未找到 curl（仅 download-imgs/process_attachments 需要）')
    print('\n结论: %s' % ('可以开工' if report['ok'] else '还缺依赖，先按上面安装'))
    sys.exit(0 if report['ok'] else 1)


if __name__ == '__main__':
    main()
