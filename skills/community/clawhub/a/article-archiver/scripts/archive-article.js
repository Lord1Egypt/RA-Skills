#!/usr/bin/env node
/**
 * Article Archiver - Main Script
 * 自动识别链接类型并抓取完整内容
 * Usage: node archive-article.js <url>
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

async function archiveArticle(url) {
  console.log(`开始归档: ${url}`);
  
  // 识别链接类型
  const isTwitterArticle = url.includes('x.com/i/article/') || 
                          (url.includes('x.com') && url.includes('status'));
  
  let title = '';
  let content = '';
  let source = '';
  
  if (isTwitterArticle) {
    console.log('检测到 Twitter Article，使用 Playwright 抓取...');
    
    // 读取 Cookie
    const cookieFile = path.join(__dirname, '../config/twitter-cookies.txt');
    if (!fs.existsSync(cookieFile)) {
      console.error('错误：未找到 Twitter Cookie 配置文件');
      console.error('请运行：echo "auth_token=xxx; ct0=yyy" > config/twitter-cookies.txt');
      process.exit(1);
    }
    
    const cookieString = fs.readFileSync(cookieFile, 'utf8').trim();
    
    // 如果是推文链接，先提取 Article ID
    let articleUrl = url;
    if (url.includes('/status/') && !url.includes('/i/article/')) {
      // 需要先获取推文，提取 Article 链接
      console.log('从推文中提取 Article 链接...');
      // 这里简化处理，假设用户直接提供 Article 链接
    }
    
    // 调用 Twitter Article 抓取脚本
    const scriptPath = path.join(__dirname, 'fetch-twitter-article.js');
    const result = execSync(
      `node "${scriptPath}" "${articleUrl}" "${cookieString}"`,
      { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
    );
    
    const data = JSON.parse(result);
    
    if (!data.success) {
      console.error('抓取失败:', data.error);
      process.exit(1);
    }
    
    title = data.title || '未命名文章';
    content = data.content;
    source = 'x.com (Twitter Article)';
    
  } else {
    console.log('检测到普通网页，使用 web_fetch 抓取...');
    
    // 使用 curl + Jina Reader
    try {
      const result = execSync(
        `curl -s "https://r.jina.ai/${url}" -H "Accept: text/markdown"`,
        { encoding: 'utf8', maxBuffer: 10 * 1024 * 1024 }
      );
      
      // 提取标题和内容
      const lines = result.split('\n');
      const titleLine = lines.find(line => line.startsWith('Title:'));
      title = titleLine ? titleLine.replace('Title:', '').trim() : '未命名文章';
      
      // 提取 Markdown 内容
      const contentStart = lines.findIndex(line => line.includes('Markdown Content:'));
      if (contentStart !== -1) {
        content = lines.slice(contentStart + 1).join('\n').trim();
      } else {
        content = result;
      }
      
      const urlObj = new URL(url);
      source = urlObj.hostname;
      
    } catch (error) {
      console.error('抓取失败:', error.message);
      process.exit(1);
    }
  }
  
  // 准备归档数据
  const now = new Date();
  const archiveTime = now.toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
  const month = now.toISOString().slice(0, 7);
  
  const archiveData = {
    title,
    url,
    source,
    archiveTime,
    month,
    content
  };
  
  // 输出 JSON 供 OpenClaw 处理
  console.log(JSON.stringify(archiveData, null, 2));
}

// 命令行调用
if (require.main === module) {
  const url = process.argv[2];
  
  if (!url) {
    console.error('Usage: node archive-article.js <url>');
    process.exit(1);
  }
  
  archiveArticle(url).catch(error => {
    console.error('Error:', error);
    process.exit(1);
  });
}

module.exports = { archiveArticle };
