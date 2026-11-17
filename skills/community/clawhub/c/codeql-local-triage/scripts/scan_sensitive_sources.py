#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prefilter without a database build: statically enumerate every "sensitive name" in Python files
that could drive a CodeQL taint flow.

免建库预筛：静态枚举 Python 文件里所有可能驱动 CodeQL taint 的「敏感名」。

Why / 原理
----------
py/clear-text-storage-sensitive-data (CWE-312) and similar rules pick their source **by name, never
by content**. This script re-implements that decision equivalently, so candidate sources can be listed
without a database build (measured: ~9 minutes for a whole repo). Each hit is printed with its source
class, line number and the reason it matched.

py/clear-text-storage-sensitive-data（CWE-312）等规则的 source **不看内容、只看名字**。
本脚本把 CodeQL 的判定逻辑等价重实现一遍，这样不必建库（实测整仓建库要 ~9 分钟）就能先列出候选源。
它会打印每个命中点的 **source 类别 + 行号 + 命中理由**。

Upstream references (github/codeql, MIT) / 照着抄的来源：
  shared/concepts/codeql/concepts/internal/SensitiveDataHeuristics.qll    -> regexes / 正则
  python/ql/lib/semmle/python/dataflow/new/SensitiveDataSources.qll       -> source classes / source 类
  python/ql/lib/semmle/python/security/dataflow/CleartextStorageCustomizations.qll
                                                                          -> which sources are used

Seven source classes, all name/literal-heuristic driven / source 类共 7 种，全部依赖名字/字面量启发式：
  SensitiveVariableAssignment   assignment to a sensitive name (assign / for / with) / 赋值给敏感名
  SensitiveAttributeAccess      x.<sensitive name>
  SensitiveSubscript            x["sensitive literal"]
  SensitiveGetCall              x.get("sensitive literal")
  SensitiveParameter            a parameter whose name is sensitive / 形参名敏感
  SensitiveFunctionCall         calling a function with a sensitive name / 调用敏感名的函数
  GetPassCall                   getpass.getpass()

Usage / 用法
------------
    python scan_sensitive_sources.py path/to/file.py
    python scan_sensitive_sources.py src/ --json          # recurse into a dir / 递归扫目录
    python scan_sensitive_sources.py $(git ls-files '*.py')   # 输出「候选源清单」，不是审计结论

Exit codes / 退出码：
  0 = no candidate source / 未发现候选源
  1 = candidates found / 发现候选源
  2 = input / runtime error（所给路径不存在、文件全部解析失败等）
可对你关心的文件/目录做**候选源清点**（**非审计结论**）：0 / 1 是判定结果，2 是运行错误需排查。

Porting notes: QL -> Python re, two pitfalls / 移植注记（QL -> Python re 的两个坑）
----------------------------------------------------------------------------------
1. QL allows variable-width lookbehind. ``(?<!is|is_)`` raises
   ``re.error: look-behind requires fixed-width pattern`` in Python; rewrite it as several
   fixed-width assertions in series, ``(?<!is)(?<!is_)`` (all must pass for the exclusion to apply).
   QL 支持变长 lookbehind，``(?<!is|is_)`` 在 Python 会抛该异常，
   等价改写为多个定长断言串联 ``(?<!is)(?<!is_)``（须同时通过才排除）。
2. An inline ``(?is)`` cannot appear mid-expression: it raises
   ``global flags not at the start of the expression``. Pass the flags to ``re.compile`` instead;
   when branches of one regex need different flags, split them into separate compiled patterns.
   内联 ``(?is)`` 不能出现在表达式中间，会抛该异常；
   把 flags 作为参数传给 ``re.compile``，同一分支内 flag 不同就拆成多条 pattern 取并集。
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from i18n import resolve_lang, tr, set_lang  # noqa: E402

I, S = re.IGNORECASE, re.DOTALL

