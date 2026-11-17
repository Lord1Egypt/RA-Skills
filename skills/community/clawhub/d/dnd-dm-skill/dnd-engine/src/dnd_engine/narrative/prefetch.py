"""预取（P2）：玩家还在这条路上时，先把下一步要用的东西备好。

预取两件事（都不在关键路径上）：
1. **片段预取**：把「当前节点的后继场景」切片拿出来，用并行 Noul 选相关片段，
   下一轮直接可用（省掉运行时筛选）。
2. **前缀预热**（可选）：把稳定前缀（system + stable）先发一次极小请求送进服务端缓存，
   让下一轮的首字延迟更低。

缓存按节点 id 存储，写入 `reports/prefetch_cache.json`。
"""

from __future__ import annotations

import json
import pathlib
import time
from dataclasses import asdict, dataclass, field
from typing import Any

from . import budget as budget_mod
from .plot_graph import successors
from .prompt import MAX_SLICES, build_messages, prefix_signature, select_relevant

DEFAULT_CACHE = pathlib.Path(__file__).resolve().parents[3] / "reports" / "prefetch_cache.json"


@dataclass
class PrefetchEntry:
    node_id: str
    slices: list[dict[str, Any]] = field(default_factory=list)
    signature: str = ""
    created_at: float = 0.0
    note: str = ""


def candidate_slices(graph: dict[str, Any], state: dict[str, Any],
                     modules_dir: pathlib.Path) -> list[dict[str, Any]]:
    """候选片段 = 所有可达后继节点的场景切片。"""
    nodes = {n["id"]: n for n in graph.get("nodes") or []}
    candidates: list[dict[str, Any]] = []
    for node_id in successors(graph, str(state.get("current_node"))):
        node = nodes.get(node_id)
        if not node:
            continue
        text = budget_mod.scene_slice(modules_dir, node)
        if not text:
            continue
        candidates.append({"id": node_id, "title": node.get("title", ""),
                           "text": text,
                           "tokens": budget_mod.estimate_tokens(text)})
    return candidates


class PrefetchCache:
    def __init__(self, path: pathlib.Path | None = None):
        self.path = pathlib.Path(path) if path else DEFAULT_CACHE
        self.entries: dict[str, dict[str, Any]] = {}
        self.load()

    def load(self) -> None:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            self.entries = dict(data.get("entries") or {})
        except (OSError, json.JSONDecodeError):
            self.entries = {}

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(
            json.dumps({"version": 1, "entries": self.entries}, ensure_ascii=False, indent=2),
            encoding="utf-8")

    def get(self, node_id: str, signature: str = "") -> PrefetchEntry | None:
        raw = self.entries.get(node_id)
        if not raw:
            return None
        entry = PrefetchEntry(**raw)
        if signature and entry.signature and entry.signature != signature:
            return None                      # 前缀变了，缓存作废
        return entry

    def put(self, entry: PrefetchEntry) -> None:
        self.entries[entry.node_id] = asdict(entry)
        self.save()


def prefetch_node(state: dict[str, Any], graph: dict[str, Any], modules_dir: pathlib.Path,
                  relevance_provider=None, cache: PrefetchCache | None = None,
                  party_digest: str = "") -> PrefetchEntry:
    """为当前节点预取后继片段；有 Noul 提供方就用相关性筛选，否则取前 N 个。"""
    node_id = str(state.get("current_node") or "")
    signature = prefix_signature(build_messages(graph, state, party_digest, "", []))
    candidates = candidate_slices(graph, state, modules_dir)

    picked: list[dict[str, Any]]
    note = ""
    if relevance_provider is not None and candidates:
        from .plot_graph import injection_context
        picked = select_relevant(candidates, injection_context(graph, state), relevance_provider)
        note = f"相关性筛选：{len(candidates)} → {len(picked)}"
    else:
        picked = candidates[:MAX_SLICES]
        note = f"未筛选，取前 {len(picked)} 个"

    entry = PrefetchEntry(node_id=node_id, slices=picked, signature=signature,
                          created_at=time.time(), note=note)
    if cache is not None:
        cache.put(entry)
    return entry


def warm_prefix(provider, messages: list[dict[str, str]]) -> dict[str, Any]:
    """把稳定前缀送一次极小请求，促使服务端缓存该前缀（可选，默认不调）。"""
    if provider is None or not getattr(provider, "available", False):
        return {"warmed": False, "reason": "provider unavailable"}
    stable = messages[:2]
    try:
        provider.complete_json_messages(stable, stream=False, max_tokens=1)
        return {"warmed": True, "signature": prefix_signature(messages)}
    except Exception as exc:  # noqa: BLE001
        return {"warmed": False, "reason": str(exc)[:80]}


def render_entry(entry: PrefetchEntry) -> str:
    tokens = sum(int(item.get("tokens") or 0) for item in entry.slices)
    lines = [f"预取节点：{entry.node_id} | 片段 {len(entry.slices)} 个 / ≈{tokens} tok",
             f"前缀签名：{entry.signature}｜{entry.note}"]
    for item in entry.slices:
        lines.append(f"  · {item.get('title') or item.get('id')}"
                     f"（相关度 {item.get('relevance', '-')} / ≈{item.get('tokens', 0)} tok）")
    return "\n".join(lines)
