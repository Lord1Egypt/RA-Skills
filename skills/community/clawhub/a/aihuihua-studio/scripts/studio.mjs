#!/usr/bin/env node
/**
 * AI 创作技能的命令行入口：登录、查余额、买点数、生图 / 视频 / 音乐、查任务和历史。
 *
 * 零依赖，Node 20+。同一份脚本服务 superx 和 aihuihua 两个站点，站点信息在 ../site.json。
 * 退出码：0 成功；1 出错；2 用法不对；3 点数不足；4 没登录 / 登录失效 / 等授权超时。
 */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { ApiError, requestJson, requestStream, setClientVersion, setClientAgent, request } from './lib/http.mjs';
import {
  SITE, BASE_URL, SKILL_ROOT, STATE_DIR, api, artApi, currentToken, fullUrl, readState, writeState, removeState,
} from './lib/store.mjs';
import { localVersion, isNewer, latestManifest, cannotSelfUpdate, installLatest } from './lib/update.mjs';
import { buildMatrix, renderTerminal, renderSvg, renderPng, writeHtml, openExternal } from './lib/qr.mjs';
import { detectAgent } from './lib/agent.mjs';
import { modelsForSite, findModel, mjAction, MJ_ACTION_LIST, STATUS_TEXT } from './lib/catalog.mjs';
import { ensureUrl } from './lib/upload.mjs';

const VERSION = localVersion();
setClientVersion(SITE.name, VERSION);
setClientAgent(detectAgent);
const SELF = path.join(SKILL_ROOT, 'scripts', 'studio.mjs');
const CMD = `node ${SELF}`;

const EXIT = { OK: 0, ERROR: 1, USAGE: 2, POINTS: 3, AUTH: 4 };
let JSON_MODE = false;

const info = (...a) => { if (!JSON_MODE) console.log(...a); };
const warn = (...a) => console.error(...a);
const P = SITE.pointName;

class Exit extends Error {
  constructor(code, message) {
    super(message);
    this.exitCode = code;
  }
}

// ─── 参数解析 ──────────────────────────────────────────────────

const BOOL_FLAGS = new Set(['json', 'start', 'wait', 'list', 'check', 'stream', 'help', 'force', 'no-open', 'audio', 'instrumental', 'watermark', 'all']);

function parseArgs(argv) {
  const out = { _: [], flags: {} };
  for (let i = 0; i < argv.length; i += 1) {
    const a = argv[i];
    if (a === '-h') { out.flags.help = true; continue; }
    if (!a.startsWith('--')) { out._.push(a); continue; }
    let key = a.slice(2);
    let value;
    const eq = key.indexOf('=');
    if (eq >= 0) { value = key.slice(eq + 1); key = key.slice(0, eq); }
    if (key.startsWith('no-') && key !== 'no-open') { out.flags[key.slice(3)] = false; continue; }
    if (value === undefined) {
      const next = argv[i + 1];
      if (BOOL_FLAGS.has(key) || next === undefined || (next.startsWith('--') && next.length > 2)) value = true;
      else { value = next; i += 1; }
    }
    if (out.flags[key] === undefined) out.flags[key] = value;
    else out.flags[key] = [].concat(out.flags[key], value);
  }
  return out;
}

const one = (v) => (Array.isArray(v) ? v[v.length - 1] : v);

// ─── 公共 ──────────────────────────────────────────────────────

function requireToken() {
  const token = currentToken();
  if (!token) throw new Exit(EXIT.AUTH, `还没登录 ${SITE.brand}。先运行：${CMD} login --start`);
  return token;
}

function classify(err) {
  const code = err?.code;
  const msg = String(err?.message || err);
  if (code === 40015 || code === 40101 || code === 401) return new Exit(EXIT.AUTH, `${msg}\n登录失效了，重新登录：${CMD} login --start`);
  if (code === 40022 || /(点数|积分)不足/.test(msg)) {
    return new Exit(EXIT.POINTS, `${msg}\n${P}不够了。看看充值套餐：${CMD} buy --list（买完再重试这条命令）`);
  }
  if (code === 'USAGE') return new Exit(EXIT.USAGE, msg);
  if (err?.status >= 500) {
    return new Exit(EXIT.ERROR, `网站这个功能暂时出错了（HTTP ${err.status}），一般是上游模型临时不可用，这次没有扣${P}。换个模型试试，或者过一会儿再试`);
  }
  return new Exit(EXIT.ERROR, msg);
}

async function me(token) {
  return (await requestJson(api('agent/me'), { token })).data;
}

function stamp() {
  const d = new Date();
  const p = (n) => String(n).padStart(2, '0');
  return `${d.getFullYear()}${p(d.getMonth() + 1)}${p(d.getDate())}-${p(d.getHours())}${p(d.getMinutes())}${p(d.getSeconds())}`;
}

const EXT_BY_TYPE = {
  'image/png': 'png', 'image/jpeg': 'jpg', 'image/webp': 'webp', 'image/gif': 'gif', 'video/mp4': 'mp4', 'audio/mpeg': 'mp3', 'audio/mp3': 'mp3', 'audio/wav': 'wav',
};

