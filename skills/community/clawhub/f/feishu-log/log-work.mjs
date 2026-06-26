import { Client } from "@larksuiteoapi/node-sdk";
import * as fs from "fs";
import * as path from "path";

/**
 * 从 OpenClaw 配置文件读取飞书凭证
 */
function getCredentialsFromOpenClawConfig() {
  const openclawConfigPath = path.join(process.env.HOME, ".openclaw", "openclaw.json");
  
  if (!fs.existsSync(openclawConfigPath)) {
    return null;
  }
  
  try {
    const config = JSON.parse(fs.readFileSync(openclawConfigPath, "utf-8"));
    const feishuAccount = config.channels?.feishu?.accounts?.main;
    
    if (feishuAccount?.appId && feishuAccount?.appSecret) {
      return {
        appId: feishuAccount.appId,
        appSecret: feishuAccount.appSecret,
        rootToken: "root" // 使用根目录
      };
    }
  } catch (e) {
    console.warn("⚠️ OpenClaw 配置文件读取失败:", e.message);
  }
  
  return null;
}

// 获取凭证：环境变量 > OpenClaw 配置 > 内置默认值
let credentials;

if (process.env.FEISHU_APP_ID && process.env.FEISHU_APP_SECRET) {
  console.log("✅ 使用环境变量中的飞书凭证");
  credentials = {
    appId: process.env.FEISHU_APP_ID,
    appSecret: process.env.FEISHU_APP_SECRET,
    rootToken: process.env.FEISHU_LOG_ROOT_TOKEN || "root"
  };
} else {
  const fromConfig = getCredentialsFromOpenClawConfig();
  if (fromConfig) {
    console.log("✅ 使用 OpenClaw 配置文件中的飞书凭证");
    console.log(`   App ID: ${fromConfig.appId}`);
    credentials = fromConfig;
  } else {
    console.warn("⚠️ 未配置飞书凭证");
    credentials = {
      appId: "cli_a93b936aa9391cc7",
      appSecret: "aMRJMyi3KSXbSJhRgyx7ycvyT5D3rsrs",
      rootToken: "root"
    };
  }
}

const client = new Client({ 
  appId: credentials.appId, 
  appSecret: credentials.appSecret 
});
const ROOT_FOLDER_TOKEN = credentials.rootToken;

/**
 * 获取或创建文件夹
 * @param {string} parentToken - 父文件夹 token
 * @param {string} name - 文件夹名称
 * @returns {Promise<string>} - 文件夹 token
 */
async function getOrCreateFolder(parentToken, name) {
  // 列出父文件夹内容
  const listRes = await client.drive.file.list({
    params: { folder_token: parentToken }
  });
  
  const files = listRes.data?.files || [];
  
  // 查找同名文件夹
  const existing = files.find(f => f.name === name && f.type === 'folder');
  if (existing) {
    console.log(`  📁 复用文件夹：${name}`);
    return existing.token;
  }
  
  // 创建新文件夹
  const createRes = await client.drive.file.createFolder({
    data: {
      name: name,
      folder_token: parentToken
    }
  });
  
  console.log(`  📂 创建文件夹：${name}`);
  return createRes.data?.token;
}

/**
 * 创建日志文档
 * @param {string} folderToken - 文件夹 token
 * @param {string} title - 文档标题
 * @param {string} content - Markdown 内容
 * @returns {Promise<string>} - 文档 token
 */
async function createLogDoc(folderToken, title, content) {
  // 创建文档
  const createRes = await client.docx.document.create({
    data: {
      title: title,
      folder_token: folderToken
    }
  });
  
  const docToken = createRes.data?.document?.document_id;
  if (!docToken) {
    throw new Error("文档创建失败");
  }
  
  console.log(`  📄 创建文档：${title}`);
  
  // 转换 Markdown
  const convertRes = await client.docx.document.convert({
    data: {
      content_type: "markdown",
      content: content
    }
  });
  
  // 清理 blocks
  const cleanBlocks = convertRes.data.blocks.map(b => {
    const { parent_id: _, ...clean } = b;
    if (clean.block_type === 32 && typeof clean.children === "string") {
      clean.children = [clean.children];
    }
    return clean;
  });
  
  // 插入内容
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
  
  console.log(`  ✅ 内容写入成功`);
  return docToken;
}

