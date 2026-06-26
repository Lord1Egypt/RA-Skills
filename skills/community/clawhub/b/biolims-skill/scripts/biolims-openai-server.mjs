#!/usr/bin/env node
/**
 * Bio-LIMS OpenAI-Compatible API Server
 *
 * Provides standard OpenAI Chat Completions API format
 * External agents can call Bio-LIMS like calling GPT
 *
 * Start: node biolims-openai-server.mjs [port]
 * Default port: 3457
 */

import http from 'http';
import { execSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const BIOLIMS_SCRIPT = join(__dirname, 'biolims.mjs');

const PORT = process.argv[2] || 3457;
const API_KEY = process.env.BIOLIMS_API_KEY || ''; // Configure via BIOLIMS_API_KEY env var, empty to skip auth

// ============ Bio-LIMS Command Execution ============

function execBioLIMS(command, ...args) {
  try {
    const cmd = `node "${BIOLIMS_SCRIPT}" ${command} ${args.map(a => `"${a}"`).join(' ')}`;
    const result = execSync(cmd, { encoding: 'utf-8', timeout: 30000 });
    return JSON.parse(result);
  } catch (err) {
    return { status: 500, msg: err.message };
  }
}

// ============ Intent Parsing ============

function parseIntent(message) {
  const msg = message.toLowerCase();
  
  // Order query
  if (msg.match(/order.*detail|get.*order/i)) {
    const orderMatch = message.match(/[A-Z]{2}\d{10}|ORDER\d+/i);
    if (orderMatch) {
      return { command: 'order', args: [orderMatch[0]] };
    }
  }

  // Order list
  if (msg.match(/list.*order|recent.*order/i)) {
    const pageMatch = message.match(/page[=:\s]*(\d+)/i);
    const rowsMatch = message.match(/rows[=:\s]*(\d+)|(\d+)\s*items/i);
    return {
      command: 'order-list',
      args: [pageMatch?.[1] || '1', rowsMatch?.[1] || rowsMatch?.[2] || '10']
    };
  }

  // Order samples
  if (msg.match(/order.*sample/i)) {
    const orderMatch = message.match(/[A-Z]{2}\d{10}/i);
    if (orderMatch) {
      return { command: 'order-samples', args: [orderMatch[0]] };
    }
  }

  // Receive list
  if (msg.match(/receive.*list/i)) {
    return { command: 'receive-list', args: ['1', '10'] };
  }

  // Receive details
  if (msg.match(/receive.*detail/i)) {
    const receiveMatch = message.match(/SR\d+|[A-Z]{2}\d{10}/i);
    if (receiveMatch) {
      return { command: 'receive', args: [receiveMatch[0]] };
    }
  }

  // Experiment list
  if (msg.match(/experiment.*list/i)) {
    const suffixMatch = message.match(/NAE|LP|E|Se/i);
    return { command: 'experiment-list', args: [suffixMatch?.[0]?.toUpperCase() || 'NAE', '1', '10'] };
  }

  // Sample pool
  if (msg.match(/sample.*pool/i)) {
    const suffixMatch = message.match(/NAE|LP|E|Se/i);
    return { command: 'experiment-sample-pool', args: [suffixMatch?.[0]?.toUpperCase() || 'NAE', '1', '20'] };
  }

  // Sequencing QC
  if (msg.match(/qc|sequencing.*qc/i)) {
    return { command: 'seq-qc-list', args: ['1', '10'] };
  }

  // Sample types
  if (msg.match(/sample.*type/i)) {
    const searchMatch = message.match(/search[:\s]*(.+)/i);
    if (searchMatch) {
      return { command: 'search-sample-type', args: [searchMatch[1]] };
    }
    return { command: 'sample-types', args: ['1', '50'] };
  }
  
  // Direct command mode: /command arg1 arg2
  if (message.startsWith('/')) {
    const parts = message.slice(1).split(/\s+/);
    return { command: parts[0], args: parts.slice(1) };
  }
  
  return null;
}

// ============ Format Response ============

function formatResponse(data, intent) {
  if (data.status !== 200) {
    return `Operation failed: ${data.msg || 'Unknown error'}`;
  }
  
  const result = data.data;
  
  // Order Details
  if (intent?.command === 'order' && result.order) {
    const o = result.order;
    return `Order Details\n` +
      `Order ID: ${o.id}\n` +
      `Patient Name: ${o.name}\n` +
      `Test Item: ${o.productName}\n` +
      `Status: ${o.stateName}\n` +
      `Created: ${o.createTime}`;
  }

  // Order list
  if (intent?.command === 'order-list' && result.result) {
    const orders = result.result.slice(0, 5);
    return `Order List (${result.total} total)\n\n` +
      orders.map((o, i) =>
        `${i+1}. ${o.id} | ${o.name} | ${o.productName} | ${o.stateName}`
      ).join('\n');
  }
  
  // Generic JSON response
  return JSON.stringify(result, null, 2);
}

// ============ OpenAI Format Response ============

function createChatCompletion(content, model = 'biolims-gpt') {
  return {
    id: `chatcmpl-${Date.now()}`,
    object: 'chat.completion',
    created: Math.floor(Date.now() / 1000),
    model: model,
    choices: [{
      index: 0,
      message: {
        role: 'assistant',
        content: content
      },
      finish_reason: 'stop'
    }],
    usage: {
      prompt_tokens: 0,
      completion_tokens: 0,
      total_tokens: 0
    }
  };
}

// ============ HTTP Server ============

const server = http.createServer(async (req, res) => {
  // CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  
  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }
  
  // Validate API Key (optional)
  const authHeader = req.headers.authorization;
  if (API_KEY && authHeader !== `Bearer ${API_KEY}`) {
    res.writeHead(401, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ error: { message: 'Invalid API key', type: 'invalid_request_error' } }));
    return;
  }
  
  const url = new URL(req.url, `http://localhost:${PORT}`);
  
  // GET /v1/models - Model list
  if (req.method === 'GET' && url.pathname === '/v1/models') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      object: 'list',
      data: [
        { id: 'biolims-gpt', object: 'model', created: 1700000000, owned_by: 'biolims' },
        { id: 'biolims-fast', object: 'model', created: 1700000000, owned_by: 'biolims' }
      ]
    }));
    return;
  }
  
  // POST /v1/chat/completions - Chat Completions API
  if (req.method === 'POST' && url.pathname === '/v1/chat/completions') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const request = JSON.parse(body);
        const messages = request.messages || [];
        const lastMessage = messages[messages.length - 1];
        
        if (!lastMessage || lastMessage.role !== 'user') {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: { message: 'No user message found' } }));
          return;
        }
        
        const userContent = lastMessage.content;
        const intent = parseIntent(userContent);
        
        let responseContent;
        if (intent) {
          const result = execBioLIMS(intent.command, ...intent.args);
          responseContent = formatResponse(result, intent);
        } else {
          responseContent = `Bio-LIMS API\n\nSupported queries:\n` +
            `- Query order DB2602060003\n` +
            `- Order list / Recent 10 orders\n` +
            `- Order samples DB2602060003\n` +
            `- Receive list\n` +
            `- Experiment list NAE/LP/E/Se\n` +
            `- Sample pool NAE\n` +
            `- Sample types / Search sample type Blood\n` +
            `- QC list\n\n` +
            `Or use direct command: /order-list 1 20`;
        }
        
        const completion = createChatCompletion(responseContent, request.model || 'biolims-gpt');
        
        res.writeHead(200, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify(completion));
        
      } catch (err) {
        res.writeHead(500, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: { message: err.message } }));
      }
    });
    return;
  }
  
  // Health check
  if (req.method === 'GET' && (url.pathname === '/' || url.pathname === '/health')) {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({ status: 'ok', service: 'biolims-openai-api', version: '1.0.0' }));
    return;
  }
  
  // 404
  res.writeHead(404, { 'Content-Type': 'application/json' });
  res.end(JSON.stringify({ error: { message: 'Not found' } }));
});

server.listen(PORT, () => {
  console.log(`🚀 Bio-LIMS OpenAI-Compatible API Server`);
  console.log(`   http://localhost:${PORT}`);
  console.log(`   `);
  console.log(`📡 Endpoints:`);
  console.log(`   GET  /v1/models`);
  console.log(`   POST /v1/chat/completions`);
  console.log(`   `);
  console.log(`🔧 Usage (Python openai):`);
  console.log(`   client = OpenAI(base_url="http://localhost:${PORT}/v1", api_key="your-api-key")`);
  console.log(`   response = client.chat.completions.create(`);
  console.log(`       model="biolims-gpt",`);
  console.log(`       messages=[{"role": "user", "content": "Query order DB2602060003"}]`);
  console.log(`   )`);
});
