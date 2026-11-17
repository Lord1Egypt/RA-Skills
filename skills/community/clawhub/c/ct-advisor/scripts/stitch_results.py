#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""跨技能结果回程汇总（2026-11-09，纯代码 / 本地 / 零出站）。

补齐 handoff 的「回程」：用户分别调用多个兄弟技能后，把产物路径或文本交给
本模块，由**代码**机械解析并确定性缝合，不需要本地 LLM 做任何判断，也绝不
把这些内容发往 Coze 或任何外部端点（F33 出域红线：产物可能含 B 档涉密数据）。

2026-11-09 L3 扩展：本模块新增 `build_numeric_summary()`，从 JSON 产物中
**仅萃取字段白名单内的纯数值**，供 `interpret_results.py`（独立模块）在用户
显式 `interpret=true` 时外发请求方法学解释。原始产物文本、文件名、药名、
方案名、ID、用户原问题**一律不出域**；本模块自身仍保持零网络 import。

约束（全部由代码强制）：
  * 不 import orchestrate / refiner / cloud_brief，不发起任何 HTTP；
  * 文件读取限扩展名白名单、单文件大小上限、总文件数上限、文本截断上限；
  * 文件名含 token/secret/credential/password/.env 一律拒绝；
  * 解析失败或缺文件明确标注，绝不推断、绝不补数值、绝不生成结论。

输入 spec（JSON 字符串，或 `@path` 指向 JSON 文件）：
    {
      "question": "原始混合问题",
      "results": [
        {"tool": "ct-registry", "files": ["C:/out/report.md"], "text": "可选直接文本"},
        {"tool": "ct-safety",   "files": ["C:/out/faers_report.xlsx"]},
        {"tool": "ct-literature", "text": "可选直接文本"}
      ]
    }

