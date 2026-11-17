#!/usr/bin/env node
/**
 * run.mjs —— 投标报价AI审查（免费）
 *
 * 全部检查都在**本机**完成：调用同目录下的 engine/quote-audit.js（纯 Node 标准库实现）。
 * 检查全部在**本机**完成（纯 Node 标准库），不读环境变量、不外发材料、不需要注册与 API Key。
 *
 * 刻意不做的事：
 *   · 不实现本版本范围之外的检查项（它们只能是未执行，绝不会被伪造出来）；
 *   · 材料不足时**不给结论**：打印缺什么并以退出码 3 结束。
 *
 * 用法：
 *   node scripts/run.mjs --sample
 *   node scripts/run.mjs --input my-input.json
 *   node scripts/run.mjs --input my-input.json --json
 *
 * 退出码：
 *   0  已执行检查（结果里有问题项或没有问题项都算执行成功）
 *   1  没给入参
 *   3  材料不足（空 / 只有空白 / 只有一个字符 / 解析不出任何明细行）—— 此时不给"没问题"的结论
 *   4  入参文件读不到
 *   9  未预期错误
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const ENGINE = require(path.join(HERE, 'engine', 'quote-audit.js'));

const CAPABILITY = '投标报价AI审查（免费）';

const NOTE = '本版本只执行上面列出的检查项，核对全部在本机完成；'
  + '未执行的检查项已如实列出，不会用默认值编造结论。';

const SAMPLE = {
  "text": "序号\t项目名称\t数量\t单价\t合价\n1\t土方开挖\t100\t25\t2500\n2\t混凝土浇筑\t50\t400\t19000\n3\t钢筋制安\t\t3800\t76000"
};

const USAGE = `投标报价AI审查（免费） —— 本机执行的AI核对

  检查项：${ENGINE.CHECKS_GIVEN.join('、')}
  本版本不包含：${ENGINE.CHECKS_WITHHELD.join('、')}

用法：
  node scripts/run.mjs --sample
  node scripts/run.mjs --input my-input.json

参数：
  -i, --input    入参 JSON 文件路径（也接受直接粘贴报价表的纯文本文件）
      --sample   使用内置样例
      --json     以 JSON 输出（默认给人看）
  -h, --help     显示本帮助

退出码：0 已执行检查 / 1 缺少入参 / 3 材料不足 / 4 入参文件读不到
`;

function parseArgs(argv) {
  const out = { input: '', sample: false, json: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--input' || a === '-i') out.input = argv[++i] || '';
    else if (a === '--sample') out.sample = true;
    else if (a === '--json') out.json = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

/** 读入参：合法 JSON 就按其结构走；不是 JSON 就当作纯文本材料（例如直接粘贴的报价表） */
function loadInput(file) {
  let raw;
  try {
    raw = fs.readFileSync(file, 'utf8');
  } catch (e) {
    return { error: `读不到入参文件：${file}（${e.code || e.message}）` };
  }
  const stripped = raw.replace(/^\uFEFF/, '');
  const trimmed = stripped.trim();
  if (!trimmed) return { payload: { text: '' }, note: '入参文件内容为空' };
  try {
    return { payload: JSON.parse(trimmed) };
  } catch {
    return { payload: { text: stripped }, note: '入参文件不是合法 JSON，已按纯文本报价材料处理' };
  }
}

/** 材料不足：说清楚缺什么，并且明确不给结论 */
function reportInsufficient(args, outcome, loaded) {
  const missing = (outcome && outcome.missing) || ['入参无法解析成可校验的材料'];
  const advice = (outcome && outcome.advice)
    || '请提供报价文本（text）或结构化明细（items），或先用 --sample 看看需要什么格式。';

  if (args.json) {
    console.log(JSON.stringify({
      ok: false,
      insufficient: true,
      tier: 'free',
      capability: CAPABILITY,
      checks_given: ENGINE.CHECKS_GIVEN,
      checks_withheld: ENGINE.CHECKS_WITHHELD,
      missing,
      advice,
      note: '材料不足，本次没有执行任何检查，因此不出结论：既不做"符合"的认定，也不做"不符合"的认定。',
    }, null, 2));
    return 3;
  }

  console.log('材料不足，本次没有执行任何检查，因此不出结论。');
  console.log('（检查项依赖你提供的字段：材料不足时不做任何认定，也不套用默认值。）');
  if (loaded && loaded.note) console.log(`（${loaded.note}）`);
  console.log('');
  console.log('缺少的内容：');
  for (const m of missing) console.log(`  - ${m}`);
  console.log('');
  console.log(`怎么补：${advice}`);
  return 3;
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { console.log(USAGE); return 0; }

  let payload = null;
  let loaded = null;
  if (args.input) {
    loaded = loadInput(args.input);
    if (loaded.error) { console.error(loaded.error); return 4; }
    payload = loaded.payload;
  } else if (args.sample) {
    payload = SAMPLE;
  } else {
    console.error('缺少入参。用 --input 指定 JSON 文件，或用 --sample 自检。');
    console.error('');
    console.error(USAGE);
    return 1;
  }

  let outcome;
  try {
    outcome = ENGINE.run(payload);
  } catch (e) {
    console.error(`引擎执行出错：${e.message}`);
    return 9;
  }

  if (!outcome || outcome.status !== 'success') {
    return reportInsufficient(args, outcome, loaded);
  }

  const view = {
    ok: true,
    tier: 'free',
    capability: CAPABILITY,
    checks_given: ENGINE.CHECKS_GIVEN,
    checks_withheld: ENGINE.CHECKS_WITHHELD,
    omitted_findings: (outcome.result.summary && outcome.result.summary.omitted) || 0,
    note: NOTE,
    result: outcome.result,
  };

  if (args.json) {
    console.log(JSON.stringify(view, null, 2));
    return 0;
  }

  console.log('免费AI核对完成');
  console.log(`本次执行的检查项：${view.checks_given.join('、') || '(无)'}`);
  if (view.checks_withheld.length) {
    console.log(`本版本不包含：${view.checks_withheld.join('、')}`);
  }
  console.log('执行方式：核对在本机用 Node 标准库完成，不发送你的材料、没有次数上限');
  if (loaded && loaded.note) console.log(`（${loaded.note}）`);
  console.log('');
  console.log(JSON.stringify(view.result, null, 2));
  console.log('');
}

try {
  process.exit(main());
} catch (e) {
  console.error(`未预期的错误：${e && e.message ? e.message : e}`);
  process.exit(9);
}
