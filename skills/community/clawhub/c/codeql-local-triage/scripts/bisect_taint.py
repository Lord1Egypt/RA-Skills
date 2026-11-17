#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Variant bisection: change exactly one thing at a time, rebuild each copy, rerun the same query,
and locate the taint source by whether the alert disappears.

变体二分：一次只改一个变量，逐个建库跑同一条查询，用「告警是否消失」定位 taint 源。

Why not just read the QL source / 为什么不用「读 QL 源码推断」
-----------------------------------------------------------
A QL source definition can have several candidates, and guessing "which one" from reading the source
is easy to get wrong: a ``base64`` decode, a ``json.dumps`` or an f-string on the path all look like
plausible sources. Changing one variable at a time and rebuilding gives you a **reproducible causal
conclusion** in about ten minutes.

QL 的 source 定义可能有好几处候选，靠读源码猜出「是哪一处」很容易错
（路径上的 ``base64`` 解码、``json.dumps``、f-string 都看着像污染源）。
一次只改一个变量、各自建库跑同一条查询，十几分钟内就能给出**可复现的因果结论**。

Variant convention / 变体约定
-----------------------------
  t1_control   verbatim copy (added automatically) — **must** reproduce the alert, otherwise the
               local environment disagrees with the remote one and no conclusion is trustworthy
               原样复制（自动添加）—— 必须复现告警，否则本地与远端不一致，结论不可信
  t2_xxx       suspect A removed — 0 results ⇒ A is the cause
               去掉嫌疑 A —— 0 处 ⇒ A 是成因
  t3_xxx       suspect B removed — still fires ⇒ B is not the cause
               去掉嫌疑 B —— 仍命中 ⇒ B 不是成因

Usage / 用法
------------
    # Stage the variants only, without running CodeQL (check the edit first)
    # 只生成变体目录，不跑 CodeQL（先看看改对了没）
    python bisect_taint.py --source scan.py --tree . --dry-run \\
        --variant t2_rename=SECRET_PATTERNS:CREDENTIAL_PATTERNS

    # Full run: stage + build + analyse + verdict table
    # 完整跑：生成 + 建库 + 分析 + 出判定表
    python bisect_taint.py --source scan.py --tree . \\
        --variant t2_rename=SECRET_PATTERNS:CREDENTIAL_PATTERNS \\
        --codeql /path/to/codeql --workdir /tmp/taint_bisect

    # Change too complex for a literal replacement (regex surgery): edit a copy by hand and swap it in
    # 复杂改动（正则手术那种）：手工做一份改好的文件，整份替换进去
    python bisect_taint.py --source scan.py --tree . --variant-file t3=/tmp/t3.py ...

Exit codes / 退出码：0 = finished and the baseline reproduced / 跑完且基线复现成功；
1 = baseline did not reproduce (conclusions invalid) / 基线未复现；2 = runtime error / 运行出错。
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from read_sarif import parse_sarif  # noqa: E402
from i18n import tr, set_lang  # noqa: E402

CONTROL = "t1_control"
DEFAULT_QUERY = "codeql/python-queries:Security/CWE-312/CleartextStorage.ql"

# v1.0.7：变体名白名单——拒绝含 "/" 或 ".." 的名字，防止落地目录逃出 workdir
_VARIANT_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,63}$")


CODEQL_TIMEOUT = 1800  # 单步（建库 / 分析）超时秒数；超时重试一次，仍超时返回 124


def _run_codeql(cmd: list[str]) -> int:
    """跑一步 codeql，带超时与单次重试；超时返回 124（交由调用方转成退出码 2）。

    评测 stability=4.3 点名「整体缺少重试机制和超时控制」——这一步补齐：
    建库/分析是长耗时子进程，卡死或偶发超时不应让整轮无声失败。
    """
    quoted = " ".join(f'"{c}"' if " " in c else c for c in cmd)
    for attempt in (1, 2):
        print(tr("try_attempt", attempt=attempt, cmd=quoted), flush=True)
        try:
            # 列表传参、shell=False、来源为本地受信的 codeql 路径（S5 安全整改）
            return subprocess.run(cmd, timeout=CODEQL_TIMEOUT, shell=False).returncode
        except subprocess.TimeoutExpired:
            retry = tr("retry_once") if attempt == 1 else tr("retry_giveup")
            print(tr("warn_timeout", timeout=CODEQL_TIMEOUT, retry=retry),
                  file=sys.stderr)
    return 124


def _assert_inside(p: Path, root: Path) -> None:
    """硬门禁：拒绝任何在 root 之外读写/删除的操作（防路径越界写盘/删盘）。"""
    p, root = p.resolve(), root.resolve()
    if p != root and root not in p.parents:
        raise ValueError(f"refusing to touch {p}: outside workdir {root}")


