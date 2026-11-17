#!/usr/bin/env node
/**
 * 钉钉文档企业 API 工具
 *
 * 只操作已有文档：读取内容、覆写内容，以及插入、修改、删除内容块。
 * 本脚本不实现文档、知识库、文件夹或副本的创建接口。
 */

const API_BASE = 'https://api.dingtalk.com';
const TIMEOUT_MS = 30000;
const USER_CACHE_TTL_MS = 5 * 60 * 1000;
const userCache = new Map();

function getCredentials() {
  const appKey = process.env.DINGTALK_CLIENTID;
  const appSecret = process.env.DINGTALK_CLIENTSECRET;
  if (!appKey || !appSecret) {
    throw new Error('缺少配置：请设置 DINGTALK_CLIENTID 和 DINGTALK_CLIENTSECRET');
  }
  return { appKey, appSecret };
}

function maskValue(value, keep = 4) {
  const text = String(value || '');
  if (!text) return '';
  if (text.length <= keep) return '*'.repeat(text.length);
  return `${'*'.repeat(text.length - keep)}${text.slice(-keep)}`;
}

function debug(message) {
  if (process.env.DINGTALK_DEBUG === 'true') console.error(`[调试] ${message}`);
}

async function readJsonResponse(response) {
  const text = await response.text();
  if (!text) return {};
  try {
    return JSON.parse(text);
  } catch (error) {
    throw new Error(`解析 API 响应失败：${error.message}`);
  }
}

async function getAccessToken() {
  const { appKey, appSecret } = getCredentials();
  const response = await fetch(`${API_BASE}/v1.0/oauth2/accessToken`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ appKey, appSecret })
  });
  const data = await readJsonResponse(response);
  if (!response.ok || (data.code && data.code !== 0)) {
    throw new Error(`获取 Token 失败：${data.message || data.code || `HTTP ${response.status}`}`);
  }
  if (!data.accessToken) throw new Error('获取 Token 失败：响应中缺少 accessToken');
  return data.accessToken;
}

async function getUnionId(userId, token) {
  const cached = userCache.get(userId);
  if (cached && Date.now() - cached.timestamp < USER_CACHE_TTL_MS) return cached.unionId;

  const url = `https://oapi.dingtalk.com/user/get?access_token=${encodeURIComponent(token)}&userid=${encodeURIComponent(userId)}`;
  const response = await fetch(url, { method: 'GET' });
  const data = await readJsonResponse(response);
  if (!response.ok || data.errcode !== 0) {
    throw new Error(`获取用户信息失败：${data.errmsg || `HTTP ${response.status}`}`);
  }
  if (!data.unionid) throw new Error('获取用户信息失败：响应中缺少 unionid');

  userCache.set(userId, { unionId: data.unionid, timestamp: Date.now() });
  return data.unionid;
}

/**
 * 线上优先使用当前消息发送者。DINGTALK_OPERATOR_ID 仅作为没有 sender_id 时的本地调试回退。
 */
async function getCurrentOperatorId(token = null) {
  const senderId = process.env.OPENCLAW_SENDER_ID || process.env.DINGTALK_SENDER_ID;
  if (senderId) {
    const accessToken = token || await getAccessToken();
    const unionId = await getUnionId(senderId, accessToken);
    debug(`已从当前 sender_id 解析 operatorId（sender=${maskValue(senderId)}, operator=${maskValue(unionId)}）`);
    return unionId;
  }

  const localOperatorId = process.env.DINGTALK_OPERATOR_ID;
  if (localOperatorId) {
    debug(`未收到 sender_id，使用本地调试 operatorId（operator=${maskValue(localOperatorId)}）`);
    return localOperatorId;
  }

  throw new Error('缺少当前用户身份：请确认连接器传入 OPENCLAW_SENDER_ID；本地调试可设置 DINGTALK_OPERATOR_ID');
}

async function callAPI(endpoint, method = 'GET', body = null, operatorId = null, token = null) {
  const accessToken = token || await getAccessToken();
  const currentOperatorId = operatorId || await getCurrentOperatorId(accessToken);
  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);
  const separator = endpoint.includes('?') ? '&' : '?';
  const url = `${API_BASE}${endpoint}${separator}operatorId=${encodeURIComponent(currentOperatorId)}`;
  const options = {
    method,
    headers: {
      'x-acs-dingtalk-access-token': accessToken,
      'Content-Type': 'application/json'
    },
    signal: controller.signal
  };
  if (body !== null) options.body = JSON.stringify(body);

  try {
    const response = await fetch(url, options);
    const result = await readJsonResponse(response);
    const hasErrorCode = result.code !== undefined
      && result.code !== null
      && result.code !== 0
      && result.code !== '0';
    if (!response.ok || result.success === false || hasErrorCode) {
      const error = new Error(`API 调用失败：${result.message || result.code || `HTTP ${response.status}`}`);
      error.code = result.code;
      error.requestId = result.requestId;
      throw error;
    }
    return result;
  } catch (error) {
    if (error.name === 'AbortError') throw new Error(`API 调用超时（${TIMEOUT_MS}ms）`);
    throw error;
  } finally {
    clearTimeout(timeoutId);
  }
}

