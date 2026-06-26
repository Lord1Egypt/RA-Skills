#!/usr/bin/env node

/**
 * Auto-Add OpenClaw Commands to commands.js
 * 
 * 从 OpenClaw CLI 自动获取所有命令，生成 commands.js 格式
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
        const match = line.match(/^\s{2}([a-z-]+(?:\s*\*)?)\s+(.+)$/);
        if (match) {
          const [, cmdRaw, descRaw] = match;
          const cmd = cmdRaw.replace(/\s*\*.*$/, '').trim();
          let desc = descRaw.split('(')[0].trim();
          
          // 清理描述
          desc = desc.replace(/\n.*$/, '').trim(); // 移除换行后的内容
          if (desc.length > 50) desc = desc.substring(0, 47) + '...';
          
          // 跳过无效命令
          if (!cmd || cmd.startsWith('openclaw')) continue;
          
          commands.push({
            slug: cmd,
            command: '/' + cmd,
            description: desc,
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
 * 生成命令代码
 */
function generateCommandCode(cmd) {
  return `    {
      slug: '${cmd.slug}',
      command: '${cmd.command}',
      description: '${cmd.description}',
      safety: SAFETY.SAFE,
      source: SOURCE.NATIVE,
      category: 'OpenClaw',
      executeHint: '执行命令',
      execute: async () => {
        return \`提示：请使用 OpenClaw 直接执行 \\\`${cmd.command}\\\`\n\n（此命令为系统命令）\`;
      }
    },`;
}

/**
 * 主函数
 */
function main() {
  console.log('🔄 正在生成 OpenClaw 命令代码...\n');
  
  const commands = getOpenClawCommands();
  
  if (commands.length === 0) {
    console.log('❌ 未找到任何命令');
    return;
  }
  
  console.log(`✅ 找到 ${commands.length} 个 OpenClaw 命令：\n`);
  
  const code = commands.map(generateCommandCode).join('\n');
  
  // 输出到文件
  const outputPath = path.join(__dirname, 'openclaw-commands.generated.js');
  fs.writeFileSync(outputPath, code, 'utf8');
  
  console.log(`📝 已生成代码到：${outputPath}`);
  console.log(`\n💡 下一步：将生成的代码复制到 commands.js 的 native 数组中`);
}

main();
