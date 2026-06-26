#!/usr/bin/env node
/**
 * Automatic Skill — Push Toggle (推送开关)
 * 管理 openclaw cron 定时任务（每日 02:00 自动运行流水线）。
 *
 * 用法:
 *   node scripts/push-toggle.js on             # 开启每日自动运行
 *   node scripts/push-toggle.js on --dry-run   # 开启（dry-run 模式，不上传）
 *   node scripts/push-toggle.js off            # 关闭
 *   node scripts/push-toggle.js status         # 查看当前状态
 */

const fs = require('fs');
const path = require('path');

const args = process.argv.slice(2);
const action = args[0];
const dryRun = args.includes('--dry-run');
const scriptDir = path.join(__dirname);

const VALID_ACTIONS = ['on', 'off', 'status'];
if (!action || !VALID_ACTIONS.includes(action)) {
  console.error('Usage: node scripts/push-toggle.js on|off|status [--dry-run]');
  process.exit(1);
}

const cronCmd = `cd ${path.join(scriptDir, '..')} && node scripts/daily-pipeline.js${dryRun ? ' --dry-run' : ''}`;
const cronSchedule = '0 2 * * *';

if (action === 'on') {
  console.log(`
To enable automatic daily skill generation, run this command in your terminal:

  openclaw cron add "${cronSchedule}" "${cronCmd}"

This will schedule the pipeline to run every day at 02:00.
${dryRun ? 'DRY-RUN mode is enabled — stages 7-9 (upload) will be skipped.' : ''}

After adding, verify with:
  openclaw cron list

To disable later:
  node scripts/push-toggle.js off
`);
} else if (action === 'off') {
  console.log(`
To disable automatic daily skill generation, run:

  openclaw cron list

Find the cron job with the command containing "automatic-skill" and note its ID, then:

  openclaw cron delete <task-id>

Or to delete all automatic-skill cron jobs at once (if supported):
  openclaw cron list | grep automatic-skill | awk '{print $1}' | xargs -I{} openclaw cron delete {}
`);
} else if (action === 'status') {
  console.log(`
To check if the automatic daily pipeline cron job is active:

  openclaw cron list

Look for an entry with:
  Schedule: ${cronSchedule}  (02:00 every day)
  Command:  ...automatic-skill...

If found → pipeline is ACTIVE
If not found → pipeline is INACTIVE (run: node scripts/push-toggle.js on)
`);
}
