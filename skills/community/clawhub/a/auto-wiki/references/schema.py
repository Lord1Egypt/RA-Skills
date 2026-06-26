"""Wiki 页面 frontmatter 的 Pydantic 校验模型。

用法：
    python schema.py .wiki/my-research/
    python schema.py .wiki/my-research/entities/alpha-corp.md

Agent 在 ingest 完成后应自动运行校验。lint 操作也会调用。
"""

from __future__ import annotations

import sys
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Any, Optional, Union

import yaml
from pydantic import BaseModel, Field, field_validator, model_validator


# ── 枚举 ──────────────────────────────────────────────────

class PageType(str, Enum):
    source = "source"
    entity = "entity"
    concept = "concept"
    analysis = "analysis"
    mental_model = "mental-model"


class Confidence(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"
    contested = "contested"


class SourceType(str, Enum):
    primary = "primary"
    authoritative_secondary = "authoritative-secondary"
    secondary = "secondary"
    hearsay = "hearsay"
    inference = "inference"
    oral = "oral"


# ── 关系 ──────────────────────────────────────────────────

class Relation(BaseModel):
    """页面间的类型化关系。"""
    target: str                             # 目标页面 slug
    type: str                               # 关系类型

    @field_validator("type")
    @classmethod
    def known_type(cls, v: str) -> str:
        """建议使用标准关系类型，但不强制。"""
        standard = {
            "part_of", "manages", "regulated_by", "competes_with",
            "implements", "derived_from", "contradicts", "influenced_by",
            "applies_to", "supplies", "subsidiary_of", "contrasted_with",
        }
        if v not in standard:
            import warnings
            warnings.warn(
                f"非标准关系类型 '{v}'（允许使用，但建议对齐标准类型：{', '.join(sorted(standard))}）",
                stacklevel=2,
            )
        return v


# ── 三重验证（cognitive 类型专用）──────────────────────────

class MentalModelVerification(BaseModel):
    """心智模型的三重验证结果。"""
    cross_domain: bool = False              # 跨域复现
    generative: bool = False                # 有生成力
    exclusive: bool = False                 # 有排他性
    domains: list[str] = Field(default_factory=list)  # 出现过的领域


# ── 页面基类 ──────────────────────────────────────────────

class BasePage(BaseModel):
    """所有页面的公共字段。"""
    title: str
    type: PageType
    created: Union[str, date]               # YYYY-MM-DD（YAML 可能解析为 date 对象）
    updated: Union[str, date]               # YYYY-MM-DD
    sources: list[str] = Field(default_factory=list)
    confidence: Confidence = Confidence.high

    @field_validator("created", "updated", mode="before")
    @classmethod
    def coerce_date(cls, v: Any) -> str:
        """YAML 会把 2026-04-07 自动解析为 datetime.date，统一转为 str。"""
        if isinstance(v, date):
            return v.isoformat()
        if isinstance(v, str):
            try:
                date.fromisoformat(v)
            except ValueError:
                raise ValueError(f"日期必须为 YYYY-MM-DD 格式: {v}")
            return v
        raise ValueError(f"日期类型错误: {type(v)}")


class SourcePage(BasePage):
    """source 类型页面。"""
    type: PageType = PageType.source
    source_type: SourceType
    source_origin: str                      # 来源出处
    source_date: Union[str, date]           # 原始材料日期
    source_url: str = ""                    # 来源 URL

    @field_validator("source_date", mode="before")
    @classmethod
    def coerce_source_date(cls, v: Any) -> str:
        if isinstance(v, date):
            return v.isoformat()
        return v

    @model_validator(mode="after")
    def sources_should_be_empty(self) -> "SourcePage":
        if self.sources:
            raise ValueError("source 类型页面的 sources 应为空列表")
        return self


class DataPage(BasePage):
    """entity / concept / analysis 页面。
    结构化数据（data/history）存在 data.db 中，不在 frontmatter。
    relations 保留在 frontmatter（Obsidian wikilink 渲染），同时写入 data.db。
    """
    relations: list[Relation] = Field(default_factory=list)

    @model_validator(mode="after")
    def sources_not_empty(self) -> "DataPage":
        if self.type != PageType.source and not self.sources:
            raise ValueError(f"{self.type.value} 类型页面的 sources 不能为空")
        return self


class MentalModelPage(BasePage):
    """mental-model 类型页面（cognitive wiki 专用）。"""
    type: PageType = PageType.mental_model
    verification: Optional[MentalModelVerification] = None
    relations: list[Relation] = Field(default_factory=list)


# ── 解析与校验 ────────────────────────────────────────────

def parse_frontmatter(path: Path) -> dict[str, Any]:
    """从 markdown 文件中提取 YAML frontmatter。"""
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        raise ValueError(f"页面缺少 YAML frontmatter: {path}")
    parts = text.split("---", 2)
    if len(parts) < 3:
        raise ValueError(f"YAML frontmatter 格式错误: {path}")
    return yaml.safe_load(parts[1]) or {}


def validate_page(path: Path) -> tuple[bool, str]:
    """校验单个页面。返回 (通过?, 消息)。"""
    try:
        fm = parse_frontmatter(path)
    except Exception as e:
        return False, f"PARSE ERROR: {e}"

    page_type = fm.get("type", "")
    warnings_list: list[str] = []

    # data/history 应在 data.db 中，不在 frontmatter
    if "data" in fm and fm["data"]:
        warnings_list.append("MIGRATE: frontmatter 中有 data 字段，应迁移到 data.db（python store.py init）")
    if "history" in fm and fm["history"]:
        warnings_list.append("MIGRATE: frontmatter 中有 history 字段，应迁移到 data.db")

    # 从 fm 中移除 data/history 避免 Pydantic 报错（模型已不包含这些字段）
    fm_clean = {k: v for k, v in fm.items() if k not in ("data", "history")}

    try:
        if page_type == "source":
            SourcePage(**fm_clean)
        elif page_type == "mental-model":
            MentalModelPage(**fm_clean)
        elif page_type in ("entity", "concept", "analysis"):
            DataPage(**fm_clean)
        else:
            return False, f"UNKNOWN TYPE: {page_type}"
        if warnings_list:
            return True, "OK (⚠️ " + "; ".join(warnings_list) + ")"
        return True, "OK"
    except Exception as e:
        return False, f"VALIDATION ERROR: {e}"


def validate_wiki(wiki_dir: Path) -> list[tuple[str, bool, str]]:
    """校验整个 wiki 目录。返回 [(文件名, 通过?, 消息)]。"""
    results = []
    for subdir in ["sources", "entities", "concepts", "analyses", "mental-models"]:
        d = wiki_dir / subdir
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            if f.name.startswith("_"):
                continue
            ok, msg = validate_page(f)
            rel = f.relative_to(wiki_dir)
            results.append((str(rel), ok, msg))
    return results


# ── Report 数据提取 ──────────────────────────────────────

import json
import re
from collections import Counter

def _page_body(path: Path) -> str:
    """读取 markdown 正文（frontmatter 之后的部分）。"""
    text = path.read_text(encoding="utf-8")
    parts = text.split("---", 2)
    return parts[2] if len(parts) >= 3 else ""

def _extract_wikilinks(body: str) -> list[str]:
    """提取正文中的 [[slug]] 或 [[slug|display]] 链接。"""
    return re.findall(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]", body)

def collect_report_data(wiki_dir: Path) -> dict[str, Any]:
    """扫描 wiki 目录，提取完整的报告数据。"""
    meta_path = wiki_dir / "meta.yaml"
    meta = {}
    if meta_path.exists():
        meta = yaml.safe_load(meta_path.read_text(encoding="utf-8")) or {}

    nodes: list[dict] = []
    edges: list[dict] = []
    data_rows: list[dict] = []
    type_counts: Counter = Counter()
    confidence_counts: Counter = Counter()
    contested_pages: list[str] = []
    inlink_counts: Counter = Counter()
    page_slugs: set[str] = set()
    freshness: list[dict] = []

    subdirs = ["sources", "entities", "concepts", "analyses", "mental-models"]
    for subdir in subdirs:
        d = wiki_dir / subdir
        if not d.exists():
            continue
        for f in sorted(d.glob("*.md")):
            if f.name.startswith("_"):
                continue
            slug = f.stem
            page_slugs.add(slug)
            rel_path = str(f.relative_to(wiki_dir))

            try:
                fm = parse_frontmatter(f)
            except Exception:
                continue

            page_type = fm.get("type", "unknown")
            confidence = fm.get("confidence", "unknown")
            title = fm.get("title", slug)
            updated = str(fm.get("updated", ""))

            type_counts[page_type] += 1
            confidence_counts[confidence] += 1

            if confidence == "contested":
                contested_pages.append(rel_path)

            # 节点颜色按类型
            color_map = {
                "entity": "#4A90D9",
                "concept": "#7B68EE",
                "source": "#50C878",
                "analysis": "#FF8C00",
                "mental-model": "#E91E63",
            }
            nodes.append({
                "id": slug,
                "label": title,
                "type": page_type,
                "color": color_map.get(page_type, "#999"),
                "confidence": confidence,
                "updated": updated,
                "path": rel_path,
            })

            freshness.append({"slug": slug, "updated": updated, "type": page_type})

            # 关系 → 边
            for rel in fm.get("relations", []):
                target = rel.get("target", "")
                rel_type = rel.get("type", "")
                if target:
                    edges.append({
                        "from": slug,
                        "to": target,
                        "label": rel_type,
                    })

            # 正文 wikilinks → 入链统计
            body = _page_body(f)
            for linked_slug in _extract_wikilinks(body):
                inlink_counts[linked_slug] += 1

    # 从 data.db 读取结构化数据（唯一数据源）
    db_path = wiki_dir / "data.db"
    if db_path.exists():
        import sqlite3 as _sqlite3
        _conn = _sqlite3.connect(str(db_path))
        _conn.row_factory = _sqlite3.Row
        for r in _conn.execute("SELECT * FROM data_points ORDER BY page_slug, field").fetchall():
            page_title = r["page_slug"]
            pg = _conn.execute("SELECT title FROM pages WHERE slug=?", (r["page_slug"],)).fetchone()
            if pg:
                page_title = pg["title"]
            data_rows.append({
                "page": page_title, "slug": r["page_slug"], "field": r["field"],
                "value": r["value"], "unit": r["unit"], "period": r["period"],
                "source": r["source_slug"], "verified": r["verified"],
                "confidence": r["confidence"] or "high",
            })
        # DB relations 补充 frontmatter edges
        edge_set = {(e["from"], e["to"], e["label"]) for e in edges}
        for r in _conn.execute("SELECT * FROM relations").fetchall():
            key = (r["from_slug"], r["to_slug"], r["type"])
            if key not in edge_set:
                edges.append({"from": r["from_slug"], "to": r["to_slug"], "label": r["type"]})
        # DB contested 补充
        contested_set = set(contested_pages)
        for r in _conn.execute("SELECT DISTINCT page_slug FROM data_points WHERE confidence='contested'").fetchall():
            for n in nodes:
                if n["id"] == r["page_slug"] and n["path"] not in contested_set:
                    contested_pages.append(n["path"])
                    contested_set.add(n["path"])
        _conn.close()

    # frontmatter relations 也算入链
    for edge in edges:
        inlink_counts[edge["to"]] += 1

    # 覆盖度分析
    coverage_gaps: list[dict] = []
    for slug in page_slugs:
        inlinks = inlink_counts.get(slug, 0)
        node = next((n for n in nodes if n["id"] == slug), None)
        if not node:
            continue
        if inlinks == 0 and node["type"] != "source":
            coverage_gaps.append({
                "slug": slug,
                "issue": "orphan",
                "detail": f"零入链（无其他页面引用）",
            })

    # 被大量引用但内容可能薄的页面（通过 wikilink 被引用但不在 page_slugs 中）
    for linked, count in inlink_counts.most_common():
        if linked not in page_slugs and count >= 2:
            coverage_gaps.append({
                "slug": linked,
                "issue": "missing",
                "detail": f"被引用 {count} 次但页面不存在",
            })

    return {
        "name": meta.get("name", wiki_dir.name),
        "ontology_type": meta.get("ontology_type", "unknown"),
        "description": meta.get("description", ""),
        "seed": meta.get("seed", ""),
        "total_pages": len(nodes),
        "type_counts": dict(type_counts),
        "confidence_counts": dict(confidence_counts),
        "contested_pages": contested_pages,
        "nodes": nodes,
        "edges": edges,
        "data_rows": data_rows,
        "freshness": freshness,
        "coverage_gaps": coverage_gaps,
    }


REPORT_HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Wiki Report: {{WIKI_NAME}}</title>
<script src="https://unpkg.com/vis-network@9.1.9/standalone/umd/vis-network.min.js"></script>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { font-family: -apple-system, "Noto Sans SC", sans-serif; background: #f0f2f5; color: #1a1a1a; height: 100vh; overflow: hidden; }

  .layout { display: flex; height: 100vh; }

  /* ── Left: header + cards + graph ── */
  .left { flex: 0 0 55%; display: flex; flex-direction: column; height: 100vh; border-right: 1px solid #e0e0e0; }
  .left-header { padding: 16px 20px 0; flex-shrink: 0; }
  h1 { font-size: 18px; font-weight: 600; color: #111; }
  .subtitle { color: #999; font-size: 12px; margin-top: 2px; }
  .cards { display: flex; gap: 8px; padding: 12px 20px 0; flex-shrink: 0; }
  .card { background: #fff; border-radius: 6px; padding: 8px 14px; border: 1px solid #e0e0e0; flex: 1; min-width: 0; }
  .card .num { font-size: 20px; font-weight: 700; color: #111; }
  .card .label { font-size: 10px; color: #aaa; margin-top: 1px; text-transform: uppercase; }
  .legend { display: flex; gap: 12px; flex-wrap: wrap; padding: 10px 20px 6px; flex-shrink: 0; }
  .legend-item { display: flex; align-items: center; gap: 4px; font-size: 11px; color: #888; }
  .legend-dot { width: 8px; height: 8px; border-radius: 50%; }
  .graph-container { flex: 1; min-height: 0; margin: 0 12px 12px; background: #fff; border-radius: 8px; border: 1px solid #e0e0e0; }

  /* ── Right: node detail + tables ── */
  .right { flex: 0 0 45%; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
  .right-scroll { flex: 1; overflow-y: auto; padding: 16px 20px; display: flex; flex-direction: column; gap: 12px; }
  .right-scroll::-webkit-scrollbar { width: 4px; }
  .right-scroll::-webkit-scrollbar-thumb { background: #d0d0d0; border-radius: 2px; }

  /* ── Node detail ── */
  .node-detail { background: #fff; border-radius: 8px; border: 1px solid #e0e0e0; overflow: hidden; flex-shrink: 0; display: none; }
  .node-detail.active { display: block; }
  .nd-header { padding: 10px 14px; background: #fafafa; border-bottom: 1px solid #eee; display: flex; align-items: center; justify-content: space-between; }
  .nd-header h3 { font-size: 14px; font-weight: 600; }
  .nd-close { cursor: pointer; color: #aaa; font-size: 16px; padding: 0 4px; }
  .nd-close:hover { color: #333; }
  .nd-body { padding: 12px 14px; font-size: 12px; color: #555; line-height: 1.7; }
  .nd-body b { color: #333; }
  .nd-section { margin-top: 8px; }
  .nd-row { display: flex; justify-content: space-between; padding: 3px 0; border-bottom: 1px solid #f5f5f5; }
  .nd-row:last-child { border-bottom: none; }
  .nd-key { color: #888; }
  .nd-val { font-weight: 600; color: #111; }
  .nd-rel { padding: 2px 0; }
  .nd-rel-arrow { color: #bbb; margin: 0 4px; }

  /* ── Panel ── */
  .panel { background: #fff; border-radius: 8px; border: 1px solid #e0e0e0; overflow: hidden; flex-shrink: 0; }
  .panel-header { padding: 9px 14px; font-size: 11px; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.5px; background: #fafafa; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center; }
  .panel-count { background: #eee; color: #666; padding: 1px 6px; border-radius: 3px; font-size: 10px; }

  /* ── Table ── */
  table { width: 100%; border-collapse: collapse; }
  th { text-align: left; padding: 7px 12px; font-size: 10px; color: #aaa; font-weight: 600; text-transform: uppercase; }
  td { padding: 6px 12px; font-size: 12px; border-top: 1px solid #f3f3f3; }
  .r { text-align: right; }
  tr:hover td { background: #f8f9fb; }

  .badge { display: inline-block; padding: 1px 7px; border-radius: 3px; font-size: 10px; font-weight: 600; }
  .badge-high { background: #dcfce7; color: #166534; }
  .badge-medium { background: #fef9c3; color: #854d0e; }
  .badge-low { background: #fee2e2; color: #991b1b; }
  .badge-contested { background: #f3e8ff; color: #7c3aed; }
  .badge-entity { background: #dbeafe; color: #1e40af; }
  .badge-concept { background: #ede9fe; color: #5b21b6; }
  .badge-source { background: #dcfce7; color: #166534; }
  .badge-analysis { background: #ffedd5; color: #9a3412; }
  .badge-mental-model { background: #fce7f3; color: #be185d; }
  .badge-orphan { background: #fee2e2; color: #991b1b; }
  .badge-missing { background: #fef9c3; color: #854d0e; }
  .empty { color: #ccc; font-style: italic; padding: 14px; text-align: center; font-size: 12px; }

  /* ── Hint overlay on graph ── */
  .graph-hint { position: absolute; bottom: 8px; left: 50%; transform: translateX(-50%); font-size: 11px; color: #bbb; pointer-events: none; transition: opacity 0.3s; }
</style>
</head>
<body>
<div class="layout">

  <!-- ── LEFT ── -->
  <div class="left">
    <div class="left-header">
      <h1>{{WIKI_NAME}}</h1>
      <div class="subtitle">{{WIKI_DESC}} · {{ONTOLOGY_TYPE}} · {{TOTAL_PAGES}} pages</div>
    </div>
    <div class="cards" id="cards"></div>
    <div class="legend" id="legend"></div>
    <div class="graph-container" id="graph" style="position:relative;">
      <div class="graph-hint" id="graph-hint">click a node to inspect</div>
    </div>
  </div>

  <!-- ── RIGHT ── -->
  <div class="right">
    <div class="right-scroll">
      <div class="node-detail" id="node-detail">
        <div class="nd-header">
          <h3 id="nd-title"></h3>
          <span class="nd-close" id="nd-close">&times;</span>
        </div>
        <div class="nd-body" id="nd-body"></div>
      </div>
      <div class="panel">
        <div class="panel-header">Data Points <span class="panel-count" id="dp-count"></span></div>
        <div id="data-table"></div>
      </div>
      <div class="panel">
        <div class="panel-header">Pages <span class="panel-count" id="pg-count"></span></div>
        <div id="freshness-table"></div>
      </div>
      <div class="panel" id="contested-panel" style="display:none">
        <div class="panel-header">Contested <span class="panel-count" id="ct-count"></span></div>
        <div id="contested-list"></div>
      </div>
      <div class="panel" id="coverage-panel" style="display:none">
        <div class="panel-header">Coverage Gaps <span class="panel-count" id="cg-count"></span></div>
        <div id="coverage-table"></div>
      </div>
    </div>
  </div>
</div>

<script>
const DATA = {{JSON_DATA}};

// ── Cards ──
const cardsEl = document.getElementById('cards');
const cc = [
  { num: DATA.total_pages, label: 'Pages' },
  ...Object.entries(DATA.type_counts).map(([k,v]) => ({ num: v, label: k })),
  { num: DATA.contested_pages.length, label: 'Contested' },
  { num: DATA.edges.length, label: 'Relations' },
];
cardsEl.innerHTML = cc.map(c => `<div class="card"><div class="num">${c.num}</div><div class="label">${c.label}</div></div>`).join('');

// ── Legend ──
const cm = { entity:'#4A90D9', concept:'#7B68EE', source:'#50C878', analysis:'#FF8C00', 'mental-model':'#E91E63' };
document.getElementById('legend').innerHTML = Object.entries(cm).map(([t,c]) =>
  `<div class="legend-item"><div class="legend-dot" style="background:${c}"></div>${t}</div>`).join('');

// ── Graph ──
const hint = document.getElementById('graph-hint');
let network = null;
if (DATA.nodes.length > 0) {
  // count connections per node for sizing
  const connCount = {};
  DATA.edges.forEach(e => { connCount[e.from] = (connCount[e.from]||0)+1; connCount[e.to] = (connCount[e.to]||0)+1; });
  const maxConn = Math.max(1, ...Object.values(connCount));

  const graphNodes = DATA.nodes.filter(n => n.type !== 'source').map(n => {
    const c = connCount[n.id] || 0;
    const sz = 14 + (c / maxConn) * 22;
    return {
      id: n.id, label: n.label,
      color: { background: n.color, border: n.color, highlight: { background: '#fff', border: n.color } },
      font: { color: '#333', size: Math.max(12, sz * 0.65), face: '-apple-system, "Noto Sans SC", sans-serif' },
      shape: 'dot', size: sz,
    };
  });
  const nodeIds = new Set(graphNodes.map(n => n.id));
  DATA.edges.forEach(e => {
    [e.to, e.from].forEach(id => {
      if (!nodeIds.has(id)) {
        graphNodes.push({ id, label: id, color:{ background:'#e0e0e0', border:'#ccc' }, font:{ color:'#999', size:11 }, shape:'dot', size:10 });
        nodeIds.add(id);
      }
    });
  });

  // dedupe edges: same from→to pair, merge labels
  const edgeMap = {};
  DATA.edges.forEach(e => {
    const key = e.from + '→' + e.to;
    if (edgeMap[key]) { edgeMap[key].label += '\n' + e.label; }
    else { edgeMap[key] = { ...e }; }
  });
  const graphEdges = Object.values(edgeMap).map((e,i) => ({
    id: i, from: e.from, to: e.to, label: e.label,
    color: { color:'#d0d0d0', highlight:'#888' },
    font: { color:'#aaa', size:10, strokeWidth:3, strokeColor:'#fff', multi:'md', face:'monospace' },
    arrows: { to:{ scaleFactor:0.5 } },
    smooth: { type:'curvedCW', roundness: 0.18 },
  }));

  network = new vis.Network(document.getElementById('graph'), { nodes: graphNodes, edges: graphEdges }, {
    physics: {
      solver: 'forceAtlas2Based',
      forceAtlas2Based: { gravitationalConstant: -80, springLength: 200, springConstant: 0.04, damping: 0.6 },
      stabilization: { iterations: 150 },
    },
    interaction: { hover: true, tooltipDelay: 150, zoomView: true, navigationButtons: false },
    layout: { improvedLayout: true },
  });

  // fit after stabilize
  network.on('stabilized', () => { network.fit({ animation: { duration: 300 } }); });

  // ── Click node → right panel detail ──
  const ndEl = document.getElementById('node-detail');
  const ndTitle = document.getElementById('nd-title');
  const ndBody = document.getElementById('nd-body');
  document.getElementById('nd-close').onclick = () => { ndEl.classList.remove('active'); network.unselectAll(); };

  network.on('click', function(p) {
    if (!p.nodes.length) { ndEl.classList.remove('active'); return; }
    hint.style.opacity = '0';
    const nid = p.nodes[0];
    const node = DATA.nodes.find(n => n.id === nid);
    if (!node) return;
    ndTitle.textContent = node.label;

    let html = `<div><span class="badge badge-${node.type}">${node.type}</span> <span class="badge badge-${node.confidence}">${node.confidence}</span> &nbsp;${node.updated}</div>`;

    // data points
    const dp = DATA.data_rows.filter(r => r.slug === nid);
    if (dp.length) {
      html += '<div class="nd-section"><b>Data</b></div>';
      dp.forEach(d => {
        html += `<div class="nd-row"><span class="nd-key">${d.field}</span><span class="nd-val">${d.value} ${d.unit} <span style="color:#aaa;font-weight:400">${d.period}</span></span></div>`;
      });
    }

    // relations
    const rels = DATA.edges.filter(e => e.from === nid || e.to === nid);
    if (rels.length) {
      html += '<div class="nd-section"><b>Relations</b></div>';
      rels.forEach(r => {
        if (r.from === nid)
          html += `<div class="nd-rel">${node.label} <span class="nd-rel-arrow">→</span> <span style="color:#7c3aed">${r.label}</span> <span class="nd-rel-arrow">→</span> ${r.to}</div>`;
        else
          html += `<div class="nd-rel">${r.from} <span class="nd-rel-arrow">→</span> <span style="color:#7c3aed">${r.label}</span> <span class="nd-rel-arrow">→</span> ${node.label}</div>`;
      });
    }

    ndBody.innerHTML = html;
    ndEl.classList.add('active');
    ndEl.scrollIntoView({ behavior:'smooth', block:'start' });
  });
} else {
  document.getElementById('graph').innerHTML = '<div class="empty">No nodes</div>';
}

// ── Data Table ──
document.getElementById('dp-count').textContent = DATA.data_rows.length;
const dtEl = document.getElementById('data-table');
if (DATA.data_rows.length) {
  dtEl.innerHTML = `<table><thead><tr><th>Page</th><th>Field</th><th class="r">Value</th><th>Unit</th><th>Period</th><th>Conf.</th></tr></thead><tbody>`
    + DATA.data_rows.map(r =>
      `<tr><td>${r.page}</td><td>${r.field}</td><td class="r"><b>${r.value}</b></td><td>${r.unit}</td><td>${r.period}</td><td><span class="badge badge-${r.confidence}">${r.confidence}</span></td></tr>`
    ).join('') + '</tbody></table>';
} else { dtEl.innerHTML = '<div class="empty">No data points</div>'; }

// ── Pages ──
document.getElementById('pg-count').textContent = DATA.freshness.length;
const ftEl = document.getElementById('freshness-table');
if (DATA.freshness.length) {
  const s = [...DATA.freshness].sort((a,b) => b.updated.localeCompare(a.updated));
  ftEl.innerHTML = `<table><thead><tr><th>Page</th><th>Type</th><th class="r">Updated</th></tr></thead><tbody>`
    + s.map(r => `<tr><td>${r.slug}</td><td><span class="badge badge-${r.type}">${r.type}</span></td><td class="r">${r.updated}</td></tr>`).join('')
    + '</tbody></table>';
} else { ftEl.innerHTML = '<div class="empty">No pages</div>'; }

// ── Contested ──
if (DATA.contested_pages.length) {
  document.getElementById('contested-panel').style.display = '';
  document.getElementById('ct-count').textContent = DATA.contested_pages.length;
  document.getElementById('contested-list').innerHTML = `<table><tbody>`
    + DATA.contested_pages.map(p => `<tr><td><span class="badge badge-contested">contested</span> &nbsp;${p}</td></tr>`).join('') + '</tbody></table>';
}

// ── Coverage ──
if (DATA.coverage_gaps.length) {
  document.getElementById('coverage-panel').style.display = '';
  document.getElementById('cg-count').textContent = DATA.coverage_gaps.length;
  document.getElementById('coverage-table').innerHTML = `<table><thead><tr><th>Page</th><th>Issue</th><th>Detail</th></tr></thead><tbody>`
    + DATA.coverage_gaps.map(r => `<tr><td>${r.slug}</td><td><span class="badge badge-${r.issue}">${r.issue}</span></td><td>${r.detail}</td></tr>`).join('')
    + '</tbody></table>';
}
</script>
</body>
</html>"""


def generate_report(wiki_dir: Path) -> Path:
    """生成 wiki 可视化报告 HTML。返回输出文件路径。"""
    data = collect_report_data(wiki_dir)
    html = REPORT_HTML_TEMPLATE
    html = html.replace("{{WIKI_NAME}}", data["name"])
    html = html.replace("{{WIKI_DESC}}", data.get("description", ""))
    html = html.replace("{{ONTOLOGY_TYPE}}", data.get("ontology_type", ""))
    html = html.replace("{{TOTAL_PAGES}}", str(data["total_pages"]))
    html = html.replace("{{JSON_DATA}}", json.dumps(data, ensure_ascii=False, default=str))

    out_path = wiki_dir / "_report.html"
    out_path.write_text(html, encoding="utf-8")
    return out_path


# ── CLI ───────────────────────────────────────────────────

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python schema.py <wiki_dir>           — validate all pages")
        print("  python schema.py <page.md>             — validate one page")
        print("  python schema.py --report <wiki_dir>   — generate visual report")
        sys.exit(1)

    # --report 模式
    if sys.argv[1] == "--report":
        if len(sys.argv) < 3:
            print("Usage: python schema.py --report <wiki_dir>")
            sys.exit(1)
        target = Path(sys.argv[2])
        if not target.is_dir():
            print(f"Not a directory: {target}")
            sys.exit(1)
        out = generate_report(target)
        print(f"Report generated: {out}")
        sys.exit(0)

    target = Path(sys.argv[1])

    if target.is_file():
        ok, msg = validate_page(target)
        status = "✅" if ok else "❌"
        print(f"{status} {target.name}: {msg}")
        sys.exit(0 if ok else 1)

    if target.is_dir():
        results = validate_wiki(target)
        if not results:
            print("No pages found.")
            sys.exit(0)

        passed = sum(1 for _, ok, _ in results if ok)
        failed = sum(1 for _, ok, _ in results if not ok)

        print(f"\n{'='*60}")
        print(f"Wiki Validation: {target.name}")
        print(f"{'='*60}\n")

        for name, ok, msg in results:
            status = "✅" if ok else "❌"
            print(f"  {status} {name}")
            if not ok:
                # 缩进显示错误详情
                for line in str(msg).split("\n"):
                    print(f"     {line}")

        print(f"\n{'─'*60}")
        print(f"  Total: {len(results)} | Passed: {passed} | Failed: {failed}")
        if failed == 0:
            print("  Result: ALL PASSED ✅")
        else:
            print(f"  Result: {failed} FAILED ❌")
        print(f"{'─'*60}\n")

        sys.exit(0 if failed == 0 else 1)

    print(f"Not a file or directory: {target}")
    sys.exit(1)


if __name__ == "__main__":
    main()