/** 把结果下载到本地。下载失败不算生成失败：地址照样给出去 */
async function download(results, { outDir, prefix }) {
  fs.mkdirSync(outDir, { recursive: true });
  const base = `${prefix}-${stamp()}`;
  let i = 0;
  for (const r of results) {
    i += 1;
    if (!r.url) continue;
    try {
      let buf;
      let ext = r.ext || '';
      if (r.url.startsWith('data:')) {
        const m = /^data:([^;]+);base64,(.*)$/s.exec(r.url);
        buf = Buffer.from(m[2], 'base64');
        ext = ext || EXT_BY_TYPE[m[1]] || 'bin';
        r.url = '';
      } else {
        const res = await request(r.url, { timeout: 10 * 60_000 });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        buf = Buffer.from(await res.arrayBuffer());
        ext = ext || EXT_BY_TYPE[(res.headers.get('content-type') || '').split(';')[0]]
          || (/\.([a-z0-9]{2,4})(?:\?|$)/i.exec(new URL(r.url).pathname)?.[1]) || { image: 'png', video: 'mp4', audio: 'mp3' }[r.kind] || 'bin';
      }
      const file = path.join(outDir, `${base}${results.length > 1 ? `-${i}` : ''}.${ext.toLowerCase()}`);
      fs.writeFileSync(file, buf);
      r.file = file;
    } catch (e) {
      r.downloadError = e.message;
    }
  }
  return results;
}

const KIND_TEXT = { image: '图片', video: '视频', audio: '音频' };

async function report(outcome, { model, token, outDir }) {
  const results = await download(outcome.results || [], { outDir, prefix: model.id });
  let balance = null;
  try {
    balance = (await me(token)).point_count;
  } catch {
    /* 查不到余额不影响结果 */
  }
  if (JSON_MODE) {
    console.log(JSON.stringify({ ok: true, model: model.id, cost: outcome.cost ?? null, balance, records_page: SITE.recordsPage || null, results, mj: outcome.mj, lyrics: outcome.lyrics }, null, 2));
    return;
  }
  info(`✓ ${model.name} 完成${outcome.cost != null ? `，消耗 ${outcome.cost} ${P}` : ''}${balance != null ? `，剩余 ${balance} ${P}` : ''}`);
  if (outcome.cost > 0 && SITE.recordsPage) info(`  ${P}消耗明细：${SITE.recordsPage}`);
  const counters = {};
  results.forEach((r) => {
    counters[r.kind] = (counters[r.kind] || 0) + 1;
    const label = `${KIND_TEXT[r.kind] || '文件'} ${counters[r.kind]}${r.title ? `（${r.title}）` : ''}`;
    if (r.file) info(`  ${label}：${r.file}`);
    if (r.url) info(`  ${r.file ? ' '.repeat(label.length + 2) : `${label}：`}${r.url}`);
    if (r.downloadError) info(`  （下载到本地失败：${r.downloadError}，可以直接用上面的地址）`);
  });
  if (outcome.mj) {
    info(`  MJ 图片 ID：${outcome.mj.imgId}`);
    if (outcome.mj.actions.length) info(`  可继续操作（1 小时内）：${CMD} mj-action --id ${outcome.mj.imgId} --action <${outcome.mj.actions.join('|')}>`);
  }
  // 一次出的两首经常是同一份歌词，只打一遍
  const seen = new Set();
  (outcome.lyrics || []).forEach((s) => {
    if (!s.lyrics || seen.has(s.lyrics)) return;
    seen.add(s.lyrics);
    info(`\n  《${s.title || '未命名'}》歌词：\n${s.lyrics.split('\n').map((l) => `    ${l}`).join('\n')}`);
  });
}

function defaultOutDir() {
  return path.resolve(process.cwd(), `${SITE.id}-outputs`);
}

// ─── 登录 ──────────────────────────────────────────────────────

function clientInfo() {
  let user = '';
  try {
    user = os.userInfo().username;
  } catch {
    /* 容器里可能没有 passwd 条目 */
  }
  let agent = '';
  try {
    agent = detectAgent();
  } catch {
    /* 认不出来就算了 */
  }
  return { hostname: os.hostname(), platform: `${process.platform}-${process.arch}`, user, agent, version: VERSION };
}

const verifyUrl = (userCode) => `${SITE.authPage}?code=${encodeURIComponent(userCode)}`;

async function loginStart({ open = true } = {}) {
  const res = await requestJson(api('agent/device/start'), { data: { client: clientInfo() } });
  const d = res.data;
  const pending = { baseUrl: BASE_URL, deviceCode: d.deviceCode, userCode: d.userCode, interval: d.interval || 3, expiresAt: Date.now() + d.expiresIn * 1000 };
  writeState('pending-login.json', pending);
  const url = verifyUrl(d.userCode);
  info(`请在浏览器打开下面的链接，确认授权码一致后点「授权」：`);
  info(`  ${url}`);
  info(`  授权码：${d.userCode}（${Math.round(d.expiresIn / 60)} 分钟内有效）`);
  info(`浏览器里还没登录 ${SITE.brand} 的话，页面会先让你登录。`);
  if (open && !process.env.STUDIO_NO_OPEN) openExternal(url);
  if (JSON_MODE) console.log(JSON.stringify({ verifyUrl: url, userCode: d.userCode, expiresIn: d.expiresIn }));
  return pending;
}

