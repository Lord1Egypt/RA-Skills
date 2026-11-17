#!/usr/bin/env python3
"""Report whether Python sources are original work or derived from a reference.

Two independent measurements, because either alone is easy to defeat:

  literal     — identical source lines, ignoring lines that are forced by the
                language or that form a public interface
  structural  — identical AST shapes after normalising away local names, so a
                copy survives renaming every variable

Verdict is derivative if either measurement crosses the threshold, or if any
file is byte-identical to its reference.
"""
import argparse
import ast
import difflib
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOL_VERSION = "1.3.3"
THRESHOLD_DEFAULT = 3

# why: a caller who can raise the bar arbitrarily turns the tool into a rubber
#      stamp — the ceiling is the largest residue observed across the measured
#      population, so anything above it cannot be justified by evidence
THRESHOLD_CEILING = 8

MEASURED_POPULATION = 363
MEASURED_LINES = 26078
THRESHOLD_BASIS = (
    f"Measured across {MEASURED_POPULATION} independently rewritten modules "
    f"({MEASURED_LINES} lines): longest identical expressive run had median 1, "
    f"P90 2, maximum 8. 34 of {MEASURED_POPULATION} modules reached 3 or more, "
    f"so 3 marks the point where similarity stops looking like convergence. "
    f"Thresholds above {THRESHOLD_CEILING} are refused because no observation "
    f"supports them."
)

_COMPOUND = re.compile(r"^(if|elif|else|for|while|with|try|except|finally)\b")
IMMUTABLE_EXACT = {"pass", "return", "continue", "break", "else:", "try:",
                   "raise", "finally:", "yield"}
IMMUTABLE_PREFIXES = ("import ", "from ", "def ", "class ", "async def ", "@")


# --------------------------------------------------------------------- shared

def strip_docstrings(code: str) -> str | None:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return None
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                node.body = body[1:] or [ast.Pass()]
    try:
        return ast.unparse(ast.fix_missing_locations(tree))
    except Exception:  # noqa: BLE001
        return None


def code_lines(text: str | None) -> list[str]:
    if not text:
        return []
    return [ln.strip() for ln in text.split("\n")
            if ln.strip() and not ln.strip().startswith("#")]


def sha256_of(paths: list[Path], base: Path) -> str:
    """Digest of a source set: content plus relative path, order-independent."""
    h = hashlib.sha256()
    for path in sorted(paths, key=lambda p: p.relative_to(base).as_posix()):
        h.update(path.relative_to(base).as_posix().encode())
        h.update(b"\x00")
        h.update(path.read_bytes())
        h.update(b"\x00")
    return "sha256:" + h.hexdigest()


def python_files(root: Path) -> list[Path]:
    if root.is_file():
        return [root] if root.suffix == ".py" else []
    return [p for p in sorted(root.rglob("*.py")) if "__pycache__" not in p.parts]


# -------------------------------------------------------------- literal layer

def _is_control_flow(line: str) -> bool:
    s = line.strip()
    return s.endswith(":") and bool(_COMPOUND.match(s))


def _single_stmt(line: str) -> ast.stmt | None:
    try:
        tree = ast.parse(line.strip())
    except SyntaxError:
        return None
    return tree.body[0] if len(tree.body) == 1 else None


def _is_schema_field(line: str) -> bool:
    node = _single_stmt(line)
    if not isinstance(node, ast.AnnAssign):
        return False
    if not isinstance(node.target, ast.Name) or node.target.id.startswith("_"):
        return False
    if node.value is None:
        return True
    return all(isinstance(n, (ast.Constant, ast.Tuple, ast.List, ast.Set,
                              ast.Dict, ast.UnaryOp, ast.Load))
               for n in ast.walk(node.value))


def _is_field_binding(line: str) -> bool:
    node = _single_stmt(line)
    if not isinstance(node, ast.Assign) or len(node.targets) != 1:
        return False
    t = node.targets[0]
    return (isinstance(t, ast.Attribute) and isinstance(t.value, ast.Name)
            and t.value.id == "self" and isinstance(node.value, ast.Name))


