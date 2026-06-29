#!/usr/bin/env node
/**
 * 天气查询脚本 - 查询城市天气，辅助出行建议
 * 
 * 用法:
 *   node scripts/check-weather.js --city=杭州
 */

const { getWeather, parseArgs } = require('../index');

async function main() {
  const args = parseArgs();

  if (!args.city) {
    console.error('用法: node check-weather.js --city=<城市名称>');
    process.exit(1);
  }

  try {
    const weather = await getWeather(args.city);
    console.log(`\n🌤️  ${weather.province} ${weather.city} 当前天气:\n`);
    console.log(`   天气: ${weather.weather}`);
    console.log(`   温度: ${weather.temperature}°C`);
    console.log(`   风向: ${weather.winddirection}风 ${weather.windpower}级`);
    console.log(`   湿度: ${weather.humidity}%`);
    console.log(`   更新时间: ${weather.reporttime}`);

    // 出行建议
    const temp = parseInt(weather.temperature);
    if (temp > 35) console.log('\n   ⚠️  高温预警，建议携带防晒和充足饮水');
    if (temp < 5) console.log('\n   ⚠️  低温预警，注意保暖');
    if (weather.weather.includes('雨')) console.log('\n   🌧️  有雨，请携带雨具');

    console.log('\n--- JSON ---');
    console.log(JSON.stringify(weather, null, 2));

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
