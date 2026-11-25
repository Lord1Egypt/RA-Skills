#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""claim-audit 自检：9 条用例，覆盖上对、对不上、验不了三种结论。

每条用例都在临时目录里造一个最小包，然后调用 scripts/audit.py，
断言它的输出与退出码。断言是真的比较，不是打印 PASS。
"""
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
PKG = os.path.dirname(HERE)
AUDIT = os.path.join(PKG, "scripts", "audit.py")

CASES = []


def case(fn):
    CASES.append(fn)
    return fn


def write(root, rel, text):
    p = os.path.join(root, rel)
    d = os.path.dirname(p)
    if d:
        os.makedirs(d, exist_ok=True)
    with io.open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    return p


RUNNER_OK = '''print("PASS T1")
print("PASS T2")
print("--- 2/2 PASS ---")
'''

RUNNER_SHORT = '''print("PASS T1")
print("--- 1/2 PASS ---")
'''


def run(args, cwd=None):
    p = subprocess.run([sys.executable, AUDIT] + args, capture_output=True,
                       text=True, encoding="utf-8", timeout=120, cwd=cwd)
    return p.returncode, (p.stdout or "") + (p.stderr or "")


@case
def g01_tests_claim_ok():
    """G01 声明的自检条数与实跑一致 → OK"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "自检：2/2 PASS\n")
        write(t, "tests/run_golden.py", RUNNER_OK)
        code, out = run(["check", t])
        assert code == 0, code
        assert "tests" in out and "OK" in out
        assert "对不上 0" in out


@case
def g02_tests_claim_mismatch():
    """G02 声明的 2/2 实际只有 1/2 → MISMATCH 且退出码 1"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "自检：2/2 PASS\n")
        write(t, "tests/run_golden.py", RUNNER_SHORT)
        code, out = run(["check", t])
        assert code == 1, code
        assert "MISMATCH" in out
        assert "1/2" in out


@case
def g03_files_claim_ok():
    """G03 文件数声明与真实文件数一致 → OK"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "全包共 3 个文件\n")
        write(t, "a.py", "print(1)\n")
        write(t, "b.md", "x\n")
        code, out = run(["check", t])
        assert code == 0, code
        assert "files" in out or "OK" in out


@case
def g04_files_claim_mismatch():
    """G04 文件数声明偏大 → MISMATCH"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "全包共 9 个文件\n")
        write(t, "a.py", "print(1)\n")
        code, out = run(["check", t])
        assert code == 1, code
        assert "MISMATCH" in out


@case
def g05_path_claim_missing():
    """G05 声明的 references/ 路径不存在 → MISMATCH"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "- 细则见 `references/rules.md`\n")
        code, out = run(["check", t])
        assert code == 1, code
        assert "不存在" in out


@case
def g06_prose_path_is_not_claim():
    """G06 正文举例里的路径不算声明 → 不产生 MISMATCH"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "一条结论写成 `scripts/review.py:157` 就能被核对。\n")
        code, out = run(["check", t])
        assert code == 0, code
        assert "MISMATCH" not in out


@case
def g07_no_runner_is_unverifiable():
    """G07 有自检声明但没有 runner → UNVERIFIABLE，默认不算失败"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "自检：9/9 PASS\n")
        code, out = run(["check", t])
        assert code == 0, code
        assert "UNVERIFIABLE" in out


@case
def g08_strict_turns_unverifiable_into_failure():
    """G08 加 --strict 后 UNVERIFIABLE 也算失败"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "自检：9/9 PASS\n")
        code, out = run(["check", t, "--strict"])
        assert code == 1, code


@case
def g09_list_mode_and_bad_root():
    """G09 list 只列不跑；根目录不存在时退出码 2"""
    with tempfile.TemporaryDirectory() as t:
        write(t, "SKILL.md", "自检：9/9 PASS\n")
        code, out = run(["list", t])
        assert code == 0, code
        assert "未核验" in out
        code2, out2 = run(["check", os.path.join(t, "no-such-dir")])
        assert code2 == 2, code2


def main():
    rows = []
    fails = 0
    for fn in CASES:
        cid = fn.__name__.split("_")[0].upper()
        try:
            fn()
            rows.append((cid, fn.__doc__, "PASS"))
            print("PASS  %s  %s" % (cid, fn.__doc__))
        except AssertionError as e:
            fails += 1
            rows.append((cid, fn.__doc__, "FAIL: %s" % e))
            print("FAIL  %s  %s  →  %s" % (cid, fn.__doc__, e))
        except Exception as e:  # noqa: BLE001
            fails += 1
            rows.append((cid, fn.__doc__, "ERROR: %s" % e))
            print("ERROR %s  %s  →  %s" % (cid, fn.__doc__, e))

    print("\n---- %d/%d PASS ----" % (len(CASES) - fails, len(CASES)))
    with io.open(os.path.join(HERE, "result.json"), "w", encoding="utf-8", newline="\n") as f:
        json.dump({"cases": [{"id": r[0], "desc": r[1], "result": r[2]} for r in rows]},
                  f, ensure_ascii=False, indent=2)
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
