#!/usr/bin/env node
/**
 * BRAIN.md Cortex Engine
 * 
 * Self-review process that examines pathway weights and adjusts them.
 * The meta-script — the part that modifies everything else.
 * 
 * Commands:
 *   review              — run self-review cycle (strengthen/weaken/decay)
 *   record <id> <bool>  — record a pathway outcome (creates if new)
 *   status              — show all pathways with visual bars
 *   prune               — remove pathways with weight <= 0.05
 */

const fs = require('fs');
const path = require('path');

// Resolve paths relative to brain root (parent of cortex/)
const BRAIN_ROOT = process.env.BRAIN_ROOT || path.join(__dirname, '..');
const WEIGHTS_PATH = path.join(BRAIN_ROOT, 'weights', 'pathways.json');
const MUTATIONS_DIR = path.join(BRAIN_ROOT, 'mutations');

// === Configurable thresholds (self-modifiable) ===
const THRESHOLDS = {
  strengthenRate: 0.05,
  strengthenMinSuccessRate: 0.8,
  strengthenMinFires: 3,
  weakenRate: 0.10,
  weakenMaxSuccessRate: 0.5,
  weakenMinFires: 3,
  decayRate: 0.02,
  decayOnsetDays: 7,
  maxWeight: 0.95,
  minWeight: 0.05,
  newPathwayWeight: 0.3,
  instinctFloor: 0.8,
  reflexFloor: 0.2,
};

function loadWeights() {
  if (!fs.existsSync(WEIGHTS_PATH)) {
    return { version: 1, pathways: {} };
  }
  return JSON.parse(fs.readFileSync(WEIGHTS_PATH, 'utf8'));
}

function saveWeights(data) {
  data.version = (data.version || 0) + 1;
  fs.writeFileSync(WEIGHTS_PATH, JSON.stringify(data, null, 2));
}

function logMutation(mutation) {
  if (!fs.existsSync(MUTATIONS_DIR)) {
    fs.mkdirSync(MUTATIONS_DIR, { recursive: true });
  }
  const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
  const logPath = path.join(MUTATIONS_DIR, `${timestamp}.json`);
  fs.writeFileSync(logPath, JSON.stringify({
    ...mutation,
    timestamp: new Date().toISOString()
  }, null, 2));
  console.log(`📝 Mutation logged: ${mutation.type} → ${mutation.target}`);
}

function getMinWeight(pathwayId) {
  if (pathwayId.startsWith('instinct:')) return THRESHOLDS.instinctFloor;
  if (pathwayId.startsWith('reflex:')) return THRESHOLDS.reflexFloor;
  return THRESHOLDS.minWeight;
}

function review() {
  const data = loadWeights();
  const mutations = [];

  for (const [id, p] of Object.entries(data.pathways)) {
    const minW = getMinWeight(id);

    // Strengthen: high success rate
    if (p.fires >= THRESHOLDS.strengthenMinFires && 
        p.successes / p.fires >= THRESHOLDS.strengthenMinSuccessRate) {
      if (p.weight < THRESHOLDS.maxWeight) {
        const oldWeight = p.weight;
        p.weight = Math.min(THRESHOLDS.maxWeight, p.weight + THRESHOLDS.strengthenRate);
        mutations.push({
          type: 'strengthen', target: id,
          from: oldWeight, to: p.weight,
          reason: `${p.successes}/${p.fires} success rate`
        });
      }
    }

    // Weaken: low success rate
    if (p.fires >= THRESHOLDS.weakenMinFires && 
        p.successes / p.fires < THRESHOLDS.weakenMaxSuccessRate) {
      if (p.weight > minW) {
        const oldWeight = p.weight;
        p.weight = Math.max(minW, p.weight - THRESHOLDS.weakenRate);
        mutations.push({
          type: 'weaken', target: id,
          from: oldWeight, to: p.weight,
          reason: `${p.successes}/${p.fires} success rate`
        });
      }
    }

    // Decay: unused pathways fade
    if (p.lastFired) {
      const daysSince = (Date.now() - new Date(p.lastFired).getTime()) / 86400000;
      if (daysSince > THRESHOLDS.decayOnsetDays && p.weight > minW) {
        const oldWeight = p.weight;
        p.weight = Math.max(minW, p.weight - THRESHOLDS.decayRate);
        mutations.push({
          type: 'decay', target: id,
          from: oldWeight, to: p.weight,
          reason: `${Math.floor(daysSince)} days since last use`
        });
      }
    }
  }

  if (mutations.length > 0) {
    saveWeights(data);
    mutations.forEach(m => logMutation(m));
    console.log(`\n🧠 Cortex review: ${mutations.length} mutations applied`);
  } else {
    console.log('🧠 Cortex review: no mutations needed');
  }

  return mutations;
}

