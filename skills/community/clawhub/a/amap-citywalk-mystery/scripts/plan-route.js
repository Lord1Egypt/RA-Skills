#!/usr/bin/env node
/**
 * 路径规划脚本 - 规划故事地点间的路线
 * 
 * 用法:
 *   node scripts/plan-route.js --type=walking --origin=120.15507,30.27415 --destination=120.14873,30.24267
 *   node scripts/plan-route.js --type=driving --origin=116.397428,39.90923 --destination=116.427281,39.903719
 *   node scripts/plan-route.js --type=walking --origin=120.15507,30.27415 --destination=120.14873,30.24267 --waypoints=120.15000,30.26000
 *   node scripts/plan-route.js --type=transfer --origin=116.397428,39.90923 --destination=116.427281,39.903719 --city=北京
 */

const { planRoute, parseArgs } = require('../index');

async function main() {
  const args = parseArgs();

  if (!args.origin || !args.destination) {
    console.error('用法: node plan-route.js --type=<walking|driving|riding|transfer> --origin=<经度,纬度> --destination=<经度,纬度> [--waypoints=<经度,纬度>] [--city=<城市>]');
    process.exit(1);
  }

  try {
    const result = await planRoute({
      type: args.type || 'walking',
      origin: args.origin,
      destination: args.destination,
      waypoints: args.waypoints || '',
      city: args.city || ''
    });

    const typeNames = {
      walking: '🚶 步行',
      driving: '🚗 驾车',
      riding: '🚲 骑行',
      transfer: '🚌 公交'
    };

    console.log(`\n${typeNames[result.type] || result.type} 路线规划：`);
    console.log(`起点: ${result.origin}`);
    console.log(`终点: ${result.destination}`);
    console.log(`距离: ${result.totalDistance}`);
    console.log(`预计时间: ${result.totalDuration}`);
    console.log('');

    if (result.steps && result.steps.length > 0) {
      console.log('详细路线:');
      result.steps.forEach((step, i) => {
        console.log(`  ${i + 1}. ${step.instruction}`);
      });
    }

    // 输出 JSON 格式
    console.log('\n--- JSON ---');
    console.log(JSON.stringify(result, null, 2));

  } catch (err) {
    console.error('❌ 错误:', err.message);
    process.exit(1);
  }
}

main();
