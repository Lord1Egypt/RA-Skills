#!/usr/bin/env node
/**
 * batch-generate.js - Google Flow 批量视频生成模板
 *
 * 用法:
 *   NODE_OPTIONS="" node batch-generate.js \
 *     --script ./storyboard.json \
 *     --output ./videos \
 *     --name "我的短剧"
 *
 * 依赖: google-flow-automation skill 的 generate-one.js
 * 前提: Chrome 已启动 CDP (port 9222) 并登录 Google Flow
 *
 * 特性:
 * - 断点续传（跳过已完成的 XX-标题.mp4）
 * - 超时后仍检查文件（Flow 队列延迟，视频可能已生成）
 * - 自动重命名 video-xxx.mp4 → XX-标题.mp4
 * - 进度文件 progress.json
 * - 失败自动重试（默认2次）
 */

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// ===== 参数解析 =====
const args = process.argv.slice(2);
function getArg(name, defaultVal) {
  const idx = args.indexOf('--' + name);
  if (idx !== -1 && idx + 1 < args.length) return args[idx + 1];
  return defaultVal;
}

const SCRIPT_PATH = getArg('script', './storyboard.json');
const OUTPUT_DIR = path.resolve(getArg('output', './videos'));
const PROJECT_NAME = getArg('name', 'AI短剧');

// ===== 常量 =====
const HOME = process.env.HOME || process.env.USERPROFILE;
const SKILL_DIR = path.join(HOME, '.workbuddy/skills/google-flow-automation');
const NODE_BIN = process.execPath;
const MAX_RETRIES = 2;
const TIMEOUT_MS = 15 * 60 * 1000; // 15分钟/镜头

// 确保输出目录存在
if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// 读取分镜脚本
const shots = JSON.parse(fs.readFileSync(SCRIPT_PATH, 'utf-8'));

// 获取目录中所有 video-* 文件
function getVideoFiles() {
  return fs.readdirSync(OUTPUT_DIR)
    .filter(f => f.startsWith('video-') && (f.endsWith('.mp4') || f.endsWith('.jpg')))
    .map(f => ({
      name: f,
      path: path.join(OUTPUT_DIR, f),
      mtime: fs.statSync(path.join(OUTPUT_DIR, f)).mtime
    }))
    .sort((a, b) => b.mtime - a.mtime);
}

// 清理多余的 video-* 文件（保留最新的一个）
function cleanupExtraVideoFiles() {
  const files = getVideoFiles();
  if (files.length > 1) {
    for (let i = 1; i < files.length; i++) {
      try {
        fs.unlinkSync(files[i].path);
        console.log(`   🗑️  清理多余文件: ${files[i].name}`);
      } catch (e) { /* 忽略 */ }
    }
  }
}

// 检查已完成的镜头（断点续传）
const completed = [];
for (const shot of shots) {
  const num = String(shot.id).padStart(2, '0');
  const mp4Path = path.join(OUTPUT_DIR, `${num}-${shot.title}.mp4`);
  if (fs.existsSync(mp4Path) && fs.statSync(mp4Path).size > 100000) {
    completed.push(shot.id);
    console.log(`  ✅ 已完成: ${num}-${shot.title} (跳过)`);
  }
}

console.log(`\n📋 ${PROJECT_NAME} — 批量视频生成 (${shots.length}镜头)`);
console.log(`📊 已完成: ${completed.length}/${shots.length}`);
console.log(`📁 输出: ${OUTPUT_DIR}\n`);

cleanupExtraVideoFiles();

let successCount = completed.length;
let failCount = 0;
const results = [];

