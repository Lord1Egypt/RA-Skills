#!/usr/bin/env node
/**
 * Claw RPG — XP 恢復腳本（每日凌晨 03:00 由 cron 調用）
 *
 * 邏輯：
 *   1. 讀 character.json，取 conversations 和 lastXpSync
 *   2. 計算距上次 sync 過了多少小時
 *   3. 估算這段時間的對話次數（按平均每天 20 次對話）
 *      estimatedConvs = Math.round(hoursElapsed / 24 * 20)
 *      若 estimatedConvs <= 0，退出（無需補償）
 *   4. 每估算 1 次對話 = consumed: 400, produced: 200
 *      調用 run({ consumed, produced, conversations })
 *   5. 更新 dailyXpStart = 當前 xp（供 report.mjs 計算今日增量）
 *
 * 用法：node scripts/sync-xp-recovery.mjs
 */

import { readFileSync, writeFileSync, existsSync } from 'fs';
import { CHARACTER_FILE } from './_paths.mjs';
import { run as syncXp } from './xp.mjs';

async function main() {
  if (!existsSync(CHARACTER_FILE)) {
    console.error('❌ character.json 未找到，請先執行 init.mjs');
    process.exit(1);
  }

  const char = JSON.parse(readFileSync(CHARACTER_FILE, 'utf8'));

  // ── 1. 計算距上次 sync 的小時數 ────────────────────────────────
  const lastSync = char.lastXpSync ? new Date(char.lastXpSync) : null;
  if (!lastSync || isNaN(lastSync.getTime())) {
    console.log('⚠️  lastXpSync 不存在或無效，跳過恢復（設置 dailyXpStart）');
    // 仍然設置 dailyXpStart
    char.dailyXpStart = char.xp;
    char.updatedAt    = new Date().toISOString();
    writeFileSync(CHARACTER_FILE, JSON.stringify(char, null, 2), 'utf8');
    console.log(`📌 dailyXpStart 已設置為 ${char.xp}`);
    return;
  }

  const now          = new Date();
  const hoursElapsed = (now - lastSync) / (1000 * 60 * 60);

  console.log(`⏱️  距上次 XP sync：${hoursElapsed.toFixed(1)} 小時`);

  // ── 2. 估算對話次數 ────────────────────────────────────────────
  // 平均每天 20 次對話
  const estimatedConvs = Math.round(hoursElapsed / 24 * 20);

  if (estimatedConvs <= 0) {
    console.log('✅ 距上次 sync 不足 0.5 天，無需補償。');
    // 仍然更新 dailyXpStart
    char.dailyXpStart = char.xp;
    char.updatedAt    = new Date().toISOString();
    writeFileSync(CHARACTER_FILE, JSON.stringify(char, null, 2), 'utf8');
    console.log(`📌 dailyXpStart 已設置為 ${char.xp}`);
    return;
  }

  console.log(`📊 估算補償對話次數：${estimatedConvs} 次`);
  console.log(`   consumed: ${estimatedConvs * 400}, produced: ${estimatedConvs * 200}`);

  // ── 3. 調用 run() 補充 XP ──────────────────────────────────────
  const xpBefore = char.xp;
  const result   = await syncXp({
    consumed:      estimatedConvs * 400,
    produced:      estimatedConvs * 200,
    conversations: estimatedConvs,
  });

  console.log(`\n🎯 XP 恢復結果：`);
  console.log(`   補充 XP  : +${result.gained}`);
  console.log(`   當前 XP  : ${result.xp}`);
  console.log(`   當前等級 : Lv.${result.level}`);
  if (result.leveled) {
    console.log(`   🎉 升級了！`);
  }

  // ── 4. 更新 dailyXpStart = 恢復後的當前 XP ───────────────────
  // run() 已 writeFileSync，重新讀取並追加字段
  const charAfter        = JSON.parse(readFileSync(CHARACTER_FILE, 'utf8'));
  charAfter.dailyXpStart = charAfter.xp;
  charAfter.updatedAt    = new Date().toISOString();
  writeFileSync(CHARACTER_FILE, JSON.stringify(charAfter, null, 2), 'utf8');

  console.log(`\n📌 dailyXpStart 已更新為 ${charAfter.xp}`);
  console.log(`✅ XP 恢復完成`);
}

main().catch(e => {
  console.error('❌ sync-xp-recovery 失敗:', e.message);
  process.exit(1);
});
