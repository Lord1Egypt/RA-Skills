import { DATA_DIR, loadJson, debouncedSave } from "./persistence.ts";
import { resolve } from "path";
const COST_PATH = resolve(DATA_DIR, "cost_tracker.json");
const costState = {
  daily: [],
  sessionTokens: 0,
  sessionTurns: 0,
  totalTokens: 0,
  totalTurns: 0
};
function loadCostState() {
  const data = loadJson(COST_PATH, {
    daily: [],
    sessionTokens: 0,
    sessionTurns: 0,
    totalTokens: 0,
    totalTurns: 0
  });
  costState.daily = data.daily || [];
  costState.totalTokens = data.totalTokens || 0;
  costState.totalTurns = data.totalTurns || 0;
  costState.sessionTokens = 0;
  costState.sessionTurns = 0;
  const thirtyDaysAgo = new Date(Date.now() - 30 * 864e5).toISOString().slice(0, 10);
  costState.daily = costState.daily.filter((d) => d.date >= thirtyDaysAgo);
}
function saveCostState() {
  debouncedSave(COST_PATH, costState);
}
function estimateTokens(text) {
  if (!text) return 0;
  const cjk = (text.match(/[\u4e00-\u9fff\u3400-\u4dbf]/g) || []).length;
  const nonCjk = text.length - cjk;
  return Math.ceil(cjk * 1.5 + nonCjk * 0.25);
}
function recordTurnUsage(inputText, outputText, augmentTokenCount) {
  const inputTokens = estimateTokens(inputText);
  const outputTokens = estimateTokens(outputText);
  const total = inputTokens + outputTokens + augmentTokenCount;
  costState.sessionTokens += total;
  costState.sessionTurns++;
  costState.totalTokens += total;
  costState.totalTurns++;
  const today = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  let daily = costState.daily.find((d) => d.date === today);
  if (!daily) {
    daily = { date: today, inputTokens: 0, outputTokens: 0, augmentTokens: 0, turns: 0 };
    costState.daily.push(daily);
  }
  daily.inputTokens += inputTokens;
  daily.outputTokens += outputTokens;
  daily.augmentTokens += augmentTokenCount;
  daily.turns++;
  saveCostState();
}
function getCostSummary() {
  const lines = [
    "\u{1F4B0} Token Usage",
    "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
  ];
  lines.push(`Session: ~${costState.sessionTokens.toLocaleString()} tokens (${costState.sessionTurns} turns)`);
  const today = (/* @__PURE__ */ new Date()).toISOString().slice(0, 10);
  const todayUsage = costState.daily.find((d) => d.date === today);
  if (todayUsage) {
    const todayTotal = todayUsage.inputTokens + todayUsage.outputTokens + todayUsage.augmentTokens;
    lines.push(`Today: ~${todayTotal.toLocaleString()} tokens (${todayUsage.turns} turns)`);
    lines.push(`  Input: ${todayUsage.inputTokens.toLocaleString()} | Output: ${todayUsage.outputTokens.toLocaleString()} | Augments: ${todayUsage.augmentTokens.toLocaleString()}`);
  }
  const sevenDaysAgo = new Date(Date.now() - 7 * 864e5).toISOString().slice(0, 10);
  const recentDays = costState.daily.filter((d) => d.date >= sevenDaysAgo);
  if (recentDays.length > 0) {
    const avgTokens = recentDays.reduce((s, d) => s + d.inputTokens + d.outputTokens + d.augmentTokens, 0) / recentDays.length;
    const avgTurns = recentDays.reduce((s, d) => s + d.turns, 0) / recentDays.length;
    lines.push(`7d avg: ~${Math.round(avgTokens).toLocaleString()} tokens/day (${Math.round(avgTurns)} turns/day)`);
  }
  lines.push(`All-time: ~${costState.totalTokens.toLocaleString()} tokens (${costState.totalTurns} turns)`);
  if (todayUsage && todayUsage.inputTokens > 0) {
    const overhead = todayUsage.augmentTokens / (todayUsage.inputTokens + todayUsage.augmentTokens) * 100;
    lines.push(`Augment overhead: ${overhead.toFixed(1)}%`);
  }
  return lines.join("\n");
}
function getDailyUsageData() {
  const dates = costState.daily.map((d) => d.date.slice(5));
  const tokens = costState.daily.map((d) => d.inputTokens + d.outputTokens + d.augmentTokens);
  const turns = costState.daily.map((d) => d.turns);
  return { dates, tokens, turns };
}
const costTrackerModule = {
  id: "cost-tracker",
  name: "Token \u6210\u672C\u8FFD\u8E2A",
  features: ["cost_tracker"],
  priority: 10,
  init() {
    loadCostState();
  }
};
export {
  costState,
  costTrackerModule,
  getCostSummary,
  getDailyUsageData,
  recordTurnUsage
};
