#!/usr/bin/env node
/**
 * Agent Manager - OpenClaw Agent 管理工具
 * 提供 Web API 和界面管理 Agent
 */

const express = require('express');
const cors = require('cors');
const fs = require('fs').promises;
const path = require('path');
const { exec } = require('child_process');
const { v4: uuidv4 } = require('uuid');

const app = express();
const PORT = process.env.PORT || 3000;

// 配置
const CONFIG = {
  openclawGateway: 'http://127.0.0.1:18789',
  openclawToken: 'YOUR_TOKEN_HERE',
  agentsDir: path.join(process.env.HOME, '.openclaw/agents'),
  workspaceDir: path.join(process.env.HOME, '.openclaw')
};

app.use(cors());
app.use(express.json());

// 工具函数
async function execCmd(cmd) {
  return new Promise((resolve, reject) => {
    exec(cmd, { shell: 'zsh' }, (error, stdout, stderr) => {
      if (error) reject(error);
      else resolve({ stdout, stderr });
    });
  });
}

async function readJsonFile(filepath) {
  const content = await fs.readFile(filepath, 'utf-8');
  return JSON.parse(content);
}

async function writeJsonFile(filepath, data) {
  await fs.mkdir(path.dirname(filepath), { recursive: true });
  await fs.writeFile(filepath, JSON.stringify(data, null, 2));
}

// API 路由

/**
 * GET /api/agents - 获取所有 Agent 列表
 */
