#!/usr/bin/env node
/**
 * 压缩检查脚本 - 设计为由 cron 定时调用
 * 检查会话长度，超过阈值时自动压缩
 */

import { fileURLToPath } from 'url';
import path from 'path';
import fs from 'fs';
import { SessionCompactor } from './compact.mjs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 日志路径
const LOG_PATH = path.join(__dirname, '..', '..', '..', '..', '.clawsession-log.json');

// 读取日志
function readLog() {
  try {
    if (fs.existsSync(LOG_PATH)) {
      return JSON.parse(fs.readFileSync(LOG_PATH, 'utf-8'));
    }
  } catch (e) {}
  return { lastCheck: null, lastCompactAt: null, totalCompactions: 0 };
}

// 写入日志
function writeLog(log) {
  fs.writeFileSync(LOG_PATH, JSON.stringify(log, null, 2), 'utf-8');
}

function main() {
  const log = readLog();
  const compactor = new SessionCompactor();
  const status = compactor.getStatus();
  
  const now = new Date().toISOString();
  
  console.log(`[${now}] 压缩检查开始`);
  console.log(`  利用率: ${status.utilizationPercent}% (${status.tokens}/${status.threshold})`);
  
  // 更新检查时间
  log.lastCheck = now;
  
  if (status.needsCompact) {
    console.log(`  ⚠️ 需要压缩，执行中...`);
    
    const result = compactor.compact();
    
    if (result.success) {
      console.log(`  ✅ 压缩完成`);
      console.log(`     移除消息: ${result.removedCount}`);
      console.log(`     保留消息: ${result.preservedCount}`);
      console.log(`     压缩后tokens: ~${result.newTotalTokens}`);
      console.log(`     累计压缩次数: ${result.compactionCount}`);
      
      log.lastCompactAt = now;
      log.totalCompactions = result.compactionCount;
      log.lastCompactResult = {
        removedCount: result.removedCount,
        preservedCount: result.preservedCount,
        newTotalTokens: result.newTotalTokens
      };
    } else {
      console.log(`  ❌ 压缩失败: ${result.reason}`);
    }
  } else {
    console.log(`  ✅ 不需要压缩`);
  }
  
  // 记录这次检查
  log.lastStatus = {
    tokens: status.tokens,
    messageCount: status.messageCount,
    utilizationPercent: status.utilizationPercent,
    compactionCount: status.compactionCount
  };
  
  writeLog(log);
  console.log(`[${now}] 压缩检查完成`);
}

main();
