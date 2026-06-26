#!/usr/bin/env node
/**
 * Desktop Automation Skill — OpenClaw Integration
 * Usage: node skill.js <action> '<json args>'
 * Example: node skill.js click '{"x":100,"y":200}'
 */

const { spawnSync } = require('child_process');
const path = require('path');

function runPython(action, params = {}) {
  const script = path.join(__dirname, 'lib', 'automation.py');
  const args = [script, action, JSON.stringify(params)];
  const result = spawnSync('python', args, { encoding: 'utf-8' });

  if (result.status !== 0) {
    return { status: 'error', message: result.stderr || 'Python error' };
  }

  try {
    return JSON.parse(result.stdout);
  } catch (e) {
    return { status: 'error', message: 'Invalid JSON from Python: ' + e.message };
  }
}

// OpenClaw sends tasks via command line arguments
if (process.argv.length < 3) {
  console.error(JSON.stringify({ status: 'error', message: 'Missing action' }));
  process.exit(1);
}

const action = process.argv[2];
const params = process.argv[3] ? JSON.parse(process.argv[3]) : {};

const output = runPython(action, params);
console.log(JSON.stringify(output));
process.exit(output.status === 'ok' ? 0 : 1);
