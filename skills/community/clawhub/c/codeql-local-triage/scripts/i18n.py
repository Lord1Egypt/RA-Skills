#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Language selection for the codeql-local-triage CLI tools.

Language selection mechanism — four clearly separated tiers
============================================================
The scripts cannot "see" the user's conversation, so the language is a
*user-controlled setting*: ``--lang {zh,en,auto}`` / ``TRIAGE_LANG`` / ``AGENT_UI_LANG``
take precedence; ``auto`` follows the host locale and falls back to ``en``.
Rationale: these messages land in CI logs and terminals that are grepped, so one
predictable language per stream is the useful default — and any user who wants the
other language pins it with ``--lang``. See README → "Language selection".

Tier 1 — Explicit choice (highest priority)
    ``--lang {zh,en}`` CLI flag, or the ``TRIAGE_LANG`` environment variable
    (values like ``zh`` / ``zh-CN`` / ``en`` / ``en-US``).

Tier 2 — Agent UI hint (the "dynamic" hook)
    The hosting agent is expected to export ``AGENT_UI_LANG`` to the language
    the user is *actually writing in* (``zh`` or ``en``). When the agent invokes
    a script **without** an explicit ``--lang``, this is the signal it should
    have set. If absent, we fall back to the OS locale variables
    ``LANG`` / ``LC_ALL`` / ``LC_MESSAGES`` / ``LANGUAGE`` (a ``zh`` / ``CN`` /
    ``Hans`` / ``Hant`` substring selects Chinese).

Tier 3 — Safe default (mono-language, never bilingual)
    If nothing above resolves, default to ``en`` (English). This is a hard
    guarantee: the tool always emits exactly one language.

