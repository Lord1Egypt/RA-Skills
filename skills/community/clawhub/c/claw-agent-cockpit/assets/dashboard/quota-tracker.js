#!/usr/bin/env node
/**
 * Coding Plan 额度追踪器（自学习版 v2）
 * 
 * 核心逻辑：
 *   预测调用数 = (当前token总量 - 基准token) / tokensPerCall
 * 
 * 学习流程：
 *   1. 第一次填实际值 → 初始化基准点，让预测=实际（冷启动）
 *   2. 后续填实际值 → 算两次之间的增量，学习 tokensPerCall
 *   3. tokensPerCall 变化 → 预测值自动跟着变
 * 
 * 实际值永远不碰，只校准 tokensPerCall 参数
 */

const fs = require('fs');
const path = require('path');

const QUOTA_FILE = path.join(__dirname, 'quota-data.json');
const AGENT_DATA_FILE = path.join(__dirname, 'agent-data.json');

const DEFAULT_TOKENS_PER_CALL = 1500;
const EMA_ALPHA = 0.4;

function loadQuotaData() {
  try { return JSON.parse(fs.readFileSync(QUOTA_FILE, 'utf8')); }
  catch { return null; }
}

function saveQuotaData(data) {
  data.lastUpdated = Date.now();
  fs.writeFileSync(QUOTA_FILE, JSON.stringify(data, null, 2));
}

function getTodayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
}

function getCurrentMonthKey() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}`;
}

function getCycleDays(q) {
  if (q.config.billingCycleStart && q.config.billingCycleEnd) {
    // 包含起始日和结束日：end - start + 1
    return Math.round((new Date(q.config.billingCycleEnd) - new Date(q.config.billingCycleStart)) / 86400000) + 1;
  }
  const d = new Date();
  return new Date(d.getFullYear(), d.getMonth()+1, 0).getDate();
}

function getDaysPassed(q) {
  if (q.config.billingCycleStart) {
    const s = new Date(q.config.billingCycleStart);
    const n = new Date();
    const sd = new Date(s.getFullYear(), s.getMonth(), s.getDate());
    const nd = new Date(n.getFullYear(), n.getMonth(), n.getDate());
    return Math.max(1, Math.round((nd - sd) / 86400000));
  }
  return new Date().getDate();
}

/** 读取当前所有 Agent 的 token 总量 */
function getCurrentTokenTotal() {
  try {
    const agents = JSON.parse(fs.readFileSync(AGENT_DATA_FILE, 'utf8'));
    return agents.reduce((sum, a) => sum + (a.tokens || 0), 0);
  } catch { return 0; }
}

/**
 * 核心预测函数
 * 预测调用数 = (当前token - 基准token) / tokensPerCall
 */
function predict(quota) {
  const tpc = quota.model?.tokensPerCall || DEFAULT_TOKENS_PER_CALL;
  const currentTokens = getCurrentTokenTotal();
  const baseline = quota.baselineTokenTotal;

  if (baseline == null) {
    // 还没初始化基准，用旧的累加值
    return quota.usage?.total || 0;
  }

  const tokenDelta = Math.max(0, currentTokens - baseline);
  return Math.round(tokenDelta / tpc);
}

/**
 * 学习函数：用户填实际值时调用
 * 
 * 第一次：用实际值反推基准点 baseline = currentTokens - actual * TPC
 * 后续：用两次实际值之间的增量学习 tokensPerCall
 */
function learnFromManual(quota) {
  if (!quota.manualHistory || quota.manualHistory.length < 1) return;
  if (!quota.model) quota.model = { tokensPerCall: DEFAULT_TOKENS_PER_CALL, calibrations: 0 };

  const history = [...quota.manualHistory].sort((a, b) => a.date.localeCompare(b.date));
  const currentTokens = getCurrentTokenTotal();
  const daysPassed = getDaysPassed(quota);

  if (history.length === 1) {
    // 第一次填实际值 → 初始化基准点 + 分摊到每日
    const actual = history[0].total;
    const tpc = quota.model.tokensPerCall;
    quota.baselineTokenTotal = currentTokens - (actual * tpc);
    quota.lastCalibrationTokens = currentTokens;
    quota.lastCalibrationManual = actual;
    quota.model.calibrations = 1;
    quota.model.lastCalibration = {
      type: 'init',
      date: history[0].date,
      actual,
      baseline: quota.baselineTokenTotal,
      tokensPerCall: tpc,
    };
    
    // 分摊到每日：actual / daysPassed
    const dailyAvg = Math.round(actual / daysPassed);
    const start = new Date(quota.config.billingCycleStart || '2026-04-11');
    const todayKey = getTodayKey();
    for (let i = 0; i < daysPassed; i++) {
      const d = new Date(start.getTime() + i * 86400000);
      const dateKey = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
      if (dateKey <= todayKey) {
        if (!quota.usage.daily[dateKey]) quota.usage.daily[dateKey] = 0;
        quota.usage.daily[dateKey] = dailyAvg;
      }
    }
    // 修正舍入误差，让总和 = actual
    const sum = Object.values(quota.usage.daily).reduce((a,b) => a+b, 0);
    const diff = actual - sum;
    if (diff !== 0 && quota.usage.daily[todayKey] != null) {
      quota.usage.daily[todayKey] += diff;
    }
    quota.usage.total = actual;
    
    console.log(`🎓 冷启动校准: baseline=${quota.baselineTokenTotal}, 预测将=${actual}, 日均=${dailyAvg}`);

  } else {
    // 有 ≥2 个数据点 → 用增量学习 tokensPerCall
    const prev = history[history.length - 2];
    const curr = history[history.length - 1];
    const callDelta = curr.total - prev.total;

    if (callDelta > 0 && quota.lastCalibrationTokens != null) {
      const tokenDelta = currentTokens - quota.lastCalibrationTokens;

      if (tokenDelta > 0) {
        const observedTPC = tokenDelta / callDelta;
        const oldTPC = quota.model.tokensPerCall;
        const newTPC = Math.max(50, Math.min(10000,
          Math.round(EMA_ALPHA * observedTPC + (1 - EMA_ALPHA) * oldTPC)
        ));

        quota.model.tokensPerCall = newTPC;
        quota.model.calibrations = (quota.model.calibrations || 0) + 1;
        quota.model.lastCalibration = {
          type: 'learn',
          date: curr.date,
          callDelta,
          tokenDelta,
          observedTPC: Math.round(observedTPC),
          oldTPC,
          newTPC,
        };

        // 注意：baseline 不动！只改 TPC
        // 预测值会因为 TPC 变化而自动调整

        console.log(`🎓 学习更新: tokensPerCall ${oldTPC} → ${newTPC} (观测:${Math.round(observedTPC)}, 校准#${quota.model.calibrations})`);
      }
    }

    // 更新快照，为下次学习做准备
    quota.lastCalibrationTokens = currentTokens;
    quota.lastCalibrationManual = curr.total;
  }
}

