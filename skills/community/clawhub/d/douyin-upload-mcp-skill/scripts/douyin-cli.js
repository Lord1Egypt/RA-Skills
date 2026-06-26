#!/usr/bin/env node
import { createDouyinSession, disconnect } from '../src/index.js';

function usage() {
  console.error(`Usage:
  node scripts/douyin-cli.js check-login [--sms-code 123456]
  node scripts/douyin-cli.js probe
  node scripts/douyin-cli.js screenshot
  node scripts/douyin-cli.js publish-state [--title 标题]
  node scripts/douyin-cli.js verify-published [--title 标题]
  node scripts/douyin-cli.js request-publish-sms [--allow-resend]
  node scripts/douyin-cli.js submit-sms-code --sms-code 123456
  node scripts/douyin-cli.js publish-current-draft [--title 标题]
  node scripts/douyin-cli.js publish-video --file /abs/video.mp4 [--title 标题] [--description 简介] [--topics 话题1,话题2] [--cover-image /abs/cover.png] [--timeout 1800000] [--assistant-timeout 600000] [--fresh]
`);
}

function parseArgs(argv) {
  const args = {};
  for (let i = 0; i < argv.length; i += 1) {
    const item = argv[i];
    if (!item.startsWith('--')) continue;
    const key = item.slice(2).replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) {
      args[key] = true;
    } else {
      args[key] = next;
      i += 1;
    }
  }
  return args;
}

function printJson(payload) {
  console.log(JSON.stringify(payload, null, 2));
}

async function withSession(fn) {
  const { ops } = await createDouyinSession();
  try {
    await fn(ops);
  } finally {
    disconnect();
  }
}

async function main() {
  const [command, ...rest] = process.argv.slice(2);
  const args = parseArgs(rest);

  if (!command || args.help) {
    usage();
    process.exit(command ? 0 : 2);
  }

  if (command === 'check-login') {
    await withSession(async (ops) => {
      const result = await ops.checkLogin({ smsCode: args.smsCode });
      printJson({
        ok: result.ok,
        loggedIn: result.loggedIn,
        phase: result.phase,
        qrcodePath: result.qrcodePath,
        message: result.message,
        clicked: result.clicked,
      });
    });
    return;
  }

  if (command === 'probe') {
    await withSession(async (ops) => {
      printJson(await ops.probe());
    });
    return;
  }

  if (command === 'screenshot') {
    await withSession(async (ops) => {
      const { mkdirSync, writeFileSync } = await import('node:fs');
      const { join } = await import('node:path');
      const config = (await import('../src/config.js')).default;
      mkdirSync(config.outputDir, { recursive: true });
      const filePath = join(config.outputDir, `douyin-cli-screenshot_${Date.now()}.png`);
      const buffer = await ops.screenshot({ fullPage: true });
      writeFileSync(filePath, buffer);
      printJson({ ok: true, filePath });
    });
    return;
  }

  if (command === 'publish-state') {
    await withSession(async (ops) => {
      const login = await ops.checkLogin();
      let verification = null;
      let assistant = null;
      let currentPage = null;
      try {
        verification = await ops.getPublishVerificationState();
      } catch (err) {
        verification = { found: false, error: err.message };
      }
      try {
        assistant = await ops.getPublishAssistantState();
      } catch (err) {
        assistant = { ready: false, error: err.message };
      }
      try {
        currentPage = await ops.getCurrentPageSummary();
      } catch (err) {
        currentPage = { error: err.message };
      }

      let manage = null;
      const shouldVerifyManage = Boolean(args.verifyManage || args.verifyPublished || args.manage || args.title);
      if (shouldVerifyManage && login.loggedIn && !verification?.found) {
        manage = await ops.verifyPublished({ title: args.title, waitMs: Number(args.waitMs || 2500) });
      }

      const text = `${currentPage?.textSample || ''} ${manage?.textSample || ''}`;
      const hasLoadedManageText = !/加载中，请稍候/.test(text);
      const published = args.title
        ? Boolean(manage?.found)
        : Boolean(manage?.found || (hasLoadedManageText && /发布成功|审核中|已发布/.test(text)));

      printJson({
        ok: true,
        loggedIn: Boolean(login.loggedIn || verification?.found),
        phase: verification?.found ? 'publish_verification' : login.phase,
        published,
        title: args.title || '',
        verification,
        assistant,
        currentPage,
        manage,
      });
    });
    return;
  }

  if (command === 'verify-published') {
    await withSession(async (ops) => {
      printJson(await ops.verifyPublished({ title: args.title }));
    });
    return;
  }

  if (command === 'request-publish-sms') {
    await withSession(async (ops) => {
      const result = await ops.requestPublishSmsCode({ allowResend: Boolean(args.allowResend) });
      printJson(result);
      if (!result.ok) process.exitCode = 1;
    });
    return;
  }

  if (command === 'submit-sms-code') {
    const code = String(args.smsCode || args.code || '').trim();
    if (!/^\d{6}$/.test(code)) {
      printJson({ ok: false, error: 'sms_code_required' });
      process.exitCode = 2;
      return;
    }
    await withSession(async (ops) => {
      const result = await ops.submitVisibleSmsCode(code);
      printJson(result);
      if (!result.ok) process.exitCode = 1;
    });
    return;
  }

  if (command === 'publish-video') {
    if (!args.file) {
      usage();
      process.exit(2);
    }

    await withSession(async (ops) => {
      const login = await ops.checkLogin();
      if (!login.loggedIn) {
        printJson({
          ok: false,
          needsUserAction: true,
          action: login.phase,
          qrcodePath: login.qrcodePath,
          message: login.message || `未登录，当前阶段: ${login.phase}`,
        });
        process.exitCode = 3;
        return;
      }

      const timeout = args.timeout ? Number(args.timeout) : undefined;
      const assistantTimeout = args.assistantTimeout ? Number(args.assistantTimeout) : undefined;
      const result = await ops.publishVideo(args.file, {
        title: args.title,
        description: args.description,
        topics: args.topics,
        coverImagePath: args.coverImage,
        timeout,
        assistantTimeout,
        freshUpload: Boolean(args.fresh),
      });

      printJson({
        ok: result.ok,
        type: result.type,
        file: result.file,
        elapsed: result.elapsed,
        coverSelected: result.coverSelected,
        cover: result.cover,
        publish: result.publish,
        error: result.error,
        detail: result.detail,
      });
      if (!result.ok) process.exitCode = 1;
    });
    return;
  }

  if (command === 'publish-current-draft') {
    await withSession(async (ops) => {
      const login = await ops.checkLogin();
      if (!login.loggedIn) {
        printJson({
          ok: false,
          needsUserAction: true,
          action: login.phase,
          qrcodePath: login.qrcodePath,
          message: login.message || `未登录，当前阶段: ${login.phase}`,
        });
        process.exitCode = 3;
        return;
      }

      const result = await ops.publishCurrentDraft({
        title: args.title,
      });

      printJson({
        ok: result.ok,
        type: result.type,
        publish: result.publish,
        error: result.error,
        detail: result.detail,
      });
      if (!result.ok) process.exitCode = 1;
    });
    return;
  }

  usage();
  process.exit(2);
}

main().catch((err) => {
  printJson({ ok: false, error: err.message, stack: err.stack });
  disconnect();
  process.exit(1);
});
