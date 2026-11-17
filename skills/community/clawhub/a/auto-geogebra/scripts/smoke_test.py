#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""geogebra 双验证器 · 回归冒烟测试

一键复跑 L1（语法）/ L2（语义）两支验证器在下列场景的既有行为：

  1. 好样例 ×3     —— 期望 L1 ok=true 且 0 错 0 警；L2 0 语义错
  2. 埋错样例 ×1   —— 期望 L1 命中 3 errors + 3 warnings；L2 命中 3 errors
  3. stdin 管道    —— 带 UTF-8 BOM / GBK 字节流，期望零误报
  4. 文件编码边界  —— UTF-8+BOM / GBK(ANSI) 文件，期望不崩溃、正常验证
  5. 命名规则      —— 小写坐标名 / 保留名提示（v1.3）
  6. 使用顺序      —— 先使用后定义提示（v1.3）
  7. 退化构造预检  —— 零值滑块参与两点构造时的提示与抑制（v1.3.1）
  8. 内置常量名    —— e / pi 作对象名的提醒（v1.3.1）
  9. 按钮样例      —— 单参 Button 不误报；二参 Button 提示 button-script（v1.4）
 10. 嵌套迭代      —— Polygon(Sequence(…, k, …)) 不误报（v1.4a）
 11. 引擎命令      —— Random 识别（v1.4.2）

用法：
    python scripts/smoke_test.py        # 跑全部用例，输出 PASS/FAIL 与汇总
    python scripts/smoke_test.py -v     # 同时打印每个用例的原始输出