function extractDocId(input) {
  if (!input) return null;
  const value = String(input).trim();
  if (/^https?:\/\//i.test(value)) {
    let parsedUrl;
    try {
      parsedUrl = new URL(value);
    } catch {
      throw new Error('无法识别钉钉文档链接或 docKey');
    }
    if (parsedUrl.hostname.toLowerCase() !== 'alidocs.dingtalk.com') {
      throw new Error('只允许 alidocs.dingtalk.com 钉钉文档链接');
    }
  } else if (value.includes('/') && !/^alidocs\.dingtalk\.com\//i.test(value)) {
    throw new Error('无法识别钉钉文档链接或 docKey');
  }
  const patterns = [
    /\/i\/nodes\/([a-zA-Z0-9_-]+)/,
    /\/nodes\/([a-zA-Z0-9_-]+)/,
    /[?&]docKey=([a-zA-Z0-9_-]+)/,
    /[?&]dentryKey=([a-zA-Z0-9_-]+)/
  ];
  for (const pattern of patterns) {
    const match = value.match(pattern);
    if (match) return match[1];
  }
  if (/^[a-zA-Z0-9_-]+$/.test(value)) return value;
  throw new Error('无法识别钉钉文档链接或 docKey');
}

function validateBlockId(input) {
  const blockId = String(input || '').trim();
  if (!/^[a-zA-Z0-9_-]+$/.test(blockId)) throw new Error('无效的 blockId');
  return blockId;
}

function encodePathId(input) {
  return encodeURIComponent(extractDocId(input));
}

function extractBlocks(result) {
  const candidates = [
    result?.blocks,
    result?.data,
    result?.result?.data,
    result?.result?.blocks,
    result?.data?.blocks,
    result?.data?.result?.data
  ];
  return candidates.find(Array.isArray) || [];
}

function truncateText(text, maxLength = 80) {
  if (!text) return '';
  return text.length > maxLength ? `${text.slice(0, maxLength)}...` : text;
}

function blockPreview(block) {
  if (block?.paragraph?.text) return truncateText(block.paragraph.text);
  if (Array.isArray(block?.paragraph?.contents)) {
    const text = block.paragraph.contents.map(item => item?.text || '').join('').trim();
    if (text) return truncateText(text);
  }
  if (block?.heading?.text) return truncateText(block.heading.text);
  if (block?.text) return truncateText(block.text);
  return '';
}

async function queryBlocks(docKeyOrUrl, operatorId, token) {
  return callAPI(`/v1.0/doc/suites/documents/${encodePathId(docKeyOrUrl)}/blocks`, 'GET', null, operatorId, token);
}

async function insertBlock(docKeyOrUrl, text, position, operatorId, token) {
  const parsedPosition = Number(position);
  if (!Number.isInteger(parsedPosition) || parsedPosition < 0) throw new Error('position 必须是大于或等于 0 的整数');
  const element = { blockType: 'paragraph', paragraph: { text } };
  return callAPI(
    `/v1.0/doc/suites/documents/${encodePathId(docKeyOrUrl)}/blocks`,
    'POST',
    { element, position: parsedPosition },
    operatorId,
    token
  );
}

async function modifyBlock(docKeyOrUrl, blockId, text, operatorId, token) {
  const element = { blockType: 'paragraph', paragraph: { text } };
  return callAPI(
    `/v1.0/doc/suites/documents/${encodePathId(docKeyOrUrl)}/blocks/${encodeURIComponent(validateBlockId(blockId))}`,
    'PUT',
    { element },
    operatorId,
    token
  );
}

async function deleteBlock(docKeyOrUrl, blockId, operatorId, token) {
  return callAPI(
    `/v1.0/doc/suites/documents/${encodePathId(docKeyOrUrl)}/blocks/${encodeURIComponent(validateBlockId(blockId))}`,
    'DELETE',
    null,
    operatorId,
    token
  );
}

async function overwriteContent(docKeyOrUrl, markdown, operatorId, token) {
  return callAPI(
    `/v1.0/doc/suites/documents/${encodePathId(docKeyOrUrl)}/overwriteContent`,
    'POST',
    { dataType: 'markdown', content: markdown },
    operatorId,
    token
  );
}

function requireArgs(args, count, usage) {
  if (args.length < count) throw new Error(`参数不足。用法：${usage}`);
}

async function cmdRead(args) {
  requireArgs(args, 1, 'read <docKey|url>');
  const docKey = extractDocId(args[0]);
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token);
  const result = await queryBlocks(docKey, operatorId, token);
  const blocks = extractBlocks(result);

  console.log('\n=== 文档概览 ===\n');
  if (!blocks.length) {
    console.log('(未返回内容块；如文档并非空文档，请使用 blocks 查看原始响应)');
    return result;
  }
  blocks.forEach((block, index) => {
    const blockType = block.blockType || block.type || 'unknown';
    const blockId = block.blockId || block.id || '(无 ID)';
    console.log(`${index + 1}. [${blockType}] ${blockId}`);
    const preview = blockPreview(block);
    if (preview) console.log(`   预览：${preview}`);
  });
  return result;
}

