#!/usr/bin/env node
/**
 * Agent Manager CLI - 命令行版本
 */

const { execSync } = require('child_process');
const readline = require('readline');

const API_BASE = 'http://localhost:3000/api';

function execCmd(cmd) {
  try {
    return execSync(cmd, { encoding: 'utf-8', shell: 'zsh' });
  } catch (error) {
    return error.stdout || error.message;
  }
}

async function fetchAPI(endpoint, options = {}) {
  const { execSync } = require('child_process');
  const curl = require('curl');
  
  const url = API_BASE + endpoint;
  const method = options.method || 'GET';
  const body = options.body ? JSON.stringify(options.body) : null;
  
  let cmd = `curl -s -X ${method} "${url}"`;
  if (body) {
    cmd += ` -H "Content-Type: application/json" -d '${body}'`;
  }
  
  try {
    const result = execSync(cmd, { encoding: 'utf-8' });
    return JSON.parse(result);
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// 简化的 fetch（不依赖外部库）
async function simpleFetch(endpoint, options = {}) {
  const { execSync } = require('child_process');
  
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
    console.error('API 调用失败:', error.message);
    return { success: false, error: error.message };
  }
}

const commands = {
  async list() {
    console.log('📋 获取 Agent 列表...\n');
    const data = await simpleFetch('/agents');
    
    if (!data.success) {
      console.error('❌ 错误:', data.error);
      return;
    }
    
    console.log('已注册 Agent:');
    console.log('─'.repeat(60));
    
    if (data.registered.length === 0) {
      console.log('  暂无 Agent');
    } else {
      data.registered.forEach((agent, i) => {
        console.log(`  ${i + 1}. ${agent.name}`);
        console.log(`     ID: ${agent.id}`);
        console.log(`     模型：${agent.model}`);
        console.log(`     描述：${agent.description || '无'}`);
        console.log(`     状态：${agent.status}`);
        console.log();
      });
    }
  },
  
  async create(name, description, model) {
    console.log(`🆕 创建 Agent: ${name}...\n`);
    
    const data = await simpleFetch('/agents', {
      method: 'POST',
      body: { name, description, model: model || 'bailian/qwen3.5-plus' }
    });
    
    if (data.success) {
      console.log('✅ 创建成功!');
      console.log(`   ID: ${data.agent.id}`);
      console.log(`   名称：${data.agent.name}`);
      console.log(`   模型：${data.agent.model}`);
    } else {
      console.error('❌ 创建失败:', data.error);
    }
  },
  
  async delete(agentId) {
    if (!agentId) {
      console.error('❌ 请提供 Agent ID');
      return;
    }
    
    console.log(`🗑️  删除 Agent: ${agentId}...\n`);
    const data = await simpleFetch(`/agents/${agentId}`, { method: 'DELETE' });
    
    if (data.success) {
      console.log('✅ 已删除');
    } else {
      console.error('❌ 删除失败:', data.error);
    }
  },
  
  async chat(agentId) {
    if (!agentId) {
      console.error('❌ 请提供 Agent ID');
      return;
    }
    
    console.log(`💬 与 ${agentId} 对话 (输入 quit 退出)\n`);
    
    const rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    const ask = () => {
      rl.question('你：', async (message) => {
        if (message.toLowerCase() === 'quit' || message.toLowerCase() === 'exit') {
          console.log('👋 再见!');
          rl.close();
          return;
        }
        
        const data = await simpleFetch(`/agents/${agentId}/chat`, {
          method: 'POST',
          body: { message }
        });
        
        if (data.success) {
          console.log(`${agentId}:`, data.response);
        } else {
          console.error('❌ 错误:', data.error);
        }
        
        console.log();
        ask();
      });
    };
    
    ask();
  },
  
  help() {
    console.log(`
🤖 Agent Manager CLI

用法：node cli.js <命令> [参数]

命令:
  list                    列出所有 Agent
  create <名称> [描述]     创建新 Agent
  delete <ID>             删除 Agent
  chat <ID>               与 Agent 对话
  help                    显示帮助

示例:
  node cli.js list
  node cli.js create Judy "营销外展专家"
  node cli.js delete agent-judy
  node cli.js chat agent-judy

Web 界面：http://localhost:3000
`);
  }
};

// 主程序
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command || command === 'help') {
    commands.help();
    return;
  }
  
  switch (command) {
    case 'list':
      await commands.list();
      break;
    case 'create':
      await commands.create(args[1], args[2], args[3]);
      break;
    case 'delete':
      await commands.delete(args[1]);
      break;
    case 'chat':
      await commands.chat(args[1]);
      break;
    default:
      console.error('❌ 未知命令:', command);
      commands.help();
  }
}

main().catch(console.error);
