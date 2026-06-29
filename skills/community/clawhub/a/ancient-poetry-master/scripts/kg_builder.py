#!/usr/bin/env python3
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
"""
古人诗词知识图谱构建器
基于 poets.json 数据，构建诗人-诗作-朝代-流派-典故多维关系网络，
生成交互式 D3.js 力导向图 HTML 可视化报告。
"""
import json
import os
import sys
from pathlib import Path

SKILL_DIR = Path(__file__).resolve().parent.parent


def load_poets() -> dict:
    """加载诗人数据"""
    poets_path = SKILL_DIR / "references" / "poets.json"
    with open(poets_path, "r", encoding="utf-8") as f:
        return json.load(f)


def build_graph(data: dict) -> dict:
    """构建知识图谱的 nodes 和 links"""
    nodes = []
    links = []
    node_ids = set()

    poets_data = data.get("poets", [])
    themes_data = data.get("themes", [])
    dynasties_data = data.get("dynasties", [])

    # 1. 诗人节点
    for p in poets_data:
        pid = p["id"]
        if pid in node_ids:
            continue
        node_ids.add(pid)
        nodes.append({
            "id": pid,
            "name": p["name"],
            "group": "poet",
            "dynasty": p["dynasty"],
            "school": p.get("school", ""),
            "tags": p.get("tags", [])[:3],
            "masterpieces": p.get("masterpieces", [])[:3],
            "influence": p.get("influence", "")
        })

    # 2. 朝代节点
    for d in data.get("dynasties", []):
        did = f"dynasty_{d['name']}"
        if did in node_ids:
            continue
        node_ids.add(did)
        nodes.append({
            "id": did,
            "name": d["name"],
            "group": "dynasty",
            "period": d.get("period", ""),
            "forms": d.get("forms", []),
            "representatives": d.get("representatives", [])
        })
        # 诗人-朝代 连线
        for rep in d.get("representatives", []):
            for p in poets_data:
                if p["name"] == rep:
                    links.append({"source": p["id"], "target": did, "type": "belongs_to"})

    # 3. 流派节点
    schools_set = set()
    for p in poets_data:
        s = p.get("school", "")
        if s:
            schools_set.add(s)
    for s in sorted(schools_set):
        sid = f"school_{s}"
        if sid in node_ids:
            continue
        node_ids.add(sid)
        members = [p["name"] for p in poets_data if p.get("school") == s]
        nodes.append({
            "id": sid,
            "name": s,
            "group": "school",
            "members": members
        })
        for p in poets_data:
            if p.get("school") == s:
                links.append({"source": p["id"], "target": sid, "type": "member_of"})

    # 4. 主题节点
    for t in themes_data:
        tid = f"theme_{t['name']}"
        if tid in node_ids:
            continue
        node_ids.add(tid)
        nodes.append({
            "id": tid,
            "name": t["name"],
            "group": "theme",
            "poets": t.get("poets", [])
        })
        for pn in t.get("poets", []):
            for p in poets_data:
                if p["name"] == pn:
                    links.append({"source": p["id"], "target": tid, "type": "writes_about"})

    # 5. 诗人关系连线
    for p in poets_data:
        for rel in p.get("relations", []):
            target_name = rel["target"]
            target_id = None
            for tp in poets_data:
                if tp["name"] == target_name:
                    target_id = tp["id"]
                    break
            if target_id:
                links.append({
                    "source": p["id"],
                    "target": target_id,
                    "type": rel["type"],
                    "desc": rel.get("desc", "")
                })

    # 去重 links
    seen = set()
    unique_links = []
    for l in links:
        key = f"{l['source']}-{l['target']}-{l['type']}"
        if key not in seen:
            seen.add(key)
            unique_links.append(l)

    return {"nodes": nodes, "links": unique_links}


def generate_html(graph: dict, output_path: str = None) -> str:
    """生成交互式知识图谱 HTML"""
    nodes_json = json.dumps(graph["nodes"], ensure_ascii=False)
    links_json = json.dumps(graph["links"], ensure_ascii=False)

    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>中国古典诗词知识图谱</title>
<script src="https://d3js.org/d3.v7.min.js"></script>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: "Microsoft YaHei", "PingFang SC", sans-serif; background: #f5f0eb; overflow: hidden; }}
#header {{
  position: absolute; top: 0; left: 0; right: 0; z-index: 10;
  background: linear-gradient(135deg, #8B4513, #A0522D);
  color: white; padding: 12px 24px;
  display: flex; align-items: center; justify-content: space-between;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}}
