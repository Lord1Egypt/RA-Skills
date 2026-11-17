# -*- coding: utf-8 -*-
r"""生成器→看板 的「Python 常量名泄漏进 JS」静态 lint。

为什么需要它
------------
用 Python 生成 HTML 看板时，JS 只能通过注入的 `DATA.xxx` 或 JS 自己 `var` 的变量取值。
如果不小心把 **Python 侧的常量名**（如 `FACADE_IDX`、`MIN_NOFAC`）直接写进 JS 字符串，
语法检查（node --check）**查不出来**（它是合法标识符），只有在浏览器里跑到那一行才抛
`ReferenceError` —— 而这个 IIFE 之后的**全部渲染会被静默中断**：
表格空、图表不画、按钮无响应，页面却不报白屏，极难定位。

典型事故：`+'<td>'+fmt(DATA.r2[v].cats[FACADE_IDX],2)+'</td>'`
（Python 里有 `FACADE_IDX = 4`，JS 里的等价物是 `var FAC = DATA.facade_idx`）
→ 该行之后的「定标建议 / 评分表 / 评委打分 / 飞书记录」全部空白。

用法
----
    python lint_py_const_leak.py <生成器.py> <产物.html>
    # 退出码 0 = 无泄漏；1 = 有泄漏（不可交付）；2 = 用法错误

判定规则
--------
    1. 从生成器取所有「顶格的大写常量」定义名：`^([A-Z][A-Z0-9_]{2,})\s*=`
    2. 取产物里所有 `<script>` 块（跳过第 1 个，它通常是内联的 echarts 压缩包）
3. **先剥离 JS 注释**（`/* */` 与 `//`）——注释里出现常量名只是说明文字
4. 若某常量名以「完整标识符」形式（前后不是 `\\w` 或 `.`）出现在 JS 代码里，
   且该名字**不是** JS 自己 `var` 声明的同名变量 → 判定为泄漏
"""
import io
import os
import re
import sys


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 2
    py_path, html_path = sys.argv[1], sys.argv[2]
    for p in (py_path, html_path):
        if not os.path.exists(p):
            print('[lint] 文件不存在: %s' % p)
            return 2

    src = io.open(py_path, encoding='utf-8', errors='replace').read()
    html = io.open(html_path, encoding='utf-8', errors='replace').read()

    consts = set(re.findall(r'^([A-Z][A-Z0-9_]{2,})\s*=', src, re.M))
    blocks = re.findall(r'<script>(.*?)</script>', html, re.S)
    if not blocks:
        print('[lint] 产物中未找到 <script> 块')
        return 2
    # 第 1 个 script 通常是内联 echarts，跳过；其余为 DATA + app
    js = '\n'.join(blocks[1:]) if len(blocks) > 1 else blocks[0]

    # 剥离注释后再扫描
    code = re.sub(r'/\*.*?\*/', ' ', js, flags=re.S)
    code = re.sub(r'//[^\n]*', ' ', code)

    js_vars = set(re.findall(r'\bvar\s+([A-Za-z_$][\w$]*)', code))
    leaks = []
    for c in sorted(consts):
        if c in js_vars:
            continue
        hits = list(re.finditer(r'(?<![\w.])' + re.escape(c) + r'\b', code))
        if hits:
            leaks.append((c, hits))

    print('[lint] script 块 = %d（已跳过首个 echarts 块）｜生成器常量 = %d 个' % (len(blocks), len(consts)))
    if not leaks:
        print('[lint] ✅ 无 Python 常量泄漏（JS 只通过 DATA.* 取值）')
        return 0

    print('[lint] ❌ 发现 %d 个 Python 常量名泄漏进 JS —— 运行时必抛 ReferenceError，' % len(leaks))
    print('       且该 IIFE 之后的全部渲染会被静默中断：')
    for c, hits in leaks:
        print('  · %s（%d 处）' % (c, len(hits)))
        for m in hits[:4]:
            ctx = code[max(0, m.start() - 70):m.start() + 40].replace('\n', ' ')
            print('      … %s' % ctx)
    print('')
    print('  修法：改用 JS 侧已有变量或 DATA 字段，例如')
    print('    Python: FACADE_IDX = 4  →  DATA["facade_idx"]  →  JS: var FAC = DATA.facade_idx')
    return 1


if __name__ == '__main__':
    raise SystemExit(main())
