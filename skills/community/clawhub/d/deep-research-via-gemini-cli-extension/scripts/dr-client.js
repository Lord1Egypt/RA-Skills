#!/usr/bin/env node
/**
 * Gemini Deep Research MCP Client
 * 
 * Wraps the gemini-deep-research MCP server to perform a complete
 * research workflow: start → poll → save report.
 * 
 * Usage:
 *   node dr-client.js --input "<research query>" [--output "<path>"] [--format "<report format>"] [--timeout <ms>]
 * 
 * Report formats:
 *   Comprehensive Research Report  (default)
 *   Executive Brief
 *   Technical Deep Dive
 * 
 * Output: JSON to stdout { status, researchId, reportPath, error }
 */

import { spawn } from 'child_process';
import { writeFileSync, mkdirSync, readFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';
import { createRequire } from 'module';

const require = createRequire(import.meta.url);
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// ─── Argument Parsing ──────────────────────────────────────────────────────────

const args = process.argv.slice(2).reduce((acc, arg, i, arr) => {
  if (arg.startsWith('--')) {
    const key = arg.slice(2);
    acc[key] = arr[i + 1] && !arr[i + 1].startsWith('--') ? arr[i + 1] : true;
  }
  return acc;
}, {});

const INPUT     = args.input     || args.i;
const OUTPUT    = args.output    || args.o;
const FORMAT    = args.format    || args.f || 'Comprehensive Research Report';
const TIMEOUT   = parseInt(args.timeout || args.t || '900000', 10); // 15 min default
const DRY_RUN   = args['dry-run'] === true;

// ─── Extension Path ──────────────────────────────────────────────────────────

// Resolve ~/.gemini/extensions/gemini-deep-research
// __dirname = .../skills/gemini-deep-research/scripts
// Up 3 levels = .../skills/gemini-deep-research
// Up 4 levels = ~/.openclaw/workspace
// Up 5 levels = ~
const HOME = process.env.HOME || '/home/node';
const EXT_PATH = join(HOME, '.gemini', 'extensions', 'gemini-deep-research');

if (!INPUT) {
  console.error(JSON.stringify({ status: 'error', error: 'Missing --input <research query>' }));
  process.exit(1);
}

const VALID_FORMATS = ['Comprehensive Research Report', 'Executive Brief', 'Technical Deep Dive'];
if (!VALID_FORMATS.includes(FORMAT)) {
  console.error(JSON.stringify({ status: 'error', error: `Invalid --format. Must be one of: ${VALID_FORMATS.join(', ')}` }));
  process.exit(1);
}

// ─── MCP Server Communication ─────────────────────────────────────────────────

let id = 1;

function nextId() {
  return id++;
}

function sendCommand(cmd) {
  return new Promise((resolve, reject) => {
    const line = JSON.stringify(cmd);
    server.stdin.write(line + '\n');
    
    function handler(data) {
      const lines = data.toString().split('\n').filter(l => l.trim());
      for (const l of lines) {
        try {
          const j = JSON.parse(l);
          if (j.id === cmd.id) {
            server.stdout.off('data', handler);
            resolve(j);
            return;
          }
        } catch {}
      }
    }
    
    server.stdout.on('data', handler);
    
    // Timeout for individual commands (15 min max for deep research)
    setTimeout(() => {
      server.stdout.off('data', handler);
      reject(new Error(`Command timeout after 900000ms: ${JSON.stringify(cmd).slice(0, 80)}`));
    }, 900000);
  });
}

// ─── Load .env for MCP server ───────────────────────────────────────────────

function loadEnv(envPath) {
  const env = {};
  try {
    const content = readFileSync(envPath, 'utf8');
    for (const line of content.split('\n')) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      const eqIdx = trimmed.indexOf('=');
      if (eqIdx < 0) continue;
      const key = trimmed.slice(0, eqIdx).trim();
      const val = trimmed.slice(eqIdx + 1).trim();
      env[key] = val;
    }
  } catch {}
  return env;
}

const envPath = join(EXT_PATH, '.env');
const extEnv = loadEnv(envPath);

// ─── Spawn MCP Server ─────────────────────────────────────────────────────────

const distPath = join(EXT_PATH, 'dist', 'index.js');

let server;
try {
  server = spawn('node', ['dist/index.js'], {
    cwd: EXT_PATH,
    stdio: ['pipe', 'pipe', 'pipe'],
    env: { ...process.env, ...extEnv }
  });
} catch (err) {
  console.error(JSON.stringify({ status: 'error', error: `Failed to spawn MCP server: ${err.message}` }));
  process.exit(1);
}

server.stderr.on('data', d => {
  process.stderr.write('[MCP STDERR] ' + d.toString());
});

