#!/usr/bin/env node

import { fileURLToPath } from 'url';

import {
  SIDECAR_CREDENTIALS_PATH,
  buildDefaultConfig,
  loadSidecarConfig,
  log,
  normalizeFeishuDeliveryMode,
  normalizeWeeklyDay,
  saveSidecarConfig
} from './sidecar-common.js';
import {
  hasDirectFeishuCredentials,
  loadSidecarCredentials,
  mergeDirectFeishuCredentials,
  redactSidecarCredentials,
  saveSidecarCredentials
} from './sidecar-credentials.js';

function parseArgs(argv) {
  const args = argv.slice(2);
  const parsed = {};

  for (let index = 0; index < args.length; index += 1) {
    const arg = args[index];
    switch (arg) {
      case '--language':
        parsed.language = args[++index];
        break;
      case '--timezone':
        parsed.timezone = args[++index];
        break;
      case '--frequency':
        parsed.frequency = args[++index];
        break;
      case '--weekly-day':
        parsed.weeklyDay = args[++index];
        break;
      case '--driver':
        parsed.driver = args[++index];
        break;
      case '--channel':
        parsed.channel = args[++index];
        break;
      case '--to':
        parsed.to = args[++index];
        break;
      case '--account':
        parsed.accountId = args[++index];
        break;
      case '--model':
        parsed.model = args[++index];
        break;
      case '--feishu-account':
        parsed.feishuAccountId = args[++index];
        break;
      case '--feishu-mode':
        parsed.feishuMode = args[++index];
        break;
      case '--feishu-chat-id':
        parsed.feishuChatId = args[++index];
        break;
      case '--feishu-app-id':
        parsed.feishuAppId = args[++index];
        break;
      case '--feishu-app-secret':
        parsed.feishuAppSecret = args[++index];
        break;
      case '--feishu-domain':
        parsed.feishuDomain = args[++index];
        break;
      case '--avatar-fallback-account':
        parsed.avatarFallbackAccountId = args[++index];
        break;
      default:
        throw new Error(`Unknown argument: ${arg}`);
    }
  }

  return parsed;
}

function inferFeishuMode(args, config) {
  if (args.feishuMode) {
    return normalizeFeishuDeliveryMode(args.feishuMode);
  }
  if (args.feishuAppId || args.feishuAppSecret) {
    return 'direct_credentials';
  }
  return normalizeFeishuDeliveryMode(config.delivery?.feishu?.mode);
}

function validateFeishuConfig(config, directCredentials) {
  if (config.delivery?.driver !== 'feishu_card') {
    return;
  }

  if (!config.delivery?.feishu?.chatId) {
    throw new Error('Feishu card delivery requires chatId');
  }

  if (config.delivery?.feishu?.mode === 'direct_credentials') {
    if (!hasDirectFeishuCredentials(directCredentials)) {
      throw new Error(`Direct Feishu mode requires appId and appSecret in ${SIDECAR_CREDENTIALS_PATH}`);
    }
    return;
  }

  if (!config.delivery?.feishu?.accountId) {
    throw new Error('Feishu card delivery requires a Feishu accountId from OpenClaw');
  }
}

async function main() {
  const args = parseArgs(process.argv);
  const config = await loadSidecarConfig();
  const existingCredentials = await loadSidecarCredentials();
  const feishuMode = inferFeishuMode(args, config);
  const nextCredentials = mergeDirectFeishuCredentials(existingCredentials, {
    feishu: {
      ...(args.feishuAppId ? { appId: args.feishuAppId } : {}),
      ...(args.feishuAppSecret ? { appSecret: args.feishuAppSecret } : {}),
      ...(args.feishuChatId ? { chatId: args.feishuChatId } : {}),
      ...(args.feishuDomain ? { domain: args.feishuDomain } : {})
    }
  });

  const nextConfig = buildDefaultConfig({
    ...config,
    ...(args.language ? { language: args.language } : {}),
    ...(args.timezone ? { timezone: args.timezone } : {}),
    ...(args.frequency ? { frequency: args.frequency } : {}),
    ...(args.weeklyDay ? { weeklyDay: normalizeWeeklyDay(args.weeklyDay) } : {}),
    ...(args.model ? { model: args.model } : {}),
    delivery: {
      ...config.delivery,
      ...(args.driver ? { driver: args.driver } : {}),
      openclaw: {
        ...config.delivery.openclaw,
        ...(args.channel ? { channel: args.channel } : {}),
        ...(args.to ? { to: args.to } : {}),
        ...(args.accountId ? { accountId: args.accountId } : {})
      },
      feishu: {
        ...config.delivery.feishu,
        ...(feishuMode ? { mode: feishuMode } : {}),
        ...(args.feishuAccountId ? { accountId: args.feishuAccountId } : {}),
        ...(args.feishuChatId ? { chatId: args.feishuChatId } : {}),
        ...(args.feishuDomain ? { domain: args.feishuDomain } : {})
      },
      ...(args.avatarFallbackAccountId ? { avatarFallbackAccountId: args.avatarFallbackAccountId } : {})
    }
  });
  if (nextConfig.delivery?.feishu?.mode === 'direct_credentials' && !nextConfig.delivery?.feishu?.chatId) {
    nextConfig.delivery.feishu.chatId = nextCredentials.feishu.chatId || null;
  }
  if (nextConfig.delivery?.feishu?.mode === 'direct_credentials' && !nextConfig.delivery?.feishu?.domain) {
    nextConfig.delivery.feishu.domain = nextCredentials.feishu.domain || 'feishu';
  }
  if (nextConfig.delivery?.feishu?.mode === 'direct_credentials') {
    nextConfig.delivery.feishu.accountId = null;
  }

  validateFeishuConfig(nextConfig, nextCredentials);

  await saveSidecarConfig(nextConfig);
  if (hasDirectFeishuCredentials(nextCredentials)) {
    await saveSidecarCredentials(nextCredentials);
  }

  process.stdout.write(`${JSON.stringify({
    status: 'ok',
    config: nextConfig,
    directCredentials: redactSidecarCredentials(nextCredentials)
  })}\n`);
}

const IS_ENTRYPOINT = process.argv[1] && fileURLToPath(import.meta.url) === process.argv[1];

if (IS_ENTRYPOINT) {
  main().catch((error) => {
    log('error', 'Sidecar configure failed', {
      error: error.message,
      stack: error.stack
    });
    process.exit(1);
  });
}
