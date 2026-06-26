#!/usr/bin/env node
/**
 * ELK JSON → SVG renderer
 *
 * Usage:
 *   node render-elk.mjs <input.json> <output.svg>
 *   node render-elk.mjs --dir <folder>          # renders all .json → svg/
 *   node render-elk.mjs --dir <folder> --png     # also converts to PNG via sips
 *
 * Input: ELK JSON graph with optional `color`, `label`, `containerColor`,
 *        `edgeColor`, `dashed`, `subtitle`, `title` fields.
 *
 * Requires: elkjs (npm install elkjs)
 * Optional: sips (macOS) for PNG conversion
 */

import { createRequire } from 'module';
const require = createRequire(process.cwd() + '/');
const ELK = require('elkjs');
import { readFileSync, writeFileSync, readdirSync, mkdirSync, existsSync } from 'fs';
import { join, basename } from 'path';
import { execSync } from 'child_process';

const elk = new ELK();

// ── Color palette ──────────────────────────────────────────────
// 8 semantic colors with clear, distinct meanings.
// Every node should map to one of these categories.
const COLORS = {
  action:    { fill: '#3B82F6', stroke: '#1E40AF', text: '#FFFFFF' },  // Blue — system actions (API calls, DB writes, processing)
  external:  { fill: '#14B8A6', stroke: '#0D9488', text: '#FFFFFF' },  // Teal — external services (Google, Twilio, Stripe)
  decision:  { fill: '#EC4899', stroke: '#BE185D', text: '#FFFFFF' },  // Pink — decision/branch points (yes/no, if/else)
  user:      { fill: '#F97316', stroke: '#EA580C', text: '#FFFFFF' },  // Orange — user actions (clicks, reviews, inputs)
  success:   { fill: '#10B981', stroke: '#047857', text: '#FFFFFF' },  // Green — positive outcomes (done, confirmed, created)
  negative:  { fill: '#EF4444', stroke: '#B91C1C', text: '#FFFFFF' },  // Red — negative outcomes (canceled, error, not built)
  neutral:   { fill: '#6B7280', stroke: '#374151', text: '#FFFFFF' },  // Gray — neutral/info (labels, starting points, inactive)
  data:      { fill: '#F59E0B', stroke: '#D97706', text: '#1F2937' },  // Amber — data/artifacts (records, drafts, outputs)
  // Container default
  container: { fill: '#F3F4F6', stroke: '#D1D5DB', text: '#374151' },
  // Legacy aliases (backward compat)
  core: null, provider: null, tool: null, output: null, context: null,
  state: null, highlight: null, model: null, graph: null, step: null,
};
// Wire up legacy aliases
COLORS.core = COLORS.action;
COLORS.provider = COLORS.external;
COLORS.tool = COLORS.success;
COLORS.output = COLORS.data;
COLORS.context = COLORS.decision;
COLORS.state = COLORS.user;
COLORS.highlight = COLORS.negative;
COLORS.model = COLORS.action;
COLORS.graph = COLORS.action;
COLORS.step = { fill: '#DBEAFE', stroke: '#93C5FD', text: '#1E3A5F' };

// Legend labels for semantic colors
const LEGEND_ENTRIES = {
  action:   { label: 'System action' },
  external: { label: 'External service' },
  decision: { label: 'Decision point' },
  user:     { label: 'User action' },
  success:  { label: 'Positive outcome' },
  negative: { label: 'Negative outcome' },
  neutral:  { label: 'Neutral / info' },
  data:     { label: 'Data / artifact' },
};

function escapeXml(s) {
  return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}

function wrapText(text, maxWidth, fontSize = 13) {
  const charWidth = fontSize * 0.58;
  const maxChars = Math.floor(maxWidth / charWidth);
  if (text.length <= maxChars) return [text];
  const words = text.split(' ');
  const lines = [];
  let current = '';
  for (const word of words) {
    if (current && (current + ' ' + word).length > maxChars) {
      lines.push(current);
      current = word;
    } else {
      current = current ? current + ' ' + word : word;
    }
  }
  if (current) lines.push(current);
  return lines;
}

