#!/usr/bin/env node

/**
 * Telegram Inline Keyboard - 斜杠命令分页显示
 * 
 * 使用 Telegram Inline Keyboard 实现可点击按钮
 * 支持分页、搜索、一键执行
 */

const { getAllCommands } = require('./commands.js');

/**
 * 生成 Telegram Inline Keyboard 格式
 */
async function showCommandsTelegram(page = 1, pageSize = 10) {
  const allCommands = getAllCommands(false);
  const totalPages = Math.ceil(allCommands.length / pageSize);
  const startIndex = (page - 1) * pageSize;
  const endIndex = Math.min(startIndex + pageSize, allCommands.length);
  const pagedCommands = allCommands.slice(startIndex, endIndex);
  
  let output = `📋 *斜杠命令全览 第${page}/${totalPages}页*\n\n`;
  output += `显示 ${startIndex + 1}-${endIndex} / ${allCommands.length} 个命令\n\n`;
  
  // 生成命令列表（带安全图标）
  pagedCommands.forEach((cmd, index) => {
    const safetyIcon = cmd.safety === 'warning' ? '🟡' : '🟢';
    const safetyText = cmd.safety === 'warning' ? '（需确认）' : '';
    
    output += `${safetyIcon} ${cmd.command} ${safetyText}\n`;
    output += `   ${cmd.description}\n\n`;
  });
  
  // 生成 Inline Keyboard 按钮
  const inlineKeyboard = [];
  
  // 每个命令一行按钮（使用 switch_inline_query 实现一键填入）
  pagedCommands.forEach((cmd) => {
    const cmdName = cmd.command.split(' ')[0]; // 移除参数，如 "/search <关键词>" → "/search"
    inlineKeyboard.push([
      {
        text: `${cmd.safety === 'warning' ? '🟡' : '🟢'} ${cmdName}`,
        switch_inline_query_current_chat: `${cmdName} `
      }
    ]);
  });
  
  // 分页导航按钮（使用 callback_data，因为不需要填入输入框）
  const navButtons = [];
  
  if (page > 1) {
    navButtons.push({
      text: '⬅️ 上一页',
      callback_data: `page_${page - 1}`
    });
  }
  
  if (page < totalPages) {
    navButtons.push({
      text: '➡️ 下一页',
      callback_data: `page_${page + 1}`
    });
  }
  
  if (navButtons.length > 0) {
    inlineKeyboard.push(navButtons);
  }
  
  // 功能按钮
  inlineKeyboard.push([
    { text: '🔍 搜索', switch_inline_query_current_chat: '/search ' },
    { text: '📤 导出', callback_data: 'export' }
  ]);
  
  return {
    text: output,
    reply_markup: {
      inline_keyboard: inlineKeyboard
    }
  };
}

/**
 * 生成普通文本格式（非 Telegram）
 */
async function showCommandsText(page = 1, pageSize = 20) {
  const allCommands = getAllCommands(false);
  const totalPages = Math.ceil(allCommands.length / pageSize);
  const startIndex = (page - 1) * pageSize;
  const endIndex = Math.min(startIndex + pageSize, allCommands.length);
  const pagedCommands = allCommands.slice(startIndex, endIndex);
  
  let output = `\n`;
  output += `┌─────────────────────────────────────────────────┐\n`;
  output += `│  📋 斜杠命令全览 第${page}/${totalPages}页              🔍     │\n`;
  output += `├─────────────────────────────────────────────────┤\n`;
  
  pagedCommands.forEach((cmd, index) => {
    const safetyIcon = cmd.safety === 'warning' ? '🟡' : '🟢';
    const safetyText = cmd.safety === 'warning' ? '（需确认）' : '';
    
    output += `│  ${safetyIcon} ${cmd.command.padEnd(30)} ${safetyText.padEnd(10)}│\n`;
    output += `│     ${cmd.description.substring(0, 30).padEnd(30)}          │\n`;
    output += `│     [执行] [详情]${' '.repeat(12)}│\n`;
    
    if (index < pagedCommands.length - 1) {
      output += `│                                                 │\n`;
    }
  });
  
  output += `├─────────────────────────────────────────────────┤\n`;
  output += `│  显示 ${startIndex + 1}-${endIndex} / ${allCommands.length} 个命令`.padEnd(54) + `│\n`;
  output += `│  [⬅️ 上一页] [➡️ 下一页] [🔍 搜索] [📤 导出]`.padEnd(54) + `│\n`;
  output += `└─────────────────────────────────────────────────┘\n`;
  
  return output;
}

// CLI 入口
if (require.main === module) {
  const args = process.argv.slice(2);
  const page = parseInt(args[0]) || 1;
  const telegram = args.includes('--telegram');
  
  if (telegram) {
    showCommandsTelegram(page).then(result => {
      console.log('📱 Telegram Inline Keyboard 格式：\n');
      console.log(result.text);
      console.log('\n📎 Inline Keyboard 按钮：');
      console.log(JSON.stringify(result.reply_markup, null, 2));
    });
  } else {
    showCommandsText(page).then(console.log);
  }
}

module.exports = {
  showCommandsTelegram,
  showCommandsText
};
