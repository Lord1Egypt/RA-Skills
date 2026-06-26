/**
 * 从 BlockBeats 获取快讯并（可选）按关键词筛选，输出 JSON 数组。
 *
 * 使用方式（Node 18+，已内置 fetch）：
 *   node new.js {keyword} {limit} {maxLimit}
 *
 * 参数说明：
 * - {keyword}: 关键字字符串，多个用英文逗号分隔，如 "btc,okx"；为空或省略时不过滤
 * - {limit}:   最多返回的条数，默认 10
 * - {maxLimit}:最多抓取的原始资讯条数，默认 1000
 *
 * 行为：
 * - 如果 keyword 为空：直接返回最新资讯列表，数量不超过 limit
 * - 如果 keyword 不为空：先在最多 maxLimit 条内做关键词匹配，再返回前 limit 条匹配结果
 */

const BASE_URL = 'https://api.theblockbeats.news/v1/open-api/open-flash';
const PAGE_SIZE = 200;

/**
 * 解析命令行参数中的关键词，形式如："btc,okx,eth"
 * @returns {string[]} 小写关键词数组，若无关键词则返回空数组
 */
function getKeywordsFromArgv() {
  const raw = process.argv[2] || '';
  return raw
    .split(',')
    .map((s) => s.trim().toLowerCase())
    .filter(Boolean);
}

/**
 * 解析最多显示条数 {limit}，形式如：node new.js "btc,okx" 10
 * @returns {number} 正整数则为限制条数；否则返回默认值 10
 */
function getLimitFromArgv() {
  const raw = process.argv[3];
  if (!raw) return 10;
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) return 10;
  return Math.floor(n);
}

/**
 * 解析最多抓取条数 {maxLimit}，形式如：node new.js "btc,okx" 10 1000
 * @returns {number} 正整数则为限制条数；否则返回默认值 1000
 */
function getMaxLimitFromArgv() {
  const raw = process.argv[4];
  if (!raw) return 1000;
  const n = Number(raw);
  if (!Number.isFinite(n) || n <= 0) return 1000;
  return Math.floor(n);
}

/**
 * 获取单页快讯数据
 * @param {number} page
 * @returns {Promise<any[]>}
 */
async function fetchPage(page) {
  const url = new URL(BASE_URL);
  url.searchParams.set('page', String(page));
  url.searchParams.set('size', String(PAGE_SIZE));
  url.searchParams.set('type', 'push');
  url.searchParams.set('lang', 'cn');

  const res = await fetch(url.toString());
  if (!res.ok) {
    throw new Error(`请求失败 page=${page}, status=${res.status}`);
  }

  const json = await res.json();

  // 兼容不同的数据结构（TheBlockBeats 实际结构：{ status, message, data: { page, data: [] } }）
  if (Array.isArray(json)) return json;
  if (Array.isArray(json.data)) return json.data;
  if (json.data && Array.isArray(json.data.data)) return json.data.data;
  if (json.data && Array.isArray(json.data.list)) return json.data.list;
  if (Array.isArray(json.list)) return json.list;

  return [];
}

/**
 * 简单去除 HTML 标签并做一点点清洗
 * @param {string} html
 * @returns {string}
 */
function stripHtml(html) {
  if (typeof html !== 'string') return '';
  // 去标签
  let text = html.replace(/<[^>]*>/g, '');
  // 实体和多余空白的简单处理
  text = text
    .replace(/&nbsp;/gi, ' ')
    .replace(/&amp;/gi, '&')
    .replace(/&lt;/gi, '<')
    .replace(/&gt;/gi, '>')
    .replace(/\s+/g, ' ')
    .trim();
  return text;
}

/**
 * 将一条新闻对象中的文本字段拼接为统一字符串，用于关键词匹配
 * @param {any} item
 * @returns {string}
 */
