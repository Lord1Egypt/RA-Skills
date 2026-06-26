---
title: "OC Brain Map — BrainMapProjects Component"
created: 2026-03-17
modified: 2026-04-17
tags: [brain-map, react, d3, component, tsx]
status: active
---

# BrainMapProjects.tsx

Project-centric Brain Map component. Left panel shows attention projects ranked by recency-weighted density. Right panel renders a D3 force-directed graph for the selected project.

**Dependencies:** `d3`, `@types/d3`

```bash
npm install d3 @types/d3
```

---

## Recency-Weighted Ranking

The left panel sorts projects by a recency-weighted score rather than raw co-access density. This surfaces recently-active projects over historically-dense-but-stale ones.

**Equation:**

```
rank_score = coAccessScore / (daysSinceLastSession + 1)
```

- `coAccessScore` — total edge weight across all sessions (aggregate attention density)
- `daysSinceLastSession` — days since `dateLast` (ISO date from parser output)
- `+1` — prevents division by zero for projects touched today

A project touched yesterday with moderate density outranks a project with high lifetime density last touched 60 days ago. The `+1` floor keeps today's sessions from producing infinite scores.

**Implementation:**

```tsx
const rankedProjects = data?.projects
  ? [...data.projects].sort((a, b) => {
      const now = Date.now();
      const daysA = (now - new Date(a.dateLast).getTime()) / 86_400_000;
      const daysB = (now - new Date(b.dateLast).getTime()) / 86_400_000;
      const scoreA = a.coAccessScore / (daysA + 1);
      const scoreB = b.coAccessScore / (daysB + 1);
      return scoreB - scoreA;
    })
  : [];
```

Then render `rankedProjects.map(proj => ...)` instead of `data.projects.map`.

---

## Project Interface

```tsx
interface Project {
  id: string;           // machine id, e.g. "ghost-publishing"
  label: string;        // display name
  color: string;        // hex color for this project
  sessionCount: number; // journal sessions attributed to this project
  fileCount: number;    // unique files accessed
  coAccessScore: number;// total edge weight — aggregate attention proxy
  dateFirst: string;    // YYYY-MM-DD of earliest session
  dateLast: string;     // YYYY-MM-DD of most recent session
  sessions: ProjectSession[];
  nodes: ProjectNode[];
  edges: ProjectEdge[];
}

interface ProjectData {
  projects: Project[];
  generated: string;    // ISO timestamp of last parser run
  journalCount: number; // number of journal files parsed
}
```

---

## Node Color Groups

```tsx
const NODE_COLORS: Record<string, string> = {
  core: '#c8a84b',
  memory: '#a78bfa',
  publishing: '#22c55e',
  infrastructure: '#60a5fa',
  skills: '#f97316',
  journal: '#6b7280',
  general: '#6b7280',
};
```

---

## Component

