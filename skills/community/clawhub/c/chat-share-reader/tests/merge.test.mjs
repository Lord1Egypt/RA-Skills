// 分片合并的回归测试。
//
// Codex 的 fork 会把一条线程写成多个 rollout 文件，文件名换新 id、session_meta
// 里还留着父线程 id。合并错了的表现是：对话顺序乱、同一句话出现两遍。
// 这两件事都不会报错，只能靠测试挡。

import test from 'node:test';
import assert from 'node:assert/strict';
import { dedupeShards, expandShards, stitchMessages } from '../scripts/lib/merge.mjs';

const sid = '01a1af92-aaaa-bbbb-cccc-000000000001';

const shard = (name, time) => ({ name: 'codex', source: 'codex', file: `/s/${name}`, ref: `/s/${name}`, time });

test('dedupeShards 按文件去重并保持时间升序', () => {
  const a = shard('a', 300);
  const b = shard('b', 100);
  const out = dedupeShards([a, b, { ...a }]);
  assert.deepEqual(out.map((x) => x.file), ['/s/b', '/s/a']);
});

test('dedupeShards 对 ref 型条目按 ref 去重', () => {
  const x = { name: 'chatgpt', ref: 'https://x/1' };
  const out = dedupeShards([x, { ...x }]);
  assert.equal(out.length, 1);
});

test('expandShards 文件名带父线程 id 时按路径收齐，不读文件头', async () => {
  const seed = shard(`rollout-${sid}.jsonl`, 100);
  const sib = shard(`rollout-${sid}-2.jsonl`, 200);
  const other = shard('rollout-unrelated.jsonl', 300);
  const items = [seed, sib, other];

  let reads = 0;
  const idOf = async () => {
    reads++;
    return sid;
  };

  const out = await expandShards([seed], items, idOf);
  assert.deepEqual(out.map((x) => x.file).sort(), [seed.file, sib.file].sort());
  assert.equal(reads, 1, '只该读种子一次');
});

test('expandShards 分片改名时回落到读 session_meta', async () => {
  const seed = shard('rollout-seed.jsonl', 100);
  const renamed = shard('rollout-renamed.jsonl', 200);
  const items = [seed, renamed];

  const idOf = async (f) => (String(f).includes('seed') || String(f).includes('renamed') ? sid : '');
  const out = await expandShards([seed], items, idOf);
  assert.equal(out.length, 2);
});

test('expandShards 不跨来源合并', async () => {
  const seed = shard('a.jsonl', 100);
  const alien = { name: 'claude', source: 'claude', file: `/s/${sid}.jsonl`, ref: '', time: 200 };
  const out = await expandShards([seed], [seed, alien], async () => sid);
  assert.deepEqual(out.map((x) => x.file), [seed.file]);
});

test('expandShards 读不出种子 id 时原样返回', async () => {
  const seed = shard('a.jsonl', 100);
  const sib = shard('b.jsonl', 200);
  const out = await expandShards([seed], [seed, sib], async () => '');
  assert.deepEqual(out.map((x) => x.file), [seed.file]);
});

test('stitchMessages 去掉分片间重复的历史', () => {
  const parts = [
    { messages: [{ role: '用户', body: '问题', at: '2026-11-13T01:00:00Z' }] },
    {
      messages: [
        { role: '用户', body: '问题', at: '2026-11-13T01:00:00Z' },
        { role: '模型', body: '回答', at: '2026-11-13T01:00:05Z' },
      ],
    },
  ];
  const { messages } = stitchMessages(parts);
  assert.equal(messages.length, 2);
  assert.deepEqual(messages.map((m) => m.role), ['用户', '模型']);
});

test('stitchMessages 按消息时间排序，不按分片顺序', () => {
  const parts = [
    { messages: [{ role: '模型', body: '后', at: '2026-11-13T02:00:00Z' }] },
    { messages: [{ role: '用户', body: '先', at: '2026-11-13T01:00:00Z' }] },
  ];
  assert.deepEqual(stitchMessages(parts).messages.map((m) => m.body), ['先', '后']);
});

test('stitchMessages 让无时间的工具消息跟随上一条', () => {
  const parts = [
    {
      messages: [
        { role: '用户', body: 'q1', at: '2026-11-13T01:00:00Z' },
        { role: '工具', body: 'out1' },
        { role: '模型', body: 'a1', at: '2026-11-13T01:00:09Z' },
      ],
    },
  ];
  assert.deepEqual(stitchMessages(parts).messages.map((m) => m.body), ['q1', 'out1', 'a1']);
});

test('stitchMessages 保留第一个非空的 note', () => {
  const { note } = stitchMessages([
    { note: '', messages: [] },
    { note: '截断到 20 条', messages: [] },
    { note: '别的说明', messages: [] },
  ]);
  assert.equal(note, '截断到 20 条');
});

test('stitchMessages 只对前 300 字相同、角色不同的消息分开算', () => {
  const body = 'x'.repeat(400);
  const parts = [
    { messages: [{ role: '用户', body, at: '2026-11-13T01:00:00Z' }] },
    { messages: [{ role: '模型', body, at: '2026-11-13T01:00:01Z' }] },
  ];
  assert.equal(stitchMessages(parts).messages.length, 2);
});