function extractTextFromItem(item) {
  if (!item || typeof item !== 'object') return '';

  const candidateFields = [
    'title',
    'content',
    'text',
    'summary',
    'desc',
    'brief',
    'brief_content',
  ];

  const parts = [];

  for (const key of candidateFields) {
    if (typeof item[key] === 'string') {
      parts.push(stripHtml(item[key]));
    }
  }

  // 如果预设字段都拿不到，就兜底把所有 string 字段拼起来
  if (parts.length === 0) {
    for (const value of Object.values(item)) {
      if (typeof value === 'string') {
        parts.push(stripHtml(value));
      }
    }
  }

  return parts.join(' ');
}

/**
 * 把 Unix 秒时间戳（字符串或数字）转成 YYYY-MM-DD HH:mm:ss
 * @param {string|number} ts
 * @returns {string|null}
 */
function formatTimestamp(ts) {
  if (ts == null) return null;
  const n = Number(ts);
  if (!Number.isFinite(n) || n <= 0) return null;
  // API 返回的是秒，这里转成毫秒
  const d = new Date(n * 1000);
  if (Number.isNaN(d.getTime())) return null;

  const pad = (x) => String(x).padStart(2, '0');
  const year = d.getFullYear();
  const month = pad(d.getMonth() + 1);
  const day = pad(d.getDate());
  const hour = pad(d.getHours());
  const minute = pad(d.getMinutes());
  const second = pad(d.getSeconds());

  return `${year}-${month}-${day} ${hour}:${minute}:${second}`;
}

/**
 * 输出前，去掉主要文本字段里的 HTML 标签，并格式化时间戳
 * @param {any} item
 * @returns {any}
 */
function sanitizeItemForOutput(item) {
  if (!item || typeof item !== 'object') return item;
  const clone = { ...item };
  const textFields = [
    'content',
    'text',
    'summary',
    'desc',
    'brief',
    'brief_content',
  ];
  for (const key of textFields) {
    if (typeof clone[key] === 'string') {
      clone[key] = stripHtml(clone[key]);
    }
  }

  // 处理时间字段：保留原值到 *_raw，并新增格式化后的字段
  const timeFields = ['create_time', 'update_time', 'time', 'timestamp'];
  for (const key of timeFields) {
    if (clone[key] != null && clone[`${key}_formatted`] == null) {
      const formatted = formatTimestamp(clone[key]);
      if (formatted) {
        clone[`${key}_raw`] = clone[key];
        clone[key] = formatted;
      }
    }
  }

  return clone;
}

/**
 * 判断一条快讯是否匹配任意关键词
 * @param {any} item
 * @param {string[]} keywords 已经小写化的关键词数组
 * @returns {boolean}
 */
function matchItemByKeywords(item, keywords) {
  if (!keywords.length) return false;
  const text = extractTextFromItem(item).toLowerCase();
  if (!text) return false;
  return keywords.some((kw) => text.includes(kw));
}

async function main() {
  const keywords = getKeywordsFromArgv();
  const limit = getLimitFromArgv();
  const maxLimit = getMaxLimitFromArgv();

  const totalPages = Math.max(1, Math.ceil(maxLimit / PAGE_SIZE));
  const pageNumbers = Array.from({ length: totalPages }, (_, i) => i + 1);

  let allItems = [];

  try {
    const pageResults = await Promise.all(pageNumbers.map((p) => fetchPage(p)));
    for (const list of pageResults) {
      if (Array.isArray(list)) {
        allItems = allItems.concat(list);
      }
    }
  } catch (err) {
    console.error('请求过程中出现错误：', err);
  }

  // 截断到 maxLimit，避免超过用户期望的抓取量
  if (allItems.length > maxLimit) {
    allItems = allItems.slice(0, maxLimit);
  }

  let result;

  if (keywords.length === 0) {
    // 无关键词：直接返回最新资讯
    result = allItems.slice(0, limit);
  } else {
    // 有关键词：先过滤再截断
    const matched = allItems.filter((item) => matchItemByKeywords(item, keywords));
    result = matched.slice(0, limit);
  }

  // 输出前去掉主要文本字段里的 HTML 标签
  const cleanResult = result.map(sanitizeItemForOutput);

  // 只输出 JSON，保持简洁：数组；若无数据则为 []
  console.log(JSON.stringify(cleanResult, null, 2));

}

main().catch((err) => {
  console.error('程序异常退出：', err);
  process.exit(1);
});