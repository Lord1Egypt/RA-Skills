'use strict';

// Brand mark — same 256x256 PNG that ships in evomap/evox-desktop
// (frontend/src/assets/logo.png), inlined as data: URI so the dashboard
// stays self-contained (no extra HTTP route, no build step). Original
// file is 1077 bytes; base64-encoded payload is ~1.4 KB.
const LOGO_DATA_URI = 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAD/ElEQVR42u3UoQEDMQwEwUcJUP/NPlGqCNEOmAZs3T6f7yzQ9HgEEABAAAABAAQAEABAAAABAAQAEABAAAABAAQAEABAAAABAAQAEABAAAABAAQAEABAAAABAAQAEABAAAABAAQAEABAAAABAAQAEABAAAABOO5937/wtgJAYOjCIAAYuygIAAYvCAKA0YuBAGD0YiAAGL4QCABGLwYCgOELgQBg+EIgABi+EAiA4SMEAmD4CIEAGD8iIACGjxAIgPEjAgJg+AiBABg/IiAAho8QCIDxIwICYPyIgAAYPyIgAIaPEAiA8SMCAmD8iIAAGD8iIADGjwgIgPEjAgJg/IiAABg/IiAAxo8ICIDxIwIC4KgRgGYAHDQiEA2AQ0YEogFwwIhANAAOFxEQABCAWgAcLCIQDYBDRQQEAASgFgAHighEA+AwEQEBAAGoBcBBIgLRADhEREAAQABqAXCAiIAAgADUAuDwEAEBAAGoBcDBIQICAAJQC4BDQwQEAASgFgAHhggIAAiAAIAAZALgsBABAQABqAXAQSECAgACIAAgAJkAOCREQABAAAQABCATAAeECAgACIAAgAAIAAjA/QA4HERAAEAABAAEQABAAAQABOBwABwMIiAAIAACAAIgACAAAgACIAAgABcD4FAQAQEAARAAEAABAAEQABAAAQABEAAQAAEAARAAEAABAAEQABAAAQABEAAQAAEAARAAEAABAAEQABAAAQABEAAQAAEAARAAEAABAAEQAbg1fgEAARAAEAABAAEQABAAAQABEAG4On4BAAEQABAAAQABEAAQABGA4+MXABAAAQABEAAQABGAxvgFAARAAEAARABS4xcAEAABAAEQAUiNXwBAAGZFAHrjFwAQAAEAARABSI1fAEAAZkUAeuMXABCAWRGA3vgFAARgVgSgN34BAAGYFQHojV8AQABmRQB64z8TABHA+AUABKAaABHA+OMBEAGMXwBAAKoBEAGMPx4AEcD4BQAEoBoAEcD44wEQAYw/HgARwPjjARABjF8AQACqARABjD8eABHA+OMBEAGMPx4AEcD44wEQAerjzwdABKjffz4AImD8AoBBGL8AiIBhGL8ACIGRGL4AiADGLwAigPELgAhg/AIgBBi+AIgAxi8AQoDhC4AIYPwCIAQYvgCIAMYvAEKA4QuAEGD4AiAEGL4ACAGGLwBCgOELgBhg9AIgBIaPAGD0CAAnY+BPBYBQEPyZABCJgr8QAAJh8LYCAAgAIACAAAACAAgAIACAAAACAAgAIACAAAACAAgAIACAAAACAAgAIACAAAACAAgAIACAAAACAAgAIACAAAACAAgAIAAgAIAAAAIACAAgAMBVP0So0nvkC/TPAAAAAElFTkSuQmCC';

