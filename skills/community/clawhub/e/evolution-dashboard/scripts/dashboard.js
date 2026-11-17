'use strict';

const fs = require('fs');
const path = require('path');

function findWorkspace() {
  if (process.env.WORKSPACE_ROOT) return process.env.WORKSPACE_ROOT;
  const cwd = process.cwd();
  if (fs.existsSync(path.join(cwd, 'memory', 'evolution'))) return cwd;
  const home = process.env.HOME || process.env.USERPROFILE || cwd;
  const candidate = path.join(home, '.openclaw', 'workspace');
  if (fs.existsSync(path.join(candidate, 'memory', 'evolution'))) return candidate;
  return cwd;
}
const WORKSPACE = findWorkspace();
const GRAPH_PATH = path.join(WORKSPACE, 'memory', 'evolution', 'memory_graph.jsonl');
const STATE_PATH = path.join(WORKSPACE, 'memory', 'evolution', 'evolution_state.json');
const EVENTS_PATH = path.join(WORKSPACE, '.evolver', 'gep', 'events.jsonl');
const GENES_PATH = path.join(WORKSPACE, '.evolver', 'gep', 'genes.json');
const CAPSULES_PATH = path.join(WORKSPACE, '.evolver', 'gep', 'capsules.json');

function readJsonl(filePath) {
  if (!fs.existsSync(filePath)) return [];
  const lines = fs.readFileSync(filePath, 'utf8').split('\n').filter(Boolean);
  return lines.map(line => {
    try { return JSON.parse(line); } catch { return null; }
  }).filter(Boolean);
}

function readJson(filePath) {
  if (!fs.existsSync(filePath)) return {};
  try { return JSON.parse(fs.readFileSync(filePath, 'utf8')); } catch { return {}; }
}

function readEvolverEvents() {
  if (!fs.existsSync(EVENTS_PATH)) return [];
  const lines = fs.readFileSync(EVENTS_PATH, 'utf8').split('\n').filter(Boolean);
  return lines.map(line => {
    try { return JSON.parse(line); } catch { return null; }
  }).filter(Boolean);
}

function readEvolverGenes() {
  const data = readJson(GENES_PATH);
  return data.genes || [];
}

function readEvolverCapsules() {
  const data = readJson(CAPSULES_PATH);
  return data.capsules || [];
}