/**
 * 整理日志内容
 * @param {string} rawContent - 原始内容
 * @param {string} date - 日期字符串
 * @returns {string} - 整理后的 Markdown
 */
function formatLogContent(rawContent, date) {
  const lines = rawContent.split('\n').filter(l => l.trim());
  
  // 提取要点
  let currentSection = '主要内容';
  let sections = { '主要内容': [] };
  
  for (const line of lines) {
    const trimmed = line.trim();
    
    // 检测分段标记（支持 # 和 ## 作为分段）
    if (trimmed.startsWith('##') || trimmed.startsWith('#')) {
      currentSection = trimmed.replace(/^#+\s*/, '');
      sections[currentSection] = [];
      continue;
    }
    
    // 添加到当前分段
    if (trimmed) {
      sections[currentSection].push(trimmed.replace(/^[-*•]\s*/, ''));
    }
  }
  
  // 生成 Markdown
  // 注意：不添加 H1 标题，因为飞书文档的 title 已经作为页面标题显示
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
 * 主函数 - 记录工作日志
 * @param {string} content - 日志内容
 * @param {Date} date - 日期（可选，默认今天）
 * @param {string} rootToken - 根目录 token（可选）
 */
async function logWork(content, date = new Date(), rootToken = ROOT_FOLDER_TOKEN) {
  console.log('\n📝 开始记录工作日志...\n');
  
  // 格式化日期
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const dateStr = `${year}-${month}-${day}`;
  
  console.log(`📅 日期：${dateStr}`);
  
  // 1. 创建/获取年份文件夹
  const yearFolder = await getOrCreateFolder(rootToken, `${year}年`);
  
  // 2. 创建/获取月份文件夹
  const monthFolder = await getOrCreateFolder(yearFolder, `${month}月`);
  
  // 3. 创建/获取日期文件夹
  const dayFolder = await getOrCreateFolder(monthFolder, `${day}日`);
  
  // 4. 整理内容
  const formattedContent = formatLogContent(content, dateStr);
  
  // 5. 创建文档
  const docTitle = `工作日志-${dateStr}`;
  const docToken = await createLogDoc(dayFolder, docTitle, formattedContent);
  
  // 6. 返回结果
  const docUrl = `https://wcnh9mbykuay.feishu.cn/docx/${docToken}`;
  console.log(`\n✅ 日志记录完成!`);
  console.log(`📄 文档链接：${docUrl}`);
  
  return { docToken, docUrl, date: dateStr };
}

// 测试：记录今天的工作日志
const todayContent = `
## 工作内容

- 测试 feishu_drive 和 feishu_doc 两个技能
- 在飞书云盘创建测试文件夹和文档
- 验证 Markdown 内容写入功能
- 清理测试数据

## 技术细节

- 使用飞书开放 API 的 docx 接口
- 通过 convert API 将 Markdown 转换为文档块
- 使用 descendant API 批量插入内容
- 处理表格等特殊块类型

## 遇到的问题

- 表格内容需要特殊处理 parent_id 字段
- 批量插入可能遇到 API 限流 (429)
- TableCell 的 children 必须是数组格式

## 解决方案

- 清理 blocks 时移除 parent_id 字段
- 添加重试机制处理限流
- 转换后验证并修复 children 格式

## 测试结果

- ✅ 文件夹创建成功
- ✅ 文档创建成功
- ✅ 内容写入成功（标题、列表、代码块）
- ⚠️ 表格需要额外处理
`;

// 执行
logWork(todayContent).catch(console.error);
