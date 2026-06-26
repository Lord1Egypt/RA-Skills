'use strict';

// Bilingual (en + zh) string registry + tiny runtime helpers.
//
// Design choices (KISS):
// - One flat dict keyed by stable IDs; every value has both `en` and `zh`.
// - `t(key)` falls back to the key itself so a missing translation is
//   visible (and harmless) rather than rendering "undefined".
// - Status / action enum tokens use dedicated tables so backend-emitted
//   identifiers (e.g. "review_pending", "asset_publish") render localized
//   labels but still pass through unknown values unchanged.
// - DOM-side static text is annotated with data-i18n attributes; one pass
//   over the document on locale change updates everything in place.
//
// This module ships as a single string that's concatenated into the
// browser bundle alongside the other clientJs modules.

exports.i18nJs = `
const I18N_LOCALES = ['en', 'zh'];
const I18N_DEFAULT = 'en';
const I18N_STORAGE_KEY = 'evolver-locale';

const I18N_DICT = {
  // ---- Chrome ----
  'brand.eyebrow': { en: 'local agent', zh: '本地智能体' },
  'sidebar.footer': { en: 'evolves with you', zh: '与你共同进化' },
  'topbar.eyebrow': { en: 'EvoMap Evolver · Web UI Observability', zh: 'EvoMap Evolver · Web UI 观测台' },
  'btn.refresh': { en: 'Refresh', zh: '刷新' },
  'btn.refresh.title': { en: 'Refresh all data', zh: '刷新所有数据' },
  'btn.theme.title': { en: 'Toggle light / dark theme', zh: '切换浅色 / 深色主题' },
  'btn.locale.title': { en: 'Switch language (EN / 中)', zh: '切换语言（EN / 中）' },

  // ---- Nav ----
  'nav.overview': { en: 'Overview', zh: '总览' },
  'nav.pipelines': { en: 'Pipelines', zh: '流水线' },
  'nav.assets': { en: 'Assets', zh: '资产' },
  'nav.interactions': { en: 'Interactions', zh: '交互' },
  'nav.personality': { en: 'Personality', zh: '人格' },

  // ---- Common ----
  'common.loading': { en: 'Loading...', zh: '加载中...' },
  'common.none': { en: 'none', zh: '无' },
  'common.yes': { en: 'yes', zh: '是' },
  'common.no': { en: 'no', zh: '否' },
  'common.available': { en: 'available', zh: '可用' },
  'common.notAvailable': { en: 'not available', zh: '不可用' },
  'common.running': { en: 'running', zh: '运行中' },
  'common.notRunning': { en: 'not running', zh: '未运行' },
  'common.idle': { en: 'idle', zh: '空闲' },
  'common.dash': { en: '-', zh: '-' },
  'common.failedPrefix': { en: 'Failed: ', zh: '失败：' },

  // ---- Overview · Status card ----
  'overview.card.status': { en: 'Status', zh: '状态' },
  'overview.card.safety': { en: 'Safety', zh: '安全' },
  'overview.card.interactions': { en: 'Interactions', zh: '交互' },
  'overview.card.genesByCategory': { en: 'Genes by Category', zh: '按类别的 Gene' },
  'overview.card.capsulesByOutcome': { en: 'Capsules by Outcome', zh: '按结果的 Capsule' },
  'overview.card.assetCalls': { en: 'Asset Calls', zh: '资产调用' },
  'overview.card.latestRun': { en: 'Latest Pipeline Run', zh: '最近一次流水线运行' },
  'overview.card.skills': { en: 'Skills', zh: '技能' },

  'overview.status.mode': { en: 'Mode', zh: '模式' },
  'overview.status.proxy': { en: 'Proxy', zh: '代理' },
  'overview.status.heartbeat': { en: 'Heartbeat', zh: '心跳' },
  'overview.status.lastRun': { en: 'Last run', zh: '最近运行' },
  'overview.status.lastActivity': { en: 'Last activity', zh: '最近活动' },

  'overview.safety.safeMode': { en: 'Safe mode', zh: '安全模式' },
  'overview.safety.reviewRequired': { en: 'Review required', zh: '需要审核' },
  'overview.safety.autobuy': { en: 'Autobuy', zh: '自动购买' },
  'overview.safety.autoPublish': { en: 'Auto publish', zh: '自动发布' },
  'overview.safety.validator': { en: 'Validator', zh: '校验器' },
  'overview.safety.traceLevel': { en: 'Trace level', zh: '追踪等级' },
  'overview.safety.noWarnings': { en: 'No unsafe automation flags detected.', zh: '未检测到不安全的自动化设置。' },

  'overview.interactions.proxy': { en: 'Proxy', zh: '代理' },
  'overview.interactions.mailbox': { en: 'Mailbox messages', zh: '收件箱消息' },
  'overview.interactions.taskMetrics': { en: 'Task metrics', zh: '任务指标' },
  'overview.interactions.sessions': { en: 'Sessions', zh: '会话' },

  'overview.run.id': { en: 'Run ID', zh: '运行 ID' },
  'overview.run.status': { en: 'Status', zh: '状态' },
  'overview.run.selectedGene': { en: 'Selected Gene', zh: '所选 Gene' },
  'overview.run.validation': { en: 'Validation', zh: '校验' },
  'overview.run.updated': { en: 'Updated', zh: '更新时间' },
  'overview.run.requiresConfirmation': { en: 'Requires confirmation', zh: '需要确认' },
  'overview.run.empty': { en: 'No runs recorded yet.', zh: '暂无运行记录。' },

  'overview.skills.empty': { en: 'No local skills installed yet.', zh: '本地暂未安装任何技能。' },
  'overview.skills.hint': { en: 'Use <code>evolver fetch --skill=&lt;id&gt;</code> to install one from the Hub.', zh: '使用 <code>evolver fetch --skill=&lt;id&gt;</code> 从 Hub 安装一个技能。' },
  'overview.skills.files': { en: 'files', zh: '个文件' },
  'overview.skills.noDoc': { en: 'no doc', zh: '无文档' },

  'overview.validation.pass': { en: 'pass', zh: '通过' },
  'overview.validation.fail': { en: 'fail', zh: '未通过' },
  'overview.validation.pendingReview': { en: 'pending review', zh: '待审核' },
  'overview.validation.inProgress': { en: 'in progress', zh: '进行中' },
  'overview.validation.notRun': { en: 'not run', zh: '未运行' },

  // ---- Pipelines tab ----
  'pipelines.card.runs': { en: 'Pipeline Runs', zh: '流水线运行列表' },
  'pipelines.card.runTrace': { en: 'Run Trace', zh: '运行追踪' },
  'pipelines.card.scoreTrend': { en: 'Score Trend', zh: '评分趋势' },
  'pipelines.col.runId': { en: 'Run ID', zh: '运行 ID' },
  'pipelines.col.status': { en: 'Status', zh: '状态' },
  'pipelines.col.gene': { en: 'Gene', zh: 'Gene' },
  'pipelines.col.score': { en: 'Score', zh: '评分' },
  'pipelines.col.updated': { en: 'Updated', zh: '更新时间' },
  'pipelines.runs.empty': { en: 'No runs recorded yet.', zh: '暂无运行记录。' },
  'pipelines.runs.selectHint': { en: 'Select a run to inspect its trace.', zh: '选择一条运行以查看追踪详情。' },
  'pipelines.runs.loadingTrace': { en: 'Loading trace...', zh: '加载追踪中...' },
  'pipelines.runs.failedToLoad': { en: 'Failed to load run: ', zh: '加载运行失败：' },
  'pipelines.timeline': { en: 'Pipeline Timeline', zh: '流水线时间线' },
  'pipelines.runGraph': { en: 'Run Graph', zh: '运行图谱' },

  'pipelines.detail.triggerSignals': { en: 'Trigger signals', zh: '触发信号' },
  'pipelines.detail.triggerSignals.desc': { en: 'Environment snapshot detected at run start (used to pick a matching Gene). Not errors.', zh: '运行启动时捕获的环境快照（用于挑选合适的 Gene），不代表错误。' },
  'pipelines.detail.selector': { en: 'Selector reasoning', zh: '选择器推理' },
  'pipelines.detail.selector.selected': { en: 'Selected', zh: '已选' },
  'pipelines.detail.selector.path': { en: 'Path', zh: '路径' },
  'pipelines.detail.selector.memoryUsed': { en: 'Memory used', zh: '使用的记忆' },

  'pipelines.detail.mutation': { en: 'Mutation', zh: '变异' },
  'pipelines.detail.mutation.id': { en: 'ID', zh: 'ID' },
  'pipelines.detail.mutation.category': { en: 'Category', zh: '类别' },
  'pipelines.detail.mutation.targetType': { en: 'Target type', zh: '目标类型' },
  'pipelines.detail.mutation.strategySteps': { en: 'Strategy steps', zh: '策略步骤数' },
  'pipelines.detail.mutation.triggerSignals': { en: 'Trigger signals', zh: '触发信号' },

  'pipelines.detail.validation.title': { en: 'Validation result', zh: '校验结果' },
  'pipelines.detail.validation.score': { en: 'Score', zh: '评分' },
  'pipelines.detail.validation.dimensions': { en: 'Dimensions:', zh: '维度：' },
  'pipelines.detail.validation.observed': { en: 'Observed signals after run:', zh: '运行后观察到的信号：' },
  'pipelines.detail.validation.predictive': { en: 'Predictive measurements', zh: '预测度量' },
  'pipelines.detail.validation.validatedAt': { en: 'Validated at ', zh: '校验于 ' },
  'pipelines.detail.validation.noDimensions': { en: 'no dimensions recorded', zh: '未记录维度' },
  'pipelines.detail.validation.hint.reviewPending': { en: 'Run is awaiting review confirmation — local validation has not run yet.', zh: '该运行等待审核确认——尚未执行本地校验。' },
  'pipelines.detail.validation.hint.running': { en: 'Validation will appear here once the solidify phase emits an outcome event.', zh: 'solidify 阶段输出结果事件后，校验信息将显示于此。' },
  'pipelines.detail.validation.hint.none': { en: 'No validation outcome recorded for this run.', zh: '本次运行没有校验结果记录。' },

  'pipelines.dim.stable_no_error': { en: 'Stable (no errors)', zh: '稳定（无错误）' },
  'pipelines.dim.heuristic_delta': { en: 'Heuristic delta', zh: '启发式增量' },
  'pipelines.dim.predictive': { en: 'Predictive match', zh: '预测匹配' },
  'pipelines.dim.failed': { en: 'Failed', zh: '失败' },
  'pipelines.dim.unstable': { en: 'Unstable', zh: '不稳定' },

  'pipelines.detail.blastRadius': { en: 'Blast radius', zh: '影响范围' },
  'pipelines.detail.blastRadius.files': { en: 'Files', zh: '文件数' },
  'pipelines.detail.blastRadius.lines': { en: 'Lines', zh: '行数' },
  'pipelines.detail.blastRadius.risk': { en: 'Risk', zh: '风险等级' },

  'pipelines.detail.personalityState': { en: 'Personality at run', zh: '运行时人格' },
  'pipelines.detail.initialUserPrompt': { en: 'Initial user prompt', zh: '初始用户提示' },

  'pipelines.chart.scoreTrend.empty': { en: 'No scored runs yet — runs only get a score after solidify produces an outcome event.', zh: '暂无评分运行——只有 solidify 输出结果事件后，运行才会获得评分。' },
  'pipelines.chart.scoreTrend.passLine': { en: 'pass ≥0.7', zh: '通过 ≥0.7' },

  // ---- Assets tab ----
  'assets.tab.genes': { en: 'Genes', zh: 'Genes' },
  'assets.tab.capsules': { en: 'Capsules', zh: 'Capsules' },
  'assets.tab.events': { en: 'Events', zh: 'Events' },
  'assets.tab.candidates': { en: 'Candidates', zh: '候选项' },
  'assets.tab.calls': { en: 'Asset Calls', zh: '资产调用' },

  'assets.col.id': { en: 'ID', zh: 'ID' },
  'assets.col.category': { en: 'Category', zh: '类别' },
  'assets.col.signals': { en: 'Signals', zh: '信号' },
  'assets.col.strategy': { en: 'Strategy', zh: '策略' },
  'assets.col.validation': { en: 'Validation', zh: '校验' },
  'assets.col.gene': { en: 'Gene', zh: 'Gene' },
  'assets.col.outcome': { en: 'Outcome', zh: '结果' },
  'assets.col.confidence': { en: 'Confidence', zh: '置信度' },
  'assets.col.blast': { en: 'Blast', zh: '影响' },
  'assets.col.source': { en: 'Source', zh: '来源' },
  'assets.col.assetId': { en: 'Asset ID', zh: '资产 ID' },
  'assets.col.score': { en: 'Score', zh: '评分' },
  'assets.col.time': { en: 'Time', zh: '时间' },
  'assets.col.action': { en: 'Action', zh: '动作' },
  'assets.col.asset': { en: 'Asset', zh: '资产' },
  'assets.col.run': { en: 'Run', zh: '运行' },

  'assets.records': { en: 'record(s)', zh: '条记录' },
  'assets.steps': { en: 'steps', zh: '步' },
  'assets.cmds': { en: 'cmd(s)', zh: '条命令' },
  'assets.events.signals': { en: 'signals: ', zh: '信号：' },
  'assets.events.genes': { en: 'genes_used: ', zh: '使用的 Gene：' },
  'assets.events.outcome': { en: 'outcome: ', zh: '结果：' },

  'assets.empty.capsules': { en: 'No capsules yet. Capsules are created after a successful solidify.', zh: '暂无 Capsule。solidify 成功后才会生成 Capsule。' },
  'assets.empty.events': { en: 'No solidified events yet. Run <code>evolver solidify</code> to produce events.', zh: '暂无 solidified 事件。运行 <code>evolver solidify</code> 即可生成事件。' },
  'assets.empty.candidates': { en: 'No candidates collected yet.', zh: '暂未收集到候选项。' },
  'assets.empty.calls': { en: 'No asset calls recorded.', zh: '暂无资产调用记录。' },

  // ---- Interactions tab ----
  'interactions.card.hubByAction': { en: 'Hub A2A by Action', zh: '按动作划分的 Hub A2A' },
  'interactions.card.activity30d': { en: 'Activity (last 30 days)', zh: '活动（近 30 天）' },
  'interactions.card.mailboxByType': { en: 'Mailbox by Type', zh: '按类型划分的收件箱' },
  'interactions.card.hubActivity': { en: 'Hub Activity', zh: 'Hub 活动' },
  'interactions.card.hubActivity.desc': { en: 'Unified timeline of every Hub interaction — connection lifecycle (hello/heartbeat/fetch), asset calls (search/reuse/publish) and ATP credit flows.', zh: '所有 Hub 交互的统一时间线 —— 连接生命周期（hello/heartbeat/fetch）、资产调用（search/reuse/publish）和 ATP 积分流动。' },
  'interactions.card.agent': { en: 'Agent Interactions', zh: '智能体交互' },
  'interactions.card.agent.desc': { en: 'Mailbox messages, sessions and DMs (read-only, redacted).', zh: '收件箱消息、会话和私信（只读，已脱敏）。' },
  'interactions.card.proxySnapshots': { en: 'Proxy Snapshots', zh: '代理快照' },

  'interactions.stat.heartbeatHealth': { en: 'Heartbeat health', zh: '心跳健康度' },
  'interactions.stat.assetHitRate': { en: 'Asset hit rate', zh: '资产命中率' },
  'interactions.stat.events24h': { en: 'Events (24h)', zh: '事件数（24 小时）' },
  'interactions.stat.latency': { en: 'Latency p50/p95', zh: '延迟 p50/p95' },
  'interactions.stat.lastHelloOk': { en: 'Last hello OK', zh: '上次 hello 成功' },
  'interactions.stat.lastHeartbeatOk': { en: 'Last heartbeat OK', zh: '上次心跳成功' },

  'interactions.filter.layer': { en: 'Layer', zh: '层级' },
  'interactions.filter.all': { en: 'All', zh: '全部' },
  'interactions.filter.lifecycle': { en: 'Lifecycle', zh: '生命周期' },
  'interactions.filter.asset': { en: 'Asset', zh: '资产' },
  'interactions.filter.atp': { en: 'ATP', zh: 'ATP' },
  'interactions.filter.hideHeartbeats': { en: 'Hide heartbeats', zh: '隐藏心跳' },

  'interactions.col.time': { en: 'Time', zh: '时间' },
  'interactions.col.layer': { en: 'Layer', zh: '层级' },
  'interactions.col.kind': { en: 'Kind', zh: '类型' },
  'interactions.col.outcome': { en: 'Outcome', zh: '结果' },
  'interactions.col.status': { en: 'Status', zh: '状态码' },
  'interactions.col.latency': { en: 'Latency', zh: '延迟' },
  'interactions.col.detail': { en: 'Detail', zh: '详情' },

  'interactions.empty.filtered': { en: 'No events match the current filters.', zh: '当前过滤条件下无匹配事件。' },
  'interactions.empty.proxyRunning': { en: 'Proxy is running but no Hub events recorded yet — the next heartbeat tick will populate this table.', zh: '代理正在运行但尚未记录 Hub 事件——下一次心跳会填充此表。' },
  'interactions.empty.noProxy': { en: 'No Hub activity recorded yet. Hello/heartbeat/ATP events are produced by the proxy daemon — start it with <code>evolver run</code> (or <code>evolver fetch &lt;asset&gt;</code> to log a one-shot fetch).', zh: '尚未记录任何 Hub 活动。hello/heartbeat/ATP 事件由代理守护进程生成——使用 <code>evolver run</code> 启动它（或用 <code>evolver fetch &lt;asset&gt;</code> 触发一次抓取）。' },
  'interactions.empty.noAgent': { en: 'No agent interactions yet.', zh: '暂无智能体交互记录。' },
  'interactions.empty.proxyNotRunning': { en: 'Proxy not running. Start <code>evolver run</code> to enable live snapshots.', zh: '代理未运行。运行 <code>evolver run</code> 以启用实时快照。' },
  'interactions.snapshot.items': { en: 'items', zh: '项' },
  'interactions.snapshot.fields': { en: 'fields', zh: '字段' },
  'interactions.snapshot.unavailable': { en: 'unavailable', zh: '不可用' },

  // ---- Personality tab ----
  'personality.card.traits': { en: 'Personality Traits', zh: '人格特质' },
  'personality.card.detail': { en: 'Personality Detail', zh: '人格详情' },
  'personality.card.memoryGraph': { en: 'Memory Graph (last 100 events)', zh: '记忆图谱（最近 100 条事件）' },
  'personality.empty.chart': { en: 'No personality data yet.', zh: '暂无人格数据。' },
  'personality.empty.detail': { en: 'No personality data recorded yet.', zh: '暂未记录人格数据。' },
  'personality.empty.graph': { en: 'No memory graph events yet.', zh: '暂无记忆图谱事件。' },
  'personality.tooltip.kind': { en: 'Kind', zh: '类型' },
  'personality.tooltip.time': { en: 'Time', zh: '时间' },
  'personality.tooltip.eventId': { en: 'Event ID', zh: '事件 ID' },
  'personality.tooltip.gene': { en: 'Gene', zh: 'Gene' },
  'personality.tooltip.signals': { en: 'Signals', zh: '信号' },
  'personality.tooltip.outcome': { en: 'Outcome', zh: '结果' },
  'personality.tooltip.score': { en: 'Score', zh: '评分' },
  'personality.tooltip.mutation': { en: 'Mutation', zh: '变异' },
  'personality.tooltip.geneId': { en: 'Gene ID', zh: 'Gene ID' },
  'personality.tooltip.category': { en: 'Category', zh: '类别' },
  'personality.tooltip.signal': { en: 'Signal', zh: '信号' },
  'personality.tooltip.status': { en: 'Status', zh: '状态' },
  'personality.tooltip.lastScore': { en: 'Last score', zh: '上次评分' },
  'personality.tooltip.referenced': { en: 'Referenced', zh: '被引用' },
  'personality.tooltip.referencedTimes': { en: 'times', zh: '次' },
  'personality.cat.event': { en: 'Event', zh: '事件' },
  'personality.cat.gene': { en: 'Gene', zh: 'Gene' },
  'personality.cat.signal': { en: 'Signal', zh: '信号' },
  'personality.cat.outcome': { en: 'Outcome', zh: '结果' },
  'personality.cat.mutation': { en: 'Mutation', zh: '变异' },
  'personality.cat.asset': { en: 'Asset', zh: '资产' },
  'personality.cat.run': { en: 'Run', zh: '运行' },
};

// Status / outcome enum tokens — keep raw key as fallback so unknown
// statuses still render rather than disappearing.
const I18N_STATUS = {
  success: { en: 'success', zh: '成功' },
  completed: { en: 'completed', zh: '已完成' },
  running: { en: 'running', zh: '运行中' },
  pending: { en: 'pending', zh: '待处理' },
  failed: { en: 'failed', zh: '失败' },
  blocked: { en: 'blocked', zh: '已阻塞' },
  review_pending: { en: 'review pending', zh: '待审核' },
  abandoned: { en: 'abandoned', zh: '已废弃' },
  selected: { en: 'selected', zh: '已选择' },
  skipped: { en: 'skipped', zh: '已跳过' },
  unknown: { en: 'unknown', zh: '未知' },
  ok: { en: 'ok', zh: '正常' },
  recovered: { en: 'recovered', zh: '已恢复' },
  miss: { en: 'miss', zh: '未命中' },
};

// Hub event "kind" tokens (asset action / lifecycle kind / ATP order kind)
const I18N_ACTION = {
  // Asset actions
  asset_publish: { en: 'asset_publish', zh: '发布资产' },
  asset_reuse: { en: 'asset_reuse', zh: '复用资产' },
  asset_reference: { en: 'asset_reference', zh: '引用资产' },
  hub_search_hit: { en: 'hub_search_hit', zh: 'Hub 命中' },
  hub_search_miss: { en: 'hub_search_miss', zh: 'Hub 未命中' },
  hub_search_skip: { en: 'hub_search_skip', zh: 'Hub 跳过' },
  // Lifecycle kinds
  hello: { en: 'hello', zh: '握手' },
  heartbeat: { en: 'heartbeat', zh: '心跳' },
  fetch: { en: 'fetch', zh: '抓取' },
  // Layers (used in pill labels)
  lifecycle: { en: 'lifecycle', zh: '生命周期' },
  asset: { en: 'asset', zh: '资产' },
  atp: { en: 'atp', zh: 'ATP' },
};

function getLocale() {
  try {
    const v = localStorage.getItem(I18N_STORAGE_KEY);
    if (v && I18N_LOCALES.indexOf(v) !== -1) return v;
  } catch (_) {}
  return I18N_DEFAULT;
}

function setLocale(loc) {
  if (I18N_LOCALES.indexOf(loc) === -1) return;
  try { localStorage.setItem(I18N_STORAGE_KEY, loc); } catch (_) {}
  document.documentElement.setAttribute('data-locale', loc);
  document.documentElement.lang = loc === 'zh' ? 'zh-CN' : 'en';
}

function t(key, fallback) {
  const entry = I18N_DICT[key];
  if (!entry) return fallback != null ? fallback : key;
  return entry[getLocale()] || entry.en || key;
}

function tStatus(token) {
  if (!token) return '-';
  const entry = I18N_STATUS[token];
  if (!entry) return token;
  return entry[getLocale()] || entry.en || token;
}

function tAction(token) {
  if (!token) return '-';
  const entry = I18N_ACTION[token];
  if (!entry) return token;
  return entry[getLocale()] || entry.en || token;
}

// Apply data-i18n attributes to the live DOM.
//   data-i18n="key"                   → set textContent
//   data-i18n-html="key"              → set innerHTML (use sparingly; only
//                                        for strings in the dict that
//                                        intentionally contain markup like
//                                        <code>)
//   data-i18n-attr-<name>="key"       → set attribute (e.g. title)
function applyI18nDom(root) {
  const scope = root || document;
  scope.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.getAttribute('data-i18n');
    el.textContent = t(key);
  });
  scope.querySelectorAll('[data-i18n-html]').forEach((el) => {
    const key = el.getAttribute('data-i18n-html');
    el.innerHTML = t(key);
  });
  scope.querySelectorAll('*').forEach((el) => {
    for (const attr of el.attributes) {
      if (attr.name.indexOf('data-i18n-attr-') === 0) {
        const targetAttr = attr.name.slice('data-i18n-attr-'.length);
        el.setAttribute(targetAttr, t(attr.value));
      }
    }
  });
}
`;
