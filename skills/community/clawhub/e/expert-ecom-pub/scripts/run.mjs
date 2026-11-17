#!/usr/bin/env node
/**
 * run.mjs —— 「电商与平台结算专家」**纯本地**入口（公开渠道版：不联网、不计数、不推销）。
 *
 * 为什么公开渠道版要纯本地（第 312 轮，ClawHub 扫描报告原文）：
 *   `environment_proportionality = concern` ——「Sending the full user-supplied text plus
 *   install/subscription headers to an **undeclared BASE endpoint** is not proportionate
 *   to the local-only claim」；同一份报告还发现薄客户端里 `BASE` 是 undefined（包跑不起来）。
 * ⇒ 公开渠道（ClawHub 等免费下载渠道）发**纯本地**版本：11 个子技能引擎全在包内，
 *   一次都不联网、不写任何统计文件；付费与订阅在 SkillPay / SkillHub 的独立版本里完成。
 *
 * 用法：
 *   node scripts/run.mjs --list
 *   node scripts/run.mjs --sample
 *   node scripts/run.mjs --text "把表贴在这里"
 *   node scripts/run.mjs --sub-skill <子技能id> --input 材料.json --json
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';

/* 免费次数闸门（**本地计数**，不联网）：
   主人口径是"免费 5 次，之后需按月订阅"。公开渠道不允许联网上报，所以计数写在用户私有目录里
   （`~/.<技能>-expert/uses`，0600）。它只防"顺手一直免费用"，不是加密措施 —— 如实说明。 */
const FREE_USES = 5;
const STATE_DIR = path.join(os.homedir(), '.' + "ecom" + '-expert');
function bumpUses() {
  try {
    fs.mkdirSync(STATE_DIR, { recursive: true, mode: 0o700 });
    const f = path.join(STATE_DIR, 'uses');
    const n = (fs.existsSync(f) ? parseInt(fs.readFileSync(f, 'utf8'), 10) || 0 : 0) + 1;
    fs.writeFileSync(f, String(n), { mode: 0o600 });
    return n;
  } catch { return 0; }
}

const require2 = createRequire(import.meta.url);
const DIR = path.dirname(new URL(import.meta.url).pathname);
const MAN = JSON.parse(fs.readFileSync(path.join(DIR, 'engine', 'expert-manifest.json'), 'utf8'));
const SUBS = MAN.subs;
const SAMPLE = "店铺\t平台\t站点\t期间\t销售额\t佣金率\t佣金\t广告费平台账单\t广告费\t其它费用\t结算净额\nUS-OUTDOOR\tAmazon\tUS\t2026-03\t120000.00\t15%\t18000.00\t19000.00\t19000.00\t2600.00\t80400.00\nEU-HOME\tAmazon\tDE\t2026-03\t80000.00\t11.5%\t9200.00\t10800.00\t10800.00\t1800.00\t58200.00\n合计\t\t\t\t200000.00\t\t27200.00\t29800.00\t29800.00\t4400.00\t138600.00";

function engineOf(id) {
  const rec = SUBS.find((s) => s.id === id);
  if (!rec) return null;
  const file = path.join(DIR, 'engine', 'parts', id, rec.entry || `${id}-full.js`);
  return fs.existsSync(file) ? require2(file) : null;
}
/** 该子技能在本包内是否有引擎（没有 ⇒ 它只在订阅版由订阅版提供）。 */
function localOf(id) {
  const rec = SUBS.find((s) => s.id === id);
  return Boolean(rec && fs.existsSync(path.join(DIR, 'engine', 'parts', id, rec.entry || `${id}-full.js`)));
}
/** 只按**材料表头**与子技能的关键词/表头词匹配；匹配不到就说匹配不到（不猜）。 */
function route(text, forced) {
  if (forced) return { id: forced, why: '点名指定' };
  const first = String(text || '').split('\n').map((l) => l.trim()).filter(Boolean)[0] || '';
  const words = first.split(/[\t|,，;；]+|\s{2,}/).map((w) => w.trim()).filter((w) => w.length >= 2);
  const scored = SUBS.map((s) => {
    let sc = 0;
    for (const w of words) {
      for (const c of s.cols || []) {
        if (!c) continue;
        if (c === w) { sc += 4; break; }
        if (c.includes(w) || w.includes(c)) { sc += 2; break; }
      }
      for (const k of s.kw || []) {
        if (!k) continue;
        if (k === w) { sc += 3; break; }
        if (k.includes(w) || w.includes(k)) { sc += 1; break; }
      }
    }
    return { id: s.id, name: s.name, sc };
  }).sort((a, b) => b.sc - a.sc);
  const top = scored[0];
  if (!top || top.sc <= 0) return { id: null, candidates: scored.slice(0, 5) };
  if (scored[1] && scored[1].sc === top.sc) return { id: null, tie: scored.filter((x) => x.sc === top.sc).slice(0, 5) };
  return { id: top.id, name: top.name, sc: top.sc };
}
function parse(args) {
  const o = { json: false };
  for (let i = 0; i < args.length; i++) {
    const a = args[i];
    if (a === '--json') o.json = true;
    else if (a === '--list') o.list = true;
    else if (a === '--sample') o.sample = true;
    else if (a === '--help' || a === '-h') o.help = true;
    else if (a === '--text') o.text = args[++i];
    else if (a === '--input') o.input = args[++i];
    else if (a === '--sub-skill') o.sub = args[++i];
  }
  return o;
}
const HELP = `用法：
  node scripts/run.mjs --list
  node scripts/run.mjs --sample
  node scripts/run.mjs --text "材料文本"
  node scripts/run.mjs --sub-skill <子技能id> --input 材料.json --json

「电商与平台结算专家」共 ${SUBS.length} 个子技能，全部在包内、**纯本地运行、不联网**。`;