// Inline lucide-style SVG icons (24x24, currentColor stroke).
const ICONS = {
  layout: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="9" x="3" y="3" rx="1"/><rect width="7" height="5" x="14" y="3" rx="1"/><rect width="7" height="9" x="14" y="12" rx="1"/><rect width="7" height="5" x="3" y="16" rx="1"/></svg>',
  pipeline: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="6" x2="6" y1="3" y2="15"/><circle cx="18" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M18 9a9 9 0 0 1-9 9"/></svg>',
  package: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m7.5 4.27 9 5.15"/><path d="M21 8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16Z"/><path d="m3.3 7 8.7 5 8.7-5"/><path d="M12 22V12"/></svg>',
  activity: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-2.48a2 2 0 0 0-1.93 1.46l-2.35 8.36a.5.5 0 0 1-.96 0L9.68 3.18a.5.5 0 0 0-.96 0l-2.35 8.36A2 2 0 0 1 4.44 13H2"/></svg>',
  brain: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 5a3 3 0 1 0-5.997.125 4 4 0 0 0-2.526 5.77 4 4 0 0 0 .556 6.588A4 4 0 1 0 12 18Z"/><path d="M12 5a3 3 0 1 1 5.997.125 4 4 0 0 1 2.526 5.77 4 4 0 0 1-.556 6.588A4 4 0 1 1 12 18Z"/><path d="M15 13a4.5 4.5 0 0 1-3-4 4.5 4.5 0 0 1-3 4"/></svg>',
  refresh: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 12a9 9 0 0 1 9-9 9.75 9.75 0 0 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/><path d="M21 12a9 9 0 0 1-9 9 9.75 9.75 0 0 1-6.74-2.74L3 16"/><path d="M8 16H3v5"/></svg>',
  sun: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2"/><path d="M12 20v2"/><path d="m4.93 4.93 1.41 1.41"/><path d="m17.66 17.66 1.41 1.41"/><path d="M2 12h2"/><path d="M20 12h2"/><path d="m6.34 17.66-1.41 1.41"/><path d="m19.07 4.93-1.41 1.41"/></svg>',
  moon: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9Z"/></svg>',
};

// Sidebar items reference an i18n key; the live label is rendered by
// applyI18nDom() based on current locale.
const NAV = [
  { tab: 'overview',     icon: 'layout',   labelKey: 'nav.overview' },
  { tab: 'pipelines',    icon: 'pipeline', labelKey: 'nav.pipelines' },
  { tab: 'assets',       icon: 'package',  labelKey: 'nav.assets' },
  { tab: 'interactions', icon: 'activity', labelKey: 'nav.interactions' },
  { tab: 'personality',  icon: 'brain',    labelKey: 'nav.personality' },
];

function navItem({ tab, icon, labelKey }, idx) {
  const active = idx === 0 ? ' active' : '';
  return `<button class="tab nav-item${active}" data-tab="${tab}">
        <span class="nav-icon">${ICONS[icon]}</span>
        <span class="nav-label" data-i18n="${labelKey}">${labelKey}</span>
      </button>`;
}

// Pre-CSS theme bootstrap. Runs synchronously in <head> so the chosen
// theme class is set on <html> *before* the stylesheet evaluates, which
// avoids a flash of the wrong palette on first paint. Reads
// localStorage 'evolver-theme' (light|dark|system, default system) and
// adds .dark to <html> if appropriate.
const THEME_INIT_SCRIPT = `(function(){try{
  var saved = localStorage.getItem('evolver-theme') || 'system';
  var dark = saved === 'dark' || (saved === 'system' && window.matchMedia('(prefers-color-scheme: dark)').matches);
  if (dark) document.documentElement.classList.add('dark');
}catch(_){}})()`;

// Pre-CSS locale bootstrap. Sets <html lang> + data-locale before paint
// so server-rendered static text doesn't flash English when a Chinese
// preference is stored. Defaults to English; switches to zh only when
// explicitly chosen.
const LOCALE_INIT_SCRIPT = `(function(){try{
  var saved = localStorage.getItem('evolver-locale') || 'en';
  if (saved !== 'en' && saved !== 'zh') saved = 'en';
  document.documentElement.setAttribute('data-locale', saved);
  document.documentElement.lang = saved === 'zh' ? 'zh-CN' : 'en';
}catch(_){}})()`;

