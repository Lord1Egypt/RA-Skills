#!/usr/bin/env python3
"""embedded-register-lookup：按 CMSIS-SVD 查询外设、寄存器、位域、地址与寄存器值。

示例：
  python scripts/lookup.py lookup USART1.CR1.UE --chip STM32G431
  python scripts/lookup.py fields TIM1.CR1 --svd ./STM32G431xx.svd
  python scripts/lookup.py set TIM1.CR1 CEN=1 DIR=UP --chip STM32G431
  python scripts/lookup.py diff USART1.CR1 --svd-a ./F103.svd --svd-b ./G431.svd
"""

from __future__ import annotations

import argparse
import json
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _HERE)

from etk_core import query  # noqa: E402
from etk_core.cache import load_device_cached  # noqa: E402
from etk_core.discovery import doctor_report, find_svd, list_devices  # noqa: E402
from etk_core.errors import E_INPUT_INVALID, E_INTERNAL, E_SVD_NOT_FOUND, EtkError  # noqa: E402
from etk_core.output import envelope  # noqa: E402
from etk_core.values import parse_number  # noqa: E402

TOOL = "embedded-register-lookup"
__version__ = "1.11.3"
MAX_WARNINGS_SHOWN = 20
DEMO_SVD = os.path.normpath(os.path.join(_HERE, os.pardir, "assets", "demo.svd"))


