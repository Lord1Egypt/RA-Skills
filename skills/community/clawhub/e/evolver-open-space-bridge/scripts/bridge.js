#!/usr/bin/env node
/**
 * bridge.js - Evolver to OpenSpace bridge
 *
 * Usage: node bridge.js --prompt <gep_prompt_file> [--output <output_dir>]
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const https = require('https');
const { URL } = require('url');
const pathMapper = require('./path-mapper');
const fileWait = require('./file-wait');
const { TimeoutManager } = require('./timeout-manager');

const OPENSPACE_MCP = process.env.OPENSPACE_MCP || 'http://127.0.0.1:8081/mcp';
const OPENSPACE_SESSION_ID = process.env.OPENSPACE_SESSION_ID || null;
const DEFAULT_OUTPUT_DIR = path.join(process.cwd(), 'memory', 'evolution', 'openspace_output');

function log(msg) { console.log(`[bridge] ${msg}`); }

function base64Encode(str) {
  return Buffer.from(str, 'utf-8').toString('base64');
}

function httpRequest(url, options = {}, body = null) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const transport = parsed.protocol === 'https:' ? https : http;

    const reqOptions = {
      hostname: parsed.hostname,
      port: parsed.port || (parsed.protocol === 'https:' ? 443 : 80),
      path: parsed.pathname + parsed.search,
      method: options.method || 'GET',
      headers: {
        'Accept': 'application/json, text/event-stream',
        'Content-Type': 'application/json',
        ...options.headers
      }
    };

    const req = transport.request(reqOptions, (res) => {
      const chunks = [];
      res.on('data', (d) => chunks.push(d));
      res.on('end', () => {
        const raw = Buffer.concat(chunks).toString('utf-8');
        const sessionId = res.headers['mcp-session-id'];
        resolve({ status: res.statusCode, body: raw, sessionId });
      });
    });

    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

async function initializeSession() {
  const payload = JSON.stringify({
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'evolver-bridge', version: '0.1.0' }
    }
  });

  const res = await httpRequest(OPENSPACE_MCP, { method: 'POST' }, payload);
  if (res.status !== 200) {
    throw new Error(`Initialize failed: ${res.status}`);
  }

  let sessionId = res.sessionId || OPENSPACE_SESSION_ID;
  if (!sessionId) {
    const m = res.body.match(/mcp-session-id[":\s]+([^\s"}]+)/);
    sessionId = m ? m[1] : null;
  }

  if (!sessionId) {
    throw new Error('No session ID from OpenSpace');
  }

  return sessionId;
}

async function callExecuteTask(sessionId, promptFile, outputDir, maxIterations = 20) {
  const task = `执行文件里记录的进化任务：读取 ${promptFile}，按内容完成演化，并把结果写到 ${outputDir}。不要重新编码或打印原始内容。`;

  const payload = JSON.stringify({
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: {
      name: 'execute_task',
      arguments: {
        task,
        workspace_dir: pathMapper.toWslPath(process.cwd()),
        max_iterations: maxIterations,
        search_scope: 'local'
      }
    }
  });

  log(`Dispatching execute_task with max_iterations=${maxIterations}`);

  const maxAttempts = 2;
  let lastError = null;
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      const res = await httpRequest(
        OPENSPACE_MCP,
        { method: 'POST', headers: { 'mcp-session-id': sessionId } },
        payload
      );

      if (res.status !== 200) {
        throw new Error(`execute_task failed: ${res.status}`);
      }

      const bodyStr = typeof res.body === 'string' ? res.body : JSON.stringify(res.body);
      try {
        return JSON.parse(bodyStr);
      } catch (e) {
        throw new Error(`execute_task response is not valid JSON: ${bodyStr.slice(0, 300)}`);
      }
    } catch (err) {
      lastError = err;
      if (attempt < maxAttempts) {
        log(`execute_task attempt ${attempt} failed, retrying...`);
        await new Promise((r) => setTimeout(r, 1000 * attempt));
      }
    }
  }

  throw lastError || new Error('execute_task failed after retries');
}

async function run(promptFile, outputDir) {
  const startTime = Date.now();
  const tm = new TimeoutManager();
  const timeoutMs = 180000;

  if (!fs.existsSync(promptFile)) {
    throw new Error(`Prompt file not found: ${promptFile}`);
  }

  log(`Reading prompt file: ${promptFile}`);
  const promptStat = fs.statSync(promptFile);
  log(`Prompt file size: ${promptStat.size} bytes`);

  const wslOutputDir = pathMapper.toWslPath(outputDir || DEFAULT_OUTPUT_DIR);
  log(`Output dir (WSL): ${wslOutputDir}`);

  log('Initializing OpenSpace session...');
  const sessionId = await initializeSession();
  log(`Session ID: ${sessionId}`);

  log('Calling execute_task with file-based prompt...');
  const result = await callExecuteTask(sessionId, promptFile, wslOutputDir, 20);

  log('Task dispatched. Output directory should appear at:');
  log(`Windows: ${outputDir || DEFAULT_OUTPUT_DIR}`);
  log(`WSL: ${wslOutputDir}`);
  console.log(JSON.stringify(result, null, 2));
}

function main() {
  const args = process.argv.slice(2);
  const promptIdx = args.indexOf('--prompt');
  const outputIdx = args.indexOf('--output');

  if (promptIdx === -1 || !args[promptIdx + 1]) {
    console.error('Usage: node bridge.js --prompt <gep_prompt_file> [--output <output_dir>]');
    process.exit(1);
  }

  const promptFile = args[promptIdx + 1];
  const outputDir = outputIdx !== -1 ? args[outputIdx + 1] : null;

  if (!fs.existsSync(promptFile)) {
    console.error(`Prompt file not found: ${promptFile}`);
    process.exit(1);
  }

  run(promptFile, outputDir).catch(err => {
    console.error('[bridge] ERROR:', err.message);
    process.exit(1);
  });
}

if (require.main === module) {
  main();
}

module.exports = { run };
