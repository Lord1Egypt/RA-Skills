#!/usr/bin/env python3
"""
拓扑甜甜圈关联引擎 (Topology Donut Engine)

功能：
- 读取面包屑条目，自动发现5种逻辑关联
- 聚合成拓扑甜甜圈（闭环/嵌套/分支/链状）
- 生成 donuts.json 独立存储，不污染主数据
- 支持手动调用或任意调度器（cron/任务计划程序/Launchd等）定时触发
- 艾宾浩斯复习时可按关联扩展展示

5种关联类型：
1. tag_cluster       标签聚类 — 共享≥2个标签
2. content_bridge    内容桥接 — 标题/内容共现≥3个关键词
3. source_family     同源家族 — 来源文件在同一目录
4. sequential_chain  序贯链接 — auto_source引用链
5. conceptual_hierarchy 概念层级 — 标题含包含关系

甜甜圈类型：
- closed    闭环 — 多节点形成闭合环路
- nested    嵌套 — 小甜甜圈完全包含在大甜甜圈内
- branching 分支 — 从一个中心节点发散
- chain     链状 — 线性串联
"""

import argparse
import json
import os
import sys
import re
from collections import defaultdict, Counter
from datetime import datetime
from itertools import combinations
from pathlib import Path

# ── 常量 ──────────────────────────────────────────────

SKILL_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = SKILL_DIR.parent / ".standardization" / "everything-search-breadmemory" / "data"
DONUT_FILE = DATA_DIR / "donuts.json"
BREADCRUMB_FILE = DATA_DIR / "breadcrumb.json"

# 关联阈值（可调）
TAG_OVERLAP_MIN = 2          # 最少共享标签数
KEYWORD_OVERLAP_MIN = 2      # 最少共现关键词数
KEYWORD_MIN_LEN = 2          # 关键词最短长度（字符）
SOURCE_FAMILY_MIN = 2        # 最少同源条目数
HIERARCHY_CONFIDENCE = 0.6   # 概念层级置信度阈值

# 中文停用词（常见无意义词）
STOP_WORDS = {
    "的", "是", "在", "和", "了", "有", "不", "也", "与", "及",
    "或", "为", "等", "从", "到", "对", "以", "将", "所", "但",
    "而", "且", "就", "要", "能", "会", "可", "被", "让", "用",
    "中", "上", "下", "内", "外", "前", "后", "左", "右",
    "一个", "没有", "自己", "什么", "这个", "那个", "这样", "那种",
    "可以", "必须", "应该", "不能", "需要", "知道",
    "因为", "所以", "如果", "虽然", "但是", "而且", "然后",
    "因此", "于是", "接着", "最后", "首先", "其次", "再次",
    "主要", "基本", "一般", "相关", "具体", "不同", "其他",
    "如何", "怎么", "怎样", "是否", "什么", "哪些", "哪里",
    "通过", "使用", "根据", "按照", "关于", "对于", "除了",
    "所有", "全部", "很多", "一些", "部分", "大多数",
    "目前", "现在", "之前", "之后", "以后", "以前",
    "一种", "用来", "能够", "其中", "进行", "作为",
    "它们", "他们", "这些", "那些", "这里", "那里",
}


# ── 工具函数 ──────────────────────────────────────────

