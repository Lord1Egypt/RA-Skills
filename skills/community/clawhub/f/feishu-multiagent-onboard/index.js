#!/usr/bin/env node

/**
 * feishu-multiagent-onboard Skill
 * 飞书多 Agent 快速配置向导
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const CONFIG_PATH = path.join(require('os').homedir(), '.openclaw/openclaw.json');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  red: '\x1b[31m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m',
  cyan: '\x1b[36m',
};

function log(color, message) {
  console.log(`${color}${message}${colors.reset}`);
}

function logSuccess(message) {
  log(colors.green, `✅ ${message}`);
}

function logError(message) {
  log(colors.red, `❌ ${message}`);
}

function logWarn(message) {
  log(colors.yellow, `⚠️  ${message}`);
}

function logInfo(message) {
  log(colors.blue, `ℹ️  ${message}`);
}

// 读取配置
function readConfig() {
  try {
    const content = fs.readFileSync(CONFIG_PATH, 'utf8');
    return JSON.parse(content);
  } catch (error) {
    logError(`读取配置失败：${error.message}`);
    return null;
  }
}

// 写入配置
function writeConfig(config) {
  try {
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf8');
    logSuccess('配置已保存');
    return true;
  } catch (error) {
    logError(`写入配置失败：${error.message}`);
    return false;
  }
}

// 验证 JSON 格式
function validateJSON() {
  try {
    execSync(`cat ${CONFIG_PATH} | python3 -m json.tool > /dev/null 2>&1`);
    logSuccess('JSON 格式正确');
    return true;
  } catch (error) {
    logError('JSON 格式错误');
    return false;
  }
}

// 检查配置
function checkConfig() {
  logInfo('检查配置...');
  
  const config = readConfig();
  if (!config) return false;
  
  // 检查 channels.feishu
  const feishu = config.channels?.feishu;
  if (!feishu) {
    logError('未配置飞书通道');
    return false;
  }
  
  // 检查 accounts
  const accounts = feishu.accounts;
  if (!accounts || Object.keys(accounts).length === 0) {
    logError('未配置 accounts');
    return false;
  }
  
  logSuccess(`配置了 ${Object.keys(accounts).length} 个飞书账号`);
  
  // 检查每个 account
  for (const [accountId, account] of Object.entries(accounts)) {
    if (!account.appId || !account.appSecret) {
      logError(`账号 ${accountId} 缺少 appId 或 appSecret`);
      return false;
    }
    logSuccess(`账号 ${accountId}: ${account.appId}`);
  }
  
  // 检查 bindings
  const bindings = config.bindings || [];
  if (bindings.length === 0) {
    logError('未配置 bindings');
    return false;
  }
  
  logSuccess(`配置了 ${bindings.length} 个绑定`);
  
  // 验证 JSON
  if (!validateJSON()) {
    return false;
  }
  
  logSuccess('配置检查通过！');
  return true;
}

// 配置向导
function wizard() {
  logInfo('🚀 飞书多 Agent 配置向导');
  logInfo('');
  
  const config = readConfig();
  if (!config) {
    logError('无法读取配置，请先确保 OpenClaw 已初始化');
    return;
  }
  
  // 获取 Agent 数量
  console.log('请输入要配置的 Agent 数量：');
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
  });
  
  readline.question('Agent 数量 (默认 2): ', (answer) => {
    const count = parseInt(answer) || 2;
    logInfo(`将配置 ${count} 个 Agent`);
    
    const accounts = {};
    const bindings = [];
    
    let completed = 0;
    
    function nextAgent(index) {
      if (index >= count) {
        // 完成配置
        config.channels = config.channels || {};
        config.channels.feishu = {
          enabled: true,
          accounts: accounts,
        };
        config.bindings = bindings;
        
        if (writeConfig(config)) {
          logSuccess('配置完成！');
          logInfo('');
          logInfo('下一步：');
          logInfo('1. 在飞书开放平台创建应用');
          logInfo('2. 配置事件订阅（长连接 + 接收消息）');
          logInfo('3. 重启 Gateway: openclaw gateway restart');
          logInfo('4. 批准配对码：openclaw pairing approve feishu <配对码>');
        }
        readline.close();
        return;
      }
      
      const agentId = index === 0 ? 'writer' : index === 1 ? 'media' : `agent${index}`;
      logInfo('');
      logInfo(`--- 配置 Agent ${index + 1}/${count} ---`);
      
      readline.question(`Agent ID (默认 ${agentId}): `, (idAnswer) => {
        const id = idAnswer || agentId;
        
        readline.question('飞书 App ID: ', (appId) => {
          readline.question('飞书 App Secret: ', (appSecret) => {
            accounts[id] = {
              appId: appId,
              appSecret: appSecret,
            };
            
            bindings.push({
              agentId: id,
              match: { channel: 'feishu', accountId: id },
            });
            
            logSuccess(`Agent ${id} 配置完成`);
            completed++;
            nextAgent(index + 1);
          });
        });
      });
    }
    
    nextAgent(0);
  });
}

// 故障诊断
function debug() {
  logInfo('🔍 开始诊断...');
  logInfo('');
  
  // 检查配置
  logInfo('1. 检查配置...');
  checkConfig();
  
  // 检查插件
  logInfo('');
  logInfo('2. 检查插件...');
  try {
    const output = execSync('openclaw plugins list | grep feishu', { encoding: 'utf8' });
    if (output.includes('feishu-openclaw-plugin') && output.includes('loaded')) {
      logSuccess('飞书官方插件已加载');
    } else {
      logWarn('飞书官方插件未加载');
    }
  } catch (error) {
    logError('无法检查插件状态');
  }
  
  // 检查 Gateway
  logInfo('');
  logInfo('3. 检查 Gateway...');
  try {
    const output = execSync('openclaw status', { encoding: 'utf8' });
    if (output.includes('running')) {
      logSuccess('Gateway 运行中');
    } else {
      logWarn('Gateway 未运行');
    }
  } catch (error) {
    logError('无法检查 Gateway 状态');
  }
  
  // 检查日志
  logInfo('');
  logInfo('4. 检查最近日志...');
  try {
    const output = execSync('tail -20 /tmp/openclaw/openclaw-*.log 2>/dev/null | grep -i "feishu.*error" | tail -5', { encoding: 'utf8' });
    if (output) {
      logWarn('发现错误日志:');
      console.log(output);
    } else {
      logSuccess('没有发现明显错误');
    }
  } catch (error) {
    logInfo('日志文件不存在或为空');
  }
  
  logInfo('');
  logInfo('诊断完成！');
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.includes('--check')) {
    checkConfig();
  } else if (args.includes('--debug')) {
    debug();
  } else if (args.includes('--help') || args.includes('-h')) {
    console.log(`
feishu-multiagent-onboard - 飞书多 Agent 快速配置

用法:
  openclaw skill run feishu-multiagent-onboard          # 配置向导
  openclaw skill run feishu-multiagent-onboard --check  # 验证配置
  openclaw skill run feishu-multiagent-onboard --debug  # 故障诊断
  openclaw skill run feishu-multiagent-onboard --help   # 显示帮助
    `);
  } else {
    wizard();
  }
}

main();
