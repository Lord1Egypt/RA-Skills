#!/usr/bin/env node

/**
 * Bing Search for OpenClaw
 * 使用必应中文搜索引擎
 */

const https = require('https');
const http = require('http');

const BLACKLIST = [
  'zhihu.com',
  'xiaohongshu.com', 
  'weibo.com',
  'weixin.qq.com',
  'douyin.com',
  'tiktok.com',
  'bilibili.com',
  'csdn.net'
];

function isBlacklisted(url) {
  return BLACKLIST.some(domain => url.includes(domain));
}

function parseHtmlEntities(text) {
  return text
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'")
    .replace(/&#(\d+);/g, (_, num) => String.fromCharCode(parseInt(num, 10)));
}

function cleanText(html) {
  return parseHtmlEntities(html.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim());
}

async function bingSearch(query, count = 10, offset = 0) {
  return new Promise((resolve, reject) => {
    const searchUrl = `https://cn.bing.com/search?q=${encodeURIComponent(query)}&first=${offset + 1}&count=${count}`;
    
    const req = https.get(searchUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Cookie': 'SRCHHPGUSR=ADLT=Off&CRTLS=1'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const results = parseBingResults(data, count);
          resolve({
            total: results.length,
            results: results
          });
        } catch (e) {
          reject(e);
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('请求超时'));
    });
  });
}

function parseBingResults(html, maxResults = 10) {
  const results = [];
  
  // 匹配结果总数
  const totalMatch = html.match(/约\s*([\d,]+)\s*个结果/i);
  const total = totalMatch ? totalMatch[1].replace(/,/g, '') : '0';
  
  // 使用更宽松的正则匹配搜索结果
  // 匹配 b_algo 块中的内容
  const algoRegex = /<li[^>]*class="b_algo"[^>]*>[\s\S]*?<\/li>/gi;
  let match;
  
  while ((match = algoRegex.exec(html)) !== null && results.length < maxResults) {
    const block = match[0];
    
    // 提取h2中的链接（这是标题）
    const h2Match = block.match(/<h2[^>]*>[\s\S]*?<a[^>]+href="([^"]+)"[^>]*>([\s\S]*?)<\/a>[\s\S]*?<\/h2>/i);
    if (!h2Match) continue;
    
    const url = h2Match[1];
    const title = cleanText(h2Match[2]);
    
    // 跳过黑名单网站
    if (isBlacklisted(url)) continue;
    
    // 提取摘要 - 查找 b_caption 或 p 标签
    let snippet = '';
    const captionMatch = block.match(/<p[^>]*>([\s\S]*?)<\/p>/i);
    if (captionMatch) {
      snippet = cleanText(captionMatch[1]);
    }
    
    // 提取网站名称
    let site = '';
    const siteMatch = block.match(/<cite>([\s\S]*?)<\/cite>/i);
    if (siteMatch) {
      site = cleanText(siteMatch[1]).split('›')[0].trim();
    }
    
    // 清理URL（去除跟踪参数）
    const cleanUrl = url.split('?')[0];
    
    if (title && cleanUrl) {
      results.push({
        title,
        url: cleanUrl,
        snippet: snippet.substring(0, 200),
        site
      });
    }
  }
  
  // 如果上面的方法没找到结果，尝试备用方法
  if (results.length === 0) {
    // 备用：直接搜索所有链接
    const linkRegex = /<a[^>]+href="(https?:\/\/[^"]+)"[^>]*>([^<]+)<\/a>/gi;
    let linkMatch;
    const seen = new Set();
    
    while ((linkMatch = linkRegex.exec(html)) !== null && results.length < maxResults * 2) {
      const url = linkMatch[1];
      const title = cleanText(linkMatch[2]);
      
      if (isBlacklisted(url)) continue;
      if (seen.has(url)) continue;
      if (!title || title.length < 3) continue;
      if (url.includes('bing.com') || url.includes('microsoft.com')) continue;
      
      seen.add(url);
      results.push({
        title,
        url,
        snippet: '',
        site: new URL(url).hostname
      });
    }
  }
  
  return {
    total: results.length,
    results: results.slice(0, maxResults)
  };
}

async function crawlWebpage(url) {
  if (isBlacklisted(url)) {
    throw new Error('该网站在黑名单中，无法抓取');
  }
  
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    
    const req = client.get(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        // 提取标题
        const titleMatch = data.match(/<title>([^<]+)<\/title>/i);
        const title = titleMatch ? cleanText(titleMatch[1]) : '无标题';
        
        // 移除脚本和样式
        let text = data
          .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
          .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
          .replace(/<header[^>]*>[\s\S]*?<\/header>/gi, '')
          .replace(/<footer[^>]*>[\s\S]*?<\/footer>/gi, '')
          .replace(/<nav[^>]*>[\s\S]*?<\/nav>/gi, '')
          .replace(/<[^>]+>/g, ' ')
          .replace(/\s+/g, ' ')
          .trim();
        
        // 限制长度
        text = text.substring(0, 8000);
        
        resolve({ title, content: text });
      });
    });
    
    req.on('error', reject);
    req.setTimeout(15000, () => {
      req.destroy();
      reject(new Error('请求超时'));
    });
  });
}

// CLI 接口
const args = process.argv.slice(2);
const command = args[0];

async function main() {
  try {
    if (command === 'search') {
      const query = args[1];
      const count = parseInt(args[2]) || 10;
      const offset = parseInt(args[3]) || 0;
      
      const result = await bingSearch(query, count, offset);
      console.log(JSON.stringify(result, null, 2));
    } else if (command === 'fetch') {
      const url = args[1];
      const result = await crawlWebpage(url);
      console.log(JSON.stringify(result, null, 2));
    } else {
      console.log(JSON.stringify({ 
        help: '用法: node bing-search.js search <关键词> [数量] [偏移]',
        example: 'node bing-search.js search "Python教程" 10 0'
      }));
    }
  } catch (e) {
    console.log(JSON.stringify({ success: false, error: e.message }));
  }
}

main();