```tsx
'use client';

import { useEffect, useRef, useState } from 'react';
import * as d3 from 'd3';

// --- Types ---
interface Node extends d3.SimulationNodeDatum {
  id: string;
  group: string;
  accessCount: number;
  path: string;
}

interface Edge {
  source: string | Node;
  target: string | Node;
  weight: number;
  sessionType: string;
  sessions: string[];
}

interface GraphData {
  nodes: Node[];
  edges: Edge[];
  generated: string;
  sessionCount: number;
}

// --- Color maps ---
const GROUP_COLORS: Record<string, string> = {
  core:           '#c8a84b',   // Gold
  memory:         '#a78bfa',   // Purple
  publishing:     '#22c55e',   // Green
  infrastructure: '#60a5fa',   // Blue
  skills:         '#f97316',   // Orange
  journal:        '#94a3b8',   // Slate
  general:        '#6b7280',   // Gray
};

const SESSION_TYPE_COLORS: Record<string, string> = {
  strategy:       '#c8a84b',
  memory:         '#a78bfa',
  publishing:     '#22c55e',
  infrastructure: '#60a5fa',
  research:       '#f97316',
  general:        '#6b7280',
};

// --- Upstream tier (for dot direction) ---
const GROUP_TIER: Record<string, number> = {
  core: 5, memory: 4, publishing: 2, infrastructure: 2, skills: 1, journal: 0, general: 0
};

export default function BrainMapGraph() {
  const svgRef = useRef<SVGSVGElement>(null);
  const [graphData, setGraphData] = useState<GraphData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [tooltip, setTooltip] = useState<{ x: number; y: number; title: string; rows: { label: string; value: string }[]; hint?: string } | null>(null);
  const [focusNode, setFocusNode] = useState<string | null>(null);
  const lastClickRef = useRef<string | null>(null);
  const simRef = useRef<d3.Simulation<Node, Edge> | null>(null);

  // Fetch graph data
  useEffect(() => {
    fetch('/api/brain-map/graph')
      .then(r => r.json())
      .then(data => { setGraphData(data); setLoading(false); })
      .catch(err => { setError(String(err)); setLoading(false); });
  }, []);

  // Render graph
  useEffect(() => {
    if (!graphData || !svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const width = svgRef.current.clientWidth || 900;
    const height = svgRef.current.clientHeight || 600;

    // Defs: glow filter
    const defs = svg.append('defs');
    const filter = defs.append('filter').attr('id', 'glow');
    filter.append('feGaussianBlur').attr('stdDeviation', 2.5).attr('result', 'coloredBlur');
    const feMerge = filter.append('feMerge');
    feMerge.append('feMergeNode').attr('in', 'coloredBlur');
    feMerge.append('feMergeNode').attr('in', 'SourceGraphic');

    // Zoom layer
    const g = svg.append('g');
    svg.call(
      d3.zoom<SVGSVGElement, unknown>()
        .scaleExtent([0.3, 4])
        .on('zoom', (event) => g.attr('transform', event.transform))
    );

    const nodes: Node[] = graphData.nodes.map(n => ({ ...n }));
    const edges: Edge[] = graphData.edges.map(e => ({ ...e }));

    // Simulation
    const sim = d3.forceSimulation<Node>(nodes)
      .force('link', d3.forceLink<Node, Edge>(edges)
        .id(d => d.id)
        .distance(d => Math.max(60, 120 - (d as any).weight * 6))
        .strength(d => Math.min(0.8, 0.2 + (d as any).weight * 0.05))
      )
      .force('charge', d3.forceManyBody().strength(-220))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide(20));

    simRef.current = sim;

    // Edges
    const link = g.append('g')
      .selectAll<SVGLineElement, Edge>('line')
      .data(edges)
      .join('line')
      .attr('stroke', d => SESSION_TYPE_COLORS[d.sessionType] || '#6b7280')
      .attr('stroke-opacity', 0.35)
      .attr('stroke-width', d => Math.max(1, Math.min(4, (d as any).weight * 0.7)));

    // Flow dots (one per edge)
    const dotData = edges.map((e, i) => ({ edge: e, phase: i * 0.413, speed: 0.00025 + (e as any).weight * 0.00006 }));
    const dots = g.append('g')
      .selectAll<SVGCircleElement, typeof dotData[0]>('circle.flow-dot')
      .data(dotData)
      .join('circle')
      .attr('class', 'flow-dot')
      .attr('r', 3)
      .attr('fill', d => SESSION_TYPE_COLORS[d.edge.sessionType] || '#6b7280')
      .attr('opacity', 0.55)
      .attr('filter', 'url(#glow)');

    // Nodes
    const node = g.append('g')
      .selectAll<SVGCircleElement, Node>('circle.node')
      .data(nodes)
      .join('circle')
      .attr('class', 'node')
      .attr('r', d => Math.max(6, Math.min(18, 6 + d.accessCount * 1.8)))
      .attr('fill', d => GROUP_COLORS[d.group] || '#6b7280')
      .attr('stroke', '#1a1a1a')
      .attr('stroke-width', 1.5)
      .attr('cursor', 'pointer')
      .call(
        d3.drag<SVGCircleElement, Node>()
          .on('start', (event, d) => { if (!event.active) sim.alphaTarget(0.3).restart(); d.fx = d.x; d.fy = d.y; })
          .on('drag', (event, d) => { d.fx = event.x; d.fy = event.y; })
          .on('end', (event, d) => { if (!event.active) sim.alphaTarget(0); d.fx = null; d.fy = null; })
      );

    // Labels
    const labels = g.append('g')
      .selectAll<SVGTextElement, Node>('text')
      .data(nodes)
      .join('text')
      .text(d => d.id.split('/').pop() || d.id)
      .attr('font-size', 9)
      .attr('fill', '#e5e7eb')
      .attr('text-anchor', 'middle')
      .attr('dy', d => -(Math.max(6, Math.min(18, 6 + d.accessCount * 1.8)) + 4))
      .attr('pointer-events', 'none');

    // Tooltip handlers
    node
      .on('mouseover', (event, d) => {
        setTooltip({
          x: event.pageX + 12,
          y: event.pageY - 28,
          title: d.id,
          rows: [
            { label: 'Group', value: d.group },
            { label: 'Sessions', value: String(d.accessCount) },
          ],
          hint: 'Click to focus · Click again to open',
        });
      })
      .on('mousemove', (event) => {
        setTooltip(prev => prev ? { ...prev, x: event.pageX + 12, y: event.pageY - 28 } : null);
      })
      .on('mouseout', () => setTooltip(null))
      .on('click', (event, d) => {
        event.stopPropagation();
        if (lastClickRef.current === d.id) {
          // Second click: open file, reset graph
          lastClickRef.current = null;
          setFocusNode(null);
          resetGraph();
          // Attempt to open file in reader panel if available
          window.dispatchEvent(new CustomEvent('brain-map:open-file', { detail: { path: d.path } }));
        } else {
          lastClickRef.current = d.id;
          setFocusNode(d.id);
          focusOnNode(d.id);
        }
      });

    // Edge tooltips
    link
      .on('mouseover', (event, d) => {
        const src = typeof d.source === 'object' ? (d.source as Node).id : d.source;
        const tgt = typeof d.target === 'object' ? (d.target as Node).id : d.target;
        setTooltip({
          x: event.pageX + 12,
          y: event.pageY - 28,
          title: `${src} → ${tgt}`,
          rows: [
            { label: 'Type', value: d.sessionType },
            { label: 'Co-access', value: `${(d as any).weight}×` },
            { label: 'Sessions', value: d.sessions.slice(0, 3).join(', ') + (d.sessions.length > 3 ? '…' : '') },
          ],
        });
      })
      .on('mousemove', (event) => {
        setTooltip(prev => prev ? { ...prev, x: event.pageX + 12, y: event.pageY - 28 } : null);
      })
      .on('mouseout', () => setTooltip(null));

    // Click background: reset focus
    svg.on('click', () => {
      lastClickRef.current = null;
      setFocusNode(null);
      resetGraph();
    });

    // Simulation tick
    sim.on('tick', () => {
      link
        .attr('x1', d => (d.source as Node).x!)
        .attr('y1', d => (d.source as Node).y!)
        .attr('x2', d => (d.target as Node).x!)
        .attr('y2', d => (d.target as Node).y!);
      node
        .attr('cx', d => d.x!)
        .attr('cy', d => d.y!);
      labels
        .attr('x', d => d.x!)
        .attr('y', d => d.y!);
    });

    // --- Flow dot animation ---
    let rafId: number;
    function animateDots(timestamp: number) {
      dots.each(function (d) {
        const src = d.edge.source as Node;
        const tgt = d.edge.target as Node;
        if (!src.x || !tgt.x) return;
        const t = ((timestamp * d.speed + d.phase) % 1);
        const x = src.x + (tgt.x - src.x) * t;
        const y = src.y! + (tgt.y! - src.y!) * t;
        d3.select(this).attr('cx', x).attr('cy', y);
      });
      rafId = requestAnimationFrame(animateDots);
    }
    rafId = requestAnimationFrame(animateDots);

    // --- Focus helpers ---
    function focusOnNode(nodeId: string) {
      const connected = new Set<string>([nodeId]);
      edges.forEach(e => {
        const srcId = typeof e.source === 'object' ? (e.source as Node).id : e.source;
        const tgtId = typeof e.target === 'object' ? (e.target as Node).id : e.target;
        if (srcId === nodeId) connected.add(tgtId);
        if (tgtId === nodeId) connected.add(srcId);
      });

      node.attr('opacity', n => connected.has(n.id) ? 1 : 0.15);
      labels.attr('opacity', n => connected.has(n.id) ? 1 : 0.1);
      link.attr('stroke-opacity', e => {
        const srcId = typeof e.source === 'object' ? (e.source as Node).id : e.source;
        const tgtId = typeof e.target === 'object' ? (e.target as Node).id : e.target;
        return (srcId === nodeId || tgtId === nodeId) ? 0.8 : 0.05;
      });
      dots.attr('opacity', d => {
        const srcId = typeof d.edge.source === 'object' ? (d.edge.source as Node).id : d.edge.source;
        const tgtId = typeof d.edge.target === 'object' ? (d.edge.target as Node).id : d.edge.target;
        return (srcId === nodeId || tgtId === nodeId) ? 0.9 : 0;
      });

      // Restart simulation centered on this node
      const target = nodes.find(n => n.id === nodeId);
      if (target) {
        sim.force('center', d3.forceCenter(target.x || width / 2, target.y || height / 2));
        sim.alphaTarget(0.5).restart();
        setTimeout(() => sim.alphaTarget(0), 800);
      }
    }

    function resetGraph() {
      node.attr('opacity', 1);
      labels.attr('opacity', 1);
      link.attr('stroke-opacity', 0.35);
      dots.attr('opacity', 0.55);
      sim.force('center', d3.forceCenter(width / 2, height / 2));
      sim.alphaTarget(0.3).restart();
      setTimeout(() => sim.alphaTarget(0), 600);
    }

    return () => {
      sim.stop();
      cancelAnimationFrame(rafId);
    };
  }, [graphData]);

  if (loading) return (
    <div className="flex items-center justify-center h-full text-gray-400 text-sm">
      Loading brain map…
    </div>
  );

  if (error) return (
    <div className="flex items-center justify-center h-full text-red-400 text-sm">
      Error loading graph: {error}
    </div>
  );

  const stats = graphData ? `${graphData.nodes.length} nodes · ${graphData.edges.length} edges · ${graphData.sessionCount} sessions` : '';

  return (
    <div className="relative w-full h-full bg-black" style={{ minHeight: 500 }}>
      {/* Stats bar */}
      <div className="absolute top-2 left-3 text-xs text-gray-500 z-10 select-none">
        {stats}
        {graphData?.generated && (
          <span className="ml-3 text-gray-600">
            Updated: {new Date(graphData.generated).toLocaleDateString()}
          </span>
        )}
      </div>

      {/* Legend */}
      <div className="absolute top-2 right-3 z-10 flex flex-col gap-1">
        {Object.entries(GROUP_COLORS).map(([group, color]) => (
          <div key={group} className="flex items-center gap-1.5 text-xs text-gray-400">
            <span style={{ width: 8, height: 8, borderRadius: '50%', background: color, display: 'inline-block' }} />
            {group}
          </div>
        ))}
      </div>

      {/* SVG */}
      <svg
        ref={svgRef}
        className="w-full h-full"
        style={{ display: 'block', background: 'black' }}
      />

      {/* Focus label */}
      {focusNode && (
        <div className="absolute bottom-3 left-3 text-xs text-gray-400 z-10">
          Focused: <span className="text-white">{focusNode}</span>
          <span className="ml-2 text-gray-600">(click again to open · click background to reset)</span>
        </div>
      )}

      {/* Tooltip */}
      {tooltip && (
        <div
          className="fixed z-50 pointer-events-none bg-gray-900 border border-gray-700 text-gray-200 text-xs rounded px-2 py-1.5 max-w-xs shadow-lg"
          style={{ left: tooltip.x, top: tooltip.y }}
        >
          <div className="font-semibold mb-1">{tooltip.title}</div>
          {tooltip.rows.map(r => (
            <div key={r.label}>{r.label}: {r.value}</div>
          ))}
          {tooltip.hint && <div className="mt-1 italic text-gray-400">{tooltip.hint}</div>}
        </div>
      )}
    </div>
  );
}
```

---

## Integration Notes

- The component fetches `/api/brain-map/graph` on mount. Ensure the API route is wired (see `references/graph-schema.md`).
- The `brain-map:open-file` custom event fires on second-click. Wire a listener in your host page to handle file reading if you have a reader panel.
- Tooltip renders structured data (title, label/value rows, optional hint) as discrete React elements — no raw HTML injection.
- Flow dot animation uses `requestAnimationFrame` and cleans up on unmount via the returned function from `useEffect`.
- The component is fully self-contained — no external state, no context dependencies.

## Standalone Usage (no Next.js)

To use outside of Next.js, compile the component with any React bundler (Vite, CRA, etc.) and serve `data/brain-map-graph.json` as a static file or via a simple Express route.
