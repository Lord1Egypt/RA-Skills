#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const BASE_URL = 'http://bjjs.zjw.beijing.gov.cn';
const FEISHU_BASE_URL = 'https://open.feishu.cn';
const SKILL_DIR = path.resolve(__dirname, '..');
const DEFAULT_CONFIG_PATH = path.join(SKILL_DIR, 'projects.json');
const DETAILS_CACHE_PATH = path.join(SKILL_DIR, 'room-cache.json');
const LEDGER_COLUMNS = [
  '地块名',
  '销售楼号',
  '自然楼层',
  '房号',
  '建筑面积',
  '户型',
  '估计成交价',
  '项目已签约套数',
  '已签约面积(M2)',
  '项目成交均价',
  '更新时间'
];
const LEGACY_LEDGER_COLUMNS = [
  '地块名',
  '销售楼号',
  '自然楼层',
  '房号',
  '估计成交价',
  '更新时间',
  '项目已签约套数',
  '项目成交均价'
];
const MAX_WRITE_ROWS = 5000;
const MAX_WRITE_COLUMNS = 100;

const STATUS_BY_COLOR = {
  '#ff0000': '已签约',
  '#d2691e': '网上联机备案',
  '#ffcc99': '已预订',
  '#33cc00': '可售',
  '#cccccc': '不可售',
  '#ffff00': '已办理预售项目抵押',
  '#00ffff': '资格核验中'
};

const SIGNED_LIKE_STATUSES = new Set(['已签约', '网上联机备案']);

function getShanghaiDateParts(date = new Date()) {
  const formatter = new Intl.DateTimeFormat('sv-SE', {
    timeZone: 'Asia/Shanghai',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false
  });
  return Object.fromEntries(
    formatter.formatToParts(date).filter(part => part.type !== 'literal').map(part => [part.type, part.value])
  );
}