async function cmdBlocks(args) {
  requireArgs(args, 1, 'blocks <docKey|url>');
  const docKey = extractDocId(args[0]);
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token);
  const result = await queryBlocks(docKey, operatorId, token);
  console.log(JSON.stringify(result, null, 2));
  return result;
}

async function cmdInsert(args) {
  requireArgs(args, 3, 'insert <docKey|url> <position> <text>');
  const docKey = extractDocId(args[0]);
  const position = Number(args[1]);
  if (!Number.isInteger(position) || position < 0) throw new Error('position 必须是大于或等于 0 的整数');
  const text = args.slice(2).join(' ');
  if (!text) throw new Error('插入文本不能为空');
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token);
  const result = await insertBlock(docKey, text, position, operatorId, token);
  console.log('✅ 内容块插入成功');
  console.log(JSON.stringify(result, null, 2));
  return result;
}

async function cmdModify(args) {
  requireArgs(args, 3, 'modify <docKey|url> <blockId> <text>');
  const docKey = extractDocId(args[0]);
  const blockId = validateBlockId(args[1]);
  const text = args.slice(2).join(' ');
  if (!text) throw new Error('修改文本不能为空；删除内容块请使用 delete');
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token);
  const result = await modifyBlock(docKey, blockId, text, operatorId, token);
  console.log('✅ 内容块修改成功');
  console.log(JSON.stringify(result, null, 2));
  return result;
}

async function cmdDelete(args) {
  requireArgs(args, 2, 'delete <docKey|url> <blockId>');
  const docKey = extractDocId(args[0]);
  const blockId = validateBlockId(args[1]);
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token);
  const result = await deleteBlock(docKey, blockId, operatorId, token);
  console.log('✅ 内容块删除成功');
  console.log(JSON.stringify(result, null, 2));
  return result;
}

async function cmdUpdate(args) {
  requireArgs(args, 2, 'update <docKey|url> <markdown>');
  const docKey = extractDocId(args[0]);
  const markdown = args.slice(1).join(' ');
  if (!markdown) throw new Error('覆写内容不能为空');
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token);
  const result = await overwriteContent(docKey, markdown, operatorId, token);
  console.log('✅ 文档内容覆写成功');
  console.log(JSON.stringify(result, null, 2));
  return result;
}

const COMMAND_HANDLERS = Object.freeze({
  read: cmdRead,
  blocks: cmdBlocks,
  insert: cmdInsert,
  modify: cmdModify,
  delete: cmdDelete,
  update: cmdUpdate
});

function printHelp() {
  console.log(`
钉钉文档企业 API 工具

只操作已有文档，不提供任何文档创建能力。

用法:
  node doc-enterprise.js <command> [args]

命令:
  read <docKey|url>                         读取文档概览
  blocks <docKey|url>                       查询完整块结构
  update <docKey|url> <markdown>            覆写已有文档内容
  insert <docKey|url> <position> <text>      插入段落块（position 支持 0）
  modify <docKey|url> <blockId> <text>       修改段落块
  delete <docKey|url> <blockId>              删除内容块

明确不支持:
  创建文档、创建空白文档、创建知识库、创建文件夹、复制文档。

环境变量:
  DINGTALK_CLIENTID          企业内部应用 ClientId
  DINGTALK_CLIENTSECRET      企业内部应用 ClientSecret
  OPENCLAW_SENDER_ID         当前钉钉消息发送者 sender_id（线上优先）
  DINGTALK_SENDER_ID         sender_id 兼容变量
  DINGTALK_OPERATOR_ID       本地调试回退（线上不要配置）
  DINGTALK_DEBUG=true        输出脱敏调试信息
`);
}

async function runCommand(command, args = []) {
  const handler = COMMAND_HANDLERS[command];
  if (!handler) throw new Error(`未知或不允许的命令：${command}`);
  return handler(args);
}

async function main(argv = process.argv.slice(2)) {
  if (!argv.length || argv.includes('--help')) {
    printHelp();
    return;
  }
  await runCommand(argv[0], argv.slice(1));
}

module.exports = {
  COMMAND_HANDLERS,
  deleteBlock,
  extractBlocks,
  extractDocId,
  getCurrentOperatorId,
  insertBlock,
  main,
  modifyBlock,
  overwriteContent,
  queryBlocks,
  runCommand
};

if (require.main === module) {
  main().catch(error => {
    console.error(`\n错误：${error.message}`);
    if (error.code) console.error(`错误码：${error.code}`);
    if (error.requestId) console.error(`请求 ID：${error.requestId}`);
    process.exitCode = 1;
  });
}
