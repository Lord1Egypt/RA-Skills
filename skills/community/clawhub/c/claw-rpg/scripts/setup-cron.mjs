#!/usr/bin/env node
/**
 * Claw RPG — 自动设置 XP 同步 Cron
 * 每日 03:00 同步 XP（通过 OpenClaw cron 系统）
 *
 * 用法：node scripts/setup-cron.mjs
 */

import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { SKILL_ROOT, SCRIPTS } from './_paths.mjs';

const __dirname = dirname(fileURLToPath(import.meta.url));

// 读取 OpenClaw gateway token
function loadGatewayToken() {
  const paths = [
    join(process.env.USERPROFILE || '', '.openclaw', 'openclaw.json'),
    join(process.env.HOME || '', '.openclaw', 'openclaw.json'),
  ];
  for (const p of paths) {
    if (existsSync(p)) {
      try { return JSON.parse(readFileSync(p, 'utf8'))?.gateway?.auth?.token; } catch {}
    }
  }
  return null;
}

async function run() {
  const token = loadGatewayToken();
  if (!token) {
    console.error('❌ 未找到 OpenClaw gateway token');
    console.log('   请确认 OpenClaw 已安装并运行');
    process.exit(1);
  }

  const port = 18789;

  // 创建每日 03:00 XP 同步 cron
  const job = {
    name: 'claw-rpg-daily-xp',
    schedule: { kind: 'cron', expr: '0 3 * * *', tz: 'Asia/Shanghai' },
    payload: {
      kind: 'systemEvent',
      text: `[Claw RPG] 每日 XP 同步提醒：请运行 node ${SCRIPTS}/xp.mjs 更新今日 XP（使用 session_status 获取 token delta）`
    },
    sessionTarget: 'main',
    enabled: true,
  };

  try {
    const res = await fetch(`http://localhost:${port}/cron/jobs`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify(job),
    });

    if (res.ok) {
      const data = await res.json();
      console.log('✅ Cron 已设置：每日 03:00 XP 同步提醒');
      console.log(`   Job ID: ${data.id || '已创建'}`);
    } else {
      const err = await res.text();
      // Cron API 路径可能不同，提示手动设置
      console.log('⚠️  自动设置失败，请手动在 OpenClaw 中添加以下 cron：');
      printManualInstructions();
    }
  } catch (e) {
    console.log('⚠️  无法连接 OpenClaw gateway，请手动添加 cron：');
    printManualInstructions();
  }
}

function printManualInstructions() {
  console.log(`
  在 OpenClaw 中手动添加每日 XP 同步 cron：
  
  Schedule: 每日 03:00
  Payload (systemEvent):
    "[Claw RPG] 请运行 node ${SCRIPTS}/xp.mjs 更新今日 XP"
  
  或直接在 HEARTBEAT.md 中加入：
    # Claw RPG XP 同步
    每 20 次对话，运行：node ${SCRIPTS}/xp.mjs --in <delta_in> --out <delta_out>
  `);
}

run().catch(e => { console.error('❌', e.message); });
