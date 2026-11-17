#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoGebra 指令「语义（类型）」验证器

与 `validate_commands.py`（语法验证）配套，组成指令生成的「双验证」：

    python scripts/validate_commands.py <指令文件>   # L1 语法：括号/颜色/换行/拼写/未定义变量
    python scripts/validate_types.py    <指令文件>   # L2 语义：参数类型/矩阵维度/数值列表

本脚本补 validate_commands.py 的盲区：后者只查语法，对「参数类型不匹配」「维度不匹配」
这类语义错误静态通过。本脚本用 data/commands-index.json 里的类型签名做参数类型推断与匹配。

核心设计：
  1. 类型名白名单 —— GeoGebra 文档签名里混着「参数名」（<Min>, <Start>, <Variable>），
     只有白名单内的词才是类型，其余视为参数名 = 不检查。
  2. 参数个数放宽 —— 允许省略尾部可选参数（如 Slider 只写 3 个）。
  3. Expression 只接纳数值表达式，不接纳几何对象（否则 Derivative(多边形) 会漏报）。
  4. 迭代命令（Sequence/Zip/…）的表达式位放宽 —— GeoGebra 允许对象表达式。

实测（2026-09-10）：5 处典型语义错误 5/5 检出；39 条正确指令 0 误报。
局限：仅静态推断，覆盖不到 GeoGebra 脚本（SetValue/StartAnimation/OnClick）、
     自定义工具、Locus 轨迹、依赖顺序敏感的构造 —— 这些必须实际执行验证。