function nowShanghaiString() {
  const parts = getShanghaiDateParts();
  return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}:${parts.second}`;
}

function normalizeWhitespace(value) {
  return String(value || '')
    .replace(/\u00a0/g, ' ')
    .replace(/&nbsp;/gi, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function normalizeColor(color) {
  return normalizeWhitespace(color).toLowerCase();
}

function normalizeKeyPart(value) {
  return normalizeWhitespace(value).replace(/\s+/g, '');
}

function decodeHtmlEntities(input) {
  return String(input || '')
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&quot;/gi, '"')
    .replace(/&#39;/gi, "'")
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/&#(\d+);/g, (_, code) => {
      const num = Number(code);
      return Number.isFinite(num) ? String.fromCharCode(num) : _;
    })
    .replace(/&#x([\da-fA-F]+);/g, (_, code) => {
      const num = parseInt(code, 16);
      return Number.isFinite(num) ? String.fromCharCode(num) : _;
    });
}

function stripTags(html) {
  return normalizeWhitespace(decodeHtmlEntities(String(html || '').replace(/<[^>]+>/g, ' ')));
}

function htmlToText(html) {
  return normalizeWhitespace(
    decodeHtmlEntities(
      String(html || '')
        .replace(/<script[\s\S]*?<\/script>/gi, ' ')
        .replace(/<style[\s\S]*?<\/style>/gi, ' ')
        .replace(/<\/(td|tr|div|p|li|table|h\d|br)>/gi, '\n')
        .replace(/<br\s*\/?>/gi, '\n')
        .replace(/<[^>]+>/g, ' ')
    )
      .replace(/\r/g, '\n')
      .replace(/\n[ \t]+/g, '\n')
      .replace(/[ \t]+\n/g, '\n')
      .replace(/\n{2,}/g, '\n')
  );
}

function ensureParentDir(filePath) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
}

function readJson(filePath, fallback) {
  try {
    if (!fs.existsSync(filePath)) return fallback;
    return JSON.parse(fs.readFileSync(filePath, 'utf8'));
  } catch (error) {
    return fallback;
  }
}

function writeJson(filePath, value) {
  ensureParentDir(filePath);
  fs.writeFileSync(filePath, `${JSON.stringify(value, null, 2)}\n`, 'utf8');
}

function normalizeTimestampString(value) {
  const text = normalizeWhitespace(value);
  if (!text) return '';
  const directMatch = text.match(/^(\d{4}-\d{2}-\d{2})[T\s](\d{2}:\d{2}:\d{2})/);
  if (directMatch) return `${directMatch[1]} ${directMatch[2]}`;
  const date = new Date(text);
  if (Number.isNaN(date.getTime())) return text;
  const parts = getShanghaiDateParts(date);
  return `${parts.year}-${parts.month}-${parts.day} ${parts.hour}:${parts.minute}:${parts.second}`;
}

function compareNatural(a, b) {
  return String(a ?? '').localeCompare(String(b ?? ''), 'zh-CN', { numeric: true, sensitivity: 'base' });
}

function sortLedgerRows(rows) {
  return [...rows].sort((left, right) => {
    return compareNatural(left['地块名'], right['地块名'])
      || compareNatural(normalizeTimestampString(left['更新时间']), normalizeTimestampString(right['更新时间']))
      || compareNatural(left['销售楼号'], right['销售楼号'])
      || compareNatural(left['自然楼层'], right['自然楼层'])
      || compareNatural(left['房号'], right['房号']);
  });
}

function normalizeLedgerRows(rows) {
  return rows.map(row => ({
    ...row,
    '更新时间': normalizeTimestampString(row['更新时间'])
  }));
}

function roomKey({ projectName, buildingName, naturalFloor, roomNo }) {
  return [projectName, buildingName, naturalFloor, roomNo].map(normalizeKeyPart).join('||');
}

function roomKeyCandidates({ projectName, buildingName, naturalFloor, roomNo, buildingId }) {
  const names = new Set([buildingName]);
  if (buildingId) names.add(`building-${buildingId}`);
  return [...names].filter(Boolean).map(name => roomKey({ projectName, buildingName: name, naturalFloor, roomNo }));
}

function hasExistingRoomKey(existingKeys, room) {
  return roomKeyCandidates(room).some(key => existingKeys.has(key));
}

function getExistingRoomKeySet(rows) {
  const keys = new Set();
  for (const row of rows) {
    for (const key of roomKeyCandidates({
      projectName: row['地块名'],
      buildingName: row['销售楼号'],
      naturalFloor: row['自然楼层'],
      roomNo: row['房号']
    })) {
      keys.add(key);
    }
  }
  return keys;
}

function cacheRoomKey({ projectName, buildingName, naturalFloor, roomNo }) {
  return roomKey({ projectName, buildingName, naturalFloor, roomNo });
}

function parseNumber(value) {
  const cleaned = String(value || '').replace(/,/g, '').trim();
  const direct = Number(cleaned);
  if (Number.isFinite(direct)) return direct;
  const match = cleaned.match(/-?\d+(?:\.\d+)?/);
  if (!match) return null;
  const num = Number(match[0]);
  return Number.isFinite(num) ? num : null;
}

function round2(value) {
  return Math.round((value + Number.EPSILON) * 100) / 100;
}

function formatMoney(value) {
  return Number(value || 0).toFixed(2);
}

function parseProjectFieldFromHtml(html, label) {
  const escaped = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const pattern = new RegExp(
    `<tr[^>]*class="${escaped}"[^>]*>[\\s\\S]*?<td[^>]*>[^<]*${escaped}[^<]*<\\/td>[\\s\\S]*?<td[^>]*>([\\s\\S]*?)<\\/td>[\\s\\S]*?<\\/tr>`,
    'i'
  );
  const match = String(html || '').match(pattern);
  return match ? stripTags(match[1]) : null;
}

function parseProjectSummary(html) {
  const text = htmlToText(html);
  const projectName = parseProjectFieldFromHtml(html, '项目名称');
  const salePermitNumber = parseProjectFieldFromHtml(html, '预售许可证编号');
  const statMatch = text.match(/期房签约统计[\s\S]*?住宅\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)\s+(\d+(?:\.\d+)?)/);
  if (!statMatch) throw new Error('未能从项目详情页解析“期房签约统计”');
  return {
    projectName,
    salePermitNumber,
    signedUnits: parseNumber(statMatch[1]) ?? 0,
    signedArea: parseNumber(statMatch[2]) ?? 0,
    averagePrice: parseNumber(statMatch[3]) ?? 0
  };
}

function absolutizeUrl(url, base = BASE_URL) {
  return new URL(url, base).toString();
}

function extractBuildingUrls(html, baseUrl) {
  const urls = new Set();
  const regex = /href="([^"]*pageId=320833[^"]*buildingId=\d+[^"]*)"/gi;
  let match;
  while ((match = regex.exec(html)) !== null) urls.add(absolutizeUrl(match[1], baseUrl));
  return urls;
}

function extractMoreBuildingListUrl(html, baseUrl) {
  const match = html.match(/href="([^"]*pageId=411612[^"]*)"[^>]*>查看更多&gt;&gt;<\/a>/i)
    || html.match(/href="([^"]*pageId=411612[^"]*)"/i);
  return match ? absolutizeUrl(match[1], baseUrl) : null;
}

function parseTotalRecords(html) {
  const match = html.match(/总记录数\s*:?\s*(\d+)/);
  return match ? Number(match[1]) : null;
}

function parsePageSize(html) {
  const match = html.match(/每页显示\s*(\d+)/);
  return match ? Number(match[1]) : 20;
}

async function fetchText(url, options = {}, retries = 3) {
  let lastError;
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 25000);
    try {
      const response = await fetch(url, {
        redirect: 'follow',
        signal: controller.signal,
        ...options,
        headers: {
          'user-agent': 'Mozilla/5.0 (OpenClaw Skill Tracker)',
          ...(options.headers || {})
        }
      });
      const text = await response.text();
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      clearTimeout(timeout);
      return text;
    } catch (error) {
      clearTimeout(timeout);
      lastError = error;
      if (attempt < retries) await new Promise(resolve => setTimeout(resolve, attempt * 1500));
    }
  }
  throw lastError;
}

async function fetchAllBuildingPageUrls(projectHtml, projectUrl) {
  const urls = new Set(extractBuildingUrls(projectHtml, projectUrl));
  const moreUrl = extractMoreBuildingListUrl(projectHtml, projectUrl);
  if (!moreUrl) return [...urls];

  const firstPageHtml = await fetchText(moreUrl);
  for (const url of extractBuildingUrls(firstPageHtml, moreUrl)) urls.add(url);

  const totalRecords = parseTotalRecords(firstPageHtml) || urls.size;
  const pageSize = parsePageSize(firstPageHtml) || 20;
  const totalPages = Math.max(1, Math.ceil(totalRecords / pageSize));

  for (let currentPage = 2; currentPage <= totalPages; currentPage += 1) {
    const body = new URLSearchParams({ currentPage: String(currentPage), pageSize: String(pageSize) }).toString();
    const pageHtml = await fetchText(moreUrl, {
      method: 'POST',
      headers: { 'content-type': 'application/x-www-form-urlencoded' },
      body
    });
    for (const url of extractBuildingUrls(pageHtml, moreUrl)) urls.add(url);
  }

  return [...urls];
}

function parseBuildingIdFromUrl(url) {
  const match = String(url || '').match(/buildingId=(\d+)/i);
  return match ? match[1] : '';
}

function parseBuildingName(html, fallbackUrl) {
  const text = htmlToText(html);
  for (const pattern of [/([^\s]+#住宅楼)\s*楼盘表/, /([^\s]+号楼)\s*楼盘表/]) {
    const match = text.match(pattern);
    if (match) return normalizeWhitespace(match[1]);
  }
  const spanMatch = String(html || '').match(/<span>\s*([^<\s]+(?:#住宅楼|号楼))\s*&nbsp;\s*楼盘表\s*<\/span>/i);
  if (spanMatch) return normalizeWhitespace(decodeHtmlEntities(spanMatch[1]));
  const buildingId = parseBuildingIdFromUrl(fallbackUrl);
  return buildingId ? `building-${buildingId}` : '未知楼栋';
}

function parseRoomsFromBuildingPage(html, buildingUrl) {
  const buildingId = parseBuildingIdFromUrl(buildingUrl);
  const buildingName = parseBuildingName(html, buildingUrl);
  const tableMatch = html.match(/<table[^>]*id="table_Buileing"[^>]*>([\s\S]*?)<\/table>/i);
  if (!tableMatch) return { buildingName, rooms: [] };
  const tableHtml = tableMatch[1];
  const rowRegex = /<tr>\s*<td[^>]*>\s*([^<]+?)\s*<\/td>\s*<td[^>]*>\s*([\s\S]*?)\s*<\/td>\s*<td[^>]*>([\s\S]*?)<\/td>\s*<\/tr>/gi;
  const rooms = [];
  let rowMatch;
  while ((rowMatch = rowRegex.exec(tableHtml)) !== null) {
    const naturalFloor = stripTags(rowMatch[1]);
    if (!naturalFloor || naturalFloor.includes('自然楼层')) continue;
    const roomCellHtml = rowMatch[3];
    const roomRegex = /<div[^>]*style="[^"]*background:\s*([^;\"]+)[^"]*"[^>]*>[\s\S]*?<a[^>]*href="([^"]*)"[^>]*>([^<]+)<\/a>/gi;
    let roomMatch;
    while ((roomMatch = roomRegex.exec(roomCellHtml)) !== null) {
      const color = normalizeColor(roomMatch[1]);
      const status = STATUS_BY_COLOR[color] || '未知状态';
      const roomNo = stripTags(roomMatch[3]);
      const href = normalizeWhitespace(decodeHtmlEntities(roomMatch[2] || ''));
      rooms.push({
        buildingName,
        naturalFloor,
        roomNo,
        status,
        houseUrl: href && href !== '#' ? absolutizeUrl(href, buildingUrl) : null,
        buildingId
      });
    }
  }
  return { buildingName, rooms };
}

function parseHouseDetail(html) {
  const rowRegex = /<tr[^>]*>[\s\S]*?<td[^>]*id="desc"[^>]*>([\s\S]*?)<\/td>[\s\S]*?<td[^>]*id="desc"[^>]*>([\s\S]*?)<\/td>[\s\S]*?<\/tr>/gi;
  const fields = new Map();
  let match;
  while ((match = rowRegex.exec(String(html || ''))) !== null) {
    const key = normalizeWhitespace(stripTags(match[1])).replace(/\s+/g, '');
    const value = stripTags(match[2]);
    if (key) fields.set(key, value);
  }
  const roomType = fields.get('户型') || fields.get('户　　型') || '';
  const builtArea = parseNumber(fields.get('建筑面积') || '');
  return {
    roomType,
    builtArea: builtArea ?? null
  };
}

function normalizeProjectEntry(project = {}) {
  const normalizedName = normalizeWhitespace(project.name);
  const rawUrls = Array.isArray(project.urls) ? project.urls : [project.url];
  const urls = [...new Set(rawUrls.map(normalizeWhitespace).filter(Boolean))];
  return { name: normalizedName, urls, updatedAt: normalizeWhitespace(project.updatedAt) || nowShanghaiString() };
}

function mergeProjectEntries(projects = []) {
  const merged = new Map();
  for (const project of projects) {
    const normalized = normalizeProjectEntry(project);
    if (!normalized.name || !normalized.urls.length) continue;
    const existing = merged.get(normalized.name);
    if (!existing) merged.set(normalized.name, normalized);
    else {
      existing.urls = [...new Set([...existing.urls, ...normalized.urls])];
      if (compareNatural(existing.updatedAt, normalized.updatedAt) < 0) existing.updatedAt = normalized.updatedAt;
    }
  }
  return [...merged.values()];
}

function getProjectUrls(project) {
  return normalizeProjectEntry(project).urls;
}

function loadConfig(configPath) {
  const config = readJson(configPath, { projects: [] });
  return {
    feishu: typeof config.feishu === 'object' && config.feishu ? config.feishu : {},
    projects: mergeProjectEntries(Array.isArray(config.projects) ? config.projects : [])
  };
}

function saveConfig(configPath, config) {
  writeJson(configPath, { ...config, projects: mergeProjectEntries(config.projects) });
}

function loadRoomCache(cachePath = DETAILS_CACHE_PATH) {
  const raw = readJson(cachePath, { rooms: {} });
  return raw && typeof raw.rooms === 'object' ? raw : { rooms: {} };
}

function saveRoomCache(cache, cachePath = DETAILS_CACHE_PATH) {
  writeJson(cachePath, cache);
}

function upsertProject(config, name, url) {
  const normalizedName = normalizeWhitespace(name);
  const normalizedUrl = normalizeWhitespace(url);
  const updatedAt = nowShanghaiString();
  const existingIndex = config.projects.findIndex(item => item.name === normalizedName);
  if (existingIndex >= 0) {
    const existing = normalizeProjectEntry(config.projects[existingIndex]);
    existing.urls = [...new Set([...existing.urls, normalizedUrl])];
    existing.updatedAt = updatedAt;
    config.projects[existingIndex] = existing;
    return existing;
  }
  const project = { name: normalizedName, urls: [normalizedUrl], updatedAt };
  config.projects.push(project);
  return project;
}

function removeProject(config, name) {
  const before = config.projects.length;
  config.projects = config.projects.filter(project => project.name !== name);
  return config.projects.length !== before;
}

function updateFeishuConfig(config, input) {
  config.feishu = { ...(config.feishu || {}), ...input, updatedAt: nowShanghaiString() };
  return config.feishu;
}

function getLatestProjectSnapshot(rows, projectName) {
  const projectRows = rows.filter(row => row['地块名'] === projectName);
  if (!projectRows.length) return { signedUnits: 0, signedArea: 0, averagePrice: 0, updatedAt: null };
  const latestRow = sortLedgerRows(normalizeLedgerRows(projectRows)).at(-1);
  const signedUnits = Number(latestRow['项目已签约套数'] || 0);
  const signedArea = Number(latestRow['已签约面积(M2)'] || 0);
  const averagePrice = Number(latestRow['项目成交均价'] || 0);
  return {
    signedUnits: Number.isFinite(signedUnits) ? signedUnits : 0,
    signedArea: Number.isFinite(signedArea) ? signedArea : 0,
    averagePrice: Number.isFinite(averagePrice) ? averagePrice : 0,
    updatedAt: latestRow['更新时间'] || null
  };
}

function computeEstimatedAveragePrice(previousSignedArea, previousAveragePrice, currentSignedArea, currentAveragePrice) {
  const deltaArea = currentSignedArea - previousSignedArea;
  if (deltaArea <= 0) return null;
  const value = ((currentSignedArea * currentAveragePrice) - (previousSignedArea * previousAveragePrice)) / deltaArea;
  return round2(value);
}

function encodeSheetRange(range) {
  return encodeURIComponent(range).replace(/%21/g, '!').replace(/%3A/g, ':').replace(/%2C/g, ',');
}

function matrixRowToLedgerRow(values = [], header = LEDGER_COLUMNS) {
  const row = {};
  header.forEach((column, index) => {
    row[column] = normalizeWhitespace(values[index]);
  });
  return migrateLegacyLedgerRow(row);
}

function migrateLegacyLedgerRow(row = {}) {
  if ('已签约面积(M2)' in row) {
    const normalized = {};
    for (const column of LEDGER_COLUMNS) normalized[column] = normalizeWhitespace(row[column]);
    return normalized;
  }
  return {
    '地块名': normalizeWhitespace(row['地块名']),
    '销售楼号': normalizeWhitespace(row['销售楼号']),
    '自然楼层': normalizeWhitespace(row['自然楼层']),
    '房号': normalizeWhitespace(row['房号']),
    '建筑面积': '',
    '户型': '',
    '估计成交价': normalizeWhitespace(row['估计成交价']),
    '项目已签约套数': normalizeWhitespace(row['项目已签约套数']),
    '已签约面积(M2)': '',
    '项目成交均价': normalizeWhitespace(row['项目成交均价']),
    '更新时间': normalizeWhitespace(row['更新时间'])
  };
}

function ledgerRowToMatrixRow(row) {
  return LEDGER_COLUMNS.map(header => String(row?.[header] ?? ''));
}

function isHeaderRow(values = [], header = LEDGER_COLUMNS) {
  return header.every((column, index) => normalizeWhitespace(values[index]) === column);
}

function parseSpreadsheetToken(input) {
  const text = normalizeWhitespace(input);
  if (!text) return '';
  try {
    const url = new URL(text);
    const match = url.pathname.match(/\/sheets\/([^/?#]+)/);
    return match ? match[1] : text;
  } catch (error) {
    return text;
  }
}

function maskSecret(value) {
  const text = normalizeWhitespace(value);
  if (!text) return '(未配置)';
  if (text.length <= 8) return `${text.slice(0, 2)}***`;
  return `${text.slice(0, 4)}***${text.slice(-4)}`;
}

function getOption(options, key, fallback = '') {
  return normalizeWhitespace(options[key] || fallback);
}

function resolveFeishuConfig(config, options) {
  const sheetUrl = getOption(options, 'sheet-url', process.env.FEISHU_SHEET_URL || config.feishu?.sheetUrl || '');
  const spreadsheetToken = parseSpreadsheetToken(getOption(options, 'spreadsheet-token', config.feishu?.spreadsheetToken || sheetUrl));
  const appId = getOption(options, 'app-id', process.env.FEISHU_APP_ID || config.feishu?.appId || '');
  const appSecret = getOption(options, 'app-secret', process.env.FEISHU_APP_SECRET || config.feishu?.appSecret || '');
  const sheetId = getOption(options, 'sheet-id', config.feishu?.sheetId || '');
  const sheetTitle = getOption(options, 'sheet-title', config.feishu?.sheetTitle || '');
  const notifyUserOpenId = getOption(options, 'notify-user-open-id', process.env.FEISHU_NOTIFY_USER_OPEN_ID || config.feishu?.notifyUserOpenId || '');
  return { sheetUrl, spreadsheetToken, appId, appSecret, sheetId, sheetTitle, notifyUserOpenId };
}

async function fetchJson(url, options = {}, retries = 3) {
  let lastError;
  for (let attempt = 1; attempt <= retries; attempt += 1) {
    const controller = new AbortController();
    const timeout = setTimeout(() => controller.abort(), 25000);
    try {
      const response = await fetch(url, {
        signal: controller.signal,
        ...options,
        headers: {
          'user-agent': 'Mozilla/5.0 (OpenClaw Skill Tracker)',
          ...(options.body ? { 'content-type': 'application/json; charset=utf-8' } : {}),
          ...(options.headers || {})
        }
      });
      const text = await response.text();
      const json = text ? JSON.parse(text) : {};
      if (!response.ok || Number(json.code || 0) !== 0) {
        const error = new Error(json?.msg || `HTTP ${response.status}`);
        error.response = json;
        error.status = response.status;
        throw error;
      }
      clearTimeout(timeout);
      return json;
    } catch (error) {
      clearTimeout(timeout);
      lastError = error;
      if (attempt < retries) await new Promise(resolve => setTimeout(resolve, attempt * 1500));
    }
  }
  throw lastError;
}

async function getTenantAccessToken(appId, appSecret) {
  if (!appId || !appSecret) throw new Error('缺少飞书 app_id 或 app_secret，请在配置文件、环境变量或命令参数中提供');
  const json = await fetchJson(`${FEISHU_BASE_URL}/open-apis/auth/v3/tenant_access_token/internal`, {
    method: 'POST',
    body: JSON.stringify({ app_id: appId, app_secret: appSecret })
  });
  return json.tenant_access_token;
}

function buildFeishuAuthHeaders(accessToken) {
  return { Authorization: `Bearer ${accessToken}` };
}

async function querySpreadsheetSheets(spreadsheetToken, accessToken) {
  const json = await fetchJson(`${FEISHU_BASE_URL}/open-apis/sheets/v3/spreadsheets/${spreadsheetToken}/sheets/query`, {
    method: 'GET', headers: buildFeishuAuthHeaders(accessToken)
  });
  return Array.isArray(json?.data?.sheets) ? json.data.sheets : [];
}

function formatRowAsMobileText(row) {
  return [
    `楼号：${row?.['销售楼号'] ?? ''}`,
    `楼层：${row?.['自然楼层'] ?? ''}`,
    `房号：${row?.['房号'] ?? ''}`,
    `面积：${row?.['建筑面积'] ?? ''}`,
    `户型：${row?.['户型'] ?? ''}`,
    `估计成交价：${row?.['估计成交价'] ?? ''}`,
    `项目签约套数：${row?.['项目已签约套数'] ?? ''}`,
    `项目签约面积：${row?.['已签约面积(M2)'] ?? ''}`,
    `项目均价：${row?.['项目成交均价'] ?? ''}`,
    `更新时间：${row?.['更新时间'] ?? ''}`
  ].join('\n');
}

function groupRowsByProject(rows) {
  const groups = new Map();
  for (const row of rows) {
    const name = String(row?.['地块名'] ?? '').trim() || '未命名地块';
    if (!groups.has(name)) groups.set(name, []);
    groups.get(name).push(row);
  }
  return Array.from(groups.entries()).map(([name, groupedRows]) => ({ name, rows: groupedRows }));
}

function formatRowsAsMobileText(rows) {
  return groupRowsByProject(rows).map(({ name, rows: groupedRows }) => {
    const firstRow = groupedRows[0] || {};
    const header = [
      `=== ${name}（${groupedRows.length} 套） ===`,
      `项目签约：${firstRow['项目已签约套数'] ?? ''}`,
      `签约面积：${firstRow['已签约面积(M2)'] ?? ''}`,
      `项目均价：${firstRow['项目成交均价'] ?? ''}`
    ].join('\n');
    const body = groupedRows.map((row, index) => `【新增 ${index + 1}】\n${formatRowAsMobileText(row)}`).join('\n\n');
    return `${header}\n${body}`;
  }).join('\n\n');
}

function chunkNotificationRows(rows, maxChars = 2500) {
  const chunks = [];
  let current = [];
  let currentLength = 0;
  for (const row of rows) {
    const rowText = formatRowAsMobileText(row);
    const nextLength = currentLength + (current.length ? 4 : 0) + rowText.length;
    if (current.length && nextLength > maxChars) {
      chunks.push(current);
      current = [];
      currentLength = 0;
    }
    current.push(row);
    currentLength += (current.length > 1 ? 4 : 0) + rowText.length;
  }
  if (current.length) chunks.push(current);
  return chunks;
}

async function sendFeishuTextMessage(accessToken, receiveId, text) {
  return fetchJson(`${FEISHU_BASE_URL}/open-apis/im/v1/messages?receive_id_type=open_id`, {
    method: 'POST',
    headers: buildFeishuAuthHeaders(accessToken),
    body: JSON.stringify({ receive_id: receiveId, msg_type: 'text', content: JSON.stringify({ text }) })
  });
}

async function sendSyncStatusNotification(accessToken, notifyUserOpenId, rows, reports) {
  if (!notifyUserOpenId) return { sent: false, messageCount: 0 };
  const normalizedRows = sortLedgerRows(normalizeLedgerRows(rows));
  if (normalizedRows.length) {
    const rowChunks = chunkNotificationRows(normalizedRows);
    for (const [index, chunk] of rowChunks.entries()) {
      const title = rowChunks.length === 1
        ? `北京住建委签约更新：新增 ${normalizedRows.length} 行\n`
        : `北京住建委签约更新：新增 ${normalizedRows.length} 行（第 ${index + 1}/${rowChunks.length} 条消息）\n`;
      await sendFeishuTextMessage(accessToken, notifyUserOpenId, `${title}${formatRowsAsMobileText(chunk)}`);
    }
    return { sent: true, messageCount: rowChunks.length };
  }
  const lines = ['北京住建委签约更新', '状态：本次无新增签约'];
  for (const report of reports || []) {
    lines.push(`- ${report.projectName}：签约套数 ${report.currentSignedUnits}，签约面积 ${formatMoney(report.currentSignedArea)}，新增房号 ${report.newRoomsFound}`);
  }
  await sendFeishuTextMessage(accessToken, notifyUserOpenId, lines.join('\n'));
  return { sent: true, messageCount: 1 };
}

function pickTargetSheet(sheets, preferredSheetId, preferredSheetTitle) {
  if (!sheets.length) throw new Error('目标飞书表格中没有可用工作表');
  if (preferredSheetId) {
    const matched = sheets.find(sheet => sheet.sheet_id === preferredSheetId);
    if (!matched) throw new Error(`未找到指定 sheet_id: ${preferredSheetId}`);
    return matched;
  }
  if (preferredSheetTitle) {
    const matched = sheets.find(sheet => normalizeWhitespace(sheet.title) === preferredSheetTitle);
    if (!matched) throw new Error(`未找到指定工作表标题: ${preferredSheetTitle}`);
    return matched;
  }
  return sheets.find(sheet => !sheet.hidden) || sheets[0];
}

async function readSheetMatrix(spreadsheetToken, sheetId, accessToken) {
  const range = `${sheetId}!A:K`;
  const url = `${FEISHU_BASE_URL}/open-apis/sheets/v2/spreadsheets/${spreadsheetToken}/values/${encodeSheetRange(range)}?valueRenderOption=ToString&dateTimeRenderOption=FormattedString`;
  const json = await fetchJson(url, { method: 'GET', headers: { ...buildFeishuAuthHeaders(accessToken), 'content-type': 'application/json; charset=utf-8' } });
  return Array.isArray(json?.data?.valueRange?.values) ? json.data.valueRange.values : [];
}

async function writeSheetRange(spreadsheetToken, accessToken, range, values) {
  if (!values.length) return;
  if (values.length > MAX_WRITE_ROWS) throw new Error(`单次写入行数超过限制 ${MAX_WRITE_ROWS}`);
  if (values[0].length > MAX_WRITE_COLUMNS) throw new Error(`单次写入列数超过限制 ${MAX_WRITE_COLUMNS}`);
  await fetchJson(`${FEISHU_BASE_URL}/open-apis/sheets/v2/spreadsheets/${spreadsheetToken}/values`, {
    method: 'PUT', headers: buildFeishuAuthHeaders(accessToken), body: JSON.stringify({ valueRange: { range, values } })
  });
}

async function appendSheetRows(spreadsheetToken, accessToken, sheetId, rows) {
  if (!rows.length) return;
  await fetchJson(`${FEISHU_BASE_URL}/open-apis/sheets/v2/spreadsheets/${spreadsheetToken}/values_append?insertDataOption=INSERT_ROWS`, {
    method: 'POST', headers: buildFeishuAuthHeaders(accessToken), body: JSON.stringify({ valueRange: { range: `${sheetId}!A:K`, values: rows } })
  });
}

async function rewriteSheetSorted(spreadsheetToken, accessToken, sheetId, allRows) {
  const matrix = [LEDGER_COLUMNS, ...allRows.map(ledgerRowToMatrixRow)];
  for (let offset = 0; offset < matrix.length; offset += MAX_WRITE_ROWS) {
    const chunk = matrix.slice(offset, offset + MAX_WRITE_ROWS);
    const startRow = offset + 1;
    const endRow = startRow + chunk.length - 1;
    const range = `${sheetId}!A${startRow}:K${endRow}`;
    await writeSheetRange(spreadsheetToken, accessToken, range, chunk);
  }
}

function parseLedgerRowsFromSheet(matrix) {
  if (!matrix.length) return { rows: [], hasHeader: false };
  const header = matrix[0].map(cell => normalizeWhitespace(cell));
  if (isHeaderRow(header, LEDGER_COLUMNS)) {
    const rows = matrix.slice(1).filter(row => row.some(cell => normalizeWhitespace(cell))).map(row => matrixRowToLedgerRow(row, LEDGER_COLUMNS));
    return { rows, hasHeader: true, header: LEDGER_COLUMNS };
  }
  if (isHeaderRow(header, LEGACY_LEDGER_COLUMNS)) {
    const rows = matrix.slice(1).filter(row => row.some(cell => normalizeWhitespace(cell))).map(row => matrixRowToLedgerRow(row, LEGACY_LEDGER_COLUMNS));
    return { rows, hasHeader: true, header: LEGACY_LEDGER_COLUMNS, migrated: true };
  }
  throw new Error('飞书表格首行不是预期表头，也不是旧版表头，请先修正后再同步');
}

async function ensureSheetHeader(spreadsheetToken, accessToken, sheetId, matrix) {
  if (!matrix.length) {
    await writeSheetRange(spreadsheetToken, accessToken, `${sheetId}!A1:K1`, [LEDGER_COLUMNS]);
    return { created: true, migrated: false };
  }
  const header = matrix[0].map(cell => normalizeWhitespace(cell));
  if (isHeaderRow(header, LEDGER_COLUMNS)) return { created: false, migrated: false };
  if (isHeaderRow(header, LEGACY_LEDGER_COLUMNS)) return { created: false, migrated: true };
  throw new Error('飞书表格首行不是预期表头，且已存在数据，已停止以避免破坏历史数据');
}

async function warmRoomCache(projectName, rooms, cache) {
  for (const room of rooms) {
    if (!room.houseUrl) continue;
    if (SIGNED_LIKE_STATUSES.has(room.status)) continue;
    const key = cacheRoomKey({ projectName, buildingName: room.buildingName, naturalFloor: room.naturalFloor, roomNo: room.roomNo });
    const existing = cache.rooms[key];
    if (existing?.builtArea && existing?.roomType) continue;
    try {
      const html = await fetchText(room.houseUrl);
      const detail = parseHouseDetail(html);
      cache.rooms[key] = {
        projectName,
        buildingName: room.buildingName,
        naturalFloor: room.naturalFloor,
        roomNo: room.roomNo,
        builtArea: detail.builtArea === null ? '' : String(detail.builtArea),
        roomType: detail.roomType || '',
        statusWhenCached: room.status,
        sourceUrl: room.houseUrl,
        updatedAt: nowShanghaiString()
      };
    } catch (error) {
      // ignore single-room cache misses
    }
  }
}

async function syncOneProject(project, existingRows, existingKeys, cache) {
  const sourceUrls = getProjectUrls(project);
  if (!sourceUrls.length) throw new Error(`项目 ${project.name || '未命名地块'} 没有可用链接`);

  const projectName = project.name || '未命名地块';
  const sourceSummaries = [];
  const buildingUrlSet = new Set();
  const salePermitNumbers = new Set();
  const skippedSources = [];

  for (const sourceUrl of sourceUrls) {
    try {
      const projectHtml = await fetchText(sourceUrl);
      const summary = parseProjectSummary(projectHtml);
      sourceSummaries.push(summary);
      if (summary.salePermitNumber) salePermitNumbers.add(summary.salePermitNumber);
      const buildingUrls = await fetchAllBuildingPageUrls(projectHtml, sourceUrl);
      for (const buildingUrl of buildingUrls) buildingUrlSet.add(buildingUrl);
    } catch (error) {
      skippedSources.push({ url: sourceUrl, reason: error.message });
    }
  }

  if (!sourceSummaries.length) {
    throw new Error(`该地块下 ${sourceUrls.length} 个链接都无法解析；最后错误：${skippedSources.at(-1)?.reason || '未知错误'}`);
  }

  const allRooms = [];
  for (const buildingUrl of buildingUrlSet) {
    const buildingHtml = await fetchText(buildingUrl);
    const { rooms } = parseRoomsFromBuildingPage(buildingHtml, buildingUrl);
    allRooms.push(...rooms);
  }

  const uniqueRooms = [];
  const seen = new Set();
  for (const room of allRooms) {
    const key = roomKey({ projectName, buildingName: room.buildingName, naturalFloor: room.naturalFloor, roomNo: room.roomNo });
    if (seen.has(key)) continue;
    seen.add(key);
    uniqueRooms.push(room);
  }

  await warmRoomCache(projectName, uniqueRooms, cache);

  const signedRooms = uniqueRooms.filter(room => SIGNED_LIKE_STATUSES.has(room.status));
  const previousSnapshot = getLatestProjectSnapshot(existingRows, projectName);
  const currentSignedUnits = sourceSummaries.reduce((sum, summary) => sum + Number(summary.signedUnits || 0), 0);
  const currentSignedArea = round2(sourceSummaries.reduce((sum, summary) => sum + Number(summary.signedArea || 0), 0));
  const weightedAverageSum = sourceSummaries.reduce((sum, summary) => sum + (Number(summary.signedArea || 0) * Number(summary.averagePrice || 0)), 0);
  const currentAveragePrice = currentSignedArea > 0 ? round2(weightedAverageSum / currentSignedArea) : 0;
  const deltaSignedUnits = currentSignedUnits - previousSnapshot.signedUnits;
  const deltaSignedArea = round2(currentSignedArea - previousSnapshot.signedArea);
  const estimatedAveragePrice = computeEstimatedAveragePrice(
    previousSnapshot.signedArea,
    previousSnapshot.averagePrice,
    currentSignedArea,
    currentAveragePrice
  );

  const newRooms = signedRooms.filter(room => !hasExistingRoomKey(existingKeys, {
    projectName,
    buildingName: room.buildingName,
    naturalFloor: room.naturalFloor,
    roomNo: room.roomNo,
    buildingId: room.buildingId
  }));

  const updateTime = nowShanghaiString();
  const appendRows = [];
  if (estimatedAveragePrice !== null) {
    for (const room of newRooms) {
      const cached = cache.rooms[cacheRoomKey({
        projectName,
        buildingName: room.buildingName,
        naturalFloor: room.naturalFloor,
        roomNo: room.roomNo
      })] || {};
      const row = {
        '地块名': projectName,
        '销售楼号': room.buildingName,
        '自然楼层': room.naturalFloor,
        '房号': room.roomNo,
        '建筑面积': normalizeWhitespace(cached.builtArea),
        '户型': normalizeWhitespace(cached.roomType),
        '估计成交价': formatMoney(estimatedAveragePrice),
        '项目已签约套数': String(currentSignedUnits),
        '已签约面积(M2)': formatMoney(currentSignedArea),
        '项目成交均价': formatMoney(currentAveragePrice),
        '更新时间': updateTime
      };
      appendRows.push(row);
      for (const key of roomKeyCandidates({
        projectName,
        buildingName: room.buildingName,
        naturalFloor: room.naturalFloor,
        roomNo: room.roomNo,
        buildingId: room.buildingId
      })) existingKeys.add(key);
    }
  }

  return {
    projectName,
    salePermitNumber: [...salePermitNumbers].join(', '),
    sourceCount: sourceUrls.length,
    buildingCount: buildingUrlSet.size,
    trackedSignedRooms: signedRooms.length,
    previousSignedUnits: previousSnapshot.signedUnits,
    currentSignedUnits,
    previousSignedArea: previousSnapshot.signedArea,
    currentSignedArea,
    previousAveragePrice: previousSnapshot.averagePrice,
    currentAveragePrice,
    deltaSignedUnits,
    deltaSignedArea,
    estimatedAveragePrice,
    newRoomsFound: newRooms.length,
    appendedRows: appendRows,
    warnings: [
      ...(sourceUrls.length > 1 ? [`该地块配置了 ${sourceUrls.length} 个项目详情链接，已合并统计。`] : []),
      ...skippedSources.map(item => `已跳过链接 ${item.url}：${item.reason}`),
      ...(deltaSignedUnits < 0 || deltaSignedArea < 0 ? [`项目统计出现回退（套数 ${previousSnapshot.signedUnits}→${currentSignedUnits}，面积 ${formatMoney(previousSnapshot.signedArea)}→${formatMoney(currentSignedArea)}），未回滚历史数据。`] : []),
      ...(deltaSignedArea > 0 && estimatedAveragePrice === null ? ['签约面积有增量，但未能计算估计成交均价。'] : []),
      ...(deltaSignedUnits > 0 && deltaSignedUnits !== newRooms.length ? [`统计增量为 ${deltaSignedUnits} 套，但本次在楼盘表中发现 ${newRooms.length} 套新房号。`] : []),
      ...(deltaSignedArea <= 0 && newRooms.length > 0 ? ['楼盘表发现了历史中不存在的签约房号，但项目签约面积没有增加，已跳过以避免错误估价。'] : []),
      ...appendRows.filter(row => !row['建筑面积'] || !row['户型']).map(row => `房号 ${row['销售楼号']}/${row['自然楼层']}/${row['房号']} 没命中本地缓存，建筑面积或户型为空。`)
    ]
  };
}

function printHelp() {
  console.log(`北京住建委新签约均价追踪器（飞书表格版）

