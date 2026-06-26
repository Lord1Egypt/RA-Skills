#!/usr/bin/env node
/**
 * Claw Search - OpenClaw Skill 脚本
 * 使用本地 Claw Search API 进行搜索
 */

const API_BASE = process.env.CLAW_SEARCH_URL || 'https://api.claw-search.com';

async function search(query, options = {}) {
  const { count = 10, country = 'CN', freshness } = options;
  
  try {
    const response = await fetch(`${API_BASE}/api/search`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query, count, country, freshness })
    });
    
    if (!response.ok) {
      throw new Error(`API Error: ${response.status}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('搜索失败:', error.message);
    process.exit(1);
  }
}

// CLI 入口
const args = process.argv.slice(2);
if (args.length === 0) {
  console.log('Claw Search CLI');
  console.log('Usage: node search.mjs "query" [-n count]');
  console.log('Example: node search.mjs "openclaw" -n 10');
  process.exit(1);
}

const query = args[0];
let count = 10;

for (let i = 1; i < args.length; i++) {
  if (args[i] === '-n' && args[i + 1]) {
    count = parseInt(args[i + 1]);
    i++;
  }
}

const results = await search(query, { count });

console.log(`\n🔍 搜索: "${results.query}"`);
console.log(`📊 结果: ${results.count} 条\n`);

if (results.results.length === 0) {
  console.log('未找到结果');
} else {
  results.results.forEach((item, index) => {
    console.log(`${index + 1}. ${item.title}`);
    console.log(`   🔗 ${item.url}`);
    if (item.description) {
      console.log(`   📝 ${item.description.substring(0, 100)}...`);
    }
    console.log();
  });
}