用法：python validate_types.py <指令文件>   （无参数则从 stdin 读）
"""
import sys, os, json, re

HERE = os.path.dirname(os.path.abspath(__file__))
# 索引定位：按「同技能内 → 同工作区 → 各环境已安装位置」的顺序探测，取第一个存在的。
INDEX_CANDIDATES = [
    os.path.join(HERE, "..", "data", "commands-index.json"),                      # geogebra/scripts/
    os.path.join(HERE, "..", "geogebra", "data", "commands-index.json"),          # <workspace>/tools/
    os.path.join(HERE, "..", "..", "geogebra", "data", "commands-index.json"),    # <workspace>/x/scripts/
    os.path.expanduser("~/.workbuddy/skills/auto-geogebra/data/commands-index.json"),
    os.path.expanduser("~/.config/opencode/skills/auto-geogebra/data/commands-index.json"),
    os.path.expanduser("~/.openclaw-autoclaw/skills/auto-geogebra/data/commands-index.json"),
]


def read_text_smart(path=None):
    """读取指令文本：剥 BOM 字节 → utf-8 优先 → 回退 gb18030；无路径则读 stdin。"""
    raw = open(path, "rb").read() if path else sys.stdin.buffer.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("gb18030", errors="replace")


# ---------- 真正的 GeoGebra 类型词（其余 <...> 一律视作参数名，不检查） ----------
TYPE_WORDS = {
    'Object', 'Point', 'Line', 'Segment', 'Ray', 'Vector', 'Polygon', 'Conic',
    'Circle', 'Ellipse', 'Hyperbola', 'Parabola', 'Quadric', 'Surface', 'Plane',
    'Curve', 'Implicit', 'Spline', 'Function', 'Expression', 'Equation',
    'Polynomial', 'Number', 'Numeric', 'Integer', 'Complex', 'Boolean', 'Text',
    'Matrix', 'List', 'Interval', 'Locus', 'Angle', 'Region', 'Image', 'File',
}

# ---------- 命令 → 返回类型（高频；未列出即 Unknown，不下判断） ----------
RET = {
    'Slider': 'Number', 'InputBox': 'Object', 'Checkbox': 'Boolean',
    'Point': 'Point', 'Intersect': 'Point', 'Midpoint': 'Point', 'Centroid': 'Point',
    'Root': 'Point', 'Extremum': 'Point', 'InflectionPoint': 'Point',
    'Center': 'Point', 'Vertex': 'Point', 'Focus': 'Point', 'Corner': 'Point',
    'Line': 'Line', 'Segment': 'Line', 'Ray': 'Line', 'Vector': 'Vector',
    'Tangent': 'Line', 'PerpendicularLine': 'Line', 'PerpendicularBisector': 'Line',
    'AngleBisector': 'Line', 'PolyLine': 'Line', 'FitLine': 'Line',
    'Polygon': 'Polygon', 'Circle': 'Conic', 'Ellipse': 'Conic', 'Conic': 'Conic',
    'Hyperbola': 'Conic', 'Parabola': 'Conic', 'CircularArc': 'Conic',
    'CircularSector': 'Conic', 'ImplicitCurve': 'Conic', 'Semicircle': 'Conic',
    'Determinant': 'Number', 'Slope': 'Number', 'Area': 'Number', 'Length': 'Number',
    'Distance': 'Number', 'Angle': 'Number', 'Sum': 'Number', 'Product': 'Number',
    'Mean': 'Number', 'SD': 'Number', 'SampleSD': 'Number', 'Min': 'Number',
    'Max': 'Number', 'Median': 'Number', 'Variance': 'Number', 'Radius': 'Number',
    'Derivative': 'Function', 'Integral': 'Function', 'TaylorPolynomial': 'Function',
    'Text': 'Text', 'FractionText': 'Text', 'ScientificText': 'Text',
    'Sequence': 'List', 'Zip': 'List', 'KeepIf': 'List', 'Filter': 'List',
    'Sort': 'List', 'Unique': 'List', 'Union': 'List', 'Intersection': 'List',
}

# 返回「与第 N 个参数同类型」/「List<第 N 个参数的元素类型>」
SAME_AS_ARG = {'ApplyMatrix': 2, 'Reflect': 2, 'Rotate': 2, 'Translate': 2,
               'Dilate': 2, 'Stretch': 2, 'Shear': 2}
LIST_OF_ARG = {'Sequence': 1, 'Zip': 1, 'KeepIf': 1, 'Filter': 1}

# 语义上要求「数值列表」的命令（签名只写 <List>）
NUM_LIST_ARG = {'Sum': 0, 'Product': 0, 'Mean': 0, 'SD': 0, 'SampleSD': 0,
                'Min': 0, 'Max': 0, 'Median': 0, 'Variance': 0}

# 迭代命令的「表达式位」（第 N 个参数，1-based）：GeoGebra 允许对象表达式 → 不检查
FREE_ARG_POS = {'Sequence': 1, 'Zip': 1, 'KeepIf': 1, 'Filter': 1}

HIER = {
    'Point': {'Object'}, 'Line': {'Object'}, 'Segment': {'Object', 'Line'},
    'Ray': {'Object', 'Line'}, 'Vector': {'Object', 'Line'},
    'Polygon': {'Object'}, 'Conic': {'Object'}, 'Circle': {'Object', 'Conic'},
    'Number': {'Object'}, 'Boolean': {'Object', 'Number'}, 'Text': {'Object'},
    'Matrix': {'Object'}, 'List': {'Object'}, 'Polynomial': {'Object', 'Function'},
    'Function': {'Object', 'Expression'}, 'Expression': {'Object'},
    'Equation': {'Object'}, 'Angle': {'Object'}, 'Plane': {'Object'},
}
BUILTIN = {'pi': 'Number', 'e': 'Number', 'i': 'Number', 'true': 'Boolean',
           'false': 'Boolean', 'x': 'Number', 'y': 'Number', 'z': 'Number'}
# Expression 只接纳「数值表达式」，不接纳几何对象（否则 Derivative(多边形) 漏报）
EXPR_OK = {'Number', 'Boolean', 'Expression', 'Function', 'Unknown'}


def load_sigs():
    path = next((os.path.normpath(p) for p in INDEX_CANDIDATES if os.path.exists(os.path.normpath(p))), None)
    if not path:
        return {}
    data = json.load(open(path, encoding='utf-8'))
    out = {}
    for c in data.get('commands', []):
        name, sigs = c.get('name'), c.get('syntax') or []
        parsed = []
        for s in sigs:
            m = re.search(r'\((.*)\)', s, re.S)
            if not m:
                continue
            inner = re.sub(r'<xref:[^\[\]]*\[([^\]]*)\]>', r'<\1>', m.group(1))
            args = []
            for a in re.findall(r'<([^>]*)>', inner):
                w = re.split(r'[\s,]', a.strip())[0].strip()
                w = re.sub(r'\(s?\)$', '', w)          # Point(s) → Point
                w = w.strip('"')
                args.append(w if w in TYPE_WORDS else '*')   # 非类型词 → 参数名 → 不检查
            if not args:
                continue
            parsed.append({'args': args, 'star': ('...' in inner or '…' in inner)})
        if parsed:
            out[name] = parsed
    return out


def split_args(call):
    m = re.match(r'^([A-Za-z]\w*)\s*\((.*)\)\s*$', call, re.S)
    if not m:
        return None, []
    name, inner = m.group(1), m.group(2)
    args, depth, cur, instr = [], 0, '', False
    for ch in inner:
        if ch == '"':
            instr = not instr
        if not instr:
            if ch in '([{':
                depth += 1
            elif ch in ')]}':
                depth -= 1
            elif ch == ',' and depth == 0:
                args.append(cur); cur = ''; continue
        cur += ch
    if cur.strip():
        args.append(cur)
    return name, [a.strip() for a in args]


def infer(expr, env):
    """返回 (类型, 元素类型)。"""
    e = expr.strip()
    if not e:
        return 'Unknown', None
    if e.startswith('"') and e.endswith('"'):
        return 'Text', None
    if re.fullmatch(r'\{\{.*\}\}', e, re.S):
        return 'Matrix', len(re.findall(r'\{([^{}]*)\}', e))   # elem = 维度
    if e.startswith('{'):
        inner = e[1:-1] if e.endswith('}') else e[1:]
        return 'List', (infer(inner.split(',')[0], env)[0] if inner.strip() else 'Unknown')
    if re.fullmatch(r'\([^()]*,[^()]*\)', e) or re.fullmatch(r'\([^()]*,[^()]*,[^()]*\)', e):
        return 'Point', None
    if re.fullmatch(r'[-+]?\d*\.?\d+', e):
        return 'Number', None
    m = re.match(r'^([A-Za-z]\w*)\s*\(', e)
    if m:
        name = m.group(1)
        if name in SAME_AS_ARG:
            return infer_arg(e, SAME_AS_ARG[name], env)
        if name in LIST_OF_ARG:
            return 'List', infer_arg(e, LIST_OF_ARG[name], env)[0]
        if name in RET:
            t = RET[name]
            return (t, None) if t != 'List' else ('List', 'Unknown')
        return 'Unknown', None
    if e in BUILTIN:
        return BUILTIN[e], None
    if e in env:
        return env[e]
    return 'Unknown', None


def infer_arg(call, n, env):
    _, args = split_args(call)
    return infer(args[n - 1], env) if len(args) >= n else ('Unknown', None)


def accepts(actual, expected):
    if actual == 'Unknown' or expected in ('*', 'Object'):
        return True
    if actual == expected:
        return True
    if expected == 'Expression':
        return actual in EXPR_OK
    if expected == 'List':
        return actual in ('List',)
    return expected in HIER.get(actual, set())


def check(text):
    sigs = load_sigs()
    lines = [l.strip() for l in text.replace('\r\n', '\n').split('\n')
             if l.strip() and not l.strip().startswith(('#', '//'))]

    env = {}
    for line in lines:
        m = re.match(r'^([\w]+)\s*[:=]\s*(.+)$', line)
        if m and not re.match(r'^[\w]+\s*\(', line.split('=')[0].strip()):
            env[m.group(1)] = infer(m.group(2), env)
            continue
        m = re.match(r'^([\w]+)\s*\([^)]*\)\s*[:=]', line)
        if m:
            env[m.group(1)] = ('Function', None)

    errs = []
    for i, line in enumerate(lines, 1):
        rhs = line.split('=', 1)[1].strip() if '=' in line else line
        call = None
        m = re.match(r'^([A-Za-z]\w*)\s*\(', rhs)
        if m:
            seg = rhs
        else:
            mm = re.search(r'([A-Za-z]\w*)\s*\(', rhs)
            seg = rhs[mm.start():] if mm else None
        if seg:
            depth = 0
            for k, ch in enumerate(seg):
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0:
                        call = seg[:k + 1]
                        break
        if not call:
            continue
        name, args = split_args(call)
        if not name or name not in sigs:
            continue

        if name == 'Button':
            if len(args) >= 2:
                errs.append({'line': i, 'rule': 'button-script',
                             'message': 'Button 二参（带脚本）形式不受支持：本引擎经命令注入会静默失败（真机实测，按钮不会被创建）。请用 Button("标题") 创建，再用 tools/ggb-export/ggb_patch.py 注入脚本。',
                             'text': line})
            continue

        atypes = [infer(a, env) for a in args]
        free_pos = FREE_ARG_POS.get(name, 0)
        ok_any = False
        for sig in sigs[name]:
            exp = sig['args']
            if sig['star']:
                if len(atypes) < 2:
                    continue
                exps = [exp[0]] * len(atypes)
            else:
                if len(atypes) > len(exp):
                    continue          # 参数个数超出签名
                exps = exp[:len(atypes)]
            if all(accepts(a[0], e) for idx, (a, e) in enumerate(zip(atypes, exps), 1)
                   if idx != free_pos):
                ok_any = True
                break
        if not ok_any:
            exp_show = ' 或 '.join(
                '(' + ', '.join(s['args']) + (', …' if s['star'] else '') + ')'
                for s in sigs[name])
            act = ', '.join(a[0] for a in atypes)
            errs.append({'line': i, 'rule': 'arg-type',
                         'message': f'{name} 参数类型不匹配：实际 ({act})，签名要求 {exp_show}',
                         'text': line})

        pos = NUM_LIST_ARG.get(name)
        if pos is not None and pos < len(atypes):
            t, elem = atypes[pos]
            if t == 'List' and elem not in ('Number', 'Unknown'):
                errs.append({'line': i, 'rule': 'numeric-list',
                             'message': f'{name} 需要「数值列表」，实际是 List<{elem}>'
                                        f'（对几何对象列表求和是常见语义错误）', 'text': line})

        if name == 'ApplyMatrix' and len(args) >= 2:
            t1, dim = atypes[0]
            m0 = args[0].strip()
            if t1 == 'Matrix' and not dim and re.fullmatch(r'\{\{.*\}\}', m0, re.S):
                dim = len(re.findall(r'\{([^{}]*)\}', m0))
            t2 = atypes[1][0]
            if t1 == 'Matrix' and dim == 3 and t2 in ('Polygon', 'Point', 'Line',
                                                      'Vector', 'Conic', 'Segment'):
                errs.append({'line': i, 'rule': 'matrix-dim',
                             'message': f'ApplyMatrix 维度不匹配：矩阵 {dim}×{dim}（3D）'
                                        f'作用于 2D {t2}；2D 变换请用 2×2 矩阵',
                             'text': line})
    return errs


def main():
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    path = sys.argv[1] if len(sys.argv) > 1 else None
    text = read_text_smart(path).lstrip('\ufeff')
    errs = check(text)
    print(json.dumps({'semanticErrors': len(errs), 'errors': errs}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