def load_breadcrumbs():
    """加载面包屑条目（直接读JSON，不依赖breadcrumb.py）"""
    if not BREADCRUMB_FILE.exists():
        return []
    with open(BREADCRUMB_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("entries", [])


def load_donuts():
    """加载现有甜甜圈数据"""
    if not DONUT_FILE.exists():
        return {"generated_at": None, "associations": [], "donuts": []}
    with open(DONUT_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_donuts(data):
    """保存甜甜圈数据"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    data["generated_at"] = datetime.now().isoformat()
    with open(DONUT_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def extract_keywords(text):
    """
    从文本中提取关键词。
    简化策略：按常见分隔符切分，过滤停用词和短词。
    不依赖第三方分词库，保持跨平台零依赖。
    """
    if not text:
        return set()
    # 按非中文字符+常见英文分隔符切分
    words = re.findall(r'[\u4e00-\u9fff\u3400-\u4dbf]{2,}', text)
    # 也可以提取英文/数字词
    en_words = re.findall(r'[a-zA-Z0-9]{2,}', text)
    words.extend(en_words)
    # 过滤停用词和短词
    result = set()
    for w in words:
        w_lower = w.lower()
        if w_lower not in STOP_WORDS and len(w) >= KEYWORD_MIN_LEN:
            result.add(w_lower)
    return result


def get_entry_text(entry):
    """获取条目的可搜索文本：标题 + 内容"""
    parts = []
    if entry.get("title"):
        parts.append(entry["title"])
    if entry.get("content"):
        parts.append(entry["content"])
    return " ".join(parts)


# ── 5种关联检测算法 ───────────────────────────────────

def detect_tag_clusters(entries):
    """
    类型1：标签聚类 (tag_cluster)
    共享 ≥ TAG_OVERLAP_MIN 个标签的条目对。
    """
    associations = []
    seen = set()

    for i, a in enumerate(entries):
        tags_a = set(a.get("tags", []))
        if len(tags_a) < TAG_OVERLAP_MIN:
            continue
        for j, b in enumerate(entries):
            if i >= j:
                continue
            tags_b = set(b.get("tags", []))
            shared = tags_a & tags_b
            if len(shared) >= TAG_OVERLAP_MIN:
                pair_key = tuple(sorted([a["id"], b["id"]]))
                if pair_key in seen:
                    continue
                seen.add(pair_key)
                associations.append({
                    "id": f"asc_tc_{len(associations)+1:03d}",
                    "type": "tag_cluster",
                    "node_a": a["id"],
                    "node_b": b["id"],
                    "edge_label": f"共享标签: {', '.join(sorted(shared))}",
                    "logic": f"「{a['title']}」与「{b['title']}」共享 {len(shared)} 个标签: {', '.join(sorted(shared))}，属于同一知识领域，关联复习可加深领域认知",
                    "strength": min(len(shared) / max(len(tags_a), len(tags_b), 1), 1.0),
                    "evidence": {"shared_tags": sorted(shared)}
                })
    return associations


def detect_content_bridges(entries):
    """
    类型2：内容桥接 (content_bridge)
    标题/内容共现 ≥ KEYWORD_OVERLAP_MIN 个关键词的条目对。
    """
    # 先为每个条目提取关键词集合
    entry_keywords = {}
    for e in entries:
        text = get_entry_text(e)
        entry_keywords[e["id"]] = extract_keywords(text)

    associations = []
    seen = set()

    for i, a in enumerate(entries):
        kws_a = entry_keywords.get(a["id"], set())
        if len(kws_a) < KEYWORD_OVERLAP_MIN:
            continue
        for j, b in enumerate(entries):
            if i >= j:
                continue
            # 已通过标签聚类关联的，不重复
            tags_a = set(a.get("tags", []))
            tags_b = set(b.get("tags", []))
            if len(tags_a & tags_b) >= TAG_OVERLAP_MIN:
                continue

            kws_b = entry_keywords.get(b["id"], set())
            shared = kws_a & kws_b
            if len(shared) >= KEYWORD_OVERLAP_MIN:
                pair_key = tuple(sorted([a["id"], b["id"]]))
                if pair_key in seen:
                    continue
                seen.add(pair_key)
                top_shared = sorted(shared, key=lambda k: len(k), reverse=True)[:5]
                associations.append({
                    "id": f"asc_cb_{len(associations)+1:03d}",
                    "type": "content_bridge",
                    "node_a": a["id"],
                    "node_b": b["id"],
                    "edge_label": f"内容共现: {', '.join(top_shared)}",
                    "logic": f"「{a['title']}」与「{b['title']}」在标题/内容中共现 {len(shared)} 个关键词 {top_shared}，可能讨论同类话题，建议串联理解",
                    "strength": min(len(shared) / 10, 1.0),
                    "evidence": {"shared_keywords": sorted(shared)[:20]}
                })
    return associations


def detect_source_families(entries):
    """
    类型3：同源家族 (source_family)
    来源路径在同一目录下，或auto_source有交叉。
    """
    # 解析条目所属目录
    entry_dirs = {}
    for e in entries:
        dirs = set()
        # 主source
        src = e.get("source", "")
        if src:
            parent = str(Path(src).parent)
            if parent and parent != ".":
                dirs.add(parent)
        # auto_source
        for asrc in e.get("auto_source", []):
            parent = str(Path(asrc).parent)
            if parent and parent != ".":
                dirs.add(parent)
        if dirs:
            entry_dirs[e["id"]] = dirs

    associations = []
    seen = set()

    for i, a in enumerate(entries):
        dirs_a = entry_dirs.get(a["id"], set())
        for j, b in enumerate(entries):
            if i >= j:
                continue
            dirs_b = entry_dirs.get(b["id"], set())
            shared_dirs = dirs_a & dirs_b
            if shared_dirs:
                pair_key = tuple(sorted([a["id"], b["id"]]))
                if pair_key in seen:
                    continue
                seen.add(pair_key)
                sample_dir = sorted(shared_dirs)[0]
                associations.append({
                    "id": f"asc_sf_{len(associations)+1:03d}",
                    "type": "source_family",
                    "node_a": a["id"],
                    "node_b": b["id"],
                    "edge_label": f"同源: ...{sample_dir[-30:]}",
                    "logic": f"「{a['title']}」与「{b['title']}」的原文来源在同一目录 {sample_dir}，属于同一项目/主题的衍生知识，联动复习可形成项目全局视角",
                    "strength": len(shared_dirs) / max(len(dirs_a), len(dirs_b), 1),
                    "evidence": {"shared_dirs": sorted(shared_dirs)}
                })
    return associations


def detect_sequential_chains(entries):
    """
    类型4：序贯链接 (sequential_chain)
    通过 auto_source 引用链：A引用B的source → 形成序贯关系。
    同时检测标题中的序列模式（如"入门→进阶→高级"）。
    """
    # 构建source→entry映射
    source_to_ids = defaultdict(list)
    for e in entries:
        src = e.get("source", "")
        if src:
            source_to_ids[src].append(e["id"])

    associations = []
    seen = set()

    # 通过 auto_source 反向链接
    for e in entries:
        for asrc in e.get("auto_source", []):
            ref_ids = source_to_ids.get(asrc, [])
            for ref_id in ref_ids:
                if ref_id == e["id"]:
                    continue
                pair_key = tuple(sorted([e["id"], ref_id]))
                if pair_key in seen:
                    continue
                seen.add(pair_key)
                associations.append({
                    "id": f"asc_sc_{len(associations)+1:03d}",
                    "type": "sequential_chain",
                    "node_a": e["id"],
                    "node_b": ref_id,
                    "edge_label": f"序贯引用: {Path(asrc).name}",
                    "logic": f"「{e['title']}」引用/关联了「{ref_id}」的原文，形成知识演进链条，建议先复习被引用条目再复习本条",
                    "strength": 0.7,
                    "evidence": {"via_source": asrc}
                })

    return associations


def detect_conceptual_hierarchies(entries):
    """
    类型5：概念层级 (conceptual_hierarchy)
    检测标题间的包含/上下位关系：
    - A标题是B标题的子串 → A可能是B的细分
    - 通过标签数量判断一般vs具体
    """
    associations = []
    seen = set()

    for i, a in enumerate(entries):
        title_a = (a.get("title") or "").strip().lower()
        tags_a = set(a.get("tags", []))
        for j, b in enumerate(entries):
            if i >= j:
                continue
            title_b = (b.get("title") or "").strip().lower()
            tags_b = set(b.get("tags", []))

            parent = None
            child = None
            relation = ""

            # 检测标题包含关系
            if len(title_a) > 3 and len(title_b) > 3:
                if title_a in title_b and title_a != title_b:
                    parent, child = a, b
                    relation = f"「{a['title']}」是「{b['title']}」的上位概念"
                elif title_b in title_a and title_a != title_b:
                    parent, child = b, a
                    relation = f"「{b['title']}」是「{a['title']}」的上位概念"

            # 检测标签包含关系（B的标签是A标签的子集→A是上位）
            if not parent and tags_a and tags_b:
                if tags_b.issubset(tags_a) and len(tags_a) > len(tags_b):
                    parent, child = a, b
                    relation = f"「{a['title']}」(标签: {len(tags_a)}个) 涵盖「{b['title']}」(标签: {len(tags_b)}个)"
                elif tags_a.issubset(tags_b) and len(tags_b) > len(tags_a):
                    parent, child = b, a
                    relation = f"「{b['title']}」(标签: {len(tags_b)}个) 涵盖「{a['title']}」(标签: {len(tags_a)}个)"

            if parent and child:
                pair_key = tuple(sorted([parent["id"], child["id"]]))
                if pair_key in seen:
                    continue
                seen.add(pair_key)
                associations.append({
                    "id": f"asc_ch_{len(associations)+1:03d}",
                    "type": "conceptual_hierarchy",
                    "node_a": parent["id"],
                    "node_b": child["id"],
                    "edge_label": "上位概念→细分",
                    "logic": f"{relation}，建议先掌握上位概念「{parent['title']}」再深入细分「{child['title']}」，形成层级认知结构",
                    "strength": HIERARCHY_CONFIDENCE,
                    "evidence": {"parent_title": parent["title"], "child_title": child["title"]}
                })

    return associations


# ── 甜甜圈聚合 ────────────────────────────────────────

def build_graph(entries, associations):
    """从关联列表构建邻接表图"""
    graph = defaultdict(set)
    entry_map = {e["id"]: e for e in entries}
    for asc in associations:
        graph[asc["node_a"]].add(asc["node_b"])
        graph[asc["node_b"]].add(asc["node_a"])
    return graph, entry_map


def find_connected_components(graph):
    """找所有连通分量（BFS）"""
    visited = set()
    components = []
    for node in graph:
        if node in visited:
            continue
        comp = set()
        queue = [node]
        while queue:
            n = queue.pop(0)
            if n in visited:
                continue
            visited.add(n)
            comp.add(n)
            for neighbor in graph[n]:
                if neighbor not in visited:
                    queue.append(neighbor)
        if len(comp) >= 2:  # 至少2个节点才形成甜甜圈
            components.append(comp)
    return components


def classify_donut_type(subgraph, nodes, edge_ids):
    """
    分类甜甜圈类型：
    - closed:  每个节点度≥2 且 len(nodes)≥3 → 闭合环路
    - branching: 存在一个中心节点度远大于其他节点 → 星形分支
    - chain:   最长路径长度 = len(nodes) 且每个节点度≤2 → 链状
    - nested:  该甜甜圈的所有节点被另一个甜甜圈完全包含
    """
    n = len(nodes)
    if n < 2:
        return "chain"

    nodes_set = set(nodes)
    degrees = {node: len(subgraph.get(node, set()) & nodes_set) for node in nodes}
    max_deg = max(degrees.values()) if degrees else 0
    min_deg = min(degrees.values()) if degrees else 0

    # 判断branching：有1个中心节点度≥ 其他节点度*2
    center_candidates = [node for node, deg in degrees.items() if deg >= max_deg * 0.7]
    if len(center_candidates) == 1 and max_deg >= 3:
        return "branching"

    # 判断closed：所有节点度≥2 且 n≥3
    if n >= 3 and min_deg >= 2:
        return "closed"

    # 判断chain：大部分节点度≤2
    chain_nodes = sum(1 for d in degrees.values() if d <= 2)
    if chain_nodes >= n * 0.8:
        return "chain"

    return "branching"


def aggregate_donuts(entries, associations):
    """
    将关联聚合成甜甜圈。
    先找连通分量，再分类甜甜圈类型，最后检测嵌套关系。
    """
    graph, entry_map = build_graph(entries, associations)
    components = find_connected_components(graph)

    # 构建关联索引（按节点）
    asc_by_node = defaultdict(list)
    asc_by_id = {}
    for asc in associations:
        asc_by_node[asc["node_a"]].append(asc)
        asc_by_node[asc["node_b"]].append(asc)
        asc_by_id[asc["id"]] = asc

    donuts = []
    for comp in components:
        # 收集该连通分量中的所有关联
        comp_edges = set()
        edge_ids = []
        for node in comp:
            for asc in asc_by_node[node]:
                if asc["node_a"] in comp and asc["node_b"] in comp:
                    edge_key = tuple(sorted([asc["node_a"], asc["node_b"]]))
                    if edge_key not in comp_edges:
                        comp_edges.add(edge_key)
                        edge_ids.append(asc["id"])

        # 提取子图
        subgraph = {node: {n for n in graph.get(node, set()) if n in comp} for node in comp}

        # 分类
        donut_type = classify_donut_type(subgraph, list(comp), edge_ids)

        # 生成甜甜圈名称（从条目标题取前2个+更多）
        titles = []
        for node_id in sorted(comp)[:3]:
            e = entry_map.get(node_id)
            if e:
                titles.append(e.get("title", node_id)[:15])
        name = " → ".join(titles)
        if len(comp) > 3:
            name += f" 等{len(comp)}项"

        # 生成逻辑说明
        type_desc = {
            "closed": "闭合环路",
            "branching": "分支发散结构",
            "chain": "线性知识链条",
        }
        logic = f"由 {len(comp)} 个面包屑组成的{type_desc.get(donut_type, '知识关联')}"

        donuts.append({
            "id": f"donut_{len(donuts)+1:03d}",
            "name": name,
            "type": donut_type,
            "description": logic,
            "nodes": sorted(comp),
            "edges": edge_ids,
            "logic": logic,
            "parent_donut": None,
        })

    # 检测嵌套关系
    for i, di in enumerate(donuts):
        for j, dj in enumerate(donuts):
            if i >= j:
                continue
            set_i = set(di["nodes"])
            set_j = set(dj["nodes"])
            if set_i.issubset(set_j) and set_i != set_j:
                di["parent_donut"] = dj["id"]
                di["type"] = "nested"
            elif set_j.issubset(set_i) and set_i != set_j:
                dj["parent_donut"] = di["id"]
                dj["type"] = "nested"

    return donuts


# ── 生成与查询 ─────────────────────────────────────────

def generate(entries):
    """执行完整的拓扑甜甜圈生成流程"""
    all_associations = []
    all_associations.extend(detect_tag_clusters(entries))
    all_associations.extend(detect_content_bridges(entries))
    all_associations.extend(detect_source_families(entries))
    all_associations.extend(detect_sequential_chains(entries))
    all_associations.extend(detect_conceptual_hierarchies(entries))

    # 去重（同一条目对只保留强度最高的关联）
    deduped = {}
    for asc in all_associations:
        key = tuple(sorted([asc["node_a"], asc["node_b"]]))
        if key not in deduped or asc["strength"] > deduped[key]["strength"]:
            deduped[key] = asc

    associations = sorted(deduped.values(), key=lambda a: a["strength"], reverse=True)

    # 聚合甜甜圈
    donuts = aggregate_donuts(entries, associations)

    # 统计
    type_counts = Counter(a["type"] for a in associations)
    linked_ids = set()
    for a in associations:
        linked_ids.add(a["node_a"])
        linked_ids.add(a["node_b"])

    data = {
        "generated_at": datetime.now().isoformat(),
        "source_entry_count": len(entries),
        "statistics": {
            "total_associations": len(associations),
            "total_donuts": len(donuts),
            "by_type": dict(type_counts),
            "linked_entries": len(linked_ids),
            "coverage_rate": round(len(linked_ids) / max(len(entries), 1), 2),
            "donut_types": dict(Counter(d["type"] for d in donuts)),
        },
        "associations": associations,
        "donuts": donuts,
    }

    save_donuts(data)
    return data


def show_donut(donut_id=None, entry_id=None):
    """查看甜甜圈详情"""
    data = load_donuts()
    if not data.get("donuts"):
        print(json.dumps({"error": "暂无甜甜圈数据，请先执行 generate"}, ensure_ascii=False))
        return

    entries = load_breadcrumbs()
    entry_map = {e["id"]: e for e in entries}

    if entry_id:
        # 查找包含该条目的甜甜圈
        matching = [d for d in data["donuts"] if entry_id in d["nodes"]]
        if not matching:
            print(json.dumps({"error": f"条目 {entry_id} 不属于任何甜甜圈"}, ensure_ascii=False))
            return

        result = {"entry_id": entry_id, "belongs_to": []}
        for donut in matching:
            asc_by_node = {}
            for a in data["associations"]:
                if a["id"] in donut["edges"]:
                    asc_by_node[(a["node_a"], a["node_b"])] = a

            nodes_info = []
            for nid in donut["nodes"]:
                e = entry_map.get(nid, {})
                nodes_info.append({
                    "id": nid,
                    "title": e.get("title", nid),
                    "tags": e.get("tags", []),
                })

            result["belongs_to"].append({
                "donut_id": donut["id"],
                "donut_name": donut["name"],
                "type": donut["type"],
                "nodes": nodes_info,
                "logic": donut["logic"],
            })
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    if donut_id:
        for donut in data["donuts"]:
            if donut["id"] == donut_id:
                donut_result = dict(donut)
                donut_result["entries"] = []
                for nid in donut["nodes"]:
                    e = entry_map.get(nid, {})
                    donut_result["entries"].append({
                        "id": nid,
                        "title": e.get("title", nid),
                        "tags": e.get("tags", []),
                    })
                # 附上关联详情
                donut_result["edge_details"] = []
                for a in data["associations"]:
                    if a["id"] in donut["edges"]:
                        donut_result["edge_details"].append({
                            "id": a["id"],
                            "type": a["type"],
                            "between": [a["node_a"], a["node_b"]],
                            "label": a["edge_label"],
                            "logic": a["logic"],
                        })
                print(json.dumps(donut_result, ensure_ascii=False, indent=2))
                return
        print(json.dumps({"error": f"甜甜圈 {donut_id} 不存在"}, ensure_ascii=False))
        return

    # 列出所有甜甜圈摘要
    summary = []
    for d in data["donuts"]:
        summary.append({
            "id": d["id"],
            "name": d["name"],
            "type": d["type"],
            "node_count": len(d["nodes"]),
            "logic": d["logic"],
        })
    print(json.dumps({"total_donuts": len(summary), "donuts": summary}, ensure_ascii=False, indent=2))


def expand_for_review(entry_id):
    """
    复习扩展：给定一个条目ID，返回：
    1. 该条目所属的所有甜甜圈
    2. 每个甜甜圈中与其他条目的关联及逻辑说明
    便于艾宾浩斯复习时进行关联拓展
    """
    data = load_donuts()
    entries = load_breadcrumbs()
    entry_map = {e["id"]: e for e in entries}

    if not data.get("donuts"):
        return {"entry_id": entry_id, "expansions": [], "note": "暂无可用的拓扑关联数据"}

    matching_donuts = [d for d in data["donuts"] if entry_id in d["nodes"]]
    if not matching_donuts:
        return {
            "entry_id": entry_id,
            "entry_title": entry_map.get(entry_id, {}).get("title", entry_id),
            "expansions": [],
            "note": "该条目暂未加入任何拓扑甜甜圈，独立复习即可"
        }

    expansions = []
    for donut in matching_donuts:
        related_entries = []
        related_logics = []

        for nid in donut["nodes"]:
            if nid == entry_id:
                continue
            e = entry_map.get(nid, {})
            # 找到连接关系
            for a in data["associations"]:
                if a["id"] in donut["edges"] and (a["node_a"] == nid or a["node_b"] == nid):
                    if a["node_a"] == entry_id or a["node_b"] == entry_id:
                        related_entries.append({
                            "id": nid,
                            "title": e.get("title", nid),
                            "tags": e.get("tags", []),
                            "review_count": e.get("review_count", 0),
                            "next_review_at": e.get("next_review_at"),
                            "association_type": a["type"],
                            "association_label": a["edge_label"],
                        })
                        related_logics.append(f"  - [{a['type']}] {a['logic']}")

        expansions.append({
            "donut_id": donut["id"],
            "donut_name": donut["name"],
            "donut_type": donut["type"],
            "donut_logic": donut["logic"],
            "related_entries": related_entries,
            "study_suggestion": "\n".join(related_logics) if related_logics else "无直接关联逻辑",
        })

    return {
        "entry_id": entry_id,
        "entry_title": entry_map.get(entry_id, {}).get("title", entry_id),
        "expansions": expansions,
        "suggestion": f"该条目属于 {len(matching_donuts)} 个拓扑甜甜圈，复习时可关联 {sum(len(e['related_entries']) for e in expansions)} 个相关条目，加强知识串联理解"
    }


# ── CLI ───────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="拓扑甜甜圈关联引擎 - 面包屑知识图谱",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python topology_donut.py generate           # 生成拓扑甜甜圈
  python topology_donut.py show-donut         # 列出所有甜甜圈
  python topology_donut.py show-donut --id donut_001   # 查看指定甜甜圈
  python topology_donut.py show-donut --entry-id abc123  # 查看条目所属甜甜圈
  python topology_donut.py expand --id abc123  # 复习扩展
  python topology_donut.py stats               # 统计信息

定时调度（任意平台）:
  # Linux/macOS cron: 每天凌晨2点更新
  0 2 * * * /usr/bin/python3 ~/.workbuddy/skills/everything-search-breadmemory/scripts/topology_donut.py generate

  # Windows 任务计划程序: 每天
  schtasks /create /tn "拓扑甜甜圈更新" /tr "python topology_donut.py generate" /sc daily /st 02:00

  # WorkBuddy 自动化
  使用 automation_update 工具创建，调用: python topology_donut.py generate
        """
    )
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # generate
    subparsers.add_parser("generate", help="生成/更新拓扑甜甜圈")

    # show-donut
    show_parser = subparsers.add_parser("show-donut", help="查看甜甜圈")
    show_parser.add_argument("--id", help="甜甜圈ID")
    show_parser.add_argument("--entry-id", help="查找包含该条目的甜甜圈")

    # expand
    expand_parser = subparsers.add_parser("expand", help="复习扩展：获取与某条目关联的所有面包屑")
    expand_parser.add_argument("--id", required=True, help="条目ID")

    # stats
    subparsers.add_parser("stats", help="甜甜圈统计信息")

    args = parser.parse_args()

    if args.command == "generate":
        entries = load_breadcrumbs()
        if len(entries) < 2:
            print(json.dumps({
                "status": "skipped",
                "reason": f"面包屑数量不足（当前: {len(entries)}，需要 ≥ 2），无法生成甜甜圈",
            }, ensure_ascii=False, indent=2))
            return
        result = generate(entries)
        print(json.dumps({
            "status": "generated",
            "generated_at": result["generated_at"],
            "statistics": result["statistics"],
            "file": str(DONUT_FILE),
        }, ensure_ascii=False, indent=2))

    elif args.command == "show-donut":
        show_donut(donut_id=args.id, entry_id=args.entry_id)

    elif args.command == "expand":
        result = expand_for_review(args.id)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif args.command == "stats":
        data = load_donuts()
        if not data.get("donuts"):
            print(json.dumps({"status": "empty", "note": "暂未生成甜甜圈，请先执行 generate"}, ensure_ascii=False))
            return
        print(json.dumps({
            "generated_at": data.get("generated_at"),
            "statistics": data.get("statistics", {}),
            "file": str(DONUT_FILE),
        }, ensure_ascii=False, indent=2))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