用法:
  node scripts/tracker.js set-feishu --sheet-url <飞书表格链接> --app-id <app_id> --app-secret <app_secret> [--sheet-id <sheet_id>|--sheet-title <工作表标题>] [--notify-user-open-id <open_id>]
  node scripts/tracker.js add --name <地块名> --url <项目详情链接>
  node scripts/tracker.js remove --name <地块名>
  node scripts/tracker.js list
  node scripts/tracker.js sync
  node scripts/tracker.js sync --name <地块名>
  node scripts/tracker.js sync --name <临时项目> --url <项目详情链接> --sheet-url <飞书表格链接> --app-id <app_id> --app-secret <app_secret>

可选参数:
  --config <path>        配置文件路径，默认: ${DEFAULT_CONFIG_PATH}
  --sheet-url <url>      飞书表格链接，可覆盖配置
  --spreadsheet-token <token> 飞书表格 token，可覆盖配置
  --sheet-id <id>        指定工作表 ID
  --sheet-title <title>  指定工作表标题
  --app-id <id>          飞书 app_id，可覆盖配置
  --app-secret <secret>  飞书 app_secret，可覆盖配置
  --notify-user-open-id <open_id>  执行完毕后通知的飞书私聊 open_id
  --json                 以 JSON 输出同步结果

