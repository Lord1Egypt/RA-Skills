'use strict';

exports.pipelinesJs = `
function renderRuns(result) {
  const runs = result.data || [];
  const tbody = document.querySelector('#runsTable tbody');
  if (!runs.length) {
    tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;color:var(--text-muted)">' + esc(t('pipelines.runs.empty')) + '</td></tr>';
    renderScoreTrend([]);
    return;
  }
  tbody.innerHTML = runs.map((run) =>
    '<tr data-run="' + esc(run.runId) + '">' +
    '<td><strong>' + esc(run.runId) + '</strong></td>' +
    '<td><span class="status-indicator ' + getStatusClass(run.status) + '"></span>' + esc(tStatus(run.status)) + '</td>' +
    '<td>' + esc(run.selectedGeneId || '-') + '</td>' +
    '<td>' + scoreBar(run.score) + '</td>' +
    '<td>' + esc(formatTime(run.updatedAt)) + '</td>' +
    '</tr>'
  ).join('');
  document.querySelectorAll('#runsTable tbody tr[data-run]').forEach((tr) => {
    tr.addEventListener('click', () => loadRun(tr.getAttribute('data-run')));
  });
  renderScoreTrend(runs);
}

function validationDimensionLabel(d) {
  // Validation dimensions ride on stable enum tokens ('stable_no_error',
  // 'heuristic_delta', etc). Look up a localized label; fall back to the
  // raw token so unknown dimensions still render.
  const key = 'pipelines.dim.' + d;
  return I18N_DICT[key] ? t(key) : d;
}

function renderValidationBlock(validation, runStatus) {
  if (!validation) {
    const hint = runStatus === 'review_pending'
      ? t('pipelines.detail.validation.hint.reviewPending')
      : runStatus === 'running' || runStatus === 'pending'
        ? t('pipelines.detail.validation.hint.running')
        : t('pipelines.detail.validation.hint.none');
    return '<div class="detail-block"><h4>' + esc(t('pipelines.detail.validation.title')) + '</h4><p class="muted small">' + esc(hint) + '</p></div>';
  }
  const score = typeof validation.score === 'number' ? validation.score : null;
  const statusCls = validation.status === 'success' ? 'success' : validation.status === 'failed' ? 'failed' : 'unknown';
  const scoreColor = score === null ? '#888' : score >= 0.7 ? '#28a745' : score >= 0.5 ? '#ffc107' : '#dc3545';
  const dims = (validation.dimensions || []).map((d) =>
    '<span class="pill validation-dim">' + esc(validationDimensionLabel(d)) + '</span>'
  ).join('') || '<span class="muted small">' + esc(t('pipelines.detail.validation.noDimensions')) + '</span>';

  let html = '<div class="detail-block validation-block"><h4>' + esc(t('pipelines.detail.validation.title')) + '</h4>';
  html += '<div class="validation-summary">' +
    '<div class="validation-status"><span class="status-indicator ' + statusCls + '"></span>' +
      '<strong>' + esc(tStatus(validation.status || 'unknown')) + '</strong>' +
    '</div>';
  if (score !== null) {
    html += '<div class="validation-score-wrap">' +
      '<div class="validation-score-label">' + esc(t('pipelines.detail.validation.score')) + '</div>' +
      '<div class="score-bar score-bar-lg">' +
        '<div class="score-bar-fill" style="width:' + (score * 100).toFixed(0) + '%;background:' + scoreColor + '"></div>' +
        '<span class="score-bar-text">' + (score * 100).toFixed(1) + '%</span>' +
      '</div></div>';
  }
  html += '</div>';
  html += '<div class="validation-dims"><span class="muted small">' + esc(t('pipelines.detail.validation.dimensions')) + '</span> ' + dims + '</div>';
  if (validation.observedSignals && validation.observedSignals.length) {
    html += '<div class="validation-observed"><span class="muted small">' + esc(t('pipelines.detail.validation.observed')) + '</span> ' +
      pillList(validation.observedSignals, 'signal') + '</div>';
  }
  if (validation.predictive) {
    const entries = Object.entries(validation.predictive).slice(0, 6);
    html += '<details class="validation-predictive"><summary>' + esc(t('pipelines.detail.validation.predictive')) + '</summary>' + kv(entries) + '</details>';
  }
  if (validation.timestamp) {
    html += '<p class="muted small" style="margin-top:8px">' + esc(t('pipelines.detail.validation.validatedAt')) + esc(formatTime(validation.timestamp)) + '</p>';
  }
  html += '</div>';
  return html;
}

function scoreBar(score) {
  if (typeof score !== 'number') return '<span class="muted small">—</span>';
  const pct = Math.round(score * 100);
  const color = score >= 0.7 ? '#28a745' : score >= 0.5 ? '#ffc107' : '#dc3545';
  return '<div class="score-bar" title="' + score.toFixed(3) + '">' +
    '<div class="score-bar-fill" style="width:' + pct + '%;background:' + color + '"></div>' +
    '<span class="score-bar-text">' + pct + '%</span></div>';
}

function renderScoreTrend(runs) {
  const el = document.getElementById('scoreTrendChart');
  if (!el) return;
  const scored = runs.filter((r) => typeof r.score === 'number')
    .sort((a, b) => new Date(a.finishedAt || a.updatedAt) - new Date(b.finishedAt || b.updatedAt));
  if (!scored.length) {
    // Dispose any prior chart bound to this element so the empty-state
    // innerHTML write doesn't collide with ECharts owning the canvas.
    // Otherwise the next non-empty render would reuse a dead instance
    // and ECharts would warn about re-initializing an active container.
    if (state.charts['scoreTrendChart']) {
      state.charts['scoreTrendChart'].dispose();
      delete state.charts['scoreTrendChart'];
    }
    el.innerHTML = '<p class="muted small" style="padding:24px 0;text-align:center">' + esc(t('pipelines.chart.scoreTrend.empty')) + '</p>';
    return;
  }
  // Transitioning from empty-state to chart: the empty <p> left in the
  // container has to go before ensureChart's first init, otherwise
  // ECharts measures the <p> as its viewport.
  if (!state.charts['scoreTrendChart']) el.innerHTML = '';
  // Use ensureChart so the instance is tracked in state.charts and gets
  // resized on window resize / disposed on theme + locale toggle, same
  // as every other chart on the page.
  const chart = ensureChart('scoreTrendChart');
  const textColor = chartTextColor();
  chart.setOption({
    grid: { left: 50, right: 20, top: 20, bottom: 30 },
    tooltip: {
      trigger: 'axis',
      // ECharts renders the formatter return value as HTML, so every
      // dynamic field that originates from a run record must be esc()'d
      // (run IDs and gene IDs are user/agent-supplied strings that have
      // historically contained '/' and other HTML-meaningful chars).
      formatter: (params) => {
        const p = params[0];
        const r = scored[p.dataIndex];
        return '<strong>' + esc(r.runId) + '</strong><br/>' +
          esc(t('pipelines.col.gene')) + ': ' + esc(r.selectedGeneId || '-') + '<br/>' +
          esc(t('pipelines.col.score')) + ': <strong>' + esc((r.score || 0).toFixed(3)) + '</strong><br/>' +
          esc(formatTime(r.finishedAt || r.updatedAt));
      },
    },
    xAxis: {
      type: 'category',
      data: scored.map((r) => r.runId.slice(-8)),
      axisLabel: { color: textColor, fontSize: 10 },
    },
    yAxis: {
      type: 'value',
      min: 0, max: 1,
      axisLabel: { color: textColor, formatter: (v) => (v * 100).toFixed(0) + '%' },
      splitLine: { lineStyle: { color: isDarkMode() ? '#2a3038' : '#e9ecef' } },
    },
    series: [{
      type: 'line',
      smooth: true,
      data: scored.map((r) => r.score),
      areaStyle: { opacity: 0.2 },
      lineStyle: { width: 2, color: '#3274d9' },
      itemStyle: { color: '#3274d9' },
      markLine: {
        silent: true,
        symbol: 'none',
        lineStyle: { type: 'dashed', color: '#28a745' },
        data: [{ yAxis: 0.7, label: { formatter: t('pipelines.chart.scoreTrend.passLine'), color: '#28a745' } }],
      },
    }],
  });
}

function renderRunDetail(run) {
  const phases = run.phases || [];
  const detail = run.detail || {};

  let html = '<div class="run-header">' +
    '<h3>' + esc(run.runId) + '</h3>' +
    '<div class="run-meta">' +
    '<span>' + esc(t('pipelines.col.status')) + ': <span class="status-indicator ' + getStatusClass(run.status) + '"></span><strong>' + esc(tStatus(run.status)) + '</strong></span>' +
    '<span>' + esc(t('pipelines.col.gene')) + ': <strong>' + esc(run.selectedGeneId || '-') + '</strong></span>' +
    '<span>' + esc(t('pipelines.col.updated')) + ': <strong>' + esc(formatTime(run.updatedAt)) + '</strong></span>' +
    '</div></div>';

  html += '<div class="run-body">';

  html += '<div><h4>' + esc(t('pipelines.timeline')) + '</h4><ul class="timeline">';
  html += phases.map((phase) => {
    const cls = phase.status === 'success' ? 'success' :
                phase.status === 'failed' ? 'failed' :
                phase.status === 'running' || phase.status === 'pending' ? 'running' :
                phase.status === 'blocked' ? 'blocked' : '';
    return '<li class="' + cls + '">' +
      '<div class="timeline-title">' + esc(phase.phase) + ' <span class="muted small">' + esc(tStatus(phase.status)) + '</span></div>' +
      '<p class="timeline-desc">' + esc(phase.summary) + '</p>' +
      '</li>';
  }).join('');
  html += '</ul></div>';

  html += '<div><h4>' + esc(t('pipelines.runGraph')) + '</h4><div id="runGraph" class="chart-container" style="height: 360px;"></div></div>';

  html += '</div>';

  if (detail) {
    html += '<div class="run-detail-grid">';
    html += '<div class="detail-block"><h4>' + esc(t('pipelines.detail.triggerSignals')) + '</h4>' +
      '<p class="muted small" style="margin:-4px 0 8px 0">' + esc(t('pipelines.detail.triggerSignals.desc')) + '</p>' +
      pillList(detail.signals, 'signal') + '</div>';
    if (detail.selector) {
      html += '<div class="detail-block"><h4>' + esc(t('pipelines.detail.selector')) + '</h4>' +
        kv([
          [t('pipelines.detail.selector.selected'), detail.selector.selected],
          [t('pipelines.detail.selector.path'), detail.selector.selectionPath || detail.selector.selection_path],
          [t('pipelines.detail.selector.memoryUsed'), detail.selector.memoryUsed || detail.selector.memory_used],
        ]) +
        '<ul class="reason-list">' + (detail.selector.reason || []).map(r => '<li>' + esc(r) + '</li>').join('') + '</ul>' +
        '</div>';
    }
    if (detail.mutation) {
      html += '<div class="detail-block"><h4>' + esc(t('pipelines.detail.mutation')) + '</h4>' + kv([
        [t('pipelines.detail.mutation.id'), detail.mutation.id],
        [t('pipelines.detail.mutation.category'), detail.mutation.category],
        [t('pipelines.detail.mutation.targetType'), detail.mutation.targetType],
        [t('pipelines.detail.mutation.strategySteps'), detail.mutation.strategySteps],
        [t('pipelines.detail.mutation.triggerSignals'), (detail.mutation.triggerSignals || []).join(', ') || '-'],
      ]) + '</div>';
    }
    html += renderValidationBlock(detail.validation, run.status);
    if (detail.blastRadius) {
      html += '<div class="detail-block"><h4>' + esc(t('pipelines.detail.blastRadius')) + '</h4>' + kv([
        [t('pipelines.detail.blastRadius.files'), detail.blastRadius.files],
        [t('pipelines.detail.blastRadius.lines'), detail.blastRadius.lines],
        [t('pipelines.detail.blastRadius.risk'), detail.blastRadius.risk_level || detail.blastRadius.risk],
      ]) + '</div>';
    }
    if (detail.personalityState) {
      html += '<div class="detail-block"><h4>' + esc(t('pipelines.detail.personalityState')) + '</h4>' + kv(
        Object.entries(detail.personalityState).slice(0, 8)
      ) + '</div>';
    }
    if (detail.initialUserPrompt) {
      html += '<div class="detail-block"><h4>' + esc(t('pipelines.detail.initialUserPrompt')) + '</h4><pre class="snippet">' + esc(detail.initialUserPrompt) + '</pre></div>';
    }
    html += '</div>';
  }

  $('run-detail').innerHTML = html;

  setTimeout(() => renderRunGraph(run, detail), 0);
}

function renderRunGraph(run, detail) {
  const chartEl = document.getElementById('runGraph');
  if (!chartEl) return;
  // <div id="run-detail"> is rewritten on every loadRun call (see
  // renderRunDetail), which detaches the previous #runGraph DOM. A
  // cached ECharts instance from the previous run is bound to that
  // detached element and would silently render to nothing on
  // setOption. Dispose the stale instance before re-initializing
  // against the fresh #runGraph so disposeAllCharts() on theme
  // toggle and the window-resize handler keep working.
  if (state.charts['runGraph']) {
    state.charts['runGraph'].dispose();
    delete state.charts['runGraph'];
  }
  const chart = ensureChart('runGraph');
  const textColor = chartTextColor();
  const isDark = isDarkMode();

  const labelRun = t('personality.cat.run');
  const labelGene = t('personality.cat.gene');
  const labelEvent = t('personality.cat.event');
  const nodes = [{ id: 'Run', name: labelRun + '\\n' + run.runId.slice(-8), symbolSize: 56, itemStyle: { color: '#3274d9' }, category: 0 }];
  const edges = [];
  const categories = [
    { name: labelRun },
    { name: labelGene },
    { name: t('personality.cat.signal') },
    { name: labelEvent },
    { name: t('personality.cat.asset') },
  ];

  if (run.selectedGeneId) {
    nodes.push({ id: 'Gene', name: labelGene + '\\n' + run.selectedGeneId.replace('gene_gep_', ''), symbolSize: 44, itemStyle: { color: '#28a745' }, category: 1 });
    edges.push({ source: 'Run', target: 'Gene' });
  }
  (detail.signals || []).slice(0, 6).forEach((sig, i) => {
    const id = 'Sig' + i;
    nodes.push({ id, name: sig, symbolSize: 30, itemStyle: { color: '#ffc107' }, category: 2 });
    edges.push({ source: id, target: 'Run' });
    if (run.selectedGeneId) edges.push({ source: id, target: 'Gene', lineStyle: { type: 'dashed' } });
  });
  (run.evidence || []).slice(0, 5).forEach((ev, i) => {
    const id = 'Ev' + i;
    nodes.push({ id, name: labelEvent + '\\n' + (ev.id || '').slice(-6), symbolSize: 28, itemStyle: { color: '#dc3545' }, category: 3 });
    edges.push({ source: 'Run', target: id });
  });
  (run.assets || []).slice(0, 5).forEach((a, i) => {
    const id = 'Ast' + i;
    nodes.push({ id, name: a.action || 'asset', symbolSize: 26, itemStyle: { color: '#6f42c1' }, category: 4 });
    edges.push({ source: 'Run', target: id });
  });

  chart.setOption({
    tooltip: {},
    legend: { data: categories.map(c => c.name), bottom: 0, textStyle: { color: textColor } },
    series: [{
      type: 'graph',
      layout: 'force',
      data: nodes,
      links: edges,
      categories,
      roam: true,
      draggable: true,
      cursor: 'grab',
      label: { show: true, color: textColor, fontSize: 10 },
      lineStyle: { color: isDark ? '#5c6975' : '#cdd3da', width: 1.5, curveness: 0.15 },
      force: { repulsion: 220, edgeLength: 90 },
    }],
  });
}

async function loadRun(runId) {
  state.selectedRunId = runId;
  $('run-detail').innerHTML = '<p class="muted">' + esc(t('pipelines.runs.loadingTrace')) + '</p>';
  try {
    const run = await api('/webui/runs/' + encodeURIComponent(runId));
    renderRunDetail(run);
  } catch (err) {
    $('run-detail').innerHTML = '<p class="status-failed">' + esc(t('pipelines.runs.failedToLoad')) + esc(err.message) + '</p>';
  }
}

async function loadPipelines() {
  try {
    const runs = await api('/webui/runs?limit=50');
    renderRuns(runs);
  } catch (err) {
    console.error(err);
  }
}
`;
