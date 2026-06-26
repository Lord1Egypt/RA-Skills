'use strict';

function getStylesCss() {
  return `
/* ===========================================================
 * Theme — HSL CSS variables, palette ported from
 * evomap/evox-desktop/frontend/src/styles.css so the read-only
 * Evolver dashboard shares the same visual language as the
 * Wails desktop app.
 * ----------------------------------------------------------- */
:root {
  --background: 0 0% 100%;
  --foreground: 0 0% 9%;
  --card: 0 0% 100%;
  --card-foreground: 0 0% 9%;
  --popover: 0 0% 100%;
  --popover-foreground: 0 0% 9%;
  --primary: 240 5.9% 10%;
  --primary-foreground: 0 0% 98%;
  --secondary: 240 5% 94%;
  --secondary-foreground: 240 5.9% 10%;
  --muted: 240 5% 94%;
  --muted-foreground: 240 3.8% 42%;
  --accent: 217 91% 60%;
  --accent-foreground: 0 0% 98%;
  --destructive: 0 72% 50%;
  --destructive-foreground: 0 0% 98%;
  --success: 142 71% 38%;
  --warning: 38 95% 50%;
  --border: 240 5.9% 87%;
  --input: 240 5.9% 87%;
  --ring: 240 5.9% 10%;
  --radius: 0.75rem;
}
/* Dark theme — applied when <html> has the .dark class. The class is
 * set synchronously in <head> by THEME_INIT_SCRIPT (see indexHtml.js)
 * before the stylesheet evaluates, so there is no flash of the wrong
 * palette on first paint. Selection is class-based (not @media) so the
 * topbar toggle can override the OS preference at runtime. */
.dark {
  --background: 0 0% 4%;
  --foreground: 0 0% 98%;
  --card: 0 0% 6%;
  --card-foreground: 0 0% 98%;
  --popover: 0 0% 6%;
  --popover-foreground: 0 0% 98%;
  --primary: 0 0% 98%;
  --primary-foreground: 240 5.9% 10%;
  --secondary: 0 0% 12%;
  --secondary-foreground: 0 0% 98%;
  --muted: 0 0% 12%;
  --muted-foreground: 240 5% 64.9%;
  --accent: 217 91% 65%;
  --accent-foreground: 240 5.9% 10%;
  --destructive: 0 62.8% 50%;
  --destructive-foreground: 0 0% 98%;
  --success: 142 60% 45%;
  --warning: 38 95% 56%;
  --border: 0 0% 14%;
  --input: 0 0% 14%;
  --ring: 0 0% 83.1%;
}

/* ===========================================================
 * Base
 * ----------------------------------------------------------- */
* { box-sizing: border-box; }
html, body { height: 100%; margin: 0; }
body {
  font-family: "Inter", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif, "Apple Color Emoji";
  font-size: 14px;
  line-height: 1.5;
  color: hsl(var(--foreground));
  background: hsl(var(--background));
  font-feature-settings: "cv02", "cv03", "cv04", "cv11";
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
::selection { background: hsl(var(--primary) / 0.3); color: inherit; }
code, pre, .mono { font-family: "JetBrains Mono", "SFMono-Regular", Menlo, Consolas, monospace; }

/* Atmosphere — single soft radial gradient, lifted from evox-desktop. */
.app-atmosphere::before {
  content: "";
  position: fixed; inset: 0;
  pointer-events: none;
  z-index: 0;
  background: radial-gradient(ellipse 80% 80% at 50% -20%, rgba(120, 119, 198, 0.10), rgba(255, 255, 255, 0) 60%);
}
.dark .app-atmosphere::before {
  background: radial-gradient(ellipse 80% 80% at 50% -20%, rgba(99, 102, 241, 0.08), rgba(0, 0, 0, 0) 60%);
}

/* Thin scrollbar (only inside .evox-scroll containers). */
.evox-scroll::-webkit-scrollbar { width: 8px; height: 8px; }
.evox-scroll::-webkit-scrollbar-track { background: transparent; }
.evox-scroll::-webkit-scrollbar-thumb {
  background: hsl(var(--muted-foreground) / 0.3);
  border-radius: 10px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
.evox-scroll::-webkit-scrollbar-thumb:hover {
  background: hsl(var(--muted-foreground) / 0.5);
}

/* ===========================================================
 * App shell — sidebar (240) + main column
 * ----------------------------------------------------------- */
.shell {
  position: relative;
  z-index: 1;
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  width: 240px;
  flex-shrink: 0;
  border-right: 1px solid hsl(var(--border) / 0.6);
  background: hsl(var(--background) / 0.7);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  padding: 8px 0 0 0;
}

/* Brand: gradient mark + title + uppercase eyebrow. */
.brand {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px 12px 20px;
}
.brand-mark {
  width: 56px; height: 56px;
  border-radius: 16px;
  display: block;
  object-fit: cover;
  box-shadow: 0 6px 20px rgba(0,0,0,0.14), inset 0 0 0 1px rgba(0,0,0,0.10);
  user-select: none;
}
.dark .brand-mark {
  box-shadow: 0 6px 20px rgba(0,0,0,0.36), inset 0 0 0 1px rgba(255,255,255,0.10);
}
.brand-text { display: flex; flex-direction: column; line-height: 1.1; }
.brand-title { font-size: 15px; font-weight: 600; letter-spacing: -0.01em; color: hsl(var(--foreground)); }
.brand-eyebrow {
  margin-top: 4px;
  font-size: 10px; font-weight: 500;
  text-transform: uppercase; letter-spacing: 0.2em;
  color: hsl(var(--muted-foreground));
}

.nav { display: flex; flex-direction: column; gap: 2px; padding: 8px 12px 12px 12px; }
.nav-item {
  display: flex; align-items: center; gap: 12px;
  padding: 8px 12px;
  font-size: 13px; font-weight: 500;
  color: hsl(var(--muted-foreground));
  background: transparent;
  border: 0;
  border-radius: 8px;
  cursor: pointer;
  text-align: left;
  transition: background-color 150ms, color 150ms, box-shadow 150ms;
}
.nav-item:hover {
  color: hsl(var(--foreground));
  background: hsl(var(--foreground) / 0.05);
}
/* Active nav uses an accent-tinted background so the brand color
 * dominates and any radial-atmosphere bleed through the translucent
 * sidebar (the previous "pinkish" wash) is overridden. */
.nav-item.active {
  color: hsl(var(--accent));
  background: hsl(var(--accent) / 0.10);
  box-shadow: inset 0 0 0 1px hsl(var(--accent) / 0.18);
}
.nav-item.active .nav-icon { color: hsl(var(--accent)); opacity: 1; }
.nav-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 16px; height: 16px;
  opacity: 0.65;
  transition: opacity 150ms;
}
.nav-item.active .nav-icon, .nav-item:hover .nav-icon { opacity: 0.95; }
.nav-icon svg { width: 16px; height: 16px; }

.sidebar-spacer { flex: 1 1 auto; min-height: 0; }
.sidebar-footer {
  padding: 12px 20px;
  font-size: 10px; font-weight: 500;
  letter-spacing: 0.06em;
  color: hsl(var(--muted-foreground) / 0.7);
  truncate: ellipsis;
}

/* ===========================================================
 * Top bar (page title + actions)
 * ----------------------------------------------------------- */
.main-col { flex: 1 1 auto; display: flex; flex-direction: column; min-width: 0; overflow: hidden; }
.topbar {
  display: flex; align-items: center; justify-content: space-between;
  height: 64px; flex-shrink: 0;
  padding: 0 24px;
  border-bottom: 1px solid hsl(var(--border) / 0.5);
  background: hsl(var(--background) / 0.8);
  backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
  z-index: 5;
}
.topbar-left { display: flex; flex-direction: column; gap: 2px; }
.topbar-title { margin: 0; font-size: 17px; font-weight: 600; letter-spacing: -0.01em; }
.topbar-eyebrow { margin: 0; font-size: 11px; color: hsl(var(--muted-foreground)); }
.topbar-actions { display: flex; align-items: center; gap: 8px; }

.btn-ghost {
  display: inline-flex; align-items: center; gap: 6px;
  padding: 6px 12px;
  font-size: 13px; font-weight: 500;
  color: hsl(var(--muted-foreground));
  background: hsl(var(--muted) / 0.4);
  border: 1px solid hsl(var(--border) / 0.7);
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 150ms, color 150ms;
}
.btn-ghost:hover {
  color: hsl(var(--foreground));
  background: hsl(var(--foreground) / 0.05);
}
.btn-ghost .nav-icon { opacity: 0.7; }
.btn-ghost:hover .nav-icon { opacity: 1; }

/* Topbar theme toggle. Sun and moon icons are stacked; only one is
 * visible at a time depending on the active theme. The button itself
 * is a flat, square icon-button (28x28) consistent with evox-desktop. */
.btn-icon {
  display: inline-flex; align-items: center; justify-content: center;
  width: 28px; height: 28px;
  color: hsl(var(--muted-foreground) / 0.85);
  background: transparent;
  border: 0;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 150ms, color 150ms;
}
.btn-icon:hover {
  color: hsl(var(--foreground));
  background: hsl(var(--foreground) / 0.05);
}
.btn-icon svg { width: 14px; height: 14px; }
.theme-icon-sun  { display: none; }
.theme-icon-moon { display: inline-flex; }
.dark .theme-icon-sun  { display: inline-flex; }
.dark .theme-icon-moon { display: none; }

/* Locale toggle reuses .btn-icon geometry but renders a 2-character
 * glyph (EN / 中) instead of an SVG. The slightly bumped letter-spacing
 * keeps the Latin variant from looking cramped at 11px. */
.btn-locale .locale-glyph {
  font-size: 11px; font-weight: 600; letter-spacing: 0.04em;
  line-height: 1; color: inherit;
}
[data-locale="zh"] .btn-locale .locale-glyph { font-size: 13px; letter-spacing: 0; }

/* ===========================================================
 * Content + cards
 * ----------------------------------------------------------- */
.content { flex: 1 1 auto; overflow-y: auto; padding: 24px; }

.view { display: none; flex-direction: column; gap: 20px; }
.view.active { display: flex; }

.grid-top    { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.grid-charts { display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: 16px; }
.grid-bottom { display: grid; grid-template-columns: 1fr 2fr; gap: 16px; }
@media (max-width: 1100px) { .grid-bottom { grid-template-columns: 1fr; } }

.card {
  background: hsl(var(--card) / 0.6);
  border: 1px solid hsl(var(--border) / 0.4);
  border-radius: 16px;
  padding: 18px 20px;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
  backdrop-filter: blur(20px); -webkit-backdrop-filter: blur(20px);
}
.card-sub { margin: -6px 0 12px 0; }

h1, h2, h3, h4 { margin: 0; }
h2 {
  font-size: 10px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.2em;
  color: hsl(var(--muted-foreground));
  margin: 0 0 14px 0;
}
h3 { font-size: 14px; font-weight: 600; margin: 0 0 8px 0; }
h4 {
  font-size: 11px; font-weight: 600;
  text-transform: uppercase; letter-spacing: 0.1em;
  color: hsl(var(--muted-foreground));
  margin: 0 0 8px 0;
}

.chart-container { width: 100%; height: 240px; }
.chart-container.chart-tall { height: 320px; }
.chart-container.chart-xl   { height: 480px; }

button { font-family: inherit; font-size: 13px; cursor: pointer; }
code {
  background: hsl(var(--muted) / 0.7);
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.85em;
  color: hsl(var(--foreground));
}
.muted { color: hsl(var(--muted-foreground)); }
.small { font-size: 12px; }

dl { display: grid; grid-template-columns: max-content 1fr; gap: 6px 16px; margin: 0; font-size: 13px; }
dt { color: hsl(var(--muted-foreground)); }
dd { margin: 0; font-weight: 500; word-break: break-all; }

/* ===========================================================
 * Tables
 * ----------------------------------------------------------- */
.table-wrapper { overflow-x: auto; margin: 0 -20px -18px -20px; }
table { width: 100%; border-collapse: collapse; font-size: 13px; }
th, td {
  padding: 10px 20px;
  text-align: left;
  border-bottom: 1px solid hsl(var(--border) / 0.5);
  vertical-align: top;
}
th {
  color: hsl(var(--muted-foreground));
  font-weight: 500;
  background: hsl(var(--muted) / 0.4);
  position: sticky; top: 0;
  font-size: 11px; text-transform: uppercase; letter-spacing: 0.08em;
}
tr:last-child td { border-bottom: none; }
#runsTable tbody tr { transition: background-color 120ms; }
#runsTable tbody tr:hover td { background: hsl(var(--foreground) / 0.04); cursor: pointer; }

.data-table { width: 100%; }
.data-table td details summary { cursor: pointer; color: hsl(var(--accent)); }

/* ===========================================================
 * Status indicators (dot) + colored pills
 * ----------------------------------------------------------- */
.status-indicator {
  display: inline-block; width: 8px; height: 8px;
  border-radius: 50%;
  margin-right: 6px;
  vertical-align: middle;
}
.status-success  { background: hsl(var(--success)); }
.status-running  { background: hsl(var(--accent)); }
.status-failed   { background: hsl(var(--destructive)); }
.status-blocked  { background: hsl(var(--warning)); }
.status-skipped  { background: hsl(var(--muted-foreground)); }
.status-warning  { background: hsl(var(--warning)); }
.status-abandoned { background: color-mix(in srgb, hsl(var(--warning)) 60%, hsl(var(--muted-foreground))); }

.pill {
  display: inline-block;
  padding: 2px 9px;
  border-radius: 999px;
  font-size: 11px; font-weight: 500;
  background: hsl(var(--accent) / 0.12);
  color: hsl(var(--accent));
  margin: 2px 2px 2px 0;
}
.pill.repair    { background: hsl(var(--destructive) / 0.14); color: hsl(var(--destructive)); }
.pill.optimize  { background: hsl(var(--accent) / 0.14);      color: hsl(var(--accent)); }
.pill.innovate  { background: hsl(var(--success) / 0.14);     color: hsl(var(--success)); }
.pill.explore   { background: hsl(var(--warning) / 0.18);     color: hsl(var(--warning)); }
.pill.signal    { background: hsl(var(--warning) / 0.14);     color: hsl(var(--warning)); }
.pill.asset_publish, .pill.asset_publish_skip { background: hsl(var(--success) / 0.14);  color: hsl(var(--success)); }
.pill.hub_search_hit                          { background: hsl(var(--accent) / 0.14);   color: hsl(var(--accent)); }
.pill.asset_reuse, .pill.asset_reference      { background: hsl(265 80% 55% / 0.18);     color: hsl(265 70% 60%); }
.pill.hello     { background: hsl(var(--accent) / 0.16);  color: hsl(var(--accent)); }
.pill.heartbeat { background: hsl(var(--success) / 0.16); color: hsl(var(--success)); }
.pill.fetch     { background: hsl(265 80% 55% / 0.18);    color: hsl(265 70% 60%); }
.pill.lifecycle { background: hsl(var(--accent) / 0.14);  color: hsl(var(--accent)); }
.pill.asset     { background: hsl(38 95% 50% / 0.18);     color: hsl(38 95% 45%); }
.pill.atp       { background: hsl(265 80% 55% / 0.16);    color: hsl(265 70% 60%); }

/* ===========================================================
 * Timeline
 * ----------------------------------------------------------- */
.timeline { list-style: none; padding: 0; margin: 0; position: relative; }
.timeline::before {
  content: ''; position: absolute;
  left: 11px; top: 4px; bottom: 0;
  width: 2px;
  background: hsl(var(--border));
}
.timeline li { position: relative; padding: 0 0 18px 32px; }
.timeline li:last-child { padding-bottom: 0; }
.timeline li::before {
  content: ''; position: absolute;
  left: 6px; top: 4px;
  width: 12px; height: 12px;
  border-radius: 50%;
  background: hsl(var(--card));
  border: 2px solid hsl(var(--border));
  z-index: 1;
}
.timeline li.success::before { border-color: hsl(var(--success));     background: hsl(var(--success)); }
.timeline li.running::before { border-color: hsl(var(--accent));      background: hsl(var(--accent)); }
.timeline li.failed::before  { border-color: hsl(var(--destructive)); background: hsl(var(--destructive)); }
.timeline li.blocked::before { border-color: hsl(var(--warning));     background: hsl(var(--warning)); }
.timeline-title { font-weight: 600; font-size: 14px; margin-bottom: 4px; line-height: 1; }
.timeline-desc  { font-size: 13px; color: hsl(var(--muted-foreground)); margin: 0; line-height: 1.45; }

/* ===========================================================
 * Run detail blocks
 * ----------------------------------------------------------- */
.run-header { margin-bottom: 16px; }
.run-meta {
  display: flex; gap: 18px;
  font-size: 13px; color: hsl(var(--muted-foreground));
  flex-wrap: wrap; margin-top: 4px;
}
.run-meta strong { color: hsl(var(--foreground)); font-weight: 500; }
.run-body { display: grid; grid-template-columns: 1fr 1fr; gap: 24px; margin-bottom: 18px; }
@media (max-width: 1000px) { .run-body { grid-template-columns: 1fr; } }
.run-detail-grid {
  display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 12px; padding-top: 16px;
  border-top: 1px solid hsl(var(--border) / 0.5);
}
.detail-block {
  background: hsl(var(--muted) / 0.4);
  border: 1px solid hsl(var(--border) / 0.5);
  border-radius: 12px;
  padding: 14px;
}
.detail-block h4 { margin: 0 0 8px 0; }
.reason-list { padding-left: 18px; margin: 4px 0; font-size: 12.5px; }
.reason-list li { margin: 2px 0; }
.snippet {
  font-family: "JetBrains Mono", "SFMono-Regular", Menlo, monospace;
  font-size: 11.5px;
  background: hsl(var(--muted) / 0.6);
  padding: 10px 12px;
  border-radius: 8px;
  max-height: 180px;
  overflow: auto;
  white-space: pre-wrap;
  word-break: break-word;
}

/* ===========================================================
 * Filter bar (Hub Activity)
 * ----------------------------------------------------------- */
.filter-bar {
  display: flex; gap: 16px; align-items: center; flex-wrap: wrap;
  padding: 8px 0 12px 0;
  border-bottom: 1px solid hsl(var(--border) / 0.5);
  margin-bottom: 12px;
}
.filter-group { display: flex; gap: 6px; align-items: center; }
.filter-label {
  font-size: 11px; color: hsl(var(--muted-foreground));
  text-transform: uppercase; letter-spacing: 0.1em;
}
.filter-pill {
  background: transparent;
  color: hsl(var(--muted-foreground));
  border: 1px solid hsl(var(--border));
  padding: 4px 12px;
  border-radius: 999px;
  cursor: pointer;
  font-size: 12px;
  transition: color 120ms, border-color 120ms, background-color 120ms;
}
.filter-pill:hover { color: hsl(var(--foreground)); border-color: hsl(var(--accent) / 0.6); }
.filter-pill.active {
  background: hsl(var(--accent) / 0.14);
  color: hsl(var(--accent));
  border-color: hsl(var(--accent) / 0.4);
}
.filter-toggle {
  display: flex; gap: 6px; align-items: center;
  font-size: 12px;
  color: hsl(var(--muted-foreground));
  cursor: pointer;
}

/* ===========================================================
 * Lifecycle / stat boxes
 * ----------------------------------------------------------- */
.lifecycle-summary {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 10px;
  margin-bottom: 14px;
}
.stat-box {
  background: hsl(var(--muted) / 0.4);
  border: 1px solid hsl(var(--border) / 0.5);
  border-radius: 12px;
  padding: 10px 14px;
}
.stat-box.success { border-color: hsl(var(--success) / 0.4); }
.stat-box.pending { border-color: hsl(var(--warning) / 0.4); }
.stat-box.failed  { border-color: hsl(var(--destructive) / 0.4); }
.stat-label {
  font-size: 10px;
  color: hsl(var(--muted-foreground));
  text-transform: uppercase;
  letter-spacing: 0.12em;
}
.stat-value { font-size: 17px; font-weight: 600; margin-top: 4px; letter-spacing: -0.01em; }
.lifecycle-last-error {
  grid-column: 1 / -1;
  padding: 10px 12px;
  border-radius: 8px;
  background: hsl(var(--destructive) / 0.10);
  border: 1px solid hsl(var(--destructive) / 0.3);
  font-size: 13px;
}
.lifecycle-table { font-size: 12.5px; }
.lifecycle-table tr.fail td { color: hsl(var(--destructive)); }
.lifecycle-error {
  font-family: "JetBrains Mono", "SFMono-Regular", Menlo, monospace;
  font-size: 11.5px;
  max-width: 320px; overflow: hidden;
  text-overflow: ellipsis; white-space: nowrap;
}

/* ===========================================================
 * Score bar / validation
 * ----------------------------------------------------------- */
.score-bar {
  position: relative; display: inline-block;
  width: 90px; height: 16px;
  background: hsl(var(--muted) / 0.6);
  border-radius: 6px; overflow: hidden;
  vertical-align: middle;
}
.score-bar-lg { width: 240px; height: 22px; }
.score-bar-fill { height: 100%; transition: width 0.4s ease; }
.score-bar-text {
  position: absolute; inset: 0;
  display: flex; align-items: center; justify-content: center;
  font-size: 11px; font-weight: 600;
  color: hsl(var(--foreground));
  text-shadow: 0 0 2px hsl(var(--card));
}
.validation-block { grid-column: span 2; }
.validation-summary { display: flex; align-items: center; gap: 24px; flex-wrap: wrap; margin-bottom: 10px; }
.validation-status { display: flex; align-items: center; gap: 6px; font-size: 14px; }
.validation-score-wrap { display: flex; align-items: center; gap: 10px; }
.validation-score-label { font-size: 12px; color: hsl(var(--muted-foreground)); }
.validation-dims { margin: 6px 0; }
.validation-dim {
  background: hsl(var(--success) / 0.18) !important;
  color: hsl(var(--success)) !important;
}
.validation-observed   { margin-top: 6px; font-size: 12.5px; }
.validation-predictive { margin-top: 8px; font-size: 12.5px; }
.validation-predictive summary { cursor: pointer; color: hsl(var(--accent)); }

/* ===========================================================
 * Skill / event / stream / snapshot lists
 * ----------------------------------------------------------- */
.skill-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.skill-list li { padding: 10px 0; border-bottom: 1px solid hsl(var(--border) / 0.5); }
.skill-list li:last-child { border: none; }
.skill-list p { margin: 4px 0; font-size: 13px; }

.asset-tabs { display: flex; gap: 4px; flex-wrap: wrap; margin-bottom: 4px; }
.asset-tab {
  background: hsl(var(--muted) / 0.4);
  color: hsl(var(--muted-foreground));
  border: 1px solid hsl(var(--border) / 0.7);
  padding: 6px 14px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 13px; font-weight: 500;
  transition: background-color 120ms, color 120ms;
}
.asset-tab:hover { color: hsl(var(--foreground)); }
.asset-tab.active {
  background: hsl(var(--accent) / 0.12);
  color: hsl(var(--accent));
  border-color: hsl(var(--accent) / 0.4);
}

.event-list { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 10px; }
.event-list li {
  padding: 12px 14px;
  background: hsl(var(--muted) / 0.4);
  border: 1px solid hsl(var(--border) / 0.4);
  border-radius: 10px;
  font-size: 13px;
  display: flex; flex-direction: column; gap: 4px;
}

.stream-list {
  list-style: none; padding: 0; margin: 0;
  display: flex; flex-direction: column; gap: 8px;
  max-height: 540px; overflow-y: auto;
}
.stream-item {
  padding: 10px 14px;
  background: hsl(var(--muted) / 0.4);
  border-left: 3px solid hsl(var(--accent));
  border-radius: 0 10px 10px 0;
  font-size: 13px;
}
.stream-head { display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px; }
.stream-title { font-weight: 500; word-break: break-all; }

.snapshot-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 12px;
}
.snapshot-grid .snapshot-empty { grid-column: 1 / -1; margin: 0; white-space: nowrap; }
.snapshot-card {
  padding: 12px 14px;
  background: hsl(var(--muted) / 0.4);
  border: 1px solid hsl(var(--border) / 0.4);
  border-radius: 10px;
  font-size: 13px;
}
`;
}

module.exports = { getStylesCss };
