#!/usr/bin/env node

/**
 * Get Random Fun Content
 * 从缓存中随机获取一条趣味内容
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const cacheFile = path.join(__dirname, '..', 'cache', 'daily-fun.json');

function getRandomContent() {
  // 1. 检查缓存是否存在
  if (!fs.existsSync(cacheFile)) {
    return {
      error: 'no_cache',
      message: '缓存不存在，请先运行 generate.mjs'
    };
  }

  // 2. 读取缓存
  const cache = JSON.parse(fs.readFileSync(cacheFile, 'utf-8'));

  // 3. 检查日期
  const today = new Date().toISOString().split('T')[0];
  if (cache.date !== today) {
    return {
      error: 'cache_outdated',
      message: '缓存已过期，请重新生成'
    };
  }

  // 4. 随机选择一条
  if (!cache.items || cache.items.length === 0) {
    return {
      error: 'no_items',
      message: '缓存为空'
    };
  }

  const randomItem = cache.items[Math.floor(Math.random() * cache.items.length)];

  return {
    success: true,
    item: randomItem,
    remaining: cache.items.length
  };
}

// 主函数
const result = getRandomContent();

if (result.success) {
  console.log(JSON.stringify(result, null, 2));
} else {
  console.error(JSON.stringify(result, null, 2));
  process.exit(1);
}
