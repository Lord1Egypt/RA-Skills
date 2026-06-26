/**
 * Tech News Daily - 科技资讯自动聚合 (Node.js 版本)
 * 用法：node tech-news-daily.js [date]
 */

const fs = require('fs');
const path = require('path');
const https = require('https');

function fetchJSON(url) {
  return new Promise((resolve, reject) => {
    https.get(url, { headers: { 'User-Agent': 'node' } }, res => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); } catch (e) { reject(e); }
      });
    }).on('error', reject);
  });
}

// 配置
const DATE = process.env.TODAY || new Date().toISOString().split('T')[0];
const OUTPUT_DIR = path.join(__dirname, 'data', 'daily');
const OUTPUT_FILE = path.join(OUTPUT_DIR, `${DATE}.json`);

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

console.log(`\n=== 科技日报生成：${DATE} ===\n`);

(async () => {
// 1. GitHub Trending
console.log('[1/3] 抓取 GitHub Trending...');
let githubItems = [];
try {
  const data = await fetchJSON('https://api.github.com/search/repositories?q=created:>2025-03-30+stars:>10&sort=stars&per_page=10');
  githubItems = (data.items || []).slice(0, 10).map(i => ({
    title: i.name,
    description: i.description || '无简介',
    html_url: i.html_url,
    stargazers_count: i.stargazers_count
  }));
  console.log(`  - GitHub: ${githubItems.length} 条`);
} catch (e) {
  console.log(`  - GitHub: 失败 ${e.message}`);
}

// 2. 模拟 RSS 抓取（暂时用固定内容替代）
console.log('[2/3] 模拟 RSS 信源...');
const mockNews = [
  { source: "机器之心", title: "AI 最新进展", url: "#" },
  { source: "量子位", title: "大模型更新", url: "#" }
];
console.log(`  - RSS: ${mockNews.length} 条`);

// 3. 生成日报
console.log('[3/3] 生成日报...');
const report = {
  date: DATE,
  title: `📅 科技日报 | ${DATE}`,
  sections: {
    "重磅": [],
    "技术前沿": githubItems,
    "行业动态": mockNews,
    "AI 应用": []
  },
  total: githubItems.length + mockNews.length,
  generated_at: new Date().toISOString()
};

fs.writeFileSync(OUTPUT_FILE, JSON.stringify(report, null, 2));
console.log(`\n✅ 日报已保存：${OUTPUT_FILE}`);
console.log(`📊 共计 ${report.total} 条资讯`);

})();
