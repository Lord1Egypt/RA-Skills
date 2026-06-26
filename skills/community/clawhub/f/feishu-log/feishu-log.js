#!/usr/bin/env node

/**
 * 飞书日志记录工具
 * 功能：接收用户提供的日志内容，智能整理、结构化、层次化后写入飞书文档
 * 文件夹结构：工作日志/XX 年/XX 月/XX 日/
 * 权限：添加用户为协作者（full_access），不转移所有权
 * 配置来源：~/.openclaw/workspace/.env 文件
 */

const https = require('https');
const fs = require('fs');
const path = require('path');
const os = require('os');
const readline = require('readline');

// .env 文件路径
const ENV_FILE_PATH = path.join(os.homedir(), '.openclaw', 'workspace', '.env');

// 配置（默认从 .env 文件加载）
let CONFIG = {
  APP_ID: '',
  APP_SECRET: '',
  OWNER_USER_ID: '',
  BASE_URL: 'https://open.feishu.cn/open-apis',
  ROOT_LOG_FOLDER_NAME: '工作日志',
  LOG_SUBFOLDER_NAME: ''
};

// 交互式输入
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

// 从 .env 文件加载配置
function loadEnvConfig() {
  console.log('📄 加载配置文件...');
  console.log(`   文件路径：${ENV_FILE_PATH}`);
  
  if (!fs.existsSync(ENV_FILE_PATH)) {
    console.log('⚠️  .env 文件不存在');
    return false;
  }
  
  try {
    const envContent = fs.readFileSync(ENV_FILE_PATH, 'utf-8');
    const lines = envContent.split('\n');
    
    let loaded = false;
    for (const line of lines) {
      const trimmed = line.trim();
      if (!trimmed || trimmed.startsWith('#')) continue;
      
      const [key, ...valueParts] = trimmed.split('=');
      const value = valueParts.join('=').trim().replace(/^["']|["']$/g, '');
      
      if (key === 'FEISHU_APP_ID') {
        CONFIG.APP_ID = value;
        loaded = true;
      } else if (key === 'FEISHU_APP_SECRET') {
        CONFIG.APP_SECRET = value;
        loaded = true;
      } else if (key === 'DEFAULT_OWNER_ID') {
        CONFIG.OWNER_USER_ID = value;
        loaded = true;
      } else if (key === 'ROOT_LOG_FOLDER_NAME') {
        CONFIG.ROOT_LOG_FOLDER_NAME = value;
        loaded = true;
      }
    }
    
    if (loaded) {
      console.log('✅ 配置加载成功');
      console.log(`   FEISHU_APP_ID: ${CONFIG.APP_ID || '(空)'}`);
      console.log(`   FEISHU_APP_SECRET: ${CONFIG.APP_SECRET ? '***' + CONFIG.APP_SECRET.slice(-4) : '(空)'}`);
      console.log(`   DEFAULT_OWNER_ID: ${CONFIG.OWNER_USER_ID || '(空)'}`);
      console.log(`   ROOT_LOG_FOLDER_NAME: ${CONFIG.ROOT_LOG_FOLDER_NAME}`);
    }
    
    return loaded;
  } catch (error) {
    console.log(`❌ 读取配置文件失败：${error.message}`);
    return false;
  }
}

// 保存配置到 .env 文件
function saveEnvConfig() {
  console.log('\n💾 保存配置到 .env 文件...');
  
  try {
    // 确保目录存在
    const envDir = path.dirname(ENV_FILE_PATH);
    if (!fs.existsSync(envDir)) {
      fs.mkdirSync(envDir, { recursive: true });
      console.log(`✅ 创建目录：${envDir}`);
    }
    
    // 读取现有内容（如果有）
    let existingContent = '';
    if (fs.existsSync(ENV_FILE_PATH)) {
      existingContent = fs.readFileSync(ENV_FILE_PATH, 'utf-8');
    }
    
    // 构建新的 .env 内容
    const envLines = [];
    envLines.push('# 飞书日志技能配置');
    envLines.push('# 更新时间：' + new Date().toISOString());
    envLines.push('');
    envLines.push('# 飞书应用 ID');
    envLines.push(`FEISHU_APP_ID="${CONFIG.APP_ID}"`);
    envLines.push('');
    envLines.push('# 飞书应用密钥');
    envLines.push(`FEISHU_APP_SECRET="${CONFIG.APP_SECRET}"`);
    envLines.push('');
    envLines.push('# 默认协作者用户 ID（open_id）');
    envLines.push(`DEFAULT_OWNER_ID="${CONFIG.OWNER_USER_ID}"`);
    envLines.push('');
    envLines.push('# 日志根文件夹名称');
    envLines.push(`ROOT_LOG_FOLDER_NAME="${CONFIG.ROOT_LOG_FOLDER_NAME}"`);
    envLines.push('');
    
    const newContent = envLines.join('\n');
    fs.writeFileSync(ENV_FILE_PATH, newContent, 'utf-8');
    
    console.log(`✅ 配置已保存到：${ENV_FILE_PATH}`);
    console.log('');
    console.log('📋 保存的配置：');
    console.log(`   FEISHU_APP_ID: ${CONFIG.APP_ID}`);
    console.log(`   FEISHU_APP_SECRET: ***${CONFIG.APP_SECRET ? CONFIG.APP_SECRET.slice(-4) : ''}`);
    console.log(`   DEFAULT_OWNER_ID: ${CONFIG.OWNER_USER_ID || '(未设置)'}`);
    console.log(`   ROOT_LOG_FOLDER_NAME: ${CONFIG.ROOT_LOG_FOLDER_NAME}`);
    
    return true;
  } catch (error) {
    console.log(`❌ 保存配置失败：${error.message}`);
    return false;
  }
}

// HTTP 请求函数
function httpRequest(method, apiPath, options = {}) {
  return new Promise((resolve, reject) => {
    const body = options.body ? JSON.stringify(options.body) : undefined;
    const fullPath = apiPath.startsWith('/open-apis') ? apiPath : '/open-apis' + apiPath;
    
    const reqOptions = {
      hostname: 'open.feishu.cn',
      port: 443,
      path: fullPath,
      method: method,
      headers: {
        'Authorization': `Bearer ${options.token}`,
        'Content-Type': options.contentType || 'application/json; charset=utf-8',
        ...(body ? { 'Content-Length': Buffer.byteLength(body) } : {})
      }
    };

    const req = https.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.code === 0 || result.code === '0') {
            resolve(result);
          } else {
            reject(new Error(`API Error: ${result.code} - ${result.msg || result.message}`));
          }
        } catch (e) {
          reject(new Error(`Parse Error: ${e.message}`));
        }
      });
    });

    req.on('error', reject);
    if (body) req.write(body);
    req.end();
  });
}

