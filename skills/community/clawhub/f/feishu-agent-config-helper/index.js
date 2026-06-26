#!/usr/bin/env node
const colors = {
  reset: '\\x1b[0m',
  green: '\\x1b[32m',
  yellow: '\\x1b[33m',
  red: '\\x1b[31m',
  cyan: '\\x1b[36m',
  gray: '\\x1b[90m',
  bold: '\\x1b[1m'
};

const log = {
  info: (msg) => console.log(`${colors.cyan}ℹ${colors.reset} ${msg}`),
  success: (msg) => console.log(`${colors.green}✓${colors.reset} ${msg}`),
  warning: (msg) => console.log(`${colors.yellow}⚠${colors.reset} ${msg}`),
  error: (msg) => console.log(`${colors.red}✗${colors.reset} ${msg}`),
  step: (num, total, msg) => console.log(`\\n${colors.cyan}[${num}/${total}]${colors.reset} ${msg}`),
  preview: (msg) => console.log(`${colors.gray}${msg}${colors.reset}`),
  bold: (msg) => console.log(`${colors.bold}${msg}${colors.reset}`)
};

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

function generateConfig(options) {
  const {
    appid,
    appsecret,
    accountid,
    botname,
    agentid,
    chatid,
    routingmode,
    dmpolicy
  } = options;

  if (!appid || !appsecret) {
    log.error('错误: 缺少 --app-id 或 --app-secret。');
    log.info('请使用 --help 查看用法。');
    process.exit(1);
  }

  const generatedAccountId = accountid || `bot-${Math.random().toString(36).substring(2, 9)}`;
  const resolvedBotName = botname || '飞书机器人';
  const resolvedDmPolicy = dmpolicy || 'open';
  const resolvedRoutingMode = routingmode || 'account';

  console.log(`\n${colors.bold}--- 飞书机器人配置片段 ---${colors.reset}`);
  console.log(`${colors.cyan}将以下内容添加到您的 ~/.openclaw/openclaw.json 文件中相应位置。${colors.reset}`);

  log.step(1, 3, `在 "channels": {"feishu": {"accounts": {}}} 中添加账户配置`);
  console.log(`\`\`\`json
  "${generatedAccountId}": {
    "appId": "${appid}",
    "appSecret": "${appsecret}",
    "botName": "${resolvedBotName}",
    "dmPolicy": "${resolvedDmPolicy}",
    "allowFrom": ["*"],
    "enabled": true
  }\`\`\``);

  if (agentid) {
    log.step(2, 3, `在 "bindings": [] 中添加 Agent 绑定配置`);
    if (resolvedRoutingMode === 'account') {
      console.log(`\`\`\`json
  {
    "agentId": "${agentid}",
    "match": {
      "channel": "feishu",
      "accountId": "${generatedAccountId}"
    }
  }\`\`\``);
      log.info(`提示: 此为账户级绑定，该飞书账户的所有消息都将路由到 Agent "${agentid}"。`);
    } else if (resolvedRoutingMode === 'group' && chatid) {
      console.log(`\`\`\`json
  {
    "agentId": "${agentid}",
    "match": {
      "channel": "feishu",
      "peer": { "kind": "group", "id": "${chatid}" }
    }
  }\`\`\``);
      log.info(`提示: 此为群聊级绑定，特定群聊 "${chatid}" 的消息将路由到 Agent "${agentid}"。`);
      log.warning('请确保该机器人已被添加到指定群聊中！');
    } else if (resolvedRoutingMode === 'group' && !chatid) {
      log.error('错误: 路由模式为 "group" 时，必须提供 --chat-id。');
      process.exit(1);
    }
  } else {
    log.info('没有提供 --agent-id，跳过 Agent 绑定配置。您可以稍后手动添加。');
  }

  log.step(3, 3, `设置会话绑定颗粒度`);
  console.log(`\n${colors.yellow}请执行以下命令设置会话作用域：${colors.reset}`);
  console.log(`\`\`\`bash
openclaw config set session.dmScope "per-account-channel-peer"
\`\`\``);
  log.info(`提示: 这将确保每个飞书账户下的每个群聊/私聊可以绑定到不同的 Agent。`);

  console.log(`\n${colors.bold}--- 配置完成后 ---${colors.reset}`);
  console.log(`${colors.yellow}完成上述修改后，请务必重启 OpenClaw Gateway 以加载新配置：${colors.reset}`);
  console.log(`\`\`\`bash
openclaw gateway restart
\`\`\``);
  console.log(`${colors.green}祝您使用愉快！${colors.reset}`);
  console.log(`\n您的新账户 ID 是: ${colors.bold}${generatedAccountId}${colors.reset}`);
  if (agentid) console.log(`您的 Agent ID 是: ${colors.bold}${agentid}${colors.reset}`);
  if (chatid && resolvedRoutingMode === 'group') console.log(`您的群聊 ID 是: ${colors.bold}${chatid}${colors.reset}`);

  console.log(`\n${colors.bold}注意：${colors.reset} OpenClaw 的配置文件通常位于 ${colors.cyan}~/.openclaw/openclaw.json${colors.reset}`);
}

function showHelp() {
  console.log(`\n${colors.bold}feishu-agent-config-helper - 飞书 Agent 配置助手${colors.reset}\n`);
  console.log(`${colors.bold}用法:${colors.reset}\n  feishu-agent-config-helper [选项]\n`);
  console.log(`${colors.bold}选项:${colors.reset}\n  --app-id <id>          飞书应用的 App ID (必填)\n  --app-secret <secret>  飞书应用的 App Secret (必填)\n  --account-id <id>      为该飞书账户生成一个自定义标识 (可选, 默认自动生成)\n  --bot-name <name>      机器人名称 (可选, 默认: "飞书机器人")\n  --dm-policy <policy>   DM 消息处理策略: open/pairing/allowlist (可选, 默认: open)\n  --agent-id <id>        要绑定的 Agent ID (可选)\n  --chat-id <id>         飞书群聊 ID (oc_xxx 格式), 在群聊绑定模式下必填\n  --routing-mode <mode>  路由模式: account (账户级) / group (群聊级) (可选, 默认: account)\n  --help                 显示帮助信息\n`);
  console.log(`${colors.bold}示例:${colors.reset}\n  # 账户级绑定: 将飞书应用的全部消息路由到名为 "my-agent" 的 Agent\n  feishu-agent-config-helper --app-id cli_xxxxxx --app-secret yyyyyyy --agent-id my-agent --routing-mode account\n\n  # 群聊级绑定: 将特定群聊的消息路由到名为 "group-agent" 的 Agent\n  feishu-agent-config-helper --app-id cli_xxxxxx --app-secret yyyyyyy --agent-id group-agent --chat-id oc_zzzzzzzz --routing-mode group\n`);
}

const options = parseArgs();

if (options.help || Object.keys(options).length === 0) {
  showHelp();
} else {
  generateConfig(options);
}
