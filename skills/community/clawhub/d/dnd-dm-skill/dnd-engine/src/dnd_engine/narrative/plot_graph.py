"""剧情节点图：把模组抽成「节点 + 出口 + 里程碑」，并维护权威剧情状态。

为什么需要它：现状每轮把整章塞给模型，让它自己"猜我们现在在哪、下一步能去哪"。
这就把确定性的事情（节点、前置、出口）交给了概率模型——又慢又不稳。

本模块只做两件事：
1. 从模组 markdown 抽节点图（标题层级 + 交叉引用 + 升级里程碑）；
2. 维护 plot_state（当前节点 / 已访问 / 已解锁 / 里程碑），推进由代码判定。
"""

from __future__ import annotations

import json
import pathlib
import re
from typing import Any

HEADING_RE = re.compile(r"^(#{2,4})\s+(.+?)\s*$", re.M)
LEVEL_RE = re.compile(r"(?:提升至|升至|升级至|到达?)\s*(\d+)\s*级")
REF_HINT_RE = re.compile(r"(?:跳至|跳到|参见|参阅|前往|转向|移至)([^。；\n，]{2,24})")


def _slug_for_file(path: pathlib.Path) -> str:
    match = re.search(r"Ch\.?\s*(\d+)", path.name)
    if match:
        return f"ch{match.group(1)}"
    match = re.search(r"(App\.?\s*[A-Z])", path.name)
    if match:
        return match.group(1).replace(".", "").replace(" ", "").lower()
    return "mod"


def split_nodes(text: str, path: pathlib.Path, min_level: int = 2,
                max_level: int = 3) -> list[dict[str, Any]]:
    """按标题层级切节点。level 2 = 章节/节拍，level 3 = 场景。"""
    slug = _slug_for_file(path)
    lines = text.splitlines()
    marks: list[dict[str, Any]] = []
    for index, line in enumerate(lines, start=1):
        match = HEADING_RE.match(line)
        if not match:
            continue
        level = len(match.group(1))
        if not (min_level <= level <= max_level):
            continue
        marks.append({"level": level, "title": match.group(2).strip(), "start": index})

    nodes: list[dict[str, Any]] = []
    for position, mark in enumerate(marks):
        end = marks[position + 1]["start"] - 1 if position + 1 < len(marks) else len(lines)
        body = "\n".join(lines[mark["start"] - 1:end])
        nodes.append({
            "id": f"{slug}.{position + 1:03d}",
            "title": mark["title"],
            "level": mark["level"],
            "file": path.name,
            "start_line": mark["start"],
            "end_line": end,
            "chapter": next((m["title"] for m in reversed(marks[:position])
                             if m["level"] < mark["level"]), ""),
            "chars": len(body),
        })
    return nodes


def build_graph(modules_dir: pathlib.Path, min_level: int = 2,
                max_level: int = 3) -> dict[str, Any]:
    """抽节点图：节点 + 顺序出口 + 显式交叉引用 + 升级里程碑。"""
    nodes: list[dict[str, Any]] = []
    bodies: dict[str, str] = {}
    milestones: list[dict[str, Any]] = []

    for path in sorted(modules_dir.glob("*.md")):
        if path.name.endswith("-全.md") or "App." in path.name:
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        file_nodes = split_nodes(text, path, min_level, max_level)
        lines = text.splitlines()
        for node in file_nodes:
            bodies[node["id"]] = "\n".join(lines[node["start_line"] - 1:node["end_line"]])
            level_match = LEVEL_RE.search(bodies[node["id"]])
            if level_match and node["level"] == 2:
                milestones.append({"node": node["id"], "level": int(level_match.group(1)),
                                   "title": node["title"]})
        nodes.extend(file_nodes)

    title_to_id = {node["title"]: node["id"] for node in nodes}
    edges: list[dict[str, str]] = []

    # 顺序出口：**同一层级**内按顺序推进（跨层不串，避免把子场景接到下一个章节）
    by_level: dict[int, list[dict[str, Any]]] = {}
    for node in nodes:
        by_level.setdefault(node["level"], []).append(node)
    for level_nodes in by_level.values():
        for previous, current in zip(level_nodes, level_nodes[1:]):
            edges.append({"from": previous["id"], "to": current["id"], "kind": "sequence"})

    # 上层节点 → 其第一个下层子节点（进入该节的第一个场景）
    for position, node in enumerate(nodes):
        if node["level"] <= 2:
            continue
        parent = next((candidate for candidate in reversed(nodes[:position])
                       if candidate["level"] < node["level"] and candidate["chapter"] == node["chapter"]), None)
        if parent:
            edges.append({"from": parent["id"], "to": node["id"], "kind": "sequence"})

    # 显式交叉引用：正文提到另一个节点标题（长度≥3，避免噪声）
    for node in nodes:
        body = bodies.get(node["id"], "")
        for title, target in title_to_id.items():
            if target == node["id"] or len(title) < 3 or title not in body:
                continue
            edges.append({"from": node["id"], "to": target, "kind": "reference"})
        for hint in REF_HINT_RE.findall(body):
            cleaned = hint.strip("「」《》\"'（）() ")
            target = title_to_id.get(cleaned)
            if target and target != node["id"]:
                edges.append({"from": node["id"], "to": target, "kind": "reference"})

    seen: set[tuple[str, str, str]] = set()
    unique_edges: list[dict[str, str]] = []
    for edge in edges:
        key = (edge["from"], edge["to"], edge["kind"])
        if key not in seen:
            seen.add(key)
            unique_edges.append(edge)

    # 前驱表：便于判定"解锁"
    incoming: dict[str, list[str]] = {}
    for edge in unique_edges:
        incoming.setdefault(edge["to"], []).append(edge["from"])

    return {
        "version": 1,
        "source": str(modules_dir),
        "nodes": nodes,
        "edges": unique_edges,
        "incoming": incoming,
        "milestones": milestones,
    }


