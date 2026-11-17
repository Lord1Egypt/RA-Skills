#!/usr/bin/env node
/**
 * run.mjs —— 成本与存货技能包（免费版）
 *
 * 全部检查都在**本机**完成：调用同目录下的 engine/cost-inventory-pack.js（纯 Node 标准库实现）。
 * 那个引擎内部装的是仓库里**已有的 14 个成本/存货检查引擎**（逐字节拷贝，规则一行没改），
 * 本包只做"客户目录 → 逐客户跑 14 项检查 → 每个客户一行结论"这件编排工作。
 *
 * 刻意不做的事：
 *   · 不实现本版本范围之外的检查项（它们只能是未执行，绝不会被伪造出来）；
 *   · 材料不足时**不给结论**：打印缺什么并以退出码 3 结束；
 *   · **不写任何材料文件**：结果只打到 stdout（材料不出本机）。
 *
 * 用法：
 *   node scripts/run.mjs --sample                  # 单客户样例（内置，14 项检查全跑）
 *   node scripts/run.mjs --sample-batch            # 3 个客户的批量样例（干净 / 有硬伤 / 未交材料）
 *   node scripts/run.mjs --input 客户目录           # 批量：每个子目录 = 一个客户/一套底稿
 *   node scripts/run.mjs --input 单客户底稿.json    # 单客户：JSON 或纯文本
 *   node scripts/run.mjs --input 客户目录 --json    # 机器可读
 *
 * 客户目录怎么放（每个子目录里放该客户的一套成本存货底稿，每张表用 `=== 检查名 ===` 分段，Tab 分隔最稳）：
 *   客户目录/
 *     豫州精工制造有限公司/成本存货底稿.txt
 *     中岳食品加工有限公司/成本存货底稿.txt
 *     （目录里没有子目录时，直接把每个文件当一个客户）
 *   也可以把 14 张表拆成 14 个文件放进同一个子目录 —— 引擎会自己认表头找对应的那一项。
 *
 * 退出码：
 *   0  已执行检查（结果里有问题项或没有问题项都算执行成功）
 *   1  没给入参
 *   3  材料不足（一个客户的材料都没有 / 空 / 只有空白 / 认不出任何一张表）—— 此时不给任何结论
 *   4  入参文件或目录读不到 / 内容无法解析
 *   9  未预期错误
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const require = createRequire(import.meta.url);
const ENGINE = require(path.join(HERE, 'engine', 'cost-inventory-pack.js'));

const CAPABILITY = '成本与存货技能包（免费版）';

const NOTE = '本次按客户逐个跑全部 14 个成本与存货检查项，核对全部在本机完成；'
  + '未执行的检查项已如实列出，不会用默认值编造结论。';

const TEXT_EXT = new Set(['.txt', '.tsv', '.csv', '.md', '.text', '.tab', '.log', '.dat', '.json']);

const SAMPLE = { text: ENGINE.SAMPLE_TEXT, object_name: '样例客户（单客户模式）' };
const SAMPLE_BATCH = { objects: ENGINE.SAMPLE_OBJECTS };

const USAGE = `成本与存货技能包（免费版） —— 本机执行的AI核对

  检查项（每个客户都跑这几项）：${ENGINE.CHECKS_GIVEN.join('、')}
  本版本不包含：${ENGINE.CHECKS_WITHHELD.join('、')}

用法：
  node scripts/run.mjs --sample                   单客户样例（内置）
  node scripts/run.mjs --sample-batch             3 个客户的批量样例
  node scripts/run.mjs --input 客户目录            批量：每个子目录 = 一个客户
  node scripts/run.mjs --input 底稿.json           单客户：JSON 或纯文本

入参写法：
  · 批量（推荐）：--input 指向一个目录，里面每个子目录就是一个客户，子目录里放该客户的一套成本存货底稿
  · 单客户：{"text":"（把该客户的表按 === 检查名 === 分段贴进来，Tab 分隔最稳）"}

参数：
  -i, --input        入参 JSON 文件、纯文本文件，或**客户目录**
      --sample       使用内置单客户样例
      --sample-batch 使用内置批量样例（3 个客户）
      --json         以 JSON 输出（默认给人看）
  -h, --help         显示本帮助

退出码：0 已执行检查 / 1 缺少入参 / 3 材料不足 / 4 入参读不到或无法解析 / 9 未预期错误
`;

function parseArgs(argv) {
  const out = { input: '', sample: false, sampleBatch: false, json: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--input' || a === '-i') out.input = argv[++i] || '';
    else if (a === '--sample') out.sample = true;
    else if (a === '--sample-batch') out.sampleBatch = true;
    else if (a === '--json') out.json = true;
    else if (a === '--help' || a === '-h') out.help = true;
  }
  return out;
}

function isTextName(name) {
  const ext = path.extname(name).toLowerCase();
  return ext === '' || TEXT_EXT.has(ext);
}

function readText(file) {
  try {
    return fs.readFileSync(file, 'utf8').replace(/^\uFEFF/, '');
  } catch (e) {
    return null;
  }
}

function readObjectFile(file, name) {
  const raw = readText(file);
  if (raw === null) return null;
  if (path.extname(name).toLowerCase() === '.json') {
    try {
      const j = JSON.parse(raw);
      if (j && typeof j.text === 'string') return { name, text: j.text };
      if (j && (typeof j.objects === 'object' || typeof j.content === 'string')) {
        return { name, text: raw };
      }
    } catch (e) { /* 不是 JSON 就按纯文本用 */ }
  }
  return { name, text: raw };
}