输出：纯文本汇总（由调用方 entry.py::_emit_plain 统一加
<<<CT_ANSWER_END>>> / checksum / answer_file）。
"""
from __future__ import annotations

import csv
import io
import json
import math
import re
import zipfile
import xml.etree.ElementTree as ET
from pathlib import Path

ALLOWED_EXT = {".md", ".txt", ".log", ".json", ".csv", ".tsv", ".xlsx"}
MAX_FILE_BYTES = 2 * 1024 * 1024      # 单文件 2 MB
MAX_FILES = 20                        # 单次最多 20 个产物
MAX_CHARS_PER_FILE = 4000             # 单产物进正文的字符上限
MAX_TEXT_CHARS = 4000                 # 直接 text 字段上限
DENY_NAME_PARTS = ("token", "secret", "credential", "password", ".env")
_CJK = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff]")
_XLSX_NS = "{http://schemas.openxmlformats.org/spreadsheetml/2006/main}"

_JSON_KEYS = ("status", "total_count", "n_trials", "total", "count", "prr", "ror",
              "ebgm", "ic", "brief", "landscape", "projects", "measures",
              "summary", "note", "source", "missing", "partial_sources")

# ── L3 脱敏数值摘要（2026-11-09，用户拍板「允许脱敏数值摘要外发」）──────────
# 只认这些**统计量语义键**，值必须是有限数值；任何字符串 / 路径 / 名称 / ID
# 都不进入摘要。键名归一为小写后比对，避免大小写变体绕过白名单。
_NUMERIC_ALLOWLIST = {
    # 样本量 / 效能
    "n", "n_total", "ntotal", "n_per_group", "npergroup", "power", "alpha",
    "beta", "effect_size", "effectsize", "dropout", "p1", "p2", "margin", "delta",
    # 不相称性 / 区间
    "prr", "ror", "ic", "ebgm", "ci_lower", "cilower", "ci_upper", "ciupper",
    "lower", "upper", "chisq", "case_count", "casecount", "total_count",
    "event_count", "a", "b", "c", "d",
    # 通用统计量
    "estimate", "stderr", "z", "pvalue", "p_value", "hr", "or", "mean", "sd",
}
_NUMERIC_MAX_KEYS = 12                 # 单次最多外发 12 个数值
_NUMERIC_MAX_ABS = 1e9                 # 超出视为异常 / ID，拒绝
_SAFE_KEY = re.compile(r"^[a-z0-9_]{1,32}$")


def _zh(text: str) -> bool:
    return bool(_CJK.search(text or ""))


def _clip(text: str, cap: int = MAX_CHARS_PER_FILE) -> str:
    text = (text or "").replace("\r\n", "\n").strip()
    if len(text) <= cap:
        return text
    return text[:cap] + "\n…（已截断，完整内容见原始产物）"


def _safe_path(raw: str) -> tuple[Path | None, str]:
    """解析并校验产物路径；返回 (Path, 错误说明)。"""
    try:
        p = Path(str(raw)).expanduser().resolve()
    except Exception as e:  # noqa: BLE001
        return None, "路径解析失败：%s" % type(e).__name__
    low = p.name.lower()
    if any(part in low for part in DENY_NAME_PARTS):
        return None, "拒绝读取疑似凭据文件"
    if p.suffix.lower() not in ALLOWED_EXT:
        return None, "扩展名不在白名单（%s）" % (p.suffix or "无")
    if not p.is_file():
        return None, "文件不存在或不是普通文件"
    try:
        if p.stat().st_size > MAX_FILE_BYTES:
            return None, "文件超过 %d MB 上限" % (MAX_FILE_BYTES // 1024 // 1024)
    except OSError as e:
        return None, "无法读取文件大小：%s" % type(e).__name__
    return p, ""


def _parse_md(text: str) -> str:
    lines = [ln.rstrip() for ln in text.splitlines() if ln.strip()]
    heads = [ln for ln in lines if ln.lstrip().startswith("#")]
    tables = [ln for ln in lines if ln.lstrip().startswith("|")]
    numeric = [ln for ln in lines if re.search(r"\d", ln)][:6]
    parts = []
    if heads:
        parts.append("标题：" + " / ".join(_clip(h, 80) for h in heads[:5]))
    if tables:
        parts.append("表格行（前 3）：" + " / ".join(_clip(t, 120) for t in tables[:3]))
    if numeric:
        parts.append("含数值行（前 6）：" + " / ".join(_clip(n, 120) for n in numeric))
    if not parts:
        parts.append("正文预览：" + _clip("\n".join(lines[:12]), 600))
    return "\n".join("- " + x for x in parts)


def _parse_json(text: str) -> str:
    try:
        obj = json.loads(text)
    except Exception as e:  # noqa: BLE001
        return "- JSON 解析失败（%s），按纯文本预览：%s" % (
            type(e).__name__, _clip(text[:300], 300))
    if not isinstance(obj, dict):
        return "- 顶层为 %s，元素数 %d" % (type(obj).__name__, len(obj) if isinstance(obj, list) else 1)
    lines = []
    for k in _JSON_KEYS:
        if k in obj:
            v = obj[k]
            if isinstance(v, (dict, list)):
                v = "%s（%d 项）" % (type(v).__name__, len(v))
            lines.append("- %s: %s" % (k, _clip(str(v), 160)))
    if not lines:
        keys = list(obj.keys())[:10]
        lines = ["- 顶层键：" + ", ".join(keys)]
    return "\n".join(lines)


def _parse_csv(text: str, suffix: str) -> str:
    delim = "\t" if suffix == ".tsv" else ","
    try:
        rows = list(csv.reader(io.StringIO(text), delimiter=delim))
    except Exception:  # noqa: BLE001
        return "- 表格解析失败，按纯文本预览：" + _clip(text[:300], 300)
    if not rows:
        return "- 空表格"
    head = rows[0][:8]
    preview = [" | ".join(r[:8]) for r in rows[1:4]]
    out = ["- 表头：" + " | ".join(head), "- 数据行数：%d" % max(0, len(rows) - 1)]
    if preview:
        out.append("- 前 3 行：" + " / ".join(_clip(x, 160) for x in preview))
    return "\n".join(out)


def _parse_xlsx(p: Path) -> str:
    """stdlib zipfile + ElementTree 读表头与行数（不依赖 openpyxl）。"""
    try:
        with zipfile.ZipFile(p) as z:
            names = z.namelist()
            shared = []
            if "xl/sharedStrings.xml" in names:
                root = ET.fromstring(z.read("xl/sharedStrings.xml"))
                for si in root.findall(_XLSX_NS + "si"):
                    shared.append("".join(t.text or "" for t in si.iter(_XLSX_NS + "t")))
            sheets = sorted(n for n in names
                            if n.startswith("xl/worksheets/sheet") and n.endswith(".xml"))
            if not sheets:
                return "- xlsx 内无工作表"
            root = ET.fromstring(z.read(sheets[0]))
            rows = []
            for row in root.iter(_XLSX_NS + "row"):
                vals = []
                for c in row.findall(_XLSX_NS + "c"):
                    v = c.find(_XLSX_NS + "v")
                    txt = "" if v is None else (v.text or "")
                    if c.get("t") == "s" and txt.isdigit() and int(txt) < len(shared):
                        txt = shared[int(txt)]
                    vals.append(txt)
                rows.append(vals)
                if len(rows) >= 4:
                    break
            head = rows[0][:8] if rows else []
            return ("- 工作表：%s（共 %d 个）" % (sheets[0], len(sheets))
                    + "\n- 表头：" + " | ".join(head)
                    + "\n- 预览行：" + " / ".join(" | ".join(r[:8]) for r in rows[1:4]))
    except Exception as e:  # noqa: BLE001
        return "- xlsx 解析失败（%s），仅记录文件名" % type(e).__name__


def _parse_file(p: Path) -> str:
    suffix = p.suffix.lower()
    if suffix == ".xlsx":
        return _parse_xlsx(p)
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return "- 读取失败：%s" % type(e).__name__
    text = _clip(text)
    if suffix == ".json":
        return _parse_json(text)
    if suffix in (".csv", ".tsv"):
        return _parse_csv(text, suffix)
    return _parse_md(text)


def stitch(spec: dict) -> str:
    """确定性缝合：返回纯文本汇总。任何异常都转成可见说明，不抛给出口。"""
    question = str(spec.get("question") or "")
    results = spec.get("results") or []
    zh = _zh(question) or not question
    if not isinstance(results, list):
        results = []
    title = "## 跨技能结果汇总（本地代码缝合，未出站）" if zh else \
            "## Cross-skill result summary (local code stitching, no egress)"
    lines = [title, ""]
    if question:
        lines.append(("原始问题：%s" if zh else "Original question: %s") % question)
        lines.append("")
    if not results:
        lines.append("⚠️ " + ("未提供任何技能产物，无可汇总内容。" if zh else
                             "No skill outputs supplied; nothing to stitch."))
        return "\n".join(lines)

    used = 0
    for idx, item in enumerate(results):
        if not isinstance(item, dict):
            continue
        tool = str(item.get("tool") or ("unknown-%d" % (idx + 1)))
        lines.append("### %s" % tool)
        files = item.get("files") or []
        if not isinstance(files, list):
            files = [files]
        direct = str(item.get("text") or "")
        blocks = []
        if direct.strip():
            blocks.append(("- 直接文本：" if zh else "- Supplied text: ")
                          + _clip(direct, MAX_TEXT_CHARS))
        for raw in files:
            if used >= MAX_FILES:
                blocks.append("- ⚠️ " + ("达到单次文件数上限，余下产物未读取。" if zh
                                     else "File limit reached; remaining outputs not read."))
                break
            p, err = _safe_path(str(raw))
            if err:
                blocks.append("- `%s`：%s" % (raw, err))
                continue
            used += 1
            blocks.append("- `%s`%s" % (p.name, "：" if zh else ":"))
            blocks.append(_parse_file(p))
        if not blocks:
            blocks.append("- ⚠️ " + ("该技能未附产物路径或文本，未汇总。" if zh
                                 else "No output path or text supplied for this skill."))
        lines.extend(blocks)
        lines.append("")

    disclaimer = (
        "⚠️ 本汇总由本地代码**机械解析**各技能产物生成：未调用云端精校、未经人工复核、"
        "非审计级，不得用于注册申报、信号判定或临床决策。ct-advisor 不改写、不推断、"
        "不补数值；结论一律以各技能原始产物为准。产物内容全程留在本机，未发生任何出站。"
        if zh else
        "⚠️ This summary was produced by local code mechanically parsing skill outputs: "
        "no cloud refinement, no human review, not audit-grade — do not use for regulatory "
        "submissions, signal decisions or clinical decisions. ct-advisor does not rewrite, "
        "infer or fill in numbers; rely on each skill's original output. All content stayed "
        "local — no egress occurred.")
    lines.extend(["---", "", disclaimer])
    return "\n".join(lines)


def _walk_numeric(obj: dict, out: dict, depth: int = 0) -> None:
    """递归（≤3 层）收集白名单内的纯数值；跳过 list / 字符串 / bool / 异常值。"""
    if depth > 3 or not isinstance(obj, dict):
        return
    for k, v in obj.items():
        if len(out) >= _NUMERIC_MAX_KEYS:
            return
        key = str(k).strip().lower()
        if isinstance(v, dict):
            _walk_numeric(v, out, depth + 1)
            continue
        if not _SAFE_KEY.match(key) or key not in _NUMERIC_ALLOWLIST:
            continue
        if isinstance(v, bool) or not isinstance(v, (int, float)):
            continue
        f = float(v)
        if not math.isfinite(f) or abs(f) > _NUMERIC_MAX_ABS:
            continue
        out.setdefault(key, int(v) if isinstance(v, int) else round(f, 6))


def build_numeric_summary(spec: dict) -> tuple[dict, str]:
    """从 spec 的 **JSON 产物** 中萃取字段白名单内的纯数值摘要（零网络）。

    🔴 F33：只读取结构化 `.json` 文件的数值字段；md / csv / xlsx 正文、
    自由文本 (`text`)、文件名、路径、药名、方案名、ID、**用户原问题**
    一律不进入本摘要，也不随之外发。解析失败 / 文件缺失只记入 note，
    绝不推断、绝不补数值。

    Returns:
        ``(summary, note)`` —— summary 形如 ``{"prr": 1.23, "power": 0.8}``；
        note 为可读的跳过说明（供答案标注，本身也不含敏感值）。
    """
    results = spec.get("results") or []
    if not isinstance(results, list):
        return {}, "results 非列表，未萃取任何数值"
    summary: dict = {}
    scanned = 0
    skipped = 0
    for item in results:
        if not isinstance(item, dict):
            continue
        files = item.get("files") or []
        if not isinstance(files, list):
            files = [files]
        for raw in files:
            p, err = _safe_path(str(raw))
            if err:
                skipped += 1
                continue
            if p.suffix.lower() != ".json":
                continue
            scanned += 1
            try:
                obj = json.loads(p.read_text(encoding="utf-8", errors="replace"))
            except Exception:  # noqa: BLE001
                skipped += 1
                continue
            _walk_numeric(obj, summary, 0)
            if len(summary) >= _NUMERIC_MAX_KEYS:
                break
        if len(summary) >= _NUMERIC_MAX_KEYS:
            break
    bits = ["扫描 JSON 产物 %d 个，萃取白名单数值 %d 个" % (scanned, len(summary))]
    if skipped:
        bits.append("跳过 %d 个（路径被拒 / 解析失败）" % skipped)
    if not summary:
        bits.append("无可外发的脱敏数值")
    return summary, "；".join(bits)


def interpret_question(summary: dict, zh: bool = True) -> str:
    """代码构造的**纯方法学问题**（绝不复用用户原问题，避免身份信息出域）。"""
    items = "; ".join("%s=%s" % (k, v) for k, v in sorted(summary.items()))
    if zh:
        return (
            "请仅从方法学角度解释以下**脱敏统计量**的含义与判读边界：\n"
            + items + "\n\n"
            "这些数值来自临床研究技能产物，已脱敏，不含任何药物名、方案名、"
            "受试者信息、试验编号或原始文本。要求：① 只解释统计含义、前提假设与"
            "适用边界，不推断、不补齐、不改写数值，不反推原始数据；② 不做信号判定、"
            "不给临床或注册结论；③ 答案标注「方法学解释，非取数结果」并列出所依据的"
            "权威方法学出处；④ 不要要求补充原始数据，也不要调用取数技能。"
        )
    return (
        "Explain, from a methodology standpoint only, the meaning and interpretation "
        "boundaries of the following **sanitized statistics**:\n" + items + "\n\n"
        "These values come from clinical-research skill outputs and are sanitized: "
        "no drug name, protocol name, subject data, trial ID or original text is present. "
        "Requirements: (1) explain only statistical meaning, assumptions and applicability "
        "limits — do not infer, complete or rewrite values, and do not reconstruct raw data; "
        "(2) make no signal determination and give no clinical or regulatory conclusion; "
        "(3) label the answer 'methodology explanation, not a data result' and cite "
        "authoritative methodology sources; (4) do not ask for raw data or invoke "
        "any retrieval skill."
    )


def load_spec(spec_arg: str) -> dict:
    """解析 --stitch 的 JSON 字符串或 `@path`；失败返回 {}（永不抛异常）。"""
    try:
        if spec_arg.startswith("@"):
            spec_path = Path(spec_arg[1:]).expanduser().resolve()
            if spec_path.stat().st_size > MAX_FILE_BYTES:
                return {}
            raw = spec_path.read_text(encoding="utf-8")
        else:
            raw = spec_arg
        obj = json.loads(raw)
        return obj if isinstance(obj, dict) else {}
    except Exception:  # noqa: BLE001
        return {}


def run_stitch(spec_arg: str) -> str:
    """entry.py --stitch 的入口：解析 spec 并返回汇总文本（永不抛异常）。"""
    try:
        if spec_arg.startswith("@"):
            spec_path = Path(spec_arg[1:]).expanduser().resolve()
            if spec_path.stat().st_size > MAX_FILE_BYTES:
                return "⚠️ spec 文件超过大小上限，已拒绝读取。"
            raw = spec_path.read_text(encoding="utf-8")
        else:
            raw = spec_arg
        spec = json.loads(raw)
        if not isinstance(spec, dict):
            return "⚠️ stitch spec 必须是 JSON 对象。"
        return stitch(spec)
    except Exception as e:  # noqa: BLE001 - 任何失败都给人读提示，不让 stdout 变空
        return "⚠️ 回程汇总失败：%s: %s\n\n请检查 --stitch 的 JSON 格式与产物路径。" % (
            type(e).__name__, e)


if __name__ == "__main__":
    import sys
    print(run_stitch(sys.argv[1] if len(sys.argv) > 1 else "{}"))