# ─────────────────────── 剧情状态 ───────────────────────

def new_state(graph: dict[str, Any], start_node: str = "") -> dict[str, Any]:
    nodes = graph.get("nodes") or []
    entries = [n for n in nodes if n["level"] == 2]
    start = start_node or (entries[0]["id"] if entries else (nodes[0]["id"] if nodes else ""))
    return {
        "version": 1,
        "current_node": start,
        "visited": [start] if start else [],
        "unlocked": _unlocked_from(graph, {start}),
        "milestones": [],
        "events": [],
        "updated_at": "",
    }


def successors(graph: dict[str, Any], node_id: str,
               kinds: tuple[str, ...] = ("sequence", "reference")) -> list[str]:
    return [edge["to"] for edge in graph.get("edges") or []
            if edge["from"] == node_id and edge["kind"] in kinds]


def _unlocked_from(graph: dict[str, Any], visited: set[str]) -> list[str]:
    unlocked: set[str] = set(visited)
    for node_id in list(visited):
        unlocked.update(successors(graph, node_id))
    return sorted(unlocked)


def advance(state: dict[str, Any], graph: dict[str, Any],
            node_id: str, event: str = "") -> dict[str, Any]:
    """把剧情推进到某节点（由代码调用，不由模型自行决定）。"""
    nodes = {n["id"]: n for n in graph.get("nodes") or []}
    if node_id not in nodes:
        raise ValueError(f"unknown plot node: {node_id}")
    state = dict(state)
    state["current_node"] = node_id
    visited = list(dict.fromkeys(list(state.get("visited") or []) + [node_id]))
    state["visited"] = visited
    state["unlocked"] = _unlocked_from(graph, set(visited))
    if event:
        state["events"] = list(state.get("events") or []) + [event]
    for milestone in graph.get("milestones") or []:
        if milestone["node"] == node_id and milestone not in state.get("milestones", []):
            state["milestones"] = list(state.get("milestones") or []) + [milestone]
    return state


def injection_context(graph: dict[str, Any], state: dict[str, Any],
                      kind_titles: dict[str, str] | None = None) -> dict[str, Any]:
    """每轮只需要注入这些（而不是整章）——确定性、极小、可直接喂给模型。"""
    nodes = {n["id"]: n for n in graph.get("nodes") or []}
    current = nodes.get(str(state.get("current_node")), {})
    next_ids = successors(graph, str(state.get("current_node")))
    titles = kind_titles or {}
    return {
        "current": {"id": current.get("id", ""), "title": current.get("title", ""),
                    "chapter": current.get("chapter", "")},
        "next_steps": [{"id": nid, "title": nodes.get(nid, {}).get("title", "")}
                       for nid in next_ids[:6]],
        "visited_count": len(state.get("visited") or []),
        "milestones": [m.get("level") for m in state.get("milestones") or []],
        "pending_gates": [nid for nid in (next_ids or [])
                          if nid in (graph.get("incoming") or {})
                          and len(graph["incoming"][nid]) > 1][:4],
    }


def save_graph(graph: dict[str, Any], path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8")


def load_graph(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_state(state: dict[str, Any], path: pathlib.Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


def load_state(path: pathlib.Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def render_context(ctx: dict[str, Any]) -> str:
    """把注入上下文渲染成给模型的最短文本（≈100–200 tok）。"""
    lines = [f"当前节点：{ctx['current']['title']}（{ctx['current']['chapter']}）",
             f"已访问节点数：{ctx['visited_count']}"]
    if ctx["next_steps"]:
        lines.append("可达下一步：" + "、".join(item["title"] for item in ctx["next_steps"]))
    if ctx["pending_gates"]:
        lines.append("需要门槛：" + "、".join(ctx["pending_gates"]))
    if ctx["milestones"]:
        lines.append("已达里程碑等级：" + "、".join(f"Lv{n}" for n in ctx["milestones"]))
    return "\n".join(lines)
