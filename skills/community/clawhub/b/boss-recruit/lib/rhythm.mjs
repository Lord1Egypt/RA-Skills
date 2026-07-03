/**
 * 反风控节奏层 (rhythm layer)
 * ───────────────────────────────────────────────────────────────────────────
 * 三场景 skill 的共用底座。把"像真人"的确定性逻辑沉在代码里，不靠 LLM 即兴：
 *   - 随机延时（几十秒级，非固定）
 *   - 拟人点击 / 逐字输入（OpenCLI 原生 CDP，不用 DOM .click()）
 *   - 风控信号检测 → 立即熔断
 *   - 三次身份校验（防发错人）
 *   - 单轮批量上限 + 每 N 人校验 + 权益耗尽诊断
 *
 * 依赖：opencli（已 bind 的 browser session）。纯 ESM，无第三方依赖。
 * 规范见 ../references/anti-detection.md
 */
import { execFile } from 'node:child_process';
import { promisify } from 'node:util';
const pexec = promisify(execFile);

// ── 可恢复暂停态（与状态机对齐）─────────────────────────────────────────────
export const Pause = {
  WRONG_THREAD: 'paused_for_wrong_candidate_thread',
  SWITCH_THREAD: 'paused_for_switch_thread',
  SEND_MESSAGE: 'paused_for_send_message',
  QUOTA_EXHAUSTED: 'paused_for_boss_contact_quota_exhausted',
  CANDIDATE_BINDING: 'paused_for_candidate_binding',
  ATTACHMENT_ACCEPT: 'paused_for_attachment_acceptance',
  RISK_DETECTED: 'paused_for_risk_signal',
};

/** 抛出可恢复暂停：编排层捕获后停止本轮、保留进度、按 5 段式告知用户。 */
export class PausedError extends Error {
  constructor(state, detail = '', extra = {}) {
    super(`[${state}] ${detail}`);
    this.name = 'PausedError';
    this.state = state;
    this.detail = detail;
    this.extra = extra;
  }
}

// ── 默认参数（来自规范，可按需覆盖）─────────────────────────────────────────
export const DEFAULTS = {
  delayMinSec: 20,           // 相邻"写"动作最小间隔
  delayMaxSec: 60,           // 最大间隔（随机取值）
  roundLimit: 5,             // 单轮打招呼上限（3~5）
  checkEvery: 3,             // 每 N 人做一次轻量状态校验
  settleAfterClickMs: [800, 1800],   // 点击后留渲染时间（随机）
  typeCharDelayMs: [40, 140],        // 逐字输入字符间隔（随机）
  quotaFailStreak: 3,        // 连续失败达此数 → 优先判定权益耗尽
  cmdTimeoutMs: 60000,
};

// ── 基础工具 ────────────────────────────────────────────────────────────────
const rand = (min, max) => min + Math.random() * (max - min);
const randInt = (min, max) => Math.floor(rand(min, max + 1));
export const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** 随机几十秒级延时（核心反风控：节奏不能整齐）。 */
export async function humanDelay(opts = {}) {
  const min = opts.minSec ?? DEFAULTS.delayMinSec;
  const max = opts.maxSec ?? DEFAULTS.delayMaxSec;
  const sec = rand(min, max);
  if (opts.log) opts.log(`⏳ 随机停顿 ${sec.toFixed(1)}s`);
  await sleep(sec * 1000);
  return sec;
}

/** 运行一条 opencli 命令，返回 {ok, stdout, json, stderr}。 */
async function opencli(args, { timeout = DEFAULTS.cmdTimeoutMs } = {}) {
  try {
    const { stdout, stderr } = await pexec('opencli', args, { timeout, maxBuffer: 32 * 1024 * 1024 });
    let json = null;
    try { json = JSON.parse(stdout); } catch { /* 非 JSON 输出 */ }
    return { ok: true, stdout, stderr, json };
  } catch (e) {
    return { ok: false, stdout: e.stdout || '', stderr: e.stderr || String(e), json: null };
  }
}

/** 在页面执行 JS，返回解析后的结果（失败抛错）。 */
export async function evalPage(session, js) {
  const r = await opencli([ 'browser', session, 'eval', js ]);
  if (!r.ok) throw new Error(`eval 失败: ${r.stderr.slice(0, 200)}`);
  // eval 输出可能是 JSON、JSON 字符串、或裸文本
  if (r.json !== null) return r.json;
  const t = r.stdout.trim();
  try { return JSON.parse(t); } catch { return t; }
}

