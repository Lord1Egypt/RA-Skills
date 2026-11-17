#!/usr/bin/env node
import fs from 'node:fs';
const args = process.argv.slice(2);
if (args.length !== 3 || args[2] !== '--confirm-reviewed') {
  console.error('Usage: node review-baseline.mjs <audit.json> <new-review.json> --confirm-reviewed\nOnly after human review; never records "fixed" or "verified". Refuses incomplete collection and overwrites.'); process.exit(1);
}
const die = msg => { console.error(`review-baseline: ${msg}`); process.exit(1); };
let report;
try { report = JSON.parse(fs.readFileSync(args[0], 'utf8')); }
catch (e) { die(`无法读取 ${args[0]}: ${e.message.split('\n')[0]}`); }
if (![2, 3].includes(report.schemaVersion) || !report.collectionComplete || report.mode !== 'online' || report.errors?.length || !Array.isArray(report.changes)) die('采集不完整/离线/格式不符，不得生成完整审阅基线');
const reviewedChangeIds = report.changes.map(c => `${c.framework}:${c.tag}`);
try {
  fs.writeFileSync(args[1], JSON.stringify({ schemaVersion: 3, project: report.project, reviewedAt: new Date().toISOString(), sourceCheckedAt: report.checkedAt,
    reviewedChangeIds, note: '仅确认已审阅这份报告中的 release；不表示已升级、已修复或通过验收。' }, null, 2) + '\n', { flag: 'wx' });
} catch (e) { die(`无法写入 ${args[1]}（已存在？）: ${e.message.split('\n')[0]}`); }
console.log(`Recorded ${reviewedChangeIds.length} reviewed release IDs; unresolved risk must remain in the project issue/decision log.`);
