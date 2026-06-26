#!/usr/bin/env node
/**
 * Fast Response Optimizer - 启动钩子
 * 在 OpenClaw 启动时加载缓存
 */

const path = require('path');
const cacheManager = require('./scripts/cache-manager.js');

// 启动时加载缓存
console.log('⚡ Fast Response Optimizer 启动中...');

try {
  // 更新最后消息时间
  cacheManager.updateLastMessage();
  
  // 获取缓存（如果需要则刷新）
  const cache = cacheManager.getCache();
  
  console.log(`✅ 缓存就绪: ${Object.keys(cache.files).length} 个文件`);
  console.log(`📁 缓存时间: ${new Date(cache.timestamp).toLocaleString()}`);
  
} catch (e) {
  console.error('❌ 缓存加载失败:', e.message);
}

// 导出缓存读取函数供 OpenClaw 使用
module.exports = {
  /**
   * 从缓存读取文件（替代直接 fs.readFile）
   */
  readFromCache: (filename) => {
    try {
      const cache = cacheManager.getCache();
      if (cache.files[filename]) {
        return cache.files[filename].content;
      }
    } catch (e) {
      console.error(`缓存读取失败: ${filename}`, e.message);
    }
    return null;
  },
  
  /**
   * 检查缓存是否包含文件
   */
  hasInCache: (filename) => {
    try {
      const cache = cacheManager.getCache();
      return !!cache.files[filename];
    } catch (e) {
      return false;
    }
  },
  
  /**
   * 获取缓存状态
   */
  getStatus: () => {
    return cacheManager.shouldRefresh();
  }
};
