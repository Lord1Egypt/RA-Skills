#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""使用反馈整理器（只读）

把一句碎片化的想法渲染成可直接复制发送的结构化反馈。
只读取技能包内文件，只向标准输出打印文本。
"""
import argparse, datetime as _dt, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KINDS = ['数据纠错', '可复现问题', '能力建议', '口味偏好', '其他', '待分级']


def skill_version():
    p = os.path.join(ROOT, 'SKILL.md')
    head = open(p, encoding='utf-8').read().split('---', 2)[1]
    m = re.search(r'^version:\s*([^\s]+)', head, re.M)
    return m.group(1) if m else '未知'


def channel():
    p = os.path.join(ROOT, 'FEEDBACK.md')
    s = open(p, encoding='utf-8').read()
    m = re.search(r'FEEDBACK_CHANNEL\s*=\s*(.+)', s)
    val = m.group(1).strip().strip('`').strip() if m else ''
    return '市场评论区（作者尚未填写 FEEDBACK_CHANNEL）' if val in ('待填写', '', 'TODO') else val


def main():
    p = argparse.ArgumentParser(
        description='把一句使用中的想法整理成可复制的反馈文本（只读、只打印）')
    p.add_argument('text', nargs='?', default='', help='一句话说清想法')
    p.add_argument('--kind', choices=KINDS, default='待分级', help='反馈类型')
    p.add_argument('--where', default='', help='涉及的功能/命令/店名/酒名')
    p.add_argument('--want', default='', help='原本期望')
    p.add_argument('--got', default='', help='实际给的结果')
    p.add_argument('--diff', default='', help='差在哪')
    p.add_argument('--suggest', default='', help='希望怎么改')
    p.add_argument('--name', default='匿名', help='署名')
    p.add_argument('--json', action='store_true', help='改为输出 JSON，便于本地留存')
    p.add_argument('--copy', action='store_true', help='只输出结构化文本行，便于一键复制粘贴')

    # --where 常填命令名（如 --idea / --map），以短横线开头会被当成选项，这里做等值拼接
    value_opts = {'--kind', '--where', '--want', '--got', '--diff', '--suggest', '--name'}
    argv, fixed, i = sys.argv[1:], [], 0
    while i < len(argv):
        if argv[i] in value_opts and i + 1 < len(argv) and argv[i + 1].startswith('-'):
            fixed.append(argv[i] + '=' + argv[i + 1])
            i += 2
        else:
            fixed.append(argv[i])
            i += 1
    a = p.parse_args(fixed)

    item = {
        '类型': a.kind,
        '版本': 'v' + skill_version(),
        '日期': str(_dt.date.today()),
        '场景': a.text.strip(),
        '期望': a.want.strip(),
        '实际': a.got.strip(),
        '差在哪': a.diff.strip(),
        '建议': a.suggest.strip() or '只是吐槽，没想好怎么改',
        '定位': a.where.strip() or '未指定',
        '署名': a.name.strip() or '匿名',
        '投递口': channel(),
    }

    if a.json:
        print(json.dumps(item, ensure_ascii=False, indent=2))
    elif a.copy:
        for k, v in item.items():
            if k == '投递口':
                continue
            print(f'【{k}】{v}')
    else:
        print('\n  ── 可直接复制发送的反馈 ──\n')
        for k, v in item.items():
            if k == '投递口':
                continue
            print(f'  【{k}】{v}')
        print(f'\n  → 投递到：{item["投递口"]}')
        if a.kind == '待分级' or not a.text.strip():
            print('  ⓘ 还没分级 / 没写具体想法：先确认这是「个人口味」还是「技能给错了」。')
        print('  ⓘ 本脚本只打印文本，不会保存，也不会替你发送。\n')
    return 0


if __name__ == '__main__':
    sys.exit(main())
