#!/usr/bin/env node
/**
 * 钉钉文档企业 API 工具
 *
 * 支持操作：读取文档概览、查询块结构、插入块、覆写内容、删除块、追加段落文本
 *
 * 环境变量：
 *   DINGTALK_CLIENTID - 企业内部应用 ClientId
 *   DINGTALK_CLIENTSECRET - 企业内部应用 ClientSecret
 *   DINGTALK_OPERATOR_ID - 操作人 unionId（可选，不设置则自动获取）
 */

const API_BASE = 'https://api.dingtalk.com';
const TIMEOUT_MS = 30000;

// ============ 配置 ============

const APP_KEY = process.env.DINGTALK_CLIENTID;
const APP_SECRET = process.env.DINGTALK_CLIENTSECRET;
const OPERATOR_ID = process.env.DINGTALK_OPERATOR_ID;

// 用户缓存（避免重复查询）
const userCache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 分钟

// ============ 工具函数 ============

/**
 * 获取 Access Token
 */
async function getAccessToken() {
  if (!APP_KEY || !APP_SECRET) {
    throw new Error('缺少配置：请设置 DINGTALK_CLIENTID 和 DINGTALK_CLIENTSECRET');
  }

  const response = await fetch(`${API_BASE}/v1.0/oauth2/accessToken`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ appKey: APP_KEY, appSecret: APP_SECRET })
  });

  if (!response.ok) throw new Error(`获取 Token 失败：HTTP ${response.status}`);

  const data = await response.json();
  if (data.code && data.code !== 0) throw new Error(`获取 Token 失败：${data.message}`);

  return data.accessToken;
}

/**
 * 通过 userId 获取 unionId（operatorId）
 */
async function getUnionId(userId, token) {
  // 检查缓存
  const cached = userCache.get(userId);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.unionId;
  }

  // 使用旧版 API（新版 topapi/v2 不存在）
  const response = await fetch(`https://oapi.dingtalk.com/user/get?access_token=${token}&userid=${userId}`, {
    method: 'GET'
  });

  if (!response.ok) throw new Error(`获取用户信息失败：HTTP ${response.status}`);

  const data = await response.json();
  if (data.errcode !== 0) throw new Error(`获取用户信息失败：${data.errmsg}`);

  const unionId = data.unionid;
  userCache.set(userId, { unionId, timestamp: Date.now() });

  return unionId;
}

/**
 * 获取当前用户的 operatorId
 *
 * 优先级：
 * 1. 环境变量 DINGTALK_OPERATOR_ID
 * 2. 从 OpenClaw 环境变量获取 sender_id，然后查询 unionId
 */
async function getCurrentOperatorId() {
  // 优先级 1：环境变量
  if (OPERATOR_ID) {
    console.log(`[用户识别] 使用环境变量：${OPERATOR_ID}`);
    return OPERATOR_ID;
  }

  // 优先级 2：从 OpenClaw 环境变量获取 sender_id
  const senderId = process.env.OPENCLAW_SENDER_ID || process.env.DINGTALK_SENDER_ID;
  if (senderId) {
    const token = await getAccessToken();
    const unionId = await getUnionId(senderId, token);
    console.log(`[用户识别] 从 sender_id 获取：${unionId}`);
    return unionId;
  }

  throw new Error('缺少 operatorId：请配置 DINGTALK_OPERATOR_ID 环境变量，或确保钉钉连接器传递了 sender_id');
}

/**
 * 调用企业 API
 */
async function callAPI(endpoint, method = 'GET', body = null, operatorId, token) {
  if (!operatorId) operatorId = await getCurrentOperatorId();
  if (!token) token = await getAccessToken();

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);

  const separator = endpoint.includes('?') ? '&' : '?';
  const url = `${endpoint}${separator}operatorId=${encodeURIComponent(operatorId)}`;

  const options = {
    method,
    headers: {
      'x-acs-dingtalk-access-token': token,
      'Content-Type': 'application/json'
    },
    signal: controller.signal
  };

  if (body) options.body = JSON.stringify(body);

  try {
    const response = await fetch(`${API_BASE}${url}`, options);
    clearTimeout(timeoutId);

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(`API 调用失败：HTTP ${response.status} - ${errorData.message || errorData.code || response.statusText}`);
    }

    const result = await response.json();
    if (result.code && result.code !== 0) throw new Error(result.message || JSON.stringify(result));

    return result;
  } catch (error) {
    clearTimeout(timeoutId);
    throw error;
  }
}