function generate() {
  const state = readJson(STATE_PATH);
  const evEvents = readEvolverEvents();
  const evGenes = readEvolverGenes();
  const evCapsules = readEvolverCapsules();
  const legacyEvents = readJsonl(GRAPH_PATH);

  // Prefer evolver events; fall back to legacy memory_graph
  const events = evEvents.length > 0 ? evEvents : legacyEvents;

  // Filter to EvolutionEvent only (exclude ValidationReport)
  const evoEvents = events.filter(e => e.type === 'EvolutionEvent');
  const valReports = events.filter(e => e.type === 'ValidationReport');

  // Overview
  const totalCycles = state.cycleCount || evoEvents.length;
  const successes = evoEvents.filter(e => e.outcome && e.outcome.status === 'success').length;
  const failures = evoEvents.filter(e => e.outcome && e.outcome.status === 'failed').length;
  const successRate = totalCycles > 0 ? (successes / totalCycles * 100).toFixed(1) : 0;
  const avgScore = evoEvents.length > 0
    ? (evoEvents.reduce((sum, e) => sum + (e.outcome ? e.outcome.score || 0 : 0), 0) / evoEvents.length).toFixed(3)
    : 0;

  // Gene performance (from events + known genes)
  const geneStats = {};
  for (const e of evoEvents) {
    const geneId = (e.genes_used && e.genes_used[0]) || 'unknown';
    if (!geneStats[geneId]) geneStats[geneId] = { success: 0, fail: 0, total: 0, scores: [] };
    geneStats[geneId].total++;
    if (e.outcome && e.outcome.status === 'success') geneStats[geneId].success++;
    else geneStats[geneId].fail++;
    if (e.outcome && e.outcome.score) geneStats[geneId].scores.push(e.outcome.score);
  }
  // Also include genes that exist but haven't been used yet
  for (const g of evGenes) {
    const gid = g.id || 'unknown';
    if (!geneStats[gid]) geneStats[gid] = { success: 0, fail: 0, total: 0, scores: [] };
  }

  // Signal trends
  const signalCounts = {};
  for (const e of evoEvents) {
    const sigs = e.signals || [];
    for (const s of sigs) { signalCounts[s] = (signalCounts[s] || 0) + 1; }
  }
  const topSignals = Object.entries(signalCounts)
    .sort((a, b) => b[1] - a[1])
    .slice(0, 10);

  // Capsule stats
  const capsuleSuccess = evCapsules.filter(c => c.outcome && c.outcome.status === 'success').length;
  const capsuleTotal = evCapsules.length;

  // Validation health
  const valFailures = valReports.filter(v => !v.overall_ok).length;

  // Stagnation detection
  const zeroChangeStreak = [];
  let currentZeroStreak = 0;
  for (const e of evoEvents) {
    const files = (e.blast_radius && e.blast_radius.files) || 0;
    if (files === 0 && e.outcome && e.outcome.status === 'success') {
      currentZeroStreak++;
    } else {
      if (currentZeroStreak > 0) zeroChangeStreak.push(currentZeroStreak);
      currentZeroStreak = 0;
    }
  }
  if (currentZeroStreak > 0) zeroChangeStreak.push(currentZeroStreak);
  const maxZeroStreak = zeroChangeStreak.length > 0 ? Math.max(...zeroChangeStreak) : 0;

  // Strategy lock detection (same gene+intent repeated)
  const comboCounts = {};
  for (const e of evoEvents) {
    const gene = (e.genes_used && e.genes_used[0]) || 'unknown';
    const intent = e.intent || '?';
    const key = intent + '|' + gene;
    comboCounts[key] = (comboCounts[key] || 0) + 1;
  }
  const lockedCombos = Object.entries(comboCounts)
    .filter(([, count]) => count >= 3)
    .sort((a, b) => b[1] - a[1]);

  // Timeline (last 10) with blast radius
  const timeline = evoEvents.slice(-10).map(e => ({
    ts: e.at || e.created_at,
    gene: (e.genes_used && e.genes_used[0]) || 'unknown',
    intent: e.intent || '?',
    status: e.outcome ? e.outcome.status : 'unknown',
    score: e.outcome ? e.outcome.score : null,
    files: (e.blast_radius && e.blast_radius.files) || 0,
    lines: (e.blast_radius && e.blast_radius.lines) || 0
  }));

  // Cycle efficiency: recent window analysis
  const recentWindow = evoEvents.slice(-12);
  const changedCycles = recentWindow.filter(e => ((e.blast_radius && e.blast_radius.files) || 0) > 0).length;
  const efficiency = recentWindow.length > 0 ? (changedCycles / recentWindow.length * 100).toFixed(1) : 0;

  // Saturation diagnosis
  const saturation = diagnoseSaturation({
    events: evoEvents,
    genes: evGenes,
    capsules: evCapsules,
    topSignals,
    lockedCombos,
    maxZeroStreak,
    efficiency
  });

  // Format output
  const lines = [];
  lines.push('=== EVOLUTION DASHBOARD ===');
  lines.push('');
  lines.push('[Overview]');
  lines.push('  Total Cycles: ' + totalCycles);
  lines.push('  Successes: ' + successes + ' | Failures: ' + failures);
  lines.push('  Success Rate: ' + successRate + '%');
  lines.push('  Avg Score: ' + avgScore);
  lines.push('  Capsules: ' + capsuleSuccess + '/' + capsuleTotal + ' solidified');
  if (valFailures > 0) lines.push('  Validation Failures: ' + valFailures);
  if (maxZeroStreak >= 3) lines.push('  WARNING: Stagnation detected (max ' + maxZeroStreak + ' consecutive zero-change cycles)');
  if (maxZeroStreak > 0) lines.push('  Current stagnation streak: ' + maxZeroStreak + ' cycles');
  lines.push('  Recent Efficiency (last ' + recentWindow.length + '): ' + efficiency + '% changed cycles');
  lines.push('');
  lines.push('[Gene Performance]');
  for (const [geneId, stats] of Object.entries(geneStats)) {
    const rate = stats.total > 0 ? (stats.success / stats.total * 100).toFixed(0) : 0;
    const avg = stats.scores.length > 0
      ? (stats.scores.reduce((a, b) => a + b, 0) / stats.scores.length).toFixed(3)
      : 'n/a';
    lines.push('  ' + geneId + ': ' + stats.success + '/' + stats.total + ' (' + rate + '%) avg=' + avg);
  }
  lines.push('');
  lines.push('[Top Signals]');
  for (const [signal, count] of topSignals) {
    lines.push('  ' + signal + ': ' + count);
  }
  lines.push('');
  if (lockedCombos.length > 0) {
    lines.push('[Strategy Lock]');
    for (const [combo, count] of lockedCombos) {
      const [intent, gene] = combo.split('|');
      lines.push('  ' + intent + ' + ' + gene + ' : ' + count + ' cycles (consider switching strategy)');
    }
    lines.push('');
  }
  if (maxZeroStreak >= 3) {
    lines.push('[Stagnation Alert]');
    lines.push('  ' + maxZeroStreak + ' consecutive cycles with 0 files changed.');
    lines.push('  Suggestion: switch gene or introduce a new skill to break the loop.');
    lines.push('');
  }
  lines.push('[Saturation Diagnosis]');
  lines.push('  Status: ' + saturation.status);
  lines.push('  Root Cause: ' + saturation.rootCause);
  if (saturation.recommendations.length > 0) {
    lines.push('  Recommendations:');
    for (const rec of saturation.recommendations) {
      lines.push('    - ' + rec);
    }
  }
  lines.push('');
  lines.push('[Recent Timeline]');
  for (const t of timeline) {
    const ts = t.ts ? new Date(t.ts).toISOString().replace('T', ' ').slice(0, 19) : '?';
    lines.push('  ' + ts + ' | ' + t.intent + ' | ' + t.gene + ' | ' + t.status + ' | score=' + (t.score != null ? t.score : '?') + ' | files=' + t.files + ',lines=' + t.lines);
  }
  lines.push('');
  lines.push('=== END DASHBOARD ===');

  return {
    overview: { totalCycles, successes, failures, successRate: parseFloat(successRate), avgScore: parseFloat(avgScore), capsules: { total: capsuleTotal, success: capsuleSuccess }, validationFailures: valFailures, stagnationWarning: maxZeroStreak >= 3, maxZeroStreak, lockedStrategy: lockedCombos.length > 0, efficiency: parseFloat(efficiency) },
    geneStats,
    topSignals,
    lockedCombos,
    timeline,
    saturation,
    text: lines.join('\n')
  };
}

