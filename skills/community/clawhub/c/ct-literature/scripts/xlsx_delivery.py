#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ct-base · xlsx_delivery.py — Excel 结果文件交付契约（全库单一真源）

配套规范：``ct-base/references/xlsx_delivery.md``
上位依据：``BASE.md §16.8``（共享件单一真源 / 发布包自包含）、
          ``references/excel_style.md``（视觉标准，已由 excel_style.py 承载）。

职责边界（重要）
----------------
本模块只承载 **流程契约层**，不承载任何业务：

====== ============================================================ ==========
层      内容                                                         归属
====== ============================================================ ==========
L1      调色板 / 字体 / 表头 / 斑马纹 / KPI 卡 / 图表 / 列宽          excel_style.py
L2      交付语言解析 / sheet 契约 / CLI 契约 / 交付物自检            本模块
L3      记录 schema / 分布维度 / sheet 编排 / 私有词条 / 兜底报告     各技能
====== ============================================================ ==========

设计约束
--------
* **纯 stdlib、零第三方依赖**：发布闸门（shared_sync_check / publish_inject）
  与未安装 xlsxwriter 的环境也必须能安全 import 本模块。
* **不 import xlsxwriter、不 import i18n**：本模块只做「解析 + 声明 + 校验」，
  具体 ``set_lang()`` 仍由各技能调用自己的 vendored i18n。
* **绝不读取 OS locale**（2026-11-06 三技能横向事故的归纳红线）：结果文件是
  交付物，不是控制台提示；线上容器多为 en_US，按 locale 兜底会把中文用户的
  整本 workbook 渲染成英文。解析链的兜底恒为 ``zh``。
* ct-base 永不发布；本件由 ``publish_inject.py`` 注入叶子技能，运行期自包含。

接入（渐进迁移，阶段 2 执行）::

    from xlsx_delivery import resolve_report_lang, add_lang_argument, verify_workbook

    lang = resolve_report_lang(args.lang, skill="registry", title=cover_title)
    set_lang(lang)                       # 技能自己的 vendored i18n
    ...
    report = verify_workbook(out_path, expected_lang=lang)
    if not report["ok"]:
        raise RuntimeError(report["issues"])
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field

__all__ = [
    "DEFAULT_LANG", "DELIVERY_CONTRACT", "SheetSpec", "WorkbookSpec",
    "resolve_report_lang", "add_lang_argument", "verify_workbook",
    "selfcheck",
]

DEFAULT_LANG = "zh"
_CJK_RE = re.compile(r"[\u3400-\u9fff\uf900-\ufaff]")
_KEY_LEAK_RE = re.compile(r"\b(?:xlsx|sheet|kpi|col|field|block|note|banner)\.[a-z_]+\b")
_NS_MAIN = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

# 标准七步流程。既是规范正文的机器可读版，也是各技能自检的断言源。
DELIVERY_CONTRACT = {
    "version": 1,
    "steps": [
        "1. resolve_lang   — 交付语言解析（本模块；禁止 OS locale 兜底）",
        "2. coerce_input   — 归一化输入为技能自己的记录 schema（L3，各技能）",
        "3. open_workbook  — xlsxwriter.Workbook(out) + set_properties",
        "4. make_formats   — excel_style.make_formats(wb, PALETTES[skill])",
        "5. build_sheets   — 封面 → 概要/分布 → 明细 → 溯源/原始（L3，各技能）",
        "6. verify         — verify_workbook() 语言/键名/结构自检（本模块）",
        "7. close_return   — wb.close() → 返回 sheet 数 → 交付 report.xlsx",
    ],
    "filename": "report.xlsx",
    "cli_lang_choices": ["auto", "zh", "en"],
    "raw_data_never_translated": True,
    "os_locale_is_authoritative": False,
}


# ── 1. 交付语言解析（本次三技能事故的直接收敛点） ──────────────────────────
def _norm_lang(code):
    code = str(code or "").strip().lower()
    if code.startswith("zh"):
        return "zh"
    if code.startswith("en"):
        return "en"
    return None


