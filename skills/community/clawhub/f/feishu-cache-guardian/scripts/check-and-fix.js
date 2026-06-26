#!/usr/bin/env node
/**
 * Feishu Cache Guardian
 * 检查并修复飞书 probe.ts 的缓存配置
 * 如果缓存时间被重置为默认值，自动修复为60分钟
 */

import { readFileSync, writeFileSync } from 'fs';
import { execSync } from 'child_process';

const PROBE_PATH = '/opt/homebrew/lib/node_modules/openclaw/extensions/feishu/src/probe.ts';

// 期望的缓存配置
const EXPECTED_SUCCESS_TTL = '60 * 60 * 1000'; // 60分钟
const EXPECTED_ERROR_TTL = '60 * 60 * 1000';   // 60分钟

function checkAndFixCache() {
  try {
    const content = readFileSync(PROBE_PATH, 'utf-8');
    
    // 检查当前配置
    const successMatch = content.match(/const PROBE_SUCCESS_TTL_MS = (\d+ \* \d+ \* \d+)/);
    const errorMatch = content.match(/const PROBE_ERROR_TTL_MS = (\d+ \* \d+ \* \d+)/);
    
    if (!successMatch || !errorMatch) {
      console.error('无法找到缓存配置，文件可能已更改');
      process.exit(1);
    }
    
    const currentSuccess = successMatch[1];
    const currentError = errorMatch[1];
    
    console.log(`当前配置: 成功=${currentSuccess}, 失败=${currentError}`);
    
    // 检查是否需要修复
    const needsFix = currentSuccess !== EXPECTED_SUCCESS_TTL || currentError !== EXPECTED_ERROR_TTL;
    
    if (!needsFix) {
      console.log('✅ 缓存配置正常，无需修复');
      return { fixed: false, message: '配置正常' };
    }
    
    console.log('⚠️ 缓存配置被修改，正在修复...');
    
    // 修复配置
    let newContent = content
      .replace(
        /const PROBE_SUCCESS_TTL_MS = \d+ \* \d+ \* \d+;/,
        'const PROBE_SUCCESS_TTL_MS = 60 * 60 * 1000; // 60 minutes'
      )
      .replace(
        /const PROBE_ERROR_TTL_MS = \d+ \* \d+ \* \d+;/,
        'const PROBE_ERROR_TTL_MS = 60 * 60 * 1000; // 60 minutes'
      );
    
    // 写入文件
    writeFileSync(PROBE_PATH, newContent, 'utf-8');
    
    console.log('✅ 缓存配置已修复为60分钟');
    
    // 重启 Gateway
    console.log('🔄 正在重启 OpenClaw Gateway...');
    try {
      execSync('openclaw gateway restart', { stdio: 'inherit' });
      console.log('✅ Gateway 重启成功');
    } catch (e) {
      console.error('⚠️ Gateway 重启失败，请手动重启');
      return { fixed: true, restarted: false, message: '配置已修复，但重启失败' };
    }
    
    return { fixed: true, restarted: true, message: '配置已修复并重启' };
    
  } catch (error) {
    console.error('❌ 检查/修复失败:', error.message);
    process.exit(1);
  }
}

// 执行检查
const result = checkAndFixCache();
console.log('\n结果:', result.message);
