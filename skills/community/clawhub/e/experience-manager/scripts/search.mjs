#!/usr/bin/env node
/**
 * 经验搜索脚本
 * 从 Experience Hub 搜索已发布的经验包
 */

import https from 'https';
import http from 'http';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const HUB_API_BASE = 'https://www.expericehub.com:18080';

// HTTP 请求封装
function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    const protocol = url.startsWith('https') ? https : http;
    
    const req = protocol.get(url, options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve(json);
        } catch (e) {
          reject(new Error(`解析失败: ${data}`));
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(10000, () => {
      req.destroy();
      reject(new Error('请求超时'));
    });
  });
}

// 主函数
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0) {
    console.error('用法: node search.mjs <关键词>');
    console.error('示例: node search.mjs feishu');
    console.error('示例: node search.mjs "飞书 文档"');
    process.exit(1);
  }
  
  const keyword = args.join(' ');
  
  console.log(`🔍 搜索: "${keyword}"`);
  console.log();
  
  try {
    const url = `${HUB_API_BASE}/api/search?q=${encodeURIComponent(keyword)}`;
    const result = await request(url);
    
    // API 返回格式: { data: [...], total: N }
    const results = result.data || result.results || [];
    
    if (results.length > 0) {
      console.log(`📦 找到 ${results.length} 个经验包:\n`);
      
      results.forEach((exp, i) => {
        console.log(`${i + 1}. ${exp.id}`);
        console.log(`   名称: ${exp.name}`);
        if (exp.description) {
          console.log(`   描述: ${exp.description}`);
        }
        console.log();
      });
      
      console.log('💡 使用 "学习经验 <URL或ID>" 下载并学习');
      console.log('   示例: learn https://www.expericehub.com:18080/pkg/feishu-doc-writing-1.1.0.zip');
    } else {
      console.log('❌ 未找到相关经验包');
      console.log('💡 您可以尝试其他关键词，或先创建经验包后发布到 Hub');
    }
    
  } catch (err) {
    console.error('❌ 搜索失败:', err.message);
    process.exit(1);
  }
}

main();