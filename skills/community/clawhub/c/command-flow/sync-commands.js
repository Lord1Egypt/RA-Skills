#!/usr/bin/env node

/**
 * Auto-Sync OpenClaw Commands
 * 
 * 从 OpenClaw CLI 自动获取所有命令，补充到 commands.js
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

/**
 * 获取 OpenClaw 所有命令
 */
function getOpenClawCommands() {
  try {
    const output = execSync('openclaw --help', { encoding: 'utf8' });
    const lines = output.split('\n');
    
    const commands = [];
    let inCommands = false;
    
    for (const line of lines) {
      if (line.trim() === 'Commands:') {
        inCommands = true;
        continue;
      }
      
      if (inCommands && line.trim()) {
        // 跳过提示行
        if (line.includes('Hint:')) continue;
        
        // 解析命令
        const match = line.match(/^\s{2}([a-z-]+)\s+(.+)$/);
        if (match) {
          const [, cmd, desc] = match;
          commands.push({
            slug: cmd.replace(/\s*\*.*$/, ''), // 移除 * 标记
            command: '/' + cmd.replace(/\s*\*.*$/, ''),
            description: desc.split('(')[0].trim(), // 移除括号内容
            safety: 'safe',
            source: 'native',
            category: 'OpenClaw'
          });
        }
      }
    }
    
    return commands;
  } catch (error) {
    console.error('获取 OpenClaw 命令失败:', error.message);
    return [];
  }
}

/**
 * 主函数
 */
function main() {
  console.log('🔄 正在同步 OpenClaw 命令...\n');
  
  const commands = getOpenClawCommands();
  
  if (commands.length === 0) {
    console.log('❌ 未找到任何命令');
    return;
  }
  
  console.log(`✅ 找到 ${commands.length} 个 OpenClaw 命令：\n`);
  
  commands.forEach((cmd, i) => {
    console.log(`${i + 1}. ${cmd.command} - ${cmd.description}`);
  });
  
  console.log('\n💡 提示：这些命令可以手动添加到 commands.js 中');
  console.log('   或者使用 --auto 参数自动添加（待实现）');
}

main();
