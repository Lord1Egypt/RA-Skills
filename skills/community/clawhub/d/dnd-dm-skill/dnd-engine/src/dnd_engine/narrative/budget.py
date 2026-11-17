"""注入预算：把「现状 vs 分级后」的每轮上下文开销算成可复现的数字。

现状（每轮常驻）：规则全量 + 队伍全量 + 整份场景索引 + 当前场景切片
分级后：规则常驻核心 + 队伍摘要 + 当前场景切片 + 邻域摘要 + 剧情状态骨架

所有数字都来自真实文件与真实切片，不是估算。
"""

from __future__ import annotations

import json
import pathlib
from dataclasses import dataclass, field
from typing import Any

from .plot_graph import injection_context, render_context

CHARS_PER_TOKEN = 1.5      # 中文约 1.5 字符/token（估算，实际取决于分词器）
NEIGHBOR_TOKENS = 30         # 每个可达下一步的摘要预算


def estimate_tokens(text: str) -> int:
    return max(0, round(len(str(text or "")) / CHARS_PER_TOKEN))


def party_digest(sheet: dict[str, Any]) -> str:
    hp = sheet.get("hp") or {}
    stats = sheet.get("stats") or sheet.get("attributes") or {}
    key = [str(item)[:12] for item in (sheet.get("backpack") or [])[:4]]
    return (f"{sheet.get('name')}｜{sheet.get('race')}{sheet.get('class')}"
            f"{sheet.get('subclass') or ''} Lv{sheet.get('level')}｜"
            f"HP {hp.get('current')}/{hp.get('max')} AC {sheet.get('ac')}｜"
            f"关键物品：{'、'.join(key) if key else '无'}")


def scene_slice(modules_dir: pathlib.Path, node: dict[str, Any]) -> str:
    path = modules_dir / str(node.get("file") or "")
    if not path.exists():
        return ""
    lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
    return "\n".join(lines[max(0, int(node["start_line"]) - 1):int(node["end_line"])])


@dataclass
class BudgetInputs:
    rules_paths: list[pathlib.Path] = field(default_factory=list)
    rules_core_path: pathlib.Path | None = None
    party_path: pathlib.Path | None = None
    index_path: pathlib.Path | None = None
    graph: dict[str, Any] = field(default_factory=dict)
    state: dict[str, Any] = field(default_factory=dict)
    modules_dir: pathlib.Path | None = None


def _read(path: pathlib.Path | None) -> str:
    if not path or not path.exists():
        return ""
    return path.read_text(encoding="utf-8", errors="ignore")


def compare(inputs: BudgetInputs) -> dict[str, Any]:
    modules_dir = inputs.modules_dir or pathlib.Path(".")

    # ── 现状 ──
    rules_text = "".join(_read(p) for p in inputs.rules_paths)
    party_text = _read(inputs.party_path)
    index_text = _read(inputs.index_path)
    current_id = str(inputs.state.get("current_node") or "")
    node = next((n for n in inputs.graph.get("nodes") or [] if n["id"] == current_id), {})
    slice_text = scene_slice(modules_dir, node) if node else ""

    baseline = {
        "规则全量": estimate_tokens(rules_text),
        "队伍全量": estimate_tokens(party_text),
        "整份场景索引": estimate_tokens(index_text),
        "当前场景切片": estimate_tokens(slice_text),
    }

    # ── 分级后 ──
    core_text = _read(inputs.rules_core_path)
    try:
        party = json.loads(party_text) if party_text else {}
    except json.JSONDecodeError:
        party = {}
    digest_text = "\n".join(party_digest(member) for member in (party.get("party") or []))
    ctx = injection_context(inputs.graph, inputs.state)
    ctx_text = render_context(ctx)

    # 索引分级：只注入当前节点所属章节的条目
    chapter = str(node.get("chapter") or "")
    chapter_index = [n for n in inputs.graph.get("nodes") or []
                     if n.get("chapter") == chapter and n.get("level") == 2]
    chapter_text = "\n".join(f"- {n['title']}" for n in chapter_index)

    optimized = {
        "规则常驻核心": estimate_tokens(core_text),
        "队伍摘要": estimate_tokens(digest_text),
        "剧情骨架(L0)": estimate_tokens(ctx_text),
        "当前场景切片(L1)": estimate_tokens(slice_text),
        f"邻域摘要(L2) x{len(ctx['next_steps'])}": len(ctx["next_steps"]) * NEIGHBOR_TOKENS,
        "本章索引": estimate_tokens(chapter_text),
    }

    baseline_total = sum(baseline.values())
    optimized_total = sum(optimized.values())
    return {
        "baseline": baseline,
        "optimized": optimized,
        "baseline_total": baseline_total,
        "optimized_total": optimized_total,
        "saved": baseline_total - optimized_total,
        "saved_ratio": round(1 - optimized_total / baseline_total, 3) if baseline_total else 0.0,
        "current_node": {"id": node.get("id", ""), "title": node.get("title", "")},
        "graph": {"nodes": len(inputs.graph.get("nodes") or []),
                  "edges": len(inputs.graph.get("edges") or []),
                  "milestones": len(inputs.graph.get("milestones") or [])},
    }


def render_report(result: dict[str, Any]) -> str:
    lines = ["# 每轮注入预算（实测）", ""]
    lines.append(f"当前节点：{result['current_node']['title'] or '（未指定）'}"
                 f"（图：{result['graph']['nodes']} 节点 / {result['graph']['edges']} 边）")
    lines.append("")
    lines.append("| 现状（每轮常驻） | token |  | 分级后 | token |")
    lines.append("|---|---|---|---|---|")
    left = list(result["baseline"].items())
    right = list(result["optimized"].items())
    for index in range(max(len(left), len(right))):
        lk, lv = left[index] if index < len(left) else ("", "")
        rk, rv = right[index] if index < len(right) else ("", "")
        lines.append(f"| {lk} | {lv} |  | {rk} | {rv} |")
    lines.append("")
    lines.append(f"合计：**{result['baseline_total']} tok → {result['optimized_total']} tok**"
                 f"（省 {result['saved']} tok，{result['saved_ratio']:.0%}）")
    return "\n".join(lines)
