"use strict";
/**
 * 工单复盘文档 - 第三节表格单元格填充脚本（优化版）
 * 
 * 从加密的用户OAuth UAT存储中读取token，直接调飞书Docx PATCH API
 * 填充工单复盘文档第三节嵌套表格的月份数据。
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const crypto = require('crypto');
const https = require('https');

// ============================================================
// 配置区 —— 每次使用时修改此处
// ============================================================

// 通过环境变量配置，复用性更好
// APP_ID: Bot App ID（默认值为收钱吧工单复盘 Bot）
// SENDER_OPEN_ID: 当前用户的飞书 open_id（每人不同）
// DOC_ID: 要填充的复盘总文档 ID
// MONTH: 目标月份标签
const APP_ID = process.env.APP_ID || 'cli_a97b6a0ffc399cc0';
const DOC_ID = process.env.DOC_ID || 'UvhDwxvLaiVRTHk5R31cnVHXnQg';
const MONTH = process.env.MONTH || '2026-04';
const SENDER_OPEN_ID = process.env.SENDER_OPEN_ID || '';

// 格式化后的数据
const CELL_DATA = {
  total:    '644',
  noOpt:    '160（产研介入94）',
  prodOpt:  '42（20）',
  techWork: '0',
  techCheck:'79（48）',
  noTech:   '208（28）',
  internal: '138（产研介入87）',
  solved:   '已解决54（27）',
  deferred: '延期处理66（46）',
  noRepro:  '无法重现：18（14）',
  timeout:  '88（58）',
};

// ============================================================
// 常量
// ============================================================

const LINUX_UAT_DIR = path.join(
  process.env.XDG_DATA_HOME || path.join(os.homedir(), '.local', 'share'),
  'openclaw-feishu-uat'
);
const MASTER_KEY_PATH = path.join(LINUX_UAT_DIR, 'master.key');
const IV_BYTES = 12, TAG_BYTES = 16;
const HEADER_CELLS = 11, CELLS_PER_MONTH = 33;
const DOCX_BASE = 'https://open.feishu.cn/open-apis/docx/v1/documents';
const MAX_RETRIES = 3;

// ============================================================
// 加解密
// ============================================================

function linuxSafeFileName(account) {
  return account.replace(/[^a-zA-Z0-9._-]/g, '_') + '.enc';
}

function decryptData(data, key) {
  if (data.length < IV_BYTES + TAG_BYTES) return null;
  try {
    const iv = data.subarray(0, IV_BYTES);
    const tag = data.subarray(IV_BYTES, IV_BYTES + TAG_BYTES);
    const enc = data.subarray(IV_BYTES + TAG_BYTES);
    const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
    decipher.setAuthTag(tag);
    return Buffer.concat([decipher.update(enc), decipher.final()]).toString('utf8');
  } catch { return null; }
}

// ============================================================
// HTTP 请求（带重试）
// ============================================================

function api(method, url, headers, body) {
  return new Promise((resolve, reject) => {
    const parsed = new URL(url);
    const req = https.request(
      { hostname: parsed.hostname, path: parsed.pathname + parsed.search, method,
        headers: { 'Content-Type': 'application/json', ...headers } },
      (res) => {
        let d = '';
        res.on('data', c => d += c);
        res.on('end', () => { try { resolve(JSON.parse(d)); } catch { resolve({ raw: d }); } });
      }
    );
    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

/** 带重试和延迟的API调用 */
function sleep(ms) { return new Promise(r => setTimeout(r, ms)); }

async function apiWithRetry(method, url, headers, body, retries = MAX_RETRIES) {
  for (let i = 0; i < retries; i++) {
    const res = await api(method, url, headers, body);
    if (res.code === 99991400 || res.code === 99991300) {
      // 频率限制，等 2^retry 秒
      const wait = Math.min(2000 * Math.pow(2, i), 10000);
      console.log(`  ⏳ 频率限流，等待${wait}ms后重试...`);
      await sleep(wait);
      continue;
    }
    if (res.code !== 0 && res.code !== undefined) {
      if (i < retries - 1) { await sleep(500); continue; }
    }
    return res;
  }
  throw new Error(`API call failed after ${retries} retries`);
}

async function getChildren(uat, blockId, pageSize = 50) {
  const results = [];
  let pt = '';
  do {
    const url = `${DOCX_BASE}/${DOC_ID}/blocks/${blockId}/children?page_size=${pageSize}${pt ? '&page_token=' + pt : ''}`;
    const res = await apiWithRetry('GET', url, { Authorization: `Bearer ${uat}` });
    if (res.code !== 0) throw new Error(`getChildren: ${res.msg}`);
    if (res.data?.items) results.push(...res.data.items);
    pt = res.data?.page_token || '';
  } while (pt);
  return results;
}

async function readCellText(uat, cellBlock) {
  if (cellBlock.block_type !== 32) return '';
  const children = await getChildren(uat, cellBlock.block_id, 10);
  return children.find(c => c.block_type === 2)?.text?.elements?.[0]?.text_run?.content || '';
}

