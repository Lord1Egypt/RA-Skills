#!/usr/bin/env node
/**
 * Poll Gemini Deep Research status until completed or timed out.
 * Reads from task.json in the same dir.
 * Usage: node poll-research.js <task_dir>
 */
import { spawn } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const __dirname = fileURLToPath(new URL('.', import.meta.url));

const TASK_DIR    = process.argv[2] || '.';
const INTERVAL    = 300;   // 5 minutes
const MAX_POLLS   = 8;     // 8 × 5min = 40min

const EXT_PATH = join(require('os').homedir(), '.gemini', 'extensions', 'gemini-deep-research');

function log(msg) {
  console.error('[Poll] ' + msg);
  const f = TASK_DIR + '/poll.log';
  try {
    require('fs').appendFileSync(f, new Date().toISOString() + ' ' + msg + '\n');
  } catch {}
}

function sendCommand(cmd, timeout = 600000) {
  return new Promise((resolve, reject) => {
    const server = spawn('node', ['dist/index.js'], {
      cwd: EXT_PATH,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    let timedOut = false;
    const to = setTimeout(() => { timedOut = true; server.kill(); }, timeout);
    const lines = [];
    server.stdout.on('data', d => lines.push(d.toString()));
    server.on('error', err => { clearTimeout(to); reject(err); });
    server.on('exit', code => {
      clearTimeout(to);
      if (timedOut) reject(new Error('MCP timeout (>10min for single call)'));
      else if (code !== 0) reject(new Error('MCP server exited code ' + code));
      else {
        const full = lines.join('');
        try { resolve(JSON.parse(full)); }
        catch { reject(new Error('Invalid JSON: ' + full.slice(0, 200))); }
      }
    });
    server.stdin.write(JSON.stringify(cmd) + '\n');
  });
}

async function main() {
  const taskFile = join(TASK_DIR, 'task.json');
  const task = JSON.parse(readFileSync(taskFile, 'utf8'));

  if (!task.researchId) throw new Error('No researchId in task.json — run start-research.js first');
  log('Starting. Research ID: ' + task.researchId);

  // Init
  await sendCommand({
    jsonrpc: '2.0', id: 1, method: 'initialize',
    params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'gemini-dr', version: '1.0' } }
  });

  for (let poll = 1; poll <= MAX_POLLS; poll++) {
    log(`Poll ${poll}/${MAX_POLLS}`);

    const res = await sendCommand({
      jsonrpc: '2.0', id: 2, method: 'tools/call',
      params: { name: 'research_status', arguments: { id: task.researchId } }
    });

    const text = res.result?.content?.[0]?.text || '{}';
    let status = 'unknown';
    try {
      const obj = JSON.parse(text);
      status = obj.status;
    } catch {
      log('Could not parse status JSON: ' + text.slice(0, 200));
    }

    log('Status: ' + status);

    if (status === 'completed') {
      task.status = 'completed';
      writeFileSync(taskFile, JSON.stringify(task, null, 2));
      log('COMPLETED');
      console.log(JSON.stringify({ status: 'completed', researchId: task.researchId }));
      return;
    }

    if (status === 'failed') {
      task.status = 'failed';
      writeFileSync(taskFile, JSON.stringify(task, null, 2));
      log('FAILED');
      console.log(JSON.stringify({ status: 'failed', researchId: task.researchId }));
      return;
    }

    // Save progress
    task.pollCount = poll;
    task.lastPoll  = new Date().toISOString();
    writeFileSync(taskFile, JSON.stringify(task, null, 2));

    if (poll < MAX_POLLS) {
      log(`Still in_progress. Sleeping ${INTERVAL}s...`);
      await new Promise(r => setTimeout(r, INTERVAL * 1000));
    }
  }

  log('TIMEOUT after ' + MAX_POLLS + ' polls');
  task.status = 'timeout';
  writeFileSync(taskFile, JSON.stringify(task, null, 2));
  console.log(JSON.stringify({ status: 'timeout', researchId: task.researchId }));
}

main().catch(err => {
  log('ERROR: ' + err.message);
  console.error(JSON.stringify({ status: 'error', error: err.message }));
  process.exit(1);
});
