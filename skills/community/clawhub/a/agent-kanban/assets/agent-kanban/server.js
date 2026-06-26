const express = require('express');
const path = require('path');
const fs = require('fs');

// 加载配置（优先使用 config.local.js）
let config;
try {
  config = require('./config.local.js');
  console.log('Using config.local.js');
} catch (e) {
  config = require('./config.js');
  console.log('Using config.js (no config.local.js found)');
}

const app = express();
const PORT = config.server.port || 3100;
const HOST = config.server.host || '0.0.0.0';
const GATEWAY_URL = config.gateway.url;
const GATEWAY_TOKEN = config.gateway.token;

// 获取 OpenClaw 主目录
function getOpenClawHome() {
  const homeDir = config.openclaw.homeDir;
  // 如果是绝对路径，直接返回；否则拼接用户主目录
  if (path.isAbsolute(homeDir)) {
    return homeDir;
  }
  return path.join(process.env.HOME, homeDir);
}

const OPENCLAW_HOME = getOpenClawHome();

// 读取 openclaw.json 中的 agent heartbeat 配置
let heartbeatConfig = {};

function loadHeartbeatConfig() {
  try {
    const configPath = path.join(OPENCLAW_HOME, config.openclaw.configFilename);
    const openclawConfig = JSON.parse(fs.readFileSync(configPath, 'utf8'));
    const agentsList = openclawConfig.agents?.list || [];
    
    heartbeatConfig = {};  // 清空旧配置
    for (const agent of agentsList) {
      if (agent.id && agent.heartbeat) {
        heartbeatConfig[agent.id] = {
          enabled: true,
          every: agent.heartbeat.every || ''
        };
      }
    }
    
    console.log(`Loaded heartbeat config for ${Object.keys(heartbeatConfig).length} agents`);
  } catch (err) {
    console.error('Failed to load heartbeat config:', err.message);
  }
}

// 启动时加载配置
loadHeartbeatConfig();

app.use(express.static('public'));
app.use(express.json());

// CORS
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.header('Access-Control-Allow-Headers', 'Content-Type');
  if (req.method === 'OPTIONS') return res.sendStatus(200);
  next();
});

// 调用 Gateway HTTP API
async function gatewayInvoke(tool, args = {}) {
  const response = await fetch(`${GATEWAY_URL}/tools/invoke`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${GATEWAY_TOKEN}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ tool, args })
  });
  
  if (!response.ok) {
    throw new Error(`Gateway API error: ${response.status}`);
  }
  
  const data = await response.json();
  if (!data.ok) {
    throw new Error(data.error?.message || 'Unknown error');
  }
  
  return data.result;
}

// 解析 sessions_list 结果，提取前端需要的字段
function parseSessionsList(result) {
  const sessions = [];
  
  // result 可能是 { content: [{ type: "text", text: "..." }] }
  // 也可能是直接的对象
  let data = result;
  if (result.content && Array.isArray(result.content)) {
    const textContent = result.content.find(c => c.type === 'text');
    if (textContent) {
      try {
        data = JSON.parse(textContent.text);
      } catch (e) {
        console.error('Failed to parse sessions_list result:', e);
        return { sessions: [] };
      }
    }
  }
  
  const rawSessions = data.sessions || data.details?.sessions || [];
  
  // 检查 agent 是否有变化，有变化则刷新配置
  const currentAgentIds = new Set(rawSessions.map(s => (s.key || '').split(':')[1]).filter(id => id));
  const configAgentIds = new Set(Object.keys(heartbeatConfig));
  
  // 判断是否有新增或删除的 agent
  const hasNewAgent = [...currentAgentIds].some(id => !configAgentIds.has(id));
  const hasRemovedAgent = [...configAgentIds].some(id => !currentAgentIds.has(id));
  
  if (hasNewAgent || hasRemovedAgent) {
    const newAgents = [...currentAgentIds].filter(id => !configAgentIds.has(id));
    const removedAgents = [...configAgentIds].filter(id => !currentAgentIds.has(id));
    if (newAgents.length > 0) console.log(`New agents detected: ${newAgents.join(', ')}`);
    if (removedAgents.length > 0) console.log(`Agents removed: ${removedAgents.join(', ')}`);
    loadHeartbeatConfig();
  }
  
  for (const s of rawSessions) {
    // 提取 agent ID
    const parts = (s.key || '').split(':');
    const agentId = parts[1] || 'unknown';
    
    // 获取 heartbeat 配置
    const hbConfig = heartbeatConfig[agentId] || null;
    
    sessions.push({
      key: s.key,
      agentId: agentId,
      sessionId: s.sessionId,
      channel: s.channel,
      displayName: s.displayName,
      model: s.model,
      contextTokens: s.contextTokens,
      updatedAt: s.updatedAt,
      age: s.updatedAt ? Date.now() - s.updatedAt : Infinity,
      heartbeat: hbConfig,
      lastMessage: null,  // 需要从 history 获取
      lastMessageTime: s.updatedAt
    });
  }
  
  return { sessions };
}

