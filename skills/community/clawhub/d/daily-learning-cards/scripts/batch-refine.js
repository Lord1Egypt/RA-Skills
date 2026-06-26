#!/usr/bin/env node
/**
 * 补跑记忆整理（用于补跑历史日期）
 * 用法：node batch-refine.js 2026-05-12 2026-05-13 ...
 */

const path = require('path');
const { processChannel } = require('./refine-memory.js');

const CONFIG = {
  memoryDir: '/home/admin/.openclaw/workspace/memory',
  channels: {
    feishu: { dir: 'feishu', label: '飞书' },
    webui: { dir: 'webui', label: 'WebUI' }
  }
};

async function processDate(date) {
  console.log(`\n=== 处理日期: ${date} ===`);
  
  for (const [chKey, chConfig] of Object.entries(CONFIG.channels)) {
    const fullDir = path.join(CONFIG.memoryDir, chConfig.dir);
    
    try {
      console.log(`  [${chConfig.label}] 处理中...`);
      const success = await processChannel(chKey, fullDir, date);
      if (success) {
        console.log(`  [${chConfig.label}] ✅ 完成`);
      } else {
        console.log(`  [${chConfig.label}] ⚠️ 无内容或失败`);
      }
    } catch (e) {
      console.error(`  [${chConfig.label}] ❌ 错误: ${e.message}`);
    }
  }
}

async function main() {
  const dates = process.argv.slice(2);
  
  if (dates.length === 0) {
    console.log('用法: node batch-refine.js <日期1> <日期2> ...');
    console.log('示例: node batch-refine.js 2026-05-12 2026-05-13');
    process.exit(1);
  }
  
  console.log('=== 开始批量补跑记忆整理 ===');
  console.log(`目标日期: ${dates.join(', ')}`);
  
  for (const date of dates) {
    await processDate(date);
  }
  
  console.log('\n=== 批量补跑完成 ===');
}

main().catch(e => {
  console.error('❌ 错误:', e);
  process.exit(1);
});