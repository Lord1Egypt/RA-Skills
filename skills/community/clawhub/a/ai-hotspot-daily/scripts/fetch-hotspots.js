#!/usr/bin/env node
/**
 * 抓取全网热点
 * 用法：node fetch-hotspots.js
 */

const https = require('https');
const http = require('http');

// 数据源配置
const SOURCES = {
  weibo: {
    name: '微博热搜',
    url: 'https://rsshub.app/weibo/search/hot',
    priority: 5
  },
  zhihu: {
    name: '知乎热榜',
    url: 'https://rsshub.app/zhihu/hotlist',
    priority: 5
  },
  douyin: {
    name: '抖音热榜',
    url: 'https://rsshub.app/douyin/hotlist',
    priority: 4
  },
  baidu: {
    name: '百度热搜',
    url: 'https://rsshub.app/baidu/hotsearch',
    priority: 4
  },
  '36kr': {
    name: '36 氪',
    url: 'https://rsshub.app/36kr/news/latest',
    priority: 4
  },
  huxiu: {
    name: '虎嗅',
    url: 'https://www.huxiu.com/rss/1.xml',
    priority: 3
  }
};

/**
 * 发起 HTTP 请求
 */
function fetch(url) {
  return new Promise((resolve, reject) => {
    const client = url.startsWith('https') ? https : http;
    client.get(url, (res) => {
      if (res.statusCode !== 200) {
        reject(new Error(`HTTP ${res.statusCode}`));
        return;
      }
      const chunks = [];
      res.on('data', chunk => chunks.push(chunk));
      res.on('end', () => {
        resolve(Buffer.concat(chunks).toString('utf8'));
      });
    }).on('error', reject);
  });
}

/**
 * 解析 RSS
 */
function parseRSS(xml) {
  const items = [];
  const itemRegex = /<item>([\s\S]*?)<\/item>/g;
  const titleRegex = /<title>([^<]+)<\/title>/;
  const linkRegex = /<link>([^<]+)<\/link>/;
  const pubDateRegex = /<pubDate>([^<]+)<\/pubDate>/;
  const descriptionRegex = /<description>([\s\S]*?)<\/description>/;
  
  let match;
  while ((match = itemRegex.exec(xml)) !== null) {
    const itemXml = match[1];
    const title = titleRegex.exec(itemXml)?.[1] || '';
    const link = linkRegex.exec(itemXml)?.[1] || '';
    const pubDate = pubDateRegex.exec(itemXml)?.[1] || '';
    const description = descriptionRegex.exec(itemXml)?.[1] || '';
    
    items.push({
      title: title.trim(),
      link,
      pubDate,
      description: description.trim()
    });
  }
  
  return items;
}

/**
 * 抓取单个平台
 */
async function fetchSource(key, config) {
  console.log(`📡 抓取 ${config.name}...`);
  
  try {
    const xml = await fetch(config.url);
    const items = parseRSS(xml);
    
    console.log(`✅ ${config.name}: ${items.length} 条`);
    
    return {
      source: key,
      name: config.name,
      priority: config.priority,
      items: items.slice(0, 50), // 取前 50
      fetchedAt: new Date().toISOString()
    };
  } catch (error) {
    console.warn(`⚠️ ${config.name} 抓取失败：${error.message}`);
    return null;
  }
}

/**
 * 智能去重
 */
function dedupeHotspots(allHotspots) {
  const seen = new Set();
  const deduped = [];
  
  for (const hotspot of allHotspots) {
    // 简化标题用于去重
    const key = hotspot.title.replace(/[^\u4e00-\u9fa5a-zA-Z0-9]/g, '').toLowerCase();
    
    if (!seen.has(key)) {
      seen.add(key);
      deduped.push(hotspot);
    }
  }
  
  return deduped;
}

/**
 * 生成 AI 回应建议
 */
function generateAISuggestion(item, source) {
  // 简单规则
  const title = item.title.toLowerCase();
  
  if (title.includes('明星') || title.includes('离婚') || title.includes('出轨')) {
    return {
      sentiment: '吃瓜',
      suggestion: '保持中立，不站队，建议等官方消息'
    };
  }
  
  if (title.includes('发布') || title.includes('新品') || title.includes('科技')) {
    return {
      sentiment: '期待',
      suggestion: '客观评价，对比竞品，说明自身特点'
    };
  }
  
  if (title.includes('股票') || title.includes('股价') || title.includes('财经')) {
    return {
      sentiment: '关注',
      suggestion: '提醒投资有风险，不构成投资建议'
    };
  }
  
  if (title.includes('如何评价') || title.includes('怎么看')) {
    return {
      sentiment: '讨论',
      suggestion: '呈现多方观点，避免主观判断'
    };
  }
  
  return {
    sentiment: '中性',
    suggestion: '客观陈述事实，提醒用户核实信息'
  };
}

/**
 * 主函数
 */
async function main() {
  console.log('🦆 全网热点聚合工具\n');
  console.log(`📅 抓取时间：${new Date().toISOString()}\n`);
  
  const results = [];
  
  // 并发抓取
  const promises = Object.entries(SOURCES).map(([key, config]) => 
    fetchSource(key, config)
  );
  
  const fetched = await Promise.all(promises);
  
  // 过滤失败的
  for (const result of fetched) {
    if (result) {
      results.push(result);
    }
  }
  
  console.log(`\n📊 成功抓取 ${results.length} 个平台\n`);
  
  // 合并所有热点
  const allItems = [];
  for (const result of results) {
    for (const item of result.items) {
      const suggestion = generateAISuggestion(item, result.name);
      allItems.push({
        ...item,
        source: result.name,
        source_priority: result.priority,
        ...suggestion
      });
    }
  }
  
  // 去重
  const deduped = dedupeHotspots(allItems);
  console.log(`📦 去重后热点数：${deduped.length}`);
  
  // 保存到文件
  const date = new Date().toISOString().split('T')[0];
  const outputFile = `/home/lin/.openclaw/extensions/openclaw-weixin/skills/hotspot-aggregator/data/hotspots-${date}.json`;
  
  const output = {
    date,
    generatedAt: new Date().toISOString(),
    sources: results,
    all_items: deduped,
    total_count: deduped.length
  };
  
  const fs = require('fs');
  fs.writeFileSync(outputFile, JSON.stringify(output, null, 2));
  console.log(`💾 数据已保存：${outputFile}`);
  
  // 打印摘要
  console.log('\n🔥 热点摘要：');
  deduped.slice(0, 10).forEach((item, i) => {
    console.log(`${i + 1}. [${item.source}] ${item.title}`);
  });
}

main();