// 获取 tenant access token
async function getTenantToken() {
  if (!CONFIG.APP_ID || !CONFIG.APP_SECRET) {
    throw new Error('FEISHU_APP_ID 或 FEISHU_APP_SECRET 未配置');
  }
  
  const result = await httpRequest('POST', '/auth/v3/tenant_access_token/internal/', {
    body: { app_id: CONFIG.APP_ID, app_secret: CONFIG.APP_SECRET }
  });
  return result.tenant_access_token;
}

// 获取根文件夹 token
async function getRootFolderToken(token) {
  const result = await httpRequest('GET', '/drive/explorer/v2/root_folder/meta', { token });
  return result.data?.token || 'root';
}

// 获取或创建文件夹
async function getOrCreateFolder(token, parentToken, folderName) {
  console.log(`📁 查找文件夹：${folderName}...`);
  
  try {
    const listResult = await httpRequest('GET', `/drive/explorer/v2/folder/${parentToken}/children?page_size=100`, { token });
    const items = listResult.data?.children || {};
    
    const existingKey = Object.keys(items).find(key => items[key].name === folderName && items[key].type === 'folder');
    
    if (existingKey) {
      console.log(`✅ 文件夹已存在：${folderName}（复用）`);
      return { token: items[existingKey].token, existed: true };
    }
    
    console.log(`📝 创建文件夹：${folderName}...`);
    const createResult = await httpRequest('POST', '/drive/v1/files/create_folder', {
      token,
      body: {
        folder_token: parentToken,
        name: folderName
      }
    });
    
    console.log(`✅ 文件夹创建成功：${folderName}`);
    return { token: createResult.data.token, existed: false };
  } catch (error) {
    console.error(`❌ 文件夹操作失败：${error.message}`);
    throw error;
  }
}

