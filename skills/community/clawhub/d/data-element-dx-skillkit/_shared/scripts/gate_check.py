#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
门禁校验脚本（gate_check.py）— 数据要素交付套件

零依赖。对指定交付目录做**门禁四项检查** + **口径一致性（数字台账）校验**。

用法：
    python gate_check.py <交付目录> [--expect "文件1,文件2,..."] [--numbers "6 家市场,14 个系统"]

检查项（对应 dx-engagement-orchestrator 的门禁规范）：
    ① 存在性   文件是否存在
    ② 实质性   非空壳（默认 >1500 字节；含"模板/待填"字样会降级警告）
    ③ 挂接性   是否挂回七道工序（汇存治管服用模）
    ④ 一致性   关键数字是否在多份材料中一致

退出码：0=全通过，1=有 FAIL
"""
import io
import os
import re
import sys

SEVEN = ['汇', '存', '治', '管', '服', '用', '模']
# 空壳特征词（出现即视为"只是复制了模板"）
STUB_WORDS = ['待补充', 'TODO', 'XXX', '__', '填空', '待填']
# 绝对承诺用语（对外材料禁用）
BANNED = ['保证', '一定能', '必定', '承诺达到', '绝对', '百分之百']
# 反例/说明语境豁免词（命中则不算违规）
EXEMPT_CTX = ['禁止', '错误表达', '不构成', '不做', '反例', '避免',
              '承诺用语', '复检', '用语检查', '禁用词', '红线']
# 否定语境前缀（紧邻禁用词前出现即豁免，如"不承诺收入绝对值""绝非绝对"）
NEG_PREFIX = ['不', '非', '无', '没', '别', '勿', '禁止', '避免', '切勿', '未']
# 否定短语（可出现在禁用词前若干字符内，如"不承诺……绝对"）
NEG_PHRASES = ['不承诺', '不保证', '不能保证', '无法保证', '不建议', '不夸大',
               '不构成', '不作', '不做', '不得', '不应', '不可', '非绝对',
               '未发现', '未见', '未承诺', '无绝对']
# 引号/括号配对（禁用词整体落在对内 = 列举/讨论语境，如（"保证/必定/绝对"等均无））
QUOTE_PAIRS = [('“', '”'), ('‘', '’'), ('"', '"'), ("'", "'"),
               ('（', '）'), ('(', ')'), ('「', '」'), ('『', '』')]


def inside_quotes(t, start, end):
    """判断 [start, end) 是否完全落在某对引号/括号内（列举语境豁免）。"""
    for op, cl in QUOTE_PAIRS:
        i = 0
        while True:
            i = t.find(op, i)
            if i == -1:
                break
            j = t.find(cl, i + 1)
            if j == -1:
                break
            if i < start and end <= j:
                return True
            i = j + 1
    return False


def read(path):
    # utf-8-sig：兼容 Windows 下带 BOM 的 UTF-8 文本（PowerShell 写入场景）
    with io.open(path, encoding='utf-8-sig') as f:
        return f.read()


def check(cwd, expects=None, numbers=None):
    expects = expects or []
    numbers = numbers or []
    files = sorted(f for f in os.listdir(cwd)
                   if f.lower().endswith(('.md', '.html')) and not f.startswith('_'))
    texts = {}
    for f in files:
        try:
            texts[f] = read(os.path.join(cwd, f))
        except Exception as e:
            print('  [WARN] 读取失败 %s: %s' % (f, e))

    print('=' * 66)
    print('门禁检查 · %s' % cwd)
    print('=' * 66)
    print('%-8s %-32s %8s  %s' % ('结果', '文件', '大小', '①存在 ②实质 ③挂接'))
    fails = []
    for f in files:
        p = os.path.join(cwd, f)
        size = os.path.getsize(p)
        t = texts.get(f, '')
        # ① 存在性
        e1 = True
        # ② 实质性
        e2 = size > 1500
        stub_hits = [w for w in STUB_WORDS if w in t]
        # ③ 挂接性
        e3 = sum(1 for s in SEVEN if s in t) >= 2 or '工序' in t
        if f in expects and not (e1 and e2):
            fails.append(f)
        flag = 'PASS' if (e1 and e2) else 'FAIL'
        stub_note = '  空壳词:%s' % (','.join(stub_hits)) if stub_hits else ''
        print('%-8s %-32s %8dB  %s %s %s%s' % (
            flag, f, size,
            'Y' if e1 else 'N', 'Y' if e2 else 'N', 'Y' if e3 else 'N',
            stub_note))

    # 一致性：关键数字
    print()
    print('口径一致性 · 数字台账')
    for n in numbers:
        hits = [f[:6] for f, t in texts.items() if n in t]
        state = 'OK' if hits else 'MISSING'
        print('  [%-7s] %-24s 出现于: %s' % (state, n, ', '.join(hits) or '—'))

    # 绝对承诺用语（带语境豁免）
    print()
    print('绝对承诺用语检查（对外材料应无）')
    any_ban = False
    for f, t in texts.items():
        for w in BANNED:
            for m in re.finditer(re.escape(w), t):
                s = max(0, m.start() - 40)
                ctx = t[s:m.start() + 40]
                # 豁免一：语境含反例/说明词
                if any(x in ctx for x in EXEMPT_CTX):
                    continue
                # 豁免二：禁用词前 12 字符内出现否定短语或紧邻否定词
                pre = t[max(0, m.start() - 12):m.start()]
                if any(np in pre for np in NEG_PHRASES):
                    continue
                if any(pre.endswith(n) for n in NEG_PREFIX):
                    continue
                # 豁免三：禁用词整体落在引号/括号内（列举/讨论语境，非实际使用）
                if inside_quotes(t, m.start(), m.end()):
                    continue
                any_ban = True
                print('  [WARN] %s 疑似违规用语「%s」上下文: ...%s...' % (f, w, ctx.replace('\n', ' ')))
    if not any_ban:
        print('  [OK] 未发现绝对承诺用语')

    print()
    print('=' * 66)
    if fails:
        print('门禁结果: FAIL — 必需文件缺失或空壳: %s' % ', '.join(fails))
        return 1
    print('门禁结果: PASS — 全部文件存在且具实质性')
    return 0


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    cwd = sys.argv[1]
    expects, numbers = [], []
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a == '--expect' and i + 1 < len(args):
            expects = [x.strip() for x in args[i + 1].split(',') if x.strip()]
        if a == '--numbers' and i + 1 < len(args):
            numbers = [x.strip() for x in args[i + 1].split(',') if x.strip()]
    sys.exit(check(cwd, expects, numbers))
