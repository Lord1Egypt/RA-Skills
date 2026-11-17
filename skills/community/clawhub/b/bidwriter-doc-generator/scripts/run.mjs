#!/usr/bin/env node
/**
 * run.mjs —— 投标文件生成官（免费版）
 *
 * **完全本地运行**：引擎已打包在本技能内（engine/ 目录），
 * 不联网、不需要 API Key、不上传任何材料。项目资料不出本机。
 *
 * 免费版与完整版的差别**写在代码里**，不是写在文档里：
 *   - 免费版：全册目录（分册/章节/要点/字数建议）+ 逐条响应表的**结论列**（前 5 条）
 *   - 完整版：全部条款 + 逐条依据 + 应答话术 + 否决条款专项自查表
 *             + 材料清单盖章要求 + 废标雷区库 + 材料完整度评分与补全建议
 *
 * 用法：
 *   node scripts/run.mjs --sample
 *   node scripts/run.mjs --input my-project.json
 *   node scripts/run.mjs --input my-project.json --json
 */

import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const require = createRequire(import.meta.url);
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ENG = require(path.join(HERE, 'engine', 'bid-doc.js'));

const FREE_CLAUSE_LIMIT = 5;

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

const USAGE = `投标文件生成官（免费版）—— 本地离线运行

  **完全本地**：引擎在本技能内，不联网、不需要 API Key。项目资料不出本机。

用法：
  node scripts/run.mjs --sample
  node scripts/run.mjs --input my-project.json
  node scripts/run.mjs --input my-project.json --json

入参 JSON 字段：
  projectName    必填，项目名称
  bidder         必填，投标人名称
  projectNo      选填，项目编号
  tenderer       选填，招标人
  bidType        选填，goods(货物) | works(工程) | service(服务) | gov-procurement(政府采购)
  price          选填，投标报价（数字或含千分位字符串）
  qualification  选填，资质清单，如 ["建筑工程施工总承包二级", "安全生产许可证"]
  performance    选填，业绩清单，字符串或 {"name":"...","amount":"...","year":"..."}
  deliverables   选填，招标文件要求提交的材料清单
  clauses        选填，招标文件关键条款，字符串或 {"no":"1.1","text":"...","type":"reject|qualification|commercial|technical"}
  rejectClauses  选填，否决投标条款清单（单独成表时用）

参数：
  -i, --input    入参 JSON 文件路径
      --sample   使用内置样例
      --json     以 JSON 输出（免费版字段同样受限）
  -h, --help     显示本帮助

退出码：
  0 正常  1 缺少入参  2 执行失败  3 材料不足（会说明缺什么）
`;