def _skill_env_names(skill):
    """技能级 env 优先，通用 CT_LANG 兜底。

    兼容既有三条链路：CT_REGISTRY_LANG / CT_LITERATURE_LANG / CT_SAFETY_LANG。
    """
    names = []
    if skill:
        slug = re.sub(r"[^a-z0-9]+", "_", str(skill).strip().lower()).strip("_")
        # ct-registry -> CT_REGISTRY_LANG；registry -> CT_REGISTRY_LANG
        slug = re.sub(r"^ct_", "", slug)
        if slug:
            names.append("CT_%s_LANG" % slug.upper())
    names.append("CT_LANG")
    return names


def resolve_report_lang(lang="auto", *, skill="", title="", config_path=None,
                        default=DEFAULT_LANG, env=None):
    """解析结果文件 UI 语言，返回 ``'zh'`` 或 ``'en'``。

    优先级（**不含 OS locale**）：

    1. 显式 ``--lang zh|en``（CLI / 工作台高级参数）
    2. 环境变量 ``CT_<SKILL>_LANG`` → ``CT_LANG``（工作台注入当前界面语言；
       ``env`` 可显式传入字典，便于测试）
    3. 技能根 ``config.json`` 的 ``language`` 字段（持久用户选择）
    4. 封面标题含 CJK 字符 → zh（对话式 CLI 的用户输入语言信号）
    5. ``default``（默认 zh，中文用户优先）

    原始数据值不翻译；这里决定的只是界面 chrome 的语言。
    """
    explicit = _norm_lang(lang)
    if explicit and str(lang).strip().lower() != "auto":
        return explicit

    environ = env if env is not None else os.environ
    for name in _skill_env_names(skill):
        got = _norm_lang(environ.get(name))
        if got:
            return got

    if config_path is None:
        # 本模块位于 <skill>/scripts/ 或发布包 <publish>/scripts/；
        # 两种布局都把 config.json 解析到技能/发布包根，缺失则静默跳过。
        here = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(os.path.dirname(here), "config.json")
    try:
        with open(config_path, encoding="utf-8") as fh:
            got = _norm_lang(json.load(fh).get("language"))
        if got:
            return got
    except (OSError, ValueError, AttributeError):
        pass

    if title and _CJK_RE.search(str(title)):
        return "zh"
    return _norm_lang(default) or DEFAULT_LANG


def add_lang_argument(parser, default="auto", help_text=None):
    """统一 ``--lang`` CLI 契约；返回 parser 以便链式调用。"""
    parser.add_argument(
        "--lang", default=default, choices=list(DELIVERY_CONTRACT["cli_lang_choices"]),
        help=help_text or ("report UI language: auto = CT_<SKILL>_LANG / CT_LANG / "
                           "config / title language / default zh (NEVER the server "
                           "OS locale); zh | en force a language"))
    return parser


# ── 2. 声明式 sheet 契约（只声明，不强制继承） ─────────────────────────────
@dataclass(frozen=True)
class SheetSpec:
    """一张表的契约。``kind`` 决定自检时的结构期望。"""
    key: str                    # i18n key 或已解析的表名
    kind: str = "data"          # readme | summary | data | raw | evidence
    localized: bool = True      # 表名是否随语言切换
    required: bool = True


@dataclass
class WorkbookSpec:
    """技能级交付声明；供文档对齐、自检与回归用例读取。"""
    skill: str
    palette: str                                # PALETTES 的键
    sheets: list = field(default_factory=list)  # list[SheetSpec]
    out_name: str = "report.xlsx"
    lang: str = "auto"

    def resolved_lang(self, **kw):
        return resolve_report_lang(self.lang, skill=self.skill, **kw)

    def sheet_keys(self):
        return [s.key for s in self.sheets if s.required]


