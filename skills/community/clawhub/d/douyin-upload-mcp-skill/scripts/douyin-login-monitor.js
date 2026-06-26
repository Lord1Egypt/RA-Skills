#!/usr/bin/env node
import { mkdirSync, appendFileSync, writeFileSync, readFileSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { homedir } from 'node:os';
import { createDouyinSession, disconnect } from '../src/index.js';
import config from '../src/config.js';
import { sendFeishuText, sendFeishuImage, resolveFeishuConfig } from './feishu-client.js';

const STATE_DIR = process.env.DOUYIN_MONITOR_STATE_DIR || join(homedir(), '.openclaw', 'workspace', 'douyin-ops');
const LOG_PATH = join(STATE_DIR, 'login-monitor.jsonl');
const __dirname = dirname(fileURLToPath(import.meta.url));

function usage() {
  console.error(`Usage:
  node scripts/douyin-login-monitor.js check [--notify] [--send-qr auto|ask|off]
  node scripts/douyin-login-monitor.js fresh-qr [--send] [--customer-ready] [--no-reload] [--max-qr-attempts 3]
  node scripts/douyin-login-monitor.js stability --rounds 10 [--interval-ms 1000]
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (!next || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function nowIso() {
  return new Date().toISOString();
}

function logEvent(event) {
  try {
    mkdirSync(STATE_DIR, { recursive: true });
    appendFileSync(LOG_PATH, `${JSON.stringify({ ts: nowIso(), ...event })}\n`);
  } catch (err) {
    console.error(`[login-monitor] log skipped: ${err.message}`);
  }
}

function printJson(payload) {
  console.log(JSON.stringify(payload, null, 2));
}

async function screenshot(ops, prefix) {
  mkdirSync(config.outputDir, { recursive: true });
  const path = join(config.outputDir, `${prefix}_${Date.now()}.png`);
  const page = ops.operator?.page;
  if (page) {
    const viewport = page.viewport();
    if (!viewport?.width || !viewport?.height) {
      await page.setViewport({ width: 1280, height: 900 }).catch(() => {});
      await new Promise((resolve) => setTimeout(resolve, 300));
    }
  }
  try {
    await ops.screenshot({ path, fullPage: true });
    return path;
  } catch (err) {
    await ops.screenshot({ path, fullPage: false });
    return path;
  }
}

function adviceFor(classification) {
  switch (classification.kind) {
    case 'logged_in':
      return '已登录，无需客户操作。';
    case 'qrcode':
      return '请用抖音 App 扫码登录；二维码通常很快过期，准备扫码后再索取最新二维码。';
    case 'sms_verification':
      return '当前进入了验证码验证分支；默认优先扫码登录，只有扫码后页面明确切到验证码流程时才继续走短信验证。';
    case 'sms_code_input':
      return '请把 6 位短信验证码发给机器人，不要发送其他文字。';
    case 'captcha':
      return '页面出现安全/机器人验证；请按截图手动完成验证，完成后回复“已完成”。';
    case 'device_verification':
      return '抖音要求使用手机或已登录设备验证；默认先走扫码，只有扫码后页面明确切到短信验证码流程时才请求验证码。';
    case 'risk':
      return '抖音触发风控或登录环境异常；建议先人工在当前浏览器完成登录/验证，必要时换网络或稍后重试。';
    case 'upload_page_unavailable':
      return '创作者平台页面没有加载完整；请稍后重试，或刷新页面后再检查。';
    case 'page_loading':
      return '页面仍在加载，稍后自动重试。';
    default:
      return '请查看截图，根据页面提示完成最少必要操作；完成后回复“已完成”。';
  }
}

async function classifyPage(ops, login) {
  const page = ops.operator.page;
  const detail = await page.evaluate(() => {
    const text = document.body?.innerText || '';
    const has = (pattern) => pattern.test(text);
    const visible = (el) => {
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const secondVerify = [...document.querySelectorAll('[class*="second_verify"], [class*="uc_verification_component"]')]
      .some((el) => visible(el) && /身份验证|为保障账号安全|接收短信验证码|发送短信验证|请输入验证码/.test(el.textContent || ''));
    const qr = document.querySelector('img[aria-label="二维码"]');
    const secondVerifySmsInput = [...document.querySelectorAll('article[class*="uc_verification_component_layout"] #button-input[placeholder*="验证码"], div[class*="second_verify"] input#button-input[placeholder*="验证码"]')]
      .some((el) => visible(el) && Boolean(el.closest('[class*="second_verify"], article[class*="uc_verification_component_layout"]')));
    return {
      url: location.href,
      title: document.title,
      bodyText: text.slice(0, 3000),
      qrcode: Boolean(qr && visible(qr) && !secondVerify),
      secondVerify,
      smsInput: secondVerifySmsInput,
      hasSmsVerification: (/身份验证|为保障账号安全|手机验证/.test(text) && has(/接收短信验证码|发送短信验证|短信验证码|获取验证码|重新获取|重新发送|发送验证码/)),
      hasCaptcha: has(/安全验证|拖动滑块|滑块|机器人|真人验证|验证你不是机器人|请完成验证|拼图|行为验证|按住滑块/),
      hasDeviceVerification: has(/手机验证|扫码验证|已登录账号的设备|已登录设备|用手机.*验证|手机.*确认|抖音 App.*扫码验证|抖音APP.*扫码验证|为确保.*本人操作|确保为本人操作|使用.*设备扫码|打开.*抖音.*扫码/),
      hasRisk: has(/环境异常|操作频繁|访问过于频繁|账号存在风险|登录失败|暂时无法登录|系统繁忙|网络异常/),
      hasCreatorHome: location.href.includes('creator.douyin.com') && (has(/创作者|发布|内容管理|高清发布/) || !!document.querySelector('[class*="avatar"]')),
    };
  });

  let kind = 'unknown';
  if (login.phase === 'page_loading') kind = 'page_loading';
  else if (login.loggedIn && detail.hasCreatorHome) kind = 'logged_in';
  else if (login.loggedIn) kind = 'page_loading';
  else if (detail.hasCaptcha) kind = 'captcha';
  else if (detail.hasRisk) kind = 'risk';
  else if (login.phase === 'qrcode' || detail.qrcode) kind = 'qrcode';
  else if (login.phase === 'sms_code_input' || detail.smsInput) kind = 'sms_code_input';
  else if (login.phase === 'sms_verification' || detail.hasSmsVerification) kind = 'sms_verification';
  else if (detail.hasDeviceVerification) kind = 'device_verification';
  else if (detail.url.includes('creator.douyin.com') && !detail.hasCreatorHome) kind = 'upload_page_unavailable';

  return {
    kind,
    loggedIn: Boolean(login.loggedIn),
    phase: login.phase,
    qrcodePath: login.qrcodePath,
    message: login.message,
    url: detail.url,
    title: detail.title,
    textSample: detail.bodyText.replace(/\s+/g, ' ').slice(0, 500),
  };
}

function buildCustomerMessage(classification, mode) {
  const lines = [];
  if (classification.kind === 'qrcode' && mode === 'ask') {
    lines.push('抖音需要重新登录。');
    lines.push('请在电脑端打开飞书，用手机抖音 App 准备扫码。');
    lines.push('准备好后回复：发送二维码');
  } else if (classification.kind === 'qrcode' && mode === 'off') {
    lines.push('抖音仍未登录，请先完成扫码。');
  } else if (classification.kind === 'qrcode') {
    lines.push('抖音需要重新登录，请用抖音 App 扫码。');
  } else if (classification.kind === 'captcha') {
    lines.push('抖音出现安全验证，请按截图完成。');
    lines.push('完成后回复：已完成');
  } else if (classification.kind === 'device_verification') {
    lines.push('抖音要求手机/原设备验证。');
    lines.push('收到短信请直接回复 6 位验证码；如需手机确认，请确认后回复：已登录');
  } else if (classification.kind === 'sms_verification' || classification.kind === 'sms_code_input') {
    lines.push(classification.kind === 'sms_code_input'
      ? '抖音短信验证码已发送，请直接回复 6 位验证码。'
      : '抖音需要短信验证，请稍等验证码短信。');
  } else if (classification.kind === 'page_loading') {
    lines.push('抖音页面还在加载，我会稍后重试。');
  } else if (classification.kind !== 'logged_in') {
    lines.push('抖音需要人工确认，请按截图处理。');
    lines.push('完成后回复：已完成');
  }

  return lines.join('\n');
}

async function notify(classification, opts = {}) {
  const mode = opts.sendQr || 'ask';
  const feishu = resolveFeishuConfig();
  const actions = [];

  const text = buildCustomerMessage(classification, mode);
  if (text.trim()) actions.push(await sendFeishuText(text, feishu));

  const shouldSendScreenshot = classification.screenshotPath
    && !(classification.kind === 'qrcode' && (mode === 'ask' || mode === 'off'));
  if (shouldSendScreenshot) {
    actions.push(await sendFeishuImage(classification.screenshotPath, feishu));
  }
  if (classification.kind === 'qrcode' && classification.qrcodePath && mode === 'auto' && classification.reloadBeforeCapture) {
    actions.push(await sendFeishuImage(classification.qrcodePath, feishu));
  }

  return actions;
}

async function inspectOnce(opts = {}) {
  const start = Date.now();
  const { ops } = await createDouyinSession();
  try {
    const login = await ops.checkLogin({ smsCode: opts.smsCode });
    const classification = await classifyPage(ops, login);
    if (classification.kind !== 'logged_in') {
      classification.screenshotPath = await screenshot(ops, classification.kind);
    }
    classification.elapsedMs = Date.now() - start;
    classification.advice = adviceFor(classification);
    logEvent({ action: 'check', result: classification });
    return classification;
  } finally {
    disconnect();
  }
}

async function freshQr(opts = {}) {
  const start = Date.now();
  if (opts.send && !opts.customerReady) {
    const message = [
      '请在电脑端打开飞书，用手机抖音 App 准备扫码。',
      '准备好后回复：发送二维码',
    ].join('\n');
    const notify = [await sendFeishuText(message)];
    const result = {
      kind: 'qrcode_waiting_customer_ready',
      ok: false,
      sentQr: false,
      customerReady: false,
      advice: '等待客户在电脑端打开飞书并回复“发送二维码”。',
      notify,
      elapsedMs: Date.now() - start,
    };
    logEvent({ action: 'fresh-qr-blocked-unconfirmed', result });
    return result;
  }

  const { ops } = await createDouyinSession();
  try {
    let reloadBeforeCapture = opts.reload === true;
    let refreshResult = { refreshed: false };
    const maxQrAttempts = Number(opts.maxQrAttempts || 3);
    let login;
    let classification;
    const qrAttempts = [];
    for (let attempt = 1; attempt <= maxQrAttempts; attempt += 1) {
      refreshResult = opts.reload === true
        ? await refreshBeforeQrCapture(ops, { attempt })
        : await refreshExpiredQrIfNeeded(ops, { force: true, attempt });

      login = await ops.checkLogin();
      classification = await classifyPage(ops, login);
      const qrValidation = classification.qrcodePath
        ? detectQrImage(classification.qrcodePath)
        : { ok: false, reason: 'no_qrcode_path' };
      const qrcodeHash = classification.qrcodePath ? hashFile(classification.qrcodePath) : null;
      qrAttempts.push({ attempt, qrcodePath: classification.qrcodePath, qrcodeHash, qrValidation, refreshResult });
      classification.qrValidation = qrValidation;
      classification.qrAttempts = qrAttempts;
      if (classification.kind !== 'qrcode' || qrValidation.ok) break;
    }
    if (classification.kind !== 'qrcode') {
      classification.screenshotPath = await screenshot(ops, `fresh_${classification.kind}`);
    }
    classification.elapsedMs = Date.now() - start;
    classification.advice = adviceFor(classification);
    classification.reloadBeforeCapture = reloadBeforeCapture;
    classification.refreshResult = refreshResult;

    const sendActions = [];
    if (opts.send && classification.qrcodePath && classification.qrValidation?.ok && !classification.qrValidation?.expired) {
      sendActions.push(await sendFeishuText('请立即用手机抖音 App 扫码。\n注意：请在电脑端飞书查看二维码，不要在手机端保存图片后扫码。\n扫码确认后回复：已登录\n如果二维码过期，请回复：已过期'));
      sendActions.push(await sendFeishuImage(classification.qrcodePath));
    } else if (opts.send) {
      sendActions.push(await sendFeishuText([
        '暂时没有拿到可用二维码。',
        `原因：${classification.qrValidation?.reason || classification.kind || 'unknown'}`,
        '请稍后回复：发送二维码',
      ].join('\n')));
    }
    classification.notify = sendActions;
    logEvent({ action: 'fresh-qr', result: classification });
    return classification;
  } finally {
    disconnect();
  }
}

async function runStability(args) {
  const rounds = Number(args.rounds || 10);
  const intervalMs = Number(args.intervalMs || 1000);
  const results = [];
  for (let i = 0; i < rounds; i += 1) {
    const result = await inspectOnce();
    results.push(result);
    if (i + 1 < rounds) await new Promise((r) => setTimeout(r, intervalMs));
  }

  const summary = {
    rounds,
    ok: results.every((r) => r.kind !== 'unknown'),
    phases: results.reduce((acc, r) => {
      acc[r.kind] = (acc[r.kind] || 0) + 1;
      return acc;
    }, {}),
    elapsedMs: {
      min: Math.min(...results.map((r) => r.elapsedMs)),
      max: Math.max(...results.map((r) => r.elapsedMs)),
      avg: Math.round(results.reduce((sum, r) => sum + r.elapsedMs, 0) / results.length),
    },
    qrcodePaths: results.map((r) => r.qrcodePath).filter(Boolean),
  };
  const reportPath = join(STATE_DIR, `stability_${Date.now()}.json`);
  writeFileSync(reportPath, JSON.stringify({ summary, results }, null, 2));
  return { summary, reportPath };
}

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);
  if (!command || args.help) {
    usage();
    process.exit(command ? 0 : 2);
  }

  if (command === 'check') {
    const result = await inspectOnce(args);
    if (args.notify) {
      const sendQr = args.sendQr || 'ask';
      if (sendQr === 'auto' && result.kind === 'qrcode') {
        result.notify = await notify(result, { sendQr: 'ask' });
        result.qrSend = await freshQr({ send: true, reload: false });
      } else {
        result.notify = await notify(result, { sendQr });
      }
    }
    printJson(result);
    return;
  }

  if (command === 'fresh-qr') {
    printJson(await freshQr({
      send: Boolean(args.send),
      customerReady: Boolean(args.customerReady),
      reload: !args.noReload,
      maxQrAttempts: args.maxQrAttempts,
    }));
    return;
  }

  if (command === 'stability') {
    printJson(await runStability(args));
    return;
  }

  usage();
  process.exit(2);
}

main().catch((err) => {
  logEvent({ action: 'error', error: err.message, stack: err.stack });
  printJson({ ok: false, error: err.message, stack: err.stack });
  disconnect();
  process.exit(1);
});

function detectQrImage(path) {
  const python = process.env.DOUYIN_QR_PYTHON
    || (existsSync('/opt/python-env/bin/python3') ? '/opt/python-env/bin/python3' : 'python3');
  const result = spawnSync(python, [join(__dirname, 'detect-qr-image.py'), path], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  const output = result.stdout.trim();
  try {
    const parsed = JSON.parse(output);
    if (result.stderr?.trim()) parsed.stderr = result.stderr.trim().slice(0, 500);
    if (typeof result.status === 'number') parsed.status = result.status;
    return parsed;
  } catch {
    return {
      ok: false,
      reason: 'detector_output_parse_failed',
      stdout: output,
      stderr: result.stderr?.trim().slice(0, 1000) || '',
      status: result.status,
    };
  }
}

function hashFile(path) {
  try {
    return createHash('sha256').update(readFileSync(path)).digest('hex').slice(0, 16);
  } catch {
    return null;
  }
}

async function refreshBeforeQrCapture(ops, opts = {}) {
  const page = ops.operator.page;
  const startedAt = Date.now();
  const before = await getQrDomState(page);
  const currentUrl = page.url();
  const pageText = await page.evaluate(() => document.body?.innerText || '').catch(() => '');
  const inPublishEditor = /creator-micro\/content\/post\/video/.test(currentUrl);
  const publishVerifyQr = inPublishEditor && /使用原设备扫码|请使用「?抖音 ?APP」?扫码验证|去使用短信验证/.test(pageText);
  let action = 'reload';
  let refresh;

  if (publishVerifyQr) {
    await settleQrImage(page);
    const after = await getQrDomState(page);
    return {
      refreshed: false,
      confirmed: Boolean(after.found && after.complete && after.width >= 180 && after.height >= 180),
      action: 'skip_reload_publish_verify_qr',
      attempt: opts.attempt,
      elapsedMs: Date.now() - startedAt,
      reload: { ok: true, skipped: true, reason: 'publish_verify_qr' },
      before,
      after,
      surface: { ok: true, skipped: true, reason: 'publish_verify_qr' },
    };
  }

  if (!currentUrl.includes('creator.douyin.com')) {
    action = 'navigate';
    refresh = await ops.navigateTo(config.douyinUrl, { timeout: 30000 });
  } else {
    refresh = await ops.reloadPage({ timeout: 30000 });
    if (!refresh.ok) {
      action = 'navigate_after_reload_failed';
      refresh = await ops.navigateTo(config.douyinUrl, { timeout: 30000 });
    }
  }

  const surface = await waitForLoginSurface(page, { timeout: 12000 });
  const after = await getQrDomState(page);
  await settleQrImage(page);

  return {
    refreshed: Boolean(refresh?.ok),
    confirmed: Boolean(refresh?.ok && surface.ok && (!after.found || (after.complete && after.width >= 180 && after.height >= 180))),
    action,
    attempt: opts.attempt,
    elapsedMs: Date.now() - startedAt,
    reload: refresh,
    before,
    after,
    surface,
  };
}

async function getQrDomState(page) {
  return page.evaluate(() => {
    const summarizeSrc = (src) => {
      if (!src) return { length: 0, prefix: '' };
      return {
        length: src.length,
        prefix: src.slice(0, 32),
        changedKey: `${src.length}:${src.slice(-32)}`,
      };
    };
    const text = document.body?.innerText || '';
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const img = document.querySelector('img[aria-label="二维码"]')
      || [...document.querySelectorAll('img.uc-ui-verify_qr-verify_main_qr-img, img')]
        .find((el) => visible(el) && Boolean(el.closest('.uc-ui-verify_qr-verify_main_qr, .second-verify-panel, article.uc-ui-verify_qr-verify')));
    if (!img) {
      return {
        found: false,
        expiredText: /二维码失效|点击刷新/.test(text),
        url: location.href,
        title: document.title,
      };
    }
    const rect = img.getBoundingClientRect();
    const src = img.currentSrc || img.src || '';
    return {
      found: true,
      expiredText: /二维码失效|点击刷新/.test(text),
      src: summarizeSrc(src),
      complete: Boolean(img.complete),
      naturalWidth: img.naturalWidth || 0,
      naturalHeight: img.naturalHeight || 0,
      width: Math.round(rect.width),
      height: Math.round(rect.height),
      url: location.href,
      title: document.title,
    };
  }).catch((err) => ({ found: false, error: err.message }));
}

async function waitForLoginSurface(page, opts = {}) {
  const timeout = opts.timeout || 12000;
  try {
    await page.waitForFunction(() => {
      const text = document.body?.innerText || '';
      const qr = document.querySelector('img[aria-label="二维码"]')
        || document.querySelector('img.uc-ui-verify_qr-verify_main_qr-img');
      const isSecondVerify = /身份验证|为保障账号安全|接收短信验证码|发送短信验证|手机刷脸验证|验证登录密码/.test(text);
      const sms = isSecondVerify
        ? document.querySelector('article[class*="uc_verification_component_layout"] #button-input[placeholder="请输入验证码"], div[class*="second_verify"] input#button-input[placeholder="请输入验证码"]')
        : null;
      const avatar = document.querySelector('[class*="avatar"], img[class*="avatar"]');
      const captcha = /安全验证|拖动滑块|滑块|机器人|真人验证|验证你不是机器人|请完成验证|拼图|行为验证|按住滑块/.test(text);
      const deviceVerification = /手机验证|扫码验证|已登录账号的设备|已登录设备|用手机.*验证|手机.*确认|抖音 App.*扫码验证|抖音APP.*扫码验证|为确保.*本人操作|确保为本人操作|使用.*设备扫码|打开.*抖音.*扫码/.test(text);
      const risk = /环境异常|操作频繁|访问过于频繁|账号存在风险|登录失败|暂时无法登录|系统繁忙|网络异常/.test(text);
      if (qr) {
        const rect = qr.getBoundingClientRect();
        return rect.width >= 180 && rect.height >= 180 && qr.complete;
      }
      return Boolean(sms || avatar || captcha || deviceVerification || risk);
    }, { timeout, polling: 250 });
    return { ok: true };
  } catch (err) {
    return { ok: false, error: 'wait_login_surface_timeout', detail: err.message };
  }
}

async function settleQrImage(page) {
  await page.evaluate(() => new Promise((resolve) => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  await new Promise((r) => setTimeout(r, 700));
}

async function refreshExpiredQrIfNeeded(ops, opts = {}) {
  const page = ops.operator.page;
  const before = await getQrDomState(page);
  const expired = await page.evaluate(() => {
    const text = document.body?.innerText || '';
    return /二维码失效|点击刷新/.test(text);
  });
  if (!expired && !opts.force) return { refreshed: false };

  const overlayLoc = await page.evaluate(() => {
    const visible = (el) => {
      if (!el) return false;
      const rect = el.getBoundingClientRect();
      const style = getComputedStyle(el);
      return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
    };
    const publishMask = document.querySelector('.uc-ui-verify_qr-verify_main_qr-mask')
      || document.querySelector('.uc-ui-verify_qr-verify_main_qr-mask_icon.refresh')
      || document.querySelector('.uc-ui-verify_qr-verify_main_qr');
    const img = publishMask && visible(publishMask)
      ? publishMask
      : (document.querySelector('img[aria-label="二维码"]')
        || [...document.querySelectorAll('img.uc-ui-verify_qr-verify_main_qr-img, img')]
          .find((el) => visible(el) && Boolean(el.closest('.uc-ui-verify_qr-verify_main_qr, .second-verify-panel, article.uc-ui-verify_qr-verify'))));
    if (!img) return null;
    const rect = img.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) return null;
    return {
      x: rect.x + rect.width / 2,
      y: rect.y + rect.height / 2,
      width: rect.width,
      height: rect.height,
    };
  });

  if (overlayLoc) {
    await page.mouse.click(overlayLoc.x, overlayLoc.y);
    await new Promise((r) => setTimeout(r, 1800));
    const changed = await waitForQrChanged(page, before, { timeout: 5000 });
    await settleQrImage(page);
    const after = await getQrDomState(page);
    const stillExpired = after.expiredText;
    if (!stillExpired && changed.ok) return { refreshed: true, clicked: true, target: 'qr_center', before, after, changed };
    if (opts.force) {
      const fallback = await refreshBeforeQrCapture(ops, { attempt: opts.attempt, reason: 'qr_center_no_change' });
      return { ...fallback, clicked: true, target: 'page_reload_after_qr_center_no_change', before, after, changed };
    }
  }

  const loc = await page.evaluate(() => {
    const candidates = [...document.querySelectorAll('button, div, span, p, a')]
      .filter((el) => {
        const text = el.textContent || '';
        if (!/点击刷新|刷新/.test(text)) return false;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
      });
    const target = candidates[0];
    if (!target) return null;
    const rect = target.getBoundingClientRect();
    return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
  });

  if (loc) {
    await page.mouse.click(loc.x, loc.y);
    await new Promise((r) => setTimeout(r, 1800));
    const changed = await waitForQrChanged(page, before, { timeout: 5000 });
    await settleQrImage(page);
    const after = await getQrDomState(page);
    const stillExpired = after.expiredText;
    if (!stillExpired && changed.ok) {
      return { refreshed: true, clicked: true, target: 'text_refresh', expired: stillExpired, before, after, changed };
    }
    if (opts.force) {
      const fallback = await refreshBeforeQrCapture(ops, { attempt: opts.attempt, reason: 'text_refresh_no_change' });
      return { ...fallback, clicked: true, target: 'page_reload_after_text_refresh_no_change', expired: stillExpired, before, after, changed };
    }
    return { refreshed: false, clicked: true, target: 'text_refresh', expired: stillExpired, before, after, changed };
  }

  return { refreshed: false, clicked: false, target: 'no_page_reload_fallback', expired: true, before };
}

async function waitForQrChanged(page, before, opts = {}) {
  const timeout = opts.timeout || 5000;
  const beforeKey = before?.src?.changedKey || '';
  try {
    await page.waitForFunction((oldKey) => {
      const text = document.body?.innerText || '';
      if (/二维码失效|点击刷新/.test(text)) return false;
      const visible = (el) => {
        if (!el) return false;
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        return rect.width > 0 && rect.height > 0 && style.display !== 'none' && style.visibility !== 'hidden';
      };
      const img = document.querySelector('img[aria-label="二维码"]')
        || [...document.querySelectorAll('img.uc-ui-verify_qr-verify_main_qr-img, img')]
          .find((el) => visible(el) && Boolean(el.closest('.uc-ui-verify_qr-verify_main_qr, .second-verify-panel, article.uc-ui-verify_qr-verify')));
      if (!img || !visible(img) || !img.complete) return false;
      const src = img.currentSrc || img.src || '';
      const key = `${src.length}:${src.slice(-32)}`;
      return !oldKey || key !== oldKey;
    }, { timeout, polling: 250 }, beforeKey);
    return { ok: true };
  } catch (err) {
    return { ok: false, error: 'qr_change_timeout', detail: err.message };
  }
}
