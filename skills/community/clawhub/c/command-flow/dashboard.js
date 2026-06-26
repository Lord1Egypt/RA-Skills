#!/usr/bin/env node

/**
 * Slash Command Dashboard - 斜杠命令汉化和全览系统
 * 
 * 显示命令列表、搜索命令、执行命令
 * 
 * @version 1.0.0
 * @author Neo（宇宙神经系统）
 */

const { getAllCommands, searchCommands, getCommandBySlug } = require('./commands.js');
const {
  generateCommandsDisplay,
  generateAskText,
  getSafetyIcon,
  getSourceIcon,
  needsConfirm,
  generateConfirmMessage
} = require('./safety.js');

/**
 * 显示命令列表
 * 自动检测平台，Telegram 用简单格式，其他用框线格式
 * 支持分页显示
 */
async function showCommands(showHidden = false, page = 1, pageSize = 20) {
  const allCommands = getAllCommands(showHidden);
  const display = generateCommandsDisplay(allCommands, showHidden);
  
  // 合并所有命令用于分页
  const allFlat = [...display.native, ...display.ours, ...display.thirdParty];
  const totalPages = Math.ceil(allFlat.length / pageSize);
  const startIndex = (page - 1) * pageSize;
  const endIndex = Math.min(startIndex + pageSize, allFlat.length);
  const pagedCommands = allFlat.slice(startIndex, endIndex);
  
  // 使用分页后的命令直接显示（不再分类）
  const pagedDisplay = {
    native: pagedCommands,
    ours: [],
    thirdParty: []
  };
  
  // 检测是否 Telegram（通过环境变量或参数）
  const isTelegram = process.argv.includes('--telegram') || process.env.TELEGRAM_PLATFORM === 'true';
  
  let output = `\n`;
  
  if (isTelegram) {
    // Telegram 简单格式（不用框线）
    output += `📋 *斜杠命令全览 第${page}/${totalPages}页*\n\n`;
  } else {
    // 其他平台框线格式
    output += `┌─────────────────────────────────────────────────┐\n`;
    output += `│  📋 斜杠命令全览 第${page}/${totalPages}页              🔍     │\n`;
    output += `├─────────────────────────────────────────────────┤\n`;
  }
  
  // 显示分页后的命令（简化显示，不分类）
  if (isTelegram) {
    pagedCommands.forEach((cmd) => {
      const cmdDisplay = cmd.aliases && cmd.aliases.length > 0 
        ? `${cmd.command} \\(${cmd.aliases.join(', ')}\\)`
        : cmd.command;
      output += `${cmd.safety} \\` + cmdDisplay + `\n`;
      output += `   ${cmd.description}\n\n`;
    });
  } else {
    pagedCommands.forEach((cmd, index) => {
      const cmdDisplay = cmd.aliases && cmd.aliases.length > 0 
        ? `${cmd.command} ${cmd.aliases.join(', ')}`
        : cmd.command;
      output += `│  ${cmd.safety} ${cmdDisplay.padEnd(35)} │\n`;
      output += `│     ${cmd.description.substring(0, 30).padEnd(30)}│\n`;
      output += `│     [执行] [详情]${' '.repeat(12)}│\n`;
      
      if (index < pagedCommands.length - 1) {
        output += `│                                                 │\n`;
      }
    });
  }
  
  // 分页导航
  const prevPage = page > 1 ? page - 1 : 1;
  const nextPage = page < totalPages ? page + 1 : totalPages;
  
  // 说明
  if (isTelegram) {
    output += `说明：🟢 安全  🟡 危险（需确认） 🔴 隐藏（默认不显示）\n\n`;
    output += `显示 ${startIndex + 1}-${Math.min(endIndex, allFlat.length)} / ${allFlat.length} 个命令\n\n`;
    output += `[⬅️ 上一页] [➡️ 下一页] [查看隐藏命令] [导出列表] [搜索命令]\n`;
  } else {
    output += `├─────────────────────────────────────────────────┤\n`;
    output += `│  显示 ${startIndex + 1}-${Math.min(endIndex, allFlat.length)} / ${allFlat.length} 个命令`.padEnd(54) + `│\n`;
    output += `│  [⬅️ 上一页] [➡️ 下一页] [查看隐藏命令] [导出列表]`.padEnd(54) + `│\n`;
    output += `└─────────────────────────────────────────────────┘\n`;
  }
  
  return output;
}

/**
 * 显示隐藏命令
 */