// 添加协作者权限
async function addPermission(token, resourceToken, userId, resourceType = 'folder') {
  if (!userId) {
    console.log('⚠️  未设置 DEFAULT_OWNER_ID，跳过权限添加');
    return false;
  }
  
  try {
    console.log(`🔑 添加用户为${resourceType}协作者（full_access）...`);
    
    const queryParams = new URLSearchParams({ type: resourceType });
    
    const result = await httpRequest('POST', `/drive/v1/permissions/${resourceToken}/members?${queryParams}`, {
      token,
      body: {
        member_type: 'openid',
        member_id: userId,
        perm: 'full_access'
      }
    });
    
    console.log(`✅ 用户 ${userId} 已添加为协作者（可管理）`);
    return true;
  } catch (error) {
    if (error.message.includes('99991658')) {
      console.log(`ℹ️  用户已是协作者，跳过添加`);
      return true;
    }
    console.error(`⚠️  权限添加失败：${error.message}`);
    return false;
  }
}

// 检查文档是否已存在
async function findDocument(token, folderToken, title) {
  console.log(`📄 查找文档：${title}...`);
  
  try {
    const listResult = await httpRequest('GET', `/drive/explorer/v2/folder/${folderToken}/children?page_size=100`, { token });
    const items = listResult.data?.children || {};
    
    const existingKey = Object.keys(items).find(key => items[key].name === title && items[key].type === 'docx');
    
    if (existingKey) {
      console.log(`✅ 文档已存在：${title}（复用）`);
      return { document_id: items[existingKey].token, existed: true };
    }
    
    return null;
  } catch (error) {
    console.log(`⚠️  文档查找失败：${error.message}`);
    return null;
  }
}

// 创建文档
async function createDocument(token, folderToken, title) {
  console.log(`📝 创建文档：${title}...`);
  
  try {
    const body = { title, folder_token: folderToken };
    
    const createResult = await httpRequest('POST', '/docx/v1/documents', {
      token,
      body: body
    });
    
    const docToken = createResult.data.document.document_id;
    console.log(`✅ 文档创建成功：${docToken}`);
    
    return {
      document_id: docToken,
      url: `https://feishu.cn/docx/${docToken}`
    };
  } catch (error) {
    console.error(`❌ 文档创建失败：${error.message}`);
    throw error;
  }
}

// 写入内容到文档
async function writeDocumentContent(token, documentId, sections) {
  console.log(`✍️  写入文档内容...`);
  
  try {
    const blocksResult = await httpRequest('GET', `/docx/v1/documents/${documentId}/blocks?page_size=50`, { token });
    const blocks = blocksResult.data?.items || [];
    
    const pageBlock = blocks.find(b => b.block_type === 1);
    
    if (!pageBlock) {
      console.log(`⚠️  未找到页面块`);
      return false;
    }
    
    const parentId = pageBlock.block_id;
    console.log(`📄 页面块 ID: ${parentId}`);
    
    const childrenBlocks = parseSectionsToBlocks(sections);
    console.log(`📊 准备写入 ${childrenBlocks.length} 个块`);
    
    const result = await httpRequest('POST', `/docx/v1/documents/${documentId}/blocks/${parentId}/children`, {
      token,
      body: { children: childrenBlocks }
    });
    
    if (result.data) {
      console.log(`✅ 文档内容写入成功`);
      console.log(`📊 写入块数：${result.data.children?.length || childrenBlocks.length}`);
      return true;
    }
    return false;
  } catch (e) {
    console.log(`⚠️  内容写入失败：${e.message}`);
    return false;
  }
}

// 将 sections 转换为飞书块格式
function parseSectionsToBlocks(sections) {
  const blocks = [];
  
  sections.forEach(section => {
    if (section.type === 'heading2') {
      blocks.push({
        block_type: 4,
        heading2: {
          elements: [{ text_run: { content: section.content } }]
        }
      });
    } else if (section.type === 'heading3') {
      blocks.push({
        block_type: 5,
        heading3: {
          elements: [{ text_run: { content: section.content } }]
        }
      });
    } else if (section.type === 'bullet') {
      blocks.push({
        block_type: 12,
        bullet: {
          elements: [{ text_run: { content: section.content } }]
        }
      });
    } else if (section.type === 'text') {
      blocks.push({
        block_type: 2,
        text: {
          elements: [{ text_run: { content: section.content } }]
        }
      });
    }
  });
  
  return blocks;
}