// ─── Main Workflow ────────────────────────────────────────────────────────────

async function main() {
  // 1 ─── Initialize
  process.stderr.write('[DR] Initializing MCP server...\n');
  
  const initResult = await sendCommand({
    jsonrpc: '2.0',
    id: nextId(),
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'gemini-deep-research-client', version: '1.0' }
    }
  });

  if (!initResult.result || !initResult.result.serverInfo) {
    throw new Error('MCP server initialize failed: ' + JSON.stringify(initResult));
  }

  process.stderr.write(`[DR] Server: ${initResult.result.serverInfo.name} v${initResult.result.serverInfo.version}\n`);

  // 2 ─── Start Research
  process.stderr.write(`[DR] Starting research: "${INPUT}"\n`);
  
  const startResult = await sendCommand({
    jsonrpc: '2.0',
    id: nextId(),
    method: 'tools/call',
    params: {
      name: 'research_start',
      arguments: {
        input: INPUT,
        report_format: FORMAT
      }
    }
  });

  if (startResult.isError) {
    throw new Error('research_start error: ' + JSON.stringify(startResult));
  }

  const startText = startResult.result.content[0].text;
  const idMatch = startText.match(/ID:\s*([^\s]+)/);
  const researchId = idMatch ? idMatch[1] : null;

  if (!researchId) {
    throw new Error('Could not extract research ID from response: ' + startText);
  }

  process.stderr.write(`[DR] Research started. ID: ${researchId}\n`);

  // 3 ─── Poll with Exponential Backoff
  const pollIntervals = [0, 15, 30, 60, 120, 180, 240, 300, 360, 420]; // seconds
  let pollIndex = 0;
  let status = 'in_progress';
  const startTime = Date.now();

  while (status === 'in_progress') {
    if (Date.now() - startTime > TIMEOUT) {
      throw new Error(`Research timed out after ${TIMEOUT / 1000}s`);
    }

    const delay = (pollIndex < pollIntervals.length)
      ? pollIntervals[pollIndex] * 1000
      : 60000; // cap at 60s

    if (delay > 0) {
      await new Promise(r => setTimeout(r, delay));
    }

    pollIndex++;
    process.stderr.write(`[DR] Polling status (attempt ${pollIndex})...\n`);

    const statusResult = await sendCommand({
      jsonrpc: '2.0',
      id: nextId(),
      method: 'tools/call',
      params: {
        name: 'research_status',
        arguments: { id: researchId }
      }
    });

    if (statusResult.isError) {
      // Some errors are transient (rate limits etc) - retry
      process.stderr.write(`[DR] Status check error, retrying: ${JSON.stringify(statusResult)}\n`);
      continue;
    }

    const statusText = statusResult.result.content[0].text;
    let statusObj;
    try {
      statusObj = JSON.parse(statusText);
    } catch {
      // Sometimes the response isn't JSON
      process.stderr.write(`[DR] Status response: ${statusText}\n`);
      break;
    }

    status = statusObj.status;
    process.stderr.write(`[DR] Status: ${status}\n`);

    if (status === 'completed') {
      break;
    } else if (status === 'failed') {
      throw new Error(`Research failed: ${statusText}`);
    }
  }

  // 4 ─── Save Report
  if (!OUTPUT) {
    // No output path provided — return result as JSON
    console.log(JSON.stringify({
      status: 'completed',
      researchId,
      format: FORMAT,
      query: INPUT
    }));
    server.kill();
    process.exit(0);
    return;
  }

  process.stderr.write(`[DR] Saving report to: ${OUTPUT}\n`);

  // Ensure output dir exists
  try {
    mkdirSync(dirname(OUTPUT), { recursive: true });
  } catch {}

  const saveResult = await sendCommand({
    jsonrpc: '2.0',
    id: nextId(),
    method: 'tools/call',
    params: {
      name: 'research_save_report',
      arguments: { id: researchId, filePath: OUTPUT }
    }
  });

  if (saveResult.isError) {
    throw new Error('research_save_report error: ' + JSON.stringify(saveResult));
  }

  process.stderr.write(`[DR] Report saved.\n`);

  // 5 ─── Verify
  let savedSize = 0;
  try {
    savedSize = readFileSync(OUTPUT, 'utf8').length;
  } catch {}

  server.kill();

  console.log(JSON.stringify({
    status: 'completed',
    researchId,
    reportPath: OUTPUT,
    format: FORMAT,
    query: INPUT,
    savedBytes: savedSize
  }));

  process.exit(0);
}

// ─── Error Handler ────────────────────────────────────────────────────────────

main().catch(err => {
  server?.kill();
  console.error(JSON.stringify({
    status: 'error',
    researchId: null,
    error: err.message
  }));
  process.exit(1);
});
