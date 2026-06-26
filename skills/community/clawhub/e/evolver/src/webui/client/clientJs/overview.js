'use strict';

exports.overviewJs = `
function renderStatus(status) {
  const lastRun = status.lastRun || {};
  $('status').innerHTML = kv([
    [t('overview.status.mode'), status.mode],
    [t('overview.status.proxy'), status.proxy?.running ? t('common.running') : t('common.notRunning')],
    [t('overview.status.heartbeat'), status.heartbeat?.phase || t('common.idle')],
    [t('overview.status.lastRun'), lastRun.run_id || '-'],
    [t('overview.status.lastActivity'), formatTime(lastRun.finished_at || lastRun.created_at)],
  ]);
}

function renderSafety(safety) {
  const warnings = safety.warnings?.length
    ? '<ul style="margin-top:8px;padding-left:20px;color:var(--warning)">' + safety.warnings.map((w) => '<li>' + esc(w) + '</li>').join('') + '</ul>'
    : '<p style="margin-top:8px;color:var(--success)">' + esc(t('overview.safety.noWarnings')) + '</p>';
  $('safety').innerHTML = '<div style="margin-bottom:8px"><span class="status-indicator ' + (safety.safeMode ? 'status-success' : 'status-warning') + '"></span><strong>' + esc(safety.safeMode ? t('overview.safety.safeMode') : t('overview.safety.reviewRequired')) + '</strong></div>' + kv([
    [t('overview.safety.autobuy'), safety.autobuyEnabled],
    [t('overview.safety.autoPublish'), safety.autoPublishEnabled],
    [t('overview.safety.validator'), safety.validatorEnabled],
    [t('overview.safety.traceLevel'), safety.traceLevel],
  ]) + warnings;
}

function renderInteractions(interactions) {
  $('interactions').innerHTML = kv([
    [t('overview.interactions.proxy'), interactions.proxy?.running ? interactions.proxy.url : t('common.notRunning')],
    [t('overview.interactions.mailbox'), interactions.mailbox?.pagination?.totalItems || 0],
    [t('overview.interactions.taskMetrics'), interactions.proxySnapshots?.taskMetrics?.ok ? t('common.available') : t('common.notAvailable')],
    [t('overview.interactions.sessions'), interactions.proxySnapshots?.sessions?.ok ? t('common.available') : t('common.notAvailable')],
  ]);
}

function renderOverviewCharts(assets) {
  const isDark = isDarkMode();
  const textColor = chartTextColor();
  const palette = ['#3274d9', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#17a2b8'];

  ensureChart('genesChart')?.setOption({
    color: palette,
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, textStyle: { color: textColor } },
    series: [{
      type: 'pie',
      radius: ['45%', '72%'],
      itemStyle: { borderRadius: 4, borderColor: isDark ? '#181b1f' : '#fff', borderWidth: 2 },
      label: { show: false },
      labelLine: { show: false },
      data: Object.entries(assets.genesByCategory || {}).map(([name, value]) => ({ name, value })),
    }],
  });

  const capsules = Object.entries(assets.capsulesByOutcome || {});
  ensureChart('capsulesChart')?.setOption({
    color: palette,
    tooltip: { trigger: 'item' },
    legend: { bottom: 0, textStyle: { color: textColor } },
    series: [{
      type: 'pie',
      radius: ['45%', '72%'],
      itemStyle: { borderRadius: 4, borderColor: isDark ? '#181b1f' : '#fff', borderWidth: 2 },
      label: { show: false },
      labelLine: { show: false },
      data: capsules.length ? capsules.map(([name, value]) => ({ name, value })) : [{ name: 'no capsules yet', value: 1, itemStyle: { color: '#444' } }],
    }],
  });

  const calls = Object.entries(assets.assetCallsByAction || {});
  ensureChart('callsChart')?.setOption({
    color: palette,
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { left: '3%', right: '4%', bottom: '5%', containLabel: true },
    xAxis: { type: 'value', splitLine: { lineStyle: { color: isDark ? '#2c3235' : '#e4e7eb' } }, axisLabel: { color: textColor } },
    yAxis: { type: 'category', data: calls.length ? calls.map(d => d[0]) : ['no calls'], axisLabel: { color: textColor } },
    series: [{
      type: 'bar',
      data: calls.length ? calls.map(d => d[1]) : [0],
      itemStyle: { color: '#3274d9', borderRadius: [0, 4, 4, 0] },
    }],
  });
}

function renderLatestRun(runs) {
  const list = runs.data || [];
  if (!list.length) {
    $('latest-run').innerHTML = '<p class="muted">' + esc(t('overview.run.empty')) + '</p>';
    return;
  }
  const run = list[0];
  // Build the <dl> manually: only the Status value contains real HTML
  // (the status-indicator span); other values are plain text and go
  // through esc(). Avoids the kv()+partial-replace dance that left
  // &quot; / &gt; un-restored and broke the indicator render. Cursor
  // Bugbot Medium-severity finding on PR #532 -- see test guard for
  // 'kv-then-partial-replace antipattern' in test/webuiServer.test.js.
  const rows = [
    [t('overview.run.id'), esc(run.runId)],
    [t('overview.run.status'), '<span class="status-indicator ' + getStatusClass(run.status) + '"></span>' + esc(tStatus(run.status))],
    [t('overview.run.selectedGene'), esc(run.selectedGeneId || '-')],
    [t('overview.run.validation'), esc(validationDisplay(run))],
    [t('overview.run.updated'), esc(formatTime(run.updatedAt))],
    [t('overview.run.requiresConfirmation'), run.requiresConfirmation ? t('common.yes') : t('common.no')],
  ];
  $('latest-run').innerHTML = '<dl>' +
    rows.map(([k, v]) => '<dt>' + esc(k) + '</dt><dd>' + v + '</dd>').join('') +
    '</dl>';
}

function validationDisplay(run) {
  if (run.validationResult === 'pass') return t('overview.validation.pass');
  if (run.validationResult === 'fail') return t('overview.validation.fail');
  if (run.status === 'review_pending') return t('overview.validation.pendingReview');
  if (run.status === 'running' || run.status === 'pending') return t('overview.validation.inProgress');
  if (run.status === 'failed') return t('overview.validation.notRun');
  return t('overview.validation.notRun');
}

function renderSkills(skills) {
  if (!skills.exists || !skills.items.length) {
    $('skills').innerHTML = '<p class="muted">' + esc(t('overview.skills.empty')) + '</p>' +
      '<p class="muted small">' + t('overview.skills.hint') + '</p>';
    return;
  }
  $('skills').innerHTML = '<ul class="skill-list">' + skills.items.map((skill) =>
    '<li><strong>' + esc(skill.name) + '</strong>' +
    (skill.description ? '<p>' + esc(skill.description) + '</p>' : '') +
    '<small class="muted">' + skill.fileCount + ' ' + esc(t('overview.skills.files')) + ' · ' + esc(skill.docFile || t('overview.skills.noDoc')) + '</small></li>'
  ).join('') + '</ul>';
}

async function loadOverview() {
  try {
    const [status, runs, assets, interactions, skills] = await Promise.all([
      api('/webui/status'),
      api('/webui/runs?limit=20'),
      api('/webui/assets'),
      api('/webui/interactions?limit=20'),
      api('/webui/skills'),
    ]);
    renderStatus(status);
    renderSafety(status.safety || {});
    renderInteractions(interactions);
    renderOverviewCharts(assets);
    renderLatestRun(runs);
    renderSkills(skills);
  } catch (err) {
    console.error(err);
  }
}
`;