退出码：0 = 全部通过；1 = 存在失败。改动验证器后必须全绿，否则回刀。
"""
import json
import os
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PY = sys.executable
L1 = os.path.join(HERE, "validate_commands.py")
L2 = os.path.join(HERE, "validate_types.py")
VERBOSE = "-v" in sys.argv or "--verbose" in sys.argv

GOOD_CALC = r"""# 定积分矩形逼近演示——冒烟样例
f(x) = sin(x)
a = Slider(0, 3, 0.1)
b = Slider(0, 3, 0.1)
n = Slider(1, 50, 1)
sumRect = RectangleSum(f, a, b, n, 0.25)
realInt = Integral(f, a, b)
txt1 = Text("\sum_{k=1}^{n} f(x_k) \Delta x = " + sumRect, (3.6, 2), true, true)
txt2 = Text("实际积分值 = " + realInt, (3.6, 1.5), true, true)
SetColor(sumRect, 0.2, 0.6, 1)
SetColor(realInt, 1, 0.2, 0)
ShowLabel(sumRect, false)
"""

GOOD_LINALG = r"""# 线性变换动态演示——冒烟样例
a11 = Slider(-2, 2, 0.1)
a12 = Slider(-2, 2, 0.1)
a21 = Slider(-2, 2, 0.1)
a22 = Slider(-2, 2, 0.1)
M = {{a11, a12}, {a21, a22}}
polyUnit = Polygon((-1, -1), (1, -1), (1, 1), (-1, 1))
polyTrans = ApplyMatrix(M, polyUnit)
detVal = Determinant(M)
vec1 = Vector((0, 0), (a11, a12))
txtDet = Text("det = " + detVal, (3, 3), true, true)
SetColor(polyUnit, 0, 0, 1)
SetColor(polyTrans, 1, 0.4, 0)
ShowLabel(detVal, false)
ShowLabel(vec1, false)
"""

GOOD_MORE = r"""# 导数定义演示——冒烟样例（命名已按真机规则修正；含非零初值）
f(x) = x^3 - 3x + 1
a = Slider(-2, 2, 0.1)
h = Slider(-1, 1, 0.01)
SetValue(h, 0.5)
A = (a, f(a))
B = (a + h, f(a + h))
secant = Line(A, B)
tangentLn = Tangent(a, f)
mSec = Slope(secant)
mTan = Slope(tangentLn)
dTan = Derivative(f)
distAB = Distance(A, B)
txt = Text("割线斜率 = " + mSec, (3, 2), true, true)
"""

BAD_CASES = r"""# 埋错用例：覆盖 L1 与 L2 各类检查（期望全部命中）
f(x) = x^2
poly = Polygon((0, 0), (1, 0), (1, 1), (0, 1))
P = Point(f)
sl = Slope(P)
m3 = {{1, 2, 3}, {4, 5, 6}, {7, 8, 9}}
polyBad = ApplyMatrix(m3, poly)
rects = Sequence(Polygon((k, 0), (k + 0.5, 0), (k + 0.5, 1)), k, 0, 5)
total = Sum(rects)
txt = Text("第一行\n第二行", (1, 1))
SetColor(poly, 0, 0, 255)
s = Slider(5, 1, 0.1)
bad = 3 + (2
BadCommand(poly)
zzz = qqq + 1
"""

NAMING_CASES = r"""# 命名规则用例：小写坐标名 ×2 + 保留名 ×1（v1.3）
pt1 = (0, 0)
pt2 = (2, 4)
ln1 = Line(pt1, pt2)
sec = Line((0, 0), (1, 1))
"""

ORDER_CASES = r"""# 使用顺序用例：先使用、后定义（v1.3）
y1 = x1 + 1
x1 = 2
"""

DEGENERATE_CASES = r"""# 退化预检用例：零值范围滑块参与两点构造，未设非零初值（v1.3.1）
f(x) = x^2
a = Slider(-1, 1, 0.1)
h = Slider(-1, 1, 0.1)
A = (a, f(a))
B = (a + h, f(a + h))
secant = Line(A, B)
"""

DEGENERATE_FIXED_CASES = r"""# 退化预检用例：已 SetValue，非零初值（v1.3.1）
f(x) = x^2
a = Slider(-1, 1, 0.1)
h = Slider(-1, 1, 0.1)
SetValue(h, 0.5)
A = (a, f(a))
B = (a + h, f(a + h))
secant = Line(A, B)
"""

CONSTANT_CASES = r"""# 内置常量名用例：e / pi 作对象名（v1.3.1）
e = 5
pi = 3
"""

BUTTON_OK = r"""# 按钮样例：单参 Button（v1.4）
a = Slider(-1, 1, 0.1)
SetValue(a, 0.5)
btnReset = Button("重置")
"""

BUTTON_BAD = r"""# 按钮二参误写样例（v1.4）
a = Slider(-1, 1, 0.1)
btnBad = Button("二参", "SetValue(a, 1)")
"""

NESTED_ITER = r"""# 嵌套迭代用例：Sequence 内单字母变量（v1.4a）
nN = Slider(3, 60, 1)
polyN = Polygon(Sequence((cos(2 * pi * k / nN), sin(2 * pi * k / nN)), k, 1, nN))
"""

RANDOM_CASES = r"""# 引擎支持命令用例：Random（v1.4.2）
r0 = Random(0, 1)
"""

CHECKS = 0
FAILURES = []


def check(name, cond, detail=""):
    global CHECKS
    CHECKS += 1
    if cond:
        print("PASS  " + name)
    else:
        print("FAIL  " + name + (("  ->  " + detail) if detail else ""))
        FAILURES.append(name)


def rules_of(items):
    return sorted({it.get("rule") for it in items})


def run(script, args=None, stdin_bytes=None):
    cmd = [PY, script] + (list(args) if args else [])
    common = dict(stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=HERE)
    if stdin_bytes is None:
        proc = subprocess.run(cmd, stdin=subprocess.DEVNULL, **common)
    else:
        proc = subprocess.run(cmd, input=stdin_bytes, **common)
    out = proc.stdout.decode("utf-8", "replace")
    err = proc.stderr.decode("utf-8", "replace")
    if VERBOSE:
        sys.stdout.write("    raw: " + out.replace("\n", " ")[:240] + "\n")
        if err.strip():
            sys.stdout.write("    err: " + err.replace("\n", " ")[:240] + "\n")
    try:
        return json.loads(out)
    except Exception:
        return None


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    print("geogebra 双验证器 · 冒烟测试（脚本目录：%s）\n" % HERE)

    with tempfile.TemporaryDirectory(prefix="ggb-smoke-") as tmp:
        # ---------- 好样例 ×3 ----------
        for fname, content in (("good_calc.txt", GOOD_CALC),
                               ("good_linalg.txt", GOOD_LINALG),
                               ("good_more.txt", GOOD_MORE)):
            path = os.path.join(tmp, fname)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            rep = run(L1, [path])
            check("L1 好样例 %s：ok=true 且 0 错 0 警" % fname,
                  bool(rep) and rep.get("ok") is True
                  and not rep.get("errors") and not rep.get("warnings"),
                  json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")
            rep = run(L2, [path])
            check("L2 好样例 %s：0 语义错" % fname,
                  bool(rep) and rep.get("semanticErrors") == 0,
                  json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 埋错样例 ×1 ----------
        bad = os.path.join(tmp, "bad_cases.txt")
        with open(bad, "w", encoding="utf-8") as f:
            f.write(BAD_CASES)
        rep = run(L1, [bad])
        check("L1 埋错样例：3 errors + 3 warnings 且规则齐全",
              bool(rep) and rep.get("ok") is False
              and len(rep.get("errors", [])) == 3
              and len(rep.get("warnings", [])) == 3
              and set(rules_of(rep.get("errors", []))) ==
                  {"text-backslash-n", "slider-range", "unbalanced-parentheses"}
              and set(rules_of(rep.get("warnings", []))) ==
                  {"setcolor-range", "unknown-command", "undefined-variable"},
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")
        rep = run(L2, [bad])
        check("L2 埋错样例：3 语义错且规则齐全",
              bool(rep) and rep.get("semanticErrors") == 3
              and set(rules_of(rep.get("errors", []))) ==
                  {"arg-type", "matrix-dim", "numeric-list"},
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- stdin：UTF-8+BOM / GBK 字节流 ----------
        stdin_ascii = "a = Slider(-1, 1, 0.1)\ncircle = Circle((0, 0), a)\n"
        rep = run(L1, stdin_bytes=b"\xef\xbb\xbf" + stdin_ascii.encode("utf-8"))
        check("stdin 带 UTF-8 BOM：L1 ok=true 且零误报",
              bool(rep) and rep.get("ok") is True
              and not rep.get("errors") and not rep.get("warnings"),
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")
        stdin_gbk = "# 中文注释\na = Slider(-1, 1, 0.1)\ncircle = Circle((0, 0), a)\n"
        rep = run(L1, stdin_bytes=stdin_gbk.encode("gb18030"))
        check("stdin 为 GBK 字节流（含中文）：L1 ok=true 且零误报",
              bool(rep) and rep.get("ok") is True
              and not rep.get("errors") and not rep.get("warnings"),
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 文件编码边界 ----------
        gbk_path = os.path.join(tmp, "gbk_file.txt")
        with open(gbk_path, "wb") as f:
            f.write("# 定积分演示\nf(x) = x^2\na = Slider(-1, 1, 0.1)\n".encode("gb18030"))
        rep = run(L1, [gbk_path])
        check("GBK(ANSI) 文件：L1 不崩溃且 ok=true",
              bool(rep) and rep.get("ok") is True,
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")
        rep = run(L2, [gbk_path])
        check("GBK(ANSI) 文件：L2 不崩溃且 0 语义错",
              bool(rep) and rep.get("semanticErrors") == 0,
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")
        bom_path = os.path.join(tmp, "bom_file.txt")
        with open(bom_path, "wb") as f:
            f.write(b"\xef\xbb\xbf" + "# BOM 样例\na = Slider(-1, 1, 0.1)\n".encode("utf-8"))
        rep = run(L1, [bom_path])
        check("UTF-8+BOM 文件：L1 ok=true 且零误报",
              bool(rep) and rep.get("ok") is True and not rep.get("warnings"),
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 命名规则（v1.3） ----------
        naming = os.path.join(tmp, "naming_rules.txt")
        with open(naming, "w", encoding="utf-8") as f:
            f.write(NAMING_CASES)
        rep = run(L1, [naming])
        check("L1 命名规则：小写坐标名 ×2 + 保留名 ×1 全部提示",
              bool(rep) and rep.get("ok") is True
              and len(rep.get("warnings", [])) == 3
              and set(rules_of(rep.get("warnings", []))) == {"lowercase-point", "reserved-name"},
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 使用顺序（v1.3） ----------
        order = os.path.join(tmp, "order_rules.txt")
        with open(order, "w", encoding="utf-8") as f:
            f.write(ORDER_CASES)
        rep = run(L1, [order])
        check("L1 顺序检查：使用早于定义时提示 use-before-define",
              bool(rep) and rep.get("ok") is True
              and len(rep.get("warnings", [])) == 1
              and rules_of(rep.get("warnings", [])) == ["use-before-define"],
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 退化构造预检（v1.3.1） ----------
        deg = os.path.join(tmp, "degenerate_hint.txt")
        with open(deg, "w", encoding="utf-8") as f:
            f.write(DEGENERATE_CASES)
        rep = run(L1, [deg])
        check("L1 退化预检：零值滑块参与两点构造 → 提示 degenerate-hint",
              bool(rep) and rep.get("ok") is True
              and len(rep.get("warnings", [])) == 1
              and rules_of(rep.get("warnings", [])) == ["degenerate-hint"],
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        deg2 = os.path.join(tmp, "degenerate_fixed.txt")
        with open(deg2, "w", encoding="utf-8") as f:
            f.write(DEGENERATE_FIXED_CASES)
        rep = run(L1, [deg2])
        check("L1 退化预检：已 SetValue 非零初值 → 不提示",
              bool(rep) and rep.get("ok") is True and not rep.get("warnings"),
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 内置常量名（v1.3.1） ----------
        cons = os.path.join(tmp, "constant_names.txt")
        with open(cons, "w", encoding="utf-8") as f:
            f.write(CONSTANT_CASES)
        rep = run(L1, [cons])
        check("L1 常量名提醒：e/pi 作对象名 → 2 条 reserved-constant",
              bool(rep) and rep.get("ok") is True
              and len(rep.get("warnings", [])) == 2
              and set(rules_of(rep.get("warnings", []))) == {"reserved-constant"},
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 按钮样例（v1.4） ----------
        bok = os.path.join(tmp, "button_ok.txt")
        with open(bok, "w", encoding="utf-8") as f:
            f.write(BUTTON_OK)
        rep1 = run(L1, [bok])
        rep2 = run(L2, [bok])
        check("按钮行（单参 Button）L1 ok 且 L2 0 错",
              bool(rep1) and rep1.get("ok") is True and not rep1.get("warnings")
              and bool(rep2) and rep2.get("semanticErrors") == 0,
              json.dumps([rep1, rep2], ensure_ascii=False)[:300])

        bbad = os.path.join(tmp, "button_bad.txt")
        with open(bbad, "w", encoding="utf-8") as f:
            f.write(BUTTON_BAD)
        rep = run(L2, [bbad])
        check("按钮二参误写 → L2 提示 button-script",
              bool(rep) and len(rep.get("errors", [])) == 1
              and rules_of(rep.get("errors", [])) == ["button-script"],
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 嵌套迭代豁免（v1.4a） ----------
        nested = os.path.join(tmp, "nested_iter.txt")
        with open(nested, "w", encoding="utf-8") as f:
            f.write(NESTED_ITER)
        rep = run(L1, [nested])
        check("L1 嵌套迭代豁免：Polygon(Sequence(…, k, …)) 不误报",
              bool(rep) and rep.get("ok") is True and not rep.get("warnings"),
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

        # ---------- 引擎命令识别（v1.4.2） ----------
        rnd = os.path.join(tmp, "random_cmd.txt")
        with open(rnd, "w", encoding="utf-8") as f:
            f.write(RANDOM_CASES)
        rep = run(L1, [rnd])
        check("L1 引擎命令识别：Random 不误报",
              bool(rep) and rep.get("ok") is True and not rep.get("warnings"),
              json.dumps(rep, ensure_ascii=False)[:300] if rep else "no JSON")

    print("\n----- 汇总 -----")
    print("共 %d 项检查，失败 %d 项" % (CHECKS, len(FAILURES)))
    if FAILURES:
        for name in FAILURES:
            print("  [FAIL] " + name)
        sys.exit(1)
    print("SMOKE OK：全部通过。")


if __name__ == "__main__":
    main()
