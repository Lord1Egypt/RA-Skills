#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""claim-audit：把文档里的数字拉回去，跟实际跑出来的结果对一遍。

设计立场：
  文档里写「9/9 PASS」「12 个文件」「100/100」这类数字，是最容易写错、也最容易被
  读者默认相信的东西。本工具不做判断、不改文档，只做一件事——
  **把每个能验的数字重新跑一遍，然后告诉你对不上。**

三条坚决不做（见 references/limits.md）：
  1. 不判断"这句话说得对不对"，只判断"这个数字跑出来是不是这个数"。
  2. 不替作者改数字。对不上是人的事，工具只负责把它摆到台面上。
  3. 不把"验不了"当"错"。没有断言、没有命令的声明，标 UNVERIFIABLE，不算失败。
"""
import argparse
import io
import json
import os
import re
import subprocess
import sys

EXCLUDE_DIRS = {"__pycache__", ".git", "node_modules"}

# 声明来源：只读这两份，不做全仓扫描（避免把示例文本里的数字也当声明）
SOURCES = ("SKILL.md", "README.md")

RE_TESTS = re.compile(r"(\d+)\s*/\s*(\d+)\s*(?:PASS|pass|通过)")
RE_FILES = re.compile(r"(?:files?=|\b)(\d+)\s*个文件|\bfiles=(\d+)")
RE_SCORE = re.compile(r"(\d+)\s*/\s*100")
RE_PATH = re.compile(r"`((?:tests|scripts|references|demo)/[^`\s]+)`")

# 只在"引用行"上认路径声明：列表项、表格行、引用块、Markdown 链接行。
# 正文里举例提到的 `scripts/review.py:157` 是别的包的文件，不是本包的声明。
def is_ref_line(line):
    """只认引用行：列表项、Markdown 链接行、引用块。

    表格行不认——表格里常用来"解释工具会查什么"（如 `references/x.md` 这种占位），
    那是行为说明不是本包声明。宁可漏判，不可冤枉。
    """
    s = line.strip()
    return s.startswith(("-", "*", ">")) or "](" in s


def is_score_line(line):
    return bool(re.search(r"结构制|语义制|总分|score|评级|grade", line))


# 历史轨迹里的数字（"46/100 → 67/100"、"基线 46/100"）是过程记录，不是当前声明。
def is_history_line(line):
    return "→" in line or bool(re.search(r"基线|复测|轨迹|history|before/after", line))


def tick_spans(line):
    """行内反引号包裹的区间。包在反引号里的数字是举例，不是声明——
    这条是本包自审时被打出来的：27 条"声明"里 14 条是它自己文档里的示例。"""
    spans = []
    open_at = None
    for i, ch in enumerate(line):
        if ch == "`":
            if open_at is None:
                open_at = i
            else:
                spans.append((open_at, i))
                open_at = None
    return spans


def in_tick(spans, a, b):
    return any(s <= a and b <= e for s, e in spans)


def read(p):
    try:
        with io.open(p, encoding="utf-8") as f:
            return f.read()
    except Exception:  # noqa: BLE001
        return ""


def iter_files(root):
    for cur, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        for n in names:
            yield os.path.join(cur, n)


def count_files(root):
    return sum(1 for _ in iter_files(root))


def run_tests(root):
    """跑包自己的自检，返回 (通过数, 总数, 原始末行) ；跑不起来返回 None。"""
    runner = None
    for cand in ("tests/run_golden.py", "tests/run_tests.py"):
        p = os.path.join(root, cand)
        if os.path.exists(p):
            runner = p
            break
    if runner is None:
        return None
    try:
        r = subprocess.run([sys.executable, runner], cwd=root, capture_output=True,
                           text=True, encoding="utf-8", timeout=180)
    except Exception:  # noqa: BLE001
        return None
    out = (r.stdout or "") + (r.stderr or "")
    m = re.search(r"(\d+)\s*/\s*(\d+)\s*PASS", out)
    if m:
        return int(m.group(1)), int(m.group(2)), out.strip().splitlines()[-1][:120]
    return (0, 0, out.strip().splitlines()[-1][:120] if out.strip() else "无输出")


def find_reviewer(root):
    """同级目录里找 lgd-skill-review 的 review.py；找不到就不验分数。"""
    for up in (os.path.dirname(root), os.path.dirname(os.path.dirname(root))):
        cand = os.path.join(up, "lgd-skill-review", "scripts", "review.py")
        if os.path.exists(cand):
            return cand
    return None


def run_score(root):
    rv = find_reviewer(root)
    if not rv:
        return None
    try:
        r = subprocess.run([sys.executable, rv, root, "--run"], capture_output=True,
                           text=True, encoding="utf-8", timeout=180)
    except Exception:  # noqa: BLE001
        return None
    m = re.search(r"总分：(\d+)/100", r.stdout or "")
    return int(m.group(1)) if m else None


def collect(root):
    """从 SKILL.md / README.md 里抽出所有可验声明。

    跳过三类：front matter（那是介绍文字不是声明）、反引号里的示例、历史轨迹行。
    """
    claims = []
    for name in SOURCES:
        p = os.path.join(root, name)
        if not os.path.exists(p):
            continue
        text = read(p)
        in_fm = False
        fm_seen = 0
        in_fence = False
        for line in text.splitlines():
            s = line.strip()
            if s.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            if s == "---":
                fm_seen += 1
                in_fm = fm_seen == 1
                if fm_seen == 2:
                    in_fm = False
                continue
            if in_fm:
                continue
            spans = tick_spans(line)
            for m in RE_TESTS.finditer(line):
                if is_score_line(line) or in_tick(spans, *m.span()):
                    continue
                claims.append({"kind": "tests", "got": int(m.group(1)),
                               "want": int(m.group(2)), "src": name, "line": s[:90]})
            for m in RE_FILES.finditer(line):
                n = m.group(1) or m.group(2)
                if n and not in_tick(spans, *m.span()):
                    claims.append({"kind": "files", "n": int(n),
                                   "src": name, "line": s[:90]})
            for m in RE_SCORE.finditer(line):
                if is_history_line(line) or in_tick(spans, *m.span()):
                    continue
                claims.append({"kind": "score", "n": int(m.group(1)),
                               "src": name, "line": s[:90]})
            if is_ref_line(line):
                for m in RE_PATH.finditer(line):
                    claims.append({"kind": "path", "path": m.group(1),
                                   "src": name, "line": s[:90]})
    return claims


def audit(root):
    claims = collect(root)
    rows = []
    tests_cache = None
    files_cache = None
    score_cache = None

    for c in claims:
        k = c["kind"]
        if k == "tests":
            if tests_cache is None:
                tests_cache = run_tests(root)
            if tests_cache is None:
                rows.append((c, "UNVERIFIABLE", "找不到可执行的 tests/run_*.py"))
            else:
                got, total, _ = tests_cache
                ok = (got == c["got"] and total == c["want"])
                rows.append((c, "OK" if ok else "MISMATCH", "%d/%d" % (got, total)))
        elif k == "files":
            if files_cache is None:
                files_cache = count_files(root)
            ok = files_cache == c["n"]
            rows.append((c, "OK" if ok else "MISMATCH", str(files_cache)))
        elif k == "score":
            if score_cache is None:
                score_cache = run_score(root)
            if score_cache is None:
                rows.append((c, "UNVERIFIABLE", "找不到 review.py，无法复跑分数"))
            else:
                rows.append((c, "OK" if score_cache == c["n"] else "MISMATCH", str(score_cache)))
        else:
            p = os.path.join(root, c["path"].replace("/", os.sep))
            rows.append((c, "OK" if os.path.exists(p) else "MISMATCH",
                         "存在" if os.path.exists(p) else "不存在"))
    return rows


def main():
    ap = argparse.ArgumentParser(
        prog="audit.py",
        description="把文档里写的数字拉回去重跑一遍：N/M PASS、文件数、X/100、路径是否存在。")
    sub = ap.add_subparsers(dest="cmd")

    p_check = sub.add_parser("check", help="审计一个包：逐条重跑文档里的声明")
    p_check.add_argument("root", help="技能包根目录")
    p_check.add_argument("--json", action="store_true", help="输出机器可读结果")
    p_check.add_argument("--strict", action="store_true",
                         help="把 UNVERIFIABLE 也视为失败（默认不视为失败）")

    p_list = sub.add_parser("list", help="只列出抽到的声明，不跑任何东西")
    p_list.add_argument("root")

    argv = sys.argv[1:]
    if not argv or argv[0] not in ("check", "list"):
        argv = ["check"] + argv
    a = ap.parse_args(argv)

    root = os.path.abspath(a.root)
    if not os.path.isdir(root):
        sys.stderr.write("根目录不存在：%s\n" % root)
        return 2

    claims = collect(root)
    if a.cmd == "list":
        for c in claims:
            print("%-8s %-40s %s" % (c["kind"], c["src"], c["line"]))
        print("共 %d 条声明（仅列出，未核验）" % len(claims))
        return 0

    rows = audit(root)
    bad = [r for r in rows if r[1] == "MISMATCH"]
    unv = [r for r in rows if r[1] == "UNVERIFIABLE"]

    if getattr(a, "json", False):
        print(json.dumps({
            "root": root,
            "total": len(rows),
            "mismatch": len(bad),
            "unverifiable": len(unv),
            "rows": [{"kind": c["kind"], "claim": c["line"], "verdict": v, "actual": act}
                     for c, v, act in rows],
        }, ensure_ascii=False, indent=2))
    else:
        print("审计对象：%s" % root)
        print("%-10s %-8s %-12s %s" % ("类型", "结论", "实际", "声明原文"))
        for c, v, act in rows:
            print("%-10s %-8s %-12s %s" % (c["kind"], v, act, c["line"]))
        print("\n声明 %d 条：对上 %d，对不上 %d，验不了 %d"
              % (len(rows), len(rows) - len(bad) - len(unv), len(bad), len(unv)))

    if bad:
        return 1
    if unv and getattr(a, "strict", False):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
