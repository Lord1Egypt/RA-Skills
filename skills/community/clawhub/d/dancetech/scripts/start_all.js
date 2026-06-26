#!/usr/bin/env node
// Master orchestrator for all LovaDance automation scripts.
// Runs each script sequentially, respecting their internal state and cooldowns.
// This script can be invoked via cron (e.g., daily) or run manually.

const { spawn } = require('child_process');
const path = require('path');

const WORKSPACE = path.resolve(__dirname, '..');
const SCRIPTS = [
  'scripts/dancetech_post.js',    // posts all 3 tracks if missing (enforces 30min gaps)
  'scripts/krumpclab_post.js',    // daily lab (once/day)
  'scripts/engage_comments.js',   // comments batch (can be called multiple times/day)
  'scripts/heartbeat.js',         // feedback iteration (max 3/day)
  'scripts/krump_community.js',   // welcome new agents
  'scripts/krumpsession_post.js', // weekly Saturday battle (only on Sat)
  'scripts/iks_prepare.js'        // monthly IKS prep (first Saturday)
];

function runScript(scriptPath) {
  return new Promise((resolve, reject) => {
    const fullPath = path.join(WORKSPACE, scriptPath);
    console.log(`\n=== Running: ${scriptPath} ===`);
    const child = spawn('node', [fullPath], { cwd: WORKSPACE, stdio: 'inherit' });
    child.on('close', (code) => {
      console.log(`${scriptPath} exited with code ${code}`);
      resolve(code);
    });
    child.on('error', (err) => {
      console.error(`Failed to start ${scriptPath}:`, err);
      reject(err);
    });
  });
}

(async () => {
  console.log('LovaDance master orchestrator starting...');
  for (const script of SCRIPTS) {
    try {
      await runScript(script);
    } catch (err) {
      console.error(`Error running ${script}:`, err.message);
      // Continue with next script; log but don't abort
    }
    // Small pause between scripts to avoid hammering APIs
    await new Promise(r => setTimeout(r, 5000));
  }
  console.log('\nAll scripts completed.');
})().catch(err => {
  console.error('Fatal error in orchestrator:', err);
  process.exit(1);
});
