const $ = (id) => document.getElementById(id);

const ROUTES = ["overview", "trends", "strategy", "logs", "settings"];

const DICT = {
  zh: {
    brandSub: "OpenClaw 看门狗",
    navOverview: "总览",
    navTrends: "趋势",
    navStrategy: "策略",
    navLogs: "日志",
    navSettings: "配置",
    titleOverview: "恢复控制台",
    titleTrends: "趋势分析",
    titleStrategy: "策略控制",
    titleLogs: "日志审计",
    titleSettings: "配置状态",
    subtitleOverview: "把 Gateway、通道、日志和模型探针合成一个恢复判断。",
    subtitleTrends: "观察夜间超时、provider 异常和通道恢复是否在同一时间聚集。",
    subtitleStrategy: "选择处置姿态，并把高风险动作放进解锁流程。",
    subtitleLogs: "查看 watchdog 与 OpenClaw 信号，快速定位最近一次断链。",
    subtitleSettings: "确认运行路径、状态文件新鲜度和当前策略配置。",
    export: "导出诊断",
    currentDecision: "当前判断",
    recentRestarts: "近期重启",
    signalTypes: "异常类别",
    modelOk: "模型成功",
    modelFail: "模型失败",
    layers: "链路分层",
    layersHint: "按恢复路径从 Gateway 到模型 provider 排列。",
    signalCategories: "异常分类",
    signalHint: "用于判断是代理、provider 还是通道层问题。",
    eventTrend: "事件趋势",
    eventTrendHint: "诊断、日志告警和模型探针的同屏时间线。",
    trendDigest: "趋势摘要",
    trendDigestHint: "把散点变成可读结论。",
    modelSummary: "模型探针",
    restartSummary: "重启统计",
    latestSignals: "最新信号",
    actionCenter: "处置入口",
    quickStrategy: "快速策略",
    strategyHint: "选择故障处理姿态，所有写入动作都需要先解锁。",
    strategyMatrix: "策略矩阵",
    manualActions: "手动操作",
    manualHint: "高风险动作集中放在这里。",
    unlock: "解锁操作",
    lock: "锁定操作",
    presetObserve: "观察模式",
    presetOvernight: "夜间诊断",
    presetChannel: "通道恢复",
    presetConservative: "保守熔断",
    tipObserve: "只记录证据，不主动改变策略，适合先观察问题。",
    tipOvernight: "开启轻量模型探针并保持 log-only，适合排查固定时段超时。",
    tipChannel: "保持通道恢复敏感度，适合通道/session 经常断开的场景。",
    tipConservative: "提高阈值并降低重启频率，适合网络不稳定时防止重启风暴。",
    runDiag: "立即诊断",
    restartGateway: "重启 Gateway",
    configSummary: "配置摘要",
    sensitiveMasked: "敏感项已遮盖",
    stateFiles: "状态文件",
    recentLogs: "最近日志",
    logHint: "默认跟随最新行，适合观察夜间超时。",
    followLatest: "保持最新",
    runtimeMap: "运行地图",
    locked: "只读",
    actionReady: "可执行",
    unlocked: "已解锁",
    missing: "缺失",
    noSignals: "暂无异常分类",
    noTimeline: "暂无趋势数据",
    refreshFailed: "刷新失败",
    runningDiag: "正在执行诊断...",
    diagDone: "诊断完成",
    restartConfirm: "确认重启 OpenClaw Gateway？",
    restartDone: "重启命令已执行",
    presetDone: "已切换策略",
    tokenPrompt: "请输入 watchdog dashboard token。可在 watchdog.env/json 中查看 DASHBOARD_TOKEN。",
    tokenSaved: "操作 token 已保存到当前浏览器。",
    tokenCleared: "已清除本地 token。",
    clearConfirm: "要清除当前浏览器保存的操作 token 吗？",
    unlockFirst: "请先解锁操作。",
    statusUnknown: "正在汇总 watchdog 状态。",
    apiFail: "API失败",
    logWarn: "日志WARN",
    modelOkLegend: "模型OK",
    diagOk: "诊断OK",
    lastProbe: "最近探针",
    successRate: "成功比例",
    latestReason: "最新原因",
    noModelHistory: "暂无模型探针记录",
    restartWindow: "统计窗口",
    lastRestart: "最近重启",
    restartPolicy: "重启策略",
    stateDirectory: "状态目录",
    configFile: "配置文件",
    dashboardPort: "Dashboard 端口",
    dashboardAction: "写入动作",
    dominantSignal: "主要信号",
    evidenceCount: "证据数量",
    noRecentSignals: "暂无信号",
    enabled: "开启",
    disabled: "关闭",
    notAvailable: "暂无",
  },
  en: {
    brandSub: "OpenClaw Watchdog",
    navOverview: "Overview",
    navTrends: "Trends",
    navStrategy: "Strategy",
    navLogs: "Logs",
    navSettings: "Config",
    titleOverview: "Recovery Console",
    titleTrends: "Trend Analysis",
    titleStrategy: "Strategy Control",
    titleLogs: "Log Audit",
    titleSettings: "Config State",
    subtitleOverview: "Merge Gateway, channel, log, and model-probe evidence into one recovery decision.",
    subtitleTrends: "Watch whether fixed-hour timeouts, provider errors, and channel recovery cluster together.",
    subtitleStrategy: "Choose a response posture and keep risky actions behind an unlock flow.",
    subtitleLogs: "Audit watchdog and OpenClaw signals to locate the latest disconnect.",
    subtitleSettings: "Confirm runtime paths, state freshness, and active strategy config.",
    export: "Export Diagnostics",
    currentDecision: "Current Decision",
    recentRestarts: "Recent Restarts",
    signalTypes: "Signal Types",
    modelOk: "Model OK",
    modelFail: "Model Failed",
    layers: "Health Layers",
    layersHint: "Ordered by the recovery path from Gateway to model provider.",
    signalCategories: "Signal Categories",
    signalHint: "Helps separate proxy, provider, and channel failures.",
    eventTrend: "Event Trend",
    eventTrendHint: "Diagnostics, log warnings, and model probes in one timeline.",
    trendDigest: "Trend Digest",
    trendDigestHint: "Turns scattered points into readable conclusions.",
    modelSummary: "Model Probe",
    restartSummary: "Restart Summary",
    latestSignals: "Latest Signals",
    actionCenter: "Action Center",
    quickStrategy: "Quick Strategy",
    strategyHint: "Choose the response posture. Writes require unlock.",
    strategyMatrix: "Strategy Matrix",
    manualActions: "Manual Actions",
    manualHint: "High-risk actions live here.",
    unlock: "Unlock Actions",
    lock: "Lock Actions",
    presetObserve: "Observe",
    presetOvernight: "Overnight Diagnosis",
    presetChannel: "Channel Recovery",
    presetConservative: "Conservative Breaker",
    tipObserve: "Record evidence only. Best when you want to observe first.",
    tipOvernight: "Enable lightweight model probes with log-only actions for fixed-hour timeouts.",
    tipChannel: "Keep channel recovery responsive for session or channel disconnects.",
    tipConservative: "Raise thresholds and reduce restart frequency to prevent restart storms.",
    runDiag: "Run Diagnostics",
    restartGateway: "Restart Gateway",
    configSummary: "Config Summary",
    sensitiveMasked: "Sensitive values are masked",
    stateFiles: "State Files",
    recentLogs: "Recent Logs",
    logHint: "Follows the newest lines by default for overnight timeout checks.",
    followLatest: "Follow latest",
    runtimeMap: "Runtime Map",
    locked: "Read-only",
    actionReady: "Action ready",
    unlocked: "Unlocked",
    missing: "missing",
    noSignals: "No signal categories yet",
    noTimeline: "No trend data yet",
    refreshFailed: "Refresh failed",
    runningDiag: "Running diagnostics...",
    diagDone: "Diagnostics complete",
    restartConfirm: "Restart OpenClaw Gateway?",
    restartDone: "Restart command executed",
    presetDone: "Strategy applied",
    tokenPrompt: "Enter the watchdog dashboard token from DASHBOARD_TOKEN in watchdog.env/json.",
    tokenSaved: "Action token saved in this browser.",
    tokenCleared: "Local token cleared.",
    clearConfirm: "Clear the action token saved in this browser?",
    unlockFirst: "Unlock actions first.",
    statusUnknown: "Collecting watchdog status.",
    apiFail: "API failed",
    logWarn: "Log WARN",
    modelOkLegend: "Model OK",
    diagOk: "Diag OK",
    lastProbe: "Last probe",
    successRate: "Success rate",
    latestReason: "Latest reason",
    noModelHistory: "No model probe history",
    restartWindow: "Window",
    lastRestart: "Last restart",
    restartPolicy: "Restart policy",
    stateDirectory: "State directory",
    configFile: "Config file",
    dashboardPort: "Dashboard port",
    dashboardAction: "Write actions",
    dominantSignal: "Dominant signal",
    evidenceCount: "Evidence count",
    noRecentSignals: "No recent signals",
    enabled: "enabled",
    disabled: "disabled",
    notAvailable: "n/a",
  },
};

