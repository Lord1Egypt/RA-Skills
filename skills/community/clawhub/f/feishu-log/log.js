#!/usr/bin/env node

/**
 * Feishu Log - 工作日志记录工具
 * 
 * 用法:
 *   node log.js "日志内容"
 *   node log.js --date 2026-03-10 "日志内容"
 *   node log.js --help
 */

import { Client } from "@larksuiteoapi/node-sdk";
import { readFileSync } from "fs";
import { fileURLToPath } from "url";
import { dirname, join } from "path";

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 配置（支持环境变量覆盖）
// 注意：如果设置了环境变量但未提供有效凭证，会导致认证失败
const APP_ID = process.env.FEISHU_APP_ID || "cli_a93b936aa9391cc7";
const APP_SECRET = process.env.FEISHU_APP_SECRET || "aMRJMyi3KSXbSJhRgyx7ycvyT5D3rsrs";
const ROOT_FOLDER_TOKEN = process.env.FEISHU_LOG_ROOT_TOKEN || "RdVIffbJxl8HDCdJiULcIpdgnzf";

// 打印配置来源提示
if (process.env.FEISHU_APP_ID || process.env.FEISHU_APP_SECRET) {
  console.log('ℹ️  使用环境变量配置');
}

const client = new Client({ appId: APP_ID, appSecret: APP_SECRET });

/**
 * 获取或创建文件夹
 */
async function getOrCreateFolder(parentToken, name) {
  const listRes = await client.drive.file.list({
    params: { folder_token: parentToken }
  });
  
  const files = listRes.data?.files || [];
  const existing = files.find(f => f.name === name && f.type === 'folder');
  
  if (existing) {
    return existing.token;
  }
  
  const createRes = await client.drive.file.createFolder({
    data: { name, folder_token: parentToken }
  });
  
  return createRes.data?.token;
}

/**
 * 创建日志文档
 */
async function createLogDoc(folderToken, title, content) {
  const createRes = await client.docx.document.create({
    data: { title, folder_token: folderToken }
  });
  
  const docToken = createRes.data?.document?.document_id;
  if (!docToken) throw new Error("文档创建失败");
  
  const convertRes = await client.docx.document.convert({
    data: { content_type: "markdown", content }
  });
  
  const cleanBlocks = convertRes.data.blocks.map(b => {
    const { parent_id: _, ...clean } = b;
    if (clean.block_type === 32 && typeof clean.children === "string") {
      clean.children = [clean.children];
    }
    return clean;
  });
  
  const insertRes = await client.docx.documentBlockDescendant.create({
    path: { document_id: docToken, block_id: docToken },
    data: {
      children_id: convertRes.data.first_level_block_ids,
      descendants: cleanBlocks,
      index: -1
    }
  });
  
  if (insertRes.code !== 0) {
    throw new Error(`内容写入失败：${insertRes.msg}`);
  }
  
  return docToken;
}

/**
 * 智能整理日志内容
 * 注意：不添加 H1 标题，因为飞书文档的 title 已作为页面标题
 */
function formatLogContent(rawContent, date) {
  const lines = rawContent.split('\n').filter(l => l.trim());
  let sections = { '主要内容': [] };
  let currentSection = '主要内容';
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    if (trimmed.startsWith('##') || trimmed.startsWith('#')) {
      currentSection = trimmed.replace(/^#+\s*/, '');
      sections[currentSection] = [];
      continue;
    }
    
    if (trimmed) {
      sections[currentSection].push(trimmed.replace(/^[-*•]\s*/, ''));
    }
  }
  
  const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  let markdown = `记录时间：${now}\n\n`;
  markdown += `---\n\n`;
  
  for (const [section, items] of Object.entries(sections)) {
    if (items.length > 0) {
      markdown += `## ${section}\n\n`;
      for (const item of items) {
        markdown += `- ${item}\n`;
      }
      markdown += `\n`;
    }
  }
  
  markdown += `---\n\n`;
  markdown += `*本日志由 AI 助手自动生成*\n`;
  return markdown;
}

/**
 * 主函数
 */
async function logWork(content, dateStr, rootToken = ROOT_FOLDER_TOKEN) {
  const date = dateStr ? new Date(dateStr) : new Date();
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const formattedDate = `${year}-${month}-${day}`;
  
  console.log('📝 记录工作日志...');
  console.log(`📅 日期：${formattedDate}\n`);
  
  // 创建文件夹结构
  const yearFolder = await getOrCreateFolder(rootToken, `${year}年`);
  const monthFolder = await getOrCreateFolder(yearFolder, `${month}月`);
  const dayFolder = await getOrCreateFolder(monthFolder, `${day}日`);
  
  // 整理并写入内容
  const formattedContent = formatLogContent(content, formattedDate);
  const docToken = await createLogDoc(dayFolder, `工作日志-${formattedDate}`, formattedContent);
  
  const docUrl = `https://wcnh9mbykuay.feishu.cn/docx/${docToken}`;
  console.log(`✅ 日志记录完成!`);
  console.log(`📄 ${docUrl}\n`);
  
  return { docToken, docUrl, date: formattedDate };
}

// CLI 解析
const args = process.argv.slice(2);

if (args.includes('--help') || args.includes('-h')) {
  console.log(`
Feishu Log - 工作日志记录工具

用法:
  node log.js "日志内容"
  node log.js --date 2026-03-10 "日志内容"
  node log.js --help

示例:
  node log.js "今天完成了项目 A 的开发"
  node log.js --date 2026-03-10 "昨天的工作内容"
`);
  process.exit(0);
}

// 解析参数
let dateArg = null;
let contentArg = null;

for (let i = 0; i < args.length; i++) {
  if (args[i] === '--date' && args[i + 1]) {
    dateArg = args[++i];
  } else if (!args[i].startsWith('--')) {
    contentArg = args[i];
  }
}

if (!contentArg) {
  console.error('错误：请提供日志内容');
  console.error('使用 --help 查看用法');
  process.exit(1);
}

// 执行
logWork(contentArg, dateArg).catch(err => {
  console.error('错误:', err.message);
  process.exit(1);
});
