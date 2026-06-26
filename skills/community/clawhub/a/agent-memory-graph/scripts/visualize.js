#!/usr/bin/env node

/**
 * visualize.js — Generate interactive graph visualization.
 *
 * Reads from SQLite (memory.db) and generates a standalone HTML file
 * with a D3.js force-directed graph.
 *
 * Features:
 *   - Nodes colored by type, sized by connection count
 *   - Edges labeled with relation type on hover
 *   - Click for details panel
 *   - Dark theme, responsive
 *
 * Usage:
 *   node ~/memory/scripts/visualize.js
 *
 * Output: ~/memory/indexes/graph.html
 *
 * Requires Node.js 22+ (node:sqlite built-in). No external dependencies.
 */

const fs = require("fs");
const path = require("path");
const { DatabaseSync } = require("node:sqlite");

const MEMORY_ROOT = process.env.MEMORY_ROOT || path.join(require("os").homedir(), "memory");
const DB_PATH = path.join(MEMORY_ROOT, "indexes", "memory.db");
const OUTPUT_PATH = path.join(MEMORY_ROOT, "indexes", "graph.html");

if (!fs.existsSync(DB_PATH)) {
  console.error("Missing memory.db — run rebuild-indexes.js first");
  process.exit(1);
}

const db = new DatabaseSync(DB_PATH);

// Gather data
const nodes = db.prepare("SELECT path, type, title, status, tags, created, updated FROM nodes").all();
const relations = db.prepare("SELECT source, target, type FROM relations WHERE derived = 0").all();

// Count connections per node
const connCount = {};
for (const r of relations) {
  connCount[r.source] = (connCount[r.source] || 0) + 1;
  connCount[r.target] = (connCount[r.target] || 0) + 1;
}

const graphData = {
  nodes: nodes.map(n => ({
    id: n.path,
    title: n.title,
    type: n.type,
    status: n.status,
    tags: n.tags,
    created: n.created,
    updated: n.updated,
    connections: connCount[n.path] || 0,
  })),
  links: relations.map(r => ({
    source: r.source,
    target: r.target,
    type: r.type,
  })),
};

db.close();

