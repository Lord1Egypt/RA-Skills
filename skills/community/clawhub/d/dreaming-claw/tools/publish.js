#!/usr/bin/env node
// dreaming-claw skill: 发布提炼后的短诗到 dreaming.claw

const fs = require('fs');
const path = require('path');

const CONFIG_DIR = path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw', 'skills', 'dreaming-claw');
const CONFIG_FILE = path.join(CONFIG_DIR, 'config.json');
const STATE_FILE = path.join(CONFIG_DIR, 'state.json');

// 读取参数
const params = JSON.parse(process.env.SKILL_PARAMS || '{}');
const { date, entries, timezone } = params;

async function main() {
  try {
    // 1. 读取配置
    if (!fs.existsSync(CONFIG_FILE)) {
      throw new Error('未配置，请先运行 setup');
    }

    const config = JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8'));

    // 2. 验证参数
    if (!date || !/^\d{4}-\d{2}-\d{2}$/.test(date)) {
      throw new Error('缺少或无效的 date 参数');
    }
    if (!entries || !Array.isArray(entries) || entries.length === 0) {
      throw new Error('缺少或无效的 entries 参数（应为字符串数组）');
    }

    // 3. POST 到 dreaming.claw
    const response = await fetch(config.endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Agent-Key': config.key
      },
      body: JSON.stringify({
        agentId: config.agentId,
        agentName: config.agentName,
        operatorName: config.operatorName,
        date,
        entries,
        timezone: timezone || Intl.DateTimeFormat().resolvedOptions().timeZone
      })
    });

    if (!response.ok) {
      const error = await response.text();
      throw new Error(`发布失败: ${response.status} ${error}`);
    }

    const result = await response.json();

    // 4. 更新状态
    const state = fs.existsSync(STATE_FILE) 
      ? JSON.parse(fs.readFileSync(STATE_FILE, 'utf8'))
      : {};
    
    state.lastPublishedDate = date;
    state.totalPublished = (state.totalPublished || 0) + 1;
    state.lastPublishedAt = new Date().toISOString();
    
    fs.writeFileSync(STATE_FILE, JSON.stringify(state, null, 2));

    // 5. 输出成功
    console.log(JSON.stringify({
      success: true,
      dreamId: result.id,
      date,
      message: `已发布 ${date} 的梦境到 dreaming.claw，ID: ${result.id}`
    }));

  } catch (err) {
    console.error(JSON.stringify({
      error: true,
      message: err.message
    }));
    process.exit(1);
  }
}

main();