#header h1 {{ font-size: 22px; font-weight: 400; letter-spacing: 2px; }}
#legend {{ display: flex; gap: 16px; font-size: 13px; }}
.legend-item {{ display: flex; align-items: center; gap: 6px; }}
.legend-dot {{ width: 12px; height: 12px; border-radius: 50%; }}
#tooltip {{
  position: absolute; z-index: 100; pointer-events: none;
  background: rgba(255,255,255,0.96); border-radius: 8px;
  padding: 14px 18px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  max-width: 320px; font-size: 13px; line-height: 1.6;
  display: none; border-left: 3px solid #8B4513;
}}
#tooltip .tt-name {{ font-size: 17px; font-weight: bold; color: #8B4513; margin-bottom: 4px; }}
#tooltip .tt-meta {{ color: #666; font-size: 12px; margin-bottom: 6px; }}
#tooltip .tt-tags {{ display: flex; flex-wrap: wrap; gap: 4px; margin-top: 6px; }}
#tooltip .tt-tag {{ background: #f0e6d3; color: #8B4513; padding: 2px 8px; border-radius: 10px; font-size: 11px; }}
#tooltip .tt-poems {{ margin-top: 6px; color: #555; font-size: 12px; }}
#info-panel {{
  position: absolute; bottom: 20px; left: 20px; z-index: 10;
  background: rgba(255,255,255,0.9); border-radius: 8px;
  padding: 12px 16px; font-size: 12px; color: #666;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
}}
svg {{ width: 100vw; height: 100vh; }}
.links line {{ stroke: #ccc; stroke-opacity: 0.6; stroke-width: 1.2px; }}
.links line.belongs_to {{ stroke: #d4a574; stroke-opacity: 0.7; }}
.links line.member_of {{ stroke: #9b59b6; stroke-opacity: 0.5; stroke-dasharray: 4,3; }}
.links line.influence {{ stroke: #e74c3c; stroke-opacity: 0.4; stroke-dasharray: 5,2; }}
.links line.friend {{ stroke: #2ecc71; stroke-opacity: 0.5; }}
.nodes circle {{ stroke: #fff; stroke-width: 1.5px; cursor: pointer; }}
.nodes text {{ font-size: 12px; font-family: "Microsoft YaHei", "PingFang SC", sans-serif; pointer-events: none; }}
</style>
</head>
<body>
<div id="header">
  <h1>📜 中国古典诗词知识图谱</h1>
  <div id="legend">
    <div class="legend-item"><div class="legend-dot" style="background:#e74c3c"></div>诗人</div>
    <div class="legend-item"><div class="legend-dot" style="background:#3498db"></div>朝代</div>
    <div class="legend-item"><div class="legend-dot" style="background:#9b59b6"></div>流派</div>
    <div class="legend-item"><div class="legend-dot" style="background:#2ecc71"></div>主题</div>
  </div>
</div>
<div id="tooltip"></div>
<div id="info-panel">🖱 拖拽移动 · 滚轮缩放 · 悬停查看详情 · 双击聚焦</div>
<svg id="graph"></svg>

<script>
const graph = {{"nodes": {nodes_json}, "links": {links_json}}};

const W = window.innerWidth, H = window.innerHeight;

const colorMap = {{
  poet: "#e74c3c",
  dynasty: "#3498db",
  school: "#9b59b6",
  theme: "#2ecc71"
}};

const sizeMap = {{
  poet: 9,
  dynasty: 14,
  school: 12,
  theme: 10
}};

const simulation = d3.forceSimulation(graph.nodes)
  .force("link", d3.forceLink(graph.links).id(d => d.id).distance(120))
  .force("charge", d3.forceManyBody().strength(-400))
  .force("center", d3.forceCenter(W/2, H/2))
  .force("collision", d3.forceCollide().radius(20));

const svg = d3.select("#graph")
  .attr("viewBox", [0, 0, W, H])
  .call(d3.zoom()
    .scaleExtent([0.2, 5])
    .on("zoom", (event) => g.attr("transform", event.transform)));

const g = svg.append("g");

const link = g.append("g").attr("class", "links").selectAll("line")
  .data(graph.links).join("line")
  .attr("class", d => d.type || "");

const node = g.append("g").attr("class", "nodes").selectAll("g")
  .data(graph.nodes).join("g")
  .call(d3.drag()
    .on("start", (event, d) => {{
      if (!event.active) simulation.alphaTarget(0.3).restart();
      d.fx = d.x; d.fy = d.y;
    }})
    .on("drag", (event, d) => {{ d.fx = event.x; d.fy = event.y; }})
    .on("end", (event, d) => {{
      if (!event.active) simulation.alphaTarget(0);
      d.fx = null; d.fy = null;
    }}));

node.append("circle")
  .attr("r", d => sizeMap[d.group] || 8)
  .attr("fill", d => colorMap[d.group] || "#999");

node.append("text")
  .text(d => d.name)
  .attr("x", 14).attr("y", 4)
  .attr("fill", "#333");

const tooltip = d3.select("#tooltip");

node.on("mouseover", (event, d) => {{
  let html = `<div class="tt-name">${{d.name}}</div>`;
  if (d.group === "poet") {{
    html += `<div class="tt-meta">${{d.dynasty}} · ${{d.school || '无流派'}}</div>`;
    if (d.tags && d.tags.length) {{
      html += `<div class="tt-tags">${{d.tags.map(t => `<span class="tt-tag">${{t}}</span>`).join('')}}</div>`;
    }}
    if (d.masterpieces && d.masterpieces.length) {{
      html += `<div class="tt-poems">📝 ${{d.masterpieces.join(' / ')}}</div>`;
    }}
    if (d.influence) {{
      html += `<div class="tt-poems" style="color:#8B4513;">💡 ${{d.influence}}</div>`;
    }}
  }} else if (d.group === "dynasty") {{
    html += `<div class="tt-meta">${{d.period}}</div>`;
    html += `<div class="tt-meta">代表诗人: ${{(d.representatives || []).join('、')}}</div>`;
  }} else if (d.group === "school") {{
    html += `<div class="tt-meta">成员: ${{(d.members || []).join('、')}}</div>`;
  }} else if (d.group === "theme") {{
    html += `<div class="tt-meta">代表诗人: ${{(d.poets || []).join('、')}}</div>`;
  }}
  tooltip.style("display", "block").html(html);
}})
.on("mousemove", (event) => {{
  tooltip.style("left", (event.pageX + 16) + "px")
         .style("top", (event.pageY - 10) + "px");
}})
.on("mouseout", () => tooltip.style("display", "none"))
.on("dblclick", (event, d) => {{
  const transform = d3.zoomIdentity.translate(W/2 - d.x * 2, H/2 - d.y * 2).scale(2);
  svg.transition().duration(750).call(d3.zoom().transform, transform);
}});

simulation.on("tick", () => {{
  link.attr("x1", d => d.source.x).attr("y1", d => d.source.y)
      .attr("x2", d => d.target.x).attr("y2", d => d.target.y);
  node.attr("transform", d => `translate(${{d.x}},${{d.y}})`);
}});
</script>
</body>
</html>'''

    if output_path:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"✅ 知识图谱已生成: {output_path}")
    return html


def main():
    """主入口：读取数据 → 构建图谱 → 生成 HTML"""
    output_file = sys.argv[1] if len(sys.argv) > 1 else "poetry_knowledge_graph.html"
    
    print("📚 加载诗人数据...")
    data = load_poets()
    print(f"   共 {len(data['poets'])} 位诗人, {len(data['dynasties'])} 个朝代, {len(data['themes'])} 个主题")

    print("🔗 构建知识图谱...")
    graph = build_graph(data)
    print(f"   节点: {len(graph['nodes'])}, 连线: {len(graph['links'])}")

    print("🎨 生成交互式 HTML...")
    generate_html(graph, output_file)

    # 统计信息
    poet_nodes = [n for n in graph["nodes"] if n["group"] == "poet"]
    rel_types = {}
    for l in graph["links"]:
        rel_types[l["type"]] = rel_types.get(l["type"], 0) + 1
    print(f"\n📊 图谱统计:")
    print(f"   · 诗人节点: {len(poet_nodes)}")
    print(f"   · 朝代节点: {len([n for n in graph['nodes'] if n['group'] == 'dynasty'])}")
    print(f"   · 流派节点: {len([n for n in graph['nodes'] if n['group'] == 'school'])}")
    print(f"   · 主题节点: {len([n for n in graph['nodes'] if n['group'] == 'theme'])}")
    print(f"   · 关系类型: {rel_types}")


if __name__ == "__main__":
    main()