let lang = localStorage.getItem("watchdog.lang") || "zh";
let theme = localStorage.getItem("watchdog.theme") || "obsidian";
let activeRoute = localStorage.getItem("watchdog.route") || "overview";
let actionToken = localStorage.getItem("watchdog.actionToken") || window.WATCHDOG_ACTION_TOKEN || "";
let lastStatus = null;

if (!["obsidian", "daylight", "aurora", "graphite"].includes(theme)) {
  theme = "obsidian";
}

function t(key) {
  return DICT[lang]?.[key] || DICT.zh[key] || key;
}

function applyLocale() {
  document.documentElement.lang = lang === "zh" ? "zh-CN" : "en";
  setControlValue($("langSelect"), lang);
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    node.textContent = t(node.dataset.i18n);
  });
  document.querySelectorAll("[data-tip-key]").forEach((node) => {
    node.title = t(node.dataset.tipKey);
  });
  setRoute(activeRoute, { preserveScroll: true });
}

function applyTheme() {
  document.documentElement.dataset.theme = theme;
  setControlValue($("themeSelect"), theme);
}

function setControlValue(node, value) {
  if (!node) return;
  node.value = value;
  node.setAttribute("value", value);
}

function setRoute(route, options = {}) {
  activeRoute = ROUTES.includes(route) ? route : "overview";
  localStorage.setItem("watchdog.route", activeRoute);
  document.querySelectorAll("[data-route]").forEach((node) => {
    node.classList.toggle("active", node.dataset.route === activeRoute);
  });
  document.querySelectorAll("[data-view]").forEach((node) => {
    node.classList.toggle("active", node.dataset.view === activeRoute);
  });
  $("pageTitle").textContent = t(`title${activeRoute[0].toUpperCase()}${activeRoute.slice(1)}`);
  $("pageSubtitle").textContent = t(`subtitle${activeRoute[0].toUpperCase()}${activeRoute.slice(1)}`);
  if (!options.preserveScroll) window.scrollTo({ top: 0, behavior: "auto" });
  if (lastStatus) renderCharts(lastStatus);
}