// ── 拟人操作：点击 / 输入 ────────────────────────────────────────────────────
/**
 * 拟人点击：原生 CDP 点击（等价 clickAt），带前置随机延时 + 点击后渲染等待。
 * 点击优先级：browser click(原生) → clickAt → (调用方自行兜底)。绝不默认 DOM .click()。
 * 返回 {clicked:boolean, matches_n}。
 */
export async function humanClick(session, target, opts = {}) {
  await sleep(randInt(200, 700));               // 点击前的"反应时间"
  let r = await opencli([ 'browser', session, 'click', target ]);
  let env = r.json || {};
  if (!env.clicked && opts.fallbackXY) {
    // 退路：CDP 坐标点击
    r = await opencli([ 'browser', session, 'clickAt', String(opts.fallbackXY.x), String(opts.fallbackXY.y) ]);
    env = r.json || {};
  }
  const [a, b] = DEFAULTS.settleAfterClickMs;
  await sleep(randInt(a, b));                    // 点击后留渲染时间
  return { clicked: !!env.clicked, matches_n: env.matches_n };
}

/**
 * 逐字输入（nativeType，逐字符派发键盘事件），不用 fill（瞬时填充像脚本）。
 * 注：opencli `type` 已逐字；此处仅加前后随机延时与可选分段，进一步拟人。
 */
export async function humanType(session, target, text, opts = {}) {
  await sleep(randInt(300, 900));
  const r = await opencli([ 'browser', session, 'type', target, text ]);
  const env = r.json || {};
  await sleep(randInt(400, 1200));
  return { typed: env.typed !== false, text };
}

// ── 风控信号检测 → 熔断 ─────────────────────────────────────────────────────
const RISK_PROBE = `(() => {
  const out = { captcha:false, login:false, anomaly:false, quota:false, hints:[] };
  const url = location.href;
  const bodyText = (document.body && document.body.innerText || '').slice(0, 4000);
  // 登录失效
  if (/login|passport|\\/web\\/user\\/\\?ka=header-login/i.test(url)) { out.login = true; out.hints.push('url=login'); }
  if (/请登录|登录已失效|重新登录|账号在别处登录|被踢下线|账号被冻结/.test(bodyText)) { out.login = true; out.hints.push('text=login'); }
  // 验证码 / 异常验证
  if (/验证码|滑动验证|拖动滑块|安全验证|人机验证|captcha/i.test(bodyText)) { out.captcha = true; out.hints.push('text=captcha'); }
  if (document.querySelector('[class*="captcha"], [class*="verify-slider"], [id*="captcha"], .geetest_panel')) { out.captcha = true; out.hints.push('dom=captcha'); }
  // 权益/额度提示
  if (/沟通次数已用完|剩余沟通次数|沟通额度|开通权益|提升沟通|今日.*沟通.*上限|次数不足/.test(bodyText)) { out.quota = true; out.hints.push('text=quota'); }
  // 频控/异常
  if (/操作过于频繁|请稍后再试|访问异常|系统繁忙/.test(bodyText)) { out.anomaly = true; out.hints.push('text=throttle'); }
  return JSON.stringify(out);
})()`;

/** 检测风控信号。返回 {risk:boolean, captcha, login, quota, anomaly, hints[]}。 */
export async function detectRisk(session) {
  let res;
  try { res = await evalPage(session, RISK_PROBE); }
  catch { return { risk: false, error: 'probe_failed' }; }
  const o = typeof res === 'string' ? JSON.parse(res) : res;
  o.risk = !!(o.captcha || o.login || o.anomaly);   // quota 单独处理（不算"立即熔断"，走暂停）
  return o;
}

/** 检测到风控立即熔断：抛 PausedError，编排层据此停整轮。 */
export async function assertNoRisk(session, log) {
  const r = await detectRisk(session);
  if (r.login)   throw new PausedError(Pause.RISK_DETECTED, '登录态失效/被踢，需重新登录 Boss 招聘端', r);
  if (r.captcha) throw new PausedError(Pause.RISK_DETECTED, '出现验证码/人机验证，已停整轮', r);
  if (r.anomaly) throw new PausedError(Pause.RISK_DETECTED, '页面提示操作频繁/访问异常，已停整轮', r);
  if (r.quota)   throw new PausedError(Pause.QUOTA_EXHAUSTED, '页面提示沟通次数/额度已用尽', r);
  if (log && r.hints?.length) log(`风控探针: ${r.hints.join(',')}`);
  return r;
}