环境变量:
  FEISHU_SHEET_URL FEISHU_APP_ID FEISHU_APP_SECRET FEISHU_NOTIFY_USER_OPEN_ID
`);
}

function parseArgs(argv) {
  const [command = 'help', ...rest] = argv;
  const options = {};
  for (let i = 0; i < rest.length; i += 1) {
    const token = rest[i];
    if (!token.startsWith('--')) continue;
    const key = token.slice(2);
    const next = rest[i + 1];
    if (!next || next.startsWith('--')) options[key] = true;
    else {
      options[key] = next;
      i += 1;
    }
  }
  return { command, options };
}

function requireFeishuConfig(feishuConfig) {
  if (!feishuConfig.spreadsheetToken) throw new Error('缺少飞书表格链接或 spreadsheet token');
  if (!feishuConfig.appId || !feishuConfig.appSecret) throw new Error('缺少飞书 app_id 或 app_secret');
}

async function main() {
  const { command, options } = parseArgs(process.argv.slice(2));
  const configPath = path.resolve(options.config || DEFAULT_CONFIG_PATH);

  if (command === 'help' || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  const config = loadConfig(configPath);

  if (command === 'set-feishu') {
    const feishuInput = resolveFeishuConfig(config, options);
    requireFeishuConfig(feishuInput);
    const saved = updateFeishuConfig(config, {
      sheetUrl: feishuInput.sheetUrl,
      spreadsheetToken: feishuInput.spreadsheetToken,
      appId: feishuInput.appId,
      appSecret: feishuInput.appSecret,
      sheetId: feishuInput.sheetId,
      sheetTitle: feishuInput.sheetTitle,
      notifyUserOpenId: feishuInput.notifyUserOpenId
    });
    saveConfig(configPath, config);
    console.log(`已保存飞书表格配置: ${saved.spreadsheetToken}`);
    if (saved.sheetId) console.log(`sheet_id: ${saved.sheetId}`);
    if (saved.sheetTitle) console.log(`sheet_title: ${saved.sheetTitle}`);
    console.log(`配置文件: ${configPath}`);
    return;
  }

  if (command === 'add') {
    if (!options.name || !options.url) throw new Error('add 命令需要同时提供 --name 和 --url');
    const project = upsertProject(config, options.name, options.url);
    saveConfig(configPath, config);
    console.log(`已保存项目映射: ${project.name} (${project.urls.length} 个链接)`);
    console.log(`配置文件: ${configPath}`);
    return;
  }

  if (command === 'remove') {
    if (!options.name) throw new Error('remove 命令需要提供 --name');
    const removed = removeProject(config, options.name);
    if (!removed) throw new Error(`未找到项目: ${options.name}`);
    saveConfig(configPath, config);
    console.log(`已移除项目: ${options.name}`);
    return;
  }

  if (command === 'list') {
    const feishuConfig = resolveFeishuConfig(config, options);
    console.log('飞书配置:');
    console.log(`- sheet_url: ${feishuConfig.sheetUrl || '(未配置)'}`);
    console.log(`- spreadsheet_token: ${feishuConfig.spreadsheetToken || '(未配置)'}`);
    console.log(`- sheet_id: ${feishuConfig.sheetId || '(未配置)'}`);
    console.log(`- sheet_title: ${feishuConfig.sheetTitle || '(未配置)'}`);
    console.log(`- app_id: ${feishuConfig.appId || '(未配置)'}`);
    console.log(`- app_secret: ${maskSecret(feishuConfig.appSecret)}`);
    console.log(`- notify_user_open_id: ${feishuConfig.notifyUserOpenId || '(未配置)'}`);
    console.log(`- room_cache: ${DETAILS_CACHE_PATH}`);
    console.log('');
    if (!config.projects.length) {
      console.log(`当前没有已配置项目。配置文件: ${configPath}`);
      return;
    }
    console.log(`已配置项目 (${config.projects.length} 个):`);
    for (const [index, project] of config.projects.entries()) {
      console.log(`${index + 1}. ${project.name} (${getProjectUrls(project).length} 个链接)`);
      for (const [urlIndex, url] of getProjectUrls(project).entries()) console.log(`   ${urlIndex + 1}) ${url}`);
    }
    return;
  }

  if (command !== 'sync') {
    printHelp();
    throw new Error(`未知命令: ${command}`);
  }

  const feishuConfig = resolveFeishuConfig(config, options);
  requireFeishuConfig(feishuConfig);

  let projectsToSync = [];
  if (options.name && options.url) projectsToSync = [{ name: options.name, url: options.url }];
  else if (options.name) {
    const matched = config.projects.find(project => project.name === options.name);
    if (!matched) throw new Error(`配置中不存在项目: ${options.name}`);
    projectsToSync = [matched];
  } else {
    projectsToSync = config.projects;
  }

  if (!projectsToSync.length) {
    console.log(`没有需要同步的项目。配置文件: ${configPath}`);
    return;
  }

  const accessToken = await getTenantAccessToken(feishuConfig.appId, feishuConfig.appSecret);
  const sheets = await querySpreadsheetSheets(feishuConfig.spreadsheetToken, accessToken);
  const targetSheet = pickTargetSheet(sheets, feishuConfig.sheetId, feishuConfig.sheetTitle);
  const matrixBefore = await readSheetMatrix(feishuConfig.spreadsheetToken, targetSheet.sheet_id, accessToken);
  await ensureSheetHeader(feishuConfig.spreadsheetToken, accessToken, targetSheet.sheet_id, matrixBefore);
  const matrix = matrixBefore.length ? matrixBefore : [LEDGER_COLUMNS];
  const parsed = parseLedgerRowsFromSheet(matrix);
  const existingRows = sortLedgerRows(normalizeLedgerRows(parsed.rows));
  const existingKeys = getExistingRoomKeySet(existingRows);
  const roomCache = loadRoomCache();

  const reports = [];
  const rowsToAppend = [];
  for (const project of projectsToSync) {
    const report = await syncOneProject(project, existingRows, existingKeys, roomCache);
    reports.push(report);
    rowsToAppend.push(...report.appendedRows);
  }

  saveRoomCache(roomCache);

  let notification = { sent: false, messageCount: 0 };
  const finalRows = sortLedgerRows(normalizeLedgerRows([...existingRows, ...rowsToAppend]));
  if (rowsToAppend.length) {
    await appendSheetRows(feishuConfig.spreadsheetToken, accessToken, targetSheet.sheet_id, rowsToAppend.map(ledgerRowToMatrixRow));
  }
  if (rowsToAppend.length || parsed.migrated) {
    await rewriteSheetSorted(feishuConfig.spreadsheetToken, accessToken, targetSheet.sheet_id, finalRows);
  }
  notification = await sendSyncStatusNotification(accessToken, feishuConfig.notifyUserOpenId, rowsToAppend, reports);

  if (options.json) {
    console.log(JSON.stringify({
      spreadsheetToken: feishuConfig.spreadsheetToken,
      sheetId: targetSheet.sheet_id,
      sheetTitle: targetSheet.title,
      roomCachePath: DETAILS_CACHE_PATH,
      appendedRows: rowsToAppend,
      appendedCount: rowsToAppend.length,
      notification,
      reports
    }, null, 2));
    return;
  }

  console.log(`飞书表格: ${feishuConfig.spreadsheetToken}`);
  console.log(`工作表: ${targetSheet.title} (${targetSheet.sheet_id})`);
  console.log(`本次新增 ${rowsToAppend.length} 行。`);
  console.log(`房源缓存: ${DETAILS_CACHE_PATH}`);
  if (feishuConfig.notifyUserOpenId) console.log(`已发送飞书通知: ${notification.sent ? `是（${notification.messageCount} 条消息）` : '否'}`);
  else console.log('未发送飞书通知: 未配置 notify_user_open_id');
  console.log('');

  for (const report of reports) {
    console.log(`=== ${report.projectName} ===`);
    if (report.salePermitNumber) console.log(`预售证: ${report.salePermitNumber}`);
    console.log(`楼栋数: ${report.buildingCount}`);
    console.log(`楼盘表中已签约/网上联机备案房号: ${report.trackedSignedRooms}`);
    console.log(`历史签约套数: ${report.previousSignedUnits}`);
    console.log(`当前签约套数: ${report.currentSignedUnits}`);
    console.log(`签约套数变化: ${report.deltaSignedUnits}`);
    console.log(`历史签约面积: ${formatMoney(report.previousSignedArea)}`);
    console.log(`当前签约面积: ${formatMoney(report.currentSignedArea)}`);
    console.log(`签约面积变化: ${formatMoney(report.deltaSignedArea)}`);
    console.log(`历史成交均价: ${formatMoney(report.previousAveragePrice)}`);
    console.log(`当前成交均价: ${formatMoney(report.currentAveragePrice)}`);
    console.log(`估计新签约均价: ${report.estimatedAveragePrice === null ? 'N/A' : formatMoney(report.estimatedAveragePrice)}`);
    console.log(`本次发现新房号: ${report.newRoomsFound}`);
    console.log(`本次追加行数: ${report.appendedRows.length}`);
    if (report.warnings.length) {
      for (const warning of report.warnings) console.log(`警告: ${warning}`);
    }
    console.log('');
  }
}

main().catch(error => {
  const maybeResponse = error?.response;
  if (maybeResponse?.code === 1310213) {
    console.error('错误: 飞书应用还没有这张表格的文档权限。请在表格右上角添加文档应用后重试。');
  }
  console.error(`错误: ${error.message}`);
  process.exit(1);
});