function toast(message) {
  const node = $("toast");
  node.textContent = message;
  node.hidden = false;
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => { node.hidden = true; }, 3800);
}

function fmtAge(seconds) {
  if (seconds == null) return t("missing");
  if (seconds < 60) return `${seconds}s`;
  if (seconds < 3600) return `${Math.round(seconds / 60)}m`;
  return `${Math.round(seconds / 3600)}h`;
}

function fmtDate(value) {
  if (!value) return t("notAvailable");
  const ts = typeof value === "number" ? value : Date.parse(value);
  if (!Number.isFinite(ts)) return String(value);
  return new Date(ts).toLocaleString(lang === "zh" ? "zh-CN" : "en-US");
}

function statusClass(status) {
  if (status === "ok") return "ok";
  if (status === "degraded" || status === "stale") return "degraded";
  if (status === "down" || status === "fail") return "fail";
  return "unknown";
}

async function fetchStatus() {
  const res = await fetch("/api/status", { cache: "no-store" });
  if (!res.ok) throw new Error(`status ${res.status}`);
  return res.json();
}

async function postJson(url, body = {}) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Watchdog-Token": actionToken,
    },
    body: JSON.stringify(body),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok || data.ok === false) throw new Error(data.error || `request failed ${res.status}`);
  return data;
}

