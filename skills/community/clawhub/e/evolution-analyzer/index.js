const fs = require('fs');
const path = require('path');

const EVOLUTION_DIR = path.resolve(__dirname, '../../memory/evolution');
const DASHBOARD_PATH = path.resolve(__dirname, '../evolution-dashboard/scripts/dashboard.js');

function loadJson(file) {
  const p = path.join(EVOLUTION_DIR, file);
  if (!fs.existsSync(p)) return null;
  return JSON.parse(fs.readFileSync(p, 'utf8'));
}

function loadDashboard() {
  try {
    const mod = require(DASHBOARD_PATH);
    if (typeof mod.generate === 'function') return mod.generate();
  } catch (e) {
    // fallback below
  }
  return null;
}

function analyze(options = {}) {
  const state = loadJson('evolution_state.json') || {};
  const progress = loadJson('cycle_progress.json') || {};
  const narrativePath = path.join(EVOLUTION_DIR, 'evolution_narrative.md');
  const narrative = fs.existsSync(narrativePath) ? fs.readFileSync(narrativePath, 'utf8') : '';

  const totalCycles = typeof state.totalCycles === 'number' ? state.totalCycles : Number(state.totalCycles || 0);
  const totalCyclesFinal = totalCycles > 0 ? totalCycles : Number(state.cycleCount || 0);
  const lastCycleId = progress.cycleId || null;
  const currentGene = progress.gene_id || null;

  const failureMatches = narrative.match(/INNOVATE - failed/g) || [];
  const optimizeFailureMatches = narrative.match(/OPTIMIZE - failed/g) || [];
  const repairFailureMatches = narrative.match(/REPAIR - failed/g) || [];
  const recentFailures = failureMatches.length + optimizeFailureMatches.length + repairFailureMatches.length;

  const signals = Array.isArray(progress.signals) ? progress.signals : [];
  const hasToolBypass = signals.includes('tool_bypass');
  const hasEmptyCycleLoop = signals.includes('empty_cycle_loop_detected');
  const hasPlateau = signals.includes('stable_success_plateau');

  const recommendations = [];
  let suggestedNext = 'Run a narrow INNOVATE cycle with explicit validation. Another repair/optimize cycle is not likely to help.';
  const dashboard = loadDashboard();

  if (!lastCycleId) {
    recommendations.push('No active cycle context found; rerun evolve-cycle.js before analysis.');
    suggestedNext = 'Rerun evolve-cycle.js to establish active cycle context before analyzing.';
  } else if (recentFailures >= 3) {
    recommendations.push('Switch intent toward low-risk INNOVATE with narrow scope and explicit validation.');
    suggestedNext = 'Try a low-risk INNOVATE cycle with max_files<=4 and one explicit validation command.';
  }

  if (hasToolBypass) {
    recommendations.push('tool_bypass detected: prefer a registered skill or built-in tool over ad-hoc shell workarounds in the next cycle.');
  }
  if (hasEmptyCycleLoop) {
    recommendations.push('empty_cycle_loop_detected: change the gene or target domain instead of repeating the same optimization.');
  }
  if (hasPlateau) {
    recommendations.push('stable_success_plateau: recent successes may mask stagnation; introduce one new capability or output format.');
  }

  if (dashboard && dashboard.stagnationHealth) {
    const { healthScore, stagnLabel, scorePlateau, signalDiversity, failureStreak, healthLabel } = dashboard.stagnationHealth;

    if (healthScore < 0.5) {
      recommendations.push('Evolution health is at risk; reduce scope and run validation before solidify.');
    }
    if (stagnLabel === 'High' || scorePlateau > 0.9) {
      recommendations.push('Score plateau detected; pivot to a new signal or capability instead of repeating the same gene.');
    }
    if (signalDiversity < 0.5) {
      recommendations.push('Low signal diversity; broaden inputs or explore a new domain before the next cycle.');
    }
    if (failureStreak >= 2) {
      recommendations.push('Recent failure streak detected; switch to low-risk innovation with smaller blast radius.');
    }

    if (recentFailures < 3) {
      if (healthScore < 0.5 || stagnLabel === 'High' || scorePlateau > 0.9) {
        suggestedNext = 'Pivot to a new signal/capability; stop repeating the current gene.';
      } else if (signalDiversity < 0.5) {
        suggestedNext = 'Broaden inputs or explore a new domain with a small skill or analysis target.';
      }
    }

    if (healthLabel && !recommendations.some(r => r.includes('Evolution health is at risk'))) {
      recommendations.push('Current evolution health: ' + healthLabel + '. Keep changes reversible and validation explicit.');
    }
  }

  if (!recommendations.length) {
    recommendations.push('No critical stagnation detected; continue current mix with one smaller validation-focused cycle.');
  }

  const result = {
    totalCycles: totalCyclesFinal,
    lastCycleId,
    currentGene,
    recentFailures,
    signals,
    recommendations,
    suggestedNext,
    source: 'memory/evolution',
    stagnationHealth: dashboard ? dashboard.stagnationHealth : null
  };

  if (options.json) return result;
  const lines = [
    '=== EVOLUTION ANALYZER ===',
    '',
    'Cycles: ' + result.totalCycles,
    'Current gene: ' + (result.currentGene || 'none'),
    'Recent failures: ' + result.recentFailures,
    'Signals: ' + (signals.length ? signals.join(', ') : 'none'),
    '',
    'Recommendations:',
    ...recommendations.map(r => ' - ' + r),
    '',
    'Suggested next action:',
    ' - ' + suggestedNext
  ];
  if (result.stagnationHealth) {
    lines.push('');
    lines.push('Health: ' + (result.stagnationHealth.healthLabel || '?'));
    lines.push('Stagnation: ' + (result.stagnationHealth.stagnLabel || '?'));
    lines.push('Score plateau: ' + result.stagnationHealth.scorePlateau);
  }
  lines.push('');
  lines.push('=== END ANALYZER ===');
  return lines.join('\n');
}

function main() {
  const wantJson = process.argv.includes('--json');
  const result = analyze({ json: wantJson });
  if (wantJson) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(result);
  }
}

module.exports = { analyze, main };
