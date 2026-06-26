#!/usr/bin/env node
/**
 * 高德地图路线规划脚本 - 演示版本
 * 
 * 注意：这是演示版本，使用模拟数据
 * 实际使用需要申请高德地图 Web服务 API Key
 * 申请地址：https://lbs.amap.com
 */

// 模拟路线数据
const MOCK_ROUTES = {
  '上海虹桥_上海外滩': {
    driving: {
      distance: 22000,  // 米
      duration: 2400,   // 秒
      tolls: 0,
      traffic_lights: 8,
      route: '虹桥路-延安路高架-南京路-中山东一路',
      steps: [
        '从虹桥火车站出发，沿申虹路行驶500米',
        '右转进入虹桥路，行驶3.2公里',
        '上延安路高架，行驶12公里',
        '下高架进入南京路，行驶5公里',
        '左转进入中山东一路，行驶800米',
        '到达终点上海外滩'
      ]
    },
    transit: {
      duration: 3000,
      price: 6,
      transfers: 1,
      route: '地铁2号线 → 地铁10号线',
      steps: [
        '从虹桥火车站步行至虹桥2号航站楼站',
        '乘坐地铁2号线（浦东国际机场方向），17站',
        '在南京东路站下车，站内换乘',
        '乘坐地铁10号线（新江湾城方向），1站',
        '在豫园站下车，步行500米至外滩'
      ]
    },
    walking: {
      distance: 23000,
      duration: 16200  // 约4.5小时
    },
    taxi: {
      distance: 22000,
      duration: 2400,
      price_range: {
        min: 55,
        max: 65,
        premium_min: 75,
        premium_max: 90
      }
    }
  }
};

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const params = {
    from: null,
    to: null,
    mode: 'driving',  // driving | transit | walking | all
    compareAll: false
  };

  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--from') params.from = args[++i];
    else if (args[i] === '--to') params.to = args[++i];
    else if (args[i] === '--mode') params.mode = args[++i];
    else if (args[i] === '--compare-all') params.compareAll = true;
  }

  if (!params.from || !params.to) {
    console.error('❌ 错误：必须指定 --from 和 --to');
    process.exit(1);
  }

  return params;
}

/**
 * 获取路线数据
 */
function getRoute(from, to, mode) {
  const key = `${from}_${to}`;
  const data = MOCK_ROUTES[key];
  
  if (!data) {
    return null;
  }
  
  return data[mode];
}

/**
 * 格式化时间
 */
function formatDuration(seconds) {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  
  if (hours > 0) {
    return `${hours}小时${minutes}分钟`;
  }
  return `${minutes}分钟`;
}

/**
 * 格式化距离
 */
function formatDistance(meters) {
  if (meters < 1000) {
    return `${meters}米`;
  }
  return `${(meters / 1000).toFixed(1)}公里`;
}

/**
 * 打印驾车路线
 */
function printDriving(route, from, to) {
  console.log('\n【驾车】🚗');
  console.log(`├─ 距离：${formatDistance(route.distance)}`);
  console.log(`├─ 时间：${formatDuration(route.duration)}（路况良好）`);
  console.log(`├─ 路况：🟢 畅通`);
  console.log(`├─ 红绿灯：${route.traffic_lights}个`);
  console.log(`├─ 过路费：¥${route.tolls}`);
  
  // 计算油费（按0.7元/公里估算）
  const fuelCost = Math.round(route.distance / 1000 * 0.7);
  console.log(`├─ 油费：约¥${fuelCost}`);
  console.log(`└─ 路线：${route.route}`);
  
  console.log('\n   详细路线：');
  route.steps.forEach((step, i) => {
    console.log(`   ${i + 1}. ${step}`);
  });
}

/**
 * 打印公交路线
 */
function printTransit(route) {
  console.log('\n【公交/地铁】🚇');
  console.log(`├─ 时间：${formatDuration(route.duration)}`);
  console.log(`├─ 费用：¥${route.price}`);
  console.log(`├─ 换乘：${route.transfers}次`);
  console.log(`└─ 路线：${route.route}`);
  
  console.log('\n   详细路线：');
  route.steps.forEach((step, i) => {
    console.log(`   ${i + 1}. ${step}`);
  });
}

/**
 * 打印步行路线
 */
function printWalking(route) {
  console.log('\n【步行】🚶');
  console.log(`├─ 距离：${formatDistance(route.distance)}`);
  console.log(`├─ 时间：${formatDuration(route.duration)}`);
  console.log(`└─ 建议：距离较远，不建议步行`);
}

/**
 * 打印打车估价
 */
function printTaxi(route) {
  console.log('\n【打车】🚕');
  console.log(`├─ 距离：${formatDistance(route.distance)}`);
  console.log(`├─ 时间：${formatDuration(route.duration)}（当前路况）`);
  console.log(`├─ 价格区间：`);
  console.log(`│  ├─ 快车：¥${route.price_range.min}-${route.price_range.max}`);
  console.log(`│  └─ 优享：¥${route.price_range.premium_min}-${route.price_range.premium_max}`);
  console.log(`└─ 建议：适合赶时间或携带行李`);
}

/**
 * 智能建议
 */
function printRecommendation(routes) {
  console.log('\n💡 出行建议：');
  
  const drivingTime = routes.driving.duration;
  const transitTime = routes.transit.duration;
  
  if (transitTime < drivingTime * 1.2) {
    console.log('- 推荐公交/地铁：时间相近，无需担心停车和拥堵');
    console.log(`- 可节省：油费约¥${Math.round(routes.driving.distance / 1000 * 0.7)} + 停车费`);
  } else {
    console.log('- 推荐驾车：更快更便捷');
  }
  
  console.log('- 如携带大件行李，建议打车');
  console.log('- 高峰时段（7:30-9:30, 17:30-19:30）建议选择地铁');
}

/**
 * 主函数
 */
function main() {
  const params = parseArgs();
  
  console.log(`\n🗺️  ${params.from} → ${params.to}\n`);
  
  const routes = {
    driving: getRoute(params.from, params.to, 'driving'),
    transit: getRoute(params.from, params.to, 'transit'),
    walking: getRoute(params.from, params.to, 'walking'),
    taxi: getRoute(params.from, params.to, 'taxi')
  };
  
  if (!routes.driving) {
    console.log('❌ 未找到该路线的数据（演示版本仅支持：上海虹桥→上海外滩）');
    console.log('💡 实际使用请申请高德地图 API Key\n');
    console.log('申请地址：https://lbs.amap.com\n');
    return;
  }
  
  if (params.compareAll) {
    // 对比所有方案
    printDriving(routes.driving, params.from, params.to);
    printTransit(routes.transit);
    printTaxi(routes.taxi);
    printWalking(routes.walking);
    printRecommendation(routes);
  } else {
    // 仅显示指定方式
    switch (params.mode) {
      case 'driving':
        printDriving(routes.driving, params.from, params.to);
        break;
      case 'transit':
        printTransit(routes.transit);
        break;
      case 'walking':
        printWalking(routes.walking);
        break;
      case 'taxi':
        printTaxi(routes.taxi);
        break;
    }
  }
  
  console.log('\n📝 注意：这是演示版本，实际数据请使用高德地图APP');
  console.log('🔗 高德地图：https://www.amap.com\n');
}

main();
