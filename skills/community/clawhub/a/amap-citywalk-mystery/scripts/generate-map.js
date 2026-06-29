#!/usr/bin/env node
/**
 * 地图可视化生成脚本 - 生成 CityWalk 剧本杀的地图链接
 * 
 * 用法:
 *   node scripts/generate-map.js --data=<JSON文件路径>
 *   node scripts/generate-map.js --inline=<JSON字符串>
 * 
 * JSON 数据格式:
 * [
 *   { "type": "poi", "name": "断桥", "location": "120.14873,30.25954", "clue": "第一章", "chapter": 1 },
 *   { "type": "poi", "name": "岳庙", "location": "120.14433,30.25700", "clue": "第二章", "chapter": 2 },
 *   { "type": "route", "origin": "120.14873,30.25954", "destination": "120.14433,30.25700", "routeType": "walking" }
 * ]
 */

const { generateMapLink, generateCityWalkMapData, parseArgs } = require('../index');
const fs = require('fs');

function main() {
  const args = parseArgs();

  if (!args.data && !args.inline) {
    console.error('用法: node generate-map.js --data=<JSON文件路径>');
    console.error('  或: node generate-map.js --inline=<JSON字符串>');
    process.exit(1);
  }

  try {
    let rawData;

    if (args.data) {
      rawData = JSON.parse(fs.readFileSync(args.data, 'utf-8'));
    } else {
      rawData = JSON.parse(args.inline);
    }

    // 分离 POI 和路线
    const pois = rawData.filter(item => item.type === 'poi');
    const routes = rawData.filter(item => item.type === 'route');

    // 转换 POI 格式
    const storyLocations = pois.map(poi => ({
      name: poi.name,
      location: poi.location,
      clue: poi.clue || '',
      chapter: poi.chapter ? `第${poi.chapter}站` : '',
      description: poi.description || ''
    }));

    // 转换路线格式
    const routeData = routes.map(route => ({
      type: route.routeType || 'walking',
      origin: route.origin,
      destination: route.destination
    }));

    const mapData = generateCityWalkMapData(storyLocations, routeData);
    const mapLink = generateMapLink(mapData);

    console.log('\n🗺️  CityWalk 剧本杀地图已生成！\n');
    console.log(`📍 共 ${pois.length} 个故事站点`);
    console.log(`🛤️  共 ${routes.length} 段路线\n`);

    pois.forEach((poi, i) => {
      console.log(`  第${i + 1}站: ${poi.name} ${poi.clue ? '- ' + poi.clue : ''}`);
    });

    console.log(`\n🔗 地图链接:\n${mapLink}\n`);
    console.log('复制链接到浏览器即可查看地图路线。');

    // 输出 JSON
    console.log('\n--- JSON ---');
    console.log(JSON.stringify({ mapLink, mapData }, null, 2));

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
