"""
knowgraph.py — UP主知识图谱可视化 (v1.11.0)

基于 speaker_db + wiki 已有数据，生成交互式 D3.js 力导向图
输出 HTML 文件，可在浏览器/手机中打开
"""

import os, json, re, time
from typing import Dict, List, Tuple
from collections import Counter

from .paths import storage_path

SPEAKER_DB = os.path.expanduser("~/.biliyoutik2brain_speakers.json")
WIKI_DIR = os.path.expanduser("~/wiki/wiki")
OUTPUT_DIR = storage_path("knowgraph")


def load_speakers() -> Dict:
    if os.path.exists(SPEAKER_DB):
        with open(SPEAKER_DB) as f:
            return json.load(f)
    return {}


def build_nodes_edges(db: Dict) -> Tuple[List[dict], List[dict]]:
    """从 speaker_db 构建节点和边"""
    nodes = []
    edges = []
    speaker_ids = {}

    domain_colors = {
        "trading": "#e74c3c",
        "tech": "#3498db",
        "general": "#2ecc71",
    }

    for i, (name, profile) in enumerate(db.items()):
        sid = f"sp_{i}"
        speaker_ids[name] = sid

        domain = profile.get("domain", "general")
        videos = profile.get("processed_videos", [])
        topics = profile.get("common_topics", [])
        ck = profile.get("core_knowledge", {})
        sf = profile.get("skill_feedback", {})

        # 节点大小 = 视频数量 + 知识丰富度
        knowledge_count = sum(len(v) for v in ck.values())
        hotword_count = len(sf.get("hotwords", []))
        size = max(4, min(20, len(videos) * 2 + knowledge_count + hotword_count // 3))

        nodes.append({
            "id": sid,
            "name": name,
            "group": domain,
            "size": size,
            "videos": len(videos),
            "topics": topics[:5],
            "core_knowledge": {k: len(v) for k, v in ck.items()},
            "hotwords": hotword_count,
        })

        # 跨UP主边：共享 topic + 同领域 + 共享 hotwords
        for j, (name2, profile2) in enumerate(db.items()):
            if j <= i:
                continue
            sid2 = f"sp_{j}"
            domain2 = profile2.get("domain", "general")
            topics2 = profile2.get("common_topics", [])
            
            # 权重计算
            weight = 0
            labels = []
            
            # 1. 共享 topic
            shared = set(topics[:10]) & set(topics2[:10])
            if shared:
                weight += len(shared)
                labels.append("📚" + "、".join(list(shared)[:2]))
            
            # 2. 同领域加分
            if domain == domain2:
                weight += 1
            
            # 3. 共享 hotwords（至少 1 个）
            hw1 = set(sf.get("hotwords", []))
            sf2 = profile2.get("skill_feedback", {})
            hw2 = set(sf2.get("hotwords", []))
            shared_hw = hw1 & hw2
            if shared_hw:
                weight += len(shared_hw)
                labels.append("🔥" + "、".join(list(shared_hw)[:2]))
            
            if weight >= 1:
                edges.append({
                    "source": sid,
                    "target": sid2,
                    "weight": min(weight, 10),
                    "label": " · ".join(labels[:2]),
                })

    return nodes, edges


def generate_html(nodes: List[dict], edges: List[dict], output_path: str) -> str:
    """生成 D3.js 力导向图 HTML"""
    nodes_json = json.dumps(nodes, ensure_ascii=False)
    edges_json = json.dumps(edges, ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
<title>biliyoutik2brain · UP主知识图谱</title>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
body {{ font-family: "PingFang SC","Microsoft YaHei",sans-serif; background:#0d1117; color:#c9d1d9; overflow:hidden; }}
#header {{ position:fixed; top:0; left:0; right:0; z-index:10; padding:12px 20px; background:rgba(13,17,23,0.9); backdrop-filter:blur(10px); display:flex; justify-content:space-between; align-items:center; }}
h1 {{ font-size:18px; color:#58a6ff; }}
#stats {{ font-size:12px; color:#8b949e; }}
#tooltip {{ position:fixed; pointer-events:none; opacity:0; background:rgba(22,27,34,0.95); border:1px solid #30363d; border-radius:8px; padding:12px 16px; max-width:280px; z-index:100; font-size:13px; line-height:1.6; }}
#tooltip .name {{ font-size:15px; font-weight:bold; color:#58a6ff; }}
#tooltip .meta {{ color:#8b949e; font-size:11px; margin-top:4px; }}
#tooltip .tag {{ display:inline-block; padding:2px 8px; border-radius:12px; font-size:10px; margin:2px; background:#21262d; }}
#tooltip .tag.trading {{ background:rgba(231,76,60,0.2); color:#e74c3c; }}
#tooltip .tag.tech {{ background:rgba(52,152,219,0.2); color:#3498db; }}
#tooltip .tag.general {{ background:rgba(46,204,113,0.2); color:#2ecc71; }}
#legend {{ position:fixed; bottom:20px; left:20px; z-index:10; font-size:12px; background:rgba(13,17,23,0.85); padding:10px 15px; border-radius:8px; border:1px solid #30363d; }}
.legend-item {{ display:flex; align-items:center; margin:4px 0; }}
.legend-dot {{ width:10px; height:10px; border-radius:50%; margin-right:8px; }}
svg {{ width:100vw; height:100vh; }}
.link {{ stroke:#30363d; stroke-opacity:0.4; }}
.link-label {{ font-size:9px; fill:#484f58; pointer-events:none; }}
.node circle {{ cursor:pointer; stroke:#58a6ff; stroke-width:1.5px; }}
.node text {{ font-size:11px; fill:#c9d1d9; pointer-events:none; text-shadow:0 1px 3px rgba(0,0,0,0.8); }}
</style>
</head>
<body>
<div id="header">
  <h1>🧠 biliyoutik2brain · UP主知识图谱</h1>
  <span id="stats">{len(edges)}条关联 · {time.strftime('%Y-%m-%d')}</span>
</div>
<div id="tooltip"></div>
<div id="legend">
  <div class="legend-item"><span class="legend-dot" style="background:#e74c3c"></span>交易</div>
  <div class="legend-item"><span class="legend-dot" style="background:#3498db"></span>科技</div>
  <div class="legend-item"><span class="legend-dot" style="background:#2ecc71"></span>综合</div>
  <div style="color:#8b949e;margin-top:6px;font-size:10px;">节点大小=视频数+知识量</div>
</div>
<svg id="graph"></svg>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const nodes = {nodes_json};
const edges = {edges_json};

const width = window.innerWidth;
const height = window.innerHeight;

const colorScale = d3.scaleOrdinal()
  .domain(["trading","tech","general"])
  .range(["#e74c3c","#3498db","#2ecc71"]);

const svg = d3.select("#graph")
  .attr("viewBox", [0, 0, width, height]);

const g = svg.append("g");

// Add zoom
svg.call(d3.zoom().scaleExtent([0.3, 3]).on("zoom", (event) => {{
  g.attr("transform", event.transform);
}}));

const simulation = d3.forceSimulation(nodes)
  .force("link", d3.forceLink(edges).id(d => d.id).distance(150))
  .force("charge", d3.forceManyBody().strength(-300))
  .force("center", d3.forceCenter(width/2, height/2))
  .force("collision", d3.forceCollide().radius(d => d.size * 2.5));

const link = g.append("g")
  .selectAll("line")
  .data(edges)
  .join("line")
  .attr("class", "link")
  .attr("stroke-width", d => Math.sqrt(d.weight) * 0.8);

const node = g.append("g")
  .selectAll("g")
  .data(nodes)
  .join("g")
  .attr("class", "node")
  .call(d3.drag()
    .on("start", (event, d) => {{
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x;
      d.fy = d.y;
    }})
    .on("drag", (event, d) => {{
      d.fx = event.x;
      d.fy = event.y;
    }})
    .on("end", (event, d) => {{
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null;
      d.fy = null;
    }})
  );

node.append("circle")
  .attr("r", d => d.size)
  .attr("fill", d => colorScale(d.group))
  .on("mouseover", (event, d) => {{
    const tip = d3.select("#tooltip");
    const ktags = Object.entries(d.core_knowledge || {{}})
      .filter(([_,v]) => v > 0)
      .map(([k,v]) => `<span>${{k}}(${{v}})</span>`).join(" ");
    tip.style("opacity", 1)
      .html(`
        <div class="name">${{d.name}}</div>
        <div class="meta">
          <span class="tag ${{d.group}}">${{d.group}}</span>
          视频${{d.videos}}条 · 热词${{d.hotwords}}个
        </div>
        <div class="meta" style="margin-top:4px">${{ktags || '暂无知识提取'}}</div>
        <div class="meta">${{(d.topics||[]).slice(0,3).join(" · ")}}</div>
      `);
    tip.style("left", (event.pageX+12)+"px")
        .style("top", (event.pageY-40)+"px");
  }})
  .on("mouseout", () => d3.select("#tooltip").style("opacity", 0))
  .on("click", (event, d) => {{
    window.open("https://space.bilibili.com/", "_blank");
  }});

node.append("text")
  .text(d => d.name.length > 6 ? d.name.slice(0,6)+"…" : d.name)
  .attr("dx", d => d.size + 5)
  .attr("dy", 4);

simulation.on("tick", () => {{
  link
    .attr("x1", d => d.source.x)
    .attr("y1", d => d.source.y)
    .attr("x2", d => d.target.x)
    .attr("y2", d => d.target.y);
  node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
}});
</script>
</body>
</html>'''

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    return output_path


def build_knowgraph(output_path: str = None) -> str:
    """主入口：生成知识图谱 HTML"""
    db = load_speakers()
    nodes, edges = build_nodes_edges(db)

    if not output_path:
        os.makedirs(OUTPUT_DIR, exist_ok=True)
        output_path = os.path.join(OUTPUT_DIR, "knowgraph.html")

    path = generate_html(nodes, edges, output_path)
    print(f"[KnowGraph] ✅ 生成完成: {path}")
    print(f"  {len(nodes)}个UP主, {len(edges)}条关联边")
    
    # 按领域统计
    by_domain = Counter(n.get("group", "general") for n in nodes)
    for domain, count in by_domain.most_common():
        print(f"  {domain}: {count}个")

    return path