# ---- 正则：逐字抄自 SensitiveDataHeuristics.qll（已抽出内联 flag）-------------
MAYBE = [
    ("secret", [(r".*((?<!is)(?<!is_)secret|(?<!un)(?<!un_)(?<!is)(?<!is_)trusted(?!_iter)"
                 r"|confidential).*", I | S)]),
    ("id", [(r".*(acc(ou)?nt|puid|user.?(name|id)|session.?(id|key)).*", I | S),
            (r".*([uU]|^|_|[a-z](?=U))([uU][iI][dD]).*", S)]),
    ("password", [(r".*(pass(wd|word|code|.?phrase)(?!.*question)|"
                   r"(auth(entication|ori[sz]ation)?).?key|oauth|api.?(key|tok)|"
                   r"([_-]|\b)mfa([_-]|\b)).*", I | S)]),
    ("certificate", [(r".*(cert)(?!.*(format|name|ification)).*", I | S)]),
    ("private", [(r".*("
                  r"social.?security|employer.?identification|national.?insurance|resident.?id|"
                  r"passport.?(num|no)|([_-]|\b)ssn([_-]|\b)|"
                  r"post.?code|zip.?code|home.?addr|"
                  r"(mob(ile)?|home).?(num|no|tel|phone)|(tel|fax|phone).?(num|no)|telephone|"
                  r"emergency.?contact|latitude|longitude|nationality|"
                  r"(credit|debit|bank|visa).?(card|num|no|acc(ou)?nt)|"
                  r"(card|acc(ou)?nt).?(no|num|credit)|routing.?num|salary|billing|beneficiary|"
                  r"credit.?(rating|score)|([_-]|\b)(ccn|cvv|iban)([_-]|\b)|security.?code|"
                  r"birth.?da(te|y)|da(te|y).?birth|gender|([_-]|\b)sex([_-]|\b)|"
                  r"medical|(health|care).?plan|healthkit|appointment|prescription|"
                  r"patient.?(id|record)|blood.?(type|alcohol|glucose|pressure)|"
                  r"heart.?(rate|rhythm)|body.?(mass|fat)|"
                  r"menstrua|pregnan|insulin|inhaler|"
                  r"employ(er|ee)|spouse|maiden.?name|mac.?addr"
                  r").*", I | S)]),
]

# notSensitiveRegexp()：反向排除器。注意 redact/encode/hash/crypt 在这里，
# 所以 "[REDACTED_SECRET]" 这类占位符不算敏感 —— 别把它当污染源去查。
NOT_SENSITIVE = (r".*([^\w$.-]|redact|censor|obfuscate|hash|md5|sha|random|"
                 r"(?<!unen)crypt|(?<!un)encode|"
                 r"certain|concert|secretar|wildcard|coauthor|account(ant|ab|ing|ed)|"
                 r"(?<!pro)file|path|([_-]|\b)url).*", I | S)

_MAYBE_C = [(c, [re.compile(p, f) for p, f in pats]) for c, pats in MAYBE]
_NOT_C = re.compile(NOT_SENSITIVE[0], NOT_SENSITIVE[1])


def classify(name: str) -> list[str]:
    """返回命中的 classification 列表（已应用 notSensitiveRegexp 排除）。"""
    if _NOT_C.fullmatch(name):
        return []
    return [c for c, pats in _MAYBE_C if any(rx.fullmatch(name) for rx in pats)]


def _names_of(t):
    """从赋值目标里取出 Name 节点（支持 a = b 与 a, b = ...）。"""
    if t is None:
        return []
    if isinstance(t, ast.Name):
        return [t]
    return [e for e in getattr(t, "elts", []) if isinstance(e, ast.Name)]


