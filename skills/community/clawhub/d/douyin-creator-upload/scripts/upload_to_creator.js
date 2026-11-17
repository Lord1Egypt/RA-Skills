#!/usr/bin/env node

'use strict';

const fs = require('fs');
const path = require('path');

const { chromium } = require('playwright-core');

const EXIT = {
  OK: 0,
  UNCAUGHT: 1,
  ARGUMENT: 2,
  PAGE_NOT_FOUND: 3,
  UPLOAD_CONTROL_NOT_FOUND: 4,
  PUBLISH_BUTTON_NOT_FOUND: 5,
  SMS_VERIFICATION_REQUIRED: 10,
};

const DEFAULT_CDP = 'http://127.0.0.1:9222';
const DEFAULT_VISIBILITY = 'self';
const DEFAULT_PUBLISH = true;
const UPLOAD_URL = 'https://creator.douyin.com/creator-micro/content/upload';
const POST_VIDEO_URL_PART = '/content/post/video';
const VISIBILITY_LABELS = {
  public: '公开',
  friend: '好友可见',
  self: '仅自己可见',
};
const DISMISS_TEXTS = ['我知道了', '知道了', '完成'];

function log(prefix, message) {
  console.log(`${prefix}: ${message}`);
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function fail(message, code) {
  log('ERROR', message);
  process.exit(code);
}

function parseBoolean(value, defaultValue) {
  if (value === undefined) {
    return defaultValue;
  }
  const normalized = String(value).trim().toLowerCase();
  if (['true', '1', 'yes', 'y'].includes(normalized)) {
    return true;
  }
  if (['false', '0', 'no', 'n'].includes(normalized)) {
    return false;
  }
  throw new Error(`--publish 仅支持 true/false，收到: ${value}`);
}

function parseArgs(argv) {
  const args = {
    cdp: DEFAULT_CDP,
    visibility: DEFAULT_VISIBILITY,
    publish: DEFAULT_PUBLISH,
    title: '',
  };

  for (let i = 0; i < argv.length; i += 1) {
    const current = argv[i];
    if (!current.startsWith('--')) {
      throw new Error(`无法识别的参数: ${current}`);
    }
    const key = current.slice(2);
    const value = argv[i + 1];
    if (value === undefined || value.startsWith('--')) {
      throw new Error(`参数缺少值: --${key}`);
    }

    if (key === 'file') {
      args.file = value;
    } else if (key === 'visibility') {
      args.visibility = value;
    } else if (key === 'title') {
      args.title = value;
    } else if (key === 'cdp') {
      args.cdp = value;
    } else if (key === 'publish') {
      args.publish = parseBoolean(value, DEFAULT_PUBLISH);
    } else {
      throw new Error(`不支持的参数: --${key}`);
    }

    i += 1;
  }

  if (!args.file) {
    throw new Error('--file 为必填参数');
  }

  const rawFile = String(args.file).trim();
  if (!path.isAbsolute(rawFile)) {
    throw new Error('--file 必须为绝对路径');
  }
  const resolvedFile = path.resolve(rawFile);
  if (!fs.existsSync(resolvedFile)) {
    throw new Error(`视频文件不存在: ${resolvedFile}`);
  }
  if (!fs.statSync(resolvedFile).isFile()) {
    throw new Error(`--file 不是有效文件: ${resolvedFile}`);
  }

  const visibility = String(args.visibility || '').trim().toLowerCase();
  if (!Object.prototype.hasOwnProperty.call(VISIBILITY_LABELS, visibility)) {
    throw new Error('--visibility 仅支持 public / friend / self');
  }

  args.file = resolvedFile;
  args.visibility = visibility;
  args.title = String(args.title || '');
  args.cdp = String(args.cdp || DEFAULT_CDP).trim() || DEFAULT_CDP;
  return args;
}

async function findCreatorPage(browser) {
  for (const context of browser.contexts()) {
    for (const page of context.pages()) {
      const url = page.url();
      if (url.includes('creator.douyin.com')) {
        return page;
      }
    }
  }
  return null;
}

async function ensureUploadPage(page) {
  if (page.url().includes('/content/upload')) {
    log('OK', `当前已在上传页: ${page.url()}`);
    return;
  }
  log('STEP', `跳转到上传页: ${UPLOAD_URL}`);
  await page.bringToFront();
  await page.goto(UPLOAD_URL, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await sleep(6000);
  log('OK', `已进入上传页: ${page.url()}`);
}

async function findUploadInput(page) {
  for (let attempt = 1; attempt <= 3; attempt += 1) {
    log('STEP', `查找上传控件，第 ${attempt} 次`);
    const frames = page.frames();
    for (const frame of frames) {
      try {
        const input = await frame.$('input[type="file"]');
        if (input) {
          log('OK', `已在 frame 中找到上传控件: ${frame.url() || '<empty>'}`);
          return input;
        }
      } catch (error) {
        log('WARN', `扫描 frame 失败，继续尝试: ${error.message}`);
      }
    }
    if (attempt < 3) {
      await sleep(3000);
    }
  }
  return null;
}

async function dismissTips(page) {
  for (const text of DISMISS_TEXTS) {
    const locator = page.getByText(text, { exact: true }).first();
    try {
      if (await locator.isVisible({ timeout: 1000 })) {
        await locator.click({ timeout: 2000 });
        log('OK', `已关闭提示弹窗: ${text}`);
        await sleep(500);
      }
    } catch (_error) {
      // ignore
    }
  }
}

async function fillTitle(page, title) {
  if (!title) {
    return;
  }

  log('STEP', '填写作品描述');
  const editor = page.locator('[contenteditable="true"]').first();
  await editor.waitFor({ state: 'visible', timeout: 20000 });
  await editor.click({ timeout: 5000 });
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A');
  await page.keyboard.press('Backspace');
  await editor.fill(title);
  log('OK', '作品描述已填写');
}

async function setVisibility(page, visibility) {
  const label = VISIBILITY_LABELS[visibility];
  log('STEP', `设置可见性: ${label}`);

  const target = page.getByText(label, { exact: true }).first();
  await target.waitFor({ state: 'visible', timeout: 20000 });
  await target.click({ timeout: 5000 });
  log('OK', `可见性已设置为: ${label}`);
}

async function clickPublish(page) {
  log('STEP', '查找并点击发布按钮');
  const button = page.getByRole('button', { name: '发布', exact: true }).first();
  try {
    await button.waitFor({ state: 'visible', timeout: 10000 });
  } catch (_error) {
    return false;
  }
  await button.click({ timeout: 5000 });
  log('OK', '已点击发布按钮');
  return true;
}

async function detectSmsVerification(page) {
  const texts = ['短信验证码', '接收短信验证码'];
  for (const frame of page.frames()) {
    for (const text of texts) {
      try {
        const locator = frame.getByText(text, { exact: false }).first();
        if (await locator.isVisible({ timeout: 1000 })) {
          return true;
        }
      } catch (_error) {
        // ignore
      }
    }
  }
  return false;
}

async function triggerSmsCode(page) {
  for (const frame of page.frames()) {
    try {
      const cooldown = frame.locator('text=/\\d+秒后重试/').first();
      if (await cooldown.isVisible({ timeout: 1000 })) {
        const text = (await cooldown.textContent()) || '验证码已发送，当前处于倒计时冷却';
        log('OK', `验证码已发送，无需重复点击: ${text.trim()}`);
        return;
      }
    } catch (_error) {
      // ignore
    }

    try {
      const getCodeBtn = await frame.$('text=获取验证码');
      if (getCodeBtn) {
        await getCodeBtn.click();
        await sleep(1500);
        log('OK', '已自动点击「获取验证码」，短信已下发到用户手机');
        return;
      }
    } catch (error) {
      log('WARN', `点击「获取验证码」失败，继续尝试其他 frame: ${error.message}`);
    }
  }

  log('WARN', '未找到「获取验证码」按钮，请人工点击');
}

async function main() {
  let browser;
  const args = parseArgs(process.argv.slice(2));

  log('STEP', `连接 Chrome CDP: ${args.cdp}`);
  browser = await chromium.connectOverCDP({ endpointURL: args.cdp });
  log('OK', 'CDP 连接成功');

  const page = await findCreatorPage(browser);
  if (!page) {
    fail('未找到 URL 包含 creator.douyin.com 的已登录页面', EXIT.PAGE_NOT_FOUND);
  }

  log('OK', `已找到创作者中心页面: ${page.url()}`);
  await ensureUploadPage(page);

  const uploadInput = await findUploadInput(page);
  if (!uploadInput) {
    fail('未找到 iframe 内上传控件 input[type="file"]', EXIT.UPLOAD_CONTROL_NOT_FOUND);
  }

  log('STEP', `开始上传本地视频: ${args.file}`);
  await uploadInput.setInputFiles(args.file);
  log('OK', '文件已写入上传控件，等待进入发布页');

  await page.waitForFunction(
    (urlPart) => window.location.href.includes(urlPart),
    POST_VIDEO_URL_PART,
    { timeout: 120000 }
  );
  log('OK', `页面已跳转到发布页: ${page.url()}`);

  await dismissTips(page);
  await fillTitle(page, args.title);
  await setVisibility(page, args.visibility);

  if (!args.publish) {
    log('OK', '已完成上传与信息填写，按参数要求不执行发布');
    return EXIT.OK;
  }

  const publishFound = await clickPublish(page);
  if (!publishFound) {
    fail('未找到“发布”按钮', EXIT.PUBLISH_BUTTON_NOT_FOUND);
  }

  await sleep(3000);
  if (await detectSmsVerification(page)) {
    await triggerSmsCode(page);
    log('NEED_SMS', '发布触发短信验证码，请查看手机 6 位验证码并人工继续，脚本不会代填验证码');
    return EXIT.SMS_VERIFICATION_REQUIRED;
  }

  log('OK', '发布动作已提交，未检测到短信验证码');
  return EXIT.OK;
}

process.on('unhandledRejection', (error) => {
  log('ERROR', `未处理的 Promise 异常: ${error && error.stack ? error.stack : error}`);
  process.exit(EXIT.UNCAUGHT);
});

(async () => {
  try {
    const exitCode = await main();
    process.exit(exitCode);
  } catch (error) {
    if (error && /--file|--visibility|--publish|参数|文件不存在|不是有效文件/.test(String(error.message || error))) {
      log('ERROR', String(error.message || error));
      process.exit(EXIT.ARGUMENT);
    }
    log('ERROR', error && error.stack ? error.stack : String(error));
    process.exit(EXIT.UNCAUGHT);
  }
})();