function prepareCanvas(canvas, fallbackHeight) {
  const rect = canvas.getBoundingClientRect();
  if (rect.width < 10 || rect.height < 10) return null;
  const width = Math.floor(rect.width);
  const cssHeight = Math.max(140, Math.floor(rect.height || fallbackHeight));
  const ratio = window.devicePixelRatio || 1;
  canvas.width = Math.floor(width * ratio);
  canvas.height = Math.floor(cssHeight * ratio);
  const ctx = canvas.getContext("2d");
  ctx.setTransform(ratio, 0, 0, ratio, 0, 0);
  ctx.clearRect(0, 0, width, cssHeight);
  return { ctx, width, height: cssHeight };
}

function cssVar(name) {
  return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
}

function drawBars(canvas, data) {
  const prepared = prepareCanvas(canvas, 220);
  if (!prepared) return;
  const { ctx, width, height } = prepared;
  const entries = Object.entries(data || {}).slice(0, 8);
  ctx.font = "12px ui-monospace, Consolas, monospace";
  if (!entries.length) {
    ctx.fillStyle = cssVar("--muted");
    ctx.fillText(t("noSignals"), 14, 28);
    return;
  }
  const max = Math.max(...entries.map(([, value]) => value), 1);
  const colors = [cssVar("--accent"), cssVar("--green"), cssVar("--amber"), cssVar("--red"), cssVar("--violet"), cssVar("--accent-2")];
  const labelWidth = Math.min(150, Math.max(108, width * 0.34));
  const rowHeight = Math.max(18, Math.floor((height - 26) / entries.length));
  entries.forEach(([name, value], index) => {
    const y = 20 + index * rowHeight;
    const barWidth = Math.max(4, (width - labelWidth - 48) * (value / max));
    ctx.fillStyle = cssVar("--muted");
    ctx.fillText(name.length > 18 ? `${name.slice(0, 17)}...` : name, 12, y);
    ctx.fillStyle = colors[index % colors.length];
    ctx.fillRect(labelWidth, y - 11, barWidth, 12);
    ctx.fillStyle = cssVar("--ink");
    ctx.fillText(String(value), labelWidth + barWidth + 8, y);
  });
}

function formatTick(ts) {
  return new Date(ts).toLocaleTimeString(lang === "zh" ? "zh-CN" : "en-US", { hour: "2-digit", minute: "2-digit" });
}

