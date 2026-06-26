import { Client } from "@larksuiteoapi/node-sdk";

// 配置（支持环境变量覆盖）
const appId = process.env.FEISHU_APP_ID || "cli_a93b936aa9391cc7";
const appSecret = process.env.FEISHU_APP_SECRET || "aMRJMyi3KSXbSJhRgyx7ycvyT5D3rsrs";
const ROOT_FOLDER_TOKEN = process.env.FEISHU_LOG_ROOT_TOKEN || "RdVIffbJxl8HDCdJiULcIpdgnzf";

const client = new Client({ appId, appSecret });

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
 * 整理日志内容
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
 * 主函数 - 分两步：预览和确认
 */
async function logWork(content, date = new Date(), rootToken = ROOT_FOLDER_TOKEN, skipConfirm = false) {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, '0');
  const day = String(date.getDate()).padStart(2, '0');
  const formattedDate = `${year}-${month}-${day}`;
  
  // 1. 准备文件夹结构
  const yearFolder = await getOrCreateFolder(rootToken, `${year}年`);
  const monthFolder = await getOrCreateFolder(yearFolder, `${month}月`);
  const dayFolder = await getOrCreateFolder(monthFolder, `${day}日`);
  
  // 2. 整理内容
  const formattedContent = formatLogContent(content, formattedDate);
  
  // 3. 如果不需确认，直接写入
  if (skipConfirm) {
    const docToken = await createLogDoc(dayFolder, `工作日志-${formattedDate}`, formattedContent);
    const docUrl = `https://wcnh9mbykuay.feishu.cn/docx/${docToken}`;
    return { docToken, docUrl, date: formattedDate, status: 'written' };
  }
  
  // 4. 否则返回预览内容，等待确认
  const preview = `
📝 已整理好日志内容，请确认：

━━━━━━━━━━━━━━━━━━━━━━━━━━━━
**工作日志 - ${formattedDate}**

${formattedContent.replace(/\n/g, '\n')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━

请回复以下任一词语来写入文件：
- ✅ **确认**
- ✅ **OK**
- ✅ **可以**
- ✅ **没问题**
- ✅ **好的**

或提出修改意见，我会修改后再次请您确认。
`.trim();
  
  return { preview, date: formattedDate, status: 'pending', content: formattedContent, folderToken: dayFolder };
}

// 导出函数供其他模块使用
export { logWork, formatLogContent, createLogDoc, getOrCreateFolder };

// 命令行交互模式
if (import.meta.url === `file://${process.argv[1]}`) {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.log('Feishu Log - 交互式日志记录工具');
    console.log('');
    console.log('用法:');
    console.log('  node log-interactive.js                    # 交互模式');
    console.log('  node log-interactive.js "日志内容"         # 直接模式（需确认）');
    console.log('  node log-interactive.js --confirm "内容"   # 直接写入（不确认）');
    console.log('');
    process.exit(0);
  }
  
  let skipConfirm = false;
  let contentArg = null;
  
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--confirm' && args[i + 1]) {
      skipConfirm = true;
      contentArg = args[++i];
    } else if (!args[i].startsWith('--')) {
      contentArg = args[i];
    }
  }
  
  if (!contentArg) {
    console.error('错误：请提供日志内容');
    process.exit(1);
  }
  
  logWork(contentArg, new Date(), ROOT_FOLDER_TOKEN, skipConfirm)
    .then(result => {
      if (result.status === 'pending') {
        console.log(result.preview);
      } else {
        console.log('✅ 日志记录完成!');
        console.log('📄 ' + result.docUrl);
      }
    })
    .catch(err => {
      console.error('错误:', err.message);
      process.exit(1);
    });
}
