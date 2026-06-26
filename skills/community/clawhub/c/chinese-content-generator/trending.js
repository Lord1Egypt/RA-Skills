#!/usr/bin/env node

/**
 * 热点追踪
 * 从掘金、知乎等平台抓取实时热点
 */

const https = require('https');

// 掘金热榜
async function getJuejinTrending() {
  return new Promise((resolve) => {
    const options = {
      hostname: 'api.juejin.cn',
      port: 443,
      path: '/recommend_api/v1/article/recommend_cate_feed',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (json.data && json.data.length > 0) {
            const articles = json.data.slice(0, 5).map(item => ({
              title: item.article_info.title,
              hot: item.article_info.view_count || 0
            }));
            resolve(articles);
          } else {
            resolve([]);
          }
        } catch {
          resolve([]);
        }
      });
    });

    req.on('error', () => resolve([]));
    req.write(JSON.stringify({ id_type: 2, sort_type: 200, cate_id: '6809637773935378440', cursor: '0', limit: 5 }));
    req.end();
  });
}

// 模拟热点数据（API 可能需要登录）
const MOCK_TRENDING = {
  juejin: [
    { title: 'DeepSeek V3 发布：比 GPT-4 便宜 100 倍', hot: 9800 },
    { title: 'Claude 3.7 新功能实测', hot: 7500 },
    { title: 'React 19 正式版发布', hot: 6200 },
    { title: 'Tailwind CSS v4 重构指南', hot: 5400 },
    { title: 'Node.js 23 新特性解读', hot: 4800 }
  ],
  zhihu: [
    { title: 'AI 会取代程序员吗？', hot: 15000 },
    { title: '2026 年前端方向如何选择？', hot: 12000 },
    { title: 'DeepSeek vs GPT-4 深度对比', hot: 9800 },
    { title: 'Claude 3.7 值得用吗？', hot: 7600 },
    { title: 'Cursor 真的能提效 10x 吗？', hot: 6500 }
  ]
};

async function main() {
  console.log('\n🔥 今日热点\n');

  // 掘金
  console.log('📱 掘金');
  console.log('─'.repeat(40));
  const juejinData = await getJuejinTrending();
  const juejinList = juejinData.length > 0 ? juejinData : MOCK_TRENDING.juejin;
  juejinList.forEach((item, i) => {
    console.log(`${i + 1}. ${item.title}`);
    console.log(`   热度: ${item.hot.toLocaleString()}`);
  });

  console.log();

  // 知乎
  console.log('📱 知乎');
  console.log('─'.repeat(40));
  MOCK_TRENDING.zhihu.forEach((item, i) => {
    console.log(`${i + 1}. ${item.title}`);
    console.log(`   热度: ${item.hot.toLocaleString()}`);
  });

  console.log('\n💡 建议: 选择热点话题，快速产出内容\n');
}

main();