async function showHiddenCommands() {
  const hidden = getAllCommands(true).filter(cmd => cmd.safety === 'hidden');
  
  if (hidden.length === 0) {
    return '没有隐藏命令。';
  }
  
  let output = `\n`;
  output += `⚠️ 高风险命令，请谨慎使用\n\n`;
  output += `┌─────────────────────────────────────────────────┐\n`;
  output += `│  🔴 隐藏命令（高风险）                          │\n`;
  output += `├─────────────────────────────────────────────────┤\n`;
  
  hidden.forEach((cmd, index) => {
    output += `│                                                 │\n`;
    output += `│  🔴 ${cmd.command.padEnd(46)}│\n`;
    output += `│     ${cmd.description.substring(0, 30).padEnd(30)}│\n`;
    output += `│     ${cmd.warning || '⚠️ 高风险操作'}${' '.repeat(Math.max(0, 20 - (cmd.warning || '').length))}│\n`;
    output += `│     [执行]（需二次确认）${' '.repeat(24)}│\n`;
    
    if (index < hidden.length - 1) {
      output += `│                                                 │\n`;
    }
  });
  
  output += `│                                                 │\n`;
  output += `└─────────────────────────────────────────────────┘\n`;
  output += `\n确定要执行吗？这些操作不可逆。（回复"确定"或"取消"）\n`;
  
  return output;
}

/**
 * 搜索命令
 */
async function searchCommandsDisplay(query) {
  const results = searchCommands(query);
  
  if (results.length === 0) {
    return `没有找到与"${query}"相关的命令。`;
  }
  
  let output = `\n`;
  output += `找到 ${results.length} 个相关命令：\n\n`;
  
  results.forEach((cmd, index) => {
    const safetyIcon = getSafetyIcon(cmd.safety);
    const sourceIcon = getSourceIcon(cmd.source);
    
    output += `${safetyIcon.emoji} ${cmd.command}\n`;
    output += `   ${cmd.description}\n`;
    output += `   来源：${sourceIcon.emoji} ${sourceIcon.text}\n`;
    output += `   [执行] [详情]\n`;
    
    if (index < results.length - 1) {
      output += `\n`;
    }
  });
  
  return output;
}

/**
 * 导出命令列表为 Markdown
 */
async function exportToMarkdown() {
  const commands = getAllCommands(false);
  
  let markdown = `# 斜杠命令全览\n\n`;
  markdown += `**生成时间：** ${new Date().toLocaleString('zh-CN')}\n\n`;
  markdown += `---\n\n`;
  
  // 按来源分组
  const display = generateCommandsDisplay(commands);
  
  markdown += `## 🏷️ OpenClaw 原生技能\n\n`;
  display.native.forEach(cmd => {
    markdown += `### ${cmd.command}\n\n`;
    markdown += `- **说明：** ${cmd.description}\n`;
    markdown += `- **安全级别：** ${cmd.safety}\n`;
    markdown += `- **操作：** [执行] [详情]\n\n`;
  });
  
  markdown += `---\n\n`;
  markdown += `## 🛠️ 我们开发的技能\n\n`;
  display.ours.forEach(cmd => {
    markdown += `### ${cmd.command}\n\n`;
    markdown += `- **说明：** ${cmd.description}\n`;
    markdown += `- **安全级别：** ${cmd.safety}\n`;
    markdown += `- **操作：** [执行] [详情]\n\n`;
  });
  
  markdown += `---\n\n`;
  markdown += `## 🧩 第三方技能\n\n`;
  display.thirdParty.forEach(cmd => {
    markdown += `### ${cmd.command}\n\n`;
    markdown += `- **说明：** ${cmd.description}\n`;
    markdown += `- **安全级别：** ${cmd.safety}\n`;
    markdown += `- **操作：** [执行] [详情]\n\n`;
  });
  
  return markdown;
}

// 导出函数
module.exports = {
  showCommands,
  showHiddenCommands,
  searchCommandsDisplay,
  exportToMarkdown
};

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const command = args[0];
  const page = parseInt(args[1]) || 1;
  const telegram = args.includes('--telegram');
  
  // 如果是 Telegram 模式，使用 inline keyboard
  if (telegram) {
    const { showCommandsTelegram } = require('./telegram-inline.js');
    showCommandsTelegram(page).then(result => {
      console.log(JSON.stringify(result, null, 2));
    });
    return;
  }
  
  switch (command) {
    case 'show':
      showCommands(false, page).then(console.log);
      break;
    case 'show-hidden':
      showHiddenCommands().then(console.log);
      break;
    case 'search':
      if (args[1]) {
        searchCommandsDisplay(args[1]).then(console.log);
      } else {
        console.log('用法：node dashboard.js search <关键词>');
      }
      break;
    case 'export':
      exportToMarkdown().then(console.log);
      break;
    default:
      showCommands(false, 1).then(console.log);
  }
}
