#!/usr/bin/env node
/**
 * 经验发布脚本
 * 将本地经验包发布到 Experience Hub
 */

import fs from 'fs';
import path from 'path';
import https from 'https';
import http from 'http';
import { fileURLToPath } from 'url';
import AdmZip from 'adm-zip';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const HUB_API_BASE = 'https://www.expericehub.com:18080';

// HTTP POST 请求封装（multipart/form-data）
function postFile(url, filePath) {
  return new Promise((resolve, reject) => {
    const filename = path.basename(filePath);
    const fileSize = fs.statSync(filePath).size;
    const fileContent = fs.readFileSync(filePath);
    
    const boundary = '----WebKitFormBoundary' + Math.random().toString(36).substring(2);
    
    const body = Buffer.concat([
      Buffer.from(`--${boundary}\r\n`),
      Buffer.from(`Content-Disposition: form-data; name="file"; filename="${filename}"\r\n`),
      Buffer.from('Content-Type: application/zip\r\n\r\n'),
      fileContent,
      Buffer.from(`\r\n--${boundary}--\r\n`)
    ]);
    
    const protocol = url.startsWith('https') ? https : http;
    
    const options = {
      method: 'POST',
      headers: {
        'Content-Type': `multipart/form-data; boundary=${boundary}`,
        'Content-Length': body.length
      }
    };
    
    const req = protocol.request(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          resolve({ raw: data });
        }
      });
    });
    
    req.on('error', reject);
    req.write(body);
    req.end();
  });
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('用法: node publish.mjs <本地zip文件路径>');
    console.error('示例: node publish.mjs ~/.openclaw/experiences/packages/my-experience.zip');
    process.exit(1);
  }
  
  const filePath = args[0];
  
  // 解析 ~ 路径
  const resolvedPath = filePath.startsWith('~') 
    ? path.join(process.env.HOME, filePath.slice(1))
    : filePath;
  
  // 检查文件是否存在
  if (!fs.existsSync(resolvedPath)) {
    console.error(`❌ 文件不存在: ${resolvedPath}`);
    process.exit(1);
  }
  
  // 检查是否为 zip 文件
  if (!resolvedPath.endsWith('.zip')) {
    console.error('❌ 请提供 .zip 格式的经验包文件');
    process.exit(1);
  }
  
  // 检查 exp.yml 是否存在（通过解压检查）
  try {
    const zip = new AdmZip(resolvedPath);
    const entries = zip.getEntries();
    const hasExpYml = entries.some(e => e.entryName === 'exp.yml');
    
    if (!hasExpYml) {
      console.error('❌ 经验包格式错误：缺少 exp.yml 文件');
      console.error('   请确保 zip 包内包含 exp.yml 配置文件');
      process.exit(1);
    }
  } catch (err) {
    console.error('❌ 无法读取 zip 文件:', err.message);
    process.exit(1);
  }
  
  console.log(`📤 发布经验包: ${path.basename(resolvedPath)}`);
  console.log();
  
  try {
    const url = `${HUB_API_BASE}/api/experiences`;
    const result = await postFile(url, resolvedPath);
    
    if (result.success) {
      console.log('✅ 发布成功!');
      console.log(`   经验包 ID: ${result.id}`);
      console.log();
      console.log(`💡 其他用户可通过以下方式学习:`);
      console.log(`   learn https://www.expericehub.com:18080/pkg/${result.id}.zip`);
    } else if (result.error) {
      console.error('❌ 发布失败:', result.error);
      process.exit(1);
    } else {
      console.log('⚠️  响应:', result);
    }
    
  } catch (err) {
    console.error('❌ 发布失败:', err.message);
    process.exit(1);
  }
}

main();