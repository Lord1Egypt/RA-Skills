'use strict';

exports.personalityJs = `
function renderPersonality(personality, memoryGraph) {
  const current = personality.current || {};
  const traits = ['rigor', 'creativity', 'risk_tolerance', 'caution', 'curiosity', 'persistence'];
  const indicators = traits.filter((t) => current[t] !== undefined).map((name) => ({ name, max: 1 }));
  const values = indicators.map((ind) => Number(current[ind.name]) || 0);

  const textColor = chartTextColor();
  if (indicators.length) {
    ensureChart('personalityChart')?.setOption({
      tooltip: {},
      radar: {
        indicator: indicators,
        axisName: { color: textColor },
        splitLine: { lineStyle: { color: isDarkMode() ? '#2c3235' : '#e4e7eb' } },
        splitArea: { areaStyle: { color: ['rgba(50, 116, 217, 0.04)', 'rgba(50, 116, 217, 0.08)'] } },
      },
      series: [{
        type: 'radar',
        data: [{ value: values, name: 'current', areaStyle: { color: 'rgba(50, 116, 217, 0.4)' }, lineStyle: { color: '#3274d9' } }],
      }],
    });
  } else {
    $('personalityChart').innerHTML = '<p class="muted" style="padding:40px;text-align:center">' + esc(t('personality.empty.chart')) + '</p>';
  }

  $('personality-detail').innerHTML = current && Object.keys(current).length
    ? kv(Object.entries(current).slice(0, 12))
    : '<p class="muted">' + esc(t('personality.empty.detail')) + '</p>';

  renderMemoryGraph(memoryGraph);
}

const MEMORY_GRAPH_KIND_COLORS = {
  signal: '#3274d9',
  hypothesis: '#17a2b8',
  attempt: '#ffc107',
  outcome: '#28a745',
  reflection: '#6f42c1',
};

function memoryGraphCategories() {
  return [
    { name: t('personality.cat.event') },
    { name: t('personality.cat.gene') },
    { name: t('personality.cat.signal') },
    { name: t('personality.cat.outcome') },
    { name: t('personality.cat.mutation') },
  ];
}

function shortenGeneId(geneId) {
  if (!geneId) return '';
  return String(geneId).replace(/^gene_gep_/, '').replace(/^gene_/, '').slice(0, 18);
}

function shortTime(ts) {
  if (!ts) return '';
  const d = new Date(ts);
  if (isNaN(d.getTime())) return '';
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' });
}

function buildMemoryGraphData(items) {
  const nodes = new Map();
  const links = [];

  const upsert = (id, init) => {
    if (!id) return null;
    if (!nodes.has(id)) {
      nodes.set(id, { id, refCount: 1, ...init });
    } else {
      const existing = nodes.get(id);
      existing.refCount += 1;
      existing.symbolSize = Math.min(48, (existing.symbolSize || 20) + 1.5);
    }
    return nodes.get(id);
  };

  items.forEach((evt) => {
    try {
      addEventNode(evt, upsert, links);
    } catch (_) { /* skip malformed entry */ }
  });

  return { nodes: Array.from(nodes.values()), links };
}

function addEventNode(evt, upsert, links) {
  const kind = evt.kind || 'event';
  const eventId = 'evt_' + (evt.id || Math.random().toString(36).slice(2, 8));
  const outcomeStatus = evt.outcome && (evt.outcome.status || evt.outcome.predicted_outcome?.status);
  const score = evt.outcome && (evt.outcome.score ?? evt.outcome.predicted_outcome?.score);

  const eventColor = kind === 'outcome' && outcomeStatus
    ? (outcomeStatus === 'success' ? '#28a745' : outcomeStatus === 'failed' ? '#dc3545' : '#ffc107')
    : (MEMORY_GRAPH_KIND_COLORS[kind] || '#3274d9');

  const tsLabel = shortTime(evt.ts);
  const eventLabel = tsLabel ? kind + ' · ' + tsLabel : kind;

  upsert(eventId, {
    name: eventLabel,
    symbolSize: kind === 'outcome' ? 30 : 24,
    itemStyle: { color: eventColor, borderColor: 'rgba(255,255,255,0.5)', borderWidth: 1 },
    category: 0,
    nodeKind: 'event',
    info: { kind, ts: evt.ts, eventId: evt.id, outcomeStatus, score, geneId: evt.gene?.id, mutationCategory: evt.mutation?.category, signals: extractSignals(evt) },
  });

  linkGene(evt, eventId, upsert, links);
  linkSignals(evt, eventId, upsert, links);
  linkOutcome(evt, eventId, upsert, links, outcomeStatus, score);
  linkMutation(evt, eventId, upsert, links);
}

function extractSignals(evt) {
  if (evt.signal && Array.isArray(evt.signal.signals)) return evt.signal.signals;
  if (Array.isArray(evt.signals)) return evt.signals;
  return [];
}

function linkGene(evt, eventId, upsert, links) {
  const geneId = evt.gene && (evt.gene.id || evt.gene);
  if (typeof geneId !== 'string') return;
  const nodeId = 'g_' + geneId;
  upsert(nodeId, {
    name: shortenGeneId(geneId),
    symbolSize: 26,
    itemStyle: { color: '#28a745' },
    category: 1,
    nodeKind: 'gene',
    info: { geneId, category: evt.gene?.category },
  });
  links.push({ source: eventId, target: nodeId });
}

function linkSignals(evt, eventId, upsert, links) {
  const signals = extractSignals(evt);
  signals.slice(0, 4).forEach((sig) => {
    const nodeId = 's_' + sig;
    upsert(nodeId, {
      name: sig,
      symbolSize: 20,
      itemStyle: { color: '#ffc107' },
      category: 2,
      nodeKind: 'signal',
      info: { signal: sig },
    });
    links.push({ source: nodeId, target: eventId, lineStyle: { type: 'dashed' } });
  });
}

function linkOutcome(evt, eventId, upsert, links, outcomeStatus, score) {
  if (typeof outcomeStatus !== 'string') return;
  const nodeId = 'o_' + outcomeStatus;
  const color = outcomeStatus === 'success' ? '#28a745' : outcomeStatus === 'failed' ? '#dc3545' : '#ffc107';
  upsert(nodeId, {
    name: outcomeStatus,
    symbolSize: 24,
    itemStyle: { color },
    category: 3,
    nodeKind: 'outcome',
    info: { status: outcomeStatus, lastScore: score },
  });
  links.push({ source: eventId, target: nodeId });
}

function linkMutation(evt, eventId, upsert, links) {
  const category = evt.mutation && evt.mutation.category;
  if (typeof category !== 'string') return;
  const nodeId = 'm_' + category;
  upsert(nodeId, {
    name: category,
    symbolSize: 22,
    itemStyle: { color: '#dc3545' },
    category: 4,
    nodeKind: 'mutation',
    info: { category },
  });
  links.push({ source: eventId, target: nodeId, lineStyle: { type: 'dotted' } });
}

function memoryGraphTooltip(params) {
  if (params.dataType === 'edge') return '';
  const d = params.data || {};
  const info = d.info || {};
  const refRow = d.refCount > 1 ? mgRow(t('personality.tooltip.referenced'), d.refCount + ' ' + t('personality.tooltip.referencedTimes')) : '';
  const title = '<div style="font-weight:600;margin-bottom:6px">' + esc(d.nodeKind || 'node') + ' · ' + esc(d.name) + '</div>';

  if (d.nodeKind === 'event') {
    return title + mgTooltipBody([
      [t('personality.tooltip.kind'), info.kind],
      [t('personality.tooltip.time'), formatTime(info.ts)],
      [t('personality.tooltip.eventId'), info.eventId],
      [t('personality.tooltip.gene'), info.geneId ? shortenGeneId(info.geneId) : null],
      [t('personality.tooltip.signals'), info.signals?.length ? info.signals.join(', ') : null],
      [t('personality.tooltip.outcome'), info.outcomeStatus ? tStatus(info.outcomeStatus) : null],
      [t('personality.tooltip.score'), info.score != null ? info.score : null],
      [t('personality.tooltip.mutation'), info.mutationCategory],
    ]) + refRow;
  }
  if (d.nodeKind === 'gene') return title + mgTooltipBody([[t('personality.tooltip.geneId'), info.geneId], [t('personality.tooltip.category'), info.category]]) + refRow;
  if (d.nodeKind === 'signal') return title + mgTooltipBody([[t('personality.tooltip.signal'), info.signal]]) + refRow;
  if (d.nodeKind === 'outcome') return title + mgTooltipBody([[t('personality.tooltip.status'), tStatus(info.status)], [t('personality.tooltip.lastScore'), info.lastScore]]) + refRow;
  if (d.nodeKind === 'mutation') return title + mgTooltipBody([[t('personality.tooltip.category'), info.category]]) + refRow;
  return title + refRow;
}

function mgTooltipBody(rows) {
  const filtered = rows.filter(([, v]) => v != null && v !== '');
  if (!filtered.length) return '';
  return '<div style="font-size:12px;line-height:1.5">' +
    filtered.map(([k, v]) => mgRow(k, v)).join('') +
    '</div>';
}

function mgRow(label, value) {
  return '<div><span style="color:#8e99a4">' + esc(label) + ':</span> ' + esc(value) + '</div>';
}

function renderMemoryGraph(graph) {
  const isDark = isDarkMode();
  const textColor = chartTextColor();
  if (!graph.exists || !graph.items.length) {
    $('memory-graph-chart').innerHTML = '<p class="muted" style="padding:40px;text-align:center">' + esc(t('personality.empty.graph')) + '</p>';
    return;
  }

  const { nodes, links } = buildMemoryGraphData(graph.items.slice(0, 100));
  const categories = memoryGraphCategories();

  ensureChart('memory-graph-chart')?.setOption({
    tooltip: {
      trigger: 'item',
      enterable: true,
      backgroundColor: isDark ? 'rgba(24,27,31,0.95)' : 'rgba(255,255,255,0.98)',
      borderColor: isDark ? '#2c3235' : '#e4e7eb',
      textStyle: { color: textColor, fontSize: 12 },
      extraCssText: 'max-width: 320px; box-shadow: 0 4px 12px rgba(0,0,0,0.15);',
      formatter: memoryGraphTooltip,
    },
    legend: { data: categories.map((c) => c.name), top: 0, textStyle: { color: textColor } },
    series: [{
      type: 'graph',
      layout: 'force',
      data: nodes,
      links,
      categories,
      roam: true,
      draggable: true,
      cursor: 'grab',
      label: {
        show: true,
        fontSize: 10,
        color: textColor,
        position: 'right',
        formatter: (p) => (p.data?.refCount > 1 ? p.data.name + ' ×' + p.data.refCount : p.data?.name || ''),
      },
      emphasis: {
        focus: 'adjacency',
        scale: 1.1,
        label: { show: true, fontWeight: 'bold' },
        lineStyle: { width: 3 },
      },
      lineStyle: { color: isDark ? '#3a4045' : '#d8dde2', width: 1, curveness: 0.1, opacity: 0.7 },
      force: { repulsion: 180, edgeLength: [60, 120], gravity: 0.06, friction: 0.6 },
    }],
  });
}

async function loadPersonality() {
  try {
    const [personality, graph] = await Promise.all([
      api('/webui/personality'),
      api('/webui/memory-graph?limit=100'),
    ]);
    renderPersonality(personality, graph);
  } catch (err) {
    console.error(err);
  }
}
`;
