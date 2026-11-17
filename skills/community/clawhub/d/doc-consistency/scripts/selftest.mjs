#!/usr/bin/env node
// Self-test: the fixtures have known planted errors. Every one must be caught,
// and nothing else may be reported. 规则一改就跑这个 —— 假阳性和漏报都会在这里现形。
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { readDoc } from './lib/read.mjs';
import { runRules, parseGlossary } from './lib/rules.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const ex = (n) => join(here, '..', 'examples', n);

let failed = 0;
function check(name, actual, expected) {
  const a = JSON.stringify(actual), e = JSON.stringify(expected);
  if (a === e) { console.log(`  ✓ ${name}`); return; }
  failed++;
  console.log(`  ✗ ${name}\n      expected ${e}\n      actual   ${a}`);
}

function types(findings) {
  const m = {};
  for (const f of findings) m[f.type] = (m[f.type] || 0) + 1;
  return Object.fromEntries(Object.entries(m).sort());
}

// ── 教材样例：12 处埋雷，一条不能少、一条不能多 ──────────────────────────────
console.log('sample-textbook.md');
{
  const { findings } = runRules([readDoc(ex('sample-textbook.md'))]);
  check('总条数', findings.length, 12);
  check('类型分布', types(findings), {
    交叉引用悬空: 2,
    占位符残留: 4,
    术语写法不一致: 1,
    疑似旧版年份: 1,
    章节引用悬空: 1,
    章节骨架缺项: 1,
    编号跳号: 1,
    编号重号: 1,
  });
  check('高危数', findings.filter((f) => f.severity === 'high').length, 8);
  check('每条都有英文文案', findings.every((f) => f.en && f.en.type && f.en.message), true);
  check('每条都能定位', findings.every((f) => f.file && f.loc), true);
}

// ── 英文标书样例 ─────────────────────────────────────────────────────────────
console.log('sample-proposal.md');
{
  const { findings } = runRules([readDoc(ex('sample-proposal.md'))]);
  const en = findings.map((f) => f.en.type).sort();
  check('抓到悬空引用', en.includes('Dangling cross-reference'), true);
  check('抓到悬空章节引用', en.includes('Dangling section reference'), true);
  check('抓到跳号', en.includes('Numbering gap'), true);
  check('抓到占位符', en.filter((t) => t === 'Leftover placeholder').length, 3);
  check('抓到术语不一致', en.includes('Inconsistent term spelling'), true);
  check('抓到骨架缺项', en.includes('Missing standard section'), true);
}

// ── 术语表 ───────────────────────────────────────────────────────────────────
console.log('glossary');
{
  const g = parseGlossary(ex('glossary.txt'));
  check('解析出条目', g.length > 0, true);
  const { findings } = runRules([readDoc(ex('sample-textbook.md'))], { glossary: g });
  check('触发违反术语表', findings.some((f) => f.type === '违反术语表'), true);
}

// ── 干净文档不该报任何东西 ───────────────────────────────────────────────────
console.log('clean.md');
{
  const { findings } = runRules([readDoc(ex('clean.md'))]);
  check('零误报', findings.map((f) => `${f.type}@${f.loc}`), []);
}

console.log(failed ? `\n✗ ${failed} 项未通过` : '\n✓ 全部通过');
process.exit(failed ? 1 : 0);
