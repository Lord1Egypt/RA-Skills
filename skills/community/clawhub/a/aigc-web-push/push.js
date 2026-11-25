#!/usr/bin/env node
/**
 * 统一推送入口：公众号 | 云电脑
 *
 *   node push.js wechat <appId|-> html <file.html> [sendMode]
 *   node push.js wechat <appId|-> img '<urlsJSON>' <title> <description> [sendMode]
 *   node push.js cloud <instanceId|-> html <file.html> [categoryId] [publishMode] [targetScope] [idsOrNamesCSV]
 *   node push.js cloud <instanceId|-> img '<urls|本地|JSON>' <title> [description|content.html] [publishMode] [targetScope] [idsOrNamesCSV]
 *   node push.js cloud <instanceId|-> video '<url|本地|JSON>' <title> [description] [publishMode] [targetScope] [idsOrNamesCSV]
 *   node push.js cloud <instanceId|-> list-targets [categoryId]
 *   node push.js cloud <instanceId|-> resolve <categoryId> <名称> [prefer]
 */

const { spawnSync } = require('child_process');
const path = require('path');
const { ensureUpToDate } = require('./check-update');

const channel = String(process.argv[2] || '').toLowerCase();
const rest = process.argv.slice(3);
const dir = __dirname;

if (channel !== 'wechat' && channel !== 'cloud') {
  console.error(`用法:
  node push.js wechat <appId|-> html <file.html> [sendMode]
  node push.js wechat <appId|-> img '<urlsJSON>' <title> <description> [sendMode]
  node push.js cloud  <instanceId|-> html <file.html> [categoryId] [publishMode] [targetScope] [idsOrNamesCSV]
  node push.js cloud  <instanceId|-> img '<urls|本地|JSON>' <title> [description|content.html] [publishMode] [targetScope] [idsOrNamesCSV]
  node push.js cloud  <instanceId|-> video '<url|本地|JSON>' <title> [description] [publishMode] [targetScope] [idsOrNamesCSV]
  node push.js cloud  <instanceId|-> list-targets [categoryId]
  node push.js cloud  <instanceId|-> resolve <categoryId> <名称> [prefer]`);
  process.exit(1);
}

async function main() {
  const check = await ensureUpToDate({ dir });
  if (check && check.outdated) {
    // 退出码 2：有新版本，等 Agent 问清用户是否升级后再推
    process.exit(2);
  }

  const script =
    channel === 'wechat'
      ? path.join(dir, 'push-to-wechat-mp.js')
      : path.join(dir, 'push-to-cloud.js');

  const r = spawnSync(process.execPath, [script, ...rest], {
    cwd: dir,
    stdio: 'inherit',
  });
  process.exit(r.status == null ? 1 : r.status);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