function renderNode(node) {
  const x = node.x || 0;
  const y = node.y || 0;
  const w = node.width || 120;
  const h = node.height || 40;
  const color = COLORS[node.color] || COLORS.neutral;
  const isContainer = node.children && node.children.length > 0;
  const containerColor = COLORS[node.containerColor] || COLORS.container;

  let svg = '';

  if (isContainer) {
    svg += `  <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="8" ry="8" fill="${containerColor.fill}" stroke="${containerColor.stroke}" stroke-width="2" stroke-dasharray="6,3"/>\n`;
    const label = node.label || node.id;
    svg += `  <text x="${x + 10}" y="${y + 20}" font-family="Inter, -apple-system, sans-serif" font-size="12" font-weight="700" fill="${containerColor.text}" letter-spacing="0.05em">${escapeXml(label)}</text>\n`;
    for (const child of node.children) {
      svg += renderNode(child);
    }
  } else {
    const rx = 6;
    svg += `  <rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" ry="${rx}" fill="${color.fill}" stroke="${color.stroke}" stroke-width="1.5"/>\n`;

    const label = node.label || node.id;
    const fontSize = node.fontSize || 13;
    const lines = wrapText(label, w - 16, fontSize);
    const lineHeight = fontSize + 3;
    const totalTextHeight = lines.length * lineHeight;
    const startY = y + (h - totalTextHeight) / 2 + fontSize;

    for (let i = 0; i < lines.length; i++) {
      svg += `  <text x="${x + w / 2}" y="${startY + i * lineHeight}" text-anchor="middle" font-family="Inter, -apple-system, sans-serif" font-size="${fontSize}" font-weight="600" fill="${color.text}">${escapeXml(lines[i])}</text>\n`;
    }

    if (node.subtitle) {
      const subLines = wrapText(node.subtitle, w - 12, 10);
      for (let i = 0; i < subLines.length; i++) {
        svg += `  <text x="${x + w / 2}" y="${startY + lines.length * lineHeight + i * 13}" text-anchor="middle" font-family="Inter, -apple-system, sans-serif" font-size="10" fill="${color.text}" opacity="0.8">${escapeXml(subLines[i])}</text>\n`;
      }
    }
  }

  return svg;
}

function renderEdge(edge) {
  const sections = edge.sections || [];
  if (sections.length === 0) return '';

  let svg = '';
  const edgeColor = edge.edgeColor || '#64748B';
  const strokeWidth = edge.strokeWidth || 1.5;
  const isDashed = edge.dashed;

  for (const section of sections) {
    const start = section.startPoint;
    const end = section.endPoint;
    const bends = section.bendPoints || [];

    let d = `M ${start.x} ${start.y}`;
    for (const bend of bends) d += ` L ${bend.x} ${bend.y}`;
    d += ` L ${end.x} ${end.y}`;

    svg += `  <path d="${d}" fill="none" stroke="${edgeColor}" stroke-width="${strokeWidth}" marker-end="url(#arrowhead-${edgeColor.replace('#', '')})"${isDashed ? ' stroke-dasharray="5,3"' : ''}/>\n`;
  }

  if (edge.labels && edge.labels.length > 0) {
    for (const label of edge.labels) {
      if (label.text && label.x !== undefined) {
        svg += `  <rect x="${label.x - 2}" y="${label.y - 1}" width="${label.width + 4}" height="${label.height + 2}" rx="3" fill="white" opacity="0.9"/>\n`;
        svg += `  <text x="${label.x + (label.width || 0) / 2}" y="${label.y + 12}" text-anchor="middle" font-family="Inter, -apple-system, sans-serif" font-size="10" fill="#475569">${escapeXml(label.text)}</text>\n`;
      }
    }
  }

  return svg;
}

function collectEdgeColors(graph) {
  const colors = new Set();
  if (graph.edges) for (const e of graph.edges) colors.add(e.edgeColor || '#64748B');
  if (graph.children) for (const c of graph.children) for (const cl of collectEdgeColors(c)) colors.add(cl);
  return colors;
}

function collectEdgesRecursive(graph) {
  let edges = graph.edges ? [...graph.edges] : [];
  if (graph.children) for (const c of graph.children) edges = edges.concat(collectEdgesRecursive(c));
  return edges;
}