// ── 三次身份校验 ────────────────────────────────────────────────────────────
/**
 * 读取当前选中候选人的标识（选中卡片 id / 右侧面板姓名）。
 * Boss 聊天页：选中项 .geek-item.selected，其 id 形如 _<numericUid>-0。
 */
export async function readSelectedIdentity(session) {
  const js = `(() => {
    const sel = document.querySelector('.geek-item.selected, .geek-item.active');
    const id = sel ? (sel.id || sel.getAttribute('data-id') || '') : '';
    const nameEl = document.querySelector('.base-info-single-container .base-name, .base-info-content .base-name');
    const name = nameEl ? nameEl.textContent.trim() : '';
    return JSON.stringify({ id, name });
  })()`;
  const r = await evalPage(session, js);
  return typeof r === 'string' ? JSON.parse(r) : r;
}

/**
 * 身份校验：当前线程身份是否匹配期望候选人。不匹配 → 抛 WRONG_THREAD。
 * expect: { numericUid?, name? } 至少一项。stage: 'switch'|'before_write'|'before_send' 仅用于日志。
 */
export async function verifyIdentity(session, expect, stage = '') {
  const cur = await readSelectedIdentity(session);
  const idMatch = expect.numericUid ? String(cur.id).includes(String(expect.numericUid)) : null;
  const nameMatch = expect.name ? cur.name && cur.name.includes(expect.name) : null;
  const ok = (idMatch === true) || (idMatch === null && nameMatch === true);
  if (!ok) {
    throw new PausedError(Pause.WRONG_THREAD,
      `身份校验(${stage})失败：当前线程[id=${cur.id} name=${cur.name}] ≠ 目标[${expect.numericUid || expect.name}]，已停止发送防误发`,
      { current: cur, expect });
  }
  return cur;
}

// ── 批量节奏控制器 ──────────────────────────────────────────────────────────
/**
 * 管单轮上限、每 N 人校验、连续失败→权益耗尽诊断。
 * 用法：
 *   const bc = new BatchController({ log });
 *   for (const c of candidates) {
 *     if (!bc.canContinue()) break;          // 到上限停
 *     try { ...处理 c...; bc.success(); }
 *     catch (e) { bc.failure(); throw e; }
 *     await bc.betweenActions(session);       // 随机延时 + 周期校验 + 风控探针
 *   }
 */
export class BatchController {
  constructor(opts = {}) {
    this.limit = opts.roundLimit ?? DEFAULTS.roundLimit;
    this.checkEvery = opts.checkEvery ?? DEFAULTS.checkEvery;
    this.failStreakMax = opts.quotaFailStreak ?? DEFAULTS.quotaFailStreak;
    this.log = opts.log ?? (() => {});
    this.done = 0; this.failStreak = 0; this.successCount = 0;
  }
  canContinue() { return this.done < this.limit; }
  success() { this.done++; this.successCount++; this.failStreak = 0; }
  /** 记一次失败；连续失败达阈值 → 优先判定权益耗尽（关键经验：连续失败优先判定权益耗尽，而非代码问题）。 */
  failure() {
    this.done++; this.failStreak++;
    if (this.failStreak >= this.failStreakMax) {
      throw new PausedError(Pause.QUOTA_EXHAUSTED,
        `连续 ${this.failStreak} 次打招呼失败，优先判定当日沟通权益耗尽（非 selector 问题）。已成功 ${this.successCount} 人，保留进度`,
        { successCount: this.successCount });
    }
  }
  /** 两个候选人之间：随机延时 + 周期风控/状态校验。 */
  async betweenActions(session) {
    await humanDelay({ log: this.log });
    if (this.done % this.checkEvery === 0) {
      this.log(`已处理 ${this.done} 人，做一次风控/状态校验`);
      await assertNoRisk(session, this.log);
    }
  }
  summary() { return { processed: this.done, success: this.successCount, limit: this.limit }; }
}

export default {
  Pause, PausedError, DEFAULTS, sleep, humanDelay, evalPage,
  humanClick, humanType, detectRisk, assertNoRisk,
  readSelectedIdentity, verifyIdentity, BatchController,
};