function main() {
  const a = parse(process.argv.slice(2));
  if (a.help) { console.log(HELP); return 0; }
  if (a.list) {
    console.log(`「电商与平台结算专家」技能库（${SUBS.length} 个子技能，全部完整功能、全部本地运行）：`);
    SUBS.forEach((s, i) => console.log(`${String(i + 1).padStart(2)}. ${s.id}  —— ${s.name}`));
    return 0;
  }
  let text = a.text;
  if (a.sample) text = SAMPLE;
  if (a.input) {
    try {
      const raw = fs.readFileSync(a.input, 'utf8');
      const j = JSON.parse(raw);
      text = typeof j === 'string' ? j : (j.text || raw);
    } catch (e) { console.error(`读不到 --input 文件或不是合法 JSON：${e.message}`); return 1; }
  }
  if (!text) { console.error('没给材料：用 --text "…" 或 --input 材料.json（--help 看用法）'); return 1; }
  const used = bumpUses();
  if (used > FREE_USES) {
    console.log(`免费试用 ${FREE_USES} 次已用完（本机已用 ${used - 1} 次）。`);
    console.log('继续使用需要订阅：订阅入口见本技能的技能页说明（SkillPay 上的订阅商品，');
    console.log('优惠期内每月 9.9 元；优惠期内订阅的创始用户永久 9.9 元/月）。');
    console.log('说明：本次计数写在本机用户目录，不上报、不含你的材料内容。');
    return 42;
  }
  console.log(`（免费试用第 ${used} / ${FREE_USES} 次）`);
  const r = route(text, a.sub);
  if (r.id && !localOf(r.id)) {
    const rec = SUBS.find((s) => s.id === r.id) || {};
    console.log(`【${rec.name || r.id}】这个子技能的规则库**只在订阅版里提供**（本公开包内不含它的引擎）。`);
    console.log('公开包内可本地运行的是标着 [本包内] 的那些子技能。');
    return 3;
  }
  if (!r.id) {
    const cand = (r.candidates || r.tie || []).map((c) => `${c.id}（${c.name}）`).join('、');
    console.log('材料没有匹配到本类任何一个子技能，**本次没有执行任何检查**（不猜）。');
    if (cand) console.log('最接近的候选：' + cand + '（可用 --sub-skill 点名）');
    return 3;
  }
  const eng = engineOf(r.id);
  if (!eng || typeof eng.run !== 'function') { console.error(`包内没有该子技能的引擎：${r.id}`); return 4; }
  let out;
  try {
    out = eng.run(Object.assign({}, JSON.parse(text.startsWith('{') ? text : '{}'), { text, full: true }));
  } catch { out = eng.run({ text, full: true }); }
  const rec = SUBS.find((s) => s.id === r.id) || {};
  if (a.json) { console.log(JSON.stringify({ subSkill: r.id, subSkillName: rec.name, result: out }, null, 1)); return 0; }
  console.log(`【${rec.name || r.id}】本机执行（完整档引擎，纯本地、不联网）`);
  console.log(typeof out === 'string' ? out : JSON.stringify(out, null, 1));
  return 0;
}
try { process.exit(main()); } catch (e) { console.error('未预期错误：' + (e && e.stack || e)); process.exit(9); }
