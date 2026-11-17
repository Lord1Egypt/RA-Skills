#!/usr/bin/env node
/**
 * Evolver Bridge Skill — Full cycle orchestration
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.WORKSPACE_ROOT || process.cwd();
const EVOLUTION_DIR = path.join(WORKSPACE, 'memory', 'evolution');

function fullCycle() {
  const outFile = path.join(EVOLUTION_DIR, 'last_run_stdout.txt');
  fs.mkdirSync(EVOLUTION_DIR, { recursive: true });

  // Step 1: run evolver
  try {
    execSync(`evolver run > '${outFile}' 2>&1`, {
      cwd: WORKSPACE,
      timeout: 120_000,
      stdio: 'inherit'
    });
  } catch (e) {
    if (!fs.existsSync(outFile) || fs.statSync(outFile).size === 0) {
      console.error(`[evolver-bridge] run failed: ${e.message}`);
      process.exit(1);
    }
  }

  // Step 2: verify prompt captured
  const raw = fs.readFileSync(outFile, 'utf-8');
  const gepStart = raw.indexOf('GEP');
  if (gepStart === -1) {
    console.error('[evolver-bridge] No GEP prompt found');
    process.exit(1);
  }
  console.log('[evolver-bridge] GEP prompt captured');

  // Step 3: save prompt if needed
  const cycleMatch = raw.match(/Cycle #(\d+)/);
  if (cycleMatch) {
    const cycleId = cycleMatch[1];
    const promptFile = path.join(EVOLUTION_DIR, `gep_prompt_Cycle_#${cycleId}_run_${Date.now()}.txt`);
    fs.writeFileSync(promptFile, raw.slice(gepStart).trim());
    console.log('[evolver-bridge] Prompt saved to', promptFile);
  }

  console.log('[evolver-bridge] Full cycle complete. Review the prompt, then run: evolver solidify');
}

const cmd = process.argv[2];
if (!cmd || cmd === 'run') {
  fullCycle();
} else {
  console.log('Usage: node index.js [run]');
}
