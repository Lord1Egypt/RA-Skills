import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const packageJson = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
const manifest = fs.readFileSync(path.join(root, 'manifest.yaml'), 'utf8');
const skill = fs.readFileSync(path.join(root, 'SKILL.md'), 'utf8');
const readmeZh = fs.readFileSync(path.join(root, 'README.md'), 'utf8');
const readmeEn = fs.readFileSync(path.join(root, 'README.en.md'), 'utf8');
const success = JSON.parse(fs.readFileSync(path.join(root, 'fixtures/success.json'), 'utf8'));
const failure = JSON.parse(fs.readFileSync(path.join(root, 'fixtures/failure.json'), 'utf8'));

assert.match(manifest, new RegExp(`^name: ${packageJson.name}$`, 'm'));
assert.match(manifest, new RegExp(`^version: ${packageJson.version.replaceAll('.', '\\.')}$`, 'm'));
assert.equal(success.room_url, 'https://live.douyin.com/example');
assert.ok(Array.isArray(success.snapshots) && success.snapshots.length > 0);
for (const snapshot of success.snapshots) {
  assert.equal(snapshot.room_url, success.room_url);
  assert.ok(['started', 'still_live', 'ended', 'unavailable'].includes(snapshot.status));
  assert.equal(typeof snapshot.creator_name, 'string');
  assert.equal(typeof snapshot.title, 'string');
  assert.ok(snapshot.visible_metrics && typeof snapshot.visible_metrics === 'object');
  assert.ok(Number.isFinite(Date.parse(snapshot.collected_at)));
}
assert.equal(failure.status, 'needs_user_action');
assert.equal(typeof failure.reason, 'string');
assert.match(failure.url, /^https:\/\/live\.douyin\.com\//);

for (const [name, text] of [['SKILL.md', skill], ['README.md', readmeZh], ['README.en.md', readmeEn]]) {
  assert.match(text, /browserId/);
  assert.match(text, /后台监控|background monitor/i, `${name} must state the background monitoring limit`);
  assert.match(text, /通知|notification/i, `${name} must state the notification limit`);
}
assert.match(skill, /未指定且恰好只有一个在线环境，可使用该环境/);
assert.match(skill, /绝不改用其他账号或环境/);
assert.match(skill, /未给持续时间时只做一次快照/);
assert.match(skill, /不得导出 Cookie/);
assert.match(skill, /用户指定显示名或 `browserId` 时精确匹配/);
assert.match(skill, /仅当用户未指定且恰好只有一个环境在线时才自动使用/);
assert.match(skill, /多个在线环境且目标不明确时停止并请用户选择/);
for (const [name, text] of [['SKILL.md', skill], ['README.md', readmeZh], ['README.en.md', readmeEn]]) {
  assert.match(text, /github\.com\/aiispower\/easy-webbridge/, `${name} must use the verified primary repository`);
  assert.match(text, /gitee\.com\/xxjrq\/easy-webbridge/, `${name} must preserve the Gitee mirror`);
}

console.log('douyin-live-monitor-free contract self-test: ok');