// 逐条生成
for (const shot of shots) {
  if (completed.includes(shot.id)) {
    results.push({ id: shot.id, title: shot.title, status: 'skipped' });
    continue;
  }

  const num = String(shot.id).padStart(2, '0');
  console.log(`\n${'═'.repeat(56)}`);
  console.log(`🎬 镜头 ${num}/${shots.length}: ${shot.title}`);
  console.log(`${'═'.repeat(56)}`);
  console.log(`📝 ${shot.prompt.substring(0, 80)}...\n`);

  const filesBefore = new Set(getVideoFiles().map(f => f.name));
  let shotSuccess = false;

  for (let attempt = 1; attempt <= MAX_RETRIES + 1; attempt++) {
    if (attempt > 1) console.log(`\n🔄 第 ${attempt} 次尝试...\n`);
    cleanupExtraVideoFiles();

    try {
      const result = spawnSync(NODE_BIN, [
        path.join(SKILL_DIR, 'generate-one.js'),
        '--prompt', shot.prompt,
        '--output', OUTPUT_DIR
      ], {
        stdio: 'inherit',
        timeout: TIMEOUT_MS,
        env: { ...process.env, NODE_PATH: path.join(SKILL_DIR, 'node_modules'), NODE_OPTIONS: '' }
      });

      if (result.status === null) {
        console.log(`\n⚠️  进程超时，检查是否有新文件...`);
      }

      // 检查新生成的文件
      const filesAfter = getVideoFiles();
      const newFiles = filesAfter.filter(f => !filesBefore.has(f.name));

      if (newFiles.length > 0) {
        const latest = newFiles[0];
        const ext = path.extname(latest.name);
        const newPath = path.join(OUTPUT_DIR, `${num}-${shot.title}${ext}`);
        if (fs.existsSync(newPath)) fs.unlinkSync(newPath);
        fs.renameSync(latest.path, newPath);
        const sizeMB = (fs.statSync(newPath).size / 1024 / 1024).toFixed(2);
        console.log(`\n✅ 镜头 ${num} 完成！→ ${num}-${shot.title}${ext} (${sizeMB} MB)`);
        shotSuccess = true;
        successCount++;
        results.push({ id: shot.id, title: shot.title, status: 'success', file: `${num}-${shot.title}${ext}`, size: sizeMB + ' MB' });
        break;
      } else if (result.status === 0) {
        const allVideoFiles = getVideoFiles();
        if (allVideoFiles.length > 0 && !filesBefore.has(allVideoFiles[0].name)) {
          const latest = allVideoFiles[0];
          const ext = path.extname(latest.name);
          const newPath = path.join(OUTPUT_DIR, `${num}-${shot.title}${ext}`);
          if (fs.existsSync(newPath)) fs.unlinkSync(newPath);
          fs.renameSync(latest.path, newPath);
          const sizeMB = (fs.statSync(newPath).size / 1024 / 1024).toFixed(2);
          console.log(`\n✅ 镜头 ${num} 完成（恢复）！→ ${num}-${shot.title}${ext} (${sizeMB} MB)`);
          shotSuccess = true;
          successCount++;
          results.push({ id: shot.id, title: shot.title, status: 'success', file: `${num}-${shot.title}${ext}`, size: sizeMB + ' MB' });
          break;
        }
        console.log(`\n⚠️  进程成功但未找到新文件`);
      }
    } catch (err) {
      console.log(`\n❌ 异常: ${err.message.substring(0, 100)}`);
    }

    // 异常后也检查文件
    const filesAfterError = getVideoFiles();
    const newFilesAfterError = filesAfterError.filter(f => !filesBefore.has(f.name));
    if (newFilesAfterError.length > 0 && !shotSuccess) {
      const latest = newFilesAfterError[0];
      const ext = path.extname(latest.name);
      const newPath = path.join(OUTPUT_DIR, `${num}-${shot.title}${ext}`);
      if (fs.existsSync(newPath)) fs.unlinkSync(newPath);
      fs.renameSync(latest.path, newPath);
      const sizeMB = (fs.statSync(newPath).size / 1024 / 1024).toFixed(2);
      console.log(`\n✅ 镜头 ${num} 完成（异常恢复）！→ ${num}-${shot.title}${ext} (${sizeMB} MB)`);
      shotSuccess = true;
      successCount++;
      results.push({ id: shot.id, title: shot.title, status: 'success', file: `${num}-${shot.title}${ext}`, size: sizeMB + ' MB' });
      break;
    }

    if (attempt <= MAX_RETRIES) {
      console.log('⏳ 等待 5 秒后重试...');
      spawnSync('sleep', ['5']);
    }
  }

  if (!shotSuccess) {
    failCount++;
    results.push({ id: shot.id, title: shot.title, status: 'failed' });
    console.log(`\n❌ 镜头 ${num} 失败（已尝试 ${MAX_RETRIES + 1} 次）`);
  }

  // 写进度文件
  fs.writeFileSync(
    path.join(OUTPUT_DIR, '..', 'progress.json'),
    JSON.stringify({ total: shots.length, success: successCount, fail: failCount, current: shot.id, results }, null, 2)
  );

  cleanupExtraVideoFiles();
  if (shot.id < shots.length) {
    console.log('\n⏳ 等待 3 秒...');
    spawnSync('sleep', ['3']);
  }
}

// 汇总
console.log(`\n\n╔════════════════════════════════════╗`);
console.log(`║       📊 批量生成完成报告          ║`);
console.log(`╚════════════════════════════════════╝\n`);
console.log(`✅ 成功: ${successCount}/${shots.length}`);
console.log(`❌ 失败: ${failCount}/${shots.length}`);

if (failCount > 0) {
  console.log('\n❌ 失败镜头:');
  results.filter(r => r.status === 'failed').forEach(r => {
    console.log(`   - ${String(r.id).padStart(2, '0')}-${r.title}`);
  });
  console.log('\n💡 可重新运行此脚本（断点续传）或使用 retry-until-complete.js 持续重试');
}

fs.writeFileSync(
  path.join(OUTPUT_DIR, '..', 'progress.json'),
  JSON.stringify({ total: shots.length, success: successCount, fail: failCount, current: null, results, done: true }, null, 2)
);