async function loginWait(timeoutSec) {
  const pending = readState('pending-login.json');
  if (!pending || pending.baseUrl !== BASE_URL) throw new Exit(EXIT.AUTH, `没有进行中的登录，先运行：${CMD} login --start`);
  const deadline = Math.min(pending.expiresAt, Date.now() + timeoutSec * 1000);
  info(`等待你在浏览器里授权（授权码 ${pending.userCode}）…`);
  while (Date.now() < deadline) {
    const res = await requestJson(api('agent/device/poll'), { data: { deviceCode: pending.deviceCode } });
    const d = res.data;
    if (d.status === 'approved') {
      writeState('credentials.json', { baseUrl: BASE_URL, token: d.token, user: d.user ? { uid: d.user.uid, nickname: d.user.nickname } : null, savedAt: new Date().toISOString() });
      removeState('pending-login.json');
      const u = d.user || {};
      info(`✓ 登录成功：${u.nickname || u.email || `用户 ${u.uid}`}（UID ${u.uid}），${P}余额 ${u.point_count}`);
      if (JSON_MODE) console.log(JSON.stringify({ ok: true, user: u }));
      return;
    }
    if (d.status === 'denied') {
      removeState('pending-login.json');
      throw new Exit(EXIT.AUTH, `授权被拒绝了。需要的话重新运行：${CMD} login --start`);
    }
    if (d.status === 'expired') {
      removeState('pending-login.json');
      throw new Exit(EXIT.AUTH, `授权码已过期，重新运行：${CMD} login --start，把新链接发给用户`);
    }
    await new Promise((r) => setTimeout(r, (d.interval || pending.interval || 3) * 1000));
  }
  if (Date.now() >= pending.expiresAt) {
    removeState('pending-login.json');
    throw new Exit(EXIT.AUTH, `授权码已过期，重新运行：${CMD} login --start`);
  }
  throw new Exit(EXIT.AUTH, `还没等到授权。用户点完「授权」后再运行：${CMD} login --wait`);
}

async function cmdLogin(args) {
  const f = args.flags;
  const timeout = Number(one(f.timeout)) || 240;
  if (f.wait && !f.start) return loginWait(timeout);
  if (!f.force && !f.start && currentToken()) {
    try {
      const u = await me(currentToken());
      info(`已经登录：${u.nickname || u.email || u.uid}（UID ${u.uid}），${P}余额 ${u.point_count}。要换账号加 --force`);
      return;
    } catch {
      /* 令牌失效，接着登录 */
    }
  }
  await loginStart({ open: f['no-open'] !== true });
  if (f.start) {
    info(`\n用户点完「授权」后运行：${CMD} login --wait`);
    return;
  }
  await loginWait(timeout);
}

async function cmdWhoami() {
  const token = requireToken();
  let u;
  try {
    u = await me(token);
  } catch (e) {
    throw classify(e);
  }
  if (JSON_MODE) {
    console.log(JSON.stringify(u, null, 2));
    return;
  }
  info(`${SITE.brand} 账号：${u.nickname || u.email || '-'}（UID ${u.uid}）`);
  info(`${P}余额：${u.point_count}`);
}

async function cmdLogout() {
  const token = currentToken();
  if (token) {
    try {
      await requestJson(api('agent/logout'), { data: {}, token });
    } catch {
      /* 令牌已经失效也照样清本机 */
    }
  }
  removeState('credentials.json');
  info('✓ 已退出登录，本机令牌已作废');
}

// ─── 模型 ──────────────────────────────────────────────────────

function optionUsage(o) {
  const v = o.type === 'enum' ? `<${o.values.join('|')}>` : o.type === 'int' ? `<${o.min}-${o.max}>` : o.type === 'bool' ? '' : o.type === 'file' ? '<路径或URL>' : '<文本>';
  const def = o.default !== undefined && o.type !== 'bool' ? `，默认 ${o.default}` : o.type === 'bool' ? `，默认${o.default ? '开' : '关'}` : '';
  return `    --${o.key}${v ? ` ${v}` : ''}${o.multiple ? ' （可重复，最多 ' + o.max + ' 个）' : ''}  ${o.desc}${def}${o.required ? '（必填）' : ''}`;
}

function cmdModels(args) {
  const type = one(args.flags.type);
  const list = modelsForSite().filter((m) => !type || m.type === type);
  const id = args._[0];
  if (JSON_MODE) {
    const pick = id ? list.filter((m) => m.id === findModel(id)?.id) : list;
    console.log(JSON.stringify(pick.map((m) => ({
      id: m.id, type: m.type, name: m.name, summary: m.summary, details: m.details, price: m.costText(), options: m.options,
    })), null, 2));
    return;
  }
  if (id) {
    const m = findModel(id);
    if (!m) throw new Exit(EXIT.USAGE, `没有模型「${id}」。全部模型：${CMD} models`);
    info(`${m.id} —— ${m.name}`);
    info(`  ${m.summary}`);
    m.details.forEach((d) => info(`  · ${d}`));
    info(`  价格：${m.costText()}`);
    info(`  参数：`);
    if (!m.noPrompt) info(`    --prompt <文本>  提示词${m.promptOptional ? '' : '（必填）'}`);
    m.options.forEach((o) => info(optionUsage(o)));
    return;
  }
  const groups = { image: '图片', video: '视频', music: '音乐', speech: '语音', tool: '图片工具' };
  for (const [t, title] of Object.entries(groups)) {
    const ms = list.filter((m) => m.type === t);
    if (!ms.length) continue;
    info(`\n【${title}】`);
    ms.forEach((m) => info(`  ${m.id.padEnd(24)} ${m.name}：${m.summary}\n  ${''.padEnd(24)} 价格：${m.costText()}`));
  }
  info(`\n看某个模型的全部参数：${CMD} models <模型ID>`);
}

