#!/usr/bin/env node
import { execFileSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
function run(file, expectedCode, expectedText) {
  try {
    const output = execFileSync(process.execPath, ['scripts/check-draft.mjs', file], { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] });
    if (expectedCode !== 0 || !output.includes(expectedText)) throw new Error(`unexpected successful output: ${output}`);
  } catch (error) {
    const actual = error.status ?? 0;
    const text = `${error.stdout ?? ''}${error.stderr ?? ''}`;
    if (actual !== expectedCode || !text.includes(expectedText)) throw error;
  }
}
run('fixtures/success-complete.json', 0, 'ready-for-human-review');
run('fixtures/success-missing.json', 0, 'needs-completion');
run('fixtures/failure-owner-unconfirmed.json', 2, '账号或稿件归属未确认');
run('fixtures/failure-page-unconfirmed.json', 2, '当前页面不是可确认的投稿草稿页');
run('fixtures/failure-source-unbound.json', 2, '标题没有绑定可见来源');
run('fixtures/failure-assets-over-limit.json', 2, '素材与表格合计超过 100 行');
run('fixtures/failure-table-over-limit.json', 2, '素材与表格合计超过 100 行');
run('fixtures/failure-combined-over-limit.json', 2, '素材与表格合计超过 100 行');
run('fixtures/failure-empty-values.json', 0, 'needs-completion');
const checkJSON = file => JSON.parse(execFileSync(process.execPath, ['scripts/check-draft.mjs', file], { cwd: root, encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }));
const unknown = checkJSON('fixtures/failure-all-unconfirmed.json');
const expectedMissing = ['封面', '标题', '简介', '分区', '素材'];
if (unknown.status !== 'needs-completion' || JSON.stringify(unknown.missing) !== JSON.stringify(expectedMissing) || Object.keys(unknown.visible_fields).length || unknown.suggestions.some(x => x.field === '完整性')) throw new Error('全部未确认不能判定完整或进入人工复核');
const mixed = checkJSON('fixtures/success-unconfirmed-mixed.json');
if (mixed.status !== 'needs-completion' || mixed.visible_fields.title !== '真实可见标题' || JSON.stringify(mixed.missing) !== JSON.stringify(['封面', '简介', '分区', '素材'])) throw new Error('部分未确认必须逐项缺料，保留已见标题');
if (Object.keys(unknown.field_sources).length !== 5 || Object.keys(mixed.field_sources).length !== 5) throw new Error('未确认仍需保留每项可见来源');
console.log('self_test passed: 3 result fixtures and 6 safe-stop fixtures validated.');
console.log('PASS: all-unconfirmed and mixed-unconfirmed fields remain incomplete with sources; no browser was accessed.');