/**
 * 从 URL 提取文档 ID
 */
function extractDocId(input) {
  if (!input) return null;
  if (!input.includes('http') && !input.includes('/')) return input;

  const patterns = [
    /\/i\/nodes\/([a-zA-Z0-9]+)/,
    /\/nodes\/([a-zA-Z0-9]+)/,
    /docKey=([a-zA-Z0-9]+)/,
    /dentryKey=([a-zA-Z0-9]+)/,
  ];

  for (const pattern of patterns) {
    const match = input.match(pattern);
    if (match && match[1]) return match[1];
  }

  return input;
}

function truncateText(text, maxLength = 80) {
  if (!text) return '';
  return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;
}

function blockPreview(block) {
  if (block?.paragraph?.text) return truncateText(block.paragraph.text, 80);
  if (Array.isArray(block?.paragraph?.contents)) {
    const text = block.paragraph.contents.map(item => item?.text || '').join('').trim();
    if (text) return truncateText(text, 80);
  }
  if (block?.heading?.text) return truncateText(block.heading.text, 80);
  return '';
}

// ============ API 封装 ============

async function queryBlocks(dentryUuid, operatorId, token) {
  console.log(`[查询块元素] ${dentryUuid}`);
  return callAPI(`/v1.0/doc/suites/documents/${dentryUuid}/blocks`, 'GET', null, operatorId, token);
}

async function insertBlock(dentryUuid, element, position, operatorId, token) {
  console.log(`[插入块元素] ${dentryUuid}`);
  const body = { element };
  if (position) body.position = position;
  return callAPI(`/v1.0/doc/suites/documents/${dentryUuid}/blocks`, 'POST', body, operatorId, token);
}

async function modifyBlock(dentryUuid, blockId, element, operatorId, token) {
  console.log(`[更新块元素] ${dentryUuid}/${blockId}`);
  return callAPI(`/v1.0/doc/suites/documents/${dentryUuid}/blocks/${blockId}`, 'PUT', { element }, operatorId, token);
}

async function deleteBlock(dentryUuid, blockId, operatorId, token) {
  console.log(`[删除块元素] ${dentryUuid}/${blockId}`);
  return callAPI(`/v1.0/doc/suites/documents/${dentryUuid}/blocks/${blockId}`, 'DELETE', null, operatorId, token);
}

async function appendText(dentryUuid, blockId, text, operatorId, token) {
  console.log(`[追加文本] ${dentryUuid}/${blockId}`);
  return callAPI(`/v1.0/doc/suites/documents/${dentryUuid}/paragraphs/${blockId}/text`, 'POST', { text }, operatorId, token);
}

async function overwriteContent(docKey, markdown, operatorId, token) {
  console.log(`[覆写文档] ${docKey}`);
  return callAPI(`/v1.0/doc/suites/documents/${docKey}/overwriteContent`, 'POST', { dataType: 'markdown', content: markdown }, operatorId, token);
}

// ============ 命令处理 ============

async function cmdRead(args) {
  const docKey = extractDocId(args[0]);
  if (!docKey) { console.error('错误：请提供文档 ID 或链接'); process.exit(1); }

  const operatorId = await getCurrentOperatorId();
  const token = await getAccessToken();
  const result = await queryBlocks(docKey, operatorId, token);

  console.log('\n=== 文档概览 ===\n');
  if (result.blocks && result.blocks.length > 0) {
    result.blocks.forEach((block, index) => {
      console.log(`${index + 1}. [${block.blockType}] ${block.blockId}`);
      const preview = blockPreview(block);
      if (preview) console.log(`   预览：${preview}`);
    });
    console.log('\n提示：如果要做总结、定位 blockId 或查看完整结构，请使用 blocks 命令。');
  } else {
    console.log('(空文档)');
  }
}

async function cmdBlocks(args) {
  const dentryUuid = extractDocId(args[0]);
  if (!dentryUuid) { console.error('错误：请提供文档 ID 或链接'); process.exit(1); }

  const operatorId = await getCurrentOperatorId();
  const token = await getAccessToken();
  const result = await queryBlocks(dentryUuid, operatorId, token);

  console.log('\n=== 块元素详情 ===\n');
  console.log(JSON.stringify(result, null, 2));
}