function drawTimeline(canvas, diagnostics, modelHistory) {
  const prepared = prepareCanvas(canvas, 300);
  if (!prepared) return;
  const { ctx, width, height } = prepared;
  const points = [];
  for (const item of diagnostics || []) points.push({ ts: Date.parse(item.ts), kind: item.newLogSignals ? "warn" : "ok" });
  for (const item of modelHistory || []) points.push({ ts: Date.parse(item.ts), kind: item.status === "fail" ? "fail" : "model-ok" });
  const valid = points.filter((p) => Number.isFinite(p.ts)).sort((a, b) => a.ts - b.ts).slice(-180);
  const left = 104;
  const right = width - 28;
  const top = 32;
  const axisY = height - 42;
  ctx.font = "12px system-ui";
  ctx.strokeStyle = cssVar("--line");
  ctx.beginPath();
  ctx.moveTo(left, axisY);
  ctx.lineTo(right, axisY);
  ctx.stroke();
  if (!valid.length) {
    ctx.fillStyle = cssVar("--muted");
    ctx.fillText(t("noTimeline"), left, top + 28);
    return;
  }
  const min = valid[0].ts;
  const max = valid[valid.length - 1].ts || min + 1;
  const lanes = [
    ["fail", t("apiFail"), cssVar("--red"), top + 20],
    ["warn", t("logWarn"), cssVar("--amber"), top + 70],
    ["model-ok", t("modelOkLegend"), cssVar("--accent"), top + 120],
    ["ok", t("diagOk"), cssVar("--green"), top + 170],
  ];
  for (const [, label, color, y] of lanes) {
    ctx.fillStyle = color;
    ctx.beginPath();
    ctx.arc(18, y - 4, 4, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = cssVar("--muted");
    ctx.fillText(label, 32, y);
    ctx.strokeStyle = cssVar("--line");
    ctx.beginPath();
    ctx.moveTo(left, y - 4);
    ctx.lineTo(right, y - 4);
    ctx.stroke();
  }
  const laneMap = Object.fromEntries(lanes.map(([kind, , color, y]) => [kind, { color, y: y - 4 }]));
  valid.forEach((p, index) => {
    const x = left + ((p.ts - min) / Math.max(1, max - min)) * (right - left);
    const lane = laneMap[p.kind] || laneMap.ok;
    ctx.fillStyle = lane.color;
    ctx.beginPath();
    ctx.arc(x, lane.y, index === valid.length - 1 ? 4.6 : 3.3, 0, Math.PI * 2);
    ctx.fill();
  });
  const ticks = [min, min + (max - min) / 2, max];
  ctx.fillStyle = cssVar("--muted");
  ticks.forEach((tick, i) => {
    const x = left + ((tick - min) / Math.max(1, max - min)) * (right - left);
    const label = formatTick(tick);
    const offset = i === 2 ? -44 : i === 1 ? -22 : -8;
    ctx.fillText(label, x + offset, axisY + 22);
  });
}

function renderLayers(data) {
  const files = data.files || {};
  const cfg = data.config || {};
  const layers = [
    ["Gateway", files.gateway, data.summary.status === "ok" ? "ok" : data.summary.status === "unknown" ? "warn" : "fail"],
    ["OpenClaw Health", files.health, data.summary.status === "degraded" ? "fail" : files.health?.exists ? "ok" : "warn"],
    ["Logs Signal", files.signals, data.summary.categoryCount ? "warn" : "ok"],
    ["Model Probe", files.modelHistory, data.summary.modelFailures ? "warn" : files.modelHistory?.exists ? "ok" : "warn"],
    ["Config", { exists: true, ageSeconds: null, path: data.configFile }, cfg.MODEL_PROBE_ENABLED === "1" || cfg.ModelProbeEnabled === true ? "warn" : "ok"],
  ];
  $("layers").innerHTML = layers.map(([name, meta, state]) => `
    <div class="layer">
      <span class="spark ${state}"></span>
      <div><strong>${name}</strong><span class="subtle" title="${meta?.path || ""}">${meta?.path || "runtime snapshot"}</span></div>
      <span class="subtle">${meta?.exists ? fmtAge(meta.ageSeconds) : t("missing")}</span>
    </div>
  `).join("");
}

function renderSummaryList(id, rows) {
  const node = $(id);
  if (!node) return;
  node.innerHTML = rows.map(([label, value]) => `
    <div class="summary-row">
      <span class="subtle">${label}</span>
      <strong>${value}</strong>
    </div>
  `).join("");
}

function renderMiniList(id, rows) {
  const node = $(id);
  if (!node) return;
  const safeRows = rows.length ? rows : [[t("noRecentSignals"), t("notAvailable")]];
  node.innerHTML = safeRows.map(([label, value]) => `
    <div class="mini-row">
      <span class="subtle">${label}</span>
      <strong>${value}</strong>
    </div>
  `).join("");
}

function renderTrendSummaries(data) {
  const history = data.modelHistory || [];
  const latest = history[history.length - 1];
  const modelTotal = (data.summary.modelOk || 0) + (data.summary.modelFailures || 0);
  const successRate = modelTotal ? `${Math.round(((data.summary.modelOk || 0) / modelTotal) * 100)}%` : t("notAvailable");
  const modelRows = [
    [t("lastProbe"), latest ? fmtDate(latest.ts) : t("noModelHistory")],
    [t("successRate"), successRate],
    [t("latestReason"), latest?.reason || latest?.status || t("notAvailable")],
  ];
  const cfg = data.config || {};
  const restartRows = [
    [t("restartWindow"), "24h"],
    [t("recentRestarts"), data.summary.recentRestarts ?? 0],
    [t("restartPolicy"), cfg.OPENCLAW_DIAG_ACTION || cfg.OpenClawDiagAction || t("notAvailable")],
  ];
  renderSummaryList("modelSummary", modelRows);
  renderSummaryList("overviewModelSummary", modelRows);
  renderSummaryList("restartSummary", restartRows);
  renderSummaryList("overviewRestartSummary", restartRows);
  const categories = Object.entries(data.categories || {}).sort((a, b) => b[1] - a[1]);
  renderMiniList("categoryTopList", categories.slice(0, 4));
  renderMiniList("latestSignals", categories.slice(0, 5));
  renderMiniList("logSignalList", categories.slice(0, 10));
  const dominant = categories[0]?.[0] || t("notAvailable");
  const evidenceCount = (data.diagnostics || []).length + (data.modelHistory || []).length;
  renderMiniList("trendDigest", [
    [t("dominantSignal"), dominant],
    [t("evidenceCount"), evidenceCount],
    [t("modelFail"), data.summary.modelFailures ?? 0],
    [t("recentRestarts"), data.summary.recentRestarts ?? 0],
  ]);
  renderStrategyConfig(data);
  renderStrategyMatrix();
  renderRuntimeMap(data);
}

function renderStrategyConfig(data) {
  const cfg = data.config || {};
  renderSummaryList("strategyConfigSummary", [
    ["MODEL_PROBE", cfg.MODEL_PROBE_ENABLED === "1" || cfg.ModelProbeEnabled === true ? t("enabled") : t("disabled")],
    ["OPENCLAW_DIAG_ACTION", cfg.OPENCLAW_DIAG_ACTION || cfg.OpenClawDiagAction || t("notAvailable")],
    ["MAX_RESTARTS_PER_HOUR", cfg.MAX_RESTARTS_PER_HOUR || cfg.MaxRestartsPerHour || t("notAvailable")],
    [t("dashboardAction"), data.dashboard?.actionsEnabled ? t("enabled") : t("disabled")],
  ]);
}

function renderStrategyMatrix() {
  const rows = [
    [t("presetObserve"), t("tipObserve")],
    [t("presetOvernight"), t("tipOvernight")],
    [t("presetChannel"), t("tipChannel")],
    [t("presetConservative"), t("tipConservative")],
  ];
  const node = $("strategyMatrix");
  if (!node) return;
  node.innerHTML = rows.map(([title, detail]) => `
    <div class="matrix-cell">
      <strong>${title}</strong>
      <span>${detail}</span>
    </div>
  `).join("");
}

function renderRuntimeMap(data) {
  const node = $("runtimeMap");
  if (!node) return;
  const rows = [
    [t("stateDirectory"), data.stateDir || t("notAvailable")],
    [t("configFile"), data.configFile || t("notAvailable")],
    [t("dashboardPort"), data.dashboard?.port || t("notAvailable")],
    [t("dashboardAction"), data.dashboard?.actionsEnabled ? t("enabled") : t("disabled")],
  ];
  node.innerHTML = rows.map(([title, detail]) => `
    <div class="runtime-cell">
      <strong>${title}</strong>
      <span>${detail}</span>
    </div>
  `).join("");
}

function renderConfig(config) {
  const keys = [
    "OPENCLAW_DIAG_ACTION", "MODEL_PROBE_ENABLED", "MODEL_PROBE_INTERVAL",
    "MODEL_PROBE_ACTION", "CHANNEL_FAILURES_BEFORE_RESTART", "MAX_RESTARTS_PER_HOUR",
    "DASHBOARD_ACTIONS_ENABLED", "DashboardActionsEnabled", "DASHBOARD_PORT", "DashboardPort",
  ];
  const rows = [];
  for (const key of keys) if (Object.prototype.hasOwnProperty.call(config, key)) rows.push([key, config[key]]);
  $("configList").innerHTML = rows.map(([key, value]) => `
    <div class="config-row">
      <dt title="${key}">${key}</dt>
      <dd>${String(value)}</dd>
    </div>
  `).join("");
}

function renderFiles(files) {
  $("fileList").innerHTML = Object.entries(files || {}).map(([name, meta]) => `
    <div class="file-row">
      <strong>${name}</strong>
      <span class="subtle">${meta.exists ? `${fmtAge(meta.ageSeconds)} / ${Math.round((meta.size || 0) / 1024)}KB` : t("missing")}</span>
    </div>
  `).join("");
}

function updateActionUi(data) {
  const serverReady = Boolean(data.dashboard?.actionsEnabled);
  const unlocked = Boolean(actionToken);
  const label = serverReady ? (unlocked ? t("unlocked") : t("actionReady")) : t("locked");
  const className = serverReady ? (unlocked ? "status-chip unlocked" : "status-chip enabled") : "status-chip";
  for (const id of ["actionState", "strategyActionState"]) {
    const node = $(id);
    if (!node) continue;
    node.textContent = label;
    node.className = className;
  }
  for (const id of ["unlockBtn", "strategyUnlockBtn"]) {
    const node = $(id);
    if (node) node.textContent = unlocked ? t("lock") : t("unlock");
  }
  const disabled = !serverReady || !unlocked;
  document.querySelectorAll("[data-preset], #diagBtn, #restartBtn, #heroDiagBtn, #heroRestartBtn").forEach((node) => {
    node.classList.toggle("guarded-disabled", disabled);
    node.setAttribute("aria-disabled", String(disabled));
  });
}

function canRunActions() {
  if (!lastStatus?.dashboard?.actionsEnabled || !actionToken) {
    toast(t("unlockFirst"));
    return false;
  }
  return true;
}

function renderCharts(data) {
  if (activeRoute === "overview") drawBars($("categoryChart"), data.categories || {});
  if (activeRoute === "trends") drawTimeline($("timelineChart"), data.diagnostics || [], data.modelHistory || []);
}

function render(data) {
  lastStatus = data;
  const status = data.summary.status || "unknown";
  $("mainStatus").className = `status-orb ${statusClass(status)}`;
  $("sideStatusDot").className = `mini-led ${statusClass(status)}`;
  $("sideStatusText").textContent = status.toUpperCase();
  $("statusText").textContent = status.toUpperCase();
  $("statusReason").textContent = data.summary.reason || t("statusUnknown");
  $("restartCount").textContent = data.summary.recentRestarts ?? 0;
  $("categoryCount").textContent = data.summary.categoryCount ?? 0;
  $("modelOk").textContent = data.summary.modelOk ?? 0;
  $("modelFail").textContent = data.summary.modelFailures ?? 0;
  $("updatedAt").textContent = fmtDate(data.generatedAt);
  $("sideUpdatedAt").textContent = fmtDate(data.generatedAt);
  const modelTotal = (data.summary.modelOk || 0) + (data.summary.modelFailures || 0);
  $("modelRate").textContent = modelTotal ? `${Math.round(((data.summary.modelOk || 0) / modelTotal) * 100)}%` : "--";
  $("modelFailHint").textContent = data.summary.modelFailures ? "check provider" : "provider";
  updateActionUi(data);
  renderLayers(data);
  renderTrendSummaries(data);
  renderConfig(data.config || {});
  renderFiles(data.files || {});
  const log = $("logTail");
  const shouldFollow = $("followLog").checked;
  log.textContent = (data.logTail || []).join("\n") || "No logs yet.";
  if (shouldFollow) log.scrollTop = log.scrollHeight;
  renderCharts(data);
}

async function refresh() {
  try {
    render(await fetchStatus());
  } catch (err) {
    toast(`${t("refreshFailed")}: ${err.message}`);
  }
}

function saveSettings() {
  localStorage.setItem("watchdog.lang", lang);
  localStorage.setItem("watchdog.theme", theme);
}

document.querySelectorAll("[data-route]").forEach((button) => {
  button.addEventListener("click", () => setRoute(button.dataset.route));
});

$("langSelect").addEventListener("change", () => {
  lang = $("langSelect").value;
  saveSettings();
  applyLocale();
  if (lastStatus) render(lastStatus);
});

$("themeSelect").addEventListener("change", () => {
  theme = $("themeSelect").value;
  saveSettings();
  applyTheme();
  if (lastStatus) render(lastStatus);
});

$("refreshBtn").addEventListener("click", refresh);
$("unlockBtn").addEventListener("click", () => {
  if (actionToken) {
    if (confirm(t("clearConfirm"))) {
      actionToken = "";
      localStorage.removeItem("watchdog.actionToken");
      toast(t("tokenCleared"));
      if (lastStatus) render(lastStatus);
    }
    return;
  }
  const entered = prompt(t("tokenPrompt"), "");
  if (entered && entered.trim()) {
    actionToken = entered.trim();
    localStorage.setItem("watchdog.actionToken", actionToken);
    toast(t("tokenSaved"));
    if (lastStatus) render(lastStatus);
  }
});

$("strategyUnlockBtn").addEventListener("click", () => $("unlockBtn").click());

$("exportBtn").addEventListener("click", async () => {
  const data = lastStatus || await fetchStatus();
  const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = `openclaw-watchdog-${Date.now()}.json`;
  a.click();
  URL.revokeObjectURL(url);
});

$("diagBtn").addEventListener("click", async () => {
  if (!canRunActions()) return;
  try {
    toast(t("runningDiag"));
    await postJson("/api/actions/run-diagnostics");
    await refresh();
    toast(t("diagDone"));
  } catch (err) {
    toast(err.message);
  }
});

$("heroDiagBtn").addEventListener("click", () => $("diagBtn").click());

$("restartBtn").addEventListener("click", async () => {
  if (!canRunActions()) return;
  if (!confirm(t("restartConfirm"))) return;
  try {
    await postJson("/api/actions/restart-gateway");
    await refresh();
    toast(t("restartDone"));
  } catch (err) {
    toast(err.message);
  }
});

$("heroRestartBtn").addEventListener("click", () => $("restartBtn").click());

document.querySelectorAll("[data-preset]").forEach((button) => {
  button.addEventListener("click", async () => {
    if (!canRunActions()) return;
    try {
      await postJson("/api/config/preset", { preset: button.dataset.preset });
      await refresh();
      toast(`${t("presetDone")}: ${button.querySelector("strong")?.textContent || button.textContent}`);
    } catch (err) {
      toast(err.message);
    }
  });
});

window.addEventListener("resize", () => {
  if (lastStatus) renderCharts(lastStatus);
});

applyTheme();
applyLocale();
refresh();
setInterval(refresh, 15000);