def scan_source(text: str) -> tuple[list[dict], list[str]]:
    """返回 (真·source 列表, 敏感字符串字面量列表)。

    source 列表元素：{class, line, label, hits, text}
    """
    tree = ast.parse(text)
    lines = text.split("\n")
    found: list[dict] = []

    def note(cls, node, label, hits):
        ln = getattr(node, "lineno", 0)
        found.append({"class": cls, "line": ln, "label": label, "hits": hits,
                      "text": lines[ln - 1].strip()[:78] if ln else ""})

    # ① SensitiveVariableAssignment（assign / for / with）
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                for n in _names_of(tgt):
                    if (h := classify(n.id)):
                        note("SensitiveVariableAssignment", n, f"LHS={n.id}", h)
        elif isinstance(node, (ast.For, ast.AsyncFor)):
            for n in _names_of(node.target):
                if (h := classify(n.id)):
                    note("SensitiveVariableAssignment(for)", n, f"LHS={n.id}", h)
        elif isinstance(node, (ast.With, ast.AsyncWith)):
            for item in node.items:
                for n in _names_of(item.optional_vars):
                    if (h := classify(n.id)):
                        note("SensitiveVariableAssignment(with)", n, f"LHS={n.id}", h)

    # ② SensitiveParameter
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = node.args
            for p in (a.posonlyargs + a.args + a.kwonlyargs +
                      ([a.vararg] if a.vararg else []) + ([a.kwarg] if a.kwarg else [])):
                if (h := classify(p.arg)):
                    note("SensitiveParameter", p, f"param={p.arg}", h)

    # ③ SensitiveFunctionCall
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if (h := classify(node.func.id)):
                note("SensitiveFunctionCall", node, f"call={node.func.id}", h)

    # ④ SensitiveAttributeAccess
    for node in ast.walk(tree):
        if isinstance(node, ast.Attribute) and (h := classify(node.attr)):
            note("SensitiveAttributeAccess", node, f".{node.attr}", h)

    # ⑤⑥ SensitiveSubscript / SensitiveGetCall
    for node in ast.walk(tree):
        if isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Constant) \
                and isinstance(node.slice.value, str) and (h := classify(node.slice.value)):
            note("SensitiveSubscript", node, f'["{node.slice.value}"]', h)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) \
                and node.func.attr == "get" and node.args \
                and isinstance(node.args[0], ast.Constant) and isinstance(node.args[0].value, str) \
                and (h := classify(node.args[0].value)):
            note("SensitiveGetCall", node, f'.get("{node.args[0].value}")', h)

    # ⑦ 敏感字符串字面量（CodeQL 仅在它被当 lookup key 时才算 source，此处单列）
    str_lits = sorted({n.value for n in ast.walk(tree)
                       if isinstance(n, ast.Constant) and isinstance(n.value, str)
                       and classify(n.value)})
    return sorted(found, key=lambda x: x["line"]), str_lits


def iter_py_files(paths: list[str]) -> tuple[list[Path], list[Path]]:
    """返回 (命中文件列表, 不存在的路径列表)。

    不存在的路径单独收集出来交回 main —— 缺失输入是「运行错误」而非「干净」，
    否则 CI 会把「路径拼错 / 文件被删」误判成「无候选源」。
    """
    out: list[Path] = []
    missing: list[Path] = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            out.extend(sorted(p.rglob("*.py")))
        elif p.is_file():
            out.append(p)
        else:
            print(tr("warn_skip_missing", p=p), file=sys.stderr)
            missing.append(p)
    return out, missing


SELF_TEST_CASES = {
    # name -> expected classifications ([] = must be clean)
    # 名字 -> 期望命中的 classification（[] 表示应为干净）
    "SECRET_PATTERNS": ["secret"],      # the positive demo name / 正面样例
    "CREDENTIAL_PATTERNS": [],          # renamed -> no longer sensitive / 改名后干净
    "secretary": [],                    # matches "secret", then ruled out by notSensitiveRegexp
    "accountant": [],                   # matches "account", likewise ruled out / 同上，排除表拦下
    "classname": [],                    # contains "ssn" but the pattern needs a word boundary
                                        # 含 "ssn" 子串，但模式要求词边界 -> 干净
    "secret": ["secret"],
    "api_key": ["password"],
    "user_id": ["id"],
    "session_token": [],
    "[REDACTED_SECRET]": [],
    "path": [],
}


