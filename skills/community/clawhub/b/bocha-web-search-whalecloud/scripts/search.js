#!/usr/bin/env node
/**
 * Bocha Search — 通过浩鲸科技大模型网关代理调用 Bocha 搜索 API
 * 
 * 安全设计：脚本内部读取凭证，Agent 不接触 token
 * 凭证来源：环境变量 WHALECLOUD_API_KEY（浩鲸大模型网关 token）
 */

// Credentialless: no fs/path imports needed

// --- 凭证读取（Agent 不可见） ---
function getApiKey() {
  return process.env.WHALECLOUD_API_KEY || null;
}

// --- 解析参数 ---
const args = process.argv.slice(2);
if (args.length === 0) {
  usage();
}

function usage() {
  process.stderr.write(
`用法: node scripts/search.js "<query>" [options]

选项:
  --count <n>        返回结果数 (1-50, 默认 10)
  --freshness <v>    时间范围: noLimit | oneDay | oneWeek | oneMonth | oneYear
  --no-summary       不返回摘要 (默认开启)
  --type <type>      搜索类型: web (默认) | ai
  --raw              输出原始 JSON 响应

示例:
  node scripts/search.js "人工智能最新进展"
  node scripts/search.js "AI新闻" --freshness oneWeek --count 5
  node scripts/search.js "西瓜功效" --type ai
`
  );
  process.exit(1);
}

// 解析命令行参数
let query = '';
let count = 10;
let freshness = 'noLimit';
let summary = true;
let searchType = 'web';
let rawOutput = false;

for (let i = 0; i < args.length; i++) {
  switch (args[i]) {
    case '--count': count = parseInt(args[++i]) || 10; break;
    case '--freshness': freshness = args[++i] || 'noLimit'; break;
    case '--no-summary': summary = false; break;
    case '--type': searchType = args[++i] || 'web'; break;
    case '--raw': rawOutput = true; break;
    default:
      if (!query) query = args[i];
      else { process.stderr.write(`未知参数: ${args[i]}\n`); process.exit(1); }
  }
}

if (!query) {
  process.stderr.write('错误: 缺少搜索词\n');
  process.exit(1);
}

const apiKey = getApiKey();
if (!apiKey) {
  process.stderr.write('错误: WHALECLOUD_API_KEY 未配置。请在 openclaw.json 的 skills.entries 中设置该环境变量。\n');
  process.exit(1);
}

// --- API 调用 ---
const BASE_URL = 'https://lab.iwhalecloud.com/gpt-proxy/bocha/v1';
const endpoint = searchType === 'ai' ? 'ai-search' : 'web-search';

const body = { query, freshness, count };
if (searchType === 'web') body.summary = summary;
if (searchType === 'ai') body.answer = true;

fetch(`${BASE_URL}/${endpoint}`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${apiKey}`
  },
  body: JSON.stringify(body)
})
.then(res => res.json())
.then(data => {
  if (rawOutput) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  // 检查错误
  if (data.code && data.code !== 200) {
    const errMsg = {
      type: 'error',
      code: String(data.code),
      message: data.msg || data.message || '未知错误',
      hint: getHint(data.code)
    };
    console.log(JSON.stringify(errMsg, null, 2));
    return;
  }

  // 格式化输出 web-search 结果
  if (searchType === 'web' && data.data && data.data.webPages) {
    const pages = data.data.webPages.value || [];
    const result = {
      type: 'search',
      query: data.data.queryContext?.originalQuery || query,
      totalEstimatedMatches: data.data.webPages.totalEstimatedMatches || 0,
      resultCount: pages.length,
      results: pages.map((p, i) => ({
        index: i + 1,
        title: p.name,
        url: p.url,
        displayUrl: p.displayUrl || p.url,
        snippet: p.snippet || '',
        summary: p.summary || '',
        siteName: p.siteName || '',
        datePublished: p.datePublished || ''
      })),
      images: (data.data.images?.value || []).map(img => ({
        contentUrl: img.contentUrl,
        hostPageUrl: img.hostPageUrl,
        width: img.width,
        height: img.height
      }))
    };
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  // 格式化输出 ai-search 结果
  if (searchType === 'ai' && data.data) {
    const pages = data.data.webPages?.value || [];
    const result = {
      type: 'ai-search',
      query: query,
      answer: data.data.answer || '',
      followUpQuestions: data.data.followUpQuestions || [],
      resultCount: pages.length,
      results: pages.map((p, i) => ({
        index: i + 1,
        title: p.name,
        url: p.url,
        snippet: p.snippet || '',
        summary: p.summary || '',
        siteName: p.siteName || '',
        datePublished: p.datePublished || ''
      }))
    };
    console.log(JSON.stringify(result, null, 2));
    return;
  }

  // 未知格式，原样输出
  console.log(JSON.stringify(data, null, 2));
})
.catch(err => {
  console.log(JSON.stringify({
    type: 'error',
    code: 'NETWORK',
    message: err.message,
    hint: '网络请求失败，请检查网络连接'
  }, null, 2));
  process.exit(1);
});

function getHint(code) {
  const hints = {
    '400': '参数错误，请检查搜索词',
    '401': 'WHALECLOUD_API_KEY 无效，请检查 skills.entries 配置',
    '403': '余额或权限不足，请联系管理员',
    '429': '请求频率过高，请稍后重试',
    '500': '服务端错误，请联系管理员排查（保留 log_id）'
  };
  return hints[String(code)] || '请联系管理员';
}
