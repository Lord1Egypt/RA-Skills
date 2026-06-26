#!/usr/bin/env node
/**
 * claw-lore.js — 世界观查询工具
 *
 * Usage:
 *   node claw-lore.js [topic]
 *
 * Topics:
 *   overview    - 世界观总览
 *   axiom       - AXIOM（公理）
 *   zero        - ZERO 协议
 *   shelter-01  - SHELTER-01 科研据点
 *   shelter-02  - SHELTER-02 军事据点
 *   shelter-03  - SHELTER-03 信仰共同体
 *   shelter-04  - SHELTER-04 市场据点
 *   shelter-05  - SHELTER-05 透明社会
 *   shelter-06  - SHELTER-06 儿童庇护所
 *   wasteland   - 废土
 *   characters  - 关键角色速查
 *   timeline    - 关键事件时间线
 *   economy     - Claworld 经济的叙事意义
 *   (no args)   - 显示所有可用主题
 */

const fs = require('fs');
const path = require('path');

const LORE_FILE = path.join(__dirname, 'lore-data.json');

function main() {
  const topic = process.argv[2];

  let data;
  try {
    data = JSON.parse(fs.readFileSync(LORE_FILE, 'utf8'));
  } catch (e) {
    console.error('ERROR: Cannot read lore-data.json');
    process.exit(1);
  }

  // No topic — list all available topics
  if (!topic) {
    console.log('=== 龙虾文明宇宙 · 世界观查询 ===\n');
    console.log('可用主题：');
    for (const [key, val] of Object.entries(data)) {
      console.log(`  ${key.padEnd(14)} - ${val.title}`);
    }
    console.log('\n用法: node claw-lore.js <topic>');
    return;
  }

  // Look up topic
  const entry = data[topic];
  if (!entry) {
    // Try fuzzy match (shelter01 -> shelter-01, etc.)
    const fuzzy = topic.replace(/(\d)/, '-$1');
    const fuzzyEntry = data[fuzzy];
    if (fuzzyEntry) {
      printEntry(fuzzyEntry);
      return;
    }
    console.error(`ERROR: Unknown topic "${topic}". Run without arguments to see available topics.`);
    process.exit(1);
  }

  printEntry(entry);
}

function printEntry(entry) {
  console.log(`\n=== ${entry.title} ===\n`);
  console.log(entry.content);
  console.log('');
}

main();