/** 按目录里的选项定义把命令行参数整理成干净的对象，顺带校验 */
function collectOptions(model, flags) {
  const o = {};
  for (const opt of model.options) {
    let v = flags[opt.key];
    if (v === undefined) {
      if (opt.default !== undefined) o[opt.key] = opt.default;
      if (opt.required) throw new Exit(EXIT.USAGE, `${model.id} 需要 --${opt.key}（${opt.desc}）`);
      continue;
    }
    if (opt.type === 'bool') {
      o[opt.key] = one(v) !== false && one(v) !== 'false';
      continue;
    }
    if (opt.multiple) {
      v = [].concat(v).flatMap((x) => String(x).split(/\s*,\s*(?=https?:|\/|\.|~)/)).filter(Boolean);
      if (v.length > opt.max) throw new Exit(EXIT.USAGE, `--${opt.key} 最多 ${opt.max} 个`);
      o[opt.key] = v;
      continue;
    }
    v = one(v);
    if (v === true) throw new Exit(EXIT.USAGE, `--${opt.key} 后面要跟值`);
    if (opt.type === 'enum') {
      const hit = opt.values.find((x) => x.toLowerCase() === String(v).toLowerCase());
      if (!hit) throw new Exit(EXIT.USAGE, `--${opt.key} 只能是：${opt.values.join(' / ')}`);
      o[opt.key] = hit;
    } else if (opt.type === 'int') {
      const n = Number(v);
      if (!Number.isInteger(n) || n < opt.min || n > opt.max) throw new Exit(EXIT.USAGE, `--${opt.key} 要是 ${opt.min}～${opt.max} 的整数`);
      o[opt.key] = n;
    } else {
      o[opt.key] = String(v);
    }
  }
  const known = new Set([...model.options.map((x) => x.key), 'prompt', 'out', 'json', 'yes', 'help', 'max-cost']);
  const unknown = Object.keys(flags).filter((k) => !known.has(k));
  if (unknown.length) throw new Exit(EXIT.USAGE, `${model.id} 不认识这些参数：${unknown.map((k) => `--${k}`).join(' ')}。看参数：${CMD} models ${model.id}`);
  return o;
}

function readPrompt(args, model) {
  let prompt = args.flags.prompt !== undefined ? String(one(args.flags.prompt)) : args._.slice(1).join(' ');
  if (prompt && fs.existsSync(prompt) && /\.(txt|md)$/i.test(prompt)) prompt = fs.readFileSync(prompt, 'utf8');
  prompt = prompt.trim();
  if (!prompt && !model.noPrompt && !model.promptOptional) throw new Exit(EXIT.USAGE, `${model.id} 需要提示词：--prompt "…"`);
  return prompt;
}

function prepare(args) {
  const model = findModel(args._[0]);
  if (!model) throw new Exit(EXIT.USAGE, args._[0] ? `${SITE.brand} 没有模型「${args._[0]}」。全部模型：${CMD} models` : `用法：${CMD} gen <模型ID> --prompt "…"`);
  const prompt = readPrompt(args, model);
  const o = collectOptions(model, args.flags);
  model.prepare?.(o);
  const problem = model.validate?.(o, prompt);
  if (problem) throw new Exit(EXIT.USAGE, problem);
  return { model, prompt, o, cost: model.cost(o, prompt) };
}

async function cmdPrice(args) {
  const { model, cost } = prepare({ ...args, flags: { prompt: 'x', ...args.flags } });
  if (JSON_MODE) console.log(JSON.stringify({ model: model.id, points: cost, rule: model.costText() }));
  else info(`${model.name}：这组参数预计消耗 ${cost} ${P}（${model.costText()}）`);
}

async function cmdGen(args) {
  const token = requireToken();
  const { model, prompt, o, cost } = prepare(args);
  const maxCost = Number(one(args.flags['max-cost']));
  if (maxCost && cost > maxCost) throw new Exit(EXIT.USAGE, `预计消耗 ${cost} ${P}，超过 --max-cost ${maxCost}，没有提交`);
  info(`→ ${model.name}，预计消耗 ${cost} ${P}`);
  const log = (s) => info(s);
  let outcome;
  try {
    outcome = await model.run({ prompt, o, token, log });
  } catch (e) {
    if (e.pending) {
      info(`任务还在跑：${CMD} task ${model.id} ${e.pending.id}`);
      throw new Exit(EXIT.ERROR, e.message);
    }
    throw classify(e);
  }
  if (outcome.pending) {
    if (JSON_MODE) console.log(JSON.stringify({ ok: true, pending: outcome.pending }));
    else info(`✓ 已提交，任务 ID ${outcome.pending.id}。查进度并下载：${CMD} task ${model.id} ${outcome.pending.id}`);
    return;
  }
  await report(outcome, { model, token, outDir: path.resolve(one(args.flags.out) || defaultOutDir()) });
}