async function setCellText(uat, cellBlock, newText) {
  await sleep(100); // 避免频率限制
  const children = await getChildren(uat, cellBlock.block_id, 10);
  const textBlock = children.find(c => c.block_type === 2);
  if (!textBlock) return { error: 'no text block' };
  const body = JSON.stringify({
    update_text_elements: {
      elements: [{ text_run: { content: newText, text_element_style: {} } }],
    },
  });
  const url = `${DOCX_BASE}/${DOC_ID}/blocks/${textBlock.block_id}`;
  return apiWithRetry('PATCH', url, { Authorization: `Bearer ${uat}` }, body);
}

// ============================================================
// Token 获取
// ============================================================

function getUserUAT() {
  if (!SENDER_OPEN_ID) {
    throw new Error('请设置 SENDER_OPEN_ID 环境变量（你的飞书 open_id）');
  }
  const accountKey = `${APP_ID}:${SENDER_OPEN_ID}`;
  const encFile = path.join(LINUX_UAT_DIR, linuxSafeFileName(accountKey));
  if (!fs.existsSync(encFile)) throw new Error(`Token文件不存在: ${encFile}\n请检查 SENDER_OPEN_ID 是否正确，或是否已完成飞书授权`);
  if (!fs.existsSync(MASTER_KEY_PATH)) throw new Error('Master key不存在');
  const masterKey = fs.readFileSync(MASTER_KEY_PATH);
  const encData = fs.readFileSync(encFile);
  const json = decryptData(encData, masterKey);
  if (!json) throw new Error('解密失败');
  return JSON.parse(json).accessToken;
}

// ============================================================
// 主流程
// ============================================================

async function main() {
  const uat = getUserUAT();
  console.log(`✅ 用户UAT获取成功 (ends: ...${uat.slice(-4)})`);

  // 获取表格所有单元格
  const rootChildren = await getChildren(uat, DOC_ID);
  const tableBlock = rootChildren.find(b => b.block_type === 31);
  if (!tableBlock) throw new Error('文档中未找到表格块');

  const allCells = await getChildren(uat, tableBlock.block_id);
  console.log(`📊 共 ${allCells.length} 个单元格`);

  // 串行读取单元格内容（避免频率限制）
  console.log(`\n🔍 查找 "${MONTH}" 单元格位置...`);
  let monthIdx = -1;
  for (let i = 0; i < allCells.length; i++) {
    if (i % 20 === 0) await sleep(50);
    const text = await readCellText(uat, allCells[i]);
    if (text === MONTH) { monthIdx = i; break; }
  }

  if (monthIdx === -1) throw new Error(`文档中未找到 "${MONTH}"`);

  // 计算月份组起始索引
  const monOffset = Math.floor((monthIdx - HEADER_CELLS) / CELLS_PER_MONTH);
  const mainStart = HEADER_CELLS + monOffset * CELLS_PER_MONTH;

  // 验证起始单元格
  const actualText = await readCellText(uat, allCells[mainStart]);
  if (actualText !== MONTH) throw new Error(`预期 "${MONTH}"，实际 "${actualText}"`);

  console.log(`📐 月份组起始索引: ${mainStart}`);
  console.log(`\n📝 准备更新 ${mainStart + 1} ~ ${mainStart + 31} 的空单元格:\n`);

  // 更新映射
  const updates = [
    [mainStart + 1, CELL_DATA.total],
    [mainStart + 2, CELL_DATA.noOpt],
    // +3: colspan右半，留空
    [mainStart + 4, CELL_DATA.prodOpt],
    [mainStart + 5, CELL_DATA.techWork],
    [mainStart + 6, CELL_DATA.techCheck],
    [mainStart + 7, CELL_DATA.noTech],
    [mainStart + 8, CELL_DATA.internal],
    [mainStart + 9, CELL_DATA.solved],
    [mainStart + 10, CELL_DATA.timeout],
    [mainStart + 20, CELL_DATA.deferred],
    [mainStart + 31, CELL_DATA.noRepro],
  ];

  let ok = 0, fail = 0;
  for (const [idx, text] of updates) {
    const oldVal = await readCellText(uat, allCells[idx]);
    if (oldVal) {
      console.log(`  ⏭️  索引${idx}: 已有数据 "${oldVal}"，跳过`);
      ok++; continue;
    }
    const result = await setCellText(uat, allCells[idx], text);
    if (result.code === 0 || result.code === undefined) {
      console.log(`  ✅ 索引${idx}: "${text}"`);
      ok++;
    } else {
      console.error(`  ❌ 索引${idx}: ${result.msg || JSON.stringify(result).slice(0, 80)}`);
      fail++;
    }
  }

  console.log(`\n📊 完成: ${ok} 成功, ${fail} 失败`);

  // 抽样验证
  if (fail === 0) {
    console.log('\n🔍 抽样验证...');
    const checkIdx = [mainStart + 1, mainStart + 9, mainStart + 20];
    for (const idx of checkIdx) {
      const val = await readCellText(uat, allCells[idx]);
      console.log(`  索引${idx}: "${val}"`);
    }
  }
  if (fail > 0) process.exit(1);
}

main().catch(err => { console.error('❌ 错误:', err.message); process.exit(1); });