// 解析 sessions_history 结果
function parseSessionHistory(result) {
  // result 可能是 { content: [{ type: "text", text: "..." }] }
  // 也可能是直接的对象
  let data = result;
  if (result.content && Array.isArray(result.content)) {
    const textContent = result.content.find(c => c.type === 'text');
    if (textContent) {
      try {
        data = JSON.parse(textContent.text);
      } catch (e) {
        console.error('Failed to parse sessions_history result:', e);
        return { messages: [] };
      }
    }
  }
  
  const messages = [];
  const rawMessages = data.messages || data.details?.messages || [];
  
  for (const msg of rawMessages) {
    // 处理 content 字段
    let content = msg.content || '';
    
    // 如果 content 是数组，提取文本
    if (Array.isArray(content)) {
      const textParts = [];
      for (const item of content) {
        if (item.type === 'text') {
          textParts.push(item.text || '');
        } else if (item.type === 'thinking') {
          textParts.push('[思考] ' + (item.thinking || ''));
        } else if (item.type === 'toolCall') {
          textParts.push('[工具] ' + (item.name || ''));
        }
      }
      content = textParts.join('\n');
    }
    
    messages.push({
      role: msg.role,
      content: content,
      timestamp: msg.timestamp
    });
  }
  
  return { messages };
}

// 获取 agent 的 jsonl 文件大小（KB）
function getAgentJsonlSize(agentId) {
  const sessionDir = path.join(OPENCLAW_HOME, 'agents', agentId, 'sessions');
  
  if (!fs.existsSync(sessionDir)) return 0;
  
  let totalSize = 0;
  const files = fs.readdirSync(sessionDir).filter(f => f.endsWith('.jsonl'));
  
  for (const file of files) {
    const filePath = path.join(sessionDir, file);
    const stats = fs.statSync(filePath);
    totalSize += stats.size;
  }
  
  return Math.round(totalSize / 1024); // KB
}

// API: 获取所有 sessions
app.get('/api/sessions', async (req, res) => {
  try {
    const result = await gatewayInvoke('sessions_list', {});
    const data = parseSessionsList(result);
    
    // 添加每个 agent 的 jsonl 文件大小
    for (const s of data.sessions) {
      s.jsonlSizeKB = getAgentJsonlSize(s.agentId);
    }
    
    res.json(data);
  } catch (err) {
    console.error('Failed to get sessions:', err);
    res.status(500).json({ error: err.message });
  }
});

// API: 获取指定 session 的历史
app.get('/api/sessions/:key/history', async (req, res) => {
  try {
    const sessionKey = decodeURIComponent(req.params.key);
    const result = await gatewayInvoke('sessions_history', { 
      sessionKey,
      limit: 100
    });
    const data = parseSessionHistory(result);
    res.json(data);
  } catch (err) {
    console.error('Failed to get session history:', err);
    res.status(500).json({ error: err.message });
  }
});

// API: 获取 agent 的文件（SOUL.md, HEARTBEAT.md, OKR.md 等）
app.get('/api/agents/:agentId/files', async (req, res) => {
  try {
    const agentId = decodeURIComponent(req.params.agentId);
    const workspaceDir = path.join(OPENCLAW_HOME, `workspace-${agentId}`);
    
    const files = {};
    const fileNames = ['OKR.md', 'SOUL.md', 'HEARTBEAT.md'];
    
    for (const fileName of fileNames) {
      const filePath = path.join(workspaceDir, fileName);
      if (fs.existsSync(filePath)) {
        const content = fs.readFileSync(filePath, 'utf8');
        files[fileName] = {
          exists: true,
          content: content,
          lines: content.split('\n').length,
          size: Math.round(content.length / 1024) + 'KB'
        };
      } else {
        files[fileName] = {
          exists: false,
          content: '',
          lines: 0,
          size: '0KB'
        };
      }
    }
    
    res.json({ agentId, files });
  } catch (err) {
    console.error('Failed to get agent files:', err);
    res.status(500).json({ error: err.message });
  }
});

app.listen(PORT, HOST, () => {
  console.log(`Agent Kanban running at http://${HOST}:${PORT}`);
  console.log(`Using Gateway HTTP API: ${GATEWAY_URL}`);
});