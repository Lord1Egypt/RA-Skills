#!/usr/bin/env python3
"""embedded-register-verify：核验 C/C++ 代码里的寄存器写入是否与芯片 SVD 一致。

只做词法分析（规格 0.7：不执行用户代码、不 eval）；判定不确定时进"未判定"。
退出码：0 = 没有"报"；1 = 检出问题或工具出错（errors 为空时表示检出问题）。

示例：
  python scripts/verify.py demo
  python scripts/verify.py check main.c --chip STM32G431
  python scripts/verify.py check src/ --demo --checklist
  python scripts/verify.py check --patch changes.diff --chip STM32G431
  python scripts/verify.py rules
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

import crules  # noqa: E402
import cscan  # noqa: E402
from etk_core import query as etk_query  # noqa: E402
from etk_core.cache import load_device_cached  # noqa: E402
from etk_core.discovery import find_svd  # noqa: E402
from etk_core.errors import E_INPUT_INVALID, E_INTERNAL, E_SVD_NOT_FOUND, EtkError  # noqa: E402
from etk_core.output import envelope  # noqa: E402

TOOL = "embedded-register-verify"
__version__ = "1.17.0"
DEMO_SVD = os.path.normpath(os.path.join(_HERE, os.pardir, "assets", "demo.svd"))
MAX_FILES = 200
MAX_WARNINGS_SHOWN = 20
SKIP_DIRS = frozenset({"node_modules", "__pycache__", "site-packages"})


def build_parser():
    io = argparse.ArgumentParser(add_help=False)
    io.add_argument("--project-dir", metavar="DIR", help="从此目录向上查找 .etk/config.json（默认当前目录）")
    io.add_argument("--format", choices=("text", "json"), default="text", help="输出格式（默认 text）")
    io.add_argument("--out", metavar="FILE", help="把输出写入文件，而不是标准输出")

    common = argparse.ArgumentParser(add_help=False, parents=[io])
    common.add_argument("--svd", metavar="PATH", help="SVD 文件路径（优先级最高）")
    common.add_argument("--chip", metavar="NAME", help="芯片名，如 STM32G431，用于在本机 CMSIS-Pack 中查找")
    common.add_argument("--demo", action="store_true", help="使用内置演示芯片（合成数据）核验")

    parser = argparse.ArgumentParser(
        prog="verify.py",
        description="嵌入式寄存器写入审计器：核验 C/C++ 代码中的寄存器写入是否与芯片 SVD 一致（只做词法分析，不执行代码）。",
        epilog=(
            "示例：\n"
            "  verify.py demo                          # 零配置自检（内置演示芯片 + 内置样例）\n"
            "  verify.py doctor                        # 环境体检：SVD 来源与上手建议\n"
            "  verify.py rules                         # 列出核验规则 E01–E13\n"
            "  verify.py check main.c --chip STM32G431 # 核验真实代码（需要本机 CMSIS-Pack）\n"
            "  verify.py check src/ --demo --checklist  # 用内置演示芯片核验整个目录\n"
            "  verify.py check --patch changes.diff --chip STM32G431\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    # 顶层也接受 --format / --out，便于不带子命令时直接指定输出格式
    parser.add_argument("--format", choices=("text", "json"), default="text",
                        help="输出格式（默认 text）")
    parser.add_argument("--out", metavar="FILE", help="把输出写入文件，而不是标准输出")
    sub = parser.add_subparsers(dest="command")

    p = sub.add_parser("check", parents=[common], help="核验文件、目录或补丁中的寄存器写入")
    p.add_argument("paths", nargs="*", metavar="路径",
                   help="C/C++ 源文件、头文件或目录（.c/.h/.cpp/.hpp/.ino 等；用 --patch 时可省略）")
    p.add_argument("--define", action="append", default=[], metavar="NAME=VALUE", help="补充宏定义（可多次）")
    p.add_argument("--headers", action="append", default=[], metavar="路径",
                   help="从头文件加载宏定义（文件或目录，可多次；也可用分号分隔多个路径）：用于 ESP-IDF 等以寄存器常量宏写寄存器的代码")
    p.add_argument("--patch", metavar="FILE", help="核验 unified diff / git diff 文件中新增的行")
    p.add_argument("--no-clock-check", action="store_true", help="关闭 E07（时钟使能）检查")
    p.add_argument("--checklist", action="store_true", help="输出复查清单（按复查要求分组）")
    p.add_argument("--explain", action="store_true",
                   help="在报告里内联对应寄存器的定义（来自寄存器百事通的同一份 SVD）")
    p.add_argument("--limit", type=int, default=200, help="每个文件最多列出条数（默认 200）")

    sub.add_parser("rules", parents=[io], help="列出核验规则 E01–E13")
    sub.add_parser("demo", parents=[io], help="零配置自检：用内置演示芯片与内置样例跑一遍核验（无需任何参数）")
    sub.add_parser("doctor", parents=[io], help="环境体检：报告 SVD 来源与上手建议（不需要 SVD 也能跑）")
    return parser


# ---------- 输入收集 ----------

def _collect_sources(paths):
    files = []
    for item in paths:
        if os.path.isdir(item):
            for root, dirs, names in os.walk(item):
                dirs[:] = [d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS]
                for name in sorted(names):
                    if name.lower().endswith((".c", ".h", ".cpp", ".cc", ".cxx", ".hpp", ".hh", ".hxx", ".ino")):
                        files.append(os.path.join(root, name))
        elif os.path.isfile(item):
            files.append(item)
        else:
            raise EtkError(E_INPUT_INVALID, "路径不存在：%s" % item)
    files = sorted(dict.fromkeys(os.path.abspath(f) for f in files))
    truncated = len(files) > MAX_FILES
    sources = []
    for path in files[:MAX_FILES]:
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
        except OSError as exc:
            raise EtkError(E_INPUT_INVALID, "无法读取文件：%s（%s）" % (path, exc))
        sources.append((os.path.basename(path), text, path))
    return sources, truncated


HEADER_EXTS = (".h", ".hpp", ".hh", ".hxx", ".inc", ".c")
HEADER_MAX_FILES = 512
HEADER_MAX_BYTES = 8 * 1024 * 1024
_INCLUDE_RE = re.compile(r'^\s*#\s*include\s*[<"]([^>"]+)[>"]', re.M)


def _resolve_include(token, base_dirs, roots, index):
    """把 `#include` 里的路径解析为实际文件：① 相对当前/被核验文件目录 ② 相对搜索根
    ③ 按文件名匹配（同名多个时按 --headers 给定顺序优先）。"""
    rel = token.replace("\\", "/")
    for base in base_dirs:
        candidate = os.path.normpath(os.path.join(base, rel))
        if os.path.isfile(candidate):
            return candidate
    for root in roots:
        candidate = os.path.normpath(os.path.join(root, rel))
        if os.path.isfile(candidate):
            return candidate
    hits = index.get(os.path.basename(rel).lower())
    if hits:
        return hits[0]
    return None


def _collect_header_defines(paths, requested=None, source_dirs=None):
    """从头文件（或目录）收集宏定义，用于解析寄存器常量宏（如 ESP-IDF 的 UART_CONF0_REG）。

    - requested 为被核验文件里的 `#include` 列表时：先解析出这些头文件的**闭包**并优先加载，
      其余文件按路径顺序补足（上限 512 个文件 / 8 MB）——保证关键宏一定加载，避免大目录截断误伤；
    - 没有 requested（源文件没有 include / 补丁模式）时：按原行为加载全部（带上限）。

    返回 (defines, note)：note 为 None 或加载策略/达到上限的说明。
    """
    roots = []
    explicit = []
    expanded = []
    for item in paths:
        # 支持一个参数里写多个路径（分号或系统路径分隔符，如 Windows 的 "inc1;inc2"）
        for part in (item.split(os.pathsep) if os.pathsep in item else [item]):
            for piece in part.split(";"):
                piece = piece.strip()
                if piece:
                    expanded.append(piece)
    for item in expanded:
        if os.path.isdir(item):
            roots.append(os.path.abspath(item))
        elif os.path.isfile(item):
            explicit.append(os.path.abspath(item))
        else:
            raise EtkError(E_INPUT_INVALID, "--headers 路径不存在：%s" % item)

    texts = {}
    total = [0]

    def load(path):
        if path in texts:
            return texts[path]
        if total[0] >= HEADER_MAX_BYTES:
            return None
        try:
            with open(path, encoding="utf-8", errors="replace") as fh:
                text = fh.read(HEADER_MAX_BYTES - total[0])
        except OSError:
            texts[path] = None
            return None
        total[0] += len(text)
        texts[path] = text
        return text

    # 收集目录树里的全部候选文件（闭包解析与补足共用）；index 按 --headers 顺序构建，
    # 同名头文件（如各芯片家族的 rtc.h）先给哪个目录就优先用哪个
    all_files = list(explicit)
    index = {}
    for path in explicit:
        index.setdefault(os.path.basename(path).lower(), []).append(path)
    for root in roots:
        for dirpath, dirs, names in os.walk(root):
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in SKIP_DIRS]
            for name in sorted(names):
                if name.lower().endswith(HEADER_EXTS):
                    full = os.path.join(dirpath, name)
                    all_files.append(full)
                    index.setdefault(name.lower(), []).append(full)
    all_files = sorted(set(all_files))

    note = None
    closure = []
    if requested and roots:
        queue = list(requested)
        seen = set()
        while queue and len(closure) < HEADER_MAX_FILES:
            token = queue.pop(0)
            path = _resolve_include(token, source_dirs or [], roots, index)
            if path is None or path in seen:
                continue
            seen.add(path)
            closure.append(path)
            text = load(path)
            if text is None:
                continue
            for nested in _INCLUDE_RE.findall(text):
                queue.append(nested)
        if closure:
            note = "按被核验文件的 #include 优先加载了 %d 个头文件" % len(closure)

    order = closure + [path for path in all_files if path not in set(closure)]
    if len(order) > HEADER_MAX_FILES:
        cap_note = ("头文件数 %d 超过上限 %d，仅加载前 %d 个（建议把 --headers 指向更精确的目录）" % (
            len(order), HEADER_MAX_FILES, HEADER_MAX_FILES))
        note = (note + "；" + cap_note) if note else cap_note
        order = order[:HEADER_MAX_FILES]

    defines = {}
    for path in order:
        if total[0] >= HEADER_MAX_BYTES:
            cap_note = "头文件内容达到 %d MB 上限，其余未加载（建议缩小 --headers 范围）" % (
                HEADER_MAX_BYTES // (1024 * 1024))
            note = (note + "；" + cap_note) if note else cap_note
            break
        text = load(path)
        if text is None:
            continue
        joined, _line_map = cscan.join_continuations(text)
        clean = cscan.strip_comments_and_strings(joined)
        for name, expr in cscan.collect_defines(clean).items():
            defines.setdefault(name, expr)
        for name, expr in cscan.collect_enum_constants(clean, defines).items():
            defines.setdefault(name, expr)  # 头文件里的 enum 常量（#define 优先）
    return defines, note


def _patch_sources(text):
    """把 unified diff 还原成"只含新增行、行号对齐新文件"的合成文本。

    返回 (sources, added)：sources 为 (名称, 文本, 相对路径) 列表；
    added 为 {相对路径: {新增行号}}——补丁模式只核验新增行，上下文优先取磁盘上的整文件。
    """
    files = {}
    added = {}
    current_name = None
    new_line = 0
    for raw in text.split("\n"):
        if raw.startswith("+++ "):
            name = raw[4:].strip()
            if name.startswith(("b/", "a/")):
                name = name[2:]
            current_name = name
            files.setdefault(name, {})
            added.setdefault(name, set())
            continue
        if raw.startswith("@@ "):
            m = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", raw)
            if m:
                new_line = int(m.group(1))
            continue
        if current_name is None:
            continue
        if raw.startswith("+"):
            files[current_name][new_line] = raw[1:]
            added[current_name].add(new_line)
            new_line += 1
        elif raw.startswith(("-", "\\")):
            continue
        else:
            new_line += 1
    out = []
    for name, lines in sorted(files.items()):
        if not lines:
            continue
        buf = [""] * max(lines)
        for no, content in lines.items():
            buf[no - 1] = content
        out.append(("%s (patch)" % name, "\n".join(buf), name))
    return out, added


# ---------- 运行 ----------

def _run_demo(args):
    """零配置自检：用内置演示芯片 + 内置样例代码跑一遍核验，断言规则确实能命中。

    这是本技能的"零配置试用"入口：不需要用户提供任何文件、SVD 或芯片名。
    退出码 0 = 自检通过（工具本身工作正常）；1 = 自检失败（工具不可用）。
    """
    if not os.path.isfile(DEMO_SVD):
        raise EtkError(E_SVD_NOT_FOUND, "内置演示数据缺失：%s" % DEMO_SVD,
                       hint="安装不完整，请重新安装技能包。")
    demo_case = os.path.normpath(os.path.join(_HERE, os.pardir, "examples", "verify_demo.c"))
    if not os.path.isfile(demo_case):
        raise EtkError(E_INPUT_INVALID, "内置自检用例缺失：%s" % demo_case,
                       hint="安装不完整，请重新安装技能包。")

    device = load_device_cached(DEMO_SVD)
    with open(demo_case, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    verifier = crules.Verifier(device, extra_defines={}, clock_check=True, limit=200)
    result = verifier.check_file("verify_demo.c", text)

    counts = result.get("counts") or {}
    report = counts.get("report") or 0
    passed = counts.get("passed") or 0
    writes = counts.get("writes") or 0

    # 自检判据：样例文件里预埋了 3 处确定的问题（E03×1、E10×2）。
    # 能检出这些问题 + 有通过项，说明规则引擎与 SVD 读取都正常。
    problems = []
    if report < 3:
        problems.append("应检出至少 3 处预埋问题（E03×1、E10×2），实际 %d 处" % report)
    if passed < 1:
        problems.append("应至少通过 1 处合法写入，实际 %d 处" % passed)
    if writes < 1:
        problems.append("未识别到任何寄存器写入（解析器可能失效）")

    buckets = {}
    for finding in result.get("findings") or []:
        buckets[finding.get("bucket")] = buckets.get(finding.get("bucket"), 0) + 1

    summary = {
        "kind": "demo",
        "ok": not problems,
        # 只留文件名，不带本机绝对路径（发布包内不得出现本机路径）
        "source": {"file": os.path.basename(DEMO_SVD), "device": device.name, "version": device.version},
        "case": "examples/verify_demo.c",
        "counts": {"writes": writes, "report": report, "passed": passed,
                   "undetermined": counts.get("undetermined") or 0},
        "buckets": buckets,
        "problems": problems,
    }
    if problems:
        warnings = []
        errors = [{
            "code": E_INTERNAL,
            "message": "自检未通过：%s" % "；".join(problems),
            "hint": "内置演示数据或规则引擎可能损坏，请重新安装技能包；"
                    "如问题持续请附 --format json 的输出反馈。",
            "details": {"problems": problems},
        }]
    else:
        warnings = []
        errors = []
    return [summary], warnings, errors


def _run_doctor(args):
    """环境体检：不依赖任何 SVD 也能跑，报告 SVD 来源与上手建议。"""
    lines = ["SVD 来源："]
    found = []
    if os.path.isfile(DEMO_SVD):
        found.append("内置演示数据：%s（设备 ETK-DEMO，--demo 可直接用）" % os.path.basename(DEMO_SVD))
    try:
        path, selected_by, _notes = find_svd(None, None, args.project_dir)
        # 只显示文件名与来源类型；来源描述里可能含本机绝对路径，剥掉
        source_kind = re.sub(r"[A-Za-z]:\\[^\s，。；]*", "<本机路径>", selected_by)
        source_kind = re.sub(r"[A-Za-z]:/[^\s，。；]*", "<本机路径>", source_kind)
        found.append("自动发现：%s（%s）" % (os.path.basename(path), source_kind))
    except EtkError:
        pass
    if not found:
        lines.append("  未找到任何 .svd 文件")
    else:
        lines.extend("  - " + item for item in found)
    lines.append("")
    lines.append("上手建议：")
    lines.append("  - 零配置试用：verify.py demo（内置演示芯片 + 内置样例，自检 E01–E13 规则）")
    lines.append("  - 查看规则：verify.py rules")
    lines.append("  - 环境体检：verify.py doctor")
    lines.append("  - 核验真实代码：verify.py check main.c --chip STM32G431（需要本机装了 CMSIS-Pack）")
    lines.append("  - 指定 SVD：verify.py check main.c --svd /path/to/chip.svd")
    return [{"kind": "doctor", "lines": lines}], [], []


def _run(args):
    if args.command is None:
        # 不带子命令时给出用法速览并正常退出（退出码 0），
        # 便于在无参数场景下直接运行本工具确认它可用。
        return [{
            "kind": "usage",
            "lines": [
                "嵌入式寄存器写入审计器：核验 C/C++ 代码里的寄存器写入是否与芯片 SVD 一致（不执行代码）。",
                "",
                "常用命令：",
                "  verify.py demo      零配置自检（内置演示芯片 + 内置样例，退出码 0 = 工具正常）",
                "  verify.py doctor    环境体检：SVD 来源与上手建议",
                "  verify.py rules     列出核验规则 E01–E13",
                "  verify.py check <文件或目录> --chip <芯片名>   核验真实代码",
                "",
                "用 verify.py --help 查看完整参数。",
            ],
        }], [], []
    if args.command == "rules":
        return [crules.rule_table()], [], []
    if args.command == "demo":
        return _run_demo(args)
    if args.command == "doctor":
        return _run_doctor(args)
    # 以下参数只属于 check 子命令；到这一步必然是 check
    if getattr(args, "limit", 1) < 1:
        raise EtkError(E_INPUT_INVALID, "--limit 必须大于 0")
    if args.patch and not os.path.isfile(args.patch):
        raise EtkError(E_INPUT_INVALID, "--patch 指定的文件不存在：%s" % args.patch)
    if args.demo:
        if args.svd:
            raise EtkError(
                E_INPUT_INVALID,
                "--demo 与 --svd 不能同时使用",
                hint="二选一：用 --svd 核验真实芯片，或用 --demo 试用内置演示芯片。",
            )
        if not os.path.isfile(DEMO_SVD):
            raise EtkError(E_SVD_NOT_FOUND, "内置演示数据缺失：%s" % DEMO_SVD,
                           hint="安装不完整，请重新安装技能包。")
        path, selected_by = DEMO_SVD, "内置演示数据（--demo）"
        notes = ["当前使用内置演示芯片 ETK-DEMO（合成数据，非真实芯片）；真实核验请用 --svd 或 --chip。"]
    else:
        path, selected_by, notes = find_svd(args.svd, args.chip, args.project_dir)
    device = load_device_cached(path)
    warnings = list(notes) + list(device.warnings)

    if args.patch:
        with open(args.patch, encoding="utf-8", errors="replace") as fh:
            patch_sources, patch_added = _patch_sources(fh.read())
        if not patch_sources:
            raise EtkError(E_INPUT_INVALID, "补丁里没有可核验的新增行：%s" % args.patch)
        # 优先用磁盘上的完整文件做上下文（E06/E07/E11 需要看未改动的使能/置位）
        base_dirs = [os.getcwd(), os.path.dirname(os.path.abspath(args.patch))]
        sources = []
        missing_full = []
        for item in patch_sources:
            relpath = item[2]
            full = None
            for base in base_dirs:
                candidate = os.path.join(base, relpath)
                if os.path.isfile(candidate):
                    try:
                        with open(candidate, encoding="utf-8", errors="replace") as fh:
                            full = fh.read()
                    except OSError:
                        full = None
                    break
            if full is not None:
                sources.append((item[0], full, relpath))
            else:
                sources.append(item)
                missing_full.append(relpath)
        if missing_full:
            warnings.append(
                "补丁模式：未找到完整文件（%s）——文件级检查（E06/E07/E11）看不到未改动的上下文，"
                "可能有误报；建议在仓库目录内运行或加 --no-clock-check。" % "、".join(missing_full[:3]))
    else:
        patch_added = None
        if not args.paths:
            raise EtkError(E_INPUT_INVALID, "请给出要核验的文件、目录，或用 --patch 指定补丁文件。")
        sources, truncated = _collect_sources(args.paths)
        if truncated:
            warnings.append("文件数超过 %d，只核验了前 %d 个。" % (MAX_FILES, MAX_FILES))
        if not sources:
            raise EtkError(E_INPUT_INVALID, "没有找到可核验的 .c/.h/.cpp/.hpp/.ino 文件。")

    defines = {}
    for item in args.define:
        name, sep, value = item.partition("=")
        if not sep or not name.strip():
            raise EtkError(E_INPUT_INVALID, "--define 需要 NAME=VALUE 形式：%r" % item)
        defines[name.strip()] = value.strip()
    user_defines = dict(defines)
    if args.headers:
        requested = []
        source_dirs = set()
        for _name, text, path_hint in sources:
            if path_hint:
                parent = os.path.dirname(path_hint)
                if parent:
                    source_dirs.add(parent)
            for token in _INCLUDE_RE.findall(text):
                if token not in requested:
                    requested.append(token)
        header_defines, header_note = _collect_header_defines(
            args.headers, requested=requested, source_dirs=sorted(source_dirs))
        message = "从头文件加载了 %d 个宏定义（--headers）" % len(header_defines)
        if header_note:
            message += "；" + header_note
        warnings.append(message)
        merged = dict(header_defines)
        merged.update(defines)  # --define 显式指定优先
        defines = merged

    # --define 值明显无法求值（不含任何标识符 → 不可能引用其它宏）：给出警告（不静默丢）
    for name, value in user_defines.items():
        if re.search(r"[A-Za-z_]", value):
            continue  # 可能引用其它宏：留给核验阶段求值
        if cscan.eval_int(value, defines) is None:
            warnings.append("--define %s=%s 的值无法求值（该宏按未定义处理）" % (name, value))

    verifier = crules.Verifier(device, extra_defines=defines,
                               clock_check=not args.no_clock_check, limit=args.limit)
    verifier.checklist = bool(args.checklist)

    results = []
    errors = []
    selection = _selection_args(args)
    for name, text, path_hint in sources:
        try:
            res = verifier.check_file(
                name, text,
                patch_lines=(patch_added.get(path_hint) if patch_added else None))
        except EtkError as exc:
            errors.append(exc.to_dict())
            continue
        res["path"] = path_hint
        res["source"]["selected_by"] = selected_by
        _attach_next(res, selection)
        if args.explain:
            _attach_explain(res, device)
        results.append(res)
    return results, warnings, errors


# ---------- 与寄存器百事通的联动 ----------

def _selection_args(args):
    """复现本次 SVD 选择的参数，用于生成可直接运行的查证命令。"""
    if args.demo:
        return ["--demo"]
    if args.svd:
        return ["--svd", os.path.abspath(args.svd)]
    if args.chip:
        return ["--chip", args.chip]
    if args.project_dir:
        return ["--project-dir", os.path.abspath(args.project_dir)]
    return []


def _attach_next(res, selection):
    """每条 finding 生成"下一步查证"命令（可在 embedded-register-lookup 技能里直接执行）。"""
    for finding in res["findings"]:
        hint = finding.get("lookup") or {}
        action = hint.get("action")
        if action == "lookup":
            call = ["lookup", hint["path"]]
        elif action == "addr":
            call = ["addr", hint["address"]]
        elif action == "search":
            call = ["search", hint["keyword"]]
        else:
            call = []
        finding["next"] = [{
            "tool": "embedded-register-lookup",
            "args": call + selection,
            "reason": hint.get("reason") or "查看寄存器事实",
        }] if call else []


def _attach_explain(res, device):
    """--explain：把对应寄存器的定义内联进报告（与百事通同一份 SVD、同一套查询）。"""
    cache = {}
    for finding in res["findings"]:
        finding["explain"] = _explain_lines(device, finding.get("lookup") or {}, cache)


def _explain_lines(device, hint, cache):
    action = hint.get("action")
    key = (action, hint.get("path") or hint.get("address") or hint.get("keyword"))
    if key in cache:
        return cache[key]
    lines = []
    try:
        if action == "lookup":
            lines = _format_lookup(etk_query.lookup(device, hint["path"]))
        elif action == "addr":
            lines = _format_addr(etk_query.find_address(device, int(hint["address"], 16)))
    except EtkError:
        lines = []
    cache[key] = lines
    return lines


def _format_lookup(data):
    kind = data.get("kind")
    if kind == "register":
        reg = data["register"]
        lines = ["寄存器 %s.%s：地址 %s  宽 %d 位  访问 %s  复位 %s" % (
            data["peripheral"], reg["name"], reg["address"], reg["size"], reg["access"], reg["reset"])]
        sem = []
        if reg.get("write_semantics"):
            sem.append("写语义 %s" % reg["write_semantics"])
        if reg.get("read_semantics"):
            sem.append("读语义 %s" % reg["read_semantics"])
        if sem:
            lines.append("  " + "；".join(sem))
        sib = data.get("siblings") or []
        if sib:
            lines.append("  相关寄存器：" + "、".join("%s（%s）" % (s["name"], s["kind"]) for s in sib)
                         + "——位操作建议用它们，避免读改写")
        shown = data["fields"][:8]
        for f in shown:
            desc = "（%s）" % f["description"] if f["description"] and f["description"] != f["name"] else ""
            lines.append("  位 %-6s %-12s %s 复位 %d%s" % (
                f["bits"], f["name"], f["access"], f["reset"], desc))
        if len(data["fields"]) > len(shown):
            lines.append("  …另有 %d 个位域（用 lookup 查看全部）" % (len(data["fields"]) - len(shown)))
        return lines
    if kind == "field":
        f = data["field"]
        reg = data["register"]
        lines = ["位域 %s.%s.%s：位 %s（宽 %d） 访问 %s 复位 %d（寄存器复位 %s）" % (
            data["peripheral"], reg["name"], f["name"], f["bits"], f["width"],
            f["access"], f["reset"], reg["reset"])]
        for e in f["enums"][:6]:
            lines.append("  枚举 %s = %s%s" % (
                e["pattern"], e["name"], "（%s）" % e["description"] if e["description"] else ""))
        return lines
    if kind == "peripheral":
        shown = data["registers"][:8]
        lines = ["外设 %s：基地址 %s，共 %d 个寄存器" % (
            data["peripheral"], data["base_address"], len(data["registers"]))]
        lines.append("  " + "、".join(r["name"] for r in shown)
                     + ("……" if len(data["registers"]) > len(shown) else ""))
        return lines
    return []


def _format_addr(data):
    kind = data.get("kind")
    if kind == "exact" and data.get("matches"):
        m = data["matches"][0]
        return ["%s 是寄存器 %s（访问 %s，复位 %s）" % (
            data["address"], m["path"], m["access"], m["reset"])]
    if kind == "inside_register":
        n = data["nearest"]
        return ["%s 位于寄存器 %s 内部（第 %d 字节）" % (
            data["address"], n["path"], n["offset_in_register"])]
    if kind == "gap":
        return ["%s 不是寄存器地址（%s 内的保留区附近）" % (data["address"], data.get("peripheral") or "?")]
    return ["%s 不在任何外设地址范围内" % data["address"]]


# ---------- 渲染 ----------

def _render_rules(res):
    lines = ["核验规则（E01–E13）："]
    for item in res["rules"]:
        lines.append("  %s %s（%s）｜桶：%s｜标签：%s｜严重度：%s" % (
            item["class"], item["name"], item["verdict"], item["bucket"], item["label"], item["severity"]))
    lines.append("  " + res["note"])
    return lines


def _render_checklist(res):
    cl = res["checklist"]
    lines = ["复查清单："]
    if cl["chip_default"]:
        lines.append("  芯片默认（写入等于复位值，确认可删或有意为之）：")
        for item in cl["chip_default"][:20]:
            lines.append("    第 %d 行 %s" % (item["line"], item["code"]))
    lines.append("  已核验（无需复查）：%d 处" % cl["verified"])
    if cl["manual"]:
        lines.append("  需查手册（%d 条）：" % len(cl["manual"]))
        for item in cl["manual"][:20]:
            if "class" in item:
                lines.append("    第 %d 行（%s）%s" % (item["line"], item["class"], item["message"]))
            else:
                lines.append("    第 %d 行（未判定）%s" % (item["line"], item["reason"]))
    if cl["measured"]:
        lines.append("  需实测（%d 条，涉及 DMA/NVIC/SysTick 等，建议上板验证）：" % len(cl["measured"]))
        for item in cl["measured"][:20]:
            lines.append("    第 %d 行 %s" % (item["line"], item["code"]))
    return lines


def _render_verify(res):
    c = res["counts"]
    by_class = c.get("report_by_class") or {}
    report_text = "报 %d" % c["report"]
    if by_class:
        detail = "、".join("%s %d" % (k, v) for k, v in by_class.items())
        if c.get("findings") and c["findings"] != c["report"]:
            # 一处写入可能命中多条问题：把"写入数"与"问题条数"都写清楚
            report_text += "（%d 条问题：%s）" % (c["findings"], detail)
        else:
            report_text += "（%s）" % detail
    lines = ["%s：%d 处寄存器写入（%s、未判定 %d、通过 %d）" % (
        res["file"], c["writes"], report_text, c["undetermined"], c["passed"])]
    for item in res["findings"]:
        lines.append("  [报] %s 第 %d 行：%s" % (item["class"], item["line"], item["message"]))
        lines.append("      代码：%s" % item["code"])
        if item.get("suggestion"):
            lines.append("      建议：%s" % item["suggestion"])
        for explain in item.get("explain") or []:
            lines.append("      " + explain)
        for nxt in item.get("next") or []:
            lines.append("      下一步：%s %s  （%s）" % (
                nxt["tool"], " ".join(nxt["args"]), nxt["reason"]))
    if res["findings_truncated"]:
        lines.append("  （问题过多，仅显示前 %d 条；用 --format json 获取全部）" % len(res["findings"]))
    for item in res["undetermined"]:
        lines.append("  [未判定] 第 %d 行：%s" % (item["line"], item["reason"]))
        lines.append("      代码：%s" % item["code"])
    if res["undetermined_truncated"]:
        lines.append("  （未判定条目过多，仅显示前 %d 条）" % len(res["undetermined"]))
    by_cat = c.get("undetermined_by_category") or {}
    if c["undetermined"] >= 2 and by_cat:
        lines.append("  未判定分布：%s" % "、".join("%s %d" % (k, v) for k, v in by_cat.items()))
    if res.get("checklist"):
        lines.extend(_render_checklist(res))
    src = res.get("source") or {}
    lines.append("[核验] 依据：%s（设备 %s，版本 %s）" % (
        src.get("file"), src.get("device"), src.get("version")))
    return lines


def _render_demo(res):
    src = res.get("source") or {}
    counts = res.get("counts") or {}
    lines = ["[自检] 内置演示芯片 %s（版本 %s）：%s" % (
        src.get("device"), src.get("version"), src.get("file")),
        "  用例：%s" % res.get("case"),
        "  解析：%d 处寄存器写入 → 报 %d、未判定 %d、通过 %d" % (
            counts.get("writes") or 0, counts.get("report") or 0,
            counts.get("undetermined") or 0, counts.get("passed") or 0)]
    for problem in res.get("problems") or []:
        lines.append("  ✗ %s" % problem)
    if res.get("ok"):
        lines.append("  自检通过：规则引擎、SVD 读取、样例解析均正常。")
        lines.append("  下一步：verify.py check <你的 .c 文件> --chip <芯片名>")
    return lines


def render_text(env):
    lines = []
    for err in env["errors"]:
        lines.append("错误 [%s] %s" % (err["code"], err["message"]))
        if err.get("hint"):
            lines.append("  提示：%s" % err["hint"])
        for item in (err.get("details") or {}).get("tried", []):
            lines.append("  已尝试：%s" % item)
    for w in env["warnings"][:MAX_WARNINGS_SHOWN]:
        lines.append("注意：%s" % w)
    if len(env["warnings"]) > MAX_WARNINGS_SHOWN:
        lines.append("注意：另有 %d 条警告，用 --format json 查看全部" % (
            len(env["warnings"]) - MAX_WARNINGS_SHOWN))
    for res in env["results"]:
        if res["kind"] == "verify":
            lines.extend(_render_verify(res))
        elif res["kind"] == "rules":
            lines.extend(_render_rules(res))
        elif res["kind"] == "demo":
            lines.extend(_render_demo(res))
        elif res["kind"] == "doctor":
            lines.extend(res.get("lines") or [])
        elif res["kind"] == "usage":
            lines.extend(res.get("lines") or [])
        else:
            lines.append(json.dumps(res, ensure_ascii=False))
    files = [r for r in env["results"] if r["kind"] == "verify"]
    if len(files) > 1:
        keys = ("writes", "report", "undetermined", "passed", "findings")
        total = {k: sum(r["counts"][k] for r in files) for k in keys}
        lines.append("合计：%d 个文件、%d 处写入（报 %d、未判定 %d、通过 %d）" % (
            len(files), total["writes"], total["report"], total["undetermined"], total["passed"]))
    return "\n".join(lines)


def _emit(text, out_path):
    if out_path:
        with open(out_path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text + "\n")
        print("已写入 %s" % out_path)
    else:
        sys.stdout.write(text + "\n")


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    # format / out / project-dir 定义在子解析器上；不带子命令时给默认值（避免 AttributeError）
    if not hasattr(args, "format"):
        args.format = "text"
    if not hasattr(args, "out"):
        args.out = None
    if not hasattr(args, "project_dir"):
        args.project_dir = None
    try:
        results, warnings, errors = _run(args)
        env = envelope(TOOL, __version__, results=results, warnings=warnings, errors=errors)
    except EtkError as exc:
        env = envelope(TOOL, __version__, errors=[exc.to_dict()])
    except Exception as exc:  # 兜底：避免向用户抛出裸 traceback
        env = envelope(TOOL, __version__, errors=[{
            "code": E_INTERNAL,
            "message": "内部错误：%s: %s" % (exc.__class__.__name__, exc),
            "hint": "请加 --format json 复现，并把输出附在 issue 中。",
            "details": {},
        }])
    text = json.dumps(env, ensure_ascii=False, indent=2) if args.format == "json" else render_text(env)
    _emit(text, args.out)
    if not env["ok"]:
        return 1
    if args.command == "demo":
        # 自检命令：退出码只看自检本身是否通过，不看"报"桶（样例本来就有 3 处预埋问题）
        return 0 if all(r.get("ok") for r in env["results"] if r.get("kind") == "demo") else 1
    if args.command == "check":
        for res in env["results"]:
            counts = res.get("counts") or {}
            if counts.get("report"):
                return 1
            # 文件级问题（E09/E11）不对应某条写入，counts.report 不含它们：
            # 任一 result 的 findings 里有"报"桶即返回 1。
            if any(f.get("bucket") == "报" for f in res.get("findings") or []):
                return 1
            # findings 可能被 --limit 截断；report_by_class 按截断前的全部 findings 统计
            if any((counts.get("report_by_class") or {}).values()):
                return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