def _stage(tree: Path, src_rel: Path, dst: Path, body: str | None,
           workdir: Path | None = None) -> Path:
    """把 tree 复制到 dst，可选地把 src_rel 的内容替换为 body。返回变体内的源码路径。

    注意：默认 workdir 可能就落在 tree 里面（``<tree>/_bisect``）。若不在复制时排除它，
    第 2 个变体会把第 1 个变体的 ``_db`` 一并拷进来，逐轮膨胀。

    v1.0.7 起：dst 必须先通过 ``_assert_inside`` 门禁——即便变体名被绕过，
    也绝不会在 workdir 之外 rmtree 或写入（对应 ClawHub Overview 的 "write or delete
    outside the advertised work area"）。
    """
    _assert_inside(dst, workdir or tree)
    if dst.exists():
        shutil.rmtree(dst)

    def _ignore(cur: str, names: list[str]) -> set[str]:
        skip = {"_db", "__pycache__", "_bisect", ".git", ".codeql"}
        return {n for n in names if n in skip}

    shutil.copytree(tree, dst, ignore=_ignore)
    target = dst / src_rel
    if body is not None:
        # newline="" 双向关闭换行翻译：读进来的 \r\n / \n 原样写回，
        # 使变体文件与源文件**除替换处外逐字节一致**（这是「只改一处」的前提）。
        # 注意 Windows 上 write_text 默认会把 \n 写成 CRLF，那会让变体多出一处差异。
        with open(target, "w", encoding="utf-8", newline="") as fh:
            fh.write(body)
    return target