/** 文字转语音的音色表（tts 模型的 --voice 从这里挑），带试听链接；不用登录 */
async function cmdVoices(args) {
  const res = await requestJson(api('text-speech/voices'), { timeout: 30_000 });
  const { voices, featured, sampleBase, defaultVoice } = res.data;
  const f = (k) => (args.flags[k] === undefined ? '' : String(one(args.flags[k])).trim());
  const lang = f('lang');
  const gender = f('gender');
  const scene = f('scene');
  const q = f('q') || args._.join(' ').trim();
  const rank = (v) => (featured.includes(v.id) ? featured.indexOf(v.id) : featured.length);
  const list = voices
    .filter((v) => (!lang || v.lang.includes(lang)) && (!gender || v.gender === gender) && (!scene || v.scene.includes(scene))
      && (!q || v.name.includes(q) || v.id.includes(q)))
    .sort((a, b) => rank(a) - rank(b))
    .map((v) => ({ ...v, featured: featured.includes(v.id), sample: `${sampleBase}/${v.id}.mp3` }));
  if (JSON_MODE) {
    console.log(JSON.stringify({ default: defaultVoice, count: list.length, voices: list }, null, 2));
    return;
  }
  if (!list.length) {
    info(`没有符合条件的音色。语种有：${[...new Set(voices.map((v) => v.lang))].join(' ')}；场景有：${[...new Set(voices.map((v) => v.scene))].join(' ')}`);
    return;
  }
  const limit = Number(one(args.flags.limit)) || (args.flags.all ? list.length : 60);
  info(`共 ${list.length} 个音色${list.length > limit ? `，先列 ${limit} 个（--all 看全部，或加 --lang/--gender/--scene/--q 筛选）` : ''}；默认 ${defaultVoice}`);
  list.slice(0, limit).forEach((v) => info(`  ${v.featured ? '★' : ' '} ${v.name}（${v.gender}·${v.scene}·${v.lang}）  ${v.id}\n      试听：${v.sample}`));
  info(`\n用法：${CMD} gen tts --voice <音色ID> --prompt "要念的文字"`);
}

async function cmdMjAction(args) {
  const token = requireToken();
  const imgId = one(args.flags.id) || args._[0];
  const action = one(args.flags.action) || args._[1];
  if (!imgId || !action) {
    throw new Exit(EXIT.USAGE, `用法：${CMD} mj-action --id <MJ图片ID> --action <操作>\n可用操作：\n${MJ_ACTION_LIST.map(([a, , c, d]) => `  ${a.padEnd(10)} ${d}（${c} ${P}）`).join('\n')}`);
  }
  let outcome;
  try {
    outcome = await mjAction({ imgId, action, token, log: (s) => info(s) });
  } catch (e) {
    throw classify(e);
  }
  await report(outcome, { model: findModel('midjourney'), token, outDir: path.resolve(one(args.flags.out) || defaultOutDir()) });
}

async function cmdTask(args) {
  const token = requireToken();
  if (!args._[0]) {
    const list = readState('tasks.json') || [];
    if (!list.length) return info('本机没有提交过视频任务');
    info('最近提交的视频任务（新的在前）：');
    list.slice(0, 15).forEach((t) => info(`  ${t.model.padEnd(20)} 任务 ${t.id}  ${new Date(t.at).toLocaleString('zh-CN')}`));
    info(`查进度并下载：${CMD} task <模型ID> <任务ID>`);
    return;
  }
  const model = findModel(args._[0]);
  const id = args._[1] || one(args.flags.id);
  if (!model?.resume || !id) throw new Exit(EXIT.USAGE, `用法：${CMD} task <视频模型ID> <任务ID> [--no-wait]`);
  const wait = args.flags.wait !== false;
  let outcome;
  try {
    outcome = await model.resume({ id, token, log: (s) => info(s), wait });
  } catch (e) {
    if (e.pending) throw new Exit(EXIT.ERROR, e.message);
    throw classify(e);
  }
  if (outcome.task) {
    const t = outcome.task;
    if (JSON_MODE) console.log(JSON.stringify(t, null, 2));
    else info(`任务 ${t.id}：${STATUS_TEXT[t.status] || t.status}${t.video_url ? `，${fullUrl(t.video_url)}` : ''}${t.error ? `，${t.error}` : ''}`);
    return;
  }
  await report(outcome, { model, token, outDir: path.resolve(one(args.flags.out) || defaultOutDir()) });
}

