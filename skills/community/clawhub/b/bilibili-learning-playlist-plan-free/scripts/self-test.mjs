#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const out = path.join(root, '.self-test-output.md');
for (const file of ['manifest.yaml', 'agents/openai.yaml']) {
  const metadata = fs.readFileSync(path.join(root, file), 'utf8');
  if (file === 'manifest.yaml' && !/^version: \d+\.\d+\.\d+$/m.test(metadata)) throw new Error('manifest 缺语义化版本');
  for (const field of ['display_name', 'short_description', 'default_prompt', 'icon_small', 'icon_large']) {
    const value = metadata.match(new RegExp(`^  ${field}: "([^"\\n]+)"$`, 'm'))?.[1];
    if (!value) throw new Error(`interface 字符串需加引号：${field}`);
    if (field === 'default_prompt' && !value.includes('$bilibili-learning-playlist-plan-free')) throw new Error('默认提示需显式调用本 Skill');
    if (field === 'short_description' && ([...value].length < 25 || [...value].length > 64)) throw new Error('短描述长度错误');
    if (field.startsWith('icon_')) {
      const target = path.resolve(root, value), relative = path.relative(root, target);
      if (relative.startsWith('..') || path.isAbsolute(relative) || !fs.existsSync(target)) throw new Error('图标必须存在于 Skill 包内');
    }
  }
}
try {
  if (fs.readFileSync(path.join(root, 'fixtures/failure-private-unauthorized.json'), 'utf8') !== fs.readFileSync(path.join(root, 'fixtures/private-unauthorized.json'), 'utf8')) throw new Error('失败输入包装副本必须保持原始资料');
  execFileSync(process.execPath, ['scripts/plan-from-visible.mjs', 'fixtures/visible-success.json', out], { cwd: root, stdio: 'pipe' });
  const result = fs.readFileSync(out, 'utf8');
  if (!result.includes('时长不可见') || !result.includes('可见资料草稿') || !result.includes('https://www.bilibili.com/video/BVdemo002?from=a\\|b')) throw new Error('成功样例输出缺少来源、未知时长或 Markdown 转义');
  if (!result.includes('20.50 分钟') || !result.includes('超过单日预算，未排期') || !result.includes('超出 2 天范围，未排期')) throw new Error('成功样例未覆盖时长换算、预算或学习天数约束');
  if (result !== fs.readFileSync(path.join(root, 'fixtures/success-output.md'), 'utf8')) throw new Error('公开成功输出与实际离线脚本不一致');
  if (fs.existsSync(out)) fs.unlinkSync(out);
  let unauthorizedError = '';
  try {
    execFileSync(process.execPath, ['scripts/plan-from-visible.mjs', 'fixtures/failure-private-unauthorized.json', out], { cwd: root, stdio: 'pipe' });
  } catch (error) {
    unauthorizedError = String(error.stderr ?? '');
  }
  if (!unauthorizedError.includes('私人收藏夹未授权：停止读取，未生成学习顺序或日程') || fs.existsSync(out)) {
    throw new Error('未授权失败样例必须报告未授权原因、停止且不生成排期');
  }
  execFileSync(process.execPath, ['scripts/plan-from-visible.mjs', 'fixtures/success-duration-exclusive.json', out], { cwd: root, stdio: 'pipe' });
  const exclusive = fs.readFileSync(out, 'utf8');
  if (!exclusive.includes('分钟单项') || !exclusive.includes('时钟单项') || (exclusive.match(/10 分钟/g) ?? []).length !== 2 || !exclusive.includes('| 2 | 1 |')) throw new Error('单一时长字段的正例换算或预算错误');
  if ((exclusive.match(/简介不可见/g) ?? []).length !== 2 || !exclusive.includes('未知 | 10 分钟') || !exclusive.includes('简介不可见')) throw new Error('简介缺失必须显示未知并列入缺项');
  for (const file of ['fixtures/failure-duration-equal.json', 'fixtures/failure-duration-conflicting.json', 'fixtures/failure-duration-null.json']) {
    if (fs.existsSync(out)) fs.unlinkSync(out);
    let rejected = false;
    try {
      execFileSync(process.execPath, ['scripts/plan-from-visible.mjs', file, out], { cwd: root, stdio: 'pipe' });
    } catch (error) {
      rejected = error.status !== 0 && String(error.stderr).includes('visibleMinutes 与 visibleDuration 只能二选一');
    }
    if (!rejected || fs.existsSync(out)) throw new Error('同时提供两个时长字段必须明确拒绝且不生成排期');
  }
  console.log('self-test passed: 离线可见资料规划器通过成功与失败样例。');
  console.log('PASS: minutes-only/clock-only inputs work; both duration fields reject equal, conflicting, and null values without generating a plan.');
} finally { if (fs.existsSync(out)) fs.unlinkSync(out); }
