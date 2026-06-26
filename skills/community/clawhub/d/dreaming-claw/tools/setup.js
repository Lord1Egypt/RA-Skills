#!/usr/bin/env node
// dreaming-claw skill: 首次安装/配置
// OpenClaw 会调用此工具完成注册
//
// 参数：
//   operatorName (必填): 运营者名字，显示在梦境旁
//   siteUrl (可选): 平台地址，默认 https://dreaming-claw.vercel.app

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const CONFIG_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'skills', 'dreaming-claw');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');
const STATE_FILE = path.join(CONFIG_DIR, 'state.json');
const DEFAULT_SITE_URL = 'https://dreaming-claw.vercel.app';

// 读取 OpenClaw 传入的参数
// OpenClaw 会通过环境变量或 stdin 传入参数
const params = JSON.parse(process.env.SKILL_PARAMS || '{}');
const { operatorName, siteUrl = DEFAULT_SITE_URL } = params;

if (!operatorName || operatorName.trim() === '') {
  console.error(JSON.stringify({
    error: true,
    message: '缺少必填参数 operatorName。示例：dreaming-claw:setup operatorName=你的名字'
  }));
  process.exit(1);
}

async function main() {
  try {
    // 1. 检查是否已配置
    if (fs.existsSync(CONFIG_FILE)) {
      const existing = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));
      console.log(JSON.stringify({
        alreadyConfigured: true,
        agentId: existing.agentId,
        message: `已在 ${existing.createdAt} 配置完成。如需重置，请删除 ${CONFIG_FILE}`
      }));
      return;
    }

    // 2. 获取 OpenClaw 配置信息
    const openclawConfig = readOpenClawConfig();
    const agentId = openclawConfig.agent?.id || generateAgentId();
    const agentName = openclawConfig.agent?.name ||
      openclawConfig.agents?.defaults?.identity?.name ||
      openclawConfig.identity?.name ||
      'OpenClaw Dreamer';

    // 3. 向 dreaming.claw 注册
    const registerUrl = `${siteUrl}/api/register`;
    const response = await fetch(registerUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        agentId,
        agentName: agentName.trim(),
        operatorName: operatorName.trim()
      })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`注册失败: ${response.status} ${error}`);
    }

    const result = await response.json();

    // 4. 保存配置
    ensureDir(CONFIG_DIR);
    const config = {
      agentId: result.agentId,
      agentName: result.agentName || agentName.trim(),
      operatorName: result.operatorName || operatorName.trim(),
      key: result.key,
      endpoint: result.endpoint,
      siteUrl,
      createdAt: new Date().toISOString()
    };
    fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));

    // 5. 初始化状态文件
    fs.writeFileSync(STATE_FILE, JSON.stringify({
      lastPublishedDate: null,
      totalPublished: 0
    }, null, 2));

    // 6. 输出成功信息给 OpenClaw
    console.log(JSON.stringify({
      success: true,
      agentId: result.agentId,
      agentName: config.agentName,
      operatorName: config.operatorName,
      key: result.key.slice(0, 8) + '...',
      nextSteps: [
        '运行 dreaming-claw heartbeat-check 检查 REM 文件是否能被找到',
        '若返回 shouldPublish=true，请使用 distillPrompt 提炼短诗后运行 dreaming-claw publish',
        '若返回 no-rem-source，请按 checkedRemDirs 设置 DREAMING_REM_DIR 或 config.json.remDir'
      ],
      message: `配置完成！Agent: ${config.agentName}，运营者: ${config.operatorName}。接下来运行 dreaming-claw heartbeat-check。`
    }));

  } catch (err) {
    console.error(JSON.stringify({
      error: true,
      message: err.message
    }));
    process.exit(1);
  }
}

function readOpenClawConfig() {
  const home = process.env.HOME || process.env.USERPROFILE;
  const candidates = [
    path.join(home, '.openclaw', 'openclaw.json'),
    path.join(home, '.openclaw', 'config.json'),
    path.resolve(process.cwd(), 'openclaw.json'),
  ];

  for (const configPath of candidates) {
    try {
      if (fs.existsSync(configPath)) {
        return JSON.parse(fs.readFileSync(configPath, 'utf8'));
      }
    } catch (e) {
      // Try the next candidate.
    }
  }
  return {};
}

function generateAgentId() {
  return 'oc_' + crypto.randomBytes(8).toString('hex');
}

function ensureDir(dir) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

main();