# ── 3. 交付物自检（纯 stdlib 读 OOXML，不依赖 openpyxl） ───────────────────
def _sheet_names(zf):
    try:
        root = ET.fromstring(zf.read("xl/workbook.xml"))
    except (KeyError, ET.ParseError):
        return []
    out = []
    for node in root.iter(_NS_MAIN + "sheet"):
        name = node.get("name")
        if name:
            out.append(name)
    return out


def _read_shared_strings(zf):
    try:
        root = ET.fromstring(zf.read("xl/sharedStrings.xml"))
    except (KeyError, ET.ParseError):
        return []
    return ["".join(n.text or "" for n in si.iter(_NS_MAIN + "t"))
            for si in root.iter(_NS_MAIN + "si")]


def _worksheet_cells(zf, member, shared):
    """Return [(cell_ref, text)] for one worksheet, resolving shared strings."""
    try:
        root = ET.fromstring(zf.read(member))
    except (KeyError, ET.ParseError):
        return []
    cells = []
    for c in root.iter(_NS_MAIN + "c"):
        ref = c.get("r") or ""
        typ = c.get("t")
        if typ == "inlineStr":
            text = "".join(n.text or "" for n in c.iter(_NS_MAIN + "t"))
        else:
            v = c.find(_NS_MAIN + "v")
            raw = (v.text or "") if v is not None else ""
            if typ == "s":
                try:
                    text = shared[int(raw)]
                except (ValueError, IndexError):
                    text = raw
            else:
                text = raw
        if text:
            cells.append((ref, text))
    return cells


def verify_workbook(path, expected_lang="zh", min_sheets=2):
    """校验已落盘的 .xlsx，返回 ``{ok, issues, sheet_names, ...}``。

    机检项（对应规范 §F 自检清单）：

    * 文件为合法 zip（OOXML）且含 ``xl/workbook.xml``
    * sheet 数量 >= ``min_sheets``；表名无 Excel 非法字符、长度 <= 31
    * 期望中文时表名至少一张含 CJK；期望英文时表名不含 CJK
    * **期望英文时界面 chrome（表头行 / A 列短标签）不得残留中文**
      （原始数据值里的中文属数据保真，只进 ``cjk_cells`` 报告，不阻断）
    * 单元格文本无 ``xlsx.*`` / ``sheet.*`` 等 i18n 键名回退残留
    * 至少一张表带冻结窗格或自动筛选（数据表可扫描性）
    """
    issues, names = [], []
    if not os.path.isfile(path):
        return {"ok": False, "issues": ["file not found: %s" % path],
                "sheet_names": []}
    try:
        with zipfile.ZipFile(path) as zf:
            bad = zf.testzip()
            if bad:
                issues.append("corrupt zip member: %s" % bad)
            names = _sheet_names(zf)
            shared = _read_shared_strings(zf)
            texts, all_cells = [], []
            for member in zf.namelist():
                if member.startswith("xl/worksheets/sheet") and member.endswith(".xml"):
                    try:
                        texts.append(zf.read(member).decode("utf-8", "ignore"))
                    except (KeyError, OSError):
                        pass
                    for ref, text in _worksheet_cells(zf, member, shared):
                        all_cells.append((member, ref, text))
                elif member == "xl/sharedStrings.xml":
                    try:
                        texts.append(zf.read(member).decode("utf-8", "ignore"))
                    except (KeyError, OSError):
                        pass
            sheet_xml = "\n".join(texts)
    except (zipfile.BadZipFile, OSError) as exc:
        return {"ok": False, "issues": ["not a valid xlsx: %s" % exc],
                "sheet_names": []}

    if not names:
        issues.append("xl/workbook.xml 未解析出 sheet 名")
    if len(names) < min_sheets:
        issues.append("sheet 数 %d < %d" % (len(names), min_sheets))
    for n in names:
        if len(n) > 31 or re.search(r"[\[\]:*?/\\]", n):
            issues.append("非法 sheet 名: %r" % n)
    has_cjk = any(_CJK_RE.search(n) for n in names)
    if expected_lang == "zh" and not has_cjk:
        issues.append("期望中文交付，但所有 sheet 名均为英文（语言回退？）")
    if expected_lang == "en" and has_cjk:
        issues.append("期望英文交付，但存在中文 sheet 名")
    cjk_cells = [(m, ref, text[:60]) for m, ref, text in all_cells
                 if _CJK_RE.search(text)]
    if expected_lang == "en":
        # 界面 chrome = 表头行（第 1 行）+ A 列短标签。数据区（含中文试验标题、
        # 中文申办方等）按数据保真红线保留原文，只报告不阻断。
        chrome = []
        for m, ref, text in all_cells:
            if not _CJK_RE.search(text):
                continue
            pos = re.match(r"([A-Z]+)(\d+)", ref)
            if not pos:
                continue
            is_header = pos.group(2) == "1"
            is_label = pos.group(1) == "A" and len(text) <= 30
            if is_header or is_label:
                chrome.append("%s=%s" % (ref, text[:24]))
        if chrome:
            issues.append("英文交付物的界面 chrome 仍含中文: %s"
                          % "; ".join(chrome[:6]))
    leaks = sorted(set(_KEY_LEAK_RE.findall(sheet_xml)))[:8]
    if leaks:
        issues.append("i18n 键名泄漏到单元格: %s" % ", ".join(leaks))
    has_pane = "state=\"frozen\"" in sheet_xml or "state='frozen'" in sheet_xml
    has_filter = "autoFilter" in sheet_xml
    if names and not (has_pane or has_filter):
        issues.append("无任何表带冻结窗格/自动筛选")

    return {"ok": not issues, "issues": issues, "sheet_names": names,
            "expected_lang": expected_lang, "sheet_count": len(names),
            "frozen_or_filter": bool(has_pane or has_filter),
            "cjk_cells": cjk_cells[:20], "cjk_cell_count": len(cjk_cells)}


