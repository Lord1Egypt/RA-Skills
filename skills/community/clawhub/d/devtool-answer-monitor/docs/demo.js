const state = {
  data: null,
  projectId: 'mineru',
  runId: 'baseline',
};

const metricLabels = {
  mention_rate: 'Mention rate',
  positive_mention_rate: 'Positive mention rate',
  capability_accuracy: 'Capability accuracy',
  ecosystem_accuracy: 'Ecosystem accuracy',
};

const percent = (value) => `${Number(value).toFixed(2)}%`;

function getProject() {
  return state.data.projects.find((project) => project.id === state.projectId);
}

function getRun() {
  const project = getProject();
  return project.runs.find((run) => run.id === state.runId) || project.runs[0];
}

function renderTabs() {
  const projectTabs = document.getElementById('project-tabs');
  const runTabs = document.getElementById('run-tabs');
  const project = getProject();

  projectTabs.innerHTML = state.data.projects.map((item) => `
    <button class="tab ${item.id === state.projectId ? 'is-active' : ''}" data-project="${item.id}">${item.name}</button>
  `).join('');

  runTabs.innerHTML = project.runs.map((item) => `
    <button class="tab ${item.id === state.runId ? 'is-active' : ''}" data-run="${item.id}">${item.label}</button>
  `).join('');

  projectTabs.querySelectorAll('[data-project]').forEach((button) => {
    button.addEventListener('click', () => {
      state.projectId = button.dataset.project;
      state.runId = getProject().runs[0].id;
      render();
    });
  });

  runTabs.querySelectorAll('[data-run]').forEach((button) => {
    button.addEventListener('click', () => {
      state.runId = button.dataset.run;
      render();
    });
  });
}

function renderHeadline() {
  const project = getProject();
  const run = getRun();
  document.getElementById('headline').innerHTML = `
    <h2>${project.headline.title}: ${project.name} / ${run.label}</h2>
    <p>${project.headline.body}</p>
  `;
}

function renderMetrics() {
  const project = getProject();
  const run = getRun();
  const baseline = project.runs[0];
  const cards = Object.entries(run.metrics).map(([key, value]) => {
    const baselineValue = baseline.metrics[key];
    const delta = Number(value) - Number(baselineValue);
    const deltaLabel = run.id === baseline.id ? 'baseline view' : `${delta >= 0 ? '+' : ''}${delta.toFixed(2)} pts vs baseline`;
    const deltaClass = run.id === baseline.id || Math.abs(delta) < 0.01
      ? 'neutral'
      : (delta > 0 ? 'positive' : 'negative');
    return `
      <article class="metric-card card">
        <h3>${metricLabels[key]}</h3>
        <div class="metric-value">${percent(value)}</div>
        <div class="metric-delta ${deltaClass}">${deltaLabel}</div>
      </article>
    `;
  }).join('');
  document.getElementById('metrics-grid').innerHTML = cards;
}

function renderStages() {
  const run = getRun();
  document.getElementById('stage-caption').textContent = `${run.record_count} sample records · ${run.source}`;
  const stages = run.by_funnel_stage || [];
  document.getElementById('stage-list').innerHTML = stages.length ? stages.map((stage) => {
    const positive = stage.positive_mention_rate ?? 0;
    return `
      <section class="stage-row">
        <header>
          <h3>${stage.funnel_stage}</h3>
          <span>${percent(stage.mention_rate)}</span>
        </header>
        <div class="bar-track"><div class="bar-fill" style="width:${positive}%"></div></div>
        <p class="panel-label">Positive mention: ${stage.positive_mention_rate == null ? 'NA' : percent(stage.positive_mention_rate)} · Capability: ${stage.capability_accuracy == null ? 'NA' : percent(stage.capability_accuracy)} · Ecosystem: ${stage.ecosystem_accuracy == null ? 'NA' : percent(stage.ecosystem_accuracy)}</p>
      </section>
    `;
  }).join('') : '<p class="panel-label">No funnel-stage slices were captured for this sample run.</p>';
}

function renderRepairList() {
  const run = getRun();
  const items = run.repair_candidates.length
    ? run.repair_candidates.map((item) => `
        <div class="repair-item">
          <div>
            <strong>${item.query_id}</strong>
            <p class="panel-label">Model: ${item.model_id}</p>
          </div>
          <span class="badge">${item.repair_type.replace(/_/g, ' ')}</span>
        </div>
      `).join('')
    : '<p class="panel-label">No open repair candidates in this sample summary.</p>';
  document.getElementById('repair-list').innerHTML = items;
}

function render() {
  renderTabs();
  renderHeadline();
  renderMetrics();
  renderStages();
  renderRepairList();
}

fetch('data/demo-metrics.json')
  .then((response) => response.json())
  .then((data) => {
    state.data = data;
    render();
  })
  .catch((error) => {
    document.querySelector('.shell').innerHTML = `<section class="card"><h1>Demo data failed to load</h1><p>${error.message}</p></section>`;
  });
