#!/usr/bin/env node
/**
 * auto-evolve.js — Full automation: evolver run → bridge → solidify
 *
 * Usage: node skills/evolver-open-space-bridge/scripts/auto-evolve.js
 */

const { execSync, exec } = require('child_process');
const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.WORKSPACE_ROOT || process.cwd();
const EVOLUTION_DIR = path.join(WORKSPACE, 'memory', 'evolution');
const OPENSPACE_VENV = '/home/admin147258/openspace-venv';
const BRIDGE_SCRIPT = '/tmp/evolver-bridge/bridge.js';

function log(msg) { console.log(`[auto-evolve] ${msg}`); }

function runEvolver() {
  const outFile = path.join(EVOLUTION_DIR, 'last_run_stdout.txt');
  fs.mkdirSync(EVOLUTION_DIR, { recursive: true });

  log('Step 1: Running evolver run...');
  try {
    execSync(
      `powershell -NoProfile -Command "evolver run | Out-File -FilePath '${outFile}' -Encoding utf8"`,
      { cwd: WORKSPACE, timeout: 120_000, stdio: 'inherit' }
    );
  } catch (e) {
    if (!fs.existsSync(outFile) || fs.statSync(outFile).size === 0) {
      log(`evolver run failed: ${e.message}`);
      process.exit(1);
    }
  }

  const raw = fs.readFileSync(outFile, 'utf-8');
  const gepStart = raw.indexOf('GEP');
  const gepEnd = raw.indexOf('Evolver finished.');
  if (gepStart === -1) {
    log('ERROR: no GEP prompt in output');
    process.exit(1);
  }

  const gep = raw.slice(gepStart, gepEnd > gepStart ? gepEnd : undefined).trim();
  const cycleId = (gep.match(/Cycle #(\d+)/) || [])[1] || '????';
  const runId = `run_${Date.now()}`;
  const filename = `gep_prompt_Cycle_#${cycleId.padStart(4, '0')}_${runId}.txt`;
  const outPath = path.join(EVOLUTION_DIR, filename);
  fs.writeFileSync(outPath, gep, 'utf-8');

  log(`Saved GEP prompt: ${filename} (${gep.length} bytes)`);

  return { gepPromptPath: outPath, cycleId: cycleId.padStart(4, '0'), runId };
}

function runBridge(gepPromptPath, cycleId) {
  log('Step 2: Running bridge to OpenSpace...');
  const wslPrompt = `/mnt/${gepPromptPath.replace(/\\/g, '/').replace(/^([A-Za-z]):\//, (m, drive) => `${drive.toLowerCase()}/`)}`;
  const outputDir = `/mnt/${EVOLUTION_DIR.replace(/\\/g, '/').replace(/^([A-Za-z]):\//, (m, drive) => `${drive.toLowerCase()}/`)}/openspace_output_cycle_${cycleId}`;
  const cmd = `wsl -d Ubuntu bash -lc "cd /tmp/evolver-bridge && node bridge.js --prompt '${wslPrompt}' --output '${outputDir}'"`;

  try {
    const result = execSync(cmd, {
      cwd: WORKSPACE,
      timeout: 300_000,
      encoding: 'utf-8',
      stdio: 'pipe'
    });
    log(`Bridge output: ${result.slice(0, 500)}`);
    return { success: true, outputDir };
  } catch (e) {
    log(`Bridge failed: ${e.message}`);
    return { success: false, error: e.message };
  }
}

function validateOutput(outputDir) {
  log('Step 3: Validating bridge output...');
  const wslOutput = outputDir || `/mnt${EVOLUTION_DIR.replace(/\\/g, '/')}/openspace_output`;
  
  try {
    const checkCmd = `wsl -d Ubuntu bash -lc "if [ -f '${wslOutput}' ]; then echo FILE; wc -l '${wslOutput}'; else echo MISSING; fi"`;
    const result = execSync(checkCmd, { encoding: 'utf-8', timeout: 10_000 }).trim();
    
    if (result.startsWith('MISSING')) {
      log('ERROR: Bridge output not found');
      return false;
    }

    const lineCount = parseInt(result.split('\n')[1] || '0', 10);
    log(`Output file has ${lineCount} lines`);

    if (lineCount < 5) {
      log('ERROR: Output has fewer than 5 expected lines');
      return false;
    }

    log('Output validation passed');
    return true;
  } catch (e) {
    log(`Validation failed: ${e.message}`);
    return false;
  }
}

function runSolidify() {
  log('Step 4: Running evolver solidify...');
  try {
    execSync('evolver solidify', { cwd: WORKSPACE, timeout: 120_000, stdio: 'inherit' });
    log('Solidify completed');
    return true;
  } catch (e) {
    log(`Solidify failed: ${e.message}`);
    return false;
  }
}

function main() {
  log('Starting automated evolution cycle...');

  const { gepPromptPath, cycleId } = runEvolver();
  const bridgeResult = runBridge(gepPromptPath, cycleId);

  if (!bridgeResult.success) {
    log('Bridge failed, stopping before solidify');
    process.exit(1);
  }

  const valid = validateOutput(bridgeResult.outputDir);
  if (!valid) {
    log('Output validation failed, stopping before solidify');
    process.exit(1);
  }

  runSolidify();
  log('Automated cycle complete');
}

main();
