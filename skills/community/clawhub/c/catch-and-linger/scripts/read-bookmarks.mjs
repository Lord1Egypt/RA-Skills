#!/usr/bin/env node
/**
 * read-bookmarks.mjs — 读取本机 Chrome / Edge 书签，输出 URL 列表。
 *
 * 用法：
 *   node read-bookmarks.mjs [--browser chrome|edge|all] [--profile Default]
 *                           [--limit N] [--folder 路径片段]
 *
 * 零依赖。浏览器运行时也能读（Node 在 Windows 上默认以共享读方式打开文件）。
 * JSON 解析失败会重试 3 次（间隔 300ms），因为浏览器可能正在写回。
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

const BROWSERS = {
  chrome: {
    label: 'Chrome',
    root: path.join(os.homedir(), 'AppData', 'Local', 'Google', 'Chrome', 'User Data'),
  },
  edge: {
    label: 'Edge',
    root: path.join(
      os.homedir(),
      'AppData',
      'Local',
      'Microsoft',
      'Edge',
      'User Data',
    ),
  },
};

const RETRIES = 3;
const RETRY_DELAY_MS = 300;

function parseArgs(argv) {
  const args = {
    browser: 'all',
    profile: 'Default',
    limit: Infinity,
    folder: null,
  };

  for (let i = 0; i < argv.length; i += 1) {
    const v = argv[i];
    if (v === '--browser') args.browser = argv[++i] ?? 'all';
    else if (v === '--profile') args.profile = argv[++i] ?? 'Default';
    else if (v === '--limit') args.limit = Number(argv[++i] ?? '0') || Infinity;
    else if (v === '--folder') args.folder = argv[++i] ?? null;
  }

  return args;
}

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

/** 读取并解析书签 JSON，失败时重试（浏览器可能正在写回文件）。 */
function readBookmarksJson(file) {
  return (async () => {
    let lastError = null;

    for (let attempt = 0; attempt < RETRIES; attempt += 1) {
      try {
        const raw = fs.readFileSync(file, 'utf8');
        return JSON.parse(raw);
      } catch (e) {
        lastError = e;
        if (attempt < RETRIES - 1) {
          await sleep(RETRY_DELAY_MS);
        }
      }
    }

    throw lastError;
  })();
}

/** 遍历 Chrome/Edge 的 roots 树，收集所有 type==='url' 的节点。 */
function collectUrls(node, folderPath, out) {
  if (!node || typeof node !== 'object') return;

  if (node.type === 'url' && typeof node.url === 'string') {
    out.push({
      url: node.url,
      title: node.name ?? '',
      folder: folderPath,
      date_added: node.date_added ?? null,
    });
    return;
  }

  if (Array.isArray(node.children)) {
    for (const child of node.children) {
      collectUrls(child, folderPath, out);
    }
  }
}

function collectFromRoots(roots, out) {
  if (!roots || typeof roots !== 'object') return;

  for (const [rootName, rootNode] of Object.entries(roots)) {
    // 根节点下的每个一级目录（如「书签栏」「其他书签」）本身也是文件夹
    if (rootNode && Array.isArray(rootNode.children)) {
      for (const child of rootNode.children) {
        if (!child || typeof child !== 'object') continue;
        // url 节点直接挂在根下（如书签栏里的散条）→ 归属根目录名；
        // 文件夹节点 → 用它自己的名字
        const folderName =
          child.type === 'url' ? rootName : (child.name ?? rootName);
        collectUrls(child, folderName, out);
      }
    }
  }
}

const args = parseArgs(process.argv.slice(2));
const targets = args.browser === 'all' ? ['chrome', 'edge'] : [args.browser];

const result = [];
const errors = [];

for (const key of targets) {
  const browser = BROWSERS[key];
  if (!browser) {
    errors.push({ browser: key, error: `未知的浏览器：${key}` });
    continue;
  }

  const file = path.join(browser.root, args.profile, 'Bookmarks');

  if (!fs.existsSync(file)) {
    errors.push({ browser: key, error: `找不到书签文件：${file}` });
    continue;
  }

  try {
    const json = await readBookmarksJson(file);
    const out = [];
    collectFromRoots(json.roots, out);
    result.push(...out);
  } catch (e) {
    errors.push({ browser: key, error: `解析失败：${e?.message ?? e}` });
  }
}

let filtered = result;
if (args.folder) {
  const needle = args.folder.toLowerCase();
  filtered = filtered.filter((b) => (b.folder ?? '').toLowerCase().includes(needle));
}
if (Number.isFinite(args.limit)) {
  filtered = filtered.slice(0, args.limit);
}

// 去重（同一 URL 可能出现在多个目录）
const seen = new Set();
const unique = filtered.filter((b) => {
  if (seen.has(b.url)) return false;
  seen.add(b.url);
  return true;
});

console.log(
  JSON.stringify(
    {
      count: unique.length,
      total_read: result.length,
      errors,
      bookmarks: unique,
    },
    null,
    2,
  ),
);

if (errors.length > 0 && unique.length === 0) {
  process.exit(1);
}
