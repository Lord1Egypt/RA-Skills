#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""扫描 Codex 四层规则，输出重复簇与冲突项（只读，不修改被扫文件）。

四层：
  memory  : ${CODEX_HOME}/memories/memory_summary.md
  agents  : ${CODEX_HOME}/AGENTS.md
  rules   : ${CODEX_HOME}/rules/*.md + ${CODEX_HOME}/rules/default.rules
  lessons : ${CODEX_HOME}/lessons/LESSONS.md + ${CODEX_HOME}/lessons/archive/*.md

抽取：`- ` 列表、数字编号、Markdown 表格行、default.rules 的 prefix_rule。
重复：归一化后完全相同 -> exact；difflib >= 0.85 -> near（带极性保护）。
冲突：已知键（context_window、auto_compact、预算、版本、路径、日期）同键不同值。

输出（默认写到本 skill 的 outputs/ 下）：
  <skill>/outputs/duplicate-conflict-20261109.json
  <skill>/outputs/duplicate-conflict-20261109.md

边界：只报告，不自动合并、不删行；冲突项交用户决策。
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime
from difflib import SequenceMatcher
from pathlib import Path

SCHEMA_VERSION = 1
TOOL = "scan_layers.py"
NEAR_THRESHOLD = 0.85
EXACT_MIN_NORM = 6
NEAR_MIN_NORM = 10
MAX_TEXT = 4000
MAX_NEAR_CANDIDATES = 220
MAX_CLUSTER_MEMBERS = 10

LAYER_ORDER = ["memory", "agents", "rules", "lessons"]
LAYER_LABEL = {
    "memory": "记忆摘要",
    "agents": "全局 AGENTS",
    "rules": "rules/*.md + default.rules",
    "lessons": "LESSONS.md + archive",
}
LAYER_PRIORITY = {"agents": 0, "rules": 1, "memory": 2, "lessons": 3}
CURRENT_LAYERS = {"memory", "agents", "rules"}

NEG_MARKERS = (
    "禁止", "不得", "不要", "不做", "不能", "不可", "避免", "绝不", "勿",
    "无需", "不用", "不删", "不改", "不上", "不把", "不将", "不写", "不输出",
    "不重试", "不覆盖", "不静默", "不盲", "不猜", "不伪造", "不冒充",
)
NORMATIVE_MARKERS = (
    "禁止", "不得", "必须", "红线", "紧急停止", "stop", "公司数据", "密钥",
    "删除", "覆盖", "权限", "不上云", "审计", "发布需", "预授权", "provider",
    "base_url", "认证", "计费", "sha-256", "备份", "回滚", "验证",
)
DETAIL_MARKERS = ("命令", "脚本", "参数", "路径", "示例", "日志", "表", "字段", "rsync", "python", "git")

BULLET_RE = re.compile(r"^\s*[-*+]\s+")
NUMBERED_RE = re.compile(r"^\s*\d+[.)、]\s+")
PREFIX_RULE_RE = re.compile(r"^\s*prefix_rule\s*\(")
TABLE_SEP_RE = re.compile(r"^\s*\|?[\s:|\-]+\|?\s*$")
FENCE_RE = re.compile(r"^\s*(```|~~~)")


def now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def sha256_hex(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def display_path(path: Path, codex_home: Path) -> str:
    try:
        rel = path.resolve().relative_to(codex_home.resolve())
        return "${CODEX_HOME}/" + str(rel)
    except Exception:
        return str(path)


def normalize_rule(text: str) -> str:
    """NFKC + 去标点/空格/全半角差异，保留字母数字与 CJK。"""
    s = unicodedata.normalize("NFKC", text).strip()
    s = BULLET_RE.sub("", s)
    s = NUMBERED_RE.sub("", s)
    if s.startswith("|") and s.endswith("|"):
        s = s[1:-1]
    s = s.replace("**", "").replace("__", "").replace("`", "")
    chars = []
    for ch in s:
        if ch.isalnum():
            chars.append(ch.lower())
    return "".join(chars)


def norm_prefix_rule(text: str) -> str:
    """把 prefix_rule 归一成 decision:命令词，便于同层比较。"""
    decision = "allow"
    m = re.search(r'decision\s*=\s*"([^"]+)"', text)
    if m:
        decision = m.group(1)
    cmd = []
    m = re.search(r"pattern\s*=\s*\[(.*?)\]", text)
    if m:
        cmd = re.findall(r'"([^"]*)"', m.group(1))
    return decision + ":" + normalize_rule(" ".join(cmd))


def is_table_row(line: str) -> bool:
    s = line.strip()
    return s.startswith("|") and s.count("|") >= 2


def is_table_separator(line: str) -> bool:
    s = line.strip()
    return bool(s) and "-" in s and bool(TABLE_SEP_RE.match(s))


def classify_rule_line(line: str) -> str | None:
    if PREFIX_RULE_RE.match(line):
        return "prefix_rule"
    if BULLET_RE.match(line):
        return "bullet"
    if NUMBERED_RE.match(line):
        return "numbered"
    if is_table_row(line):
        return "table"
    return None


def extract_records(path: Path, layer: str, codex_home: Path) -> tuple[list[dict], dict]:
    raw = path.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    lines = text.splitlines()
    records: list[dict] = []
    in_fence = False
    skipped = Counter()

    for idx, line in enumerate(lines, start=1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            skipped["fence_line"] += 1
            continue
        if in_fence:
            skipped["inside_fence"] += 1
            continue
        if not line.strip():
            skipped["blank"] += 1
            continue
        if is_table_separator(line):
            skipped["table_separator"] += 1
            continue
        # 表头：下一行是分隔行
        if is_table_row(line) and idx < len(lines) and is_table_separator(lines[idx]):
            skipped["table_header"] += 1
            continue

        kind = classify_rule_line(line)
        if kind is None:
            skipped["not_rule"] += 1
            continue

        if len(line) > MAX_TEXT:
            skipped["too_long"] += 1
            continue

        if kind == "prefix_rule":
            normalized = norm_prefix_rule(line)
        else:
            normalized = normalize_rule(line)

        if not normalized:
            skipped["empty_after_norm"] += 1
            continue
        if kind != "prefix_rule" and len(normalized) < EXACT_MIN_NORM:
            skipped["too_short"] += 1
            continue

        records.append({
            "layer": layer,
            "file": str(path),
            "display": display_path(path, codex_home),
            "line": idx,
            "text": line.strip(),
            "normalized": normalized,
            "rule_kind": kind,
            "bytes": len(line.encode("utf-8")),
        })

    meta = {
        "layer": layer,
        "path": str(path),
        "display": display_path(path, codex_home),
        "bytes": len(raw),
        "sha256": sha256_hex(raw),
        "lines": len(lines),
        "rule_lines": len(records),
        "skipped": dict(skipped),
    }
    return records, meta


def discover_files(codex_home: Path) -> list[tuple[str, Path]]:
    specs: list[tuple[str, Path]] = []

    def add(layer: str, path: Path) -> None:
        if path.exists() and path.is_file():
            specs.append((layer, path))

    add("memory", codex_home / "memories" / "memory_summary.md")
    add("agents", codex_home / "AGENTS.md")
    rules_dir = codex_home / "rules"
    if rules_dir.exists():
        for p in sorted(rules_dir.glob("*.md")):
            add("rules", p)
    add("rules", rules_dir / "default.rules")
    add("lessons", codex_home / "lessons" / "LESSONS.md")
    archive_dir = codex_home / "lessons" / "archive"
    if archive_dir.exists():
        for p in sorted(archive_dir.glob("*.md")):
            add("lessons", p)

    # 去重并保持层顺序
    seen = set()
    out: list[tuple[str, Path]] = []
    for layer, path in specs:
        key = str(path.resolve())
        if key in seen:
            continue
        seen.add(key)
        out.append((layer, path))
    out.sort(key=lambda item: (LAYER_ORDER.index(item[0]), str(item[1])))
    return out


def has_negation(text: str) -> bool:
    return any(marker in text for marker in NEG_MARKERS)


def polarity_compatible(a: str, b: str) -> bool:
    return has_negation(a) == has_negation(b)


def bigrams(s: str) -> set[str]:
    if len(s) < 2:
        return {s} if s else set()
    return {s[i:i + 2] for i in range(len(s) - 1)}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def occurrence_key(occ: dict) -> tuple:
    return (occ["file"], occ["line"])


def make_cluster(kind: str, members: list[dict], similarity: float, cluster_id: str) -> dict:
    occurrences = []
    for rec in members:
        occurrences.append({
            "layer": rec["layer"],
            "file": rec["file"],
            "display": rec["display"],
            "line": rec["line"],
            "text": rec["text"],
            "rule_kind": rec["rule_kind"],
            "bytes": rec["bytes"],
        })
    occurrences.sort(key=lambda x: (LAYER_PRIORITY.get(x["layer"], 9), x["file"], x["line"]))
    layers = sorted({o["layer"] for o in occurrences}, key=lambda x: LAYER_PRIORITY.get(x, 9))
    files = sorted({o["file"] for o in occurrences})
    gross = sum(o["bytes"] for o in occurrences)
    keep = pick_keep(occurrences, layers)
    recommendation = recommend(layers, keep, occurrences)
    return {
        "id": cluster_id,
        "kind": kind,
        "similarity": round(similarity, 4),
        "layers": layers,
        "layer_labels": [LAYER_LABEL.get(x, x) for x in layers],
        "distinct_files": len(files),
        "occurrence_count": len(occurrences),
        "occurrences": occurrences,
        "keep_candidate": {"display": keep["display"], "line": keep["line"], "layer": keep["layer"]},
        "gross_duplicate_bytes": gross,
        "estimate_note": "毛重复字节=簇内原文总字节，不等于净节省；改指针后仍有指针成本。",
        "recommendation": recommendation,
    }


def pick_keep(occurrences: list[dict], layers: list[str]) -> dict:
    texts = " ".join(o["text"] for o in occurrences)
    normative = any(m.lower() in texts.lower() for m in NORMATIVE_MARKERS)
    detailed = any(m.lower() in texts.lower() for m in DETAIL_MARKERS)

    # AGENTS + rules：长细则/命令留 rules，短硬约束留 AGENTS
    if "agents" in layers and "rules" in layers:
        want = "rules" if detailed and max(len(o["text"]) for o in occurrences) > 100 else "agents"
        for o in occurrences:
            if o["layer"] == want:
                return o
    if "memory" in layers and "agents" in layers:
        want = "agents" if normative else "memory"
        for o in occurrences:
            if o["layer"] == want:
                return o
    if "memory" in layers and "rules" in layers:
        want = "rules" if detailed or normative else "memory"
        for o in occurrences:
            if o["layer"] == want:
                return o
    for o in occurrences:
        if o["layer"] == layers[0]:
            return o
    return occurrences[0]


def recommend(layers: list[str], keep: dict, occurrences: list[dict]) -> str:
    layer = keep["layer"]
    if layer == "agents":
        return ("保留「全局 AGENTS」的规范句；记忆摘要改为一句指针（详见 AGENTS.md），"
                "规则文件只留操作细节/命令；历史归档不改，若会误导则标 superseded。")
    if layer == "rules":
        return ("保留 rules 中的操作细则；AGENTS 只留触发条件或一句硬约束，记忆摘要只留指针；"
                "历史归档不改，若会误导则标 superseded。")
    if layer == "memory":
        return ("保留记忆摘要的用户偏好句；AGENTS/规则若需执行约束，改成一句指针；"
                "历史归档不改，若会误导则标 superseded。")
    return "保留现行层，其余改指针；历史归档不改。"


def score_cluster(c: dict) -> tuple:
    exact = 1 if c["kind"] == "exact" else 0
    return (
        exact,
        len(c["layers"]),
        c["occurrence_count"],
        c["similarity"],
        c["gross_duplicate_bytes"],
    )


def find_exact_groups(records: list[dict]) -> list[list[dict]]:
    groups: dict[str, list[dict]] = defaultdict(list)
    for rec in records:
        groups[rec["normalized"]].append(rec)
    out = []
    for norm, occ in groups.items():
        layers = {o["layer"] for o in occ}
        if len(occ) >= 2 and len(layers) >= 2 and (layers & CURRENT_LAYERS):
            out.append(occ)
    return out


def find_near_groups(records: list[dict], exact_groups: list[list[dict]]) -> list[tuple[list[dict], float]]:
    # 以“归一化行”为原子建代表；单行也参与
    by_norm: dict[str, list[dict]] = defaultdict(list)
    for rec in records:
        by_norm[rec["normalized"]].append(rec)

    reps = []
    for norm, occ in by_norm.items():
        if len(norm) < NEAR_MIN_NORM:
            continue
        if any(not polarity_compatible(occ[0]["text"], o["text"]) for o in occ[1:]):
            continue
        layers = {o["layer"] for o in occ}
        reps.append({"norm": norm, "occ": occ, "layers": layers, "bytes": sum(o["bytes"] for o in occ)})
    reps.sort(key=lambda r: (-len(r["norm"]), -r["bytes"]))

    # 倒排 bigram，避免 3000^2 全比
    rep_bigrams = [bigrams(r["norm"]) for r in reps]
    index: dict[str, set[int]] = defaultdict(set)
    for i, bg in enumerate(rep_bigrams):
        for g in bg:
            index[g].add(i)

    assigned: set[int] = set()
    clusters: list[tuple[list[dict], float]] = []

    for i, seed in enumerate(reps):
        if i in assigned:
            continue
        if len(seed["norm"]) < NEAR_MIN_NORM:
            continue
        counts: Counter[int] = Counter()
        for g in rep_bigrams[i]:
            for j in index.get(g, ()):  # type: ignore[arg-type]
                if j != i and j not in assigned:
                    counts[j] += 1
        if not counts:
            continue
        # 共享 bigram 越多越可能；限制候选数
        candidates = [j for j, _ in counts.most_common(MAX_NEAR_CANDIDATES)]
        chosen = [seed]
        chosen_norm = {seed["norm"]}
        best_sim = 0.0
        for j in candidates:
            cand = reps[j]
            if cand["norm"] in chosen_norm:
                continue
            la, lb = len(seed["norm"]), len(cand["norm"])
            if min(la, lb) / max(la, lb) < 0.72:
                continue
            if not polarity_compatible(seed["occ"][0]["text"], cand["occ"][0]["text"]):
                continue
            if jaccard(rep_bigrams[i], rep_bigrams[j]) < 0.32:
                continue
            sm = SequenceMatcher(None, seed["norm"], cand["norm"])
            if sm.quick_ratio() < 0.86:
                continue
            ratio = sm.ratio()
            if ratio < NEAR_THRESHOLD:
                continue
            chosen.append(cand)
            chosen_norm.add(cand["norm"])
            best_sim = max(best_sim, ratio)
            if len(chosen) >= MAX_CLUSTER_MEMBERS:
                break

        if len(chosen) < 2:
            continue
        layers = set()
        members = []
        for rep in chosen:
            layers |= rep["layers"]
            members.extend(rep["occ"])
        if len(layers) < 2 or not (layers & CURRENT_LAYERS):
            continue
        # 与已报 exact 簇完全重叠的跳过
        if exact_groups:
            member_keys = {occurrence_key(o) for o in members}
            subset_of_exact = False
            for eg in exact_groups:
                eg_keys = {occurrence_key(o) for o in eg}
                if member_keys and member_keys <= eg_keys:
                    subset_of_exact = True
                    break
            if subset_of_exact:
                continue
        for idx in range(len(reps)):
            if reps[idx] in chosen:
                assigned.add(idx)
        clusters.append((members, best_sim))
    return clusters


def find_candidate_pairs(records: list[dict], exact_groups: list[list[dict]],
                         near_groups: list[tuple[list[dict], float]]) -> list[dict]:
    """0.70–0.85 的跨层候补对：不计数为 near，只供人工复核。"""
    covered: set[tuple] = set()
    for group in exact_groups:
        keys = [occurrence_key(o) for o in group]
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                covered.add(tuple(sorted((keys[i], keys[j]))))
    for members, _ in near_groups:
        keys = [occurrence_key(o) for o in members]
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                covered.add(tuple(sorted((keys[i], keys[j]))))

    # 用归一化代表行，减少重复对
    by_norm: dict[str, dict] = {}
    for rec in records:
        if len(rec["normalized"]) < 12:
            continue
        cur = by_norm.get(rec["normalized"])
        if cur is None:
            by_norm[rec["normalized"]] = {
                "norm": rec["normalized"],
                "occ": [rec],
                "layers": {rec["layer"]},
                "bytes": rec["bytes"],
            }
        else:
            cur["occ"].append(rec)
            cur["layers"].add(rec["layer"])
            cur["bytes"] += rec["bytes"]
    reps = list(by_norm.values())
    reps.sort(key=lambda r: (-len(r["norm"]), -r["bytes"]))

    candidates = []
    for i, a in enumerate(reps):
        if not (a["layers"] & CURRENT_LAYERS):
            continue
        for b in reps[i + 1:]:
            if not (b["layers"] & CURRENT_LAYERS):
                continue
            if a["layers"] == b["layers"] and len(a["layers"]) == 1:
                continue
            if not ((a["layers"] | b["layers"]) & CURRENT_LAYERS):
                continue
            if len(a["layers"] | b["layers"]) < 2:
                continue
            la, lb = len(a["norm"]), len(b["norm"])
            if min(la, lb) / max(la, lb) < 0.60:
                continue
            if not polarity_compatible(a["occ"][0]["text"], b["occ"][0]["text"]):
                continue
            if jaccard(bigrams(a["norm"]), bigrams(b["norm"])) < 0.18:
                continue
            sm = SequenceMatcher(None, a["norm"], b["norm"])
            if sm.quick_ratio() < 0.72:
                continue
            ratio = sm.ratio()
            if not (0.70 <= ratio < NEAR_THRESHOLD):
                continue
            # 已落在 exact/near 簇里的对跳过
            pair_keys = []
            for oa in a["occ"]:
                for ob in b["occ"]:
                    pair_keys.append(tuple(sorted((occurrence_key(oa), occurrence_key(ob)))))
            if pair_keys and all(k in covered for k in pair_keys):
                continue
            members = a["occ"] + b["occ"]
            layers = sorted({o["layer"] for o in members}, key=lambda x: LAYER_PRIORITY.get(x, 9))
            keep = pick_keep(members, layers)
            candidates.append({
                "kind": "candidate",
                "similarity": round(ratio, 4),
                "layers": layers,
                "layer_labels": [LAYER_LABEL.get(x, x) for x in layers],
                "occurrences": sorted(members, key=lambda x: (LAYER_PRIORITY.get(x["layer"], 9), x["file"], x["line"])),
                "keep_candidate": {"display": keep["display"], "line": keep["line"], "layer": keep["layer"]},
                "gross_duplicate_bytes": sum(o["bytes"] for o in members),
                "recommendation": recommend(layers, keep, members),
                "status": "BELOW_THRESHOLD_HUMAN_REVIEW",
            })
    candidates.sort(key=lambda c: (c["similarity"], len(c["layers"]), c["gross_duplicate_bytes"]), reverse=True)
    return candidates


def check_conflicts(records: list[dict]) -> tuple[list[dict], list[dict]]:
    """返回 (冲突列表, 检查项列表)。"""
    findings: list[dict] = []  # raw occurrences per key
    checks: dict[str, dict] = {}

    def add(key: str, label: str, value: str, role: str, rec: dict, note: str = "") -> None:
        checks.setdefault(key, {"key": key, "label": label, "values": {}})
        v = checks[key]["values"].setdefault(value, {
            "value": value,
            "normalized": value,
            "roles": set(),
            "occurrences": [],
        })
        v["roles"].add(role)
        v["occurrences"].append({
            "layer": rec["layer"],
            "display": rec["display"],
            "file": rec["file"],
            "line": rec["line"],
            "text": rec["text"],
            "role": role,
            "note": note,
        })

    for rec in records:
        text = rec["text"]

        # 1 上下文窗口：只收实际赋值；风险引用单独收
        for key, label in (("model_context_window", "本地上下文窗口"),
                           ("model_auto_compact_token_limit", "自动压缩阈值")):
            for m in re.finditer(key + r"\s*[=:：]\s*([0-9][0-9,]*)", text):
                val = str(int(m.group(1).replace(",", "")))
                # 历史归档里的 provider 运行时值不是当前本机配置，单独排除，避免假冲突
                if rec["layer"] == "lessons" and ("运行时" in text or "catalog" in text.lower()):
                    continue
                add(key, label, val, "current_setting", rec)
        if "上下文" in text or "context_window" in text:
            for m in re.finditer(r"(?:修复回|修复为|改成|覆盖回|退回)\s*([0-9]{5,})", text):
                val = str(int(m.group(1)))
                if val in {"400000", "256000", "128000"}:
                    add("model_context_window", "本地上下文窗口", val, "risk_reference", rec,
                        "历史归档描述脚本可能改回旧值；不是当前配置实测")

        # 2 预算（按主题键）
        budget_patterns = [
            ("budget:memory_summary", "记忆摘要预算",
             r"(?:记忆摘要|memory_summary)[^\n]{0,80}?(?:≤|<=|压到|预算(?:为|是)?|控制在)\s*([0-9][0-9,\.]*)\s*(B|KB|KiB|字节)"),
            ("budget:skills_index", "技能清单预算",
             r"(?:技能(?:清单|目录|索引)|skills?[_ ]index)[^\n]{0,60}?(?:约|≤|<=|预算(?:为|是)?|控制在)\s*([0-9][0-9,\.]*)\s*(B|KB|KiB|字节)"),
            ("budget:AGENTS", "全局 AGENTS 预算",
             r"(?:全局\s*AGENTS|AGENTS\.md|AGENTS)[^\n]{0,40}?(?:≤|<=|压到|预算(?:为|是)?|控制在)\s*([0-9][0-9,\.]*)\s*(B|KB|KiB|字节)"),
            ("budget:LESSONS", "LESSONS 预算",
             r"(?:LESSONS(?:\.md)?|经验库)[^\n]{0,40}?(?:≤|<=|压到|预算(?:为|是)?|控制在)\s*([0-9][0-9,\.]*)\s*(B|KB|KiB|字节)"),
            ("budget:default_rules", "default.rules 预算",
             r"(?:default\.rules|规则列表)[^\n]{0,40}?(?:≤|<=|压到|预算(?:为|是)?|控制在)\s*([0-9][0-9,\.]*)\s*(B|KB|KiB|字节)"),
            ("budget:total_injection", "七块固定注入预算",
             r"(?:七块|固定注入|总注入|合计)[^\n]{0,60}?(?:≤|<=|闸门|预算(?:为|是)?|控制在)\s*([0-9][0-9,\.]*)\s*(B|KB|KiB|字节)"),
        ]
        for key, label, pattern in budget_patterns:
            for m in re.finditer(pattern, text, re.I):
                raw = m.group(1).replace(",", "")
                unit = m.group(2).lower()
                try:
                    num = float(raw)
                except ValueError:
                    continue
                if unit in ("kb", "kib"):
                    num *= 1024
                val = str(int(round(num)))
                add(key, label, val, "budget_target", rec, f"原文 {m.group(1)} {m.group(2)}")

        # 3 版本号：只收显式命名版本
        m = re.search(r"agent-slim[^\n]{0,30}?v([0-9]+\.[0-9]+\.[0-9]+)", text, re.I)
        if m:
            add("version:agent-slim", "agent-slim 版本", "v" + m.group(1), "version", rec)
        # memory_summary 首行 v1
        if rec["file"].endswith("memory_summary.md") and rec["line"] == 1 and re.fullmatch(r"v[0-9]+", text):
            add("version:memory_summary", "记忆摘要 schema 版本", text, "version", rec)

        # 4 路径：只收有明确“固定/只在/位于”的目录
        path_patterns = [
            ("path:company_kb", "公司知识库目录",
             r"公司知识库[^\n]{0,30}?(?:固定(?:在)?|默认使用本地路径|位于|路径[：:]?)\s*`?((?:/" + "Users" + r"/|~/)[^\s`，。；;、）)]+)"),
            ("path:construction_log", "施工日志项目目录",
             r"施工日志[^\n]{0,50}?(?:只在|位于|路径[：:]?)\s*`?((?:/" + "Users" + r"/|~/)[^\s`，。；;、）)]+)"),
        ]
        for key, label, pattern in path_patterns:
            for m in re.finditer(pattern, text):
                raw_path = m.group(1).rstrip("。；;，,、）)")
                if raw_path.endswith(".md"):
                    continue
                try:
                    norm_path = str(Path(os.path.expanduser(raw_path)).resolve())
                except Exception:
                    norm_path = raw_path
                add(key, label, norm_path, "path", rec, f"原文 {raw_path}")

        # 5 日期：只收有明确语义标签的日期
        date_patterns = [
            ("date:last_updated", "最后更新日期", r"最近更新[:：]\s*(\d{4}-\d{2}-\d{2})"),
            ("date:session", "会话日期", r"会话日期[:：]\s*(\d{4}-\d{2}-\d{2})"),
            ("date:review", "复盘/执行日期", r"(?:复盘节点|执行日期|实测日期)[:：]?\s*(\d{4}-\d{2}-\d{2})"),
            ("date:snapshot:token", "Token 快照日期", r"已验证快照[（(](\d{4}-\d{2}-\d{2})[）)]"),
        ]
        for key, label, pattern in date_patterns:
            for m in re.finditer(pattern, text):
                add(key, label, m.group(1), "date", rec)

    # 汇总冲突
    for key, check in checks.items():
        vals = check["values"]
        distinct = sorted(vals.keys())
        check["distinct_values"] = distinct
        check["occurrence_count"] = sum(len(v["occurrences"]) for v in vals.values())
        if len(distinct) >= 2:
            values_out = []
            for val in distinct:
                v = vals[val]
                values_out.append({
                    "value": v["value"],
                    "normalized": v["normalized"],
                    "roles": sorted(v["roles"]),
                    "occurrences": sorted(v["occurrences"], key=lambda x: (LAYER_PRIORITY.get(x["layer"], 9), x["file"], x["line"])),
                })
            findings.append({
                "key": key,
                "label": check["label"],
                "values": values_out,
                "recommendation": conflict_recommendation(key),
                "decision": "USER_DECISION",
            })
        check["status"] = "CONFLICT" if len(distinct) >= 2 else "OK"

    # 清理 set
    for check in checks.values():
        for v in check["values"].values():
            v["roles"] = sorted(v["roles"])
    findings.sort(key=lambda x: x["key"])
    checks_out = sorted(checks.values(), key=lambda x: x["key"])
    return findings, checks_out


def conflict_recommendation(key: str) -> str:
    if key.startswith("model_context_window") or key.startswith("model_auto_compact"):
        return ("以现行 AGENTS/rules 的 200000/160000 为准；历史归档中的 400000/256000 "
                "只能标为 historical/superseded，不得作为当前配置依据。需用户确认后再改归档文字。")
    if key.startswith("budget:"):
        return "先确认该预算是否仍生效；同一预算只保留一个数，另一处改指针或标历史。需用户决策。"
    if key.startswith("path:"):
        return "以用户当前指定的目录为准；另一处改指针或标历史，不自动迁移任何文件。需用户决策。"
    if key.startswith("version:"):
        return "以当前 canonical 版本为准；历史版本保留在归档并标注日期，不覆盖新版本。需用户决策。"
    return "以现行层为准，另一处改指针或标历史；需用户决策。"


def build_markdown(payload: dict, max_clusters: int) -> str:
    s = payload["stats"]
    lines = []
    lines.append("# 四层规则重复/冲突看板（2026-11-09）")
    lines.append("")
    lines.append(f"- 生成：`{payload['generated_at']}`")
    lines.append(f"- 扫描文件：**{s['files_scanned']}** 个（memory {s['files_by_layer'].get('memory',0)} / agents {s['files_by_layer'].get('agents',0)} / rules {s['files_by_layer'].get('rules',0)} / lessons {s['files_by_layer'].get('lessons',0)}）")
    lines.append(f"- 规则型行：**{s['rule_lines']}**；原始行 {s['lines_total']}；跳过 {s['skipped_total']}（表头/分隔/围栏/非规则等）")
    lines.append(f"- 重复簇：**{s['clusters_total']}**（exact {s['exact_clusters']} / near {s['near_clusters']}）；本页列前 **{min(max_clusters, len(payload['clusters']))}** 簇")
    lines.append(f"- 冲突：**{s['conflicts_total']}** 项；检查已知键 {s['conflict_checks']} 个")
    lines.append("- 边界：只报告，不自动合并、不删行；冲突项交用户决策。")
    lines.append("")
    lines.append("## 1 覆盖与规则行")
    lines.append("")
    lines.append("| 层 | 文件 | 字节 | 规则型行 |")
    lines.append("|---|---:|---:|---:|")
    for layer in LAYER_ORDER:
        fs = [f for f in payload["files"] if f["layer"] == layer]
        lines.append(f"| {LAYER_LABEL[layer]} | {len(fs)} | {sum(f['bytes'] for f in fs):,} | {sum(f['rule_lines'] for f in fs):,} |")
    lines.append("")
    lines.append("已扫文件：")
    lines.append("")
    for f in payload["files"]:
        lines.append(f"- `{f['display']}`（{f['rule_lines']} 条规则型行，{f['bytes']:,} B）")
    lines.append("")
    lines.append(f"## 2 重复簇 Top {min(max_clusters, len(payload['clusters']))}")
    lines.append("")
    if not payload["clusters"]:
        lines.append("未发现跨层重复簇。")
        lines.append("")
    for c in payload["clusters"][:max_clusters]:
        sim = "100%" if c["kind"] == "exact" else f"{c['similarity']*100:.1f}%"
        lines.append(f"### {c['id']} {c['kind']} · {sim} · {' + '.join(c['layer_labels'])}")
        lines.append("")
        lines.append("| # | 层 | file:line | 原文 |")
        lines.append("|---:|---|---|---|")
        for i, o in enumerate(c["occurrences"], start=1):
            text = o["text"].replace("|", "\\|")
            if len(text) > 220:
                text = text[:217] + "..."
            lines.append(f"| {i} | {LAYER_LABEL.get(o['layer'], o['layer'])} | `{o['display']}:{o['line']}` | {text} |")
        lines.append("")
        lines.append(f"- 建议：{c['recommendation']}")
        lines.append(f"- 保留候选：`{c['keep_candidate']['display']}:{c['keep_candidate']['line']}`")
        lines.append(f"- 毛重复字节：{c['gross_duplicate_bytes']:,} B（估算，不等于净节省）")
        lines.append("")
    if s["clusters_omitted"] > 0:
        lines.append(f"> 另有 {s['clusters_omitted']} 簇未在 Markdown 展开，机器可读结果见 JSON。")
        lines.append("")
    lines.append("## 2B 阈值下候补（0.70–0.85，不计数，供人工复核）")
    lines.append("")
    if not payload.get("candidate_pairs"):
        lines.append("无 0.70–0.85 的跨层候补对。")
        lines.append("")
    else:
        lines.append("> 这些不是正式 near 簇（未达 0.85），不得自动合并；只用于人工判断是否同义重复。")
        lines.append("")
        for c in payload["candidate_pairs"][:max_clusters]:
            lines.append(f"### {c['id']} candidate · {c['similarity']*100:.1f}% · {' + '.join(c['layer_labels'])}")
            lines.append("")
            lines.append("| 层 | file:line | 原文 |")
            lines.append("|---|---|---|")
            for o in c["occurrences"]:
                text = o["text"].replace("|", "\\|")
                if len(text) > 220:
                    text = text[:217] + "..."
                lines.append(f"| {LAYER_LABEL.get(o['layer'], o['layer'])} | `{o['display']}:{o['line']}` | {text} |")
            lines.append("")
            lines.append(f"- 建议：{c['recommendation']}")
            lines.append(f"- 状态：`{c['status']}`")
            lines.append("")
    lines.append("## 3 冲突项（需用户决策）")
    lines.append("")
    if not payload["conflicts"]:
        lines.append("未发现同键不同值。已知键检查结果如下：")
        lines.append("")
        lines.append("| 键 | 状态 | 值 | 出现次数 |")
        lines.append("|---|---|---|---:|")
        for c in payload["conflict_checks"]:
            vals = ", ".join(c["distinct_values"]) if c["distinct_values"] else "—"
            lines.append(f"| `{c['key']}` | {c['status']} | {vals} | {c['occurrence_count']} |")
        lines.append("")
    for c in payload["conflicts"]:
        lines.append(f"### {c['key']} · {c['label']}")
        lines.append("")
        lines.append("| 值 | 角色 | file:line | 原文 |")
        lines.append("|---|---|---|---|")
        for v in c["values"]:
            for o in v["occurrences"]:
                text = o["text"].replace("|", "\\|")
                if len(text) > 220:
                    text = text[:217] + "..."
                lines.append(f"| `{v['value']}` | {', '.join(v['roles'])} | `{o['display']}:{o['line']}` | {text} |")
        lines.append("")
        lines.append(f"- 建议：{c['recommendation']}")
        lines.append(f"- 决策：`{c['decision']}`")
        lines.append("")
    lines.append("## 4 口径与误报边界")
    lines.append("")
    lines.append("- 归一化：NFKC 全半角统一，去掉标点/空格/列表符号，保留字母数字与 CJK；因此“格式不同、语义相同”的句子可能成簇。")
    lines.append("- 近重复：difflib `SequenceMatcher.ratio() >= 0.85`；带否定极性保护（“做/不做”“禁止/允许”不会仅因一字之差成簇）。")
    lines.append("- 只列跨层簇，且至少一层是 memory/agents/rules；仅 lessons 内部的历史重复不列入，避免把归档当现行规则。")
    lines.append("- 表头、表格分隔行、代码围栏内命令不抽取；`default.rules` 的 `prefix_rule` 单独归一为 `decision:命令词`。")
    lines.append("- 冲突只对已知键做键值抽取；同一日期在不同语义下不强行判冲突，避免把“快照日/复盘日”混为一谈。")
    lines.append("- 所有建议均为文本层面，不自动改任何被扫文件；预算与路径冲突需用户决策。")
    lines.append("")
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="扫描 Codex 四层规则，输出重复/冲突看板（只读）")
    parser.add_argument("--codex-home", default=os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    parser.add_argument("--json-out", default=None)
    parser.add_argument("--md-out", default=None)
    parser.add_argument("--max-clusters", type=int, default=30)
    parser.add_argument("--summary", action="store_true", help="只打印摘要 JSON")
    args = parser.parse_args(argv)

    codex_home = Path(args.codex_home).expanduser()
    skill_root = Path(__file__).resolve().parent.parent
    json_out = Path(args.json_out) if args.json_out else skill_root / "outputs" / "duplicate-conflict-20261109.json"
    md_out = Path(args.md_out) if args.md_out else skill_root / "outputs" / "duplicate-conflict-20261109.md"

    specs = discover_files(codex_home)
    if not specs:
        print(json.dumps({"error": "没有找到任何四层文件", "codex_home": str(codex_home)}, ensure_ascii=False))
        return 3

    records: list[dict] = []
    files_meta: list[dict] = []
    for layer, path in specs:
        try:
            recs, meta = extract_records(path, layer, codex_home)
        except OSError as exc:
            print(json.dumps({"error": f"读取失败: {path}: {exc}"}, ensure_ascii=False))
            return 3
        records.extend(recs)
        files_meta.append(meta)

    exact_groups = find_exact_groups(records)
    near_groups = find_near_groups(records, exact_groups)
    candidate_pairs = find_candidate_pairs(records, exact_groups, near_groups)

    clusters: list[dict] = []
    for group in exact_groups:
        clusters.append(make_cluster("exact", group, 1.0, "TMP"))
    for members, sim in near_groups:
        clusters.append(make_cluster("near", members, sim, "TMP"))
    clusters.sort(key=score_cluster, reverse=True)

    # 给 top N 编号；同时统计总数
    clusters_total = len(clusters)
    max_clusters = max(1, args.max_clusters)
    clusters_out = []
    for i, c in enumerate(clusters[:max_clusters], start=1):
        c["id"] = f"D{i:03d}"
        clusters_out.append(c)
    clusters_omitted = max(0, clusters_total - len(clusters_out))

    conflicts, checks = check_conflicts(records)

    # 候补对编号（不进入正式簇计数）
    max_candidates = max(1, args.max_clusters)
    candidate_pairs = candidate_pairs[:max_candidates]
    for i, c in enumerate(candidate_pairs, start=1):
        c["id"] = f"C{i:03d}"

    files_by_layer = Counter(f["layer"] for f in files_meta)
    skipped_total = sum(sum(f["skipped"].values()) for f in files_meta)
    payload = {
        "schema_version": SCHEMA_VERSION,
        "tool": TOOL,
        "generated_at": now_iso(),
        "codex_home": str(codex_home),
        "inputs": [{"layer": layer, "path": str(path)} for layer, path in specs],
        "files": files_meta,
        "stats": {
            "files_scanned": len(files_meta),
            "files_by_layer": dict(files_by_layer),
            "lines_total": sum(f["lines"] for f in files_meta),
            "rule_lines": len(records),
            "skipped_total": skipped_total,
            "clusters_total": clusters_total,
            "exact_clusters": len(exact_groups),
            "near_clusters": len(near_groups),
            "clusters_omitted": clusters_omitted,
            "conflicts_total": len(conflicts),
            "conflict_checks": len(checks),
            "near_threshold": NEAR_THRESHOLD,
            "candidate_pairs": len(candidate_pairs),
        },
        "clusters": clusters_out,
        "candidate_pairs": candidate_pairs,
        "conflicts": conflicts,
        "conflict_checks": checks,
        "notes": [
            "只读工具；不修改任何被扫文件。",
            "仅列跨层簇，且至少一层是 memory/agents/rules；仅 lessons 内部重复不列。",
            "毛重复字节不是净节省；改指针仍有指针成本。",
            "冲突项 decision=USER_DECISION，需用户确认后再改。",
        ],
    }

    json_out.parent.mkdir(parents=True, exist_ok=True)
    md_out.parent.mkdir(parents=True, exist_ok=True)
    json_out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    md_out.write_text(build_markdown(payload, max_clusters) + "\n", encoding="utf-8")

    summary = {
        "tool": TOOL,
        "generated_at": payload["generated_at"],
        "files_scanned": len(files_meta),
        "files_by_layer": dict(files_by_layer),
        "rule_lines": len(records),
        "clusters_total": clusters_total,
        "exact_clusters": len(exact_groups),
        "near_clusters": len(near_groups),
        "conflicts_total": len(conflicts),
        "conflict_checks": len(checks),
        "candidate_pairs": len(candidate_pairs),
        "json_out": str(json_out),
        "md_out": str(md_out),
        "bytes": {"json": json_out.stat().st_size, "md": md_out.stat().st_size},
    }
    if args.summary:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(json.dumps(summary, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