def build_parser():
    io = argparse.ArgumentParser(add_help=False)
    io.add_argument("--project-dir", metavar="DIR", help="从此目录向上查找 .etk/config.json，并在其中浅层扫描 .svd（默认当前目录）")
    io.add_argument("--format", choices=("text", "json", "md"), default="text", help="输出格式：text（默认）、json、md（Markdown 表格）")
    io.add_argument("--out", metavar="FILE", help="把输出写入文件，而不是标准输出")

    common = argparse.ArgumentParser(add_help=False, parents=[io])
    common.add_argument("--svd", metavar="PATH", help="SVD 文件路径（优先级最高）")
    common.add_argument("--chip", metavar="NAME", help="芯片名，如 STM32G431，用于在本机 CMSIS-Pack 中查找")
    common.add_argument("--demo", action="store_true", help="使用内置演示芯片（合成数据，零配置试用）")

    parser = argparse.ArgumentParser(
        prog="lookup.py",
        description="嵌入式寄存器查询器：查询 CMSIS-SVD 中的外设、寄存器与位域。",
        epilog=(
            "示例：\n"
            "  lookup.py lookup USART1.CR1.UE --chip STM32G431\n"
            "  lookup.py fields GPIOA.MODER --demo\n"
            "  lookup.py decode USART1.CR1 0x109 --write --demo\n"
            "  lookup.py macros USART1.CR1 --demo --format md\n"
            "  lookup.py diff USART1.CR1 --chip-a STM32F103C8 --chip-b STM32G431\n"
            "  lookup.py doctor\n"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--version", action="version", version="%(prog)s " + __version__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("lookup", parents=[common], help="查外设、寄存器或位域，如 USART1.CR1.UE（可给多个路径）")
    p.add_argument("paths", nargs="+", metavar="路径", help="外设.寄存器.位域，也可写 USART1->CR1")

    p = sub.add_parser("addr", parents=[common], help="地址反查，如 0x4001380C")
    p.add_argument("address", help="十六进制（0x 开头）或十进制地址")

    p = sub.add_parser("search", parents=[common], help="按名称或描述搜索，如 baud")
    p.add_argument("keyword")
    p.add_argument("--kind", choices=("peripheral", "register", "field"), help="只搜索某一层级")
    p.add_argument("--peripheral", metavar="外设", help="只在该外设内搜索")
    p.add_argument("--limit", type=int, default=50, help="最多显示条数（默认 50）")

    p = sub.add_parser("irq", parents=[common], help="查中断号：irq USART1 或 irq 37（不给参数则列出全部）")
    p.add_argument("query", nargs="?", default=None, help="中断名/外设名的一部分，或中断号")
    p.add_argument("--limit", type=int, default=100, help="最多显示条数（默认 100）")

    p = sub.add_parser("decode", parents=[common], help="按位域解码寄存器值，如 RCC.CR 0x00040002（可给多个值）")
    p.add_argument("register", help="外设.寄存器")
    p.add_argument("value", nargs="+", help="寄存器值，十六进制或十进制，可给多个")
    p.add_argument("--write", action="store_true", help="按写入方视角给提示：只读位域、未定义位、写读语义")

    p = sub.add_parser("fields", parents=[common], help="位域速查表：位范围、掩码、访问、复位（可给多个寄存器）")
    p.add_argument("paths", nargs="+", metavar="寄存器", help="外设.寄存器")

    p = sub.add_parser("diagram", parents=[common], help="寄存器位图（符号图 + 图例，可给多个寄存器）")
    p.add_argument("paths", nargs="+", metavar="寄存器", help="外设.寄存器")

    p = sub.add_parser("set", parents=[common], help="按位域赋值计算寄存器写入值，如 set TIM1.CR1 CEN=1 DIR=UP")
    p.add_argument("register", help="外设.寄存器")
    p.add_argument("assignments", nargs="+", metavar="字段=值", help="值可以是数字或字段的枚举名，可给多个")
    p.add_argument("--from", dest="from_value", default="reset", metavar="VALUE",
                   help="基准值：reset（默认，以复位值为基准）或数字")

    p = sub.add_parser("macros", parents=[common], help="生成 CMSIS 风格参考宏（_Pos/_Msk/枚举值），带出处注释")
    p.add_argument("path", help="外设、外设.寄存器 或 外设.寄存器.位域")

    p = sub.add_parser("diff", parents=[io], help="对比两份 SVD：给寄存器（全字段对比）或外设（全部寄存器）")
    p.add_argument("registers", nargs="+", metavar="寄存器或外设", help="外设.寄存器，或只给外设名做整体对比")
    p.add_argument("--svd-a", metavar="PATH", help="A 侧 SVD 文件路径")
    p.add_argument("--chip-a", metavar="NAME", help="A 侧芯片名（在本机 CMSIS-Pack 中查找）")
    p.add_argument("--svd-b", metavar="PATH", help="B 侧 SVD 文件路径")
    p.add_argument("--chip-b", metavar="NAME", help="B 侧芯片名（在本机 CMSIS-Pack 中查找）")
    p.add_argument("--all", action="store_true", help="外设整体对比时显示全部寄存器（默认只显示差异）")

    p = sub.add_parser("range", parents=[common], help="列出地址区间内的寄存器，如 range 0x40013800 0x40013FFF")
    p.add_argument("start", help="起始地址（含）")
    p.add_argument("end", help="结束地址（含）")
    p.add_argument("--limit", type=int, default=200, help="最多显示条数（默认 200）")

    p = sub.add_parser("lint", parents=[common], help="SVD 质量检查：重叠、越界、重复名、复位值超宽、中断号冲突")
    p.add_argument("--peripheral", metavar="外设", help="只检查某个外设")
    p.add_argument("--limit", type=int, default=200, help="最多显示条数（默认 200）")

    sub.add_parser("info", parents=[common], help="SVD 元信息：厂商、CPU、统计与文件哈希")
    sub.add_parser("list", parents=[common], help="列出全部外设及基地址")
    p = sub.add_parser("devices", parents=[io], help="列出本机可用的 SVD（芯片清单）")
    p.add_argument("--filter", dest="keyword", metavar="关键词", help="按文件名、设备名或路径过滤")
    p.add_argument("--limit", type=int, default=200, help="最多显示条数（默认 200）")
    sub.add_parser("doctor", parents=[io], help="环境体检：SVD 来源与数量、上手建议")
    return parser


_PATH_COMMANDS = ("lookup", "fields", "diagram")
_PATH_FUNCS = {
    "lookup": query.lookup,
    "fields": query.register_fields,
    "diagram": query.diagram,
}


def _run(args):
    if args.command in ("search", "range", "irq", "lint", "devices") and args.limit < 1:
        raise EtkError(E_INPUT_INVALID, "--limit 必须大于 0")
    if args.command == "doctor":
        return [doctor_report(args.project_dir, DEMO_SVD)], [], []
    if args.command == "devices":
        return [list_devices(args.project_dir, args.keyword, args.limit)], [], []
    if args.command == "diff":
        return _run_diff(args)
    if args.demo:
        if args.svd:
            raise EtkError(
                E_INPUT_INVALID,
                "--demo 与 --svd 不能同时使用",
                hint="二选一：用 --svd 查询真实芯片，或用 --demo 试用内置演示芯片。",
            )
        if not os.path.isfile(DEMO_SVD):
            raise EtkError(
                E_SVD_NOT_FOUND,
                "内置演示数据缺失：%s" % DEMO_SVD,
                hint="安装不完整，请重新安装技能包。",
            )
        path, selected_by = DEMO_SVD, "内置演示数据（--demo）"
        notes = ["当前使用内置演示芯片 ETK-DEMO（合成数据，非真实芯片）；真实查询请用 --svd 或 --chip。"]
        if args.chip:
            notes.append("--demo 已生效，--chip 参数被忽略。")
    else:
        path, selected_by, notes = find_svd(args.svd, args.chip, args.project_dir)
    device = load_device_cached(path)
    warnings = list(notes) + list(device.warnings)
    if args.command in _PATH_COMMANDS:
        fn = _PATH_FUNCS[args.command]
        results = []
        errors = []
        for item in args.paths:
            try:
                res = fn(device, item)
            except EtkError as exc:
                errors.append(exc.to_dict())
                continue
            res["source"]["selected_by"] = selected_by
            results.append(res)
        return results, warnings, errors
    if args.command == "addr":
        result = query.find_address(device, _parse(args.address, "地址"))
    elif args.command == "search":
        result = query.search(device, args.keyword, args.limit, args.kind, args.peripheral)
    elif args.command == "irq":
        result = query.find_interrupts(device, args.query, args.limit)
    elif args.command == "lint":
        result = query.lint(device, args.peripheral, args.limit)
    elif args.command == "decode":
        results = []
        errors = []
        for raw in args.value:
            try:
                res = query.decode(device, args.register, _parse(raw, "寄存器值"), args.write)
            except EtkError as exc:
                errors.append(exc.to_dict())
                continue
            res["source"]["selected_by"] = selected_by
            results.append(res)
        return results, warnings, errors
    elif args.command == "set":
        source_value = None if args.from_value == "reset" else _parse(args.from_value, "基准值")
        result = query.set_fields(device, args.register, args.assignments, source_value)
    elif args.command == "macros":
        result = query.macros_for(device, args.path, generator="%s v%s" % (TOOL, __version__))
    elif args.command == "range":
        result = query.find_in_range(
            device, _parse(args.start, "起始地址"), _parse(args.end, "结束地址"), args.limit)
    elif args.command == "info":
        result = query.device_info(device)
    else:
        result = query.list_peripherals(device)
    result["source"]["selected_by"] = selected_by
    return [result], warnings, []


def _run_diff(args):
    path_a, by_a, notes_a = find_svd(args.svd_a, args.chip_a, args.project_dir)
    path_b, by_b, notes_b = find_svd(args.svd_b, args.chip_b, args.project_dir)
    device_a = load_device_cached(path_a)
    device_b = load_device_cached(path_b)
    warnings = []
    warnings.extend("A 侧：%s" % item for item in list(notes_a) + list(device_a.warnings))
    warnings.extend("B 侧：%s" % item for item in list(notes_b) + list(device_b.warnings))
    if os.path.normcase(os.path.abspath(path_a)) == os.path.normcase(os.path.abspath(path_b)):
        warnings.append("两侧解析到同一份 SVD 文件，本次为自比对；要对比两份文件请用 --svd-a / --svd-b。")
    results = []
    errors = []
    for text in args.registers:
        try:
            if "." in text:
                result = query.diff_registers(device_a, device_b, text)
            else:
                result = query.diff_peripherals(device_a, device_b, text)
                result["show_all"] = bool(args.all)
        except EtkError as exc:
            errors.append(exc.to_dict())
            continue
        result["a"]["source"]["selected_by"] = by_a
        result["b"]["source"]["selected_by"] = by_b
        results.append(result)
    return results, warnings, errors


def _parse(text, what):
    try:
        return parse_number(text)
    except ValueError:
        raise EtkError(
            E_INPUT_INVALID,
            "%s %r 无法解析" % (what, text),
            hint="使用十六进制（如 0x4001380C）或十进制数字。",
        ) from None


def _footer(res):
    src = res.get("source", {})
    text = "[%s] 来源：%s（设备 %s，版本 %s）" % (
        res.get("label", ""), src.get("file", ""), src.get("device", ""), src.get("version", ""))
    if src.get("selected_by"):
        text += "，SVD 选择方式：%s" % src["selected_by"]
    return text


def _desc(name, description):
    """描述与名称相同（不少 SVD 这样写）时不重复显示。"""
    return "" if not description or description == name else description


def _semantics_extra(r):
    extras = []
    if r.get("write_semantics"):
        extras.append("写语义 %s" % r["write_semantics"])
    if r.get("read_semantics"):
        extras.append("读语义 %s" % r["read_semantics"])
    return extras


def _fmt_ranges(bits):
    return "、".join(
        "%d-%d" % (lo, hi) if lo != hi else "%d" % lo
        for lo, hi in query.bit_ranges(bits))


def _render_peripheral(res):
    head = "%s  基地址 %s  地址范围 0x%X 字节" % (res["peripheral"], res["base_address"], res["address_span"])
    extras = []
    if res.get("group"):
        extras.append("组 %s" % res["group"])
    if res.get("derived_from"):
        extras.append("派生自 %s" % res["derived_from"])
    if extras:
        head += "  " + "  ".join(extras)
    lines = [head]
    if res.get("description"):
        lines.append("说明：%s" % res["description"])
    if res.get("interrupts"):
        lines.append("中断：")
        for item in res["interrupts"]:
            desc = "  " + item["description"] if item["description"] else ""
            lines.append("  %-3d %-26s%s" % (item["value"], item["name"], desc))
    lines.append("寄存器（%d 个）：" % len(res["registers"]))
    for r in res["registers"]:
        lines.append("  %-6s %-12s %s  复位 %s  %s" % (
            r["offset"], r["name"], r["address"], r["reset"], r["access"]))
    lines.append(_footer(res))
    return lines


def _render_register(res):
    r = res["register"]
    head = "%s.%s  地址 %s  偏移 %s  宽度 %d 位  访问 %s  复位值 %s" % (
        res["peripheral"], r["name"], r["address"], r["offset"], r["size"], r["access"], r["reset"])
    extras = _semantics_extra(r)
    if extras:
        head += "  " + "  ".join(extras)
    lines = [head]
    if res.get("resolved_by") == "bare-name":
        lines.append("（按裸寄存器名解析：%s.%s；AVR/MSP430 风格）" % (res["peripheral"], r["name"]))
    if r["description"]:
        lines.append("说明：%s" % r["description"])
    sib_line = _sibling_line(res)
    if sib_line:
        lines.append(sib_line)
    for note in res.get("notes", []):
        lines.append("读改写提示：%s" % note)
    if res["fields"]:
        lines.append("位域：")
        for f in res["fields"]:
            tail = _desc(f["name"], f["description"])
            if f["write_semantics"]:
                tail += ("  " if tail else "") + "写语义 %s" % f["write_semantics"]
            if f["read_semantics"]:
                tail += ("  " if tail else "") + "读语义 %s" % f["read_semantics"]
            lines.append("  bit %-6s %-12s 访问 %-11s 复位 %d  %s" % (
                f["bits"], f["name"], f["access"], f["reset"], tail))
            for e in f["enums"]:
                lines.append("        %s = %s%s" % (e["pattern"], e["name"], "  " + e["description"] if e["description"] else ""))
    lines.append(_footer(res))
    return lines


def _render_field(res):
    f = res["field"]
    r = res["register"]
    head = "%s.%s.%s  位 %s（宽 %d）  访问 %s  复位值 %d（寄存器复位 %s）" % (
        res["peripheral"], r["name"], f["name"], f["bits"], f["width"], f["access"], f["reset"], r["reset"])
    extras = _semantics_extra(f)
    if extras:
        head += "  " + "  ".join(extras)
    lines = [head]
    if f["description"]:
        lines.append("说明：%s" % f["description"])
    if f["enums"]:
        lines.append("枚举：")
        for e in f["enums"]:
            lines.append("  %s = %s%s" % (e["pattern"], e["name"], "  " + e["description"] if e["description"] else ""))
    lines.append(_footer(res))
    return lines


def _render_cluster(res):
    lines = ["%s.%s（簇，%d 个寄存器）  基地址 %s" % (
        res["peripheral"], res["cluster"], len(res["registers"]), res["base_address"])]
    for r in res["registers"]:
        lines.append("  %-6s %-12s %s  复位 %s  %s" % (r["offset"], r["name"], r["address"], r["reset"], r["access"]))
    lines.append(_footer(res))
    return lines


def _render_address(res):
    kind = res["kind"]
    if kind == "exact":
        lines = ["%s 是寄存器地址：" % res["address"]]
        if res.get("probed_address"):
            lines.append("  （按 AVR 数据空间口径匹配：%s + 0x800000 = %s）" % (
                res["address"], res["probed_address"]))
        for m in res["matches"]:
            lines.append("  %s  偏移 %s  访问 %s  复位 %s  %s" % (
                m["path"], m["offset"], m["access"], m["reset"], m["description"]))
    elif kind == "inside_register":
        n = res["nearest"]
        lines = ["%s 位于寄存器 %s 内部（第 %d 字节，寄存器宽 %d 位）" % (
            res["address"], n["path"], n["offset_in_register"], n["size"])]
    elif kind == "gap":
        if res["nearest"]:
            n = res["nearest"]
            lines = ["%s 不是寄存器地址。最近的寄存器：%s（%s），之后 %d 字节。" % (
                res["address"], n["path"], n["address"], n["offset_in_register"])]
        else:
            lines = ["%s 不是寄存器地址，位于 %s 内，前面没有寄存器定义。" % (res["address"], res["peripheral"])]
        lines.append("SVD 中此处未定义寄存器，可能是保留区。")
    else:
        lines = ["%s 不在 SVD 定义的任何外设地址范围内。" % res["address"]]
    lines.append(_footer(res))
    return lines


def _render_search(res):
    head = "关键词 %s：共 %d 条" % (res["keyword"], res["total"])
    if res["truncated"]:
        head += "，显示前 %d 条" % len(res["matches"])
    lines = [head]
    for m in res["matches"]:
        desc = "  " + m["description"] if m["description"] else ""
        lines.append("  [%s] %s%s" % (m["kind"], m["path"], desc))
    if not res["matches"]:
        lines.append("没有匹配项。可换用英文缩写或寄存器名再试。")
    lines.append(_footer(res))
    return lines


def _render_decode(res):
    r = res["register"]
    lines = ["%s.%s  值 %s（十进制 %d）  宽 %d 位" % (
        res["peripheral"], r["name"], res["value_hex"], res["value"], r["size"])]
    for f in res["fields"]:
        enum = "  → %s" % f["enum"] if f["enum"] else ""
        lines.append("  bit %-6s %-12s = %-6s%s  %s" % (
            f["bits"], f["name"], f["value_hex"], enum, _desc(f["name"], f["description"])))
    if res["undefined_bits"]:
        lines.append("未定义位（SVD 中没有对应位域）：" + "、".join("bit %d" % b for b in res["undefined_bits"]))
    for note in res.get("write_notes", []):
        lines.append("写入提示：%s" % note)
    lines.append(_footer(res))
    return lines


def _nvic_text(item):
    hint = item.get("nvic") or {}
    if not hint.get("enable"):
        return ""
    text = "使能 %s bit %d" % (hint["enable"]["register"], hint["enable"]["bit"])
    if hint.get("clear_pending"):
        text += "；清挂起 %s bit %d" % (
            hint["clear_pending"]["register"], hint["clear_pending"]["bit"])
    if hint.get("priority"):
        prio = hint["priority"]
        text += "；优先级 %s 第 %d 字节（bit %d-%d）" % (
            prio["register"], prio["byte"], prio["bit_offset"], prio["bit_offset"] + 7)
    return text


def _render_irq(res):
    head = "中断列表" if not res["query"] else "中断筛选 %s" % res["query"]
    head += "：共 %d 条" % res["total"]
    if res["truncated"]:
        head += "，显示前 %d 条" % len(res["matches"])
    lines = [head]
    for m in res["matches"]:
        desc = "  " + m["description"] if m["description"] else ""
        lines.append("  %-3d  %-10s %-26s%s" % (m["value"], m["peripheral"], m["name"], desc))
        nvic = _nvic_text(m)
        if nvic:
            lines.append("        NVIC：%s" % nvic)
    if not res["matches"]:
        lines.append("没有匹配项。可用外设名或中断名的一部分再试。")
    lines.append(_footer(res))
    return lines


def _render_macros(res):
    return res["code"].splitlines()


def _render_fields(res):
    r = res["register"]
    lines = ["%s.%s  位域速查（宽 %d 位，复位 %s，访问 %s）" % (
        res["peripheral"], r["name"], r["size"], r["reset"], r["access"])]
    for f in res["fields"]:
        lines.append("  %-9s 位 %-6s 宽 %-2d 掩码 %s  访问 %-11s 复位 %d  %s" % (
            f["name"], f["bits"], f["width"], f["mask"], f["access"], f["reset"],
            _desc(f["name"], f["description"])))
    if res["undefined_bits"]:
        lines.append("未定义位：" + _fmt_ranges(res["undefined_bits"]))
    lines.append(_footer(res))
    return lines


def _render_diagram(res):
    r = res["register"]
    size = r["size"]
    chars = ["."] * size
    for cell in res["cells"]:
        chars[cell["bit"]] = cell["char"] or "."
    seq = [chars[i] for i in range(size - 1, -1, -1)]
    groups = ["".join(seq[i:i + 8]) for i in range(0, len(seq), 8)]
    lines = ["%s.%s  位域图（宽 %d 位，复位 %s；每 8 位一组，从左到右 bit%d..bit0）" % (
        res["peripheral"], r["name"], size, r["reset"], size - 1)]
    lines.append("  " + "|".join(groups))
    if res["legend"]:
        lines.append("  图例：" + " · ".join(
            "%s=%s b%s" % (item["char"], item["field"], item["bits"]) for item in res["legend"]))
    if res["reset_bits"]:
        lines.append("  复位为 1 的位：" + _fmt_ranges(res["reset_bits"]))
    lines.append(_footer(res))
    return lines


def _render_set(res):
    r = res["register"]
    lines = ["%s.%s  写入值计算（基准：%s %s）" % (
        res["peripheral"], r["name"], res["from"]["label"], res["from"]["value_hex"])]
    for a in res["assignments"]:
        change = "%d → %d" % (a["before"], a["value"])
        tags = []
        if a["via_enum"]:
            tags.append("枚举 %s" % a["via_enum"])
        if not a["changed"]:
            tags.append("无变化")
        suffix = "（%s）" % "，".join(tags) if tags else ""
        lines.append("  %-9s 位 %-6s %-10s %s%s" % (a["field"], a["bits"], a["given"], change, suffix))
    lines.append("结果：%s（十进制 %d）" % (res["value_hex"], res["value"]))
    if res["undefined_bits_set"]:
        lines.append("注意：结果中有 SVD 未定义的位被置 1：" + _fmt_ranges(res["undefined_bits_set"]))
    for note in res["notes"]:
        lines.append("注意：" + note)
    lines.append(_footer(res))
    return lines


def _render_diff(res):
    a, b = res["a"], res["b"]
    lines = ["%s  寄存器对比" % res["path"]]
    lines.append("  A：设备 %s（%s，基地址 %s）" % (a["source"]["device"], a["source"]["file"], a["base_address"]))
    lines.append("  B：设备 %s（%s，基地址 %s）" % (b["source"]["device"], b["source"]["file"], b["base_address"]))
    if res["register_differences"]:
        lines.append("寄存器级差异：")
        for item in res["register_differences"]:
            lines.append("  " + item)
    lines.append("字段对比（%d 个字段名）：" % len(res["fields"]))
    for row in res["fields"]:
        if row["status"] == "same":
            lines.append("  %-9s 相同（位 %s）" % (row["name"], row["a"]["bits"]))
        elif row["status"] == "only_a":
            lines.append("  %-9s 仅 A 侧有（位 %s）" % (row["name"], row["a"]["bits"]))
        elif row["status"] == "only_b":
            lines.append("  %-9s 仅 B 侧有（位 %s）" % (row["name"], row["b"]["bits"]))
        else:
            for item in row["differences"]:
                lines.append("  %-9s %s" % (row["name"], item))
    lines.append("结论：" + ("两侧寄存器定义一致。" if res["identical"]
                             else "存在上述差异；跨芯片移植代码时注意位位置与访问类型。"))
    return lines


def _render_diff_peripheral(res):
    a, b = res["a"], res["b"]
    c = res["counts"]
    lines = ["%s 外设整体对比：共 %d 个寄存器（相同 %d、有差异 %d、仅 A %d、仅 B %d）" % (
        res["path"], c["total"], c["same"], c["diff"], c["only_a"], c["only_b"])]
    lines.append("  A：设备 %s（%s）基地址 %s，%d 个寄存器" % (
        a["source"]["device"], a["source"]["file"], a["base_address"], a["register_count"]))
    lines.append("  B：设备 %s（%s）基地址 %s，%d 个寄存器" % (
        b["source"]["device"], b["source"]["file"], b["base_address"], b["register_count"]))
    if res["base_address_changed"]:
        lines.append("注意：外设基地址已变化 %s → %s，移植时注意地址引用。" % (
            a["base_address"], b["base_address"]))
    for row in res["registers"]:
        if row["status"] == "same" and not res.get("show_all"):
            continue
        if row["status"] == "only_a":
            lines.append("  [仅 A 侧有] %s" % row["name"])
        elif row["status"] == "only_b":
            lines.append("  [仅 B 侧有] %s" % row["name"])
        elif row["status"] == "same":
            lines.append("  [相同] %s" % row["name"])
        else:
            lines.append("  [有差异] %s：" % row["name"])
            for item in row["register_differences"]:
                lines.append("      寄存器级：%s" % item)
            for item in row["fields_changed"]:
                lines.append("      位域 %s：%s" % (item["name"], "；".join(item["differences"])))
            if row["fields_only_a"]:
                lines.append("      仅 A 侧位域：%s" % "、".join(row["fields_only_a"]))
            if row["fields_only_b"]:
                lines.append("      仅 B 侧位域：%s" % "、".join(row["fields_only_b"]))
            lines.append("      其余 %d 个位域相同" % row["fields_same"])
    if not res.get("show_all") and c["same"]:
        lines.append("（%d 个完全相同的寄存器已省略；加 --all 显示全部）" % c["same"])
    lines.append("结论：" + ("两侧外设定义一致。" if res["identical"]
                             else "存在上述差异；跨芯片移植代码时注意位位置与访问类型。"))
    return lines


def _render_range(res):
    head = "%s – %s 区间内的寄存器：共 %d 个" % (res["start"], res["end"], res["count"])
    if res["truncated"]:
        head += "，显示前 %d 个" % len(res["registers"])
    lines = [head]
    for m in res["registers"]:
        lines.append("  %-22s %s  宽 %-2d  %-11s 复位 %s  %s" % (
            m["path"], m["address"], m["size"], m["access"], m["reset"], m["description"]))
    if not res["registers"]:
        lines.append("区间内没有 SVD 定义的寄存器。")
    lines.append(_footer(res))
    return lines


def _render_info(res):
    lines = ["设备 %s（版本 %s）" % (res["device"], res["source"]["version"])]
    if res["description"]:
        lines.append("说明：%s" % res["description"])
    meta = []
    if res["vendor"]:
        meta.append("厂商 %s" % res["vendor"])
    if res["cpu"]:
        meta.append("CPU %s" % res["cpu"])
    if meta:
        lines.append("  ".join(meta))
    lines.append("文件：%s（%d 字节，修改时间 %s）" % (
        res["source"]["file"], res["file_size"], res["mtime"]))
    lines.append("sha256：%s" % res["sha256"])
    c = res["counts"]
    lines.append("统计：外设 %d 个（派生 %d）、寄存器 %d 个、位域 %d 个、枚举值 %d 条、警告 %d 条" % (
        c["peripherals"], c["derived_peripherals"], c["registers"], c["fields"], c["enums"], c["warnings"]))
    lines.append(_footer(res))
    return lines


def _render_list(res):
    lines = ["设备 %s：共 %d 个外设" % (res["device"], res["count"])]
    for p in res["peripherals"]:
        extra = "  派生自 %s" % p["derived_from"] if p["derived_from"] else ""
        lines.append("  %-12s %s  %d 个寄存器%s  %s" % (
            p["name"], p["base_address"], p["register_count"], extra, p["description"]))
    lines.append(_footer(res))
    return lines


def _render_lint(res):
    c = res["counts"]
    head = "SVD 质量检查：设备 %s" % res["device"]
    if res["scope"]:
        head += "（仅外设 %s）" % res["scope"]
    head += "，共 %d 条：error %d / warning %d / info %d" % (
        c["total"], c["error"], c["warning"], c["info"])
    if res["truncated"]:
        head += "，显示前 %d 条" % len(res["findings"])
    lines = [head]
    for item in res["findings"]:
        lines.append("  [%s] %s：%s" % (item["severity"], item["code"], item["message"]))
    if not res["findings"]:
        lines.append("未发现问题（检查项：寄存器重叠、位域重叠、越界、重复名、复位值超宽、中断号冲突；同偏移的别名会记为 info）。")
    lines.append(_footer(res))
    return lines


def _render_devices(res):
    head = "本机可用 SVD"
    if res["keyword"]:
        head += "（筛选 %s）" % res["keyword"]
    head += "：共 %d 个" % res["total"]
    if res["truncated"]:
        head += "，显示前 %d 个" % len(res["entries"])
    lines = [head]
    for item in res["entries"]:
        lines.append("  [%s] %-24s %s" % (item["source"], item["device"], item["path"]))
    if not res["entries"]:
        lines.append("没有找到 .svd。运行 doctor 查看各来源的具体情况，或先用 --demo 试用内置演示。")
    if res["sources"]:
        lines.append("来源：" + "；".join(
            "%s %d 个" % (s["name"], s["count"]) for s in res["sources"]))
    return lines


def _render_doctor(res):
    lines = ["环境体检：Python %s（%s）" % (res["python"], res["platform"])]
    for check in res["checks"]:
        exists, count = check["exists"], check["count"]
        if not exists:
            mark = "✗"
        elif count == 0:
            mark = "○"
        else:
            mark = "✓"
        count_text = ""
        if exists and count is not None:
            count_text = "找到 %d 个 .svd；" % count
        lines.append("  %s %s：%s%s" % (mark, check["name"], count_text, check["note"] or ""))
    lines.append("合计去重后 %d 个 .svd。" % res["total_svds"])
    for item in res["advice"]:
        lines.append("  - %s" % item)
    return lines


# ---------- Markdown 输出（--format md），可直接粘贴到文档、PR 或聊天 ----------

def _md_cell(value):
    text = "" if value is None else str(value)
    return text.replace("|", "\\|").replace("\n", " ").strip() or " "


def _md_table(headers, rows):
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join(["---"] * len(headers)) + " |"]
    for row in rows:
        lines.append("| " + " | ".join(_md_cell(c) for c in row) + " |")
    return lines


def _md_source(res):
    src = res.get("source") or {}
    bits = []
    if res.get("label"):
        bits.append(res["label"])
    if src.get("file"):
        bits.append("来源：%s（设备 %s，版本 %s）" % (src.get("file"), src.get("device"), src.get("version")))
    if src.get("selected_by"):
        bits.append("SVD 选择：%s" % src["selected_by"])
    return "_%s_" % "；".join(bits) if bits else None


def _md_semantics(item):
    extras = []
    if item.get("write_semantics"):
        extras.append("写语义 %s" % item["write_semantics"])
    if item.get("read_semantics"):
        extras.append("读语义 %s" % item["read_semantics"])
    return "；".join(extras)


def _md_finish(lines, res):
    src = _md_source(res)
    if src:
        lines += ["", src]
    return lines


def _md_peripheral(res):
    lines = ["## %s" % res["peripheral"], ""]
    meta = ["基地址 `%s`" % res["base_address"], "地址范围 `0x%X` 字节" % res["address_span"]]
    if res.get("group"):
        meta.append("组 %s" % res["group"])
    if res.get("derived_from"):
        meta.append("派生自 %s" % res["derived_from"])
    lines.append("｜".join(meta))
    if res.get("description"):
        lines += ["", res["description"]]
    if res.get("interrupts"):
        lines += ["", "**中断**", ""]
        lines += _md_table(["向量号", "名称", "说明"],
                           [[i["value"], i["name"], i["description"]] for i in res["interrupts"]])
    lines += ["", "**寄存器（%d 个）**" % len(res["registers"]), ""]
    lines += _md_table(
        ["偏移", "寄存器", "地址", "复位", "访问", "说明"],
        [[r["offset"], "`%s`" % r["name"], r["address"], r["reset"], r["access"], r["description"]]
         for r in res["registers"]])
    return _md_finish(lines, res)


def _md_field_table(fields):
    return _md_table(
        ["位", "位域", "访问", "复位", "掩码", "说明"],
        [[f["bits"], "`%s`" % f["name"], f["access"], f["reset"], f["mask"],
          "；".join(x for x in [f["description"], _md_semantics(f)] if x)]
         for f in fields])


def _md_enum_list(fields):
    lines = []
    for f in fields:
        if f["enums"]:
            items = "、".join(
                "`%s` = %s%s" % (e["pattern"], e["name"], "（%s）" % e["description"] if e["description"] else "")
                for e in f["enums"])
            lines.append("- **%s**：%s" % (f["name"], items))
    return lines


def _sibling_line(res, fmt="human"):
    """相关寄存器（置位/清位/翻转视图）提示行；无则返回 None。"""
    sib = res.get("siblings") or []
    if not sib:
        return None
    parts = "、".join("%s（%s）" % (s["name"], s["kind"]) for s in sib)
    if fmt == "md":
        return "相关寄存器：%s —— 位操作建议用它们，避免读改写" % parts
    return "相关寄存器：%s（位操作建议用置位/清位视图，避免读改写）" % parts


def _md_register(res):
    r = res["register"]
    lines = ["## %s.%s" % (res["peripheral"], r["name"]), ""]
    meta = ["地址 `%s`" % r["address"], "偏移 %s" % r["offset"], "宽 %d 位" % r["size"],
            "访问 %s" % r["access"], "复位 `%s`" % r["reset"]]
    extra = _md_semantics(r)
    if extra:
        meta.append(extra)
    lines.append("｜".join(meta))
    if r["description"]:
        lines += ["", r["description"]]
    sib_line = _sibling_line(res, fmt="md")
    if sib_line:
        lines += ["", sib_line]
    if res["fields"]:
        lines += ["", "**位域（%d 个）**" % len(res["fields"]), ""]
        lines += _md_field_table(res["fields"])
        enum_lines = _md_enum_list(res["fields"])
        if enum_lines:
            lines += ["", "**枚举**", ""] + enum_lines
    return _md_finish(lines, res)


def _md_field(res):
    f = res["field"]
    r = res["register"]
    lines = ["## %s.%s.%s" % (res["peripheral"], r["name"], f["name"]), ""]
    meta = ["位 %s（宽 %d）" % (f["bits"], f["width"]), "访问 %s" % f["access"],
            "复位 %d（寄存器复位 `%s`）" % (f["reset"], r["reset"])]
    extra = _md_semantics(f)
    if extra:
        meta.append(extra)
    lines.append("｜".join(meta))
    if f["description"]:
        lines += ["", f["description"]]
    if f["enums"]:
        lines += ["", "**枚举**", ""]
        for e in f["enums"]:
            lines.append("- `%s` = %s%s" % (
                e["pattern"], e["name"], "（%s）" % e["description"] if e["description"] else ""))
    return _md_finish(lines, res)


def _md_cluster(res):
    lines = ["## %s.%s（簇）" % (res["peripheral"], res["cluster"]), "",
             "基地址 `%s`｜%d 个寄存器" % (res["base_address"], len(res["registers"])), ""]
    lines += _md_table(
        ["偏移", "寄存器", "地址", "复位", "访问"],
        [[r["offset"], "`%s`" % r["name"], r["address"], r["reset"], r["access"]]
         for r in res["registers"]])
    return _md_finish(lines, res)


def _md_address(res):
    kind = res["kind"]
    lines = []
    if kind == "exact":
        lines.append("%s 是寄存器地址：" % res["address"])
        lines += ["- `%s` 偏移 %s 访问 %s 复位 %s %s" % (
            m["path"], m["offset"], m["access"], m["reset"], m["description"]) for m in res["matches"]]
    elif kind == "inside_register":
        n = res["nearest"]
        lines.append("%s 位于寄存器 `%s` 内部（第 %d 字节，寄存器宽 %d 位）。"
                     % (res["address"], n["path"], n["offset_in_register"], n["size"]))
    elif kind == "gap":
        if res["nearest"]:
            n = res["nearest"]
            lines.append("%s 不是寄存器地址。最近的寄存器：`%s`（%s），之后 %d 字节。此处可能是保留区。"
                         % (res["address"], n["path"], n["address"], n["offset_in_register"]))
        else:
            lines.append("%s 不是寄存器地址，位于 %s 内，前面没有寄存器定义。" % (res["address"], res["peripheral"]))
    else:
        lines.append("%s 不在 SVD 定义的任何外设地址范围内。" % res["address"])
    return _md_finish(lines, res)


def _md_search(res):
    head = "**关键词 %s**：共 %d 条" % (res["keyword"], res["total"])
    if res["truncated"]:
        head += "（显示前 %d 条）" % len(res["matches"])
    lines = [head, ""]
    lines += _md_table(["层级", "路径", "说明"],
                       [[m["kind"], "`%s`" % m["path"], m["description"]] for m in res["matches"]])
    if not res["matches"]:
        lines.append("没有匹配项。")
    return _md_finish(lines, res)


def _md_decode(res):
    r = res["register"]
    lines = ["## %s.%s 解码" % (res["peripheral"], r["name"]), "",
             "值 `%s`（十进制 %d）｜宽 %d 位" % (res["value_hex"], res["value"], r["size"]), ""]
    lines += _md_table(
        ["位", "位域", "值", "枚举", "说明"],
        [[f["bits"], "`%s`" % f["name"], f["value_hex"], f["enum"] or "", f["description"]]
         for f in res["fields"]])
    if res["undefined_bits"]:
        lines += ["", "- 未定义位（SVD 中没有对应位域）：" + _fmt_ranges(res["undefined_bits"])]
    for note in res.get("write_notes", []):
        lines += ["- 写入提示：%s" % note]
    return _md_finish(lines, res)


def _md_fields(res):
    r = res["register"]
    lines = ["## %s.%s 位域速查" % (res["peripheral"], r["name"]), "",
             "宽 %d 位｜复位 `%s`｜访问 %s" % (r["size"], r["reset"], r["access"]), ""]
    lines += _md_field_table(res["fields"])
    if res["undefined_bits"]:
        lines += ["", "- 未定义位：" + _fmt_ranges(res["undefined_bits"])]
    return _md_finish(lines, res)


def _md_diagram(res):
    r = res["register"]
    body = _render_diagram(res)
    if body and body[-1].startswith("["):
        body = body[:-1]
    lines = ["## %s.%s 位图" % (res["peripheral"], r["name"]), "", "```text"]
    lines += body
    lines += ["```"]
    return _md_finish(lines, res)


def _md_set(res):
    r = res["register"]
    lines = ["## %s.%s 写入值计算" % (res["peripheral"], r["name"]), "",
             "基准：%s `%s`" % (res["from"]["label"], res["from"]["value_hex"]), ""]
    lines += _md_table(
        ["位域", "位", "给定", "变化"],
        [[a["field"], a["bits"], a["given"], "%d → %d%s" % (
            a["before"], a["value"], "，枚举 %s" % a["via_enum"] if a["via_enum"] else "")]
         for a in res["assignments"]])
    lines += ["", "**结果：`%s`（十进制 %d）**" % (res["value_hex"], res["value"])]
    if res["undefined_bits_set"]:
        lines += ["", "- 注意：结果中有 SVD 未定义的位被置 1：" + _fmt_ranges(res["undefined_bits_set"])]
    for note in res["notes"]:
        lines += ["- 注意：%s" % note]
    return _md_finish(lines, res)


def _md_diff(res):
    a, b = res["a"], res["b"]
    lines = ["## %s 寄存器对比" % res["path"], "",
             "- A：设备 %s（%s）基地址 %s" % (a["source"]["device"], a["source"]["file"], a["base_address"]),
             "- B：设备 %s（%s）基地址 %s" % (b["source"]["device"], b["source"]["file"], b["base_address"])]
    if res["register_differences"]:
        lines += ["", "**寄存器级差异**", ""]
        lines += ["- %s" % item for item in res["register_differences"]]
    lines += ["", "**字段对比（%d 个字段名）**" % len(res["fields"]), ""]
    status_text = {"same": "相同", "only_a": "仅 A 侧有", "only_b": "仅 B 侧有", "diff": "有差异"}
    rows = []
    for row in res["fields"]:
        if row["differences"]:
            detail = "；".join(row["differences"])
        else:
            detail = "位 %s" % (row["a"] or row["b"])["bits"]
        rows.append(["`%s`" % row["name"], status_text.get(row["status"], row["status"]), detail])
    lines += _md_table(["位域", "状态", "说明"], rows)
    lines += ["", "**结论**：" + ("两侧寄存器定义一致。" if res["identical"]
                                  else "存在上述差异；跨芯片移植代码时注意位位置与访问类型。")]
    return _md_finish(lines, res)


def _md_diff_peripheral(res):
    a, b = res["a"], res["b"]
    c = res["counts"]
    lines = ["## %s 外设整体对比" % res["path"], "",
             "- A：设备 %s（%s）基地址 %s｜%d 个寄存器" % (
                 a["source"]["device"], a["source"]["file"], a["base_address"], a["register_count"]),
             "- B：设备 %s（%s）基地址 %s｜%d 个寄存器" % (
                 b["source"]["device"], b["source"]["file"], b["base_address"], b["register_count"]),
             "- 统计：共 %d；相同 %d｜有差异 %d｜仅 A %d｜仅 B %d" % (
                 c["total"], c["same"], c["diff"], c["only_a"], c["only_b"])]
    if res["base_address_changed"]:
        lines.append("- 注意：外设基地址已变化 %s → %s" % (a["base_address"], b["base_address"]))
    status_text = {"same": "相同", "only_a": "仅 A 侧有", "only_b": "仅 B 侧有", "diff": "有差异"}
    rows = []
    for row in res["registers"]:
        if row["status"] == "same" and not res.get("show_all"):
            continue
        detail = ""
        if row["status"] == "diff":
            bits = list(row["register_differences"])
            bits += ["位域 %s：%s" % (f["name"], "；".join(f["differences"])) for f in row["fields_changed"]]
            if row["fields_only_a"]:
                bits.append("仅 A 侧位域：%s" % "、".join(row["fields_only_a"]))
            if row["fields_only_b"]:
                bits.append("仅 B 侧位域：%s" % "、".join(row["fields_only_b"]))
            detail = "；".join(bits)
        rows.append(["`%s`" % row["name"], status_text.get(row["status"], row["status"]), detail])
    lines += _md_table(["寄存器", "状态", "说明"], rows)
    lines += ["", "**结论**：" + ("两侧外设定义一致。" if res["identical"]
                                  else "存在上述差异；跨芯片移植代码时注意位位置与访问类型。")]
    return lines


def _md_range(res):
    head = "%s – %s 区间内的寄存器：共 %d 个" % (res["start"], res["end"], res["count"])
    if res["truncated"]:
        head += "（显示前 %d 个）" % len(res["registers"])
    lines = [head, ""]
    lines += _md_table(
        ["寄存器", "地址", "宽", "访问", "复位", "说明"],
        [["`%s`" % m["path"], m["address"], m["size"], m["access"], m["reset"], m["description"]]
         for m in res["registers"]])
    if not res["registers"]:
        lines.append("区间内没有 SVD 定义的寄存器。")
    return _md_finish(lines, res)


def _md_irq(res):
    head = "**中断列表**" if not res["query"] else "**中断筛选 %s**" % res["query"]
    head += "：共 %d 条" % res["total"]
    if res["truncated"]:
        head += "（显示前 %d 条）" % len(res["matches"])
    lines = [head, ""]
    rows = []
    for m in res["matches"]:
        nvic = _nvic_text(m)
        desc = m["description"] + ("；NVIC %s" % nvic if nvic else "")
        rows.append([m["value"], m["peripheral"], m["name"], desc])
    lines += _md_table(["向量号", "外设", "名称", "说明"], rows)
    if not res["matches"]:
        lines.append("没有匹配项。")
    return _md_finish(lines, res)


def _md_macros(res):
    lines = ["## %s 参考宏" % res["path"], "", "```c"]
    lines += res["code"].splitlines()
    lines += ["```"]
    return _md_finish(lines, res)


def _md_info(res):
    lines = ["## 设备 %s（版本 %s）" % (res["device"], res["source"]["version"]), ""]
    if res["description"]:
        lines += [res["description"], ""]
    meta = []
    if res["vendor"]:
        meta.append("厂商 %s" % res["vendor"])
    if res["cpu"]:
        meta.append("CPU %s" % res["cpu"])
    if meta:
        lines.append("- " + "｜".join(meta))
    lines.append("- 文件：`%s`（%d 字节，修改时间 %s）" % (
        res["source"]["file"], res["file_size"], res["mtime"]))
    lines.append("- sha256：`%s`" % res["sha256"])
    c = res["counts"]
    lines.append("- 统计：外设 %d（派生 %d）、寄存器 %d、位域 %d、枚举 %d、中断 %d、警告 %d" % (
        c["peripherals"], c["derived_peripherals"], c["registers"], c["fields"], c["enums"],
        c["interrupts"], c["warnings"]))
    return _md_finish(lines, res)


def _md_list(res):
    lines = ["**设备 %s：共 %d 个外设**" % (res["device"], res["count"]), ""]
    lines += _md_table(
        ["外设", "基地址", "寄存器数", "派生自", "说明"],
        [["`%s`" % p["name"], p["base_address"], p["register_count"],
          p["derived_from"] or "", p["description"]] for p in res["peripherals"]])
    return _md_finish(lines, res)


def _md_lint(res):
    c = res["counts"]
    head = "**SVD 质量检查：设备 %s" % res["device"]
    if res["scope"]:
        head += "（仅外设 %s）" % res["scope"]
    head += "**：共 %d 条（error %d / warning %d / info %d）" % (
        c["total"], c["error"], c["warning"], c["info"])
    lines = [head, ""]
    if res["findings"]:
        lines += _md_table(
            ["级别", "检查项", "位置", "说明"],
            [[f["severity"], f["code"],
              ("%s.%s" % (f["peripheral"], f["register"] or "") + (".%s" % f["field"] if f["field"] else "")),
              f["message"]]
             for f in res["findings"]])
    else:
        lines.append("未发现问题。")
    return _md_finish(lines, res)


def _md_devices(res):
    head = "**本机可用 SVD**"
    if res["keyword"]:
        head += "（筛选 %s）" % res["keyword"]
    head += "：共 %d 个" % res["total"]
    lines = [head, ""]
    lines += _md_table(
        ["来源", "设备", "文件", "路径"],
        [[e["source"], e["device"], "`%s`" % e["file"], e["path"]] for e in res["entries"]])
    if not res["entries"]:
        lines.append("没有找到 .svd。运行 `doctor` 查看各来源的具体情况，或先用 `--demo`。")
    if res["sources"]:
        lines += ["", "- 来源：" + "；".join("%s %d 个" % (s["name"], s["count"]) for s in res["sources"])]
    return lines


def _md_doctor(res):
    lines = ["**环境体检**：Python %s（%s）" % (res["python"], res["platform"]), ""]
    for check in res["checks"]:
        exists, count = check["exists"], check["count"]
        mark = "✗" if not exists else ("○" if count == 0 else "✓")
        count_text = "找到 %d 个 .svd；" % count if exists and count is not None else ""
        lines.append("- %s %s：%s%s" % (mark, check["name"], count_text, check["note"] or ""))
    lines += ["", "- 合计去重后 %d 个 .svd。" % res["total_svds"]]
    for item in res["advice"]:
        lines.append("- %s" % item)
    return lines


_RENDERERS = {
    "peripheral": _render_peripheral,
    "register": _render_register,
    "field": _render_field,
    "cluster": _render_cluster,
    "search": _render_search,
    "decode": _render_decode,
    "fields": _render_fields,
    "diagram": _render_diagram,
    "set": _render_set,
    "diff": _render_diff,
    "diff_peripheral": _render_diff_peripheral,
    "range": _render_range,
    "irq": _render_irq,
    "macros": _render_macros,
    "info": _render_info,
    "list": _render_list,
    "lint": _render_lint,
    "devices": _render_devices,
    "doctor": _render_doctor,
    "exact": _render_address,
    "inside_register": _render_address,
    "gap": _render_address,
    "unmapped": _render_address,
}

_MD_RENDERERS = {
    "peripheral": _md_peripheral,
    "register": _md_register,
    "field": _md_field,
    "cluster": _md_cluster,
    "search": _md_search,
    "decode": _md_decode,
    "fields": _md_fields,
    "diagram": _md_diagram,
    "set": _md_set,
    "diff": _md_diff,
    "diff_peripheral": _md_diff_peripheral,
    "range": _md_range,
    "irq": _md_irq,
    "macros": _md_macros,
    "info": _md_info,
    "list": _md_list,
    "lint": _md_lint,
    "devices": _md_devices,
    "doctor": _md_doctor,
    "exact": _md_address,
    "inside_register": _md_address,
    "gap": _md_address,
    "unmapped": _md_address,
}


def render_text(env):
    lines = []
    for err in env["errors"]:
        lines.append("错误 [%s] %s" % (err["code"], err["message"]))
        if err.get("hint"):
            lines.append("  提示：%s" % err["hint"])
        details = err.get("details") or {}
        if details.get("tried"):
            lines.extend("  已尝试：%s" % item for item in details["tried"])
    warnings = env["warnings"]
    for w in warnings[:MAX_WARNINGS_SHOWN]:
        lines.append("注意：%s" % w)
    if len(warnings) > MAX_WARNINGS_SHOWN:
        lines.append("注意：另有 %d 条警告，用 --format json 查看全部" % (len(warnings) - MAX_WARNINGS_SHOWN))
    for res in env["results"]:
        renderer = _RENDERERS.get(res["kind"])
        if renderer is None:
            lines.append(json.dumps(res, ensure_ascii=False))
            continue
        lines.extend(renderer(res))
    return "\n".join(lines)


def render_md(env):
    lines = []
    if env["errors"]:
        lines.append("## 错误")
        for err in env["errors"]:
            lines.append("- **%s** %s" % (err["code"], err["message"]))
            if err.get("hint"):
                lines.append("  - 提示：%s" % err["hint"])
            for w in (err.get("details") or {}).get("tried", []):
                lines.append("  - 已尝试：%s" % w)
        lines.append("")
    if env["warnings"]:
        lines.append("## 警告")
        for w in env["warnings"]:
            lines.append("- %s" % w)
        lines.append("")
    for res in env["results"]:
        renderer = _MD_RENDERERS.get(res["kind"])
        if renderer is None:
            lines += ["```json", json.dumps(res, ensure_ascii=False, indent=2), "```"]
        else:
            lines += renderer(res)
        lines.append("")
    return "\n".join(lines).rstrip("\n")


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
    if args.format == "json":
        text = json.dumps(env, ensure_ascii=False, indent=2)
    elif args.format == "md":
        text = render_md(env)
    else:
        text = render_text(env)
    _emit(text, args.out)
    return 0 if env["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
