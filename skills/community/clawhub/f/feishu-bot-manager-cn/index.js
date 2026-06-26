#!/usr/bin/env node
/**
 * feishu-bot-manager
 * 飞书多账户机器人配置管理 Skill
 * 
 * 支持的路由绑定方案：
 * 1. 账户级绑定 - 该飞书账户的所有消息路由到指定 Agent
 * 2. 群聊级绑定 - 特定群聊的消息路由到指定 Agent
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置路径
const CONFIG_PATH = path.join(process.env.HOME, '.openclaw', 'openclaw.json');
const BACKUP_DIR = path.join(process.env.HOME, '.openclaw', 'backups');

// 颜色输出
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  yellow: '\x1b[33m',
  red: '\x1b[31m',
  cyan: '\x1b[36m',
  gray: '\x1b[90m',
  bold: '\x1b[1m'
};

const log = {
  info: (msg) => console.log(`${colors.cyan}ℹ${colors.reset} ${msg}`),
  success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  step: (num, total, msg) => console.log(`\n${colors.cyan}[${num}/${total}]${colors.reset} ${msg}`),
  preview: (msg) => console.log(`${colors.gray}${msg}${colors.reset}`),
  bold: (msg) => console.log(`${colors.bold}${msg}${colors.reset}`)
};

// 读取配置
function loadConfig() {
  try {
    const content = fs.readFileSync(CONFIG_PATH, 'utf8');
    return JSON.parse(content);
  } catch (err) {
    log.error(`读取配置失败: ${err.message}`);
    process.exit(1);
  }
}

// 保存配置
function saveConfig(config) {
  try {
    fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2), 'utf8');
    return true;
  } catch (err) {
    log.error(`保存配置失败: ${err.message}`);
    return false;
  }
}

// 创建备份
function createBackup() {
  try {
    if (!fs.existsSync(BACKUP_DIR)) {
      fs.mkdirSync(BACKUP_DIR, { recursive: true });
    }
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
    const backupPath = path.join(BACKUP_DIR, `openclaw.json.${timestamp}`);
    fs.copyFileSync(CONFIG_PATH, backupPath);
    return backupPath;
  } catch (err) {
    log.error(`创建备份失败: ${err.message}`);
    return null;
  }
}

// 显示路由方案说明
function showRoutingOptions() {
  console.log(`
${colors.bold}📋 路由绑定方案${colors.reset}

${colors.bold}方案 1：账户级绑定${colors.reset}
  该飞书账户的所有消息 → 指定 Agent
  适用：一个机器人专门服务一个 Agent
  
${colors.bold}方案 2：群聊级绑定${colors.reset}
  特定群聊的消息 → 指定 Agent
  适用：把 Agent 绑定到特定群聊

${colors.yellow}提示：群聊级绑定优先级更高，会覆盖账户级绑定！${colors.reset}
`);
}

// 快速模式
async function quickMode(options) {
  console.log(`\n${colors.cyan}🤖 飞书机器人配置助手${colors.reset}\n`);
  
  const { 
    appid, 
    appsecret, 
    accountid,
    botname,
    agentid, 
    chatid,
    routingmode
  } = options;
  
  if (!appid || !appsecret) {
    log.error('需要提供 --app-id 和 --app-secret');
    process.exit(1);
  }
  
  const config = loadConfig();
  const accountId = accountid || `bot-${Date.now()}`;
  
  // 创建备份
  const backupPath = createBackup();
  log.success(`配置已备份: ${path.basename(backupPath)}`);
  
  // 确保 channels.feishu.accounts 存在
  if (!config.channels) config.channels = {};
  if (!config.channels.feishu) config.channels.feishu = { enabled: true };
  if (!config.channels.feishu.accounts) config.channels.feishu.accounts = {};
  
  // 添加账户
  config.channels.feishu.accounts[accountId] = {
    appId: appid,
    appSecret: appsecret,
    botName: botname || 'Feishu Bot',
    dmPolicy: options.dmpolicy || 'open',
    allowFrom: ['*'],
    enabled: true
  };
  
  // 添加绑定
  if (!config.bindings) config.bindings = [];
  
  const mode = routingmode || 'account';
  
  if (mode === 'account' && agentid) {
    // 账户级绑定：该账户所有消息路由到指定 Agent
    config.bindings.push({
      agentId: agentid,
      match: {
        channel: 'feishu',
        accountId: accountId
      }
    });
    log.success(`已添加账户级绑定: ${agentid} ← ${accountId}`);
  } else if (mode === 'group' && agentid && chatid) {
    // 群聊级绑定：特定群聊消息路由到指定 Agent
    config.bindings.push({
      agentId: agentid,
      match: {
        channel: 'feishu',
        peer: { kind: 'group', id: chatid }
      }
    });
    log.success(`已添加群聊级绑定: ${agentid} ← ${chatid}`);
  }
  
  saveConfig(config);
  log.success('配置已更新');
  
  // 设置会话绑定颗粒度
  log.info('设置会话绑定颗粒度...');
  try {
    execSync('openclaw config set session.dmScope "per-account-channel-peer"', { stdio: 'pipe' });
    log.success('会话绑定颗粒度已设置');
  } catch (err) {
    log.warning('设置 dmScope 失败，请手动执行:');
    console.log('  openclaw config set session.dmScope "per-account-channel-peer"');
  }
  
  // 重启
  log.warning('正在重启 Gateway...');
  try {
    execSync('openclaw gateway restart', { stdio: 'inherit' });
    log.success('Gateway 重启完成');
  } catch (err) {
    log.error(`重启失败: ${err.message}`);
    log.info('请手动执行: openclaw gateway restart');
  }
  
  // 完成提示
  console.log('\n' + '─'.repeat(50));
  log.success('配置完成！');
  console.log('\n配置摘要:');
  console.log(`  账户 ID: ${accountId}`);
  console.log(`  路由模式: ${mode}`);
  if (agentid) console.log(`  Agent: ${agentid}`);
  if (chatid) console.log(`  群聊: ${chatid}`);
  console.log('\n如配置有误，可从备份恢复:');
  console.log(`  cp ${backupPath} ${CONFIG_PATH}`);
  console.log('─'.repeat(50) + '\n');
}

// 处理命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2).replace(/-/g, '');
      const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : 'true';
      options[key] = value;
      if (value !== 'true') i++;
    }
  }
  
  return options;
}

// 主入口
const options = parseArgs();

if (options.help || options.h) {
  showRoutingOptions();
  console.log(`
${colors.bold}用法:${colors.reset}
  node index.js [选项]

${colors.bold}选项:${colors.reset}
  --app-id <id>          飞书 App ID (必填)
  --app-secret <secret>  飞书 App Secret (必填)
  --account-id <id>      账户标识 (可选, 默认自动生成)
  --bot-name <name>      机器人名称 (可选)
  --dm-policy <policy>   DM 策略: open/pairing/allowlist (默认: open)
  --agent-id <id>        要绑定的 Agent ID (可选)
  --chat-id <id>         群聊 ID oc_xxx (群聊绑定时需要)
  --routing-mode <mode>  路由模式: account/group (默认: account)
  --help, -h             显示帮助

${colors.bold}示例:${colors.reset}
  # 账户级绑定 - 该机器人所有消息都由指定 Agent 处理
  node index.js --app-id cli_xxx --app-secret yyy --agent-id recruiter --routing-mode account

  # 群聊级绑定 - 特定群聊的消息由指定 Agent 处理
  node index.js --app-id cli_xxx --app-secret yyy --agent-id recruiter --chat-id oc_xxx --routing-mode group
`);
  process.exit(0);
}

if (options.appid) {
  quickMode(options);
} else {
  log.error('请提供 --app-id 和 --app-secret，或使用 --help 查看帮助');
  process.exit(1);
}