// 智能整理内容
function organizeContent(input) {
  const today = new Date();
  const dateStr = today.toISOString().split('T')[0];
  const weekdays = ['星期日', '星期一', '星期二', '星期三', '星期四', '星期五', '星期六'];
  const weekday = weekdays[today.getDay()];
  
  const lines = input.split('\n').filter(l => l.trim());
  let title = '日志记录';
  let timeInfo = '';
  let peopleInfo = '';
  let locationInfo = '';
  
  for (const line of lines) {
    if (line.includes('主题') || line.includes('Subject') || line.includes('项目')) {
      const match = line.split(/[:：]/)[1]?.trim();
      if (match) title = match;
    }
    if (line.includes('时间') || line.includes('Time') || line.includes('日期')) {
      timeInfo = line.split(/[:：]/)[1]?.trim() || '';
    }
    if (line.includes('参会') || line.includes('人员') || line.includes('人')) {
      peopleInfo = line.split(/[:：]/)[1]?.trim() || '';
    }
    if (line.includes('地点') || line.includes('Location') || line.includes('位置')) {
      locationInfo = line.split(/[:：]/)[1]?.trim() || '';
    }
  }
  
  const sections = [];
  const basicInfo = [];
  if (dateStr) basicInfo.push(`- 日期：${dateStr} (${weekday})`);
  if (timeInfo) basicInfo.push(`- 时间：${timeInfo}`);
  if (locationInfo) basicInfo.push(`- 地点：${locationInfo}`);
  if (peopleInfo) basicInfo.push(`- 人员：${peopleInfo}`);
  
  if (basicInfo.length > 0) {
    sections.push({ type: 'heading2', content: '📅 基本信息' });
    basicInfo.forEach(item => {
      sections.push({ type: 'bullet', content: item });
    });
  }
  
  let currentSection = null;
  let currentItems = [];
  let currentLevel = 2;
  const contentSections = [];
  
  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;
    
    if (trimmed.startsWith('## ')) {
      if (currentSection) {
        contentSections.push({ title: currentSection, items: currentItems, level: 2 });
      }
      currentSection = trimmed.replace(/^##\s*/, '').trim();
      currentItems = [];
      currentLevel = 2;
    } else if (trimmed.startsWith('### ')) {
      if (currentSection) {
        contentSections.push({ title: currentSection, items: currentItems, level: currentLevel || 2 });
      }
      currentSection = trimmed.replace(/^###\s*/, '').trim();
      currentItems = [];
      currentLevel = 3;
    } else if (trimmed.startsWith('#')) {
      continue;
    } else {
      currentItems.push(trimmed);
    }
  }
  
  if (currentSection) {
    contentSections.push({ title: currentSection, items: currentItems });
  }
  
  if (contentSections.length > 0) {
    contentSections.forEach(section => {
      sections.push({ type: section.level === 3 ? 'heading3' : 'heading2', content: section.title });
      section.items.forEach(item => {
        if (item.startsWith('- ') || item.startsWith('* ')) {
          sections.push({ type: 'bullet', content: item.substring(2) });
        } else {
          sections.push({ type: 'text', content: item });
        }
      });
    });
  }
  
  return { title: `${dateStr} ${title}`, sections: sections };
}

// 交互式配置
async function promptForConfig(error) {
  console.log('\n' + '='.repeat(60));
  console.log('⚠️  配置错误，需要手动配置');
  console.log('='.repeat(60));
  console.log('\n❌ 错误信息：', error.message);
  console.log('\n📋 飞书日志技能需要以下配置：\n');
  
  console.log('1️⃣  FEISHU_APP_ID');
  console.log('   作用：飞书应用的唯一标识符');
  console.log('   获取：飞书开发者后台 → 企业自建应用 → 基本信息');
  console.log('   当前值：', CONFIG.APP_ID || '(空)');
  console.log('');
  
  console.log('2️⃣  FEISHU_APP_SECRET');
  console.log('   作用：飞书应用的密钥，用于获取访问令牌');
  console.log('   获取：飞书开发者后台 → 企业自建应用 → 凭证信息');
  console.log('   当前值：', CONFIG.APP_SECRET ? '***' + CONFIG.APP_SECRET.slice(-4) : '(空)');
  console.log('');
  
  console.log('3️⃣  DEFAULT_OWNER_ID');
  console.log('   作用：你的飞书用户 ID，用于添加为文档协作者');
  console.log('   获取：从飞书消息事件中获取 sender.open_id');
  console.log('   当前值：', CONFIG.OWNER_USER_ID || '(空)');
  console.log('');
  
  console.log('4️⃣  ROOT_LOG_FOLDER_NAME');
  console.log('   作用：日志文件夹的第一级名称');
  console.log('   默认：工作日志');
  console.log('   当前值：', CONFIG.ROOT_LOG_FOLDER_NAME);
  console.log('');
  
  console.log('💡 提示：');
  console.log('   - 配置将保存到 ~/.openclaw/workspace/.env 文件');
  console.log('   - 下次运行时会自动加载配置');
  console.log('   - 也可以手动编辑 .env 文件修改配置');
  console.log('');
  
  return new Promise((resolve) => {
    console.log('是否要手动输入配置？(y/n)');
    rl.question('> ', (answer) => {
      if (answer.toLowerCase() !== 'y' && answer.toLowerCase() !== 'yes') {
        console.log('\n⚠️  已取消配置');
        rl.close();
        resolve(false);
        return;
      }
      
      const newConfig = { ...CONFIG };
      
      console.log('\n请输入 FEISHU_APP_ID（直接回车使用默认值）:');
      rl.question(`> [${newConfig.APP_ID}] `, (val) => {
        newConfig.APP_ID = val.trim() || newConfig.APP_ID;
        
        console.log('\n请输入 FEISHU_APP_SECRET:');
        rl.question('> ', (val) => {
          newConfig.APP_SECRET = val.trim();
          
          console.log('\n请输入 DEFAULT_OWNER_ID:');
          rl.question('> ', (val) => {
            newConfig.OWNER_USER_ID = val.trim();
            
            console.log('\n请输入 ROOT_LOG_FOLDER_NAME（直接回车使用默认值）:');
            rl.question(`> [${newConfig.ROOT_LOG_FOLDER_NAME}] `, (val) => {
              newConfig.ROOT_LOG_FOLDER_NAME = val.trim() || newConfig.ROOT_LOG_FOLDER_NAME;
              
              console.log('\n✅ 配置已更新');
              console.log('');
              console.log('📋 新配置：');
              console.log('   FEISHU_APP_ID:', newConfig.APP_ID);
              console.log('   FEISHU_APP_SECRET:', newConfig.APP_SECRET ? '***' + newConfig.APP_SECRET.slice(-4) : '(空)');
              console.log('   DEFAULT_OWNER_ID:', newConfig.OWNER_USER_ID || '(空)');
              console.log('   ROOT_LOG_FOLDER_NAME:', newConfig.ROOT_LOG_FOLDER_NAME);
              console.log('');
              
              // 更新全局配置
              Object.assign(CONFIG, newConfig);
              
              // 保存到 .env 文件
              saveEnvConfig();
              
              rl.close();
              resolve(true);
            });
          });
        });
      });
    });
  });
}

// 验证配置
function validateConfig() {
  const errors = [];
  
  if (!CONFIG.APP_ID) {
    errors.push('FEISHU_APP_ID 未配置');
  }
  
  if (!CONFIG.APP_SECRET) {
    errors.push('FEISHU_APP_SECRET 未配置');
  }
  
  return errors;
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  const contentArg = args.find(arg => arg.startsWith('--content='));
  const fileArg = args.find(arg => arg.startsWith('--file='));
  
  let content = '';
  
  if (contentArg) {
    content = contentArg.substring('--content='.length);
  } else if (fileArg) {
    const filePath = fileArg.substring('--file='.length);
    try {
      content = fs.readFileSync(filePath, 'utf-8');
    } catch (error) {
      console.error(`❌ 读取文件失败：${error.message}`);
      process.exit(1);
    }
  } else {
    console.log('📝 飞书日志记录工具');
    console.log('================================');
    console.log('');
    console.log('用法示例:');
    console.log('  ./feishu-log.js --content="会议记录：..."');
    console.log('  ./feishu-log.js --file=/tmp/notes.txt');
    console.log('');
    console.error('❌ 请提供日志内容：使用 --content="内容" 或 --file=文件路径');
    process.exit(1);
  }
  
  let retryWithManualConfig = false;
  
  do {
    try {
      // 1. 加载配置
      console.log('📝 飞书日志记录工具');
      console.log('================================');
      
      const loaded = loadEnvConfig();
      
      if (!loaded) {
        console.log('⚠️  .env 文件不存在或为空');
      }
      
      // 2. 验证配置
      const errors = validateConfig();
      if (errors.length > 0) {
        throw new Error(errors.join(', '));
      }
      
      // 3. 获取 token
      console.log('\n🔑 获取访问令牌...');
      const token = await getTenantToken();
      console.log('✅ 令牌获取成功');
      
      // 4. 整理内容
      console.log('\n🤖 智能整理内容...');
      const organized = organizeContent(content);
      console.log('✅ 内容整理完成');
      
      // 5. 创建文件夹结构
      console.log('\n📁 准备文件夹结构...');
      const rootToken = await getRootFolderToken(token);
      
      const today = new Date();
      const year = today.getFullYear();
      const month = String(today.getMonth() + 1).padStart(2, '0');
      const day = String(today.getDate()).padStart(2, '0');
      
      console.log(`\n📁 创建文件夹结构：${CONFIG.ROOT_LOG_FOLDER_NAME}/${year}年/${month}月/${day}日/`);
      
      const rootFolder = await getOrCreateFolder(token, rootToken, CONFIG.ROOT_LOG_FOLDER_NAME);
      const yearFolder = await getOrCreateFolder(token, rootFolder.token, `${year}年`);
      const monthFolder = await getOrCreateFolder(token, yearFolder.token, `${month}月`);
      const dayFolder = await getOrCreateFolder(token, monthFolder.token, `${day}日`);
      
      if (CONFIG.OWNER_USER_ID) {
        console.log('\n🔑 添加文件夹协作者权限...');
        await addPermission(token, rootFolder.token, CONFIG.OWNER_USER_ID, 'folder');
        await addPermission(token, yearFolder.token, CONFIG.OWNER_USER_ID, 'folder');
        await addPermission(token, monthFolder.token, CONFIG.OWNER_USER_ID, 'folder');
        await addPermission(token, dayFolder.token, CONFIG.OWNER_USER_ID, 'folder');
      }
      
      // 6. 创建或查找文档
      const docTitle = organized.title.replace(/^\d{4}-\d{2}-\d{2}\s*/, '');
      const existingDoc = await findDocument(token, dayFolder.token, docTitle);
      
      let doc;
      if (existingDoc) {
        console.log('📄 使用已存在的文档');
        doc = {
          document_id: existingDoc.document_id,
          url: `https://feishu.cn/docx/${existingDoc.document_id}`,
          existed: true
        };
      } else {
        console.log('\n📄 创建文档...');
        doc = await createDocument(token, dayFolder.token, docTitle);
        doc.existed = false;
      }
      
      // 7. 写入内容
      await writeDocumentContent(token, doc.document_id, organized.sections);
      
      // 8. 添加文档权限
      let permissionAdded = false;
      if (CONFIG.OWNER_USER_ID) {
        permissionAdded = await addPermission(token, doc.document_id, CONFIG.OWNER_USER_ID, 'docx');
      }
      
      // 9. 输出结果
      console.log('\n✅ 日志记录完成！');
      console.log('================================');
      console.log(`📎 文档链接：${doc.url}`);
      console.log(`📁 存储位置：${CONFIG.ROOT_LOG_FOLDER_NAME}/${year}年/${month}月/${day}日/`);
      console.log(`📝 文档状态：${doc.existed ? '已存在，内容已更新' : '新建'}`);
      console.log(`🔑 权限状态：${permissionAdded ? '已添加协作者权限' : '未设置协作者'}（机器人所有，用户可管理）`);
      
      retryWithManualConfig = false;
      
    } catch (error) {
      console.error(`\n❌ 错误：${error.message}`);
      
      // 检查是否是配置错误
      const isConfigError = 
        error.message.includes('FEISHU_APP_ID') ||
        error.message.includes('FEISHU_APP_SECRET') ||
        error.message.includes('app secret invalid') ||
        error.message.includes('tenant_access_token');
      
      if (isConfigError && !retryWithManualConfig) {
        const shouldRetry = await promptForConfig(error);
        if (shouldRetry) {
          console.log('\n🔄 使用新配置重试...\n');
          retryWithManualConfig = true;
          continue;
        }
      }
      
      if (error.stack) {
        console.error(error.stack);
      }
      process.exit(1);
    }
  } while (retryWithManualConfig);
}

main();
