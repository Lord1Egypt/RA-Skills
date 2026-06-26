#!/usr/bin/env node
/**
 * 简化的飞书日志记录工具
 * 使用 tenant_access_token 直接调用 API
 */

import * as https from 'https';

// 配置
const APP_ID = 'cli_a93b936aa9391cc7';
const APP_SECRET = 'aMRJMyi3KSXbSJhRgyx7ycvyT5D3rsrs';

/**
 * 获取 tenant_access_token
 */
async function getTenantAccessToken() {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      app_id: APP_ID,
      app_secret: APP_SECRET
    });
    
    const options = {
      hostname: 'open.feishu.cn',
      port: 443,
      path: '/open-apis/auth/v3/tenant_access_token/internal',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        const result = JSON.parse(body);
        if (result.code === 0) {
          resolve(result.tenant_access_token);
        } else {
          reject(new Error(result.msg));
        }
      });
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

/**
 * 获取或创建文件夹
 */
async function getOrCreateFolder(token, parentToken, name) {
  return new Promise((resolve, reject) => {
    // 根目录使用 folder_type=root，其他使用 folder_token
    const isRoot = parentToken === 'root';
    const path = isRoot 
      ? '/open-apis/drive/v1/files?folder_type=root&parent_type=root'
      : `/open-apis/drive/v1/files?folder_token=${parentToken}`;
    
    const options = {
      hostname: 'open.feishu.cn',
      port: 443,
      path: path,
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${token}`
      }
    };
    
    https.get(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        const result = JSON.parse(body);
        if (result.code === 0) {
          const existing = result.data?.files?.find(f => f.name === name && f.type === 'folder');
          if (existing) {
            console.log(`  📁 复用文件夹：${name}`);
            resolve(existing.token);
          } else {
            // 创建文件夹
            createFolder(token, parentToken, name).then(resolve).catch(reject);
          }
        } else {
          reject(new Error(result.msg));
        }
      });
    }).on('error', reject);
  });
}

/**
 * 创建文件夹
 */
function createFolder(token, parentToken, name) {
  return new Promise((resolve, reject) => {
    const isRoot = parentToken === 'root';
    const body = isRoot 
      ? { name, folder_type: 'root' }
      : { name, parent_token: parentToken };
    const data = JSON.stringify(body);
    
    const options = {
      hostname: 'open.feishu.cn',
      port: 443,
      path: '/open-apis/drive/v1/files',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        const result = JSON.parse(body);
        if (result.code === 0) {
          console.log(`  📂 创建文件夹：${name}`);
          resolve(result.data?.token);
        } else {
          reject(new Error(result.msg));
        }
      });
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

/**
 * 创建文档
 */
async function createDocument(token, folderToken, title, content) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify({
      title,
      folder_token: folderToken
    });
    
    const options = {
      hostname: 'open.feishu.cn',
      port: 443,
      path: '/open-apis/docx/v1/documents',
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json',
        'Content-Length': data.length
      }
    };
    
    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', (chunk) => body += chunk);
      res.on('end', () => {
        const result = JSON.parse(body);
        if (result.code === 0) {
          console.log(`  📄 创建文档：${title}`);
          resolve(result.data?.document?.document_id);
        } else {
          reject(new Error(result.msg));
        }
      });
    });
    
    req.on('error', reject);
    req.write(data);
    req.end();
  });
}

// 主程序
async function main() {
  const content = process.argv.slice(2).join(' ') || '测试日志';
  
  console.log('📝 开始记录工作日志...\n');
  
  try {
    // 1. 获取 token
    console.log('🔑 获取 tenant_access_token...');
    const token = await getTenantAccessToken();
    console.log('✅ Token 获取成功\n');
    
    // 2. 获取日期
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const dateStr = `${year}-${month}-${day}`;
    
    // 3. 创建文件夹结构
    console.log('📁 创建文件夹结构...');
    const rootToken = 'root';
    const yearFolder = await getOrCreateFolder(token, rootToken, `${year}年`);
    const monthFolder = await getOrCreateFolder(token, yearFolder, `${month}月`);
    const dayFolder = await getOrCreateFolder(token, monthFolder, `${day}日`);
    console.log('');
    
    // 4. 创建文档
    console.log('📄 创建文档...');
    const title = `工作日志-${dateStr}`;
    const docId = await createDocument(token, dayFolder, title, content);
    console.log('✅ 文档创建成功\n');
    
    console.log(`📋 文档 ID: ${docId}`);
    console.log(`🔗 链接：https://bytedance.feishu.cn/docx/${docId}`);
    
  } catch (e) {
    console.error('❌ 失败:', e.message);
    process.exit(1);
  }
}

main();
