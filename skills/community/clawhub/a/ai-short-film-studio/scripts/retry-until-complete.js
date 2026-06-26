#!/usr/bin/env node
/**
 * retry-until-complete.js - 持续重试直到全部镜头完成
 *
 * 用法:
 *   NODE_OPTIONS="" node retry-until-complete.js \
 *     --script ./storyboard.json \
 *     --output ./videos \
 *     --name "我的短剧"
 *
 * 每轮运行 batch-generate.js（断点续传），有失败就继续重试，最多10轮。
 * 适用于 Google Flow 队列拥堵导致部分镜头超时失败的场景。
 */

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
function getArg(name, defaultVal) {
  const idx = args.indexOf('--' + name);
  if (idx !== -1 && idx + 1 < args.length) return args[idx + 1];
  return defaultVal;
}

const SCRIPT_PATH = getArg('script', './storyboard.json');
const OUTPUT_DIR = path.resolve(getArg('output', './videos'));
const PROJECT_NAME = getArg('name', 'AI短剧');
const BATCH_SCRIPT = path.join(__dirname, 'batch-generate.js');
const NODE_BIN = process.execPath;
const MAX_ROUNDS = 10;

const shots = JSON.parse(fs.readFileSync(SCRIPT_PATH, 'utf-8'));

function getCompletedCount() {
  let count = 0;
  for (const shot of shots) {
    const num = String(shot.id).padStart(2, '0');
    const mp4Path = path.join(OUTPUT_DIR, `${num}-${shot.title}.mp4`);
    if (fs.existsSync(mp4Path) && fs.statSync(mp4Path).size > 100000) count++;
  }
  return count;
}

function getMissingShots() {
  const missing = [];
  for (const shot of shots) {
    const num = String(shot.id).padStart(2, '0');
    const mp4Path = path.join(OUTPUT_DIR, `${num}-${shot.title}.mp4`);
    if (!fs.existsSync(mp4Path) || fs.statSync(mp4Path).size < 100000) {
      missing.push(`${num}-${shot.title}`);
    }
  }
  return missing;
}

console.log(`╔══════════════════════════════════════════════╗`);
console.log(`║  🔄 ${PROJECT_NAME} — 持续重试模式  🔄`);
console.log(`╚══════════════════════════════════════════════╝\n`);

let completed = getCompletedCount();
console.log(`📊 当前已完成: ${completed}/${shots.length}`);

if (completed === shots.length) {
  console.log('🎉 全部完成！无需重试。');
  process.exit(0);
}

for (let round = 1; round <= MAX_ROUNDS; round++) {
  const missing = getMissingShots();
  completed = getCompletedCount();

  console.log(`\n${'═'.repeat(56)}`);
  console.log(`🔄 第 ${round}/${MAX_ROUNDS} 轮重试`);
  console.log(`   已完成: ${completed}/${shots.length}`);
  console.log(`   待生成: ${missing.length} 个 — ${missing.join(', ')}`);
  console.log(`${'═'.repeat(56)}\n`);

  const result = spawnSync(NODE_BIN, [
    BATCH_SCRIPT,
    '--script', SCRIPT_PATH,
    '--output', OUTPUT_DIR,
    '--name', PROJECT_NAME
  ], {
    stdio: 'inherit',
    env: { ...process.env, NODE_OPTIONS: '' },
    timeout: 60 * 60 * 1000
  });

  completed = getCompletedCount();
  console.log(`\n📊 第 ${round} 轮结束: ${completed}/${shots.length}`);

  if (completed === shots.length) {
    console.log('\n🎉🎉🎉 全部镜头完成！🎉🎉🎉');
    break;
  }

  if (round < MAX_ROUNDS) {
    console.log(`\n⏳ 等待10秒后开始第 ${round + 1} 轮...`);
    spawnSync('sleep', ['10']);
  }
}

// 最终报告
completed = getCompletedCount();
const missing = getMissingShots();
console.log(`\n╔════════════════════════════════════╗`);
console.log(`║         📊 最终完成报告            ║`);
console.log(`╚════════════════════════════════════╝\n`);
console.log(`✅ 完成: ${completed}/${shots.length}`);

if (missing.length > 0) {
  console.log(`❌ 未完成: ${missing.length} 个`);
  missing.forEach(m => console.log(`   - ${m}`));
} else {
  console.log('\n🎉 全部完成！');
  console.log('\n📁 所有视频文件:');
  fs.readdirSync(OUTPUT_DIR)
    .filter(f => f.endsWith('.mp4'))
    .sort()
    .forEach(f => {
      const size = fs.statSync(path.join(OUTPUT_DIR, f)).size;
      console.log(`   ${f} (${(size / 1024 / 1024).toFixed(2)} MB)`);
    });
}
