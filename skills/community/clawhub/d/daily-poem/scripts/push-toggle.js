#!/usr/bin/env node
/**
 * daily-poem — push-toggle.js
 * 管理 openclaw cron 定时推送开关
 *
 * 用法:
 *   node scripts/push-toggle.js on
 *   node scripts/push-toggle.js off
 *   node scripts/push-toggle.js status
 */

const path = require('path');

const args = process.argv.slice(2);
const action = args[0];

if (!action || !['on', 'off', 'status'].includes(action)) {
  console.error('Usage: node scripts/push-toggle.js on|off|status');
  process.exit(1);
}

const skillDir = path.join(__dirname, '..');
const morningCmd = `cd ${skillDir} && node scripts/morning-push.js`;
const weeklyCmd  = `cd ${skillDir} && node scripts/weekly-digest.js`;

if (action === 'on') {
  console.log(`
开启每日诗词推送，请在终端运行以下命令：

  openclaw cron add "0 8 * * *"  "${morningCmd}"
  openclaw cron add "0 20 * * 0" "${weeklyCmd}"

这将设置：
  • 每日 08:00 推送一首精选诗词
  • 每周日 20:00 推送本周诗词合辑

添加后验证：
  openclaw cron list

关闭推送：
  node scripts/push-toggle.js off
`);
} else if (action === 'off') {
  console.log(`
关闭每日诗词推送，请运行：

  openclaw cron list

找到含 "daily-poem" 的任务并记录 ID，然后：

  openclaw cron delete <morning-task-id>
  openclaw cron delete <weekly-task-id>
`);
} else if (action === 'status') {
  console.log(`
查看每日诗词推送状态：

  openclaw cron list

查找包含以下内容的条目：
  时间：0 8 * * *（每日早晨）→ morning-push.js
  时间：0 20 * * 0（每周日晚）→ weekly-digest.js

有记录 → 推送已开启 ✅
无记录 → 推送未开启（运行：node scripts/push-toggle.js on）
`);
}
