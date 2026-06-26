#!/usr/bin/env node
/**
 * Save a Gemini Deep Research report to disk.
 * Usage: node save-report.js <task_dir>
 */
import { spawn } from 'child_process';
import { readFileSync, writeFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';
import { createWriteStream } from 'fs';
import { mkdirSync } from 'fs';

const require = createRequire(import.meta.url);
const __dirname = fileURLToPath(new URL('.', import.meta.url));

const TASK_DIR  = process.argv[2] || '.';
const EXT_PATH  = join(require('os').homedir(), '.gemini', 'extensions', 'gemini-deep-research');

function sendCommand(cmd) {
  return new Promise((resolve, reject) => {
    const server = spawn('node', ['dist/index.js'], {
      cwd: EXT_PATH,
      stdio: ['pipe', 'pipe', 'pipe']
    });
    let timedOut = false;
    const to = setTimeout(() => { timedOut = true; server.kill(); }, 600000);
    const lines = [];
    server.stdout.on('data', d => lines.push(d.toString()));
    server.on('error', err => { clearTimeout(to); reject(err); });
    server.on('exit', code => {
      clearTimeout(to);
      if (timedOut) reject(new Error('MCP timeout'));
      else if (code !== 0) reject(new Error('MCP server exit ' + code));
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

  if (!task.researchId)  throw new Error('No researchId');
  if (!task.outputPath)  throw new Error('No outputPath in task.json');
  if (task.status !== 'completed') throw new Error('Research not completed yet (status: ' + task.status + ')');

  console.error('[Save] Initializing MCP...');
  await sendCommand({
    jsonrpc: '2.0', id: 1, method: 'initialize',
    params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'gemini-dr', version: '1.0' } }
  });

  console.error('[Save] Saving report to:', task.outputPath);
  const res = await sendCommand({
    jsonrpc: '2.0', id: 2, method: 'tools/call',
    params: { name: 'research_save_report', arguments: { id: task.researchId, filePath: task.outputPath } }
  });

  if (res.isError) throw new Error('save error: ' + JSON.stringify(res));

  const responseText = res.result?.content?.[0]?.text || '';
  console.error('[Save] Response:', responseText.slice(0, 200));

  // Verify
  try {
    const stats = require('fs').statSync(task.outputPath);
    console.error('[Save] File size:', stats.size, 'bytes');
  } catch {}

  console.log(JSON.stringify({ status: 'saved', path: task.outputPath }));
}

main().catch(err => {
  console.error(JSON.stringify({ status: 'error', error: err.message }));
  process.exit(1);
});
