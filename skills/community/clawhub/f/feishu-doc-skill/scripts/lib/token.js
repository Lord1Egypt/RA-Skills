#!/usr/bin/env node

const { URL } = require('url');
const { requestFeishuJson } = require('./feishu-api');

const TOKEN_PATTERNS = [
  ['/wiki/', /\/wiki\/([A-Za-z0-9]+)/],
  ['/docx/', /\/docx\/([A-Za-z0-9]+)/],
  ['/docs/', /\/docs\/([A-Za-z0-9]+)/],
  ['/sheets/', /\/sheets\/([A-Za-z0-9]+)/],
  ['/base/', /\/base\/([A-Za-z0-9]+)/],
];

function extractTokenFromUrl(url) {
  const pathname = new URL(url).pathname;
  for (const [, pattern] of TOKEN_PATTERNS) {
    const match = pathname.match(pattern);
    if (match) {
      return match[1];
    }
  }
  throw new Error('无法从链接中提取飞书文档 token');
}

function extractToken(source) {
  if (source.startsWith('http://') || source.startsWith('https://')) {
    return extractTokenFromUrl(source);
  }
  return source;
}

function looksLikeWikiToken(token) {
  return token.startsWith('wiki_') || token.startsWith('wik') || token.length >= 20;
}

async function resolveWikiNode(accessToken, wikiToken) {
  return requestFeishuJson('/wiki/v2/spaces/get_node', {
    action: '解析 wiki 节点',
    headers: { Authorization: `Bearer ${accessToken}` },
    query: { token: wikiToken },
  });
}

async function resolveDocToken(accessToken, source) {
  const token = extractToken(source);
  try {
    const data = await resolveWikiNode(accessToken, token);
    return {
      sourceToken: token,
      docToken: data.data.node.obj_token,
      wikiNode: data,
    };
  } catch (error) {
    return {
      sourceToken: token,
      docToken: token,
      wikiNode: null,
    };
  }
}

module.exports = {
  TOKEN_PATTERNS,
  extractTokenFromUrl,
  extractToken,
  looksLikeWikiToken,
  resolveWikiNode,
  resolveDocToken,
};