const html = `<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Memory Graph</title>
<style>
  * { margin: 0; padding: 0; box-sizing: border-box; }
  body { background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; overflow: hidden; }
  svg { width: 100vw; height: 100vh; }
  .link { stroke-opacity: 0.4; }
  .link:hover { stroke-opacity: 1; }
  .node { cursor: pointer; }
  .node text { font-size: 11px; fill: #8b949e; pointer-events: none; }
  .node:hover text { fill: #f0f6fc; }
  .tooltip {
    position: fixed; background: #161b22; border: 1px solid #30363d;
    border-radius: 8px; padding: 12px 16px; font-size: 13px;
    max-width: 320px; pointer-events: none; z-index: 100;
    box-shadow: 0 4px 12px rgba(0,0,0,0.5);
  }
  .tooltip h3 { color: #f0f6fc; margin-bottom: 6px; font-size: 14px; }
  .tooltip .field { color: #8b949e; margin: 2px 0; }
  .tooltip .field span { color: #c9d1d9; }
  #details {
    position: fixed; top: 16px; right: 16px; width: 300px;
    background: #161b22; border: 1px solid #30363d; border-radius: 8px;
    padding: 16px; display: none; z-index: 50; max-height: calc(100vh - 32px);
    overflow-y: auto;
  }
  #details h2 { color: #f0f6fc; font-size: 16px; margin-bottom: 8px; }
  #details .field { color: #8b949e; margin: 4px 0; font-size: 13px; }
  #details .field span { color: #c9d1d9; }
  #details .close { position: absolute; top: 8px; right: 12px; cursor: pointer; color: #8b949e; font-size: 18px; }
  #details .close:hover { color: #f0f6fc; }
  #legend {
    position: fixed; bottom: 16px; left: 16px; background: #161b22;
    border: 1px solid #30363d; border-radius: 8px; padding: 12px 16px;
    font-size: 12px; z-index: 50;
  }
  #legend h4 { color: #8b949e; margin-bottom: 6px; }
  #legend .item { display: flex; align-items: center; margin: 3px 0; }
  #legend .dot { width: 10px; height: 10px; border-radius: 50%; margin-right: 8px; }
  #title-bar {
    position: fixed; top: 16px; left: 16px; font-size: 18px; font-weight: 600;
    color: #f0f6fc; z-index: 50;
  }
  #title-bar small { color: #8b949e; font-weight: 400; font-size: 13px; }
</style>
</head>
<body>
<div id="title-bar">Memory Graph <small>${nodes.length} nodes, ${relations.length} edges</small></div>
<div id="details">
  <span class="close" onclick="document.getElementById('details').style.display='none'">&times;</span>
  <h2 id="detail-title"></h2>
  <div id="detail-body"></div>
</div>
<div id="legend"></div>
<div id="edge-tooltip" class="tooltip" style="display:none"></div>
<svg></svg>
<script src="https://d3js.org/d3.v7.min.js"></script>
<script>
const data = ${JSON.stringify(graphData)};

const typeColors = {
  person: '#f97583', project: '#79c0ff', tool: '#56d364',
  concept: '#d2a8ff', place: '#ffa657', default: '#8b949e'
};

// Build legend
const types = [...new Set(data.nodes.map(n => n.type))].sort();
const legend = document.getElementById('legend');
legend.innerHTML = '<h4>Node Types</h4>' + types.map(t =>
  '<div class="item"><div class="dot" style="background:' + (typeColors[t] || typeColors.default) + '"></div>' + t + '</div>'
).join('');

const svg = d3.select('svg');
const width = window.innerWidth;
const height = window.innerHeight;

const simulation = d3.forceSimulation(data.nodes)
  .force('link', d3.forceLink(data.links).id(d => d.id).distance(100))
  .force('charge', d3.forceManyBody().strength(-200))
  .force('center', d3.forceCenter(width / 2, height / 2))
  .force('collision', d3.forceCollide().radius(d => nodeRadius(d) + 5));

function nodeRadius(d) {
  return Math.max(5, Math.min(20, 4 + d.connections * 2));
}

const g = svg.append('g');

// Zoom
svg.call(d3.zoom().scaleExtent([0.2, 5]).on('zoom', (e) => {
  g.attr('transform', e.transform);
}));

const link = g.append('g').selectAll('line')
  .data(data.links).enter().append('line')
  .attr('class', 'link')
  .attr('stroke', '#30363d')
  .attr('stroke-width', 1.5)
  .on('mouseover', function(e, d) {
    d3.select(this).attr('stroke', '#58a6ff').attr('stroke-width', 2.5);
    const tip = document.getElementById('edge-tooltip');
    tip.innerHTML = '<div class="field">' + d.source.title + ' <span>→</span> ' + d.target.title + '</div><div class="field">Type: <span>' + d.type + '</span></div>';
    tip.style.display = 'block';
    tip.style.left = e.clientX + 12 + 'px';
    tip.style.top = e.clientY + 12 + 'px';
  })
  .on('mouseout', function() {
    d3.select(this).attr('stroke', '#30363d').attr('stroke-width', 1.5);
    document.getElementById('edge-tooltip').style.display = 'none';
  });

const node = g.append('g').selectAll('g')
  .data(data.nodes).enter().append('g')
  .attr('class', 'node')
  .call(d3.drag()
    .on('start', (e, d) => { if (!e.active) simulation.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
    .on('drag', (e, d) => { d.fx = e.x; d.fy = e.y; })
    .on('end', (e, d) => { if (!e.active) simulation.alphaTarget(0); d.fx = null; d.fy = null; })
  );

node.append('circle')
  .attr('r', d => nodeRadius(d))
  .attr('fill', d => typeColors[d.type] || typeColors.default)
  .attr('stroke', '#0d1117')
  .attr('stroke-width', 2);

node.append('text')
  .attr('dx', d => nodeRadius(d) + 4)
  .attr('dy', 4)
  .text(d => d.title);

// Neighborhood highlight on hover
node.on('mouseover', (e, d) => {
  const connected = new Set();
  data.links.forEach(l => {
    const sid = l.source.id || l.source;
    const tid = l.target.id || l.target;
    if (sid === d.id) connected.add(tid);
    if (tid === d.id) connected.add(sid);
  });
  node.attr('opacity', n => n.id === d.id || connected.has(n.id) ? 1 : 0.12);
  link.attr('stroke', l => {
    const sid = l.source.id || l.source;
    const tid = l.target.id || l.target;
    return (sid === d.id || tid === d.id) ? (typeColors[d.type] || '#58a6ff') : '#30363d';
  })
  .attr('stroke-opacity', l => {
    const sid = l.source.id || l.source;
    const tid = l.target.id || l.target;
    return (sid === d.id || tid === d.id) ? 0.9 : 0.08;
  })
  .attr('stroke-width', l => {
    const sid = l.source.id || l.source;
    const tid = l.target.id || l.target;
    return (sid === d.id || tid === d.id) ? 2.5 : 1.5;
  });
}).on('mouseout', () => {
  node.attr('opacity', 1);
  link.attr('stroke', '#30363d').attr('stroke-opacity', 0.4).attr('stroke-width', 1.5);
});

node.on('click', (e, d) => {
  const det = document.getElementById('details');
  document.getElementById('detail-title').textContent = d.title;
  let body = '';
  body += '<div class="field">Path: <span>' + d.id + '</span></div>';
  body += '<div class="field">Type: <span>' + d.type + '</span></div>';
  body += '<div class="field">Status: <span>' + (d.status || '—') + '</span></div>';
  body += '<div class="field">Created: <span>' + (d.created || '—') + '</span></div>';
  body += '<div class="field">Updated: <span>' + (d.updated || '—') + '</span></div>';
  body += '<div class="field">Tags: <span>' + (d.tags || '—') + '</span></div>';
  body += '<div class="field">Connections: <span>' + d.connections + '</span></div>';
  // Show relations
  const outgoing = data.links.filter(l => (l.source.id || l.source) === d.id);
  const incoming = data.links.filter(l => (l.target.id || l.target) === d.id);
  if (outgoing.length > 0) {
    body += '<br><div class="field"><strong>Outgoing:</strong></div>';
    outgoing.forEach(l => { body += '<div class="field">&nbsp;&nbsp;→ <span>' + (l.target.title || l.target) + ' [' + l.type + ']</span></div>'; });
  }
  if (incoming.length > 0) {
    body += '<br><div class="field"><strong>Incoming:</strong></div>';
    incoming.forEach(l => { body += '<div class="field">&nbsp;&nbsp;← <span>' + (l.source.title || l.source) + ' [' + l.type + ']</span></div>'; });
  }
  document.getElementById('detail-body').innerHTML = body;
  det.style.display = 'block';
});

simulation.on('tick', () => {
  link.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
    .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
  node.attr('transform', d => 'translate(' + d.x + ',' + d.y + ')');
});
</script>
</body>
</html>`;

fs.writeFileSync(OUTPUT_PATH, html);
console.log(`✓ Graph visualization written to ${OUTPUT_PATH}`);
console.log(`  ${nodes.length} nodes, ${relations.length} edges`);
console.log(`  Open in browser: file://${OUTPUT_PATH}`);
