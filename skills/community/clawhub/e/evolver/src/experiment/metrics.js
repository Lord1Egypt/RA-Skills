// src/experiment/metrics.js
//
// Pure, table-driven mapping from a human metric label (e.g. "完成耗时 (s)",
// "轮次", "token", "通过率") onto a per-arm field + comparison direction.
// No I/O, no side effects -- safe to unit-test in isolation.
'use strict';

function num(v, fallback) {
  const n = Number(v);
  return Number.isFinite(n) ? n : (fallback === undefined ? 0 : fallback);
}

function round(n, digits) {
  const f = Math.pow(10, digits);
  return Math.round((num(n) + Number.EPSILON) * f) / f;
}

// Ordered rules. The FIRST rule whose any keyword is a (case-insensitive)
// substring of the metric label wins. Order matters: pass-rate / rounds /
// tokens / cost are checked before duration so a label like "通过率" is not
// swallowed by a looser rule.
const METRIC_RULES = [
  { keys: ['通过率', 'pass', 'success', 'accuracy', '准确', '正确率'], field: 'passRate', lowerIsBetter: false },
  { keys: ['轮次', 'turn', 'round', 'step', 'iteration', '迭代'], field: 'rounds', lowerIsBetter: true },
  { keys: ['token', '令牌'], field: 'tokensTotal', lowerIsBetter: true },
  { keys: ['成本', 'cost', 'usd', '价格', '费用'], field: 'costUsd', lowerIsBetter: true },
  { keys: ['耗时', 'duration', 'latency', '延迟', '秒', 'second', '(s)', 'time'], field: 'durationMs', lowerIsBetter: true },
];

/**
 * Resolve a metric label to the per-arm field used for scoring, the
 * comparison direction, and the display unit.
 *
 * @param {string} metricStr
 * @returns {{ metricField: string, lowerIsBetter: boolean, scoreUnit: string, recognized: boolean }}
 */
function deriveMetric(metricStr) {
  const m = String(metricStr || '').toLowerCase();
  for (const rule of METRIC_RULES) {
    if (rule.keys.some((k) => m.includes(String(k).toLowerCase()))) {
      if (rule.field === 'durationMs') {
        // Seconds-flavoured labels ("(s)", "秒", "seconds") -> report in seconds.
        if (/\(s\)|秒|second/.test(m)) {
          return { metricField: 'durationSec', lowerIsBetter: true, scoreUnit: 'seconds', recognized: true };
        }
        return { metricField: 'durationMs', lowerIsBetter: true, scoreUnit: 'ms', recognized: true };
      }
      return { metricField: rule.field, lowerIsBetter: rule.lowerIsBetter, scoreUnit: 'raw', recognized: true };
    }
  }
  // Unrecognized -> degrade to pass-rate (higher is better). Caller records a warning.
  return { metricField: 'passRate', lowerIsBetter: false, scoreUnit: 'raw', recognized: false };
}

/**
 * Pull the scalar score for one arm given the resolved metric field.
 *
 * @param {object} arm  a normalized arm (see comparison.normalizeArm)
 * @param {string} metricField
 * @returns {number}
 */
function scoreArm(arm, metricField) {
  if (!arm) return 0;
  switch (metricField) {
    case 'durationSec': return round(num(arm.durationMs) / 1000, 2);
    case 'durationMs': return num(arm.durationMs);
    case 'rounds': return num(arm.rounds);
    case 'tokensTotal': return num(arm.tokensTotal);
    case 'costUsd': return round(num(arm.costUsd), 4);
    case 'passRate': return round(num(arm.passRate), 4);
    default: return round(num(arm.passRate), 4);
  }
}

module.exports = { deriveMetric, scoreArm, METRIC_RULES, round, num };
