# -*- coding: utf-8 -*-
"""报告质量自检（G1+G2）—— 检查 AI 交的审图报告里「质量自证」是否齐全、数字是否合常理

用法:
    python report_check.py <报告文件.md> [--prev 上一轮的条目数]

识别报告里这一行（AI 必须提供）：
    【质量自证】应读=N 实读=M | Model=A Paper=B 文字=C 块=D 图层=E Xref=F | 总条数=G 零条目图纸=H 图纸数=I
"""
import os, re, sys, argparse

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument('report')
    ap.add_argument('--prev', type=float, default=None, help='上一轮 条目数÷图纸数（用于对比骤降）')
    return ap.parse_args()

def main():
    a = get_args()
    if not os.path.exists(a.report):
        print(f'❌ 报告文件不存在: {a.report}'); sys.exit(1)
    txt = open(a.report, encoding='utf-8', errors='ignore').read()

    print(f'报告: {os.path.basename(a.report)}  ({len(txt)} 字)\n')
    problems, warns = [], []

    # 1) 是否提供了「质量自证」行
    m = re.search(r'【质量自证】(.+)', txt)
    if not m:
        # 退一步：找 Markdown 表格形式的自证
        has_tbl = all(k in txt for k in ['实读', '六处' if '六处' in txt else 'Model', '总条数'])
        print('❌ 未找到【质量自证】行（G1/G2 未自证）')
        print('   报告必须包含一行：\n'
              '   【质量自证】应读=N 实读=M | Model=A Paper=B 文字=C 块=D 图层=E Xref=F | 总条数=G 零条目图纸=H 图纸数=I')
        if has_tbl:
            print('   （检测到疑似表格形式的自证，但格式不统一，无法自动核验 —— 请补上上面那一行）')
        sys.exit(2)

    line = m.group(1).strip()
    print(f'自证行: {line}\n')
    nums = {k: (int(v) if v.isdigit() else None)
            for k, v in re.findall(r'(应读|实读|Model|Paper|文字|块|图层|Xref|总条数|零条目图纸|图纸数)=(\d+)', line)}

    need = ['应读', '实读', 'Model', 'Paper', '文字', '块', '图层', 'Xref', '总条数', '零条目图纸', '图纸数']
    missing = [k for k in need if k not in nums]
    if missing:
        problems.append(f'自证行缺字段: {missing}')
    print('解析到的数字:')
    for k in need:
        print(f'   {k:8s} = {nums.get(k)}')

    # 2) G2 覆盖率：六处任何一处全 0
    print('\n— 覆盖率达检查 —')
    for k in ['Model', 'Paper', '文字', '块', '图层', 'Xref']:
        v = nums.get(k)
        if v == 0:
            problems.append(f'六处中「{k}」为 0 —— 大概率那处没读到（"读不到 ≠ 没有"）')
    if not any(nums.get(k) == 0 for k in ['Model', 'Paper', '文字', '块', '图层', 'Xref']):
        print('   六处均有数据 ✅' if not missing else '   六处字段不全，无法判定')

    # 3) 实读 vs 应读
    if nums.get('应读') and nums.get('实读') is not None:
        if nums['实读'] < nums['应读']:
            warns.append(f'实读 {nums["实读"]} < 应读 {nums["应读"]} —— 少读的必须在报告里逐个写原因')

    # 4) G1 条目数合理性
    print('\n— 条目数合理性检查 —')
    G, H, I = nums.get('总条数'), nums.get('零条目图纸'), nums.get('图纸数')
    if I and H is not None:
        ratio0 = H / I
        print(f'   零条目图纸占比 = {H}/{I} = {ratio0:.0%}')
        if ratio0 > 0.70:
            problems.append(f'零条目图纸占比 {ratio0:.0%} > 70% —— 大概率没真读进去')
    if G is not None and I:
        per = G / I
        print(f'   条目数÷图纸数 = {G}/{I} = {per:.2f} 条/份')
        if G < 10 and I >= 50:
            problems.append(f'共 {I} 份图只审出 {G} 条 —— 大概率只看了封面/目录')
        if a.prev:
            if per < a.prev * 0.5:
                problems.append(f'条目数÷图纸数 由上轮 {a.prev:.2f} 降到 {per:.2f}（跌超一半）—— 必须解释')
            else:
                print(f'   与上轮 {a.prev:.2f} 相比: 正常')

    # 5) 结论
    print('\n=== 结论 ===')
    if problems:
        print('❌ 不通过：')
        for p in problems: print(f'   · {p}')
    else:
        print('✅ 通过（数字齐、覆盖率达、条目数合常理）')
    if warns:
        print('⚠️ 提示：')
        for w in warns: print(f'   · {w}')
    sys.exit(1 if problems else 0)

if __name__ == '__main__':
    main()
