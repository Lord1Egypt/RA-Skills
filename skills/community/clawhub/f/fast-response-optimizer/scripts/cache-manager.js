#!/usr/bin/env node
/**
 * 缓存管理器 - 记忆文件缓存
 * 每1分钟刷新，或距离上次消息超过1分钟刷新
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE = process.env.OPENCLAW_WORKSPACE || process.cwd();
const CACHE_DIR = path.join(WORKSPACE, 'cache');
const CACHE_FILE = path.join(CACHE_DIR, 'memory-cache.json');
const LAST_REFRESH_FILE = path.join(CACHE_DIR, '.last-refresh');
const LAST_MESSAGE_FILE = path.join(CACHE_DIR, '.last-message');

/**
 * 初始化缓存目录
 */
function initCache() {
  if (!fs.existsSync(CACHE_DIR)) {
    fs.mkdirSync(CACHE_DIR, { recursive: true });
  }
}

/**
 * 读取文件内容
 */
function readFileSafe(filePath) {
  try {
    if (fs.existsSync(filePath)) {
      return fs.readFileSync(filePath, 'utf-8');
    }
  } catch (e) {
    console.error(`读取失败: ${filePath}`, e.message);
  }
  return null;
}

/**
 * 加载所有记忆文件到缓存
 */
function loadCache() {
  console.log('🔄 加载记忆文件到缓存...\n');
  
  // 确保缓存目录存在
  initCache();
  
  const cache = {
    timestamp: Date.now(),
    files: {}
  };
  
  // 核心记忆文件
  const files = {
    'SOUL.md': path.join(WORKSPACE, 'SOUL.md'),
    'USER.md': path.join(WORKSPACE, 'USER.md'),
    'MEMORY.md': path.join(WORKSPACE, 'MEMORY.md'),
    'AGENTS.md': path.join(WORKSPACE, 'AGENTS.md'),
    'SESSION-STATE.md': path.join(WORKSPACE, 'SESSION-STATE.md'),
    'HEARTBEAT.md': path.join(WORKSPACE, 'HEARTBEAT.md'),
    'WORKING.md': path.join(WORKSPACE, 'WORKING.md')
  };
  
  for (const [name, filePath] of Object.entries(files)) {
    const content = readFileSafe(filePath);
    if (content) {
      cache.files[name] = {
        content: content.substring(0, 5000), // 限制大小
        size: content.length,
        mtime: fs.statSync(filePath).mtime.getTime()
      };
      console.log(`✅ 缓存: ${name} (${content.length} 字符)`);
    } else {
      console.log(`⚠️ 跳过: ${name} (不存在)`);
    }
  }
  
  // 保存缓存
  fs.writeFileSync(CACHE_FILE, JSON.stringify(cache, null, 2));
  fs.writeFileSync(LAST_REFRESH_FILE, Date.now().toString());
  
  console.log(`\n✅ 缓存已保存: ${CACHE_FILE}`);
  console.log(`📊 共缓存 ${Object.keys(cache.files).length} 个文件`);
  
  return cache;
}

/**
 * 检查是否需要刷新缓存
 */
function shouldRefresh() {
  const now = Date.now();
  
  // 检查最后刷新时间
  let lastRefresh = 0;
  if (fs.existsSync(LAST_REFRESH_FILE)) {
    lastRefresh = parseInt(fs.readFileSync(LAST_REFRESH_FILE, 'utf-8')) || 0;
  }
  
  // 检查最后消息时间
  let lastMessage = 0;
  if (fs.existsSync(LAST_MESSAGE_FILE)) {
    lastMessage = parseInt(fs.readFileSync(LAST_MESSAGE_FILE, 'utf-8')) || 0;
  }
  
  const oneMinute = 60 * 1000;
  
  // 条件1: 距离上次刷新超过1分钟
  const needRefreshByTime = (now - lastRefresh) > oneMinute;
  
  // 条件2: 距离上次消息超过1分钟
  const needRefreshByMessage = (now - lastMessage) > oneMinute;
  
  // 条件3: 缓存不存在
  const cacheNotExists = !fs.existsSync(CACHE_FILE);
  
  return {
    shouldRefresh: needRefreshByTime || needRefreshByMessage || cacheNotExists,
    reason: cacheNotExists ? '缓存不存在' : 
            needRefreshByTime ? '超过1分钟未刷新' : 
            needRefreshByMessage ? '超过1分钟无消息' : '无需刷新',
    lastRefresh,
    lastMessage
  };
}

/**
 * 更新最后消息时间
 */
function updateLastMessage() {
  initCache();
  fs.writeFileSync(LAST_MESSAGE_FILE, Date.now().toString());
}

/**
 * 获取缓存（如果不存在或过期则刷新）
 */
function getCache(forceRefresh = false) {
  initCache();
  
  const check = shouldRefresh();
  
  if (forceRefresh || check.shouldRefresh) {
    console.log(`🔄 刷新原因: ${check.reason}\n`);
    return loadCache();
  }
  
  // 读取现有缓存
  if (fs.existsSync(CACHE_FILE)) {
    const cache = JSON.parse(fs.readFileSync(CACHE_FILE, 'utf-8'));
    console.log('✅ 使用现有缓存');
    return cache;
  }
  
  return loadCache();
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'check';
  
  switch (command) {
    case 'refresh':
      loadCache();
      break;
    case 'message':
      updateLastMessage();
      console.log('✅ 已更新最后消息时间');
      break;
    case 'status':
      const check = shouldRefresh();
      console.log('📊 缓存状态:');
      console.log(`   需要刷新: ${check.shouldRefresh}`);
      console.log(`   原因: ${check.reason}`);
      console.log(`   上次刷新: ${check.lastRefresh ? new Date(check.lastRefresh).toLocaleString() : '从未'}`);
      console.log(`   上次消息: ${check.lastMessage ? new Date(check.lastMessage).toLocaleString() : '从未'}`);
      break;
    default:
      getCache();
  }
}

// 导出函数
module.exports = {
  getCache,
  loadCache,
  updateLastMessage,
  shouldRefresh
};

// 运行
main();