async function cmdHistory(args) {
  const token = requireToken();
  const limit = Math.min(Number(one(args.flags.limit)) || 10, 50);
  let res;
  try {
    res = await requestJson(artApi('my-paintings'), { data: { pageIndex: Number(one(args.flags.page)) || 1, pageSize: limit }, token });
  } catch (e) {
    throw classify(e);
  }
  const rows = (res.rows || res.data?.rows || []).map((r) => {
    let url = r.img_url;
    if (typeof url === 'string' && url.startsWith('{')) {
      try {
        url = JSON.parse(url).images?.[0] || url;
      } catch {
        /* 不是 JSON 就原样 */
      }
    }
    return {
      id: r.id, type: r.painting_type, cost: r.cost, time: r.create_time, prompt: String(r.prompt || r.prompt_zh || '').slice(0, 80), url: fullUrl(url, r.painting_type),
    };
  });
  if (JSON_MODE) return console.log(JSON.stringify({ count: res.count, rows }, null, 2));
  info(`我的作品（共 ${res.count ?? '?'} 条，显示最近 ${rows.length} 条）：`);
  const when = (t) => (t ? new Date(t).toLocaleString('zh-CN', { hour12: false }) : '-');
  rows.forEach((r) => info(`  #${r.id} ${String(r.type).padEnd(14)} ${r.cost ?? '-'} ${P}  ${when(r.time)}  ${r.prompt}\n      ${r.url}`));
}

// ─── 购买 ──────────────────────────────────────────────────────

async function listPackages() {
  if (SITE.packages === 'v2') {
    const res = await requestJson(api('get-pkg-list-v2'));
    // 技能只消耗积分，和包月会员无关，所以只卖积分包
    return (res.data || []).filter((cat) => cat.type === 'points').flatMap((cat) => (cat.pkgs || []).map((p) => ({
      id: p.id, group: '积分包（永久有效）', name: p.name, price: Number(p.price), points: p.points,
      note: (p.features || []).filter((t) => !t.includes('会员')).join('，'),
    })));
  }
  const list = await requestJson(api('get-pkg-list?host=all&pkg_type=1'));
  return (Array.isArray(list) ? list : []).map((p) => ({
    id: p.id, group: '点数包', name: p.title || `${p.paint_point} 点数`, price: Number(p.price), points: p.paint_point, note: p.desc || '',
  }));
}

async function cmdBuy(args) {
  const f = args.flags;
  if (f.wait) return buyWait(args);
  const pkgs = await listPackages();
  const pkgId = Number(one(f.pkg) || args._[0]);
  if (f.list || !pkgId) {
    if (JSON_MODE) return console.log(JSON.stringify(pkgs, null, 2));
    let group = '';
    pkgs.forEach((p) => {
      if (p.group !== group) { group = p.group; info(`\n【${group}】`); }
      info(`  套餐 ${String(p.id).padEnd(3)} ¥${p.price}  ${p.name}  → ${p.points} ${P}${p.note ? `（${p.note}）` : ''}`);
    });
    info(`\n下单（生成微信支付二维码）：${CMD} buy --pkg <套餐ID>`);
    return;
  }
  const token = requireToken();
  const pkg = pkgs.find((p) => p.id === pkgId);
  if (!pkg) throw new Exit(EXIT.USAGE, `没有套餐 ${pkgId}，看列表：${CMD} buy --list`);
  const body = SITE.packages === 'v2'
    ? { pkgId, orderType: 'native', version: 2, deviceType: 'pc', buyCount: 1 }
    : { pkgId, orderType: 'native', buyCount: 1, channel: 'agent-skill', source: 'agent-skill' };
  let order;
  try {
    order = await requestJson(api('create-order'), { data: body, token });
  } catch (e) {
    throw classify(e);
  }
  if (!order?.code_url) throw new Exit(EXIT.ERROR, `下单失败：${order?.message || order?.msg || '没有拿到支付二维码'}`);

  const matrix = buildMatrix(order.code_url);
  const dir = path.join(STATE_DIR, 'pay');
  fs.mkdirSync(dir, { recursive: true });
  const svgFile = path.join(dir, `pay-${order.out_trade_no}.svg`);
  fs.writeFileSync(svgFile, renderSvg(matrix));
  const htmlFile = writeHtml(matrix, {
    title: `${SITE.brand} 微信扫码支付`,
    lines: [`¥${pkg.price} · ${pkg.name} · ${pkg.points} ${P}`, `订单号 ${order.out_trade_no}`],
    file: path.join(dir, `pay-${order.out_trade_no}.html`),
  });
  const pngFile = path.join(dir, `pay-${order.out_trade_no}.png`);
  fs.writeFileSync(pngFile, renderPng(matrix));
  writeState('pending-order.json', { baseUrl: BASE_URL, outTradeNo: order.out_trade_no, pkg, createdAt: Date.now() });
  if (f['no-open'] !== true && !process.env.STUDIO_NO_OPEN) openExternal(htmlFile);
  // 传成 https 图片，Agent 贴进回复就能直接显示；传不上去也不影响付款，本地文件还在
  let qrUrl = '';
  try {
    qrUrl = await ensureUrl(pngFile, token);
  } catch {}

  if (JSON_MODE) {
    console.log(JSON.stringify({ outTradeNo: order.out_trade_no, codeUrl: order.code_url, qrImageUrl: qrUrl, png: pngFile, html: htmlFile, svg: svgFile, pkg }, null, 2));
    return;
  }
  info(`已下单：¥${pkg.price} · ${pkg.name}（${pkg.points} ${P}），订单号 ${order.out_trade_no}`);
  if (qrUrl) {
    info('\n【给 Agent】把下面这一行原样放进你给用户的回复里（单独一行，不要放进代码块），对话里会直接显示二维码：');
    info(`![微信扫码支付 ¥${pkg.price}](${qrUrl})\n`);
  }
  info('请用微信扫码支付（二维码已在浏览器打开；也可以扫下面这个）：\n');
  info(renderTerminal(matrix));
  info(`\n二维码图片：${pngFile}\n           ${htmlFile}`);
  info(`付完之后运行：${CMD} buy --wait  （二维码 2 小时内有效）`);
}