function getIndexHtml() {
  return `<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Evolver Web UI</title>
  <script>${THEME_INIT_SCRIPT}</script>
  <script>${LOCALE_INIT_SCRIPT}</script>
  <link rel="stylesheet" href="/app.css">
  <script src="/vendor/echarts.min.js"></script>
</head>
<body class="app-atmosphere">
  <div class="shell">
    <aside class="sidebar">
      <div class="brand">
        <img class="brand-mark" src="${LOGO_DATA_URI}" alt="Evolver" draggable="false" />
        <div class="brand-text">
          <span class="brand-title">Evolver</span>
          <span class="brand-eyebrow" data-i18n="brand.eyebrow">local agent</span>
        </div>
      </div>
      <nav class="nav">
        ${NAV.map(navItem).join('\n        ')}
      </nav>
      <div class="sidebar-spacer"></div>
      <div class="sidebar-footer">v1.80 · <span data-i18n="sidebar.footer">evolves with you</span></div>
    </aside>

    <div class="main-col">
      <header class="topbar">
        <div class="topbar-left">
          <h1 class="topbar-title" id="topbar-title" data-i18n="nav.overview">Overview</h1>
          <p class="topbar-eyebrow" data-i18n="topbar.eyebrow">EvoMap Evolver · Web UI Observability</p>
        </div>
        <div class="topbar-actions">
          <button id="locale-toggle" class="btn-icon btn-locale" data-i18n-attr-title="btn.locale.title" data-i18n-attr-aria-label="btn.locale.title" title="Switch language (EN / 中)" aria-label="Switch language">
            <span class="locale-glyph">EN</span>
          </button>
          <button id="theme-toggle" class="btn-icon" data-i18n-attr-title="btn.theme.title" data-i18n-attr-aria-label="btn.theme.title" title="Toggle light / dark theme" aria-label="Toggle theme">
            <span class="theme-icon theme-icon-sun">${ICONS.sun}</span>
            <span class="theme-icon theme-icon-moon">${ICONS.moon}</span>
          </button>
          <button id="refresh" class="btn-ghost" data-i18n-attr-title="btn.refresh.title" title="Refresh all data">
            <span class="nav-icon">${ICONS.refresh}</span>
            <span data-i18n="btn.refresh">Refresh</span>
          </button>
        </div>
      </header>

      <main class="content evox-scroll">
        <section data-view="overview" class="view active">
          <div class="grid-top">
            <div class="card"><h2 data-i18n="overview.card.status">Status</h2><div id="status" data-i18n="common.loading">Loading...</div></div>
            <div class="card"><h2 data-i18n="overview.card.safety">Safety</h2><div id="safety" data-i18n="common.loading">Loading...</div></div>
            <div class="card"><h2 data-i18n="overview.card.interactions">Interactions</h2><div id="interactions" data-i18n="common.loading">Loading...</div></div>
          </div>
          <div class="grid-charts">
            <div class="card"><h2 data-i18n="overview.card.genesByCategory">Genes by Category</h2><div id="genesChart" class="chart-container"></div></div>
            <div class="card"><h2 data-i18n="overview.card.capsulesByOutcome">Capsules by Outcome</h2><div id="capsulesChart" class="chart-container"></div></div>
            <div class="card"><h2 data-i18n="overview.card.assetCalls">Asset Calls</h2><div id="callsChart" class="chart-container"></div></div>
          </div>
          <div class="grid-bottom">
            <div class="card">
              <h2 data-i18n="overview.card.latestRun">Latest Pipeline Run</h2>
              <div id="latest-run" data-i18n="common.loading">Loading...</div>
            </div>
            <div class="card">
              <h2 data-i18n="overview.card.skills">Skills</h2>
              <div id="skills" data-i18n="common.loading">Loading...</div>
            </div>
          </div>
        </section>

        <section data-view="pipelines" class="view">
          <div class="card">
            <h2 data-i18n="pipelines.card.scoreTrend">Score Trend</h2>
            <div id="scoreTrendChart" class="chart-container"></div>
          </div>
          <div class="grid-bottom">
            <div class="card">
              <h2 data-i18n="pipelines.card.runs">Pipeline Runs</h2>
              <div class="table-wrapper">
                <table id="runsTable">
                  <thead><tr><th data-i18n="pipelines.col.runId">Run ID</th><th data-i18n="pipelines.col.status">Status</th><th data-i18n="pipelines.col.gene">Gene</th><th data-i18n="pipelines.col.score">Score</th><th data-i18n="pipelines.col.updated">Updated</th></tr></thead>
                  <tbody></tbody>
                </table>
              </div>
            </div>
            <div class="card">
              <h2 data-i18n="pipelines.card.runTrace">Run Trace</h2>
              <div id="run-detail"><p class="muted" data-i18n="pipelines.runs.selectHint">Select a run to inspect its trace.</p></div>
            </div>
          </div>
        </section>

        <section data-view="assets" class="view">
          <div class="asset-tabs">
            <button class="asset-tab active" data-asset="genes" data-i18n="assets.tab.genes">Genes</button>
            <button class="asset-tab" data-asset="capsules" data-i18n="assets.tab.capsules">Capsules</button>
            <button class="asset-tab" data-asset="events" data-i18n="assets.tab.events">Events</button>
            <button class="asset-tab" data-asset="candidates" data-i18n="assets.tab.candidates">Candidates</button>
            <button class="asset-tab" data-asset="calls" data-i18n="assets.tab.calls">Asset Calls</button>
          </div>
          <div class="card">
            <div id="asset-list" data-i18n="common.loading">Loading...</div>
          </div>
        </section>

        <section data-view="interactions" class="view">
          <div class="grid-charts">
            <div class="card"><h2 data-i18n="interactions.card.hubByAction">Hub A2A by Action</h2><div id="hubActionChart" class="chart-container"></div></div>
            <div class="card"><h2 data-i18n="interactions.card.activity30d">Activity (last 30 days)</h2><div id="activityChart" class="chart-container"></div></div>
            <div class="card"><h2 data-i18n="interactions.card.mailboxByType">Mailbox by Type</h2><div id="mailboxChart" class="chart-container"></div></div>
          </div>
          <div class="card">
            <h2 data-i18n="interactions.card.hubActivity">Hub Activity</h2>
            <p class="muted small card-sub" data-i18n="interactions.card.hubActivity.desc">Unified timeline of every Hub interaction — connection lifecycle (hello/heartbeat/fetch), asset calls (search/reuse/publish) and ATP credit flows.</p>
            <div id="hub-activity-summary" class="lifecycle-summary" data-i18n="common.loading">Loading...</div>
            <div class="filter-bar" id="hub-activity-filters" style="display:none">
              <div class="filter-group">
                <span class="filter-label" data-i18n="interactions.filter.layer">Layer</span>
                <button class="filter-pill active" data-filter-layer="all" data-i18n="interactions.filter.all">All</button>
                <button class="filter-pill" data-filter-layer="lifecycle" data-i18n="interactions.filter.lifecycle">Lifecycle</button>
                <button class="filter-pill" data-filter-layer="asset" data-i18n="interactions.filter.asset">Asset</button>
                <button class="filter-pill" data-filter-layer="atp" data-i18n="interactions.filter.atp">ATP</button>
              </div>
              <label class="filter-toggle"><input type="checkbox" id="hide-heartbeats" checked /> <span data-i18n="interactions.filter.hideHeartbeats">Hide heartbeats</span></label>
            </div>
            <div id="hub-activity" data-i18n="common.loading">Loading...</div>
          </div>
          <div class="card">
            <h2 data-i18n="interactions.card.agent">Agent Interactions</h2>
            <p class="muted small card-sub" data-i18n="interactions.card.agent.desc">Mailbox messages, sessions and DMs (read-only, redacted).</p>
            <div id="agent-stream" data-i18n="common.loading">Loading...</div>
          </div>
          <div class="card">
            <h2 data-i18n="interactions.card.proxySnapshots">Proxy Snapshots</h2>
            <div id="proxy-snapshots" class="snapshot-grid" data-i18n="common.loading">Loading...</div>
          </div>
        </section>

        <section data-view="personality" class="view">
          <div class="grid-charts">
            <div class="card"><h2 data-i18n="personality.card.traits">Personality Traits</h2><div id="personalityChart" class="chart-container chart-tall"></div></div>
            <div class="card"><h2 data-i18n="personality.card.detail">Personality Detail</h2><div id="personality-detail" data-i18n="common.loading">Loading...</div></div>
          </div>
          <div class="card">
            <h2 data-i18n="personality.card.memoryGraph">Memory Graph (last 100 events)</h2>
            <div id="memory-graph-chart" class="chart-container chart-xl"></div>
          </div>
        </section>
      </main>
    </div>
  </div>
  <script src="/app.js"></script>
</body>
</html>`;
}

module.exports = { getIndexHtml };