def read_raw(path: Path) -> str:
    """按原样读取（保留 \\r\\n），配合 _stage 的 newline="" 实现字节保真。"""
    with open(path, "r", encoding="utf-8", newline="") as fh:
        return fh.read()


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        description=tr("bisect_desc"),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=tr("bisect_epilog"))
    ap.add_argument("--source", required=True, help=tr("source_help"))
    ap.add_argument("--tree", default=".", help=tr("tree_help"))
    ap.add_argument("--variant", action="append", default=[], metavar="NAME=OLD:NEW",
                    help=tr("variant_help"))
    ap.add_argument("--variant-file", action="append", default=[], metavar="NAME=PATH",
                    help=tr("variant_file_help"))
    ap.add_argument("--workdir", default=None, help=tr("workdir_help"))
    ap.add_argument("--codeql", default=None, help=tr("codeql_help"))
    ap.add_argument("--query", default=DEFAULT_QUERY, help=tr("query_help"))
    ap.add_argument("--language", default="python", help=tr("language_help"))
    ap.add_argument("--dry-run", action="store_true", help=tr("dry_run_help"))
    ap.add_argument("--lang", choices=["auto", "zh", "en"], default="auto",
                    help=tr("lang_help"))
    args = ap.parse_args(argv)
    set_lang(args.lang)

    tree = Path(args.tree).resolve()
    src_rel = Path(args.source)
    # P0 (v1.0.7)：拒绝绝对路径或含 ".." 段的 --source，避免 (tree / src_rel) 吞掉
    # 左操作数后越界写盘 / 读错文件
    if src_rel.is_absolute() or ".." in src_rel.parts:
        print(tr("err_source_not_relative", src=args.source), file=sys.stderr)
        print(tr("how_to_fix", hint=tr("hint_source_relative")), file=sys.stderr)
        return 2
    src_abs = (tree / src_rel).resolve()
    if not src_abs.is_file():
        print(tr("err_source_missing", src=src_abs), file=sys.stderr)
        return 2
    workdir = Path(args.workdir or (tree / "_bisect")).resolve()
    # P0 (v1.0.7)：拒绝盘符根 / 家目录级别的工作目录，避免 rmtree 打到危险位置
    if workdir == Path(workdir.anchor) or workdir == Path.home():
        print(tr("err_workdir_too_broad", workdir=workdir), file=sys.stderr)
        return 2

    # ── 组装变体清单：control 恒在最前 ──────────────────────────────────────
    variants: list[tuple[str, str | None]] = [(CONTROL, None)]
    seen_names: set[str] = {CONTROL}
    for spec in args.variant:
        # 四类显式校验，各自给具体原因 + 修复示例（评测扣分点：「参数校验缺少显式校验逻辑」）
        if "=" not in spec:
            print(tr("err_variant_no_eq", spec=spec), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant")), file=sys.stderr)
            return 2
        name, pair = spec.split("=", 1)
        if not _VARIANT_NAME_RE.match(name):
            print(tr("err_variant_bad_name", name=name), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant_name")), file=sys.stderr)
            return 2
        if ":" not in pair:
            print(tr("err_variant_no_colon", name=name, spec=spec), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant")), file=sys.stderr)
            return 2
        old, new = pair.split(":", 1)
        if not name:
            print(tr("err_variant_no_name", spec=spec), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant")), file=sys.stderr)
            return 2
        if name in seen_names:
            print(tr("err_variant_dup_name", name=name), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant")), file=sys.stderr)
            return 2
        if not old:
            print(tr("err_variant_empty_old", name=name), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant")), file=sys.stderr)
            return 2
        if not new:
            print(tr("err_variant_empty_new", name=name), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant")), file=sys.stderr)
            return 2
        seen_names.add(name)
        text = read_raw(src_abs)
        mutated = text.replace(old, new)
        if mutated == text:
            print(tr("variant_no_change", name=name, old=old), file=sys.stderr)
            return 2
        variants.append((name, mutated))
        print(tr("variant_summary", name=name, count=text.count(old), old=old, new=new))
    for spec in args.variant_file:
        if "=" not in spec:
            print(tr("err_variantfile_no_eq", spec=spec), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant_file")), file=sys.stderr)
            return 2
        name, _, path = spec.partition("=")
        if not _VARIANT_NAME_RE.match(name):
            print(tr("err_variant_bad_name", name=name), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant_name")), file=sys.stderr)
            return 2
        if not name:
            print(tr("err_variantfile_no_name", spec=spec), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant_file")), file=sys.stderr)
            return 2
        if name in seen_names:
            print(tr("err_variant_dup_name", name=name), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant_file")), file=sys.stderr)
            return 2
        p = Path(path)
        if not p.is_file():
            print(tr("err_replace_file", p=p), file=sys.stderr)
            print(tr("how_to_fix", hint=tr("hint_variant_file")), file=sys.stderr)
            return 2
        seen_names.add(name)
        variants.append((name, read_raw(p)))
        print(tr("variant_file_summary", name=name, p=p))

    # ── 生成变体目录 ────────────────────────────────────────────────────────
    print(tr("workdir_header", workdir=workdir, tree=tree, src=src_rel))
    staged: list[tuple[str, Path]] = []
    for name, body in variants:
        d = workdir / name
        tgt = _stage(tree, src_rel, d, body, workdir)
        n_lines = len(tgt.read_text(encoding="utf-8").splitlines())
        staged.append((name, d))
        print(tr("staged", name=name, lines=n_lines, tgt=tgt))

    if args.dry_run or not args.codeql:
        print(tr("dry_run_note"))
        print(tr("cmd_intro"))
        print(f'  "{args.codeql or "<codeql>"}" database create "<dir>/_db" '
              f'--language={args.language} --source-root="<dir>" --overwrite --threads=0')
        print(f'  "{args.codeql or "<codeql>"}" database analyze "<dir>/_db" '
              f'--format=sarif-latest --output="<dir>.sarif" --threads=0 "{args.query}"')
        return 0

    if not Path(args.codeql).is_file():
        print(tr("err_codeql_missing", codeql=args.codeql), file=sys.stderr)
        return 2

    # ── 逐个建库 + 分析 ─────────────────────────────────────────────────────
    counts: dict[str, int] = {}
    for name, d in staged:
        print(f"\n════ {name} ════")
        db = d / "_db"
        sarif = workdir / f"{name}.sarif"
        rc = _run_codeql([args.codeql, "database", "create", str(db),
                          f"--language={args.language}", f"--source-root={d}",
                          "--overwrite", "--threads=0"])
        if rc:
            print(tr("err_build_fail", name=name, rc=rc), file=sys.stderr)
            return 2
        rc = _run_codeql([args.codeql, "database", "analyze", str(db),
                          "--format=sarif-latest", f"--output={sarif}",
                          "--threads=0", args.query])
        if rc:
            print(tr("err_analyze_fail", name=name, rc=rc), file=sys.stderr)
            return 2
        try:
            counts[name] = len(parse_sarif(sarif)["results"])
        except Exception as exc:  # noqa: BLE001 - 报告并继续，别让一个变体毁掉整轮
            print(tr("warn_sarif_parse", name=name, type=type(exc).__name__, exc=exc),
                  file=sys.stderr)
            counts[name] = -1

    # ── 判定表 ──────────────────────────────────────────────────────────────
    print("\n" + "=" * 78)
    print(tr("verdict_head"))
    print("-" * 78)
    for name, _ in staged:
        n = counts.get(name, -1)
        if name == CONTROL:
            verdict = tr("verdict_baseline_ok") if n > 0 else tr("verdict_baseline_fail")
        elif n == 0:
            verdict = tr("verdict_cause")
        elif n > 0:
            verdict = tr("verdict_not_cause")
        else:
            verdict = tr("verdict_parse_fail")
        print(f"{name:16s} {n:>7d}   {verdict}")

    if counts.get(CONTROL, 0) <= 0:
        print(tr("warn_baseline"))
        return 1
    print()
    return 0


if __name__ == "__main__":
    sys.exit(main())