async function buyWait(args) {
  const token = requireToken();
  const pending = readState('pending-order.json');
  const outTradeNo = one(args.flags.order) || pending?.outTradeNo;
  if (!outTradeNo) throw new Exit(EXIT.USAGE, `没有待支付的订单，先下单：${CMD} buy --pkg <套餐ID>`);
  const timeoutSec = Number(one(args.flags.timeout)) || 300;
  const deadline = Date.now() + timeoutSec * 1000;
  info(`等待订单 ${outTradeNo} 支付…`);
  let state = '';
  while (Date.now() < deadline) {
    const r = await requestJson(api('query-order-status'), { data: { out_trade_no: outTradeNo }, token });
    state = r?.trade_state || '';
    if (state === 'SUCCESS') {
      removeState('pending-order.json');
      await new Promise((res) => setTimeout(res, 2000)); // 到账是支付回调里做的，给它一点时间
      const u = await me(token);
      info(`✓ 支付成功，当前${P}余额 ${u.point_count}`);
      if (JSON_MODE) console.log(JSON.stringify({ ok: true, balance: u.point_count }));
      return;
    }
    if (['CLOSED', 'REVOKED', 'PAYERROR'].includes(state)) {
      removeState('pending-order.json');
      throw new Exit(EXIT.ERROR, `订单已${state === 'CLOSED' ? '关闭' : state === 'REVOKED' ? '撤销' : '支付失败'}，需要的话重新下单`);
    }
    await new Promise((res) => setTimeout(res, 3000));
  }
  throw new Exit(EXIT.AUTH, `还没支付（状态 ${state || '未知'}）。用户付完后再运行：${CMD} buy --wait`);
}

async function cmdRedeem(args) {
  if (!SITE.coupon) throw new Exit(EXIT.USAGE, `${SITE.brand} 暂不支持卡券兑换`);
  const token = requireToken();
  const code = one(args.flags.code) || args._[0];
  const password = one(args.flags.password) || args._[1];
  if (!code || !password) throw new Exit(EXIT.USAGE, `用法：${CMD} redeem --code <卡号> --password <卡密>`);
  try {
    const r = await requestJson(api('coupon/redeem'), { data: { coupon_code: code, password }, token });
    const u = await me(token);
    info(`✓ ${r.message || '兑换成功'}，当前${P}余额 ${u.point_count}`);
  } catch (e) {
    throw classify(e);
  }
}

// ─── 其他 ──────────────────────────────────────────────────────

async function cmdUpload(args) {
  const token = requireToken();
  if (!args._.length) throw new Exit(EXIT.USAGE, `用法：${CMD} upload <文件> [更多文件]`);
  for (const f of args._) info(await ensureUrl(f, token));
}

async function cmdCall(args) {
  const token = requireToken();
  const [method = 'GET', p] = args._;
  if (!p) throw new Exit(EXIT.USAGE, `用法：${CMD} call <GET|POST> <路径，如 ${SITE.artPrefix}/xxx 或 /api/xxx> [--data '{json}'] [--stream]`);
  const url = `${BASE_URL}${p.startsWith('/') ? '' : '/'}${p}`;
  const data = args.flags.data ? JSON.parse(one(args.flags.data)) : undefined;
  if (args.flags.stream) {
    const events = await requestStream(url, { data, token, onEvent: (e) => { if (!e.ps) console.log(JSON.stringify(e)); } });
    if (!events.length) console.log('(没有返回内容)');
    return;
  }
  try {
    const res = await requestJson(url, { method: method.toUpperCase(), data: method.toUpperCase() === 'GET' ? undefined : (data || {}), token });
    console.log(JSON.stringify(res, null, 2));
  } catch (e) {
    console.log(JSON.stringify(e.body || { error: e.message }, null, 2));
    throw classify(e);
  }
}

async function cmdUpdate(args) {
  const manifest = await latestManifest({ force: true });
  if (!manifest) throw new Exit(EXIT.ERROR, '取不到发布信息，稍后再试');
  if (!isNewer(manifest.version, VERSION)) return info(`已经是最新版 v${VERSION}`);
  if (args.flags.check) return info(`有新版 v${manifest.version}（本机 v${VERSION}）。更新：${CMD} update`);
  const why = cannotSelfUpdate();
  if (why) throw new Exit(EXIT.ERROR, `不能自动更新：${why}。手动更新：curl -fsSL ${manifest.tarball} | tar -xzf - -C ${path.dirname(SKILL_ROOT)}`);
  const v = await installLatest(manifest);
  info(`✓ 技能已更新：v${VERSION} → v${v}。请重新阅读 ${path.join(SKILL_ROOT, 'SKILL.md')}`);
}

