#!/usr/bin/env node
/**
 * Bilibili热搜抓取 - Skill 版本
 * 使用B站排行榜API接口
 */
const https = require('https');
const fs = require('fs');
const path = require('path');

// Skill 工作目录
const WORKSPACE = process.env.WORKSPACE || '/home/openclaw/.openclaw/workspace';
const OUTPUT_DIR = path.join(WORKSPACE, 'scripts');

// B站全站排行榜API
const BILI_RANK_API = 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all';

async function fetchBilibiliRank() {
  return new Promise((resolve, reject) => {
    console.log('📊 获取B站全站排行榜...');
    
    https.get(BILI_RANK_API, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          
          if (result.code === 0 && result.data && result.data.list) {
            console.log(`✅ 获取到 ${result.data.list.length} 条排行榜数据`);
            
            const rankItems = result.data.list.slice(0, 50).map((item, index) => ({
              rank: index + 1,
              title: item.title || '',
              up: item.owner ? item.owner.name : '',
              play: item.stat ? formatNumber(item.stat.view) + '播放' : '',
              danmu: item.stat ? formatNumber(item.stat.danmaku) + '弹幕' : '',
              like: item.stat ? formatNumber(item.stat.like) + '点赞' : '',
              coin: item.stat ? formatNumber(item.stat.coin) + '投币' : '',
              favorite: item.stat ? formatNumber(item.stat.favorite) + '收藏' : '',
              score: item.pts || 0,
              link: `https://www.bilibili.com/video/${item.bvid}`,
              type: '全站榜'
            }));
            
            resolve(rankItems);
          } else {
            console.log('❌ API返回错误:', result.message || '未知错误');
            reject(new Error(`API错误: ${result.message || '未知'}`));
          }
        } catch (error) {
          console.log('❌ 解析API响应失败:', error.message);
          reject(error);
        }
      });
      
    }).on('error', (error) => {
      console.log('❌ 网络请求失败:', error.message);
      reject(error);
    });
  });
}

// 格式化数字（万/亿）
function formatNumber(num) {
  if (num >= 100000000) {
    return (num / 100000000).toFixed(1) + '亿';
  } else if (num >= 10000) {
    return (num / 10000).toFixed(1) + '万';
  } else {
    return num.toString();
  }
}

async function main() {
  try {
    console.log('🎯 开始抓取Bilibili热搜...');
    const data = await fetchBilibiliRank();
    
    if (!data || data.length === 0) {
      console.log('❌ 抓取失败，未获取到数据');
      process.exit(1);
    }

    // 输出表格
    console.log('\n📊 Bilibili全站排行榜 (Top 50):');
    console.log('='.repeat(80));
    data.forEach((item) => {
      console.log(`${String(item.rank).padStart(2)}. ${item.title}`);
      if (item.up) console.log(`   👤 UP主: ${item.up}`);
      if (item.play) console.log(`   📺 ${item.play}`);
      if (item.danmu) console.log(`   💬 ${item.danmu}`);
      if (item.like) console.log(`   👍 ${item.like}`);
      if (item.coin) console.log(`   🪙 ${item.coin}`);
      if (item.favorite) console.log(`   ⭐ ${item.favorite}`);
      if (item.score > 0) console.log(`   🔥 综合得分: ${item.score}`);
      console.log('');
    });

    // 保存 JSON
    const outputPath = path.join(OUTPUT_DIR, 'bilibili-hot.json');
    fs.mkdirSync(OUTPUT_DIR, { recursive: true });
    fs.writeFileSync(outputPath, JSON.stringify(data, null, 2));
    console.log(`\n✅ 已保存到 ${outputPath}`);

    // 保存简化的文本版本
    const textOutputPath = path.join(OUTPUT_DIR, 'bilibili-hot.txt');
    let textContent = 'Bilibili全站排行榜 (Top 50)\n' + '='.repeat(50) + '\n\n';
    data.forEach((item) => {
      textContent += `${item.rank}. ${item.title}\n`;
      if (item.up) textContent += `   UP主: ${item.up}\n`;
      if (item.play) textContent += `   播放: ${item.play}\n`;
      textContent += '\n';
    });
    fs.writeFileSync(textOutputPath, textContent);
    console.log(`📝 已保存文本版本到 ${textOutputPath}`);

    return data;
  } catch (e) {
    console.error('❌ 主函数错误:', e.message);
    process.exit(1);
  }
}

// 如果直接运行，执行主函数
if (require.main === module) {
  main();
}

module.exports = { fetchBilibiliRank, formatNumber };