/**
 * 主更新函数
 */
function updateQuota() {
  let quota = loadQuotaData();
  if (!quota) { console.error('❌ 无法加载 quota-data.json'); return; }

  const currentMonth = getCurrentMonthKey();
  const today = getTodayKey();

  // 周期切换
  if (quota.config.billingCycleEnd) {
    const cycleEnd = new Date(quota.config.billingCycleEnd);
    if (new Date() >= cycleEnd) {
      console.log(`📅 计费周期结束，重置`);
      const cycleDays = getCycleDays(quota);
      const newStart = new Date(cycleEnd);
      const newEnd = new Date(newStart.getTime() + cycleDays * 86400000);
      quota.config.billingCycleStart = newStart.toISOString().slice(0, 10);
      quota.config.billingCycleEnd = newEnd.toISOString().slice(0, 10);
      quota.currentMonth = quota.config.billingCycleStart + '~' + quota.config.billingCycleEnd.slice(5);
      quota.usage = { total: 0, daily: {}, estimated: true };
      quota.baselineTokenTotal = getCurrentTokenTotal(); // 新周期基准 = 当前 token
      quota.lastCalibrationTokens = null;
      quota.lastCalibrationManual = null;
      quota.manualTotal = null;
      quota.manualHistory = [];
      quota.manualStats = null;
      // 保留学习到的 tokensPerCall
    }
    // 有自定义周期时，不检查自然月切换（避免重复重置）
  } else if (quota.currentMonth !== currentMonth) {
    console.log(`📅 新月份 ${currentMonth}，重置`);
    quota.currentMonth = currentMonth;
    quota.usage = { total: 0, daily: {}, estimated: true };
    quota.baselineTokenTotal = getCurrentTokenTotal();
    quota.lastCalibrationTokens = null;
    quota.lastCalibrationManual = null;
    quota.manualTotal = null;
    quota.manualHistory = [];
    quota.manualStats = null;
  }

  // 核心：用模型参数预测
  const predictedTotal = predict(quota);
  const prevTotal = quota.usage.total || 0;
  const dailyDelta = Math.max(0, predictedTotal - prevTotal);

  // 更新每日数据
  if (!quota.usage.daily) quota.usage.daily = {};
  if (!quota.usage.daily[today]) quota.usage.daily[today] = 0;
  quota.usage.daily[today] += dailyDelta;
  quota.usage.total = predictedTotal;

  // 统计
  const dailyValues = Object.values(quota.usage.daily).filter(v => v > 0);
  const daysPassed = getDaysPassed(quota);
  const cycleDays = getCycleDays(quota);
  const daysRemaining = Math.max(0, cycleDays - daysPassed);
  const dailyAvg = dailyValues.length > 0
    ? Math.round(dailyValues.reduce((a,b) => a+b, 0) / dailyValues.length)
    : 0;
  const projectedTotal = predictedTotal + (dailyAvg * daysRemaining);
  const usagePct = Math.round((predictedTotal / quota.config.monthlyQuota) * 100);
  const projectedPct = Math.round((projectedTotal / quota.config.monthlyQuota) * 100);
  const safeDailyLimit = daysRemaining > 0 ? Math.round((quota.config.monthlyQuota - predictedTotal) / daysRemaining) : 0;

  let alertLevel = 'normal';
  if (projectedPct > 100) alertLevel = 'danger';
  else if (projectedPct > 85) alertLevel = 'warning';
  else if (projectedPct > 70) alertLevel = 'caution';

  quota.stats = {
    usedTotal: predictedTotal,
    monthlyQuota: quota.config.monthlyQuota,
    usagePct,
    dailyAvg,
    projectedTotal,
    projectedPct,
    daysRemaining,
    safeDailyLimit,
    alertLevel,
    todayUsed: quota.usage.daily[today] || 0,
    tokensPerCall: quota.model?.tokensPerCall || DEFAULT_TOKENS_PER_CALL,
    calibrations: quota.model?.calibrations || 0,
  };

  saveQuotaData(quota);

  const tpc = quota.model?.tokensPerCall || DEFAULT_TOKENS_PER_CALL;
  console.log(`📊 预测: ${predictedTotal}/${quota.config.monthlyQuota} (${usagePct}%) | tpc:${tpc} | 校准:${quota.model?.calibrations || 0} | 实际:${quota.manualTotal || '-'}`);
}

module.exports = { updateQuota, learnFromManual, loadQuotaData, saveQuotaData };

if (require.main === module) {
  updateQuota();
}