"auto" is just a synonym for "run the resolver": it does **NOT** mean "print
both languages". When ``--lang auto`` is given (or omitted), the resolver picks
a single language from tiers 2–3. The agent is responsible for the *dynamic*
selection (it knows the conversation language and passes ``--lang`` or sets
``AGENT_UI_LANG``); the script's ``auto`` is the deterministic fallback.
"""
from __future__ import annotations

import os
import re

_ZH_RE = re.compile(r"zh|cn|hans|hant|chinese", re.IGNORECASE)


def resolve_lang(explicit: str | None = None) -> str:
    """Resolve to exactly one of ``"zh"`` or ``"en"``.

    ``explicit`` is the value of ``--lang`` / ``TRIAGE_LANG`` / an agent hint,
    or ``None`` to fall through to locale + default.
    """
    # Tier 1: explicit CLI / env
    lang = (explicit or "").strip().lower()
    if lang and lang != "auto":
        return "zh" if _ZH_RE.search(lang) else "en"
    # Tier 2: agent hint env, then OS locale
    for var in ("AGENT_UI_LANG", "TRIAGE_LANG", "LANG", "LC_ALL",
                "LC_MESSAGES", "LANGUAGE"):
        v = os.environ.get(var, "")
        if not v:
            continue
        if _ZH_RE.search(v):
            return "zh"
        if var in ("AGENT_UI_LANG", "TRIAGE_LANG", "LANGUAGE") and re.search(r"en", v, re.I):
            return "en"
    # Tier 3: safe mono default (NEVER bilingual)
    return "en"


# Module-level current language; updated by set_lang() once argv is parsed.
_LANG = resolve_lang()


def set_lang(explicit: str | None = None) -> None:
    """Update the module-level language after ``--lang`` is parsed."""
    global _LANG
    _LANG = resolve_lang(explicit)


def tr(key: str, lang: str | None = None, **kw) -> str:
    """Return the localized string for ``key``.

    ``lang`` defaults to the module-level ``_LANG``. ``kw`` are ``.format()``
    fields; templates contain only their intended named fields (no stray
    braces), so formatting is safe.
    """
    lang = lang or _LANG
    table = MESSAGES.get(lang) or MESSAGES["en"]
    text = table.get(key)
    if text is None:
        text = MESSAGES["en"].get(key, key)
    if kw:
        try:
            return text.format(**kw)
        except (KeyError, IndexError, ValueError):
            return text
    return text


# ── Message tables ──────────────────────────────────────────────────────────
MESSAGES = {
    "en": {
        # ---- shared ----
        "lang_help": "UI language: 'auto' follows the host/user language (AGENT_UI_LANG env or OS "
                     "locale) and defaults to English; 'zh'/'en' force one language. Pass --lang to "
                     "pin the language you want; see README -> 'Language selection'.",
        "ok_label": "ok  ",
        "fail_label": "FAIL",

        # ---- scan_sensitive_sources.py ----
        "scan_desc": "Prefilter without a DB build: list Python names that may drive a CodeQL taint flow.",
        "scan_epilog": "Exit codes: 0 = no candidate source; 1 = candidate source found; "
                       "2 = input/runtime error (missing path, etc.).",
        "paths_help": "Python file(s) or directory(ies) to scan (directories recurse).",
        "json_help": "Emit machine-readable JSON (English keys).",
        "quiet_help": "Print only a per-file candidate count.",
        "summary_help": "Print a per-file summary table (file / sources / literals).",
        "jobs_help": "Parse files in parallel with N worker threads (default 1 = serial).",
        "selftest_help": "Run the built-in regex self-test and exit.",
        "err_no_paths": "Provide at least one file or directory (or use --self-test).",
        "err_jobs_range": "--jobs must be >= 1, got {got}.",
        "warn_skip_missing": "[warn] path does not exist, skipped: {p}",
        "err_missing_paths": "[error] {n} input path(s) do not exist, aborted: {paths}",
        "warn_parse_fail": "[warn] parse failed, skipped {p}: {type}: {exc}",
        "quiet_count": "{file}: {n} candidate source(s)",
        "header_file": "File under test: {file}",
        "header_real": "[Real sources (drive taint flow)] total: {n}",
        "header_literals": "[Sensitive string literals (a source only when used as a lookup key)] total: {n}",
        "hint_text": "Note: this script lists all 5 classify classes; a given query uses only part of "
                     "them —\n      py/clear-text-storage-sensitive-data uses secret / password / private,\n"
                     "      while id and certificate are explicitly excluded "
                     "(see CleartextStorageCustomizations.qll).",
        "total_count": "Total: {files} file(s) / {total} candidate source(s)",
        "summary_head": "file                                                 sources  literals",
        "summary_row": "{file:52s} {sources:8d} {lits:9d}",
        "selftest_all": "\nSelf-test: all passed",
        "selftest_some": "\nSelf-test: {bad} failed",

        # ---- read_sarif.py ----
        "read_desc": "Parse a CodeQL SARIF file and print source->sink data flows.",
        "read_epilog": "Exit codes: 0 = zero results (or --expect matched); "
                       "1 = results present or assertion failed.",
        "sarif_help": "SARIF file(s), one or more.",
        "r_json_help": "Emit machine-readable JSON (English keys).",
        "paths_only_help": "List sink locations only, do not expand the flow.",
        "expect_help": "Assert the total result count is N; exit 1 otherwise.",
        "err_file_missing": "[error] file does not exist: {p}",
        "err_parse_fail": "[error] parse failed {p}: {type}: {exc}",
        "err_not_json": "[error] {p} is not valid JSON — failed at line {line}, column {col}: {reason}",
        "err_json_near": "near: {near}",
        "err_not_sarif": "[error] {p} is valid JSON but not a CodeQL SARIF file "
                         "(no top-level \"runs\" array). "
                         "Expected a file produced by `codeql database analyze --format=sarif-latest`.",
        "err_sarif_shape": "[error] {p} has a malformed \"runs\" entry (#{idx}): {reason}",
        "how_to_fix": "how to fix: {hint}",
        "hint_sarif_json": "re-generate it with `codeql database analyze db --format=sarif-latest "
                           "--output=out.sarif <query>`; a SARIF file must be the output of "
                           "`--format=sarif-latest`, not raw scan output.",
        "hint_sarif_shape": "check the file is produced by CodeQL itself; third-party or truncated "
                            "SARIF (e.g. an interrupted download) is common.",
        "header_sarif": "SARIF: {file}",
        "header_tool": "Tool: {tool} {version}   files scanned: {artifacts}",
        "result_prefix": "\n★ Result count: {n}  -> ",
        "status_clean": "✅ clean",
        "status_alerts": "⛔ alerts",
        "flow_header": "── taint path #{fi} (source → … → sink, {steps} steps) ──",
        "total_sarif": "Total: {n} SARIF file(s) / {total} results",
        "assert_fail": "❌ assertion failed: expected {expect} results, got {total}",
        "assert_pass": "✅ assertion passed: result count = {expect}",

        # ---- bisect_taint.py ----
        "bisect_desc": "Locate a CodeQL taint source by variant bisection.",
        "bisect_epilog": "Exit codes: 0 = finished, baseline reproduced; "
                         "1 = baseline not reproduced; 2 = error.",
        "source_help": "File to modify, relative to --tree.",
        "tree_help": "Package root, copied wholesale into each variant (default: cwd).",
        "variant_help": "Literal replacement, repeatable. OLD:NEW is colon-separated; "
                        "NEW may contain colons.",
        "variant_file_help": "Swap in a whole file, repeatable (for regex surgery).",
        "workdir_help": "Where variants and artifacts are written.",
        "codeql_help": "codeql executable; if omitted, variants are only staged.",
        "query_help": "Query to run.",
        "language_help": "--language passed to database create (CodeQL build language, not UI language).",
        "dry_run_help": "Stage variants only, do not run CodeQL.",
        "err_source_missing": "[error] source file does not exist: {src}",
        "err_source_not_relative": "[error] --source must be a path relative to --tree (no absolute path, no \"..\"): {src}",
        "hint_source_relative": "pass --source as a relative path inside --tree, e.g. --source src/scan.py",
        "err_variant_bad_name": "[error] invalid variant name {name!r}: must be [A-Za-z0-9] with . _ - only, 1-64 chars",
        "hint_variant_name": "use a simple name like t2_rename; avoid slashes, \"..\" , or spaces",
        "err_workdir_too_broad": "[error] --workdir {workdir} is too broad (drive root or home dir); pick a dedicated throwaway dir",
        "err_variant_no_eq": "[error] --variant is missing the \"=\" separator: {spec!r}",
        "err_variant_no_colon": "[error] --variant {name!r} is missing the \":\" between OLD and NEW: {spec!r}",
        "err_variant_no_name": "[error] --variant has an empty name: {spec!r}",
        "err_variant_dup_name": "[error] duplicate variant name {name!r} (each name must be unique)",
        "err_variant_empty_old": "[error] --variant {name!r} has an empty OLD string "
                                 "(nothing to search for)",
        "err_variant_empty_new": "[error] --variant {name!r} has an empty NEW string "
                                 "(nothing to replace with)",
        "err_variantfile_no_eq": "[error] --variant-file is missing the \"=\" separator: {spec!r}",
        "err_variantfile_no_name": "[error] --variant-file has an empty name: {spec!r}",
        "hint_variant": "expected --variant NAME=OLD:NEW, e.g. --variant t2_rename=OLD_NAME:NEW_NAME; "
                        "NEW may contain colons. Note t1_control is added automatically — "
                        "do not use it as a variant name.",
        "hint_variant_file": "expected --variant-file NAME=PATH, e.g. --variant-file t3=/tmp/t3.py; "
                             "use this when a literal replace cannot express the change (regex surgery).",
        "variant_no_change": "[error] variant {name} produced no change "
                              "(OLD not found?): {old}",
        "err_replace_file": "[error] replacement file does not exist: {p}",
        "variant_summary": "variant {name}: {count} occurrence(s) {old} -> {new}",
        "variant_file_summary": "variant {name}: whole file swapped in from {p}",
        "workdir_header": "\nWork dir: {workdir}\nPackage root: {tree}\nSource file: {src}\n",
        "staged": "  staged {name:14s} ({lines} lines) -> {tgt}",
        "dry_run_note": "\n(CodeQL not run. Add --codeql <path> to build + analyze.)",
        "cmd_intro": "Equivalent command template:",
        "err_codeql_missing": "[error] codeql does not exist: {codeql}",
        "err_build_fail": "[error] {name} database build failed (exit {rc})",
        "err_analyze_fail": "[error] {name} analysis failed (exit {rc})",
        "warn_sarif_parse": "[warn] {name} SARIF parse failed: {type}: {exc}",
        "verdict_head": "variant            results   verdict",
        "verdict_baseline_ok": "baseline reproduced ✅",
        "verdict_baseline_fail": "⛔ baseline NOT reproduced! conclusions invalid",
        "verdict_cause": "✅ alert gone ⇒ this change is the taint source",
        "verdict_not_cause": "⛔ still fires ⇒ this change is NOT the cause",
        "verdict_parse_fail": "? parse failed",
        "warn_baseline": "\n⚠️  The baseline did not reproduce the alert: the local environment/query may "
                        "differ from the remote one; the other variants' conclusions above cannot be trusted.",
        "try_attempt": "  (attempt {attempt}/2) $ {cmd}",
        "warn_timeout": "[warn] codeql single step timed out (>{timeout}s)"
                        "{retry}",
        "retry_once": ", retrying once",
        "retry_giveup": ", retry timed out, giving up",
    },

    "zh": {
        # ---- shared ----
        "lang_help": "界面语言：'auto' 跟随宿主/用户语言（AGENT_UI_LANG 环境变量或系统 locale），默认英文；"
                     "'zh'/'en' 强制指定某一种语言。用 --lang 固定你想要的语言；见 README「语言选择」。",
        "ok_label": "ok  ",
        "fail_label": "FAIL",

        # ---- scan_sensitive_sources.py ----
        "scan_desc": "免建库预筛：枚举 Python 文件里可能驱动 CodeQL taint 的敏感名。",
        "scan_epilog": "退出码：0 = 未发现候选源；1 = 发现候选源；2 = 输入/运行错误（路径不存在等）。",
        "paths_help": "待扫的 .py 文件或目录（目录会递归）。",
        "json_help": "输出机器可读 JSON（英文 key）。",
        "quiet_help": "只打印每文件计数。",
        "summary_help": "打印每文件汇总表（文件 / 候选源 / 字面量）。",
        "jobs_help": "用 N 个工作线程并行解析文件（默认 1 = 串行）。",
        "selftest_help": "跑内置正则自检后退出。",
        "err_no_paths": "至少要给一个文件或目录（或用 --self-test）。",
        "err_jobs_range": "--jobs 必须 ≥ 1，收到 {got}。",
        "warn_skip_missing": "[warn] 路径不存在，跳过: {p}",
        "err_missing_paths": "[error] {n} 个输入路径不存在，已中止：{paths}",
        "warn_parse_fail": "[warn] 解析失败，跳过 {p}: {type}: {exc}",
        "quiet_count": "{file}: {n} 处候选源",
        "header_file": "被测文件: {file}",
        "header_real": "【真·source（会驱动 taint 流）】共 {n} 处",
        "header_literals": "【敏感字符串字面量（仅当被当 lookup key 时才是 source）】共 {n} 个",
        "hint_text": "提示：本脚本列出全部 5 类 classify。具体某条查询只取其中一部分——\n"
                     "      py/clear-text-storage-sensitive-data 用的是 secret / password / private，\n"
                     "      而 id 与 certificate 被显式排除（见 CleartextStorageCustomizations.qll）。",
        "total_count": "合计: {files} 文件 / {total} 处候选源",
        "summary_head": "文件                                                   候选源    字面量",
        "summary_row": "{file:52s} {sources:8d} {lits:9d}",
        "selftest_all": "\n自检: 全部通过",
        "selftest_some": "\n自检: {bad} 项失败",

        # ---- read_sarif.py ----
        "read_desc": "解析 CodeQL SARIF，打印 source→sink 数据流。",
        "read_epilog": "退出码：0 = 无结果（或 --expect 断言通过）；1 = 有结果或断言失败。",
        "sarif_help": "SARIF 文件（可多个）。",
        "r_json_help": "输出机器可读 JSON（英文 key）。",
        "paths_only_help": "只列 sink 位置，不展开数据流。",
        "expect_help": "断言结果总条数为 N；不符则退出码 1。",
        "err_file_missing": "[error] 文件不存在: {p}",
        "err_parse_fail": "[error] 解析失败 {p}: {type}: {exc}",
        "err_not_json": "[error] {p} 不是合法 JSON —— 在第 {line} 行第 {col} 列解析失败: {reason}",
        "err_json_near": "出错处内容: {near}",
        "err_not_sarif": "[error] {p} 是合法 JSON，但不是 CodeQL SARIF 文件"
                         "（没有顶层 \"runs\" 数组）。"
                         "应当是 `codeql database analyze --format=sarif-latest` 的产物。",
        "err_sarif_shape": "[error] {p} 的 \"runs\" 第 {idx} 项结构不合法: {reason}",
        "how_to_fix": "怎么修: {hint}",
        "hint_sarif_json": "用 `codeql database analyze db --format=sarif-latest "
                           "--output=out.sarif <query>` 重新生成；SARIF 必须是 "
                           "`--format=sarif-latest` 的产物，而不是扫描器的原始输出。",
        "hint_sarif_shape": "确认文件由 CodeQL 自己产出；第三方转存的、或下载中断截断的 SARIF 较常见。",
        "header_sarif": "SARIF: {file}",
        "header_tool": "工具: {tool} {version}   扫描文件数: {artifacts}",
        "result_prefix": "\n★ 结果数: {n}  -> ",
        "status_clean": "✅ 干净",
        "status_alerts": "⛔ 有告警",
        "flow_header": "── taint 路径 #{fi}（source → … → sink，共 {steps} 步）──",
        "total_sarif": "合计: {n} 份 SARIF / {total} 条结果",
        "assert_fail": "❌ 断言失败：期望 {expect} 条结果，实际 {total} 条",
        "assert_pass": "✅ 断言通过：结果数 = {expect}",

        # ---- bisect_taint.py ----
        "bisect_desc": "变体二分定位 CodeQL taint 源。",
        "bisect_epilog": "退出码：0 = 跑完且基线复现；1 = 基线未复现；2 = 出错。",
        "source_help": "要改的源文件（相对 --tree）。",
        "tree_help": "包根目录，整体复制进每个变体（默认当前目录）。",
        "variant_help": "字面量替换（可重复）。OLD:NEW 用冒号分隔，NEW 里可含冒号。",
        "variant_file_help": "整份替换源文件（可重复，用于正则手术类复杂改动）。",
        "workdir_help": "变体与产物的落地目录。",
        "codeql_help": "codeql 可执行文件；不给则只生成变体。",
        "query_help": "查询（默认同上）。",
        "language_help": "database create 的 --language（CodeQL 建库语言，非界面语言）。",
        "dry_run_help": "只生成变体，不跑 CodeQL。",
        "err_source_missing": "[error] 源文件不存在: {src}",
        "err_source_not_relative": "[error] --source 必须是相对 --tree 的路径（不接受绝对路径或 '..'）: {src}",
        "hint_source_relative": "--source 传 --tree 内的相对路径，例如 --source src/scan.py",
        "err_variant_bad_name": "[error] 变体名 {name!r} 非法：只能含字母数字与 . _ -，长度 1–64",
        "hint_variant_name": "用简单名字如 t2_rename；不要含斜杠、'..' 或空格",
        "err_workdir_too_broad": "[error] --workdir {workdir} 范围过大（盘符根或家目录）；请指定一个专用的临时目录",
        "err_variant_no_eq": "[error] --variant 缺少 \"=\" 分隔符: {spec!r}",
        "err_variant_no_colon": "[error] --variant {name!r} 的 OLD 与 NEW 之间缺少 \":\": {spec!r}",
        "err_variant_no_name": "[error] --variant 的变体名为空: {spec!r}",
        "err_variant_dup_name": "[error] 变体名重复 {name!r}（每个变体名必须唯一）",
        "err_variant_empty_old": "[error] --variant {name!r} 的 OLD 为空（没有可查找的内容）",
        "err_variant_empty_new": "[error] --variant {name!r} 的 NEW 为空（没有可替换成的内容）",
        "err_variantfile_no_eq": "[error] --variant-file 缺少 \"=\" 分隔符: {spec!r}",
        "err_variantfile_no_name": "[error] --variant-file 的变体名为空: {spec!r}",
        "hint_variant": "正确格式为 --variant NAME=OLD:NEW，例如 --variant t2_rename=OLD_NAME:NEW_NAME；"
                        "NEW 里可含冒号。注意 t1_control 会自动添加——不要把它当变体名用。",
        "hint_variant_file": "正确格式为 --variant-file NAME=PATH，例如 --variant-file t3=/tmp/t3.py；"
                             "当字面量替换无法表达改动时（正则手术类）用它。",
        "variant_no_change": "[error] 变体 {name} 未产生任何改动（OLD 没出现？）: {old}",
        "err_replace_file": "[error] 替换文件不存在: {p}",
        "variant_summary": "变体 {name}: {count} 处 {old} -> {new}",
        "variant_file_summary": "变体 {name}: 整份替换为 {p}",
        "workdir_header": "\n工作目录: {workdir}\n包根: {tree}\n源文件: {src}\n",
        "staged": "  已生成 {name:14s} ({lines} 行) -> {tgt}",
        "dry_run_note": "\n（未跑 CodeQL。加 --codeql <path> 执行建库+分析。）",
        "cmd_intro": "等价命令模板：",
        "err_codeql_missing": "[error] codeql 不存在: {codeql}",
        "err_build_fail": "[error] {name} 建库失败（exit {rc}）",
        "err_analyze_fail": "[error] {name} 分析失败（exit {rc}）",
        "warn_sarif_parse": "[warn] {name} 的 SARIF 解析失败: {type}: {exc}",
        "verdict_head": "变体                结果数   判定",
        "verdict_baseline_ok": "基线复现 ✅",
        "verdict_baseline_fail": "⛔ 基线未复现！结论不可信",
        "verdict_cause": "✅ 告警消失 ⇒ 该改动就是 taint 源",
        "verdict_not_cause": "⛔ 仍命中 ⇒ 该改动不是成因",
        "verdict_parse_fail": "? 解析失败",
        "warn_baseline": "\n⚠️  基线没有复现告警：本地环境/查询与远端可能不一致，"
                        "上面其它变体的结论不能采信。",
        "try_attempt": "  (尝试 {attempt}/2) $ {cmd}",
        "warn_timeout": "[warn] codeql 单步超时（>{timeout}s）{retry}",
        "retry_once": "，重试一次",
        "retry_giveup": "，重试仍超时，放弃",
    },
}
