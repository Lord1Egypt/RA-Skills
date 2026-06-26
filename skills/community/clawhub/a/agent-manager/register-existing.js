#!/usr/bin/env node
/**
 * 注册现有工作区为 Agent
 * 自动扫描 ~/.openclaw/workspace-* 目录并注册
 */

const fs = require('fs').promises;
const path = require('path');
const { execSync } = require('child_process');

const WORKSPACE_DIR = path.join(process.env.HOME, '.openclaw');
const AGENTS_DIR = path.join(WORKSPACE_DIR, 'agents');
const API_BASE = 'http://localhost:3000/api';

// 已知 Agent 配置
const AGENT_CONFIGS = {
  'judy': {
    name: 'Judy',
    description: '首席业务官 - 营销外展、线索挖掘、冷邮件、LinkedIn 自动化',
    model: 'bailian/qwen3.5-plus'
  },
  'mnk': {
    name: 'MNK',
    description: '硅基 CTO - 技术架构、系统监控、自动化运维',
    model: 'bailian/glm-5'
  },
  'fly': {
    name: 'Fly',
    description: '助理 - 日程管理、会议安排、日常事务处理',
    model: 'bailian/qwen3.5-plus'
  },
  'dav': {
    name: 'Dav',
    description: '数据分析师 - 数据分析、报表生成、洞察挖掘',
    model: 'bailian/qwen3.5-plus'
  },
  'zhou': {
    name: 'Zhou',
    description: '运营专家 - 用户运营、活动策划、增长策略',
    model: 'bailian/qwen3.5-plus'
  },
  'pnews': {
    name: 'PNews',
    description: '新闻情报官 - 牙医行业 + IT/AI 新闻收集与播报',
    model: 'bailian/qwen3.5-plus'
  }
};

async function execCmd(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf-8', shell: 'zsh' });
  } catch (error) {
    return error.stdout || '';
  }
}

async function simpleFetch(endpoint, options = {}) {
  const url = API_BASE + endpoint;
  const method = options.method || 'GET';
  
  let cmd = `curl -s -X ${method} "${url}"`;
  if (options.body) {
    cmd += ` -H "Content-Type: application/json" -d '${JSON.stringify(options.body)}'`;
  }
  
  try {
    const result = execSync(cmd, { encoding: 'utf-8', shell: 'zsh' });
    return JSON.parse(result);
  } catch (error) {
    return { success: false, error: error.message };
  }
}

async function main() {
  console.log('🔍 扫描现有工作区...\n');
  
  // 获取所有 workspace-* 目录
  const items = await fs.readdir(WORKSPACE_DIR, { withFileTypes: true });
  const workspaceDirs = items
    .filter(d => d.isDirectory() && d.name.startsWith('workspace-'))
    .map(d => d.name);
  
  console.log(`找到 ${workspaceDirs.length} 个工作区:\n`);
  
  let registered = 0;
  let skipped = 0;
  
  for (const workspace of workspaceDirs) {
    const agentId = workspace.replace('workspace-', '');
    const config = AGENT_CONFIGS[agentId];
    
    if (!config) {
      console.log(`⏭️  跳过 ${workspace} (未知 Agent 类型)`);
      skipped++;
      continue;
    }
    
    // 检查是否已注册
    const agentsResult = await simpleFetch('/agents');
    const exists = agentsResult.registered?.some(a => a.id === `agent-${agentId}`);
    
    if (exists) {
      console.log(`✅ ${config.name} 已注册`);
      registered++;
      continue;
    }
    
    // 创建工作区目录（如果不存在）
    const agentDir = path.join(AGENTS_DIR, `agent-${agentId}`);
    await fs.mkdir(agentDir, { recursive: true });
    
    // 复制 IDENTITY.md 和 SOUL.md（如果存在）
    const workspacePath = path.join(WORKSPACE_DIR, workspace);
    const identitySrc = path.join(workspacePath, 'IDENTITY.md');
    const soulSrc = path.join(workspacePath, 'SOUL.md');
    
    try {
      await fs.copyFile(identitySrc, path.join(agentDir, 'IDENTITY.md'));
      console.log(`  📄 复制 IDENTITY.md`);
    } catch (e) {
      // 文件不存在，创建默认
      await fs.writeFile(path.join(agentDir, 'IDENTITY.md'), `# IDENTITY.md - ${config.name}\n\n- **Name:** ${config.name}\n- **Role:** Agent\n`);
    }
    
    try {
      await fs.copyFile(soulSrc, path.join(agentDir, 'SOUL.md'));
      console.log(`  📄 复制 SOUL.md`);
    } catch (e) {
      // 文件不存在，创建默认
      await fs.writeFile(path.join(agentDir, 'SOUL.md'), `# SOUL.md - ${config.name}\n\n_做最好的自己_\n`);
    }
    
    // 创建 config.json
    const agentConfig = {
      id: `agent-${agentId}`,
      name: config.name,
      description: config.description,
      model: config.model,
      workspace: workspace,
      createdAt: new Date().toISOString(),
      status: 'active'
    };
    
    await fs.writeFile(path.join(agentDir, 'config.json'), JSON.stringify(agentConfig, null, 2));
    
    // 注册到 API
    const registerResult = await simpleFetch('/agents', {
      method: 'POST',
      body: config
    });
    
    if (registerResult.success) {
      console.log(`✅ 注册成功：${config.name} (${workspace})`);
      registered++;
    } else {
      console.log(`❌ 注册失败：${config.name} - ${registerResult.error}`);
    }
    
    console.log();
  }
  
  console.log('─'.repeat(60));
  console.log(`完成！注册 ${registered} 个，跳过 ${skipped} 个`);
  console.log('\n访问 http://localhost:3000 查看所有 Agent');
}

main().catch(console.error);
