'use strict';

exports.assetsJs = `
function renderGenesTable(data) {
  return '<table class="data-table"><thead><tr>' +
    '<th>' + esc(t('assets.col.id')) + '</th>' +
    '<th>' + esc(t('assets.col.category')) + '</th>' +
    '<th>' + esc(t('assets.col.signals')) + '</th>' +
    '<th>' + esc(t('assets.col.strategy')) + '</th>' +
    '<th>' + esc(t('assets.col.validation')) + '</th>' +
    '</tr></thead><tbody>' +
    data.map((g) => '<tr><td><strong>' + esc(g.id) + '</strong></td>' +
      '<td><span class="pill ' + esc(g.category) + '">' + esc(g.category) + '</span></td>' +
      '<td>' + pillList(g.signals_match || [], 'signal') + '</td>' +
      '<td><details><summary>' + (g.strategy?.length || 0) + ' ' + esc(t('assets.steps')) + '</summary><ol class="reason-list">' + (g.strategy || []).map(s => '<li>' + esc(s) + '</li>').join('') + '</ol></details></td>' +
      '<td><details><summary>' + (g.validation?.length || 0) + ' ' + esc(t('assets.cmds')) + '</summary><ul class="reason-list">' + (g.validation || []).map(s => '<li><code>' + esc(s) + '</code></li>').join('') + '</ul></details></td>' +
      '</tr>').join('') +
    '</tbody></table>';
}

function renderCapsulesTable(data) {
  if (!data.length) return '<p class="muted">' + esc(t('assets.empty.capsules')) + '</p>';
  return '<table class="data-table"><thead><tr>' +
    '<th>' + esc(t('assets.col.id')) + '</th>' +
    '<th>' + esc(t('assets.col.gene')) + '</th>' +
    '<th>' + esc(t('assets.col.outcome')) + '</th>' +
    '<th>' + esc(t('assets.col.confidence')) + '</th>' +
    '<th>' + esc(t('assets.col.blast')) + '</th>' +
    '</tr></thead><tbody>' +
    data.map((c) => '<tr><td><strong>' + esc(c.id) + '</strong></td><td>' + esc(c.gene || '-') + '</td>' +
      '<td><span class="status-indicator ' + getStatusClass(c.outcome?.status) + '"></span>' + esc(tStatus(c.outcome?.status) || '-') + '</td>' +
      '<td>' + esc(c.confidence ?? '-') + '</td>' +
      '<td>' + esc((c.blast_radius?.files ?? '-') + '/' + (c.blast_radius?.lines ?? '-')) + '</td>' +
      '</tr>').join('') +
    '</tbody></table>';
}

function renderEventsList(data) {
  if (!data.length) return '<p class="muted">' + t('assets.empty.events') + '</p>';
  return '<ul class="event-list">' + data.map((e) => '<li>' +
    '<div><strong>' + esc(e.id || '-') + '</strong> <span class="muted small">' + esc(formatTime(e.timestamp || e.created_at)) + '</span></div>' +
    '<div>' + esc(t('assets.events.signals')) + pillList(e.signals || e.signals_matched || [], 'signal') + '</div>' +
    '<div>' + esc(t('assets.events.genes')) + pillList(e.genes_used || [], '') + '</div>' +
    '<div>' + esc(t('assets.events.outcome')) + '<span class="status-indicator ' + getStatusClass(e.outcome?.status) + '"></span>' + esc(tStatus(e.outcome?.status) || '-') + '</div>' +
    '</li>').join('') + '</ul>';
}

function renderCandidatesTable(data) {
  if (!data.length) return '<p class="muted">' + esc(t('assets.empty.candidates')) + '</p>';
  return '<table class="data-table"><thead><tr>' +
    '<th>' + esc(t('assets.col.source')) + '</th>' +
    '<th>' + esc(t('assets.col.assetId')) + '</th>' +
    '<th>' + esc(t('assets.col.score')) + '</th>' +
    '<th>' + esc(t('assets.col.time')) + '</th>' +
    '</tr></thead><tbody>' +
    data.map((c) => '<tr><td>' + esc(c.source || c.source_node_id || '-') + '</td>' +
      '<td><code>' + esc(c.asset_id || c.id || '-') + '</code></td>' +
      '<td>' + esc(c.score ?? '-') + '</td>' +
      '<td>' + esc(formatTime(c.timestamp)) + '</td></tr>').join('') +
    '</tbody></table>';
}

function renderCallsTable(data) {
  if (!data.length) return '<p class="muted">' + esc(t('assets.empty.calls')) + '</p>';
  return '<table class="data-table"><thead><tr>' +
    '<th>' + esc(t('assets.col.time')) + '</th>' +
    '<th>' + esc(t('assets.col.action')) + '</th>' +
    '<th>' + esc(t('assets.col.asset')) + '</th>' +
    '<th>' + esc(t('assets.col.run')) + '</th>' +
    '<th>' + esc(t('assets.col.score')) + '</th>' +
    '</tr></thead><tbody>' +
    data.map((c) => '<tr><td>' + esc(formatTime(c.timestamp)) + '</td>' +
      '<td><span class="pill ' + esc(c.action) + '">' + esc(tAction(c.action)) + '</span></td>' +
      '<td><code>' + esc(c.asset_id || '-') + '</code></td>' +
      '<td>' + esc(c.run_id || '-') + '</td>' +
      '<td>' + esc(c.score ?? '-') + '</td></tr>').join('') +
    '</tbody></table>';
}

const ASSET_RENDERERS = {
  genes: renderGenesTable,
  capsules: renderCapsulesTable,
  events: renderEventsList,
  candidates: renderCandidatesTable,
  calls: renderCallsTable,
};

const ASSET_ENDPOINTS = {
  genes: '/webui/assets/genes',
  capsules: '/webui/assets/capsules',
  events: '/webui/assets/events',
  candidates: '/webui/assets/candidates',
  calls: '/webui/assets/calls',
};

async function loadAsset(kind) {
  state.currentAsset = kind;
  $('asset-list').innerHTML = '<p class="muted">' + esc(t('common.loading')) + '</p>';
  document.querySelectorAll('.asset-tab').forEach((b) => b.classList.toggle('active', b.getAttribute('data-asset') === kind));
  try {
    const result = await api(ASSET_ENDPOINTS[kind] + '?limit=200');
    const renderer = ASSET_RENDERERS[kind];
    const total = result.pagination?.totalItems ?? (result.data || []).length;
    $('asset-list').innerHTML =
      '<div class="muted small" style="margin-bottom:12px">' + total + ' ' + esc(t('assets.records')) + '</div>' +
      renderer(result.data || []);
  } catch (err) {
    $('asset-list').innerHTML = '<p class="status-failed">' + esc(t('common.failedPrefix')) + esc(err.message) + '</p>';
  }
}
`;
