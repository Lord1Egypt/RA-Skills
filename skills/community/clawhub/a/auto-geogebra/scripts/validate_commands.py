#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GeoGebra 指令静态验证脚本（Claude Code 版）

移植自 aardio autos.skills.geogebra 的 validateCommands 逻辑。

用法：
    python validate_commands.py <文件路径>
    echo "a = Slider(-3,3,0.1)" | python validate_commands.py

输出：JSON 报告，含 ok / errors / warnings / info 字段。
"""
import sys
import os
import json
import re

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# 索引定位：按「同技能内 → 同工作区 → 各环境已安装位置」顺序探测，取第一个存在的
INDEX_CANDIDATES = [
    os.path.join(SCRIPT_DIR, "..", "data", "commands-index.json"),
    os.path.join(SCRIPT_DIR, "..", "geogebra", "data", "commands-index.json"),
    os.path.join(SCRIPT_DIR, "..", "..", "geogebra", "data", "commands-index.json"),
    os.path.expanduser("~/.workbuddy/skills/auto-geogebra/data/commands-index.json"),
    os.path.expanduser("~/.config/opencode/skills/auto-geogebra/data/commands-index.json"),
    os.path.expanduser("~/.openclaw-autoclaw/skills/auto-geogebra/data/commands-index.json"),
]


def read_text_smart(path=None):
    """读取指令文本：剥 BOM 字节 → utf-8 优先 → 回退 gb18030；无路径则读 stdin。

    Windows 场景：管道或文件常带 UTF-8 BOM，而 stdin 默认解码可能是 GBK，
    直接把 BOM 按本地编码解码会吞成汉字并吃掉后一个字符，产生假「未定义变量」；
    记事本另存为 ANSI（GBK/GB18030）的文件也会直接崩溃。此处统一兜底。
    """
    raw = open(path, "rb").read() if path else sys.stdin.buffer.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("gb18030", errors="replace")

# 旧名/常见误写 → 正确命令名的别名映射（与 zh-command-aliases.json 命名口径一致）
COMMAND_ALIASES = {
    "CurveCartesian": "Curve",
    "Mirror": "Reflect",
    "StudentT": "TDistribution",
    "TaylorSeries": "TaylorPolynomial",
    "FitLineY": "FitLine",
    "StandardDeviation": "SD",
    "SampleStandardDeviation": "SampleSD",
    "CircleArc": "CircularArc",
    "CircleSector": "CircularSector",
    "Textfield": "InputBox",
}

# 以 \n 开头的已知 LaTeX 命令：用于区分「误写的换行」与合法 LaTeX 指令（如 \nu、\neq）
LATEX_N_COMMANDS = (
    "newline", "nonumber", "notag", "nolinebreak", "nopagebreak",
    "nu", "neq", "nabla", "notin", "neg", "nmid",
    "nsubseteq", "nsupseteq", "nleq", "ngeq", "nless", "ngtr",
    "napprox", "nequiv", "nexists", "nparallel", "nvdash", "nvDash",
    "natural", "nearrow", "nwarrow", "not", "nolimits",
)

# GeoGebra 常见英文色名（SetColor 字符串形式仅做白名单提醒，不作硬错误）
GGB_BASIC_COLORS = {
    "black", "white", "red", "green", "blue", "cyan", "magenta", "yellow",
    "gray", "grey", "lightgray", "darkgray", "orange", "brown", "pink",
    "purple", "violet", "darkgreen", "darkblue", "darkred", "crimson",
    "turquoise",
}

# 内置对象/常量/函数名（未定义变量检查的豁免名单）
# 注意：函数名必须列入——否则 `g(x) = sin(x)` 会把 sin 误报为「使用前未定义的变量」。
# 这份表覆盖 GeoGebra 英文版全部常用内置函数；若用到表中没有的函数，
# 会退回 warning（不阻断），按提示核对即可。
BUILTIN_FUNCTIONS = {
    # 三角
    "sin", "cos", "tan", "cot", "sec", "csc",
    # 反三角
    "asin", "acos", "atan", "acot", "asec", "acsc", "atan2",
    # 双曲
    "sinh", "cosh", "tanh", "coth", "sech", "csch",
    # 反双曲
    "asinh", "acosh", "atanh", "acoth",
    # 指数与对数
    "exp", "ln", "log", "lg", "ld",
    # 幂与根
    "sqrt", "cbrt", "nroot",
    # 取整与符号
    "abs", "sgn", "sign", "floor", "ceil", "round", "fract",
    # 随机
    "random", "randomNormal",
    # 复数与角度
    "real", "imaginary", "conjugate", "arg", "deg", "rad",
    # 特殊函数
    "gamma", "beta", "erf", "erfc",
    # 既可作为函数也可作为命令的关键字
    "min", "max", "mod", "gcd", "lcm", "if",
}

BUILTIN_WORDS = {
    "pi", "e", "i", "x", "y", "z", "true", "false", "undefined",
    "xAxis", "yAxis", "zAxis", "xOyPlane",
} | BUILTIN_FUNCTIONS

# 迭代型命令：行内的单字母标识符几乎都是循环变量，豁免未定义检查
ITERATOR_CMDS = {"Sequence", "Sum", "Product", "Zip", "KeepIf", "Filter", "Sort", "CountIf"}


def load_command_index():
    """加载 GeoGebra 指令索引（不强制）。"""
    path = next((os.path.normpath(p) for p in INDEX_CANDIDATES
                 if os.path.exists(os.path.normpath(p))), None)
    if not path:
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    except Exception:
        return None


def normalize_commands(text):
    """将输入文本规范化为非空、非注释的行数组。

    GeoGebra 指令脚本用 `//` 或 `#` 写注释（真实输出以 `#` 为主），
    两种都必须跳过——否则注释里的数学符号（如 \\lim_、f1）会被当作
    命令/变量引用扫描，产生"未定义变量"假警告。
    """
    lines = []
    for raw in text.replace("\r\n", "\n").split("\n"):
        t = raw.strip()
        if t and not t.startswith("//") and not t.startswith("#"):
            lines.append(t)
    return lines


def levenshtein(s1, s2):
    """编辑距离（用于拼写检查）。"""
    if len(s1) == 0:
        return len(s2)
    if len(s2) == 0:
        return len(s1)
    prev = list(range(len(s2) + 1))
    for i, c1 in enumerate(s1, 1):
        cur = [i]
        for j, c2 in enumerate(s2, 1):
            cur.append(min(
                prev[j] + 1,
                cur[j - 1] + 1,
                prev[j - 1] + (c1 != c2)
            ))
        prev = cur
    return prev[-1]


def validate_commands(text):
    """静态验证 GeoGebra 指令脚本。

    检查：括号配对、SetColor 颜色范围、Text() 换行、Slider 参数、
    未知命令、未定义变量引用、命名规则（保留名 / 小写坐标名 / 内置常量名）、使用顺序与退化构造预检。返回 dict。
    """
    result = {
        "ok": True,
        "lineCount": 0,
        "errors": [],
        "warnings": [],
        "info": [],
        "checkedCommands": [],
    }

    lines = normalize_commands(text)
    result["lineCount"] = len(lines)

    cmd_index = load_command_index()
    cmd_names = None
    if cmd_index and isinstance(cmd_index.get("commands"), list):
        cmd_names = [c.get("name") for c in cmd_index["commands"] if isinstance(c, dict)]

    # 引擎支持但手册未单页收录的命令（真机实测，v1.4.2；Random 即 RandomBetween 系列简写）
    if cmd_names is not None:
        for _extra in ("Random",):
            if _extra not in cmd_names:
                cmd_names = cmd_names + [_extra]

    # 第一遍：解析变量定义（含 f(x)=… 函数定义形式；记录“首次”定义行号，供顺序检查用）
    defined_vars = {}
    for i, line in enumerate(lines, 1):
        m = re.match(r"^([\w_]+)\s*[:=]", line)
        if m:
            defined_vars.setdefault(m.group(1), i)
            continue
        m_fn = re.match(r"^([\w_]+)\s*\([^)]*\)\s*[:=]", line)
        if m_fn:
            defined_vars.setdefault(m_fn.group(1), i)

    # 退化预检用：范围含 0 的滑块、SetValue 固定为非零的滑块、点坐标定义表达式
    zero_sliders = set()
    fixed_sliders = set()
    coord_defs = {}
    for line in lines:
        m_sl = re.match(r"^([\w_]+)\s*=\s*Slider\(\s*([-\d.]+)\s*,\s*([-\d.]+)\s*,", line)
        if m_sl:
            try:
                if float(m_sl.group(2)) <= 0 <= float(m_sl.group(3)):
                    zero_sliders.add(m_sl.group(1))
            except ValueError:
                pass
            continue
        m_sv = re.match(r"^SetValue\(\s*([\w_]+)\s*,\s*([-\d.]+)\s*\)\s*$", line)
        if m_sv:
            try:
                if abs(float(m_sv.group(2))) > 1e-12:
                    fixed_sliders.add(m_sv.group(1))
            except ValueError:
                pass
            continue
        m_cd = re.match(r"^([A-Za-z_]\w*)\s*=\s*(\(.*\))\s*$", line)
        if m_cd:
            coord_defs[m_cd.group(1)] = m_cd.group(2).strip()

    # 第二遍：逐行检查
    for i, line in enumerate(lines, 1):
        # 1. 括号配对
        for ch_open, ch_close, name in (("(", ")", "()"), ("[", "]", "[]")):
            bal = line.count(ch_open) - line.count(ch_close)
            if bal != 0:
                msg = f"括号 {name} 不配对"
                if bal > 0:
                    msg += f"：多 {bal} 个 '{ch_open}'"
                else:
                    msg += f"：多 {-bal} 个 '{ch_close}'"
                result["errors"].append({"line": i, "severity": "error", "rule": "unbalanced-" + ("parentheses" if name == "()" else "brackets"), "message": msg, "text": line})
                result["ok"] = False

        # 2. 提取命令名
        cmd_name = None
        m = re.match(r"^([A-Z][\w]*)\s*\(", line)
        if m:
            cmd_name = m.group(1)
        else:
            m = re.match(r"^[\w_]+\s*=\s*([A-Z][\w]*)\s*\(", line)
            if m:
                cmd_name = m.group(1)
        if cmd_name:
            result["checkedCommands"].append({"line": i, "name": cmd_name})

        # 2.5 命名规则提醒（v1.3，来自真机实测：这两类命名会在导出时静默翻车）
        m_def = re.match(r"^([\w_]+)\s*(?:\([^)]*\))?\s*[:=]", line)
        if m_def and m_def.group(1) in BUILTIN_FUNCTIONS:
            _n = m_def.group(1)
            result["warnings"].append({
                "line": i, "severity": "warning", "rule": "reserved-name",
                "message": f"对象名 '{_n}' 与 GeoGebra 内置函数同名：引擎会自动改名为 {_n}_{{1}}，之后按原名引用会失败（真机实测）。建议改名，如 '{_n}Line'。",
                "text": line,
            })
        m_lc = re.match(r"^([a-z][\w]*)\s*=\s*\([^()]*,[^()]*\)\s*$", line)
        if m_lc:
            result["warnings"].append({
                "line": i, "severity": "warning", "rule": "lowercase-point",
                "message": f"'{m_lc.group(1)}' 以小写开头且定义了坐标对：该引擎会将其创建为「向量」而非「点」（真机实测）。如需要点请改用大写开头名或 Point(...)；若本意就是向量可忽略。",
                "text": line,
            })

        _const_notes = {
            "e": "真机实测：引擎会直接创建同名数值对象、遮蔽内置常量",
            "pi": "真机实测：引擎会把该行解析为方程对象（而非数值对象）",
            "π": "真机实测：同 pi，会被解析为方程对象",
        }
        if m_def and m_def.group(1) in _const_notes:
            _cn = m_def.group(1)
            result["warnings"].append({
                "line": i, "severity": "warning", "rule": "reserved-constant",
                "message": f"对象名 '{_cn}' 与内置常量同名：{_const_notes[_cn]}，易造成引用歧义或并非预期对象。建议改名。",
                "text": line,
            })

        # 2.6 退化构造预检（启发式，v1.3.1）：单侧零值滑块代换重合检查
        m_two = re.match(r"^(?:[\w_]+\s*=\s*)?(Line|Segment|Ray|Vector)\s*[\(\[]\s*([\w_]+)\s*,\s*([\w_]+)\s*[\)\]]", line)
        if m_two:
            _p1, _p2 = m_two.group(2), m_two.group(3)
            if _p1 in coord_defs and _p2 in coord_defs:
                _e1, _e2 = coord_defs[_p1], coord_defs[_p2]
                _hint = None
                for _s in sorted(zero_sliders):
                    if _s in fixed_sliders:
                        continue
                    _in1 = re.search(r"\b" + re.escape(_s) + r"\b", _e1) is not None
                    _in2 = re.search(r"\b" + re.escape(_s) + r"\b", _e2) is not None
                    if _in1 == _in2:
                        continue
                    _single = _e1 if _in1 else _e2
                    _other = _e2 if _in1 else _e1
                    _sub = re.sub(r"\b" + re.escape(_s) + r"\b", "0", _single)
                    _sub = re.sub(r"\s*\+\s*0(?![\d.])", "", _sub)
                    _sub = re.sub(r"\s+", " ", _sub).strip()
                    if _sub == re.sub(r"\s+", " ", _other).strip():
                        _hint = _s
                        break
                if _hint:
                    result["warnings"].append({
                        "line": i, "severity": "warning", "rule": "degenerate-hint",
                        "message": f"退化预检：滑块 '{_hint}' 范围含 0（初始值为 0），将其代换为 0 后两点 {_p1}、{_p2} 重合，初始状态下 '{m_two.group(1)}' 可能因重合而静默不创建（真机实测）。建议先 SetValue({_hint}, 非零初值) 再构造。",
                        "text": line,
                    })

        # 3. SetColor 颜色范围检查 (0-1)
        if cmd_name == "SetColor":
            m = re.search(r"SetColor\s*\(([^,]+),\s*([\d.]+)\s*,\s*([\d.]+)\s*,\s*([\d.]+)\s*\)", line)
            if m:
                obj, r, g, b = m.group(1).strip(), float(m.group(2)), float(m.group(3)), float(m.group(4))
                if max(r, g, b) > 1:
                    sug = "SetColor({}, {:.2f}, {:.2f}, {:.2f})".format(
                        obj, min(r / 255, 1), min(g / 255, 1), min(b / 255, 1))
                    result["warnings"].append({
                        "line": i, "severity": "warning", "rule": "setcolor-range",
                        "message": f"SetColor RGB 值疑似使用 0-255 范围 ({r:.1f}, {g:.1f}, {b:.1f})。GeoGebra 脚本中 SetColor 使用 0-1 范围，大于 1 的值会被钳制，可能导致颜色错误。如：(0,0,255)→改用(0,0,1)",
                        "text": line, "suggestion": sug,
                    })

            # 字符串色名 / hex 形式：不在常见清单时给出提醒（静态无法确证拼写，仅 warning）
            m_str = re.search(r'SetColor\s*\(\s*[^,"()]+,\s*"([^"]*)"\s*\)', line)
            if m_str:
                cname = m_str.group(1).strip()
                low = cname.lower()
                if cname.startswith("#"):
                    hex_body = low.lstrip("#")
                    if not re.fullmatch(r"[0-9a-f]{3}|[0-9a-f]{6}", hex_body):
                        result["warnings"].append({
                            "line": i, "severity": "warning", "rule": "setcolor-name",
                            "message": f"SetColor 十六进制颜色 '{cname}' 格式可疑（应为 #RGB 或 #RRGGBB）。",
                            "text": line,
                        })
                elif low not in GGB_BASIC_COLORS:
                    result["warnings"].append({
                        "line": i, "severity": "warning", "rule": "setcolor-name",
                        "message": f"SetColor 颜色名 '{cname}' 不在常见色名清单中，静态验证无法确认；请人工核对拼写，或改用 0-1 范围的 RGB 数值形式。",
                        "text": line,
                    })

        # 4. Text() 中的 \n 检查
        #    \n 后跟字母时可能是合法 LaTeX 命令（\nu、\neq…），逐个提取
        #    \n 后缀，只有当 \n+后缀 构不成任何已知 LaTeX 命令时才报错。
        if cmd_name == "Text":
            m = re.search(r'Text\s*\(\s*"((?:[^"\\]|\\.)*)"', line)
            if m:
                str_arg = m.group(1)
                for mm in re.finditer(r"\\n([A-Za-z]*)", str_arg):
                    suffix = mm.group(1)
                    cand = "n" + suffix
                    is_latex_cmd = bool(suffix) and any(
                        c == cand or c.startswith(cand) for c in LATEX_N_COMMANDS
                    )
                    if not is_latex_cmd:
                        result["errors"].append({
                            "line": i, "severity": "error", "rule": "text-backslash-n",
                            "message": "Text() 不支持 \\n 换行！LaTeX 模式下应使用 \\\\ 换行。",
                            "text": line,
                        })
                        result["ok"] = False
                        break

        # 5. Slider 参数检查
        if cmd_name == "Slider":
            m = re.search(r"Slider\s*\(\s*([\d.-]+)\s*,\s*([\d.-]+)\s*,\s*([\d.]+)", line)
            if m:
                mn, mx, step = float(m.group(1)), float(m.group(2)), float(m.group(3))
                if mn >= mx:
                    result["errors"].append({
                        "line": i, "severity": "error", "rule": "slider-range",
                        "message": f"Slider 最小值 ({mn:g}) >= 最大值 ({mx:g})", "text": line,
                    })
                    result["ok"] = False
                if step <= 0:
                    result["errors"].append({
                        "line": i, "severity": "error", "rule": "slider-step",
                        "message": f"Slider 步长 ({step:g}) 必须大于 0", "text": line,
                    })
                    result["ok"] = False

        # 6. 未知命令检查
        if cmd_name and cmd_names:
            if cmd_name not in cmd_names:
                suggestions = []
                alias_target = COMMAND_ALIASES.get(cmd_name)
                if alias_target:
                    suggestions.append(alias_target)
                for name in cmd_names:
                    # 放宽相似度：长度比在 0.5~2 之间，且编辑距离不超过 max(2, 长度差+1)
                    len_ratio = len(cmd_name) / max(len(name), 1)
                    if 0.5 <= len_ratio <= 2.0:
                        dist = levenshtein(cmd_name.lower(), name.lower())
                        if dist <= max(2, abs(len(name) - len(cmd_name)) + 1):
                            suggestions.append(name)
                suggestions = sorted(set(suggestions), key=lambda s: levenshtein(cmd_name.lower(), s.lower()))
                result["warnings"].append({
                    "line": i, "severity": "warning", "rule": "unknown-command",
                    "message": f"命令 '{cmd_name}' 未在 GeoGebra 指令索引中找到。可能拼写有误。",
                    "text": line, "suggestions": suggestions[:5],
                })

        # 7. 未定义变量引用检查（对含命令调用的行同样生效）
        #    先剥离字符串与 LaTeX 记号再扫描标识符；已知命令名、内置常量、
        #    迭代型命令行上的单字母循环变量、本行定义均豁免。
        stripped_line = re.sub(r'"(?:[^"\\]|\\.)*"', "", line)
        stripped_line = re.sub(r"\\[a-zA-Z]+", " ", stripped_line)
        # 单字母迭代变量豁免：迭代命令出现在顶层或其嵌套调用中均可
        # （如 polyN = Polygon(Sequence(..., k, ...))）
        allow_single_letter = cmd_name in ITERATOR_CMDS or any(_it in line for _it in ITERATOR_CMDS)
        for var_name in re.findall(r"[A-Za-z][\w]*", stripped_line):
            if var_name in BUILTIN_WORDS:
                continue
            if cmd_name and var_name == cmd_name:
                continue  # 本行调用的命令名（未知命令已由规则 6 单独报告）
            if cmd_names and var_name in cmd_names:
                continue  # 已知命令名不算变量引用（修复：命令行此前被整体跳过）
            if var_name in COMMAND_ALIASES:
                continue  # 别名误写已由规则 6 单独提示
            if allow_single_letter and len(var_name) == 1:
                continue
            if var_name in defined_vars:
                if defined_vars[var_name] > i:
                    result["warnings"].append({
                        "line": i, "severity": "warning", "rule": "use-before-define",
                        "message": f"变量 '{var_name}' 在第 {i} 行使用，但首次定义在第 {defined_vars[var_name]} 行：请调整为先定义后使用。",
                        "text": line,
                    })
                    break
                continue
            if re.match(re.escape(var_name) + r"\s*(?:\([^)]*\))?\s*[:=]", stripped_line):
                continue  # 本行定义变量或函数（含 f(x)=… 形式）
            result["warnings"].append({
                "line": i, "severity": "warning", "rule": "undefined-variable",
                "message": f"变量 '{var_name}' 可能在第 {i} 行使用前未定义。", "text": line,
            })
            break  # 每行只报一个

    if not result["errors"] and not result["warnings"]:
        result["info"].append({"message": "✓ 未检测到常见错误。"})
    return result


def main():
    # Windows 下确保 stdout 使用 UTF-8，避免 GBK 编码错误
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if not os.path.exists(path):
            print(json.dumps({"ok": False, "errors": [{"rule": "file-not-found", "message": f"文件不存在：{path}"}], "warnings": [], "info": []}, ensure_ascii=False, indent=2))
            return
        text = read_text_smart(path)
    else:
        text = read_text_smart()

    # 双保险：无论文件还是 stdin，最后再剥一次 BOM 字符
    text = text.lstrip("\ufeff")

    report = validate_commands(text)
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
