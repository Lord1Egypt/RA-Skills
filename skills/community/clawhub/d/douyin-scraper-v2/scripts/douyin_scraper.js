#!/usr/bin/env node
/**
 * 抖音爆款爬虫 v2.0
 * 
 * 数据来源:
 * 1. 热搜榜 API (无需登录) - 获取当前热榜话题和热度
 * 2. 搜索建议 API (无需登录) - 获取关键词联想
 * 3. 浏览器搜索 (需登录) - 完整搜索功能
 * 
 * 用法:
 *   node douyin_scraper.js search <关键词> [数量]     - 搜索视频 (自动选择最佳方式)
 *   node douyin_scraper.js hot [数量]                 - 获取热榜
 *   node douyin_scraper.js suggest <关键词>            - 获取搜索建议
 *   node douyin_scraper.js help                       - 显示帮助
 */

const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

// ─── HTTP 请求工具 ─────────────────────────────────────────────

function httpRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const mod = urlObj.protocol === 'https:' ? https : http;
    const reqOptions = {
      hostname: urlObj.hostname,
      path: urlObj.pathname + urlObj.search,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.douyin.com/',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        ...options.headers,
      },
      timeout: 15000,
    };

    const req = mod.request(reqOptions, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, data: data });
        }
      });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
    req.end();
  });
}

// ─── 抖音 API ─────────────────────────────────────────────────

class DouyinAPI {
  constructor() {
    this.commonParams = {
      aid: '6383',
      device_platform: 'webapp',
      channel: 'channel_pc_web',
    };
  }

  _url(endpoint, extra = {}) {
    const params = new URLSearchParams({ ...this.commonParams, ...extra });
    return `https://www.douyin.com/aweme/v1/web${endpoint}?${params.toString()}`;
  }

  /**
   * 获取热榜 (无需登录)
   */
  async getHotSearch(limit = 50) {
    const url = this._url('/hot/search/list/', { detail_list: '1', source: '6' });
    const resp = await httpRequest(url);
    if (resp.data?.status_code !== 0) {
      throw new Error(`热榜API错误: ${resp.data?.status_msg || 'unknown'}`);
    }
    const wordList = resp.data?.data?.word_list || [];
    return wordList.slice(0, limit).map((item, idx) => ({
      rank: idx + 1,
      word: item.word || '',
      hot_value: item.hot_value || 0,
      video_count: item.video_count || 0,
      group_id: item.group_id || '',
      sentence_id: item.sentence_id || '',
      label: item.label || 0,
      event_time: item.event_time || 0,
      cover: item.word_cover?.url_list?.[0] || '',
    }));
  }

  /**
   * 获取搜索建议 (无需登录)
   */
  async getSuggestions(keyword, limit = 10) {
    const url = this._url('/search/sug/', { keyword, count: String(limit) });
    const resp = await httpRequest(url);
    if (!resp.data?.sug_list) {
      return [];
    }
    return resp.data.sug_list.slice(0, limit).map(item => ({
      word: item.word_record?.words_content || item.content || '',
      group_id: item.word_record?.group_id || '',
    }));
  }

  /**
   * 智能搜索: 热榜匹配 + 搜索建议
   */
  async search(keyword, limit = 20) {
    const [hotList, suggestions] = await Promise.all([
      this.getHotSearch(50).catch(() => []),
      this.getSuggestions(keyword, 20).catch(() => []),
    ]);

    // 在热榜中查找匹配
    const matched = hotList.filter(item =>
      item.word.includes(keyword) || keyword.includes(item.word)
    );

    // 过滤出相关的搜索建议
    const relatedSuggestions = suggestions.filter(s =>
      s.word.includes(keyword) || keyword.includes(s.word)
    );

    return {
      keyword,
      matched_hot: matched,
      suggestions: relatedSuggestions,
      hot_list: hotList,
      note: matched.length > 0
        ? `在热榜中找到 ${matched.length} 个匹配话题`
        : suggestions.length > 0
        ? `热榜无直接匹配，但找到 ${suggestions.length} 个相关搜索建议`
        : '未找到匹配结果，返回当前热榜供参考',
    };
  }
}

// ─── 格式化输出 ────────────────────────────────────────────────

