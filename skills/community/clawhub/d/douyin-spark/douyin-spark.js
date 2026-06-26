#!/usr/bin/env node

/**
 * 抖音自动续火花脚本
 * 使用 OpenClaw 浏览器工具自动为火花联系人发消息
 * 
 * 执行流程：
 * 1. 打开抖音聊天页面 https://www.douyin.com/chat?isPopup=1
 * 2. 使用 browser snapshot refs=role 获取联系人列表
 * 3. 逐个点击联系人，在输入框 (ref=e713) 输入消息，按 Enter 发送
 * 4. 报告发送结果
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// 火花联系人列表文件
const CONTACTS_FILE = path.join(
  process.env.HOME || process.env.USERPROFILE,
  '.openclaw',
  'workspace',
  'memory',
  'douyin-spark-contacts.md'
);

// 默认续火花消息
const DEFAULT_MESSAGE = '我是 ai 续火花助手，我来续火花了';

// 抖音聊天页面 URL
const DOUYIN_CHAT_URL = 'https://www.douyin.com/chat?isPopup=1';

/**
 * 解析联系人列表
 */
function parseContacts() {
  if (!fs.existsSync(CONTACTS_FILE)) {
    console.error('联系人列表文件不存在:', CONTACTS_FILE);
    return [];
  }

  const content = fs.readFileSync(CONTACTS_FILE, 'utf-8');
  const contacts = [];
  
  // 解析 markdown 表格
  const lines = content.split('\n');
  for (const line of lines) {
    // 匹配表格行：| 用户名 | 数字 | 状态 | 备注 |
    const match = line.match(/\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|\s*([^\|]+)\s*\|/);
    if (match && match[1].trim() !== '用户名') {
      contacts.push({
        name: match[1].trim(),
        number: match[2].trim(),
        status: match[3].trim(),
        note: match[4] ? match[4].trim() : ''
      });
    }
  }
  
  return contacts;
}

/**
 * 执行 OpenClaw browser 命令
 */
function runBrowserCommand(args) {
  try {
    const cmd = `openclaw browser ${args}`;
    execSync(cmd, { stdio: 'pipe' });
    return true;
  } catch (error) {
    console.error('浏览器命令执行失败:', error.message);
    return false;
  }
}

/**
 * 发送续火花消息（自动化流程）
 * 
 * 注意：此函数需要通过 OpenClaw 会话系统执行，不能直接运行
 * AI 助手应该按照以下步骤操作：
 * 1. browser action=navigate url=DOUYIN_CHAT_URL
 * 2. browser action=snapshot refs=role
 * 3. 解析快照找到联系人 ref
 * 4. browser action=act kind=click ref=<联系人 ref>
 * 5. browser action=act kind=type ref=e713 text=<消息>
 * 6. browser action=act kind=press key=Enter
 */
function sendSparkMessage(message = DEFAULT_MESSAGE) {
  const contacts = parseContacts();
  
  if (contacts.length === 0) {
    console.log('没有火花联系人');
    return;
  }

  console.log('\n========================================');
  console.log('抖音续火花自动化指南');
  console.log('========================================\n');
  console.log(`需要发送：${contacts.length} 个联系人`);
  console.log(`消息内容：${message}\n`);
  
  console.log('请按以下步骤执行（或让 AI 助手自动执行）：\n');
  console.log('1. 打开抖音聊天页面:');
  console.log(`   browser action=navigate url=${DOUYIN_CHAT_URL}\n`);
  
  console.log('2. 获取页面快照:');
  console.log('   browser action=snapshot refs=role\n');
  
  console.log('3. 对每个联系人执行:');
  console.log('   - 点击联系人（从快照中找到对应的 ref）');
  console.log('   - 在输入框输入消息（ref=e713）');
  console.log('   - 按 Enter 发送\n');
  
  console.log('联系人列表:');
  console.log('----------------------------------------');
  
  for (const contact of contacts) {
    const statusIcon = contact.status.includes('重燃中') ? '🔥' : '✨';
    console.log(`${statusIcon} ${contact.name.padEnd(20)} ${contact.number.padEnd(8)} ${contact.status}`);
  }
  
  console.log('----------------------------------------\n');
  console.log('提示：让 AI 助手使用 browser 工具自动执行上述流程');
  console.log('========================================\n');
}

/**
 * 显示联系人列表
 */
function listContacts() {
  const contacts = parseContacts();
  
  console.log('\n火花联系人列表:\n');
  console.log('用户名 | 数字 | 状态 | 备注');
  console.log('-'.repeat(60));
  
  for (const contact of contacts) {
    console.log(`${contact.name} | ${contact.number} | ${contact.status} | ${contact.note}`);
  }
  
  console.log(`\n共 ${contacts.length} 个联系人`);
}

/**
 * 添加联系人
 */
function addContact(name) {
  console.log(`添加联系人：${name}`);
  // 实际实现需要编辑文件
}

/**
 * 移除联系人
 */
function removeContact(name) {
  console.log(`移除联系人：${name}`);
  // 实际实现需要编辑文件
}

/**
 * 睡眠函数
 */
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 主函数
 */
function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case '--list':
    case '-l':
      listContacts();
      break;
    case '--add':
      addContact(args[1]);
      break;
    case '--remove':
      removeContact(args[1]);
      break;
    case '--message':
    case '-m':
      sendSparkMessage(args[1] || DEFAULT_MESSAGE);
      break;
    case '--help':
    case '-h':
      console.log(`
抖音续火花工具

用法:
  node douyin-spark.js [选项]

选项:
  --list, -l          显示火花联系人列表
  --add <名字>        添加火花联系人
  --remove <名字>     移除火花联系人
  --message, -m <消息> 发送指定消息（默认使用测试消息）
  --help, -h          显示帮助信息

示例:
  node douyin-spark.js --list
  node douyin-spark.js --message "你好呀"
      `);
      break;
    default:
      sendSparkMessage(DEFAULT_MESSAGE);
  }
}

main();
