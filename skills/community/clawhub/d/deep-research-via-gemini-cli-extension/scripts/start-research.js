#!/usr/bin/env node
/**
 * Start a Gemini Deep Research task and save task metadata.
 * Reads config from task.json in the same dir, writes researchId to it.
 * Usage: node start-research.js <task_dir>
 */
import { spawn } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { join } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const __dirname = fileURLToPath(new URL('.', import.meta.url));

const TASK_DIR = process.argv[2] || '.';
const EXT_PATH  = join(require('os').homedir(), '.gemini', 'extensions', 'gemini-deep-research');

function sendCommand(cmd, timeout = 60000) {
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
      if (timedOut) reject(new Error('MCP command timeout'));
      else if (code !== 0) reject(new Error('MCP server exited with code ' + code));
      else {
        const full = lines.join('');
        try { resolve(JSON.parse(full)); }
        catch { reject(new Error('Invalid JSON from MCP: ' + full.slice(0, 200))); }
      }
    });
    server.stdin.write(JSON.stringify(cmd) + '\n');
  });
}

async function main() {
  const taskFile = join(TASK_DIR, 'task.json');
  const task = JSON.parse(readFileSync(taskFile, 'utf8'));

  console.error('[Start] Initializing MCP...');
  const init = await sendCommand({
    jsonrpc: '2.0', id: 1, method: 'initialize',
    params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'gemini-dr', version: '1.0' } }
  });

  console.error('[Start] Starting research:', task.input.slice(0, 60));
  const res = await sendCommand({
    jsonrpc: '2.0', id: 2, method: 'tools/call',
    params: { name: 'research_start', arguments: { input: task.input, report_format: task.format || 'Comprehensive Research Report' } }
  });

  if (res.isError) throw new Error('research_start error: ' + JSON.stringify(res));

  const idMatch = res.result.content[0].text.match(/ID:\s*([^\s]+)/);
  if (!idMatch) throw new Error('Could not extract research ID: ' + res.result.content[0].text);

  const researchId = idMatch[1];
  task.researchId = researchId;
  task.startedAt  = new Date().toISOString();
  task.status      = 'in_progress';
  writeFileSync(taskFile, JSON.stringify(task, null, 2));

  console.log(JSON.stringify({ status: 'started', researchId, taskDir: TASK_DIR }));
}

main().catch(err => {
  console.error(JSON.stringify({ status: 'error', error: err.message }));
  process.exit(1);
});
