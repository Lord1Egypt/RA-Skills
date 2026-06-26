#!/usr/bin/env node

const fs = require('fs');
const path = require('path');
const { requestFeishuJson } = require('./feishu-api');

const TOKEN_FILE = path.resolve(__dirname, '../../.feishu-user-token.json');

function loadSavedUserAccessToken(tokenFile = TOKEN_FILE) {
  if (!fs.existsSync(tokenFile)) {
    return null;
  }

  let data;
  try {
    data = JSON.parse(fs.readFileSync(tokenFile, 'utf8'));
  } catch (error) {
    throw new Error(`已保存的 user token 文件不是合法 JSON: ${tokenFile}`);
  }

  const token = data.access_token;
  if (!token) {
    throw new Error(`已保存的 user token 文件缺少 access_token 字段: ${tokenFile}`);
  }
  return token;
}

function getUserAccessToken() {
  return process.env.FEISHU_USER_ACCESS_TOKEN || loadSavedUserAccessToken();
}

function getAuthHint() {
  return (
    '缺少 FEISHU_USER_ACCESS_TOKEN，且未在 skill 目录中找到 .feishu-user-token.json。' +
    '可先设置 FEISHU_USER_ACCESS_TOKEN，或运行 node scripts/feishu_oauth_server.js 完成授权。'
  );
}

async function getTenantAccessToken(appId, appSecret) {
  const data = await requestFeishuJson('/auth/v3/tenant_access_token/internal', {
    action: '获取 tenant_access_token',
    method: 'POST',
    body: {
      app_id: appId,
      app_secret: appSecret,
    },
  });
  return data.tenant_access_token;
}

async function resolveReadAccessToken() {
  const userAccessToken = getUserAccessToken();
  if (userAccessToken) {
    return {
      accessToken: userAccessToken,
      tokenSource: 'user_access_token',
    };
  }

  const appId = process.env.FEISHU_APP_ID || '';
  const appSecret = process.env.FEISHU_APP_SECRET || '';
  if (!appId || !appSecret) {
    throw new Error(getAuthHint());
  }

  return {
    accessToken: await getTenantAccessToken(appId, appSecret),
    tokenSource: 'tenant_access_token',
  };
}

function resolveUserAccessTokenForWrite() {
  const token = getUserAccessToken();
  if (!token) {
    throw new Error(getAuthHint());
  }
  return token;
}

module.exports = {
  TOKEN_FILE,
  loadSavedUserAccessToken,
  getUserAccessToken,
  getAuthHint,
  getTenantAccessToken,
  resolveReadAccessToken,
  resolveUserAccessTokenForWrite,
};