// Cycle #0027: added saturation diagnosis and breakout recommendations to break empty loops.
function diagnoseSaturation({ events, genes, capsules, topSignals, lockedCombos, maxZeroStreak, efficiency }) {
  const recommendations = [];
  let rootCause = 'unknown';
  let status = 'stable';

  if (events.length === 0) {
    return { status: 'no_data', rootCause: 'no evolution events available', recommendations: ['run an evolver cycle first'] };
  }

  const dominantSignals = topSignals.slice(0, 3).map(([s]) => s);
  const hasLock = lockedCombos.length > 0;
  const hasZeroStreak = maxZeroStreak >= 3;
  const lowEfficiency = efficiency < 40;

  if (hasZeroStreak && lowEfficiency) {
    status = 'saturated';
    rootCause = 'repeated zero-change successes and low recent efficiency (' + efficiency + '%)';
  } else if (hasLock) {
    status = 'strategy_locked';
    rootCause = 'same intent+gene combination repeated ' + lockedCombos[0][1] + ' times';
  } else if (lowEfficiency) {
    status = 'inefficient';
    rootCause = 'recent cycles rarely produce tangible changes (' + efficiency + '% efficiency)';
  }

  if (dominantSignals.includes('evolution_saturation') || dominantSignals.includes('stable_success_plateau')) {
    recommendations.push('avoid repeating the same gene+intent; prefer explore or innovate');
  }
  if (dominantSignals.includes('empty_cycle_loop_detected')) {
    recommendations.push('break the empty loop by introducing a small tangible change or new skill');
  }
  if (dominantSignals.includes('repeated_tool_usage:exec') || dominantSignals.includes('tool_bypass')) {
    recommendations.push('reduce ad-hoc exec usage; prefer registered tools or single-shot commands');
  }
  if (dominantSignals.includes('protocol_drift')) {
    recommendations.push('review protocol output compliance; tighten JSON/GEP formatting rules');
  }
  if (hasLock) {
    recommendations.push('switch gene family for at least 1-2 cycles to reset strategy lock');
  }
  if (recommendations.length === 0 && status !== 'stable') {
    recommendations.push('collect more cycle data before changing strategy');
  }
  if (status === 'stable') {
    recommendations.push('system is healthy; consider opportunistic innovation only when useful');
  }

  return { status, rootCause, recommendations };
}


if (require.main === module) {
  const result = generate();
  console.log(result.text);
}

function quick() {
  const data = generate();
  const lines = [];
  lines.push('[Evolution Quick]');
  lines.push('  Cycles: ' + data.overview.totalCycles + ' | Success: ' + data.overview.successRate + '% | Capsules: ' + data.overview.capsules.success + '/' + data.overview.capsules.total);
  if (data.overview.stagnationWarning) {
    lines.push('  WARNING: Stagnation (' + data.overview.maxZeroStreak + ' zero-change cycles)');
  }
  if (data.saturation.status !== 'stable') {
    lines.push('  Status: ' + data.saturation.status + ' | ' + data.saturation.rootCause);
  } else {
    lines.push('  Status: healthy');
  }
  if (data.lockedCombos.length > 0) {
    const combo = data.lockedCombos[0][0];
    const count = data.lockedCombos[0][1];
    const [intent, gene] = combo.split('|');
    lines.push('  Locked: ' + intent + '+' + gene + ' x' + count);
  }
  lines.push('  Efficiency (last 12): ' + data.overview.efficiency + '%');
  return lines.join('\n');
}

module.exports = { generate, quick };