def _is_assertion(line: str) -> bool:
    return isinstance(_single_stmt(line), ast.Assert) if line.strip().startswith("assert") else False


def classify(line: str) -> str | None:
    """Why an identical line is not evidence of copying, or None if it is."""
    s = line.strip()
    if not s:
        return None
    if s.startswith(("import ", "from ")):
        return "import"
    if s.startswith("@"):
        return "decorator"
    if s.startswith(("def ", "async def ", "class ")):
        return "signature"
    if s in IMMUTABLE_EXACT:
        return "keyword"
    if _is_control_flow(s):
        return "control_flow"
    if _is_schema_field(s):
        return "schema_field"
    if _is_field_binding(s):
        return "field_binding"
    if _is_assertion(s):
        return "behaviour_assertion"
    if s.startswith(IMMUTABLE_PREFIXES):
        return "signature"
    return None


def _indexed_code_lines(code: str) -> list[tuple[str, int]]:
    """Code lines with original line numbers; docstrings/comments skipped.

    Mirrors code_lines() but keeps line numbers so the full report can point at
    real locations. Docstring lines (first statement of module/func/class) are
    dropped, matching strip_docstrings()'s behaviour.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []
    doc_ranges = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef,
                             ast.AsyncFunctionDef, ast.ClassDef)):
            body = node.body
            if (body and isinstance(body[0], ast.Expr)
                    and isinstance(body[0].value, ast.Constant)
                    and isinstance(body[0].value.value, str)):
                doc_ranges.append((body[0].lineno, body[0].end_lineno))
    out: list[tuple[str, int]] = []
    for i, ln in enumerate(code.split("\n"), 1):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if any(a <= i <= b for a, b in doc_ranges):
            continue
        out.append((s, i))
    return out


def longest_literal_run(reference: str, ours: str) -> tuple[int, list[tuple[str, int]]]:
    a = _indexed_code_lines(strip_docstrings(reference) or reference)
    b = _indexed_code_lines(strip_docstrings(ours) or ours)
    best: int = 0
    best_items: list[tuple[str, int]] = []
    for blk in difflib.SequenceMatcher(None, [x[0] for x in a],
                                       [x[0] for x in b]).get_matching_blocks():
        if blk.size < 1:
            continue
        run: list[tuple[str, int]] = []
        for text, lineno in b[blk.b:blk.b + blk.size]:
            if classify(text):
                if len(run) > best:
                    best, best_items = len(run), list(run)
                run = []
                continue
            run.append((text, lineno))
        if len(run) > best:
            best, best_items = len(run), list(run)
    return best, best_items


# ----------------------------------------------------------- structural layer

class _Shape(ast.NodeVisitor):
    """Render a statement as a name-independent shape string.

    `why`: renaming every local defeats literal comparison. Local identifiers
           collapse to a positional slot while call targets, attributes and
           literals stay — calling a *different* function is a real difference,
           whereas storing the same call in `acc` instead of `total` is not.
    """

    def __init__(self) -> None:
        self.parts: list[str] = []
        self._slots: dict[str, str] = {}

    def slot(self, name: str) -> str:
        if name not in self._slots:
            self._slots[name] = f"v{len(self._slots)}"
        return self._slots[name]

    def render(self, node: ast.AST) -> str:
        self.parts = []
        self.visit(node)
        return " ".join(self.parts)

    def generic_visit(self, node: ast.AST) -> None:
        self.parts.append(type(node).__name__)
        super().generic_visit(node)

    def visit_Name(self, node: ast.Name) -> None:
        self.parts.append(f"Name:{self.slot(node.id)}")

    def visit_Attribute(self, node: ast.Attribute) -> None:
        # why: attribute names are interface, not a local choice — keep them
        self.parts.append(f"Attr:{node.attr}")
        self.visit(node.value)

    def visit_Call(self, node: ast.Call) -> None:
        self.parts.append("Call")
        if isinstance(node.func, ast.Name):
            self.parts.append(f"Fn:{node.func.id}")
        else:
            self.visit(node.func)
        for arg in node.args:
            self.visit(arg)
        for kw in node.keywords:
            self.parts.append(f"Kw:{kw.arg}")
            self.visit(kw.value)

    def visit_Constant(self, node: ast.Constant) -> None:
        self.parts.append(f"Const:{node.value!r}")

    def visit_arg(self, node: ast.arg) -> None:
        self.parts.append(f"Arg:{self.slot(node.arg)}")


def statement_shapes(code: str) -> list[tuple[str, int]]:
    """Shape string and source line for each executable statement body.

    Signatures are skipped: identical interfaces are not copied expression, and
    including them would inflate every run. Schema fields and constructor field
    bindings are skipped too, mirroring the literal layer: a clean-room rewrite
    must keep its public dataclass interface, so flagging those as "copied shape"
    would wrongly call a legitimate rewrite derived (see review Aime, 众测).
    """
    tree = ast.parse(code)
    src_lines = code.split("\n")
    out: list[tuple[str, int]] = []
    skip_lines: set[int] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            if (len(node.body) == 1 and isinstance(node.body[0], ast.Return)
                    and isinstance(node.body[0].value, ast.Name)):
                skip_lines.add(node.lineno - 1)
                skip_lines.add(node.body[0].lineno - 1)
    for node in ast.walk(tree):
        if not isinstance(node, ast.stmt):
            continue
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef,
                             ast.Import, ast.ImportFrom)):
            continue
        line_txt = (src_lines[node.lineno - 1]
                    if 1 <= getattr(node, "lineno", 0) <= len(src_lines) else "")
        if isinstance(node, ast.AnnAssign) and _is_schema_field(line_txt):
            continue
        if isinstance(node, ast.Assign) and _is_field_binding(line_txt):
            continue
        if isinstance(node, (ast.Return, ast.Assign, ast.AnnAssign)):
            if getattr(node, "lineno", 0) - 1 in skip_lines:
                continue
        shaper = _Shape()
        try:
            out.append((shaper.render(node), getattr(node, "lineno", 0)))
        except RecursionError:
            continue
    out.sort(key=lambda item: item[1])
    return out


def longest_structural_run(reference: str, ours: str) -> tuple[int, list[tuple[str, int]]]:
    try:
        ref_shapes = statement_shapes(strip_docstrings(reference) or reference)
        our_shapes = statement_shapes(strip_docstrings(ours) or ours)
    except SyntaxError:
        return 0, []
    a = [s for s, _ in ref_shapes]
    b = [s for s, _ in our_shapes]
    best: int = 0
    best_items: list[tuple[str, int]] = []
    for blk in difflib.SequenceMatcher(None, a, b).get_matching_blocks():
        if blk.size > best:
            best = blk.size
            best_items = our_shapes[blk.b:blk.b + blk.size]
    return best, best_items


# ------------------------------------------------------------------- auditing

def audit(target: Path, reference: Path | None, threshold: int) -> dict:
    files = python_files(target)
    base = target if target.is_dir() else target.parent
    ref_base = reference if (reference and reference.is_dir()) else (
        reference.parent if reference else None)

    exemptions: dict[str, int] = {}
    literal_findings: list[dict] = []
    structural_findings: list[dict] = []
    unparsable: list[str] = []
    uncompared: list[str] = []
    identical: list[str] = []
    compared: list[Path] = []
    worst_literal = worst_structural = 0

    for path in files:
        rel = path.relative_to(base).as_posix()
        text = path.read_text(encoding="utf-8", errors="replace")
        if strip_docstrings(text) is None:
            unparsable.append(rel)
            continue

        ref_text = None
        if reference is not None:
            candidate = reference / rel if reference.is_dir() else reference
            if candidate.is_file():
                ref_text = candidate.read_text(encoding="utf-8", errors="replace")
            else:
                uncompared.append(rel)
        if ref_text is None:
            continue

        compared.append(path)
        for ln in code_lines(strip_docstrings(text) or text):
            reason = classify(ln)
            if reason:
                exemptions[reason] = exemptions.get(reason, 0) + 1

        # why: every expressive line can sit between two signatures, which makes
        #      run-length report "original" for a byte-identical copy
        if code_lines(strip_docstrings(text) or text) == \
                code_lines(strip_docstrings(ref_text) or ref_text):
            identical.append(rel)

        lit_run, lit_items = longest_literal_run(ref_text, text)
        if lit_run >= threshold:
            literal_findings.append({"path": rel, "run": lit_run,
                                     "lines": [{"text": t, "line": n}
                                               for t, n in lit_items[:12]]})
        worst_literal = max(worst_literal, lit_run)

        st_run, st_items = longest_structural_run(ref_text, text)
        if st_run >= threshold:
            structural_findings.append({"path": rel, "run": st_run,
                                        "shapes": [{"shape": s, "line": n}
                                                   for s, n in st_items[:12]]})
        worst_structural = max(worst_structural, st_run)

    if reference is None or not compared:
        # no reference at all, or a reference was given but it matched none of
        # our files — in both cases there is nothing to compare against, so the
        # result cannot be treated as a pass (see SKILL.md boundary notes)
        verdict = "unknown"
    elif (worst_literal >= threshold or worst_structural >= threshold
          or identical):
        verdict = "derivative"
    else:
        verdict = "original"

    for f in literal_findings:
        f["level"] = _risk_level(f["run"], threshold)
        f["kind"] = "literal"
        f["fix"] = _literal_fix(f)
    for f in structural_findings:
        f["level"] = _risk_level(f["run"], threshold)
        f["kind"] = "structural"
        f["fix"] = _structural_fix(f)
    literal_findings.sort(key=lambda f: -f["run"])
    structural_findings.sort(key=lambda f: -f["run"])

    all_findings = literal_findings + structural_findings
    by_level = {"high": 0, "medium": 0, "low": 0}
    for f in all_findings:
        by_level[f["level"]] += 1
    summary = {
        "total": len(all_findings),
        "by_level": by_level,
        "by_type": {"literal": len(literal_findings),
                    "structural": len(structural_findings)},
    }

    return {
        "verdict": verdict,
        "files": len(files),
        "compared": len(compared),
        "threshold": threshold,
        "summary": summary,
        "literal": {"max_run": worst_literal, "findings": literal_findings},
        "structural": {"max_run": worst_structural, "findings": structural_findings},
        "identical_files": identical,
        "exemptions": exemptions,
        "unparsable": unparsable,
        "uncompared": uncompared,
        "evidence": {
            "tool_version": TOOL_VERSION,
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "target_digest": sha256_of(files, base) if files else "sha256:empty",
            "reference_digest": (sha256_of(python_files(reference), ref_base)
                                 if reference is not None else "none"),
            "threshold_basis": THRESHOLD_BASIS,
            "method": ("literal: identical source lines excluding language-forced "
                       "and interface lines; structural: identical AST shapes with "
                       "local names normalised, call targets and attributes kept"),
        },
    }


# -------------------------------------------------------------------- reports

def render_text(r: dict) -> str:
    out = [
        f"verdict     : {r['verdict']}",
        f"files       : {r['files']} ({r['compared']} compared)",
        f"literal     : {r['literal']['max_run']} lines",
        f"structural  : {r['structural']['max_run']} statements",
        f"threshold   : {r['threshold']}",
    ]
    if r["identical_files"]:
        out += ["", "byte-identical to reference:"]
        out += [f"  {p}" for p in r["identical_files"][:10]]
    if r["literal"]["findings"]:
        out += ["", "literal matches (identical source lines):"]
        for f in r["literal"]["findings"][:6]:
            out.append(f"  {f['run']:>4} lines  {f['path']}  [{f['level']}]")
            out += [f"           L{it['line']}: {it['text'][:64]}" for it in f["lines"][:3]]
    if r["structural"]["findings"]:
        out += ["", "structural matches (same code, names differ):"]
        for f in r["structural"]["findings"][:6]:
            out.append(f"  {f['run']:>4} stmts  {f['path']}  [{f['level']}]")
            out += [f"           L{it['line']}: {it['shape'][:64]}" for it in f["shapes"][:3]]
    if r["exemptions"]:
        out += ["", "identical but exempt (not evidence of copying):"]
        out += [f"  {n:>5}  {k}" for k, n in sorted(r["exemptions"].items())]
    if r["unparsable"]:
        out += ["", f"unparsable  : {', '.join(r['unparsable'][:5])}"]
    if r["uncompared"]:
        out += ["", f"no reference: {', '.join(r['uncompared'][:5])}"]
    if r["evidence"]["reference_digest"] != "none" and r["compared"] == 0:
        out += ["", "⚠ 无有效比对：--reference 未匹配到任何文件，结论为 unknown，"
                "不可作为通过依据。"]
    if r["literal"]["findings"] or r["structural"]["findings"]:
        out += ["", "修复建议:"]
        for f in (r["literal"]["findings"] + r["structural"]["findings"])[:6]:
            out += [f"  [{f['level']}] {f['path']} ({f['kind']}, 连续 {f['run']})",
                    f"     {f['fix'][:200]}"]
    return "\n".join(out)


def render_markdown(r: dict, payment_notice: bool = True) -> str:
    ev = r["evidence"]
    out = [
        "# 代码所有权体检报告",
        "",
        f"- **判定**：`{r['verdict']}`",
        f"- **阈值**：{r['threshold']} （连续相同达到此数即认定为演绎）",
        f"- **字面相同**：{r['literal']['max_run']} 行",
        f"- **结构相同**：{r['structural']['max_run']} 条语句",
        f"- **文件**：共 {r['files']} 个，实际比对 {r['compared']} 个",
        "",
        "## 存档信息",
        "",
        "| 项 | 值 |",
        "|---|---|",
        f"| 工具版本 | {ev['tool_version']} |",
        f"| 生成时间 | {ev['generated_at']} |",
        f"| 待检指纹 | `{ev['target_digest']}` |",
        f"| 参照指纹 | `{ev['reference_digest']}` |",
        "",
        "指纹覆盖全部 `.py` 内容与相对路径，与文件顺序无关。"
        "源码任一字节变化都会改变指纹，可用于日后复核本报告对应的正是同一份代码。",
        "",
        "## 判定方法",
        "",
        ev["method"],
        "",
        "## 阈值依据",
        "",
        ev["threshold_basis"],
    ]
    if r["identical_files"]:
        out += ["", "## 与参照完全相同的文件", ""]
        out += [f"- `{p}`" for p in r["identical_files"]]
    if r["literal"]["findings"]:
        out += ["", "## 字面相同片段", ""]
        for f in r["literal"]["findings"]:
            out += [f"### `{f['path']}` — {f['run']} 行（风险等级：{LEVEL_ZH[f['level']]}）", "", "```python"]
            out += [f"# L{it['line']}\n{it['text']}" for it in f["lines"]]
            out += ["```", ""]
    if r["structural"]["findings"]:
        out += ["", "## 结构相同片段", "",
                "以下语句在改名之后仍然结构一致。局部变量已归一化为槽位，"
                "调用目标与属性名保留 —— 换个变量名不会改变这里的结论。", ""]
        for f in r["structural"]["findings"]:
            out += [f"### `{f['path']}` — {f['run']} 条语句（风险等级：{LEVEL_ZH[f['level']]}）", "", "```"]
            out += [f"# L{it['line']}\n{it['shape']}" for it in f["shapes"]]
            out += ["```", ""]
    if r["literal"]["findings"] or r["structural"]["findings"]:
        out += ["", "## 修复建议", "",
                "以下为针对每个命中片段的具体修复方向。"]
        for f in (r["literal"]["findings"] + r["structural"]["findings"]):
            out += [f"### [{LEVEL_ZH[f['level']]}] `{f['path']}`（{f['kind']}，连续 {f['run']}）", "",
                    f["fix"], ""]
    if r["exemptions"]:
        out += ["", "## 相同但豁免的行", "",
                "以下相同属于必然而非抄袭：同一件事在 Python 中只有这一种写法，"
                "或它们构成公开接口，改动即破坏调用方。", "",
                "| 类别 | 行数 |", "|---|---|"]
        out += [f"| {k} | {n} |" for k, n in sorted(r["exemptions"].items())]
    if r["unparsable"]:
        out += ["", "## 无法解析", ""] + [f"- `{p}`" for p in r["unparsable"]]
    if r["uncompared"]:
        out += ["", "## 参照中缺少对应文件", ""] + [f"- `{p}`" for p in r["uncompared"]]
    if r["evidence"]["reference_digest"] != "none" and r["compared"] == 0:
        out += ["", "## ⚠ 无有效比对", "",
                "本次提供了 `--reference`，但未匹配到任何文件，结论为 `unknown`。",
                "该结果**不可作为通过依据**，请确认参照路径与文件结构对应。"]
    # why: the placeholder only makes sense on an *unpaid* report; the certified
    #      deliverable appends a real signed block, so suppress it there.
    if payment_notice:
        out += ["", "## 付款认证", "",
                "本报告由本地 `audit.py` 离线生成。付费后将以「付款认证」块追加"
                "支付宝交易号与服务器签名回执，证明本次审计已付费解锁完整报告。"]
    out += ["", "---", "",
            "本报告为工程判断，用于自查与风险排序，不构成法律意见。"]
    return "\n".join(out) + "\n"


# ------------------------------------------------------- freemium tier helpers

LEVEL_ZH = {"high": "高", "medium": "中", "low": "低"}


def _risk_level(run: int, threshold: int) -> str:
    """Map a consecutive-match run to a severity tier.

    why: a longer identical run is harder to explain as convergent coincidence,
    so severity scales with the run, anchored to the evidence floor.
    """
    if run >= threshold + 3:
        return "high"
    if run >= threshold + 1:
        return "medium"
    return "low"


def _literal_fix(f: dict) -> str:
    n = f["run"]
    return (f"该文件与参照存在 {n} 行连续完全相同的代码，构成演绎风险。"
            "建议：(1) 若逻辑确为独立实现，请用你自己的表述重写——仅改变量名不够，"
            "需改变实现思路或控制流结构；(2) 若确属必要复用，在 module.yaml 标注来源仓库、"
            "commit 与许可，并保留 # SPDX-License-Identifier 头；"
            "(3) 高风险的整段相同应优先在净室重写链路（~/cleanroom）重新产出。")


def _structural_fix(f: dict) -> str:
    n = f["run"]
    return (f"该文件与参照在改名之后仍有 {n} 条语句结构一致，说明实现路径被复制。"
            "建议：(1) 重构关键函数的实现顺序或算法选择，使结构层不再命中阈值；"
            "(2) 对不可避免的公共接口保留即可，但需证明其在被豁免类别之外确为独立；"
            "(3) 优先将该模块纳入净室重写，从 seed 库重新拼接而非改写上游。")


def build_preview(r: dict) -> dict:
    """Free tier: risk counts, type distribution, one-line summaries only.

    Deliberately withholds code locations, line numbers and fix suggestions, so
    the user sees the value without the paid detail (lowers decision cost).
    """
    lits = r["literal"]["findings"]
    strs = r["structural"]["findings"]
    allf = lits + strs
    by_level = {"high": 0, "medium": 0, "low": 0}
    for f in allf:
        by_level[f["level"]] = by_level.get(f["level"], 0) + 1
    rank = {"high": 3, "medium": 2, "low": 1}
    items = []
    for f in sorted(allf, key=lambda x: (-rank[x["level"]], -x["run"])):
        kind = "字面相同" if f["kind"] == "literal" else "结构相同"
        items.append({
            "level": f["level"],
            "kind": f["kind"],
            "summary": f"{f['path']}：{f['run']} 处{kind}（{LEVEL_ZH[f['level']]}风险）",
        })
    return {
        "tier": "preview",
        "verdict": r["verdict"],
        "threshold": r["threshold"],
        "total_findings": len(allf),
        "by_level": by_level,
        "by_type": {"literal": len(lits), "structural": len(strs)},
        "items": items,
        "note": "以上为免费预览：仅展示风险数量、类型与一句话摘要。"
                "具体代码位置、行号、详细分析与修复建议需付费解锁完整报告。",
        "evidence": {
            "tool_version": r["evidence"]["tool_version"],
            "generated_at": r["evidence"]["generated_at"],
        },
    }


def render_preview_text(prev: dict) -> str:
    bl = prev["by_level"]
    bt = prev["by_type"]
    out = [
        f"判定        : {prev['verdict']}",
        f"风险总数    : {prev['total_findings']}",
        f"  高风险    : {bl['high']}",
        f"  中风险    : {bl['medium']}",
        f"  低风险    : {bl['low']}",
        f"类型分布    : 字面相同 {bt['literal']} 处 / 结构相同 {bt['structural']} 处",
        f"阈值        : {prev['threshold']}",
        "",
        "风险摘要（每条约一句话，无代码位置 / 无修复建议）：",
    ]
    for it in prev["items"]:
        out.append(f"  [{LEVEL_ZH[it['level']]}] {it['summary']}")
    out += ["", prev["note"]]
    return "\n".join(out)


def render_preview_markdown(prev: dict) -> str:
    bl = prev["by_level"]
    bt = prev["by_type"]
    out = [
        "# 代码所有权体检 · 免费预览报告",
        "",
        f"- **判定**：`{prev['verdict']}`",
        f"- **风险总数**：{prev['total_findings']}（高 {bl['high']} / 中 {bl['medium']} / 低 {bl['low']}）",
        f"- **类型分布**：字面相同 {bt['literal']} 处，结构相同 {bt['structural']} 处",
        f"- **阈值**：{prev['threshold']}",
        "",
        "## 风险摘要",
        "",
        "> 预览仅展示数量、类型与一句话摘要。代码位置、行号、详细分析与修复建议"
        "需付费解锁完整报告。",
        "",
    ]
    for it in prev["items"]:
        out.append(f"- [{LEVEL_ZH[it['level']]}] {it['summary']}")
    out += ["", "---", "", prev["note"], "",
            f"> 工具版本 {prev['evidence']['tool_version']} · 生成于 {prev['evidence']['generated_at']}"]
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Audit whether Python sources are original or derived.")
    ap.add_argument("target", help="File or directory to audit")
    ap.add_argument("--reference", help="Upstream file or directory to compare against")
    ap.add_argument("--threshold", type=int, default=THRESHOLD_DEFAULT,
                    help=f"Consecutive matches that count as derived "
                         f"(default {THRESHOLD_DEFAULT}, max {THRESHOLD_CEILING})")
    ap.add_argument("--json", action="store_true", help="Machine-readable output")
    ap.add_argument("--report", help="Write an archivable Markdown report here")
    ap.add_argument("--tier", choices=["preview", "full"], default="full",
                    help="preview=免费预览(数量/类型/一句话摘要, 无位置无修复); "
                         "full=完整报告(位置/行号/详情/修复建议). 默认 full")
    ap.add_argument("--version", action="version", version=TOOL_VERSION)
    args = ap.parse_args(argv)

    if args.threshold < 1:
        print("error: threshold must be at least 1", file=sys.stderr)
        return 2
    if args.threshold > THRESHOLD_CEILING:
        print(f"error: threshold {args.threshold} exceeds the evidence floor of "
              f"{THRESHOLD_CEILING}. {THRESHOLD_BASIS}", file=sys.stderr)
        return 2

    target = Path(args.target)
    if not target.exists():
        print(f"error: target not found: {target}", file=sys.stderr)
        return 2
    reference = Path(args.reference) if args.reference else None
    if reference is not None and not reference.exists():
        print(f"error: reference not found: {reference}", file=sys.stderr)
        return 2

    report = audit(target, reference, args.threshold)

    if args.tier == "preview":
        prev = build_preview(report)
        if args.report:
            dest = Path(args.report)
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(render_preview_markdown(prev), encoding="utf-8")
        print(json.dumps(prev, ensure_ascii=False, indent=2) if args.json
              else render_preview_text(prev))
        return 0

    if args.report:
        dest = Path(args.report)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(render_markdown(report), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2) if args.json
          else render_text(report))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
