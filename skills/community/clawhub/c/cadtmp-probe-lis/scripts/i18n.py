#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""海外适配轻量层：CLI --lang en|zh 双语文本与 JSON 字段（纯标准库）。

设计目标（轻量层，不改业务算法）：
- 主 CLI 增加 ``--lang en|zh``（默认 zh，不破坏现有中文用户）。
- ``--lang en --help`` 输出英文 help；``--lang zh`` 输出保持原样。
- JSON 输出的 status/message/error 字段可按 lang 本地化（status 值固定 ok/error）。
- ascii/stdout 下 en 文本不出现中文。

用法：
    raw = sys.argv[1:]
    lang = i18n.argv_lang(raw)          # 预扫描，决定 parser 用哪套 help
    i18n.add_lang_arg(parser, default=lang)
    args = parser.parse_args(raw)
    g = i18n.I18N(args.lang)
    print(g.msg("ok"))                  # "完成"/"done"
    print(g.json(status="ok", message=g.msg("ok")))
"""

try:
    import os as _boot_os, sys as _boot_sys
    _boot_here = _boot_os.path.dirname(_boot_os.path.abspath(__file__))
    if _boot_here not in _boot_sys.path:
        _boot_sys.path.insert(0, _boot_here)
except Exception:
    pass


def argv_lang(argv):
    """从命令行预扫描 ``--lang en|zh``（帮助文本必须在解析前决定语言）。"""
    lang = "zh"
    try:
        for i, item in enumerate(argv):
            if item == "--lang":
                if i + 1 < len(argv) and argv[i + 1] in ("en", "zh"):
                    lang = argv[i + 1]
                break
            if item.startswith("--lang="):
                val = item.split("=", 1)[1]
                if val in ("en", "zh"):
                    lang = val
                break
    except Exception:
        pass
    return lang


def add_lang_arg(parser, default="zh"):
    lang = default if default in ("zh", "en") else "zh"
    help_ = (
        "Output language: en English, zh Chinese (pass --lang en before --help to see English help)"
        if lang == "en"
        else "输出语言：zh 中文（默认），en English"
    )
    parser.add_argument(
        "--lang",
        choices=("zh", "en"),
        default=default,
        help=help_,
    )


_TEXTS = {
    # key -> (zh, en)
    "ok": ("完成", "done"),
    "error": ("错误", "error"),
    "not_found": ("未找到", "not found"),
    "written": ("已写入", "written"),
    "skipped": ("已跳过", "skipped"),
    "warning": ("警告", "warning"),
    "version": ("版本", "version"),
    "skill_version": ("技能版本", "skill version"),
    "output_dir": ("输出目录", "output directory"),
    "input_file": ("输入文件", "input file"),
    "processing": ("处理中", "processing"),
    "scan_done": ("扫描完成", "scan completed"),
    "regenerated": ("已完成复算", "recomputed"),
    "audit_done": ("审计完成", "audit completed"),
    "self_test_ok": ("自测通过", "self-test passed"),
    "usage_hint": ("使用 --help 查看完整用法", "run with --help for full usage"),
    "privacy_note": ("本工具本机运行，不上传图纸/文档字节", "runs locally; drawing/document bytes never leave your machine"),
    "lang_title_en": ("English", "English"),
    "lang_title_zh": ("中文", "中文"),
}

_FIELDS = {
    "ok": "ok",
    "error": "error",
    "warning": "warning",
    "skipped": "skipped",
}

_EXTRA_SKILL = {
    "skill_name": ("技能", "skill"),
    "cli": ("命令行", "CLI"),
}


def T(lang, key, **kw):
    """取双语文本：key 不存在时回退英文 key 本身；kw 支持 {k} 占位。"""
    table = _TEXTS if key in _TEXTS else _EXTRA_SKILL
    pair = table.get(key, (key, key))
    text = pair[1] if lang == "en" else pair[0]
    if kw:
        try:
            return text.format(**kw)
        except Exception:
            return text
    return text


def field(lang, key):
    """JSON 字段值：status 等语义字段固定英文 ok/error/warning；message 类按语言。"""
    if key in _FIELDS:
        return _FIELDS[key]
    return T(lang, key)


def json_result(lang, status="ok", message=None, error=None, **extra):
    """构造本地化 JSON：status 固定英文；message/error 由调用方传入已本地化文本。"""
    data = {"status": field(lang, status or "ok")}
    if message is not None:
        data["message"] = message
    if error is not None:
        data["error"] = error
    data.update(extra)
    return data


# ---- cad-file-reader 海外适配补充键（纯本地化，不改业务算法） ----
_CAD_TEXTS = {
    "read_desc": ("读取 DWG/DXF/PDF CAD 文件并输出结构化摘要与消息",
                  "Read DWG/DXF/PDF CAD files and emit structured summaries"),
    "paths_help": ("CAD 文件或文件夹", "CAD file(s) or folder(s)"),
    "json_help": ("输出 JSON 而非文本", "Output JSON instead of text"),
    "output_help": ("摘要写入该文件", "Write the summary to this file"),
    "max_text_help": ("最多纳入的文本实体数（默认 500）",
                      "Maximum text entities to include (default: 500)"),
    "render_help": ("同时用 ezdxf 生成 SVG 预览", "Also render an SVG preview with ezdxf"),
    "render_dir_help": ("SVG 预览输出目录（默认当前目录）",
                        "Directory for SVG previews (default: current directory)"),
    "recursive_help": ("递归搜索文件夹", "Search folders recursively"),
    "cap_help": ("单进程内存硬上限 MB（0=不限，默认 4096）",
                 "Single-process memory hard cap in MB (0=unlimited, default 4096)"),
    "max_file_help": ("入口大小闸：超过就不做整档解析（默认 40）",
                      "Entrance size gate in MB: above this, full parse is rejected (default 40)"),
    "allow_big_help": ("明知很大仍强行整档解析（配合 --cap-mb 使用）",
                       "Force full parse even when the file is large (use with --cap-mb)"),
    "no_files_found": ("未找到 .dwg/.dxf/.dwt 文件", "No .dwg, .dxf, or .dwt files found"),
    "preflight_fail": ("快速失败：输入不是可识别的 DWG/DXF/PDF",
                       "fast-fail: input is not a recognizable DWG/DXF/PDF"),
    "preflight_hint": ("快速失败：不假装转换成功；确认文件未被截断、未改名、不是其它格式后重试",
                       "fast-fail: no fake success; verify the file is not truncated, renamed, or another format before retrying"),
    "file_too_big": ("内存闸：文件 {mb:.0f}MB 超过入口上限 {max}MB，已拒绝整档解析",
                     "memory gate: file {mb:.0f}MB exceeds entrance limit {max}MB; full parse rejected"),
    "big_hint": ("大图纸请用 scripts/cad_scan.sh（只解文字/图层/块名，低内存）；确需整档解析再加 --allow-big",
                 "for large drawings use scripts/cad_scan.sh (text/layers/blocks only, low memory); add --allow-big to force full parse"),
    "memory_cap_error": ("内存闸：解析超出硬上限 {cap}MB 已中断（当前峰值 {peak}MB）",
                         "memory gate: parse exceeded hard cap {cap}MB and was aborted (current peak {peak}MB)"),
    "cap_hint": ("改用 scripts/cad_scan.sh，或用 --cap-mb 提高上限（别超过物理内存一半）",
                 "use scripts/cad_scan.sh, or raise --cap-mb (do not exceed half of physical RAM)"),
    "memory_cap_note": ("[cad内存闸] cap={cap} 已用峰值 RSS={peak}MB",
                        "[cad memory-gate] cap={cap} peak RSS={peak}MB"),
    "doctor_desc": ("cad-file-reader 环境分档体检（只读，不安装）",
                    "cad-file-reader environment tiered health check (read-only, no install)"),
    "doctor_title": ("[doctor] cad-file-reader 环境分档体检",
                     "[doctor] cad-file-reader environment tiers"),
    "doctor_python": ("Python: {ver} ({resolved})  vendor: {vendor}",
                      "Python: {ver} ({resolved})  vendor: {vendor}"),
    "doctor_platform": ("平台提示：{os} · 内存闸 psutil：{guard} · {hint}",
                        "Platform: {os} · memory-gate psutil: {guard} · {hint}"),
    "tier0_title": ("档 0 · 当前能力", "Tier 0 · Current capabilities"),
    "tier1_title": ("档 1 · 缺失最小修复", "Tier 1 · Minimal fixes for missing items"),
    "tier2_title": ("档 2 · DWG 转换后端", "Tier 2 · DWG conversion backends"),
    "written_to": ("已写出：{paths}", "Written: {paths}"),
    "write_json_fail": ("⚠️ 写入 JSON 报告失败：{exc}", "⚠️ failed to write JSON report: {exc}"),
    "write_md_fail": ("⚠️ 写入 Markdown 报告失败：{exc}", "⚠️ failed to write Markdown report: {exc}"),
    "md_title": ("# cad-file-reader 环境体检报告", "# cad-file-reader environment report"),
    "md_generated": ("- 生成时间：{t}", "- generated at: {t}"),
    "md_skill_root": ("- 技能根：`{p}`", "- skill root: `{p}`"),
    "md_python": ("- Python：`{p}`（resolved：`{r}`）", "- Python: `{p}` (resolved: `{r}`)"),
    "md_platform": ("- 平台提示：{os} · 内存闸 psutil：{guard} · {hint}",
                    "- Platform: {os} · memory-gate psutil: {guard} · {hint}"),
    "md_tier0": ("## 档 0 · 当前能力分档", "## Tier 0 · Current capability tiers"),
    "capability": ("能力", "Capability"),
    "tier": ("分档", "Tier"),
    "detail": ("说明", "Detail"),
    "minimal_fix": ("最小修复", "Minimal fix"),
    "md_tier1": ("## 档 1 · 缺失修复命令", "## Tier 1 · Missing fixes"),
    "none_all_ok": ("无（当前能力都可用）。", "None (all current capabilities are available)."),
    "md_tier2": ("## 档 2 · DWG 转换后端", "## Tier 2 · DWG conversion backends"),
    "status": ("状态", "Status"),
    "next_step": ("### 下一步", "### Next steps"),
    "doctor_out_dir_help": ("输出目录（默认当前目录）", "Output directory (default: current directory)"),
    "doctor_json_out_help": ("JSON 报告路径（默认 <out-dir>/doctor-report.json）",
                             "JSON report path (default <out-dir>/doctor-report.json)"),
    "doctor_md_out_help": ("Markdown 报告路径（默认 <out-dir>/doctor-report.md，仅 --skip-md 时关闭）",
                           "Markdown report path (default <out-dir>/doctor-report.md; off only with --skip-md)"),
    "doctor_skip_md_help": ("不写 Markdown 报告", "Do not write the Markdown report"),
    "doctor_no_write_help": ("不写任何文件（供测试/CI 用）", "Write nothing (for tests/CI)"),
    "doctor_json_only_help": ("只把 JSON 打到 stdout", "Print JSON to stdout only"),
    "doctor_md_only_help": ("只把 Markdown 报告打到 stdout", "Print Markdown report to stdout only"),
    "found": ("有", "available"),
    "missing": ("缺失", "missing"),
    "memory_guard_on": ("有", "available"),
    "memory_guard_off": ("无（降级为协作式超时）", "none (falls back to cooperative timeout)"),
}
_TEXTS.update(_CAD_TEXTS)