/** 每条命令前看一眼有没有新版，有就换上、用新脚本重跑这条命令 */
async function autoUpdate(argv) {
  if (process.env.STUDIO_UPDATED || cannotSelfUpdate()) return false;
  const manifest = await latestManifest();
  if (!manifest || !isNewer(manifest.version, VERSION)) return false;
  let installed;
  try {
    installed = await installLatest(manifest);
  } catch (e) {
    warn(`! 有新版技能 v${manifest.version}，自动更新没成功（${e.message}），这次先用 v${VERSION} 跑`);
    return false;
  }
  warn(`★ ${SITE.name} 技能已自动更新：v${VERSION} → v${installed}。这条命令结束后请重新阅读 ${path.join(SKILL_ROOT, 'SKILL.md')}（流程和参数可能变了）`);
  const r = spawnSync(process.execPath, [...process.execArgv, SELF, ...argv], { stdio: 'inherit', env: { ...process.env, STUDIO_UPDATED: '1' } });
  process.exit(r.status ?? 1);
  return true;
}

const HELP = `${SITE.brand} AI 创作技能 v${VERSION}（${BASE_URL}）

用法：${CMD} <命令> [参数]

账号
  login [--start|--wait]   授权码登录（--start 只出链接，--wait 等用户授权）
  whoami                   当前账号和${P}余额（没登录退出码 4）
  logout                   退出并作废本机令牌
  buy --list               充值套餐
  buy --pkg <ID>           下单，出微信支付二维码；付完运行 buy --wait
${SITE.coupon ? '  redeem --code X --password Y   卡券兑换\n' : ''}
创作
  models [模型ID] [--type image|video|music|speech|tool]   模型、能力、参数和价格
  price <模型ID> [参数]    预估消耗
  gen <模型ID> --prompt "…" [参数] [--out 目录] [--max-cost N]
                           生成并下载到本地（默认 ./${SITE.id}-outputs/）
  voices [--lang 中文] [--gender 男|女] [--scene 场景] [--q 关键词]   文字转语音的音色和试听链接
  mj-action --id <图片ID> --action <U1…V4|zoom2|pan-left…>   Midjourney 放大 / 变体 / 扩图
  task [模型ID 任务ID]     视频任务进度，出片后下载（不带参数列出最近的任务）
  history [--limit 10]     我的作品
  upload <文件>            把本地文件传成 URL

其他
  call <GET|POST> <路径> [--data JSON] [--stream]   直接调网站接口
  update [--check]         更新技能（平时会自动更新）
  version

全局：--json 输出 JSON
退出码：0 成功，1 出错，2 用法不对，3 ${P}不足，4 没登录 / 等待超时`;

/**
 * 设了 HTTPS_PROXY / HTTP_PROXY 的机器（公司网络、开着代理客户端）直连网站常常连不上，
 * curl 会走代理而 Node 的 fetch 默认不走。Node 22.21+ / 24.5+ 认 NODE_USE_ENV_PROXY，
 * 带上它把自己重跑一遍；老版本 Node 没这个能力，照旧直连。
 */
function rerunWithEnvProxy(argv) {
  const keys = ['HTTPS_PROXY', 'https_proxy', 'HTTP_PROXY', 'http_proxy'];
  if (!keys.some((k) => process.env[k]) || process.env.NODE_USE_ENV_PROXY) return;
  const [major, minor] = process.versions.node.split('.').map(Number);
  if (!((major === 22 && minor >= 21) || (major === 24 && minor >= 5) || major >= 25)) return;
  const r = spawnSync(process.execPath, ['--disable-warning=UNDICI-EHPA', SELF, ...argv], {
    stdio: 'inherit',
    env: { ...process.env, NODE_USE_ENV_PROXY: '1' },
  });
  process.exit(r.status ?? 1);
}

async function main() {
  const argv = process.argv.slice(2);
  rerunWithEnvProxy(argv);
  const args = parseArgs(argv);
  JSON_MODE = args.flags.json === true;
  const cmd = args._.shift() || 'help';
  if (args.flags.help || cmd === 'help') return console.log(HELP);
  if (cmd === 'version' || cmd === '--version') return console.log(VERSION);
  if (cmd !== 'update') await autoUpdate(argv);

  const table = {
    login: cmdLogin,
    whoami: cmdWhoami,
    balance: cmdWhoami,
    me: cmdWhoami,
    logout: cmdLogout,
    models: cmdModels,
    price: cmdPrice,
    gen: cmdGen,
    generate: cmdGen,
    voices: cmdVoices,
    'mj-action': cmdMjAction,
    task: cmdTask,
    history: cmdHistory,
    buy: cmdBuy,
    redeem: cmdRedeem,
    upload: cmdUpload,
    call: cmdCall,
    update: cmdUpdate,
  };
  // 直接写模型名也行：studio.mjs midjourney --prompt …
  if (!table[cmd] && findModel(cmd)) {
    args._.unshift(cmd);
    return cmdGen(args);
  }
  const fn = table[cmd];
  if (!fn) throw new Exit(EXIT.USAGE, `不认识的命令「${cmd}」\n\n${HELP}`);
  return fn(args);
}

main().catch((e) => {
  const err = e instanceof Exit ? e : e instanceof ApiError ? classify(e) : new Exit(EXIT.ERROR, e?.stack || String(e));
  if (JSON_MODE) console.log(JSON.stringify({ ok: false, exitCode: err.exitCode, error: err.message }));
  else warn(`✗ ${err.message}`);
  process.exit(err.exitCode);
});