function listDir(dir) {
  try {
    return fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => (a.name < b.name ? -1 : 1));
  } catch (e) {
    return null;
  }
}

/** `--input <dir>`：每个子目录 = 一个客户；没有子目录时每个文件 = 一个客户。 */
function loadDir(dir) {
  const entries = listDir(dir);
  if (!entries) return { error: `读不到客户目录：${dir}` };
  const subdirs = entries.filter((e) => e.isDirectory());
  const objects = [];
  if (subdirs.length) {
    for (const d of subdirs) {
      const dp = path.join(dir, d.name);
      const files = [];
      for (const f of (listDir(dp) || [])) {
        if (!f.isFile() || !isTextName(f.name)) continue;
        const got = readObjectFile(path.join(dp, f.name), f.name);
        if (got) files.push(got);
      }
      objects.push({ name: d.name, files });
    }
  } else {
    for (const f of entries) {
      if (!f.isFile() || !isTextName(f.name)) continue;
      const got = readObjectFile(path.join(dir, f.name), f.name);
      if (got) objects.push({ name: path.basename(f.name, path.extname(f.name)), files: [got] });
    }
  }
  return {
    payload: { objects },
    note: `目录 ${dir}：按${subdirs.length ? '子目录' : '文件'}识别到 ${objects.length} 个客户`,
  };
}

/** 读入参文件：合法 JSON 就按其结构走；不是 JSON 就当作纯文本材料 */
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
  if (trimmed.length > 4 * 1024 * 1024) {
    return { error: `入参文件过大（${trimmed.length} 字符）：超过 4M 上限，无法解析。` };
  }
  try {
    return { payload: JSON.parse(trimmed) };
  } catch (e) {
    if (e instanceof RangeError) {
      return { error: `入参 JSON 嵌套过深，无法解析（${e.message}）。` };
    }
    return { payload: { text: stripped }, note: '入参文件不是合法 JSON，已按纯文本材料处理' };
  }
}

/** 材料不足：说清楚缺什么，并且明确不给结论 */
function reportInsufficient(args, outcome, loaded) {
  const missing = (outcome && outcome.missing) || ['入参无法解析成可核对的客户材料'];
  const advice = (outcome && outcome.advice)
    || '请用 --input 指向客户目录（每个子目录 = 一个客户），或先用 --sample / --sample-batch 看看需要什么格式。';

  const view = {
    ok: false,
    tier: 'free',
    capability: CAPABILITY,
    checks_given: ENGINE.CHECKS_GIVEN,
    checks_withheld: ENGINE.CHECKS_WITHHELD,
    omitted_findings: 0,
    note: '材料不足，本次没有执行任何检查，因此不出结论：既不做"一致"的认定，也不做"不一致"的认定，'
      + '更不会给出任何结论。',
    result: {
      status: 'insufficient_input',
      missing: missing,
      advice: advice,
      executed_checks: 0,
      executed_locally: true,
      network_used: false,
      wrote_files: false,
    },
  };

  if (args.json) {
    console.log(JSON.stringify(view, null, 2));
    return 3;
  }

  console.log('材料不足，本次没有执行任何检查，因此不出结论。');
  console.log('（检查项依赖你提供的客户材料：一个客户的材料都没有、或认不出任何一张表时不做任何认定，也不套用默认值。）');
  if (loaded && loaded.note) console.log(`（${loaded.note}）`);
  console.log('');
  console.log('缺少的内容：');
  for (const m of missing) console.log(`  - ${m}`);
  console.log('');
  console.log(`怎么补：${advice}`);
  return 3;
}

