#!/usr/bin/env node
/**
 * POI 搜索脚本 - 搜索故事场景地点
 * 
 * 用法:
 *   node scripts/search-locations.js --keywords=咖啡馆 --city=杭州
 *   node scripts/search-locations.js --keywords=书店 --city=北京 --types=140600
 *   node scripts/search-locations.js --keywords=公园 --city=上海 --location=121.473701,31.230416 --radius=2000
 */

const { searchPOI, parseArgs } = require('../index');

async function main() {
  const args = parseArgs();

  if (!args.keywords) {
    console.error('用法: node search-locations.js --keywords=<关键词> --city=<城市> [--types=<类型>] [--location=<坐标>] [--radius=<半径>]');
    process.exit(1);
  }

  try {
    const result = await searchPOI({
      keywords: args.keywords,
      city: args.city || '',
      types: args.types || '',
      location: args.location || '',
      radius: parseInt(args.radius) || 3000,
      offset: parseInt(args.offset) || 10
    });

    console.log(`\n🔍 搜索 "${args.keywords}" 在 ${args.city || '全国'}，共找到 ${result.count} 个结果：\n`);

    result.pois.forEach((poi, i) => {
      console.log(`${i + 1}. ${poi.name}`);
      console.log(`   📍 地址: ${poi.address}`);
      console.log(`   📌 坐标: ${poi.location}`);
      console.log(`   📂 类型: ${poi.type}`);
      if (poi.rating) console.log(`   ⭐ 评分: ${poi.rating}`);
      if (poi.cost) console.log(`   💰 人均: ${poi.cost}元`);
      if (poi.tel) console.log(`   📞 电话: ${poi.tel}`);
      console.log('');
    });

    // 输出 JSON 格式（方便 AI 解析）
    console.log('--- JSON ---');
    console.log(JSON.stringify(result, null, 2));

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
