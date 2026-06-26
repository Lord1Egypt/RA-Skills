const fs = require('fs');
const { execSync } = require('child_process');

const WATCHLIST_PATH = '/Users/bluepop/.openclaw/scripts/drama_watchlist.json';
const DOMAINS = ['1lou.icu', '1lou.one', '1lou.me', '1lou.xyz', '1lou.info', '1lou.vip', '1lou.pro'];
const EXCLUDE_KEYWORDS = ['网盘', '夸克', '片源', '无字'];

function getDomain() {
  for (const d of DOMAINS) {
    try {
      const r = execSync(`curl -sI --connect-timeout 5 "https://${d}" -o /dev/null -w "%{http_code}"`, {encoding:'utf-8'});
      if (r.trim().match(/200|301|302/)) return `https://${d}`;
    } catch(e) {}
  }
  return 'https://1lou.icu';
}

function search(keyword) {
  const domain = getDomain();
  for (let i = 0; i < 3; i++) {
    try {
      const url = `${domain}/?s=${encodeURIComponent(keyword)}`;
      console.log(`搜索: ${url}`);
      const html = execSync(`curl -sL --connect-timeout 20 -L "${url}"`, {encoding:'utf-8', maxBuffer: 20*1024*1024});
      if (html.length > 1000) return html;
    } catch(e) { console.log(`尝试${i+1}失败`); }
  }
  return '';
}

function parse(html, keyword) {
  if (!html) return [];
  const episodes = [];
  // 匹配各种格式
  const patterns = [
    /href="(thread-\d+\.htm)"[^>]*>.*?不良医生.*?第(\d+)集/g,
    /href="(thread-\d+\.htm)"[^>]*>([^<]*第(\d+)集[^<]*)<\/a>/g,
  ];
  
  // 简单方式：搜索包含"不良医生"和"第X集"的行
  const lines = html.split('\n');
  for (const line of lines) {
    if (line.includes(keyword) && line.includes('thread-') && line.includes('第')) {
      // 提取URL
      const urlMatch = line.match(/href="(thread-\d+\.htm)"/);
      const titleMatch = line.match(/>([^<]*第\d+集[^<]*)<\/a>/);
      if (urlMatch && titleMatch) {
        const title = titleMatch[1];
        if (!EXCLUDE_KEYWORDS.some(k => title.includes(k))) {
          const epMatch = title.match(/第(\d+)集/);
          episodes.push({
            title,
            url: `https://1lou.icu/${urlMatch[1]}`,
            episode: epMatch ? epMatch[1] : '?'
          });
        }
      }
    }
  }
  
  // 去重
  const seen = new Set();
  return episodes.filter(e => {
    if (seen.has(e.url)) return false;
    seen.add(e.url);
    return true;
  }).slice(0, 10);
}

function readWatchlist() {
  try {
    return fs.existsSync(WATCHLIST_PATH) ? JSON.parse(fs.readFileSync(WATCHLIST_PATH,'utf-8')) : [];
  } catch(e) { return []; }
}

async function main() {
  console.log('=== 1lou追剧检查 ===');
  const domain = getDomain();
  console.log(`使用域名: ${domain}\n`);
  
  const watchlist = readWatchlist();
  if (!watchlist.length) return '追剧清单为空';
  
  const results = [];
  for (const item of watchlist) {
    console.log(`检查: ${item.name}`);
    const html = search(item.keyword);
    const episodes = parse(html, item.keyword);
    console.log(`找到: ${episodes.length} 条\n`);
    if (episodes.length) results.push({name: item.name, downloaded: item.downloaded_episodes||'', episodes});
  }
  
  if (!results.length) return '暂无可更新的剧集';
  
  let msg = '📺 **1lou追剧更新**\n\n';
  for (const r of results) {
    msg += `**${r.name}**`;
    if (r.downloaded) msg += ` (已下载: ${r.downloaded})`;
    msg += '\n';
    for (const e of r.episodes) msg += `- [${e.title}](${e.url})\n`;
    msg += '\n';
  }
  return msg;
}

main().then(console.log).catch(console.error);