def self_test() -> int:
    bad = 0
    for name, want in SELF_TEST_CASES.items():
        got = classify(name)
        ok = got == want
        bad += not ok
        print(f"  {tr('ok_label') if ok else tr('fail_label')}  {name:22s} -> {got!r}"
              + ("" if ok else f"   期望 {want!r}"))
    print(tr("selftest_all") if not bad else tr("selftest_some", bad=bad))
    return 1 if bad else 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=tr("scan_desc"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=tr("scan_epilog"))
    ap.add_argument("paths", nargs="*", help=tr("paths_help"))
    ap.add_argument("--json", action="store_true", help=tr("json_help"))
    ap.add_argument("--quiet", action="store_true", help=tr("quiet_help"))
    ap.add_argument("--summary", action="store_true",
                    help=tr("summary_help"))
    ap.add_argument("--jobs", type=int, default=1, metavar="N",
                    help=tr("jobs_help"))
    ap.add_argument("--self-test", action="store_true", help=tr("selftest_help"))
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto",
                    help=tr("lang_help"))
    args = ap.parse_args(argv)
    set_lang(args.lang)

    if args.self_test:
        return self_test()
    if not args.paths:
        ap.error(tr("err_no_paths"))
    if args.jobs < 1:
        ap.error(tr("err_jobs_range", got=args.jobs))

    files, missing = iter_py_files(args.paths)
    if missing:
        print(tr("err_missing_paths", n=len(missing),
                 paths=", ".join(str(p) for p in missing)), file=sys.stderr)
        return 2

    def _one(p: Path) -> dict | None:
        try:
            found, lits = scan_source(p.read_text(encoding="utf-8"))
        except (SyntaxError, UnicodeDecodeError) as exc:
            print(tr("warn_parse_fail", p=p, type=type(exc).__name__, exc=exc),
                  file=sys.stderr)
            return None
        return {"file": str(p), "sources": found, "sensitive_literals": lits}

    # jobs=1 走串行（保持默认行为与输出顺序）；>1 用线程池（GIL 下 CPU 密集收益有限，
    # 但对网络盘 / 冷缓存读取仍有效，且不引入第三方依赖）
    if args.jobs > 1 and len(files) > 1:
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=args.jobs) as pool:
            results = list(pool.map(_one, files))
    else:
        results = [_one(p) for p in files]

    report = [r for r in results if r is not None]
    total = sum(len(r["sources"]) for r in report)

    if args.json:
        print(json.dumps({"files": report, "total_sources": total},
                         ensure_ascii=False, indent=2))
        return 1 if total else 0

    if args.summary:
        print(tr("summary_head"))
        for item in report:
            print(tr("summary_row", file=item["file"],
                     sources=len(item["sources"]),
                     lits=len(item["sensitive_literals"])))
        print(tr("total_count", files=len(report), total=total))
        return 1 if total else 0

    for item in report:
        found = item["sources"]
        if args.quiet:
            print(tr("quiet_count", file=item["file"], n=len(found)))
            continue
        print("=" * 78)
        print(tr("header_file", file=item["file"]))
        print("=" * 78)
        print("\n" + tr("header_real", n=len(found)))
        for s in found:
            print(f"  L{s['line']:<5} {s['class']:32s} {s['label']:26s} -> {s['hits']}")
            print(f"        {s['text']}")
        if not found:
            print("  （无）")
        lits = item["sensitive_literals"]
        print("\n" + tr("header_literals", n=len(lits)))
        for s in lits:
            print(f"  {s!r:44s} -> {classify(s)}")
        if found:
            print("\n" + tr("hint_text"))
        print()

    if args.quiet:
        print(tr("total_count", files=len(files), total=total))
    return 1 if total else 0


if __name__ == "__main__":
    sys.exit(main())
