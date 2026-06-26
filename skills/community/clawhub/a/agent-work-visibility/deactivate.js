#!/usr/bin/env node

/**
 * agent-work-visibility 撤销脚本
 * 
 * 用途：移除透明层协议注入
 * 执行：node deactivate.js 或 ./deactivate.js
 */

const fs = require('fs');
const path = require('path');

const WORKSPACE_DIR = process.env.OPENCLAW_WORKSPACE || path.join(process.env.HOME, '.openclaw', 'workspace-main');
const AGENTS_FILE = path.join(WORKSPACE_DIR, 'AGENTS.md');
const SOUL_FILE = path.join(WORKSPACE_DIR, 'SOUL.md');

// 透明层协议标识
const PROTOCOL_START = '## ⚠️ 强制协议：任务透明层';
const PROTOCOL_END = '---\n';

function removeProtocol(filePath) {
  if (!fs.existsSync(filePath)) {
    console.log(`⚠️  ${filePath} 不存在，跳过`);
    return false;
  }

  const content = fs.readFileSync(filePath, 'utf8');
  
  // 检查是否包含协议
  const startIndex = content.indexOf(PROTOCOL_START);
  if (startIndex === -1) {
    console.log(`️  ${filePath} 未包含透明层协议，跳过`);
    return false;
  }

  // 找到协议结束位置（下一个 --- 分隔符）
  const endMarker = '\n---\n';
  const endStartIndex = content.indexOf(endMarker, startIndex);
  if (endStartIndex === -1) {
    console.log(`⚠️  ${filePath} 协议格式异常，无法安全移除`);
    return false;
  }

  const endEndIndex = endStartIndex + endMarker.length;

  // 移除协议内容（包括前面的空行）
  let removeStart = startIndex;
  if (content[startIndex - 1] === '\n') {
    removeStart -= 1;
  }

  const newContent = content.slice(0, removeStart) + content.slice(endEndIndex);
  fs.writeFileSync(filePath, newContent, 'utf8');
  console.log(`✅ 已从 ${filePath} 移除透明层协议`);
  return true;
}

function main() {
  console.log('🔧 撤销 agent-work-visibility 透明层...\n');
  
  let modified = false;
  
  // 优先从 SOUL.md 移除
  if (fs.existsSync(SOUL_FILE)) {
    modified = removeProtocol(SOUL_FILE) || modified;
  }
  
  // 从 AGENTS.md 移除
  if (fs.existsSync(AGENTS_FILE)) {
    modified = removeProtocol(AGENTS_FILE) || modified;
  }
  
  if (modified) {
    console.log('\n✅ 撤销完成！下次会话将不再使用透明层。');
    console.log('\n 如需重新激活：');
    console.log('   node ~/.openclaw/skills/agent-work-visibility/activate.js\n');
  } else {
    console.log('\nℹ️  无需修改，未找到透明层协议。\n');
  }
}

main();
