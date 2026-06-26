/**
 * 图形生成器模块
 * 生成知识图谱的各种可视化格式
 */

const { createLogger } = require('../../src/utils/logger.cjs');
const logger = createLogger('graph_generators');
const fs = require('fs');
const path = require('path');
const { getPool } = require('./db.cjs');

const OUTPUT_DIR = path.join(__dirname, '..', '..', 'output');

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

/**
 * 生成 DOT 格式（Graphviz）
 */
async function generateDotGraph() {
  const pool = getPool();

  try {
    const concepts = await pool.query(`
      SELECT id, name, access_count, importance
      FROM concepts
      ORDER BY access_count DESC, importance DESC
      LIMIT 100
    `);

    const associations = await pool.query(`
      SELECT a.from_id, a.to_id, a.weight, a.type, c1.name as from_name, c2.name as to_name
      FROM associations a
      JOIN concepts c1 ON a.from_id = c1.id
      JOIN concepts c2 ON a.to_id = c2.id
      LIMIT 200
    `);

    let dot = 'digraph BrainNetwork {\n';
    dot += '  rankdir=LR;\n';
    dot += '  node [shape=box, style=rounded, fontname="Arial"];\n';
    dot += '  edge [fontname="Arial", fontsize=10];\n\n';

    const nodeMap = new Map();
    for (const c of concepts.rows) {
      const size = Math.max(0.5, Math.min(2.0, (c.access_count || 0) * 0.1 + 0.5));
      const color = c.importance > 0.7 ? '#ff9999' :
                    c.importance > 0.4 ? '#99ccff' : '#99ff99';

      const safeName = c.name.replace(/"/g, '\\"');
      dot += `  "${c.id}" [label="${safeName}", width=${size.toFixed(1)}, fillcolor="${color}", style="filled,rounded"];\n`;
      nodeMap.set(c.id, c);
    }

    dot += '\n';

    for (const a of associations.rows) {
      if (nodeMap.has(a.from_id) && nodeMap.has(a.to_id)) {
        const penwidth = Math.max(0.5, a.weight * 2);
        const label = a.type !== 'related' ? a.type : '';
        dot += `  "${a.from_id}" -> "${a.to_id}" [weight=${a.weight.toFixed(2)}, penwidth=${penwidth.toFixed(1)}, label="${label}"];\n`;
      }
    }

    dot += '}\n';

    const dotPath = path.join(OUTPUT_DIR, 'brain-network.dot');
    fs.writeFileSync(dotPath, dot);

    return { dot, concepts: concepts.rows.length, edges: associations.rows.length, path: dotPath };
  } catch (e) {
    console.error('[graph] DOT 生成失败:', e.message);
    throw e;
  }
}

/**
 * 生成 Mermaid 格式
 */
async function generateMermaidGraph() {
  const pool = getPool();

  try {
    const concepts = await pool.query(`
      SELECT id, name, access_count, importance
      FROM concepts
      ORDER BY importance DESC, access_count DESC
      LIMIT 30
    `);

    const conceptIds = concepts.rows.map(c => c.id);

    const associations = await pool.query(`
      SELECT a.from_id, a.to_id, a.weight, c1.name as from_name, c2.name as to_name
      FROM associations a
      JOIN concepts c1 ON a.from_id = c1.id
      JOIN concepts c2 ON a.to_id = c2.id
      WHERE a.from_id = ANY($1) AND a.to_id = ANY($1)
      ORDER BY a.weight DESC
      LIMIT 50
    `, [conceptIds]);

    let mermaid = '```mermaid\ngraph TD\n\n';

    for (const c of concepts.rows) {
      const safeName = c.name.replace(/["\[\]]/g, '_');
      mermaid += `  ${c.id}["${safeName}"]\n`;
    }

    mermaid += '\n';

    for (const a of associations.rows) {
      const safeFrom = a.from_name.replace(/["\[\]]/g, '_');
      const safeTo = a.to_name.replace(/["\[\]]/g, '_');
      mermaid += `  ${a.from_id} -->|${a.weight.toFixed(1)}| ${a.to_id}\n`;
    }

    mermaid += '```\n';

    const mermaidPath = path.join(OUTPUT_DIR, 'brain-network.mmd');
    fs.writeFileSync(mermaidPath, mermaid);

    return { mermaid, concepts: concepts.rows.length, edges: associations.rows.length, path: mermaidPath };
  } catch (e) {
    console.error('[graph] Mermaid 生成失败:', e.message);
    throw e;
  }
}

/**
 * 生成文本格式
 */
async function generateTextGraph() {
  const pool = getPool();

  try {
    const concepts = await pool.query(`
      SELECT name, access_count, importance
      FROM concepts
      ORDER BY importance DESC
      LIMIT 50
    `);

    const associations = await pool.query(`
      SELECT c1.name as from_name, c2.name as to_name, a.weight
      FROM associations a
      JOIN concepts c1 ON a.from_id = c1.id
      JOIN concepts c2 ON a.to_id = c2.id
      ORDER BY a.weight DESC
      LIMIT 100
    `);

    let text = '知识网络文本视图\n';
    text += '='.repeat(50) + '\n\n';

    text += '【核心概念】\n';
    concepts.rows.slice(0, 20).forEach((c, i) => {
      const importance = '★'.repeat(Math.ceil(c.importance * 5));
      text += `${i + 1}. ${c.name} ${importance}\n`;
    });

    text += '\n【重要关联】\n';
    associations.rows.slice(0, 20).forEach((a, i) => {
      text += `${i + 1}. ${a.from_name} → ${a.to_name} (${a.weight.toFixed(2)})\n`;
    });

    const textPath = path.join(OUTPUT_DIR, 'brain-network.txt');
    fs.writeFileSync(textPath, text);

    return { text, path: textPath };
  } catch (e) {
    console.error('[graph] 文本生成失败:', e.message);
    throw e;
  }
}

/**
 * 生成 HTML 交互式图谱
 */
async function generateHtmlGraph() {
  const pool = getPool();

  try {
    const concepts = await pool.query(`
      SELECT id, name, access_count, importance
      FROM concepts
      ORDER BY importance DESC, access_count DESC
      LIMIT 50
    `);

    const conceptIds = concepts.rows.map(c => c.id);

    const associations = await pool.query(`
      SELECT a.from_id, a.to_id, a.weight, c1.name as from_name, c2.name as to_name
      FROM associations a
      JOIN concepts c1 ON a.from_id = c1.id
      JOIN concepts c2 ON a.to_id = c2.id
      WHERE a.from_id = ANY($1) AND a.to_id = ANY($1)
      ORDER BY a.weight DESC
      LIMIT 100
    `, [conceptIds]);

    const nodes = concepts.rows.map(c => ({
      id: c.id,
      name: c.name,
      size: Math.max(10, (c.access_count || 0) * 2 + 10),
      importance: c.importance
    }));

    const links = associations.rows.map(a => ({
      source: a.from_id,
      target: a.to_id,
      weight: a.weight
    }));

    const html = `<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <title>知识图谱可视化</title>
  <script src="https://d3js.org/d3.v7.min.js"></script>
  <style>
    body { margin: 0; font-family: Arial, sans-serif; }
    #graph { width: 100vw; height: 100vh; }
    .node { cursor: pointer; }
    .link { stroke: #999; stroke-opacity: 0.6; }
  </style>
</head>
<body>
  <div id="graph"></div>
  <script>
    const nodes = ${JSON.stringify(nodes)};
    const links = ${JSON.stringify(links)};
    
    const width = window.innerWidth;
    const height = window.innerHeight;
    
    const svg = d3.select("#graph").append("svg")
      .attr("width", width)
      .attr("height", height);
    
    const simulation = d3.forceSimulation(nodes)
      .force("link", d3.forceLink(links).id(d => d.id))
      .force("charge", d3.forceManyBody().strength(-300))
      .force("center", d3.forceCenter(width / 2, height / 2));
    
    const link = svg.append("g")
      .selectAll("line")
      .data(links)
      .join("line")
      .attr("class", "link")
      .attr("stroke-width", d => Math.sqrt(d.weight * 5));
    
    const node = svg.append("g")
      .selectAll("circle")
      .data(nodes)
      .join("circle")
      .attr("class", "node")
      .attr("r", d => d.size)
      .attr("fill", d => d.importance > 0.7 ? "#ff6b6b" : d.importance > 0.4 ? "#4ecdc4" : "#95e1d3");
    
    node.append("title").text(d => d.name);
    
    simulation.on("tick", () => {
      link
        .attr("x1", d => d.source.x)
        .attr("y1", d => d.source.y)
        .attr("x2", d => d.target.x)
        .attr("y2", d => d.target.y);
      
      node
        .attr("cx", d => d.x)
        .attr("cy", d => d.y);
    });
  </script>
</body>
</html>`;

    const htmlPath = path.join(OUTPUT_DIR, 'brain-network.html');
    fs.writeFileSync(htmlPath, html);

    return { html, concepts: nodes.length, edges: links.length, path: htmlPath };
  } catch (e) {
    console.error('[graph] HTML 生成失败:', e.message);
    throw e;
  }
}

module.exports = {
  generateDotGraph,
  generateMermaidGraph,
  generateTextGraph,
  generateHtmlGraph
};