async function cmdInsert(args) {
  const dentryUuid = extractDocId(args[0]);
  const position = args[1];
  const content = args.slice(2).join(' ');
  if (!dentryUuid || !content) { console.error('错误：请提供文档 ID、位置和內容'); process.exit(1); }

  const operatorId = await getCurrentOperatorId();
  const token = await getAccessToken();
  const result = await insertBlock(dentryUuid, { blockType: 'paragraph', paragraph: { text: content } }, position, operatorId, token);
  console.log('✅ 插入成功');
  console.log(JSON.stringify(result, null, 2));
}

async function cmdDelete(args) {
  const dentryUuid = extractDocId(args[0]);
  const blockId = args[1];
  if (!dentryUuid || !blockId) { console.error('错误：请提供文档 ID 和块 ID'); process.exit(1); }

  const operatorId = await getCurrentOperatorId();
  const token = await getAccessToken();
  const result = await deleteBlock(dentryUuid, blockId, operatorId, token);
  console.log('✅ 删除成功');
  console.log(JSON.stringify(result, null, 2));
}

async function cmdAppendText(args) {
  const dentryUuid = extractDocId(args[0]);
  const blockId = args[1];
  const text = args.slice(2).join(' ');
  if (!dentryUuid || !blockId || !text) { console.error('错误：请提供文档 ID、块 ID 和文本'); process.exit(1); }

  const operatorId = await getCurrentOperatorId();
  const token = await getAccessToken();
  const result = await appendText(dentryUuid, blockId, text, operatorId, token);
  console.log('✅ 追加成功');
  console.log(JSON.stringify(result, null, 2));
}

async function cmdUpdate(args) {
  const docKey = extractDocId(args[0]);
  const markdown = args.slice(1).join(' ');
  if (!docKey || !markdown) { console.error('错误：请提供文档 ID 和内容'); process.exit(1); }

  const operatorId = await getCurrentOperatorId();
  const token = await getAccessToken();
  const result = await overwriteContent(docKey, markdown, operatorId, token);
  console.log('✅ 更新成功');
  console.log(JSON.stringify(result, null, 2));
}

// ============ 主函数 ============

async function main() {
  const args = process.argv.slice(2);

  if (!args.length || args.includes('--help')) {
    console.log(`
钉钉文档企业 API 工具

用法:
  node doc-enterprise.js <command> [args]

命令:
  read <docKey|url>           读取文档概览（块列表 + 预览）
  blocks <docKey|url>         查询完整块结构（适合总结和定位 blockId）
  insert <docKey|url> <pos> <content>  插入块元素
  delete <docKey|url> <blockId>       删除块元素
  append-text <docKey|url> <blockId> <text>  追加文本到段落
  update <docKey|url> <markdown>      覆写整篇文档内容

说明:
  当前脚本未实现 create。
  如需总结文档或查找 blockId，请优先使用 blocks。

示例:
  node doc-enterprise.js read https://alidocs.dingtalk.com/i/nodes/xxx
  node doc-enterprise.js update xxx "# 标题\\n\\n内容"

环境变量:
  DINGTALK_CLIENTID          企业内部应用 ClientId
  DINGTALK_CLIENTSECRET      企业内部应用 ClientSecret
  DINGTALK_OPERATOR_ID       默认操作人 unionId（可选）
  OPENCLAW_SENDER_ID         钉钉连接器传递的 sender_id（自动注入）
`);
    process.exit(0);
  }

  const command = args[0];
  const commandArgs = args.slice(1);

  try {
    switch (command) {
      case 'read': await cmdRead(commandArgs); break;
      case 'blocks': await cmdBlocks(commandArgs); break;
      case 'insert': await cmdInsert(commandArgs); break;
      case 'delete': await cmdDelete(commandArgs); break;
      case 'append-text': await cmdAppendText(commandArgs); break;
      case 'update': await cmdUpdate(commandArgs); break;
      default: console.error(`未知命令：${command}`); process.exit(1);
    }
  } catch (error) {
    console.error('\n错误:', error.message);
    if (error.message.includes('operatorId')) {
      console.error('\n💡 提示：配置 DINGTALK_OPERATOR_ID 或确保钉钉连接器传递了 sender_id');
    } else if (error.message.includes('CLIENTID')) {
      console.error('\n💡 提示：配置 DINGTALK_CLIENTID 和 DINGTALK_CLIENTSECRET');
    } else if (error.message.includes('403')) {
      console.error('\n💡 提示：检查应用权限（Storage.File.Read/Write）');
    }
    process.exit(1);
  }
}

main();
