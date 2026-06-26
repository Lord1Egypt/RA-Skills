'use strict';

exports.interactionsJs = `
const HUB_ACTIVITY_STATE = { layer: 'all', hideHeartbeats: true, events: [] };

function buildHubActivityEvents(calls, atpProofs, atpOrders, lifecycleEvents) {
  const events = [];
  (lifecycleEvents || []).forEach((e) => events.push({
    layer: 'lifecycle',
    time: e.ts,
    kind: e.kind,
    outcome: e.outcome,
    statusCode: e.status_code,
    latencyMs: e.latency_ms,
    error: e.error,
    title: e.kind === 'fetch' && e.extra?.skill_id ? 'skill: ' + e.extra.skill_id : (e.node_id || '-'),
  }));
  (calls || []).forEach((c) => events.push({
    layer: 'asset',
    time: c.timestamp,
    kind: c.action,
    outcome: inferAssetOutcome(c.action),
    title: c.asset_id || c.reason || '-',
    meta: c.run_id ? 'run ' + c.run_id : null,
    score: c.score,
  }));
  (atpProofs || []).forEach((p) => events.push({
    layer: 'atp',
    time: p.created_at || p.timestamp,
    kind: 'proof_' + (p.status || 'pending'),
    outcome: p.status === 'verified' || p.status === 'accepted' ? 'ok' : (p.status || 'pending'),
    title: p.delivery_id || p.order_id || '-',
    meta: (p.role || 'consumer') + (p.amount != null ? ' · ' + p.amount + ' credits' : ''),
  }));
  (atpOrders || []).forEach((o) => events.push({
    layer: 'atp',
    time: o.created_at || o.updated_at,
    kind: 'order_' + (o.status || 'pending'),
    outcome: o.status === 'completed' ? 'ok' : (o.status || 'pending'),
    title: o.order_id || o.id || '-',
    meta: (o.routing || '-') + (o.budget != null ? ' · ' + o.budget + ' credits' : ''),
  }));
  return events.sort((a, b) => new Date(b.time || 0) - new Date(a.time || 0));
}

function inferAssetOutcome(action) {
  if (!action) return 'unknown';
  if (action.endsWith('_hit') || action === 'asset_reuse' || action === 'asset_reference' || action === 'asset_publish') return 'ok';
  if (action.endsWith('_miss') || action.endsWith('_skip')) return 'miss';
  return action;
}

function summarizeHubActivity(events) {
  const now = Date.now();
  const last24h = events.filter((e) => Date.parse(e.time || 0) >= now - 24 * 60 * 60 * 1000);
  const heartbeats = events.filter((e) => e.layer === 'lifecycle' && e.kind === 'heartbeat');
  const heartbeatOk = heartbeats.filter((e) => e.outcome === 'ok' || e.outcome === 'recovered');
  const heartbeatHealthPct = heartbeats.length === 0 ? null : Math.round((heartbeatOk.length / heartbeats.length) * 100);
  const latencies = events.filter((e) => typeof e.latencyMs === 'number').map((e) => e.latencyMs);
  const lastHelloOk = events.find((e) => e.layer === 'lifecycle' && e.kind === 'hello' && e.outcome === 'ok')?.time;
  const lastHeartbeatOk = events.find((e) => e.layer === 'lifecycle' && e.kind === 'heartbeat' && (e.outcome === 'ok' || e.outcome === 'recovered'))?.time;
  const assetEvents = events.filter((e) => e.layer === 'asset');
  const assetHits = assetEvents.filter((e) => e.outcome === 'ok').length;
  const assetHitRate = assetEvents.length === 0 ? null : Math.round((assetHits / assetEvents.length) * 100);

  return {
    total: events.length,
    last24h: last24h.length,
    heartbeatHealthPct,
    assetHitRate,
    lastHelloOk,
    lastHeartbeatOk,
    latencyP50: percentile(latencies, 50),
    latencyP95: percentile(latencies, 95),
  };
}

function percentile(values, p) {
  if (!values.length) return null;
  const sorted = values.slice().sort((a, b) => a - b);
  return sorted[Math.min(sorted.length - 1, Math.floor((sorted.length * p) / 100))];
}

function renderHubActivity(events, hasProxy) {
  HUB_ACTIVITY_STATE.events = events;
  HUB_ACTIVITY_STATE.hasProxy = !!hasProxy;
  renderHubActivitySummary(summarizeHubActivity(events));
  bindHubActivityFilters();
  renderHubActivityTable();
}

function renderHubActivitySummary(s) {
  const healthCls = s.heartbeatHealthPct == null ? '' : s.heartbeatHealthPct >= 95 ? 'success' : s.heartbeatHealthPct >= 70 ? 'pending' : 'failed';
  const hitCls = s.assetHitRate == null ? '' : s.assetHitRate >= 50 ? 'success' : s.assetHitRate >= 20 ? 'pending' : 'failed';
  $('hub-activity-summary').innerHTML =
    statBox(t('interactions.stat.heartbeatHealth'), s.heartbeatHealthPct == null ? '—' : s.heartbeatHealthPct + '%', healthCls) +
    statBox(t('interactions.stat.assetHitRate'), s.assetHitRate == null ? '—' : s.assetHitRate + '%', hitCls) +
    statBox(t('interactions.stat.events24h'), String(s.last24h ?? 0)) +
    statBox(t('interactions.stat.latency'), s.latencyP50 == null ? '—' : (s.latencyP50 + ' / ' + (s.latencyP95 ?? '—') + ' ms')) +
    statBox(t('interactions.stat.lastHelloOk'), formatTime(s.lastHelloOk)) +
    statBox(t('interactions.stat.lastHeartbeatOk'), formatTime(s.lastHeartbeatOk));
}

function bindHubActivityFilters() {
  const bar = $('hub-activity-filters');
  if (!bar) return;
  bar.style.display = HUB_ACTIVITY_STATE.events.length ? 'flex' : 'none';
  bar.querySelectorAll('[data-filter-layer]').forEach((btn) => {
    if (btn._bound) return;
    btn._bound = true;
    btn.addEventListener('click', () => {
      HUB_ACTIVITY_STATE.layer = btn.getAttribute('data-filter-layer');
      bar.querySelectorAll('[data-filter-layer]').forEach((b) => b.classList.toggle('active', b === btn));
      renderHubActivityTable();
    });
  });
  const cb = $('hide-heartbeats');
  if (cb && !cb._bound) {
    cb._bound = true;
    cb.checked = HUB_ACTIVITY_STATE.hideHeartbeats;
    cb.addEventListener('change', () => {
      HUB_ACTIVITY_STATE.hideHeartbeats = cb.checked;
      renderHubActivityTable();
    });
  }
}

function renderHubActivityTable() {
  const filtered = HUB_ACTIVITY_STATE.events.filter((e) => {
    if (HUB_ACTIVITY_STATE.layer !== 'all' && e.layer !== HUB_ACTIVITY_STATE.layer) return false;
    if (HUB_ACTIVITY_STATE.hideHeartbeats && e.layer === 'lifecycle' && e.kind === 'heartbeat' && (e.outcome === 'ok' || e.outcome === 'recovered')) return false;
    return true;
  }).slice(0, 150);

  if (!filtered.length) {
    $('hub-activity').innerHTML = HUB_ACTIVITY_STATE.events.length
      ? '<p class="muted">' + esc(t('interactions.empty.filtered')) + '</p>'
      : hubEmptyHint(HUB_ACTIVITY_STATE.hasProxy);
    return;
  }

  const rows = filtered.map((e) => {
    const ok = e.outcome === 'ok' || e.outcome === 'recovered';
    const fail = e.outcome && (String(e.outcome).startsWith('fail') || String(e.outcome).startsWith('auth_failed') || String(e.outcome).startsWith('http_'));
    const cls = ok ? 'ok' : fail ? 'fail' : 'neutral';
    return '<tr class="' + cls + '">' +
      '<td>' + esc(formatTime(e.time)) + '</td>' +
      '<td><span class="pill ' + esc(e.layer) + '">' + esc(tAction(e.layer)) + '</span></td>' +
      '<td><span class="pill ' + esc(e.kind || '-') + '">' + esc(tAction(e.kind) || '-') + '</span></td>' +
      '<td><span class="status-indicator ' + (ok ? 'success' : fail ? 'failed' : 'unknown') + '"></span>' + esc(tStatus(e.outcome) || '-') + '</td>' +
      // statusCode / latencyMs are SHOULD-be-numeric but the producer
      // is the proxy daemon, which has historically leaked string
      // shapes ("timeout", "n/a"). Bugbot caught the asymmetry: every
      // other column on this row is esc()'d. Defensive escape here
      // matches the rest of the renderer instead of trusting the
      // proxy to never inject HTML chars.
      '<td>' + esc(e.statusCode ?? '—') + '</td>' +
      '<td>' + esc(e.latencyMs == null ? '—' : e.latencyMs + ' ms') + '</td>' +
      '<td class="lifecycle-error">' + esc(e.title || '') + (e.meta ? ' <span class="muted small">' + esc(e.meta) + '</span>' : '') + (e.error ? ' <span class="status-failed">' + esc(e.error) + '</span>' : '') + '</td>' +
      '</tr>';
  }).join('');

  $('hub-activity').innerHTML = '<table class="data-table lifecycle-table">' +
    '<thead><tr>' +
      '<th>' + esc(t('interactions.col.time')) + '</th>' +
      '<th>' + esc(t('interactions.col.layer')) + '</th>' +
      '<th>' + esc(t('interactions.col.kind')) + '</th>' +
      '<th>' + esc(t('interactions.col.outcome')) + '</th>' +
      '<th>' + esc(t('interactions.col.status')) + '</th>' +
      '<th>' + esc(t('interactions.col.latency')) + '</th>' +
      '<th>' + esc(t('interactions.col.detail')) + '</th>' +
    '</tr></thead>' +
    '<tbody>' + rows + '</tbody></table>';
}

function hubEmptyHint(hasProxy) {
  if (hasProxy) {
    return '<p class="muted">' + esc(t('interactions.empty.proxyRunning')) + '</p>';
  }
  return '<p class="muted">' + t('interactions.empty.noProxy') + '</p>';
}

function renderAgentStream(mailbox, sessions, dms) {
  const items = [];
  (mailbox || []).forEach((m) => items.push({
    kind: 'mailbox',
    time: m.timestamp,
    action: 'mb_' + (m.direction || 'msg'),
    title: m.summary || m.type || '-',
    meta: (m.type || '-') + ' · ' + (m.status || '-'),
    detail: m,
  }));
  (sessions || []).forEach((s) => items.push({
    kind: 'session',
    time: s.created_at || s.updated_at,
    action: 'session_' + (s.status || 'active'),
    title: s.session_id || s.id || '-',
    meta: 'with ' + (s.peer || s.peer_node_id || '-'),
    detail: s,
  }));
  (dms || []).forEach((d) => items.push({
    kind: 'dm',
    time: d.created_at,
    action: 'dm_' + (d.direction || 'msg'),
    title: d.title || d.message_id || '-',
    meta: (d.from || '-') + ' → ' + (d.to || '-'),
    detail: d,
  }));

  if (!items.length) {
    $('agent-stream').innerHTML = '<p class="muted">' + esc(t('interactions.empty.noAgent')) + '</p>';
    return;
  }
  items.sort((a, b) => new Date(b.time || 0) - new Date(a.time || 0));
  $('agent-stream').innerHTML = '<ul class="stream-list">' + items.slice(0, 60).map(streamItem).join('') + '</ul>';
}

function streamItem(item) {
  return '<li class="stream-item">' +
    '<div class="stream-head">' +
      '<span class="pill ' + esc(item.action) + '">' + esc(item.action) + '</span>' +
      '<span class="muted small">' + esc(formatTime(item.time)) + '</span>' +
    '</div>' +
    '<div class="stream-title">' + esc(item.title) + '</div>' +
    '<div class="muted small">' + esc(item.meta) + '</div>' +
    '</li>';
}

function renderInteractionCharts(calls, atpProofs, mailbox) {
  const textColor = chartTextColor();
  const isDark = isDarkMode();

  const actionCounts = {};
  (calls || []).forEach((c) => { actionCounts[c.action] = (actionCounts[c.action] || 0) + 1; });
  ensureChart('hubActionChart')?.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie', radius: ['40%', '70%'],
      itemStyle: { borderRadius: 4, borderColor: isDark ? '#181b1f' : '#fff', borderWidth: 2 },
      label: { show: false },
      labelLine: { show: false },
      data: Object.keys(actionCounts).length
        ? Object.entries(actionCounts).map(([name, value]) => ({ name, value }))
        : [{ name: 'no calls', value: 1, itemStyle: { color: '#444' } }],
    }],
  });

  const dayBuckets = bucketByDay([...(calls || []), ...(atpProofs || []), ...(mailbox || [])], 30);
  ensureChart('activityChart')?.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '8%', containLabel: true },
    xAxis: { type: 'category', data: dayBuckets.labels, axisLabel: { color: textColor, fontSize: 10 } },
    yAxis: { type: 'value', axisLabel: { color: textColor }, splitLine: { lineStyle: { color: isDark ? '#2c3235' : '#e4e7eb' } } },
    series: [{
      type: 'line', data: dayBuckets.values, smooth: true, areaStyle: { opacity: 0.18, color: '#3274d9' },
      lineStyle: { color: '#3274d9', width: 2 }, itemStyle: { color: '#3274d9' },
    }],
  });

  const typeCounts = {};
  (mailbox || []).forEach((m) => { typeCounts[m.type || 'unknown'] = (typeCounts[m.type || 'unknown'] || 0) + 1; });
  ensureChart('mailboxChart')?.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '5%', containLabel: true },
    xAxis: { type: 'value', axisLabel: { color: textColor }, splitLine: { lineStyle: { color: isDark ? '#2c3235' : '#e4e7eb' } } },
    yAxis: { type: 'category', data: Object.keys(typeCounts).length ? Object.keys(typeCounts) : ['no messages'], axisLabel: { color: textColor } },
    series: [{
      type: 'bar',
      data: Object.keys(typeCounts).length ? Object.values(typeCounts) : [0],
      itemStyle: { color: '#28a745', borderRadius: [0, 4, 4, 0] },
    }],
  });
}

function bucketByDay(items, days) {
  const today = new Date(); today.setHours(0,0,0,0);
  const labels = [], counts = new Array(days).fill(0);
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(today); d.setDate(d.getDate() - i);
    labels.push((d.getMonth()+1) + '/' + d.getDate());
  }
  items.forEach((it) => {
    const t = new Date(it.timestamp || it.time || it.created_at || 0);
    if (isNaN(t.getTime())) return;
    t.setHours(0,0,0,0);
    const diff = Math.round((today - t) / 86400000);
    if (diff >= 0 && diff < days) counts[days - 1 - diff]++;
  });
  return { labels, values: counts };
}

function renderProxySnapshots(snapshots) {
  if (!snapshots || !Object.keys(snapshots).length) {
    $('proxy-snapshots').innerHTML = '<p class="muted snapshot-empty">' + t('interactions.empty.proxyNotRunning') + '</p>';
    return;
  }
  $('proxy-snapshots').innerHTML = Object.entries(snapshots).map(([key, snap]) => {
    const ok = snap?.ok;
    const dot = '<span class="status-indicator ' + (ok ? 'status-success' : 'status-failed') + '"></span>';
    const detail = ok && snap.body
      ? (Array.isArray(snap.body) ? snap.body.length + ' ' + t('interactions.snapshot.items') : Object.keys(snap.body).length + ' ' + t('interactions.snapshot.fields'))
      : (snap?.error || t('interactions.snapshot.unavailable'));
    return '<div class="snapshot-card"><div>' + dot + '<strong>' + esc(key) + '</strong></div>' +
      '<div class="muted small">' + esc(detail) + '</div></div>';
  }).join('');
}

async function loadInteractions() {
  $('hub-activity').innerHTML = '<p class="muted">' + esc(t('common.loading')) + '</p>';
  $('agent-stream').innerHTML = '<p class="muted">' + esc(t('common.loading')) + '</p>';
  try {
    // Lifecycle is optional: not every build ships /webui/lifecycle (the
    // observer-side module is only present when the proxy daemon is wired
    // in). Treat a missing/erroring lifecycle endpoint as "no data" so the
    // rest of the Hub Activity panel still renders instead of failing the
    // whole tab with "Failed: Not found".
    const [callsResult, interactions, lifecycle] = await Promise.all([
      api('/webui/assets/calls?limit=500'),
      api('/webui/interactions?last=200'),
      api('/webui/lifecycle?last=500').catch(() => ({ events: [] })),
    ]);
    const calls = callsResult.data || [];
    const proofs = interactions.proxySnapshots?.atpProofs?.body?.proofs || interactions.proxySnapshots?.atpProofs?.body || [];
    const orders = interactions.proxySnapshots?.atpProofs?.body?.orders || [];
    const sessions = interactions.proxySnapshots?.sessions?.body?.sessions || interactions.proxySnapshots?.sessions?.body || [];
    const dms = interactions.proxySnapshots?.dms?.body?.dms || interactions.proxySnapshots?.dms?.body || [];
    const mailbox = interactions.mailbox?.data || [];
    const lifecycleEvents = lifecycle?.events || [];

    const unified = buildHubActivityEvents(
      calls,
      Array.isArray(proofs) ? proofs : [],
      Array.isArray(orders) ? orders : [],
      lifecycleEvents,
    );
    renderHubActivity(unified, interactions.proxy?.running);
    renderAgentStream(mailbox, Array.isArray(sessions) ? sessions : [], Array.isArray(dms) ? dms : []);
    renderInteractionCharts(calls, Array.isArray(proofs) ? proofs : [], mailbox);
    renderProxySnapshots(interactions.proxySnapshots);
  } catch (err) {
    $('hub-activity').innerHTML = '<p class="status-failed">' + esc(t('common.failedPrefix')) + esc(err.message) + '</p>';
  }
}

function statBox(label, value, cls) {
  return '<div class="stat-box ' + (cls || '') + '">' +
    '<div class="stat-label">' + esc(label) + '</div>' +
    '<div class="stat-value">' + esc(value) + '</div>' +
    '</div>';
}
`;
