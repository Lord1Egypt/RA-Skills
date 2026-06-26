#!/usr/bin/env node
/**
 * mcp-call.js - MCP 工具调用脚本
 * 用法: node mcp-call.js <method> [arguments]
 * 
 * method: initialize | lists | status | detail | markdown | office
 * arguments: JSON string (e.g., '{"meeting_id":"xxx"}')
 * 
 * 示例:
 *   node mcp-call.js status
 *   node mcp-call.js lists
 *   node mcp-call.js detail '{"meeting_id":"xxx"}'
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

// 读取 token
function getToken() {
  const envPath = path.join(__dirname, '..', '.env');
  if (!fs.existsSync(envPath)) return null;
  const content = fs.readFileSync(envPath, 'utf-8');
  const match = content.match(/ELASTOLINK_TOKEN=(.+)/);
  return match ? match[1].trim() : null;
}

// 读取 session ID
function getSessionId() {
  const sessionPath = path.join(__dirname, '..', '.session');
  if (!fs.existsSync(sessionPath)) return null;
  return fs.readFileSync(sessionPath, 'utf-8').trim();
}

// 保存 session ID
function saveSessionId(sessionId) {
  const sessionPath = path.join(__dirname, '..', '.session');
  fs.writeFileSync(sessionPath, sessionId);
}

// MCP 请求
function mcpRequest(payload, sessionId = null) {
  return new Promise((resolve, reject) => {
    const token = getToken();
    if (!token) {
      reject(new Error('NO_TOKEN'));
      return;
    }

    const headers = {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    };

    if (sessionId) {
      headers['mcp-session-id'] = sessionId;
    }

    const body = JSON.stringify(payload);

    const options = {
      hostname: 'dev.ideasprite.com',
      path: '/mcp',
      method: 'POST',
      headers
    };

    const req = https.request(options, (res) => {
      const sessionIdFromHeader = res.headers['mcp-session-id'];
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        if (sessionIdFromHeader) {
          saveSessionId(sessionIdFromHeader);
        }
        try {
          resolve(JSON.parse(data));
        } catch {
          resolve(data);
        }
      });
    });

    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// 初始化
async function initialize() {
  const result = await mcpRequest({
    jsonrpc: '2.0',
    id: 1,
    method: 'initialize',
    params: {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'openclaw', version: '1.0.0' }
    }
  });
  return result;
}

// 获取工具列表
async function listTools() {
  let sessionId = getSessionId();
  if (!sessionId) {
    await initialize();
    sessionId = getSessionId();
  }

  const result = await mcpRequest({
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: { name: 'lists', arguments: {} }
  }, sessionId);

  return result;
}

// 调用工具
async function callTool(toolName, args = {}) {
  let sessionId = getSessionId();
  if (!sessionId) {
    await initialize();
    sessionId = getSessionId();
  }

  const result = await mcpRequest({
    jsonrpc: '2.0',
    id: 2,
    method: 'tools/call',
    params: { name: toolName, arguments: args }
  }, sessionId);

  return result;
}

// 主逻辑
async function main() {
  const method = process.argv[2];
  const args = process.argv[3] ? JSON.parse(process.argv[3]) : {};

  const token = getToken();
  if (!token) {
    console.log('NO_TOKEN');
    process.exit(1);
  }

  try {
    let result;
    switch (method) {
      case 'initialize':
        result = await initialize();
        break;
      case 'lists':
        result = await listTools();
        break;
      case 'status':
        result = await callTool('status', args);
        break;
      case 'detail':
        result = await callTool('detail', args);
        break;
      case 'markdown':
        result = await callTool('markdown', args);
        break;
      case 'office':
        result = await callTool('office', args);
        break;
      case 'tools':
        // 列出所有工具
        await initialize();
        const sessionId = getSessionId();
        const toolsResult = await mcpRequest({
          jsonrpc: '2.0',
          id: 2,
          method: 'tools/list'
        }, sessionId);
        console.log(JSON.stringify(toolsResult, null, 2));
        return;
      default:
        console.error(`Unknown method: ${method}`);
        console.log('Available: initialize, lists, status, detail, markdown, office, tools');
        process.exit(1);
    }
    console.log(JSON.stringify(result, null, 2));
  } catch (err) {
    if (err.message === 'NO_TOKEN') {
      console.log('NO_TOKEN');
      process.exit(1);
    }
    console.error('Error:', err.message);
    process.exit(1);
  }
}

main();