function recordOutcome(pathwayId, success, notes = '') {
  const data = loadWeights();

  if (!data.pathways[pathwayId]) {
    data.pathways[pathwayId] = {
      weight: THRESHOLDS.newPathwayWeight,
      fires: 0, successes: 0, failures: 0,
      lastFired: new Date().toISOString(),
      notes: notes
    };
    logMutation({
      type: 'neurogenesis', target: pathwayId,
      reason: `New pathway created: ${notes}`
    });
  }

  const p = data.pathways[pathwayId];
  p.fires++;
  if (success) p.successes++; else p.failures++;
  p.lastFired = new Date().toISOString();
  if (notes) p.notes = notes;

  saveWeights(data);
  console.log(`📊 ${pathwayId}: ${success ? '✅' : '❌'} (${p.weight.toFixed(2)} weight, ${p.successes}/${p.fires} success)`);
}

function prunePathways() {
  const data = loadWeights();
  let pruned = 0;

  for (const [id, p] of Object.entries(data.pathways)) {
    if (p.weight <= THRESHOLDS.minWeight && !id.startsWith('instinct:')) {
      logMutation({
        type: 'prune', target: id,
        from: p.weight, to: 0,
        reason: `Weight ${p.weight} at or below minimum`
      });
      delete data.pathways[id];
      pruned++;
    }
  }

  if (pruned > 0) {
    saveWeights(data);
    console.log(`\n🪓 Pruned ${pruned} dead pathways`);
  } else {
    console.log('🧠 No pathways to prune');
  }
}

function showStatus() {
  const data = loadWeights();
  const pathways = Object.entries(data.pathways);

  if (pathways.length === 0) {
    console.log('🧠 No pathways yet. Record some outcomes to start learning.');
    return;
  }

  console.log('🧠 Neural Pathway Status\n');
  const sorted = pathways.sort((a, b) => b[1].weight - a[1].weight);

  for (const [id, p] of sorted) {
    const bar = '█'.repeat(Math.round(p.weight * 10)) + '░'.repeat(10 - Math.round(p.weight * 10));
    const rate = p.fires > 0 ? `${Math.round(p.successes / p.fires * 100)}%` : 'new';
    console.log(`  ${bar} ${p.weight.toFixed(2)} ${id} (${rate}, ${p.fires} fires)`);
    if (p.notes) console.log(`             ${p.notes}`);
  }
}

// CLI
const cmd = process.argv[2];
switch (cmd) {
  case 'review': review(); break;
  case 'record':
    recordOutcome(process.argv[3], process.argv[4] === 'true', process.argv.slice(5).join(' '));
    break;
  case 'status': showStatus(); break;
  case 'prune': prunePathways(); break;
  default:
    console.log('BRAIN.md Cortex Engine');
    console.log('Usage: review.js <review|record|status|prune>');
    console.log('  review                    — run self-review cycle');
    console.log('  record <id> <true|false>  — record pathway outcome');
    console.log('  status                    — show all pathways');
    console.log('  prune                     — remove dead pathways');
}