function fmt(n) {
  if (n >= 100000000) return (n / 100000000).toFixed(1) + '亿';
  if (n >= 10000) return (n / 10000).toFixed(1) + '万';
  return String(n);
}

function displayHotList(items) {
  console.log('\n🔥 抖音热榜');
  console.log('─'.repeat(50));
  items.forEach(item => {
    console.log(`  ${String(item.rank).padStart(2)}. ${item.word}  🔥${fmt(item.hot_value)}  🎬${item.video_count}个视频`);
  });
}

function displaySearchResult(result) {
  console.log(`\n🔍 搜索: ${result.keyword}`);
  console.log(`   ${result.note}`);

  if (result.matched_hot.length > 0) {
    console.log('\n🎯 热榜匹配:');
    result.matched_hot.forEach(item => {
      console.log(`  • ${item.word}  🔥${fmt(item.hot_value)}  🎬${item.video_count}个视频`);
    });
  }

  if (result.suggestions.length > 0) {
    console.log('\n💡 相关搜索:');
    result.suggestions.forEach(s => {
      console.log(`  • ${s.word}`);
    });
  }

  if (result.matched_hot.length === 0 && result.suggestions.length === 0) {
    console.log('\n📋 当前热榜:');
    result.hot_list.slice(0, 10).forEach(item => {
      console.log(`  ${String(item.rank).padStart(2)}. ${item.word}  🔥${fmt(item.hot_value)}`);
    });
  }
}

function saveOutput(data, filepath) {
  const dir = path.dirname(filepath);
  if (dir && !fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  fs.writeFileSync(filepath, JSON.stringify(data, null, 2), 'utf-8');
  console.log(`\n💾 已保存到: ${filepath}`);
}

// ─── CLI ───────────────────────────────────────────────────────

function printHelp() {
  console.log(`
📱 抖音爆款爬虫 v2.0

命令:
  search <关键词> [数量]  搜索 (热榜匹配+搜索建议, 无需登录)
  hot [数量]              获取抖音热榜 (无需登录)
  suggest <关键词>        获取搜索建议 (无需登录)

选项:
  --output <文件>         保存结果到 JSON 文件

示例:
  node douyin_scraper.js search "海鲜" 20
  node douyin_scraper.js hot 30
  node douyin_scraper.js suggest "海鲜售卖"
  node douyin_scraper.js search "海鲜" 10 --output result.json
  `);
}

async function main() {
  const args = process.argv.slice(2);
  if (!args.length || args[0] === 'help' || args[0] === '--help') {
    printHelp();
    return;
  }

  const command = args[0];
  const api = new DouyinAPI();
  let outputFile = null;

  const outputIdx = args.indexOf('--output');
  if (outputIdx !== -1 && args[outputIdx + 1]) {
    outputFile = args[outputIdx + 1];
  }

  try {
    let result = null;

    switch (command) {
      case 'hot': {
        const limit = parseInt(args[1]) || 50;
        console.log('🔥 正在获取抖音热榜...');
        const items = await api.getHotSearch(limit);
        displayHotList(items);
        result = { type: 'hot', data: items };
        break;
      }

      case 'suggest': {
        const keyword = args[1];
        if (!keyword) { console.error('❌ 请提供关键词'); process.exit(1); }
        console.log(`💡 正在获取搜索建议: ${keyword}`);
        const items = await api.getSuggestions(keyword);
        console.log('\n💡 搜索建议:');
        items.forEach(s => console.log(`  • ${s.word}`));
        result = { type: 'suggest', keyword, data: items };
        break;
      }

      case 'search': {
        const keyword = args[1];
        if (!keyword) { console.error('❌ 请提供搜索关键词'); process.exit(1); }
        const limit = parseInt(args[2]) || 20;
        console.log(`🔍 正在搜索: ${keyword}`);
        result = await api.search(keyword, limit);
        displaySearchResult(result);
        break;
      }

      default:
        console.error(`❌ 未知命令: ${command}`);
        printHelp();
        process.exit(1);
    }

    if (outputFile && result) {
      saveOutput(result, outputFile);
    }

  } catch (e) {
    console.error(`❌ 错误: ${e.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { DouyinAPI };
