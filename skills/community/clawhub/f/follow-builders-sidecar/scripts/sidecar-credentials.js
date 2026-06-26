#!/usr/bin/env node

import { SIDECAR_CREDENTIALS_PATH } from './sidecar-common.js';
import { readJsonFile, writeJsonFile } from './sidecar-fs.js';

const DEFAULT_DIRECT_FEISHU_DOMAIN = 'feishu';

function collapseWhitespace(value) {
  return String(value || '').trim();
}

function buildDefaultCredentials(overrides = {}) {
  const base = {
    version: 1,
    feishu: {
      appId: null,
      appSecret: null,
      chatId: null,
      domain: DEFAULT_DIRECT_FEISHU_DOMAIN,
      updatedAt: null
    }
  };

  return {
    ...base,
    ...overrides,
    feishu: {
      ...base.feishu,
      ...(overrides.feishu || {})
    }
  };
}

async function loadSidecarCredentials() {
  return buildDefaultCredentials(await readJsonFile(SIDECAR_CREDENTIALS_PATH, {}));
}

async function saveSidecarCredentials(credentials) {
  await writeJsonFile(SIDECAR_CREDENTIALS_PATH, buildDefaultCredentials(credentials));
}

function hasDirectFeishuCredentials(credentials) {
  return Boolean(
    collapseWhitespace(credentials?.feishu?.appId)
    && collapseWhitespace(credentials?.feishu?.appSecret)
  );
}

function mergeDirectFeishuCredentials(existing, overrides = {}) {
  const next = buildDefaultCredentials(existing);
  const merged = buildDefaultCredentials({
    ...next,
    feishu: {
      ...next.feishu,
      ...(overrides.feishu || {})
    }
  });

  const appId = collapseWhitespace(merged.feishu.appId);
  const appSecret = collapseWhitespace(merged.feishu.appSecret);
  const chatId = collapseWhitespace(merged.feishu.chatId);
  const domain = collapseWhitespace(merged.feishu.domain) || DEFAULT_DIRECT_FEISHU_DOMAIN;

  merged.feishu.appId = appId || null;
  merged.feishu.appSecret = appSecret || null;
  merged.feishu.chatId = chatId || null;
  merged.feishu.domain = domain;
  merged.feishu.updatedAt = hasDirectFeishuCredentials(merged)
    ? (overrides.feishu?.updatedAt || new Date().toISOString())
    : null;

  return merged;
}

function redactSidecarCredentials(credentials) {
  const merged = buildDefaultCredentials(credentials);
  return {
    version: merged.version,
    feishu: {
      configured: hasDirectFeishuCredentials(merged),
      chatIdConfigured: Boolean(collapseWhitespace(merged.feishu.chatId)),
      domain: merged.feishu.domain || DEFAULT_DIRECT_FEISHU_DOMAIN,
      updatedAt: merged.feishu.updatedAt || null
    }
  };
}

export {
  SIDECAR_CREDENTIALS_PATH,
  buildDefaultCredentials,
  hasDirectFeishuCredentials,
  loadSidecarCredentials,
  mergeDirectFeishuCredentials,
  redactSidecarCredentials,
  saveSidecarCredentials
};