export async function renderElk(elkGraph) {
  const layouted = await elk.layout(elkGraph);

  const totalW = (layouted.width || 800) + 40;
  const legendPadding = elkGraph.legend !== false ? 60 : 0;
  const totalH = (layouted.height || 600) + 40 + legendPadding;
  const edgeColors = collectEdgeColors(layouted);

  let svg = `<?xml version="1.0" encoding="UTF-8"?>\n`;
  svg += `<svg xmlns="http://www.w3.org/2000/svg" width="${totalW}" height="${totalH}" viewBox="-20 -20 ${totalW} ${totalH}">\n`;
  svg += `<defs>\n`;
  for (const color of edgeColors) {
    const id = color.replace('#', '');
    svg += `  <marker id="arrowhead-${id}" markerWidth="8" markerHeight="6" refX="8" refY="3" orient="auto">\n`;
    svg += `    <polygon points="0 0, 8 3, 0 6" fill="${color}"/>\n`;
    svg += `  </marker>\n`;
  }
  svg += `</defs>\n`;
  svg += `<rect x="-20" y="-20" width="${totalW}" height="${totalH}" fill="#FFFFFF" rx="12"/>\n`;

  if (elkGraph.title) {
    svg += `<text x="${(totalW - 40) / 2}" y="5" text-anchor="middle" font-family="Inter, -apple-system, sans-serif" font-size="18" font-weight="700" fill="#1E293B">${escapeXml(elkGraph.title)}</text>\n`;
  }

  if (layouted.children) for (const node of layouted.children) svg += renderNode(node);

  const allEdges = collectEdgesRecursive(layouted);
  for (const edge of allEdges) svg += renderEdge(edge);

  // Render legend if requested
  if (elkGraph.legend !== false) {
    const usedColors = new Set();
    function collectColors(node) {
      if (node.color && LEGEND_ENTRIES[node.color]) usedColors.add(node.color);
      if (node.children) for (const c of node.children) collectColors(c);
    }
    if (layouted.children) for (const c of layouted.children) collectColors(c);

    if (usedColors.size > 0) {
      const entries = [...usedColors].filter(k => LEGEND_ENTRIES[k]).map(k => ({ key: k, ...LEGEND_ENTRIES[k] }));
      const legendX = 10;
      const legendY = (layouted.height || 600) + 15;
      const swatchSize = 12;
      const lineHeight = 18;
      const colWidth = 180;
      const cols = Math.min(entries.length, 4);

      svg += `  <text x="${legendX}" y="${legendY}" font-family="Inter, -apple-system, sans-serif" font-size="11" font-weight="700" fill="#64748B">LEGEND</text>\n`;
      for (let i = 0; i < entries.length; i++) {
        const col = i % cols;
        const row = Math.floor(i / cols);
        const x = legendX + col * colWidth;
        const y = legendY + 8 + row * lineHeight;
        const e = entries[i];
        const c = COLORS[e.key] || COLORS.neutral;
        svg += `  <rect x="${x}" y="${y}" width="${swatchSize}" height="${swatchSize}" rx="2" fill="${c.fill}" stroke="${c.stroke}" stroke-width="1"/>\n`;
        svg += `  <text x="${x + swatchSize + 5}" y="${y + swatchSize - 1}" font-family="Inter, -apple-system, sans-serif" font-size="10" fill="#475569">${escapeXml(e.label)}</text>\n`;
      }
    }
  }

  svg += `</svg>\n`;
  return svg;
}

// ── CLI ────────────────────────────────────────────────────────
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`Usage:
  render-elk.mjs <input.json> <output.svg>        Render single file
  render-elk.mjs --dir <folder>                    Render all .json in folder → svg/
  render-elk.mjs --dir <folder> --png              Also convert SVGs to PNG (macOS sips)

Colors: ${Object.keys(COLORS).join(', ')}
Node fields: id, width, height, label, color, subtitle, fontSize, children, containerColor
Edge fields: id, sources, targets, labels, edgeColor, dashed, strokeWidth`);
  process.exit(0);
}

const dirIdx = args.indexOf('--dir');
const doPng = args.includes('--png');

if (dirIdx >= 0) {
  // Batch mode
  const dir = args[dirIdx + 1];
  if (!dir) { console.error('--dir requires a folder path'); process.exit(1); }
  const outDir = join(dir, 'svg');
  mkdirSync(outDir, { recursive: true });

  const files = readdirSync(dir).filter(f => f.endsWith('.json') && !f.startsWith('package'));
  console.log(`Rendering ${files.length} diagram(s) from ${dir}\n`);

  for (const file of files.sort()) {
    const graph = JSON.parse(readFileSync(join(dir, file), 'utf8'));
    const svgName = file.replace('.json', '.svg');
    const svg = await renderElk(graph);
    writeFileSync(join(outDir, svgName), svg);

    if (doPng) {
      try {
        const pngName = file.replace('.json', '.png');
        execSync(`sips -s format png "${join(outDir, svgName)}" --out "${join(outDir, pngName)}" 2>/dev/null`);
        console.log(`  ✅ ${file} → svg/${svgName} + svg/${pngName}`);
      } catch {
        console.log(`  ✅ ${file} → svg/${svgName} (PNG conversion failed — sips not available?)`);
      }
    } else {
      console.log(`  ✅ ${file} → svg/${svgName}`);
    }
  }
  console.log(`\nDone! Output in ${outDir}/`);
} else if (args.length >= 2) {
  // Single file mode
  const [input, output] = args;
  const graph = JSON.parse(readFileSync(input, 'utf8'));
  const svg = await renderElk(graph);
  writeFileSync(output, svg);
  console.log(`Written: ${output}`);
} else {
  console.error('Usage: render-elk.mjs <input.json> <output.svg> | --dir <folder> [--png]');
  process.exit(1);
}