function freeView(r) {
  const all = r.responses || [];
  const shown = all.slice(0, FREE_CLAUSE_LIMIT).map((x) => ({
    no: x.no,
    type: x.type,
    verdict: x.verdict,
    basis: '🔒',
    talkTrack: '🔒',
  }));
  return {
    tier: 'free',
    ok: true,
    meta: r.meta,
    summary: {
      volumes: r.summary.volumes,
      chapters: r.summary.chapters,
      wordTotal: r.summary.wordTotal,
      clauses: r.summary.clauses,
    },
    volumes: r.volumes,
    responses: shown,
    responsesTotal: all.length,
    locked: {
      clauseDetail: all.length,
      rejectRows: (r.rejectRows || []).length,
      materials: (r.materials.required || []).length,
      landmines: (r.landmines || []).length,
      score: r.summary.score,
      gaps: (r.summary.gaps || []).length,
    },
  };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help) { console.log(USAGE); return 0; }

  let payload = null, origin = '';
  if (args.input) {
    payload = JSON.parse(fs.readFileSync(args.input, 'utf8'));
    origin = `--input ${path.basename(args.input)}`;
  } else if (args.sample) {
    payload = JSON.parse(fs.readFileSync(path.join(HERE, '..', 'templates', 'sample.json'), 'utf8'));
    origin = '--sample';
  } else {
    console.error('缺少入参。用 --input 指定 JSON 文件，或用 --sample 自检。');
    console.error(''); console.error(USAGE);
    return 1;
  }

  let r;
  try {
    r = ENG.generate(payload);
  } catch (e) {
    console.error(`执行失败：${e.message}`);
    return 2;
  }

  // 材料不足：明确说缺什么，绝不产出"看起来完整"的空壳
  if (!r.ok) {
    if (args.json) { console.log(JSON.stringify(r, null, 2)); return r.code; }
    console.error('无法生成投标文件骨架：' + r.reason);
    console.error('  ' + r.message);
    console.error('');
    console.error('  缺少：' + (r.detail.missing || []).join('、'));
    console.error('  至少需要：' + r.detail.need);
    return r.code;
  }

  const view = freeView(r);
  if (args.json) { console.log(JSON.stringify(view, null, 2)); return 0; }

  const m = r.meta, s = r.summary;
  console.log('投标文件生成官 · 免费版 —— 全册骨架已生成（本地运行，未联网）');
  console.log(`  来源：${origin}`);
  console.log(`  项目：${m.projectName}${m.projectNo ? '（编号 ' + m.projectNo + '）' : ''}`);
  console.log(`  招标人：${m.tenderer || '（未填写）'}　投标人：${m.bidder}`);
  console.log(`  类型：${m.bidType}${m.bidTypeInferred ? '（未指定，按货物类默认）' : ''}`
    + (m.price ? `　报价：${m.price}` : '　报价：（未填写）'));
  console.log(`  规模：${s.volumes} 册 / ${s.chapters} 章 / 建议总字数约 ${s.wordTotal} 字`);
  console.log('');

  console.log('— 投标文件全册目录 —');
  for (const v of r.volumes) {
    console.log(`  【${v.name}】${v.purpose}`);
    for (const c of v.chapters) {
      console.log(`    · ${c.name}（建议 ${c.words} 字）`);
      console.log(`        要点：${c.points.join('；')}`);
    }
    console.log('');
  }

  console.log(`— 逐条响应表（免费版只显示前 ${FREE_CLAUSE_LIMIT} 条的结论）—`);
  if (!s.clauses) {
    console.log('  未提供招标文件条款（clauses）。');
    console.log('  提示：把招标文件里"投标人须知"与"评标办法"的条款贴进 clauses，才能生成响应表。');
  }
  for (const x of view.responses) {
    console.log(`  [${x.verdict}] ${x.no}（${x.type}）`);
    console.log('      依据：🔒 完整版说明条款命中了你的哪项资质/业绩');
    console.log('      话术：🔒 完整版给出可直接写进投标文件的应答口径');
  }
  console.log('');
  if (s.clauses) {
    console.log(`  响应结论汇总：可响应 ${s.responded} 条 / 需补充 ${s.toSupplement} 条 / 待确认 ${s.toConfirm} 条`);
    console.log(`  其中否决投标条款：${s.rejectClauses} 条 ← 这些条款不响应就是废标`);
    console.log('');
  }

  const rest = Math.max(0, view.responsesTotal - FREE_CLAUSE_LIMIT);
  console.log('— 免费版到此为止 —');
  console.log(`  另有 ${rest} 条条款的结论与全部依据未展示。`);
  console.log(`  另有「否决投标条款专项自查表」（${view.locked.rejectRows} 条）未展示。`);
  console.log(`  另有「材料清单与盖章要求」（${view.locked.materials} 项）未展示。`);
  console.log(`  另有「废标雷区库」（${view.locked.landmines} 条）未展示。`);
  console.log(`  另有「材料完整度评分」（当前 ${view.locked.score}/100，缺 ${view.locked.gaps} 项）未展示。`);
  console.log('  完整版：全部条款依据与应答话术 + 否决条款自查表 + 材料盖章要求 + 废标雷区 + 补全建议。');
  console.log('');
  console.log('（本工具完全本地运行，项目资料不会离开你的机器。）');
  return 0;
}

process.exit(main());