/** 每个客户一行的结论：客户名 / 各项通过或有问题 / 材料不足标「未执行」 */
function objectLine(o) {
  const checks = o.checks
    .map((c) => `${c.check}:${c.status === 'ok' ? (c.findings ? `有问题(${c.findings})` : '通过') : '未执行'}`)
    .join('  ');
  return `  [${o.verdict}] ${o.object}｜问题 ${o.total} 项（P0 ${o.p0} / P1 ${o.p1} / P2 ${o.p2}）｜${checks}`;
}

function reportResult(view) {
  const r = view.result;
  console.log('免费AI核对完成（批量壳：一次跑完所有客户）');
  console.log(`本次执行的检查项（${view.checks_given.length} 个成本与存货检查项）：${view.checks_given.join('、')}`);
  if (view.checks_withheld.length) console.log(`本版本不包含：${view.checks_withheld.join('、')}`);
  console.log(`成员检查包自身未实现的检查项 ${(r.scope.sub_checks_not_run || []).length} 项已如实列出（见结果 scope.sub_checks_not_run）。`);
  console.log('执行方式：核对在本机用 Node 标准库完成，不发送你的材料、没有次数上限');
  console.log('');
  console.log(`客户数 ${r.summary.objects}｜有问题 ${r.summary.objects_with_issues}｜干净 ${r.summary.objects_clean}｜未执行（没交材料）${r.summary.objects_not_run}`);
  console.log('');
  console.log('客户 × 结论（每个客户一行）');
  for (const o of r.objects) console.log(objectLine(o));
  if (r.findings.length) {
    console.log('');
    console.log(`问题明细（共 ${r.findings.length} 条，带客户 + 原文文件与行号）`);
    for (const f of r.findings.slice(0, 40)) {
      console.log(`  · [${f.level}] ${f.object}｜${f.check}｜${f.evidence}｜${f.category}：${f.message}`);
    }
    if (r.findings.length > 40) console.log(`  （还有 ${r.findings.length - 40} 条，见下面的 JSON 或 --json 输出）`);
  }
  console.log('');
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { console.log(USAGE); return 0; }

  let payload = null;
  let loaded = null;
  if (args.input) {
    let st = null;
    try {
      st = fs.statSync(args.input);
    } catch (e) {
      console.error(`读不到入参路径：${args.input}（${e.code || e.message}）`);
      return 4;
    }
    if (st.isDirectory()) {
      loaded = loadDir(args.input);
      if (loaded.error) { console.error(loaded.error); return 4; }
      payload = loaded.payload;
    } else {
      loaded = loadInput(args.input);
      if (loaded.error) { console.error(loaded.error); return 4; }
      payload = loaded.payload;
    }
  } else if (args.sampleBatch) {
    payload = SAMPLE_BATCH;
  } else if (args.sample) {
    payload = SAMPLE;
  } else {
    console.error('缺少入参。用 --input 指向客户目录或底稿文件，或用 --sample / --sample-batch 自检。');
    console.error('');
    console.error(USAGE);
    return 1;
  }

  let outcome;
  try {
    outcome = ENGINE.run(payload);
  } catch (e) {
    console.error(`引擎执行出错：${e && e.message ? e.message : e}`);
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

  reportResult(view);
  if (loaded && loaded.note) console.log(`（${loaded.note}）`);
  console.log(JSON.stringify(view.result, null, 2));
  console.log('');
}

try {
  process.exit(main());
} catch (e) {
  console.error(`未预期的错误：${e && e.message ? e.message : e}`);
  process.exit(9);
}