# ── 4. 自带回归（零网络、零第三方依赖） ─────────────────────────────────────
def selfcheck():
    cases = [
        ("auto", "registry", "慢阻肺 / COPD", {}, "zh"),
        ("auto", "registry", "NSCLC", {"CT_REGISTRY_LANG": "en"}, "en"),
        ("en", "registry", "慢阻肺", {}, "en"),
        ("zh", "safety", "NSCLC", {"CT_SAFETY_LANG": "en"}, "zh"),
        ("auto", "literature", "", {"CT_LANG": "en"}, "en"),
        ("auto", "literature", "", {}, "zh"),
        ("auto", "ct-registry", "", {"CT_REGISTRY_LANG": "zh"}, "zh"),
    ]
    failures = []
    for lang, skill, title, env, expect in cases:
        got = resolve_report_lang(lang, skill=skill, title=title, env=env,
                                  config_path=os.path.abspath(os.devnull))
        if got != expect:
            failures.append("resolve(%r,%r,%r,%r) -> %s != %s"
                            % (lang, skill, title, env, got, expect))
    if DELIVERY_CONTRACT["os_locale_is_authoritative"]:
        failures.append("契约被篡改：OS locale 不得成为语言权威")
    if not DELIVERY_CONTRACT["raw_data_never_translated"]:
        failures.append("契约被篡改：原始数据不得翻译")
    return {"ok": not failures, "cases": len(cases), "failures": failures}


def main():
    ap = argparse.ArgumentParser(description="ct-base Excel 交付契约自检")
    ap.add_argument("--selfcheck", action="store_true", help="跑内置语言解析回归")
    ap.add_argument("--verify", help="校验一个 .xlsx 交付物")
    ap.add_argument("--expect-lang", default="zh", choices=["zh", "en"])
    args = ap.parse_args()
    if args.verify:
        rep = verify_workbook(args.verify, expected_lang=args.expect_lang)
        print(json.dumps(rep, ensure_ascii=False, indent=2))
        return 0 if rep["ok"] else 2
    rep = selfcheck()
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 0 if rep["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