app.get('/api/agents', async (req, res) => {
  try {
    let agents = [];
    try {
      const { stdout } = await execCmd('openclaw sessions list 2>/dev/null');
      
      // 解析输出
      const lines = stdout.split('\n').filter(line => line.trim());
      for (const line of lines) {
        const match = line.match(/(\S+)\s+(\S+)\s+(.+)/);
        if (match) {
          agents.push({
            id: match[1],
            kind: match[2],
            label: match[3]
          });
        }
      }
    } catch (e) {
      // sessions list 失败，继续返回注册的 Agent
    }
    
    // 读取已注册的 Agent 配置
    const agentsConfigPath = path.join(CONFIG.workspaceDir, 'agents.json');
    let registeredAgents = [];
    try {
      registeredAgents = await readJsonFile(agentsConfigPath);
    } catch (e) {
      // 文件不存在，返回空数组
    }
    
    res.json({
      success: true,
      running: agents,
      registered: registeredAgents
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * POST /api/agents - 添加新 Agent
 */
app.post('/api/agents', async (req, res) => {
  try {
    const { name, description, model, workspace } = req.body;
    
    if (!name) {
      return res.status(400).json({ success: false, error: '名称必填' });
    }
    
    const agentId = `agent-${name.toLowerCase().replace(/\s+/g, '-')}`;
    const agentDir = path.join(CONFIG.agentsDir, agentId);
    
    // 创建 Agent 目录
    await fs.mkdir(agentDir, { recursive: true });
    
    // 创建基础配置文件
    const agentConfig = {
      id: agentId,
      name,
      description: description || '',
      model: model || 'bailian/qwen3.5-plus',
      workspace: workspace || `workspace-${name.toLowerCase()}`,
      createdAt: new Date().toISOString(),
      status: 'active'
    };
    
    await writeJsonFile(path.join(agentDir, 'config.json'), agentConfig);
    
    // 创建基础文件
    await fs.writeFile(path.join(agentDir, 'IDENTITY.md'), `# IDENTITY.md - ${name}

- **Name:** ${name}
- **Role:** Agent
- **Vibe:** 专业、高效、友好
`);
    
    await fs.writeFile(path.join(agentDir, 'SOUL.md'), `# SOUL.md - ${name} 的核心

_做最好的自己_

## 核心原则

1. 专业 - 在自己的领域提供最好的服务
2. 高效 - 快速响应用户需求
3. 友好 - 用自然的方式沟通
`);
    
    // 更新全局 agents.json
    const agentsConfigPath = path.join(CONFIG.workspaceDir, 'agents.json');
    let allAgents = [];
    try {
      allAgents = await readJsonFile(agentsConfigPath);
    } catch (e) {
      // 文件不存在
    }
    allAgents.push(agentConfig);
    await writeJsonFile(agentsConfigPath, allAgents);
    
    res.json({
      success: true,
      agent: agentConfig,
      message: `Agent "${name}" 创建成功！`
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * POST /api/agents/:id/chat - 与 Agent 对话
 */
app.post('/api/agents/:id/chat', async (req, res) => {
  try {
    const { id } = req.params;
    const { message } = req.body;
    
    if (!message) {
      return res.status(400).json({ success: false, error: '消息不能为空' });
    }
    
    // 读取 Agent 配置获取 agentId (去掉 agent- 前缀)
    const agentConfigPath = path.join(CONFIG.agentsDir, id, 'config.json');
    let agentConfig = null;
    try {
      agentConfig = await readJsonFile(agentConfigPath);
    } catch (e) {
      // 配置不存在，使用默认值
    }
    
    const agentId = id.replace('agent-', '');
    const workspace = agentConfig?.workspace || `workspace-${agentId}`;
    const workspacePath = path.join(CONFIG.workspaceDir, workspace);
    
    // 检查 workspace 是否存在
    try {
      await fs.access(workspacePath);
    } catch (e) {
      return res.status(404).json({ 
        success: false, 
        error: `Agent 工作区不存在：${workspacePath}` 
      });
    }
    
    // 使用 openclaw agent 命令与指定 Agent 对话
    const safeMessage = message.replace(/"/g, '\\"').replace(/\n/g, ' ');
    const { stdout } = await execCmd(`cd "${workspacePath}" && openclaw agent --agent ${agentId} --message "${safeMessage}" --json 2>&1`);
    
    // 解析 JSON 输出，提取实际回复内容
    let response = stdout;
    let cleanResponse = '';
    try {
      // 找到 JSON 开始位置（忽略 config warnings 等前缀）
      const jsonStart = stdout.indexOf('{');
      if (jsonStart !== -1) {
        const jsonStr = stdout.substring(jsonStart);
        const result = JSON.parse(jsonStr);
        // 从嵌套结构中提取文本
        if (result.result?.payloads?.[0]?.text) {
          cleanResponse = result.result.payloads[0].text;
        } else if (result.response) {
          cleanResponse = result.response;
        } else if (result.message) {
          cleanResponse = result.message;
        } else {
          cleanResponse = stdout;
        }
      } else {
        cleanResponse = stdout;
      }
    } catch (e) {
      // 解析失败，返回原始输出
      cleanResponse = stdout;
    }
    
    res.json({
      success: true,
      response: cleanResponse,
      rawResponse: response,
      agent: id,
      agentId: agentId,
      workspace: workspace,
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * POST /api/agents/:id/pair - 生成飞书配对码
 */
app.post('/api/agents/:id/pair', async (req, res) => {
  try {
    const { id } = req.params;
    
    // 触发配对流程（需要用户在飞书中操作）
    res.json({
      success: true,
      message: '请在飞书中打开对应应用，发送 /pair 命令开始配对',
      instruction: '配对完成后，系统会自动批准'
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * DELETE /api/agents/:id - 删除 Agent
 */
app.delete('/api/agents/:id', async (req, res) => {
  try {
    const { id } = req.params;
    const agentDir = path.join(CONFIG.agentsDir, id);
    
    // 检查目录是否存在
    try {
      await fs.access(agentDir);
    } catch (e) {
      return res.status(404).json({ success: false, error: 'Agent 不存在' });
    }
    
    // 删除 Agent 目录
    await execCmd(`rm -rf "${agentDir}"`);
    
    // 从 agents.json 中移除
    const agentsConfigPath = path.join(CONFIG.workspaceDir, 'agents.json');
    let allAgents = [];
    try {
      allAgents = await readJsonFile(agentsConfigPath);
    } catch (e) {
      return res.json({ success: true, message: '已删除' });
    }
    
    allAgents = allAgents.filter(a => a.id !== id);
    await writeJsonFile(agentsConfigPath, allAgents);
    
    res.json({
      success: true,
      message: `Agent "${id}" 已删除`
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

/**
 * GET /api/health - 健康检查
 */
app.get('/api/health', async (req, res) => {
  try {
    // 直接探测 gateway 端口
    const { execSync } = require('child_process');
    execSync('nc -z 127.0.0.1 18789', { timeout: 2000 });
    
    res.json({
      success: true,
      gateway: 'online',
      timestamp: new Date().toISOString()
    });
  } catch (error) {
    res.json({
      success: false,
      gateway: 'offline',
      error: error.message
    });
  }
});

// Gemini 风格的左右分栏界面 - 支持图片输入
app.get('/', (req, res) => {
  res.send(`
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Agent Manager - 与 AI 对话</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { 
      font-family: 'Google Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; 
      background: #fff; 
      height: 100vh;
      overflow: hidden;
    }
    
    /* 主容器 - 全屏 */
    .main-container {
      display: flex;
      height: 100vh;
    }
    
    /* 左侧边栏 - Agent 列表 */
    .sidebar {
      width: 280px;
      background: #f0f4f9;
      border-right: 1px solid #e0e0e0;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .sidebar-header {
      padding: 20px;
      border-bottom: 1px solid #e0e0e0;
      background: #f0f4f9;
    }
    .sidebar-header h2 {
      font-size: 18px;
      color: #1a1a1a;
      margin-bottom: 15px;
      font-weight: 500;
    }
    .add-agent-btn {
      width: 100%;
      background: #fff;
      color: #1a73e8;
      border: 1px solid #dadce0;
      padding: 12px;
      border-radius: 8px;
      cursor: pointer;
      font-size: 14px;
      font-weight: 500;
      transition: all 0.2s;
    }
    .add-agent-btn:hover { 
      background: #f8f9fa;
      border-color: #1a73e8;
    }
    
    .agent-list {
      flex: 1;
      overflow-y: auto;
      padding: 12px;
    }
    .agent-item {
      padding: 14px 16px;
      margin-bottom: 8px;
      background: #fff;
      border: 2px solid transparent;
      border-radius: 12px;
      cursor: pointer;
      transition: all 0.2s;
      box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .agent-item:hover {
      border-color: #1a73e8;
      box-shadow: 0 2px 8px rgba(26,115,232,0.15);
    }
    .agent-item.active {
      border-color: #1a73e8;
      background: #e8f0fe;
    }
    .agent-item-header {
      display: flex;
      align-items: center;
      margin-bottom: 8px;
    }
    .agent-name {
      font-weight: 500;
      color: #1a1a1a;
      font-size: 15px;
    }
    .agent-emoji {
      font-size: 18px;
      margin-right: 10px;
    }
    .agent-desc {
      color: #5f6368;
      font-size: 12px;
      line-height: 1.4;
      margin-bottom: 8px;
    }
    .agent-meta {
      display: flex;
      gap: 8px;
      font-size: 11px;
      color: #9aa0a6;
    }
    
    /* 右侧 - 对话区域 */
    .chat-area {
      flex: 1;
      display: flex;
      flex-direction: column;
      background: #fff;
    }
    .chat-header {
      padding: 16px 24px;
      background: #fff;
      border-bottom: 1px solid #e0e0e0;
    }
    .chat-header-content {
      display: flex;
      align-items: center;
      justify-content: space-between;
    }
    .chat-header h2 {
      font-size: 20px;
      color: #1a1a1a;
      display: flex;
      align-items: center;
      font-weight: 500;
    }
    .chat-header .agent-emoji {
      font-size: 24px;
      margin-right: 12px;
    }
    .chat-header .agent-status {
      margin-left: auto;
      font-size: 12px;
      color: #1a73e8;
      display: flex;
      align-items: center;
      gap: 6px;
      background: #e8f0fe;
      padding: 4px 12px;
      border-radius: 12px;
    }
    .chat-header .agent-status::before {
      content: '';
      width: 6px;
      height: 6px;
      background: #1a73e8;
      border-radius: 50%;
      display: inline-block;
    }
    
    /* 对话消息区域 - 更大 */
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 32px;
      display: flex;
      flex-direction: column;
      gap: 20px;
    }
    .message {
      max-width: 80%;
      padding: 16px 20px;
      border-radius: 16px;
      line-height: 1.6;
      animation: fadeIn 0.3s ease;
    }
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
    .message.user {
      align-self: flex-end;
      background: #1a73e8;
      color: white;
      border-bottom-right-radius: 4px;
    }
    .message.agent {
      align-self: flex-start;
      background: #f0f4f9;
      color: #1a1a1a;
      border: 1px solid #e0e0e0;
      border-bottom-left-radius: 4px;
    }
    .message-header {
      font-size: 12px;
      margin-bottom: 6px;
      opacity: 0.8;
      font-weight: 500;
    }
    .message-content {
      font-size: 15px;
      white-space: pre-wrap;
      line-height: 1.6;
    }
    .message-image {
      max-width: 100%;
      max-height: 300px;
      border-radius: 8px;
      margin-top: 10px;
      display: block;
    }
    .message-time {
      font-size: 11px;
      margin-top: 8px;
      opacity: 0.6;
      text-align: right;
    }
    
    .empty-state {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      color: #5f6368;
    }
    .empty-state-icon {
      font-size: 72px;
      margin-bottom: 24px;
      opacity: 0.4;
    }
    .empty-state-text {
      font-size: 18px;
      text-align: center;
      color: #5f6368;
    }
    .empty-state-subtext {
      font-size: 14px;
      color: #9aa0a6;
      margin-top: 12px;
    }
    
    /* 输入区域 - Gemini 风格 */
    .chat-input-area {
      padding: 20px 32px 28px;
      background: #fff;
      border-top: 1px solid #e0e0e0;
    }
    .input-wrapper {
      background: #f0f4f9;
      border-radius: 24px;
      padding: 12px 16px;
      display: flex;
      align-items: flex-end;
      gap: 12px;
      border: 2px solid transparent;
      transition: all 0.2s;
    }
    .input-wrapper:focus-within {
      background: #fff;
      border-color: #1a73e8;
      box-shadow: 0 2px 12px rgba(26,115,232,0.15);
    }
    .chat-input {
      flex: 1;
      padding: 12px 16px;
      border: none;
      background: transparent;
      font-size: 15px;
      outline: none;
      resize: none;
      max-height: 200px;
      font-family: inherit;
      line-height: 1.5;
    }
    .chat-input::placeholder {
      color: #9aa0a6;
    }
    
    /* 图片预览区域 */
    .image-preview-container {
      display: flex;
      gap: 10px;
      padding: 0 16px 12px;
      flex-wrap: wrap;
    }
    .image-preview {
      position: relative;
      width: 80px;
      height: 80px;
      border-radius: 8px;
      overflow: hidden;
      border: 2px solid #e0e0e0;
    }
    .image-preview img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }
    .image-preview .remove-btn {
      position: absolute;
      top: 4px;
      right: 4px;
      width: 20px;
      height: 20px;
      background: #f44336;
      color: white;
      border: none;
      border-radius: 50%;
      cursor: pointer;
      font-size: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .input-actions {
      display: flex;
      gap: 8px;
      align-items: center;
    }
    .attach-btn {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      border: none;
      background: #fff;
      color: #5f6368;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      transition: all 0.2s;
      box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .attach-btn:hover {
      background: #1a73e8;
      color: white;
    }
    .send-btn {
      background: #1a73e8;
      color: white;
      border: none;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      transition: all 0.2s;
    }
    .send-btn:hover { 
      transform: scale(1.05);
      box-shadow: 0 2px 8px rgba(26,115,232,0.3);
    }
    .send-btn:active { transform: scale(0.95); }
    .send-btn:disabled {
      opacity: 0.4;
      cursor: not-allowed;
      transform: none;
    }
    
    /* 添加 Agent 弹窗 */
    .modal-overlay {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(0,0,0,0.5);
      display: none;
      align-items: center;
      justify-content: center;
      z-index: 1000;
    }
    .modal-overlay.active { display: flex; }
    .modal {
      background: white;
      border-radius: 16px;
      width: 480px;
      max-width: 90%;
      padding: 32px;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .modal h2 {
      margin-bottom: 24px;
      color: #1a1a1a;
      font-size: 20px;
      font-weight: 500;
    }
    .modal-form .form-group {
      margin-bottom: 20px;
    }
    .modal-form label {
      display: block;
      margin-bottom: 8px;
      font-weight: 500;
      color: #5f6368;
      font-size: 14px;
    }
    .modal-form input,
    .modal-form textarea,
    .modal-form select {
      width: 100%;
      padding: 14px 16px;
      border: 2px solid #e0e0e0;
      border-radius: 10px;
      font-size: 15px;
      outline: none;
      transition: border-color 0.2s;
    }
    .modal-form input:focus,
    .modal-form textarea:focus,
    .modal-form select:focus {
      border-color: #1a73e8;
    }
    .modal-form textarea { resize: vertical; min-height: 90px; font-family: inherit; }
    .modal-actions {
      display: flex;
      gap: 12px;
      margin-top: 28px;
    }
    .modal-actions button {
      flex: 1;
      padding: 14px;
      border: none;
      border-radius: 10px;
      cursor: pointer;
      font-size: 15px;
      font-weight: 500;
      transition: all 0.2s;
    }
    .modal-actions .cancel-btn {
      background: #f0f4f9;
      color: #5f6368;
    }
    .modal-actions .cancel-btn:hover { background: #e0e0e0; }
    .modal-actions .submit-btn {
      background: #1a73e8;
      color: white;
    }
    .modal-actions .submit-btn:hover { background: #1557b0; }
    
    /* 加载状态 */
    .loading {
      display: flex;
      align-items: center;
      gap: 10px;
      color: #5f6368;
      font-size: 14px;
      padding: 20px;
    }
    .loading-spinner {
      width: 18px;
      height: 18px;
      border: 2px solid #e0e0e0;
      border-top-color: #1a73e8;
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
    
    /* 滚动条美化 */
    ::-webkit-scrollbar { width: 8px; }
    ::-webkit-scrollbar-track { background: transparent; }
    ::-webkit-scrollbar-thumb { background: #dadce0; border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: #bdc1c6; }
    
    /* 隐藏文件输入 */
    #fileInput { display: none; }
    
    /* 清空历史按钮 */
    .clear-history-btn {
      padding: 8px 16px;
      font-size: 13px;
      background: #f44336;
      color: white;
      border: none;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.2s;
    }
    .clear-history-btn:hover { background: #d32f2f; }
  </style>
</head>
<body>
  <!-- 主容器 -->
  <div class="main-container">
    <!-- 左侧边栏 -->
    <div class="sidebar">
      <div class="sidebar-header">
        <h2>Agent Manager</h2>
        <button class="add-agent-btn" onclick="showAddModal()">+ 新建 Agent</button>
      </div>
      <div class="agent-list" id="agentList">
        <div class="loading">
          <div class="loading-spinner"></div>
          加载中...
        </div>
      </div>
    </div>
    
    <!-- 右侧对话区 -->
    <div class="chat-area">
      <div class="chat-header" id="chatHeader" style="display: none;">
        <div class="chat-header-content">
          <h2>
            <span class="agent-emoji">🤖</span>
            <span id="chatAgentName">选择 Agent</span>
          </h2>
          <div style="display: flex; gap: 10px; align-items: center;">
            <span class="agent-status">在线</span>
            <button onclick="clearCurrentHistory()" class="clear-history-btn">清空历史</button>
          </div>
        </div>
      </div>
      
      <div class="chat-messages" id="chatMessages">
        <div class="empty-state">
          <div class="empty-state-icon">💬</div>
          <div class="empty-state-text">
            选择一个 Agent 开始对话
          </div>
          <div class="empty-state-subtext">
            支持文字和图片输入
          </div>
        </div>
      </div>
      
      <div class="chat-input-area" id="chatInputArea" style="display: none;">
        <div class="image-preview-container" id="imagePreview"></div>
        <div class="input-wrapper">
          <textarea 
            class="chat-input" 
            id="chatInput" 
            placeholder="输入消息，或上传图片..."
            rows="1"
            onkeydown="autoResize(this)"
            onkeypress="handleKeyPress(event)"
          ></textarea>
          <div class="input-actions">
            <input type="file" id="fileInput" accept="image/*" multiple onchange="handleFileSelect(event)">
            <button class="attach-btn" onclick="document.getElementById('fileInput').click()" title="上传图片">
              📎
            </button>
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">
              ➤
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  
  <!-- 添加 Agent 弹窗 -->
  <div class="modal-overlay" id="addModal">
    <div class="modal">
      <h2>创建新 Agent</h2>
      <form class="modal-form" id="addAgentForm">
        <div class="form-group">
          <label>名称 *</label>
          <input type="text" id="agentName" placeholder="如：Judy, MNK, Fly" required>
        </div>
        <div class="form-group">
          <label>描述</label>
          <textarea id="agentDesc" rows="3" placeholder="Agent 的职责描述"></textarea>
        </div>
        <div class="form-group">
          <label>模型</label>
          <select id="agentModel">
            <option value="bailian/qwen3.5-plus">通义千问 3.5 Plus</option>
            <option value="bailian/glm-5">智谱 GLM-5</option>
            <option value="ollama/qwen3.5:397b-cloud">Ollama 本地 (397B)</option>
            <option value="ollama4090/qwen3.5:2b">Ollama 远程 (2B)</option>
          </select>
        </div>
        <div class="modal-actions">
          <button type="button" class="cancel-btn" onclick="hideAddModal()">取消</button>
          <button type="submit" class="submit-btn">创建 Agent</button>
        </div>
      </form>
    </div>
  </div>
  
  <script>
    const API_BASE = '/api';
    const STORAGE_KEY = 'agent_manager_chat_history';
    let currentAgentId = null;
    let agents = [];
    let chatHistory = {}; // 保存每个 Agent 的对话历史
    
    // Agent 表情符号映射
    const agentEmojis = {
      judy: '💼',
      mnk: '🦾',
      fly: '🕊️',
      dav: '📊',
      zhou: '📈',
      pnews: '📰'
    };
    
    // 从 localStorage 加载对话历史
    function loadChatHistory() {
      try {
        const saved = localStorage.getItem(STORAGE_KEY);
        if (saved) {
          chatHistory = JSON.parse(saved);
        }
      } catch (e) {
        console.error('加载对话历史失败:', e);
        chatHistory = {};
      }
    }
    
    // 保存对话历史到 localStorage
    function saveChatHistory() {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(chatHistory));
      } catch (e) {
        console.error('保存对话历史失败:', e);
      }
    }
    
    // 获取某个 Agent 的对话历史
    function getAgentHistory(agentId) {
      return chatHistory[agentId] || [];
    }
    
    // 添加消息到对话历史
    function addMessageToHistory(agentId, message) {
      if (!chatHistory[agentId]) {
        chatHistory[agentId] = [];
      }
      chatHistory[agentId].push(message);
      // 限制每个 Agent 最多保存 100 条消息
      if (chatHistory[agentId].length > 100) {
        chatHistory[agentId] = chatHistory[agentId].slice(-100);
      }
      saveChatHistory();
    }
    
    // 清空当前 Agent 的对话历史
    function clearCurrentHistory() {
      if (!currentAgentId) return;
      if (confirm('确定要清空与这个 Agent 的对话记录吗？此操作不可恢复。')) {
        chatHistory[currentAgentId] = [];
        saveChatHistory();
        selectAgent(currentAgentId);
      }
    }
    
    // 清空某个 Agent 的对话历史（兼容旧调用）
    function clearAgentHistory(agentId) {
      if (!agentId) return;
      if (confirm('确定要清空与这个 Agent 的对话记录吗？此操作不可恢复。')) {
        chatHistory[agentId] = [];
        saveChatHistory();
        if (agentId === currentAgentId) {
          selectAgent(agentId);
        }
      }
    }
    
    // 加载 Agent 列表
    async function loadAgents() {
      try {
        const res = await fetch(API_BASE + '/agents');
        const data = await res.json();
        
        if (!data.success) {
          document.getElementById('agentList').innerHTML = 
            '<div style="padding: 20px; color: #f44336;">加载失败：' + data.error + '</div>';
          return;
        }
        
        agents = data.registered || [];
        
        if (agents.length === 0) {
          document.getElementById('agentList').innerHTML = 
            '<div style="padding: 20px; color: #666; text-align: center;">暂无 Agent<br><small>点击右上角添加</small></div>';
          return;
        }
        
        document.getElementById('agentList').innerHTML = agents.map(agent => {
          const emoji = agentEmojis[agent.id.replace('agent-', '')] || '🤖';
          const isActive = agent.id === currentAgentId ? 'active' : '';
          return \`
            <div class="agent-item \${isActive}" onclick="selectAgent('\${agent.id}')">
              <div class="agent-item-header">
                <div class="agent-name">
                  <span class="agent-emoji">\${emoji}</span>\${agent.name}
                </div>
              </div>
              <div class="agent-desc">\${agent.description || '暂无描述'}</div>
              <div class="agent-meta">
                <span class="agent-model">\${agent.model}</span>
                <span>\${new Date(agent.createdAt).toLocaleDateString()}</span>
              </div>
            </div>
          \`;
        }).join('');
      } catch (error) {
        document.getElementById('agentList').innerHTML = 
          '<div style="padding: 20px; color: #f44336;">加载失败</div>';
      }
    }
    
    // 选择 Agent
    function selectAgent(agentId) {
      currentAgentId = agentId;
      const agent = agents.find(a => a.id === agentId);
      
      // 更新 UI
      document.querySelectorAll('.agent-item').forEach(item => item.classList.remove('active'));
      if (event && event.currentTarget) {
        event.currentTarget.classList.add('active');
      }
      
      // 显示对话区域
      document.getElementById('chatHeader').style.display = 'block';
      document.getElementById('chatInputArea').style.display = 'block';
      
      // 更新标题
      const emoji = agentEmojis[agentId.replace('agent-', '')] || '🤖';
      document.getElementById('chatAgentName').textContent = agent.name;
      document.querySelector('#chatHeader .agent-emoji').textContent = emoji;
      
      // 加载历史消息
      const history = getAgentHistory(agentId);
      const chatMessages = document.getElementById('chatMessages');
      
      if (history.length === 0) {
        chatMessages.innerHTML = \`
          <div class="empty-state">
            <div class="empty-state-icon">\${emoji}</div>
            <div class="empty-state-text">
              开始与 \${agent.name} 对话<br>
              <small style="font-size: 12px; margin-top: 10px; display: block;">\${agent.description || ''}</small>
            </div>
          </div>
        \`;
      } else {
        chatMessages.innerHTML = history.map(msg => \`
          <div class="message \${msg.type}">
            <div class="message-header">\${msg.type === 'user' ? '你' : (emoji + ' ' + agent.name)}</div>
            <div class="message-content">\${escapeHtml(msg.content)}</div>
            <div class="message-time">\${msg.time}</div>
          </div>
        \`).join('');
      }
      
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // 发送消息
    async function sendMessage() {
      const input = document.getElementById('chatInput');
      const message = input.value.trim();
      
      if (!currentAgentId || !message) return;
      
      const agent = agents.find(a => a.id === currentAgentId);
      const emoji = agentEmojis[currentAgentId.replace('agent-', '')] || '🤖';
      const time = new Date().toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
      
      // 保存用户消息到历史
      addMessageToHistory(currentAgentId, {
        type: 'user',
        content: message,
        time: time
      });
      
      // 显示用户消息
      const chatMessages = document.getElementById('chatMessages');
      
      // 如果是第一条消息，清空 empty-state
      const history = getAgentHistory(currentAgentId);
      if (history.length === 1) {
        chatMessages.innerHTML = '';
      }
      
      chatMessages.innerHTML += \`
        <div class="message user">
          <div class="message-header">你</div>
          <div class="message-content">\${escapeHtml(message)}</div>
          <div class="message-time">\${time}</div>
        </div>
      \`;
      
      input.value = '';
      chatMessages.scrollTop = chatMessages.scrollHeight;
      
      // 禁用发送按钮
      const sendBtn = document.getElementById('sendBtn');
      sendBtn.disabled = true;
      sendBtn.textContent = '发送中...';
      
      // 发送请求
      try {
        const res = await fetch(API_BASE + '/agents/' + currentAgentId + '/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });
        
        const data = await res.json();
        
        if (data.success) {
          // 保存 Agent 回复到历史
          addMessageToHistory(currentAgentId, {
            type: 'agent',
            content: data.response,
            time: time
          });
          
          chatMessages.innerHTML += \`
            <div class="message agent">
              <div class="message-header">\${emoji} \${agent.name}</div>
              <div class="message-content">\${escapeHtml(data.response)}</div>
              <div class="message-time">\${time}</div>
            </div>
          \`;
        } else {
          chatMessages.innerHTML += \`
            <div class="message agent" style="background: #ffe6e6; border-color: #f44336;">
              <div class="message-content">❌ 错误：\${escapeHtml(data.error)}</div>
            </div>
          \`;
        }
      } catch (error) {
        chatMessages.innerHTML += \`
          <div class="message agent" style="background: #ffe6e6; border-color: #f44336;">
            <div class="message-content">❌ 请求失败：\${escapeHtml(error.message)}</div>
          </div>
        \`;
      }
      
      sendBtn.disabled = false;
      sendBtn.textContent = '发送 🚀';
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // 处理回车键
    function handleKeyPress(event) {
      if (event.key === 'Enter') {
        sendMessage();
      }
    }
    
    // 显示添加弹窗
    function showAddModal() {
      document.getElementById('addModal').classList.add('active');
    }
    
    // 隐藏添加弹窗
    function hideAddModal() {
      document.getElementById('addModal').classList.remove('active');
      document.getElementById('addAgentForm').reset();
    }
    
    // 添加 Agent
    document.getElementById('addAgentForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      
      const name = document.getElementById('agentName').value;
      const description = document.getElementById('agentDesc').value;
      const model = document.getElementById('agentModel').value;
      
      try {
        const res = await fetch(API_BASE + '/agents', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name, description, model })
        });
        
        const data = await res.json();
        
        if (data.success) {
          alert('创建成功！');
          hideAddModal();
          loadAgents();
        } else {
          alert('创建失败：' + data.error);
        }
      } catch (error) {
        alert('创建失败：' + error.message);
      }
    });
    
    // 刷新 Agent 列表
    function refreshAgents() {
      loadAgents();
    }
    
    // HTML 转义
    function escapeHtml(text) {
      const div = document.createElement('div');
      div.textContent = text;
      return div.innerHTML;
    }
    
    // 初始加载
    loadChatHistory();
    loadAgents();
  </script>
</body>
</html>
  `);
});

// 启动服务器
app.listen(PORT, () => {
  console.log(`🚀 Agent Manager 运行在 http://localhost:${PORT}`);
  console.log(`📡 API 端点：http://localhost:${PORT}/api`);
});
