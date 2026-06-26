/**
 * 演示脚本 - 展示携程酒店搜索 Skill 的功能
 * 注意：此脚本仅演示数据结构，实际使用需要完整安装 Playwright
 */

const demoData = {
  searchParams: {
    city: '建水古城',
    checkInDate: '2026-04-09',
    checkOutDate: '2026-04-10',
    priceRange: { min: 200, max: 400 }
  },
  
  hotels: [
    {
      id: 1,
      name: '建水古城听紫云度假酒店',
      price: '¥358',
      priceValue: 358,
      rating: '4.8分',
      ratingValue: 4.8,
      location: '距离朝阳楼500米',
      link: 'https://hotels.ctrip.com/hotel/123456.html'
    },
    {
      id: 2,
      name: '建水古城里精品民宿',
      price: '¥288',
      priceValue: 288,
      rating: '4.6分',
      ratingValue: 4.6,
      location: '距离朱家花园300米',
      link: 'https://hotels.ctrip.com/hotel/234567.html'
    },
    {
      id: 3,
      name: '建水古城庭院客栈',
      price: '¥228',
      priceValue: 228,
      rating: '4.5分',
      ratingValue: 4.5,
      location: '古城中心位置',
      link: 'https://hotels.ctrip.com/hotel/345678.html'
    }
  ],
  
  comparison: {
    summary: {
      totalPrice: 874,
      avgPrice: 291,
      bestValue: {
        name: '建水古城庭院客栈',
        price: '¥228',
        rating: '4.5分',
        valueRatio: 0.0197
      },
      highestRated: {
        name: '建水古城听紫云度假酒店',
        price: '¥358',
        rating: '4.8分'
      }
    },
    recommendations: [
      {
        type: 'budget',
        title: '最经济选择',
        hotel: {
          name: '建水古城庭院客栈',
          price: '¥228',
          rating: '4.5分'
        },
        reason: '价格最低: ¥228'
      },
      {
        type: 'quality',
        title: '评分最高',
        hotel: {
          name: '建水古城听紫云度假酒店',
          price: '¥358',
          rating: '4.8分'
        },
        reason: '评分: 4.8分'
      },
      {
        type: 'value',
        title: '性价比最高',
        hotel: {
          name: '建水古城庭院客栈',
          price: '¥228',
          rating: '4.5分'
        },
        reason: '评分/价格比最优'
      }
    ]
  },
  
  report: {
    summary: {
      city: '建水古城',
      date: '2026-04-09 至 2026-04-10',
      totalHotels: 3,
      priceRange: '200-400元'
    },
    topPicks: [
      {
        name: '建水古城庭院客栈',
        price: '¥228',
        rating: '4.5分',
        reason: '价格最低: ¥228',
        type: 'budget'
      },
      {
        name: '建水古城听紫云度假酒店',
        price: '¥358',
        rating: '4.8分',
        reason: '评分: 4.8分',
        type: 'quality'
      },
      {
        name: '建水古城庭院客栈',
        price: '¥228',
        rating: '4.5分',
        reason: '评分/价格比最优',
        type: 'value'
      }
    ]
  }
};

console.log('🏨 携程酒店搜索 Skill - 演示数据');
console.log('=====================================\n');

console.log('📍 搜索条件:');
console.log(`  城市: ${demoData.searchParams.city}`);
console.log(`  日期: ${demoData.searchParams.checkInDate} 至 ${demoData.searchParams.checkOutDate}`);
console.log(`  价格: ${demoData.searchParams.priceRange.min}-${demoData.searchParams.priceRange.max}元\n`);

console.log('🏨 搜索结果:');
demoData.hotels.forEach((hotel, index) => {
  console.log(`  ${index + 1}. ${hotel.name}`);
  console.log(`     价格: ${hotel.price} | 评分: ${hotel.rating}`);
  console.log(`     位置: ${hotel.location}\n`);
});

console.log('📊 对比分析:');
console.log(`  总价: ¥${demoData.comparison.summary.totalPrice}`);
console.log(`  平均价: ¥${demoData.comparison.summary.avgPrice}`);
console.log(`  性价比最高: ${demoData.comparison.summary.bestValue.name}`);
console.log(`  评分最高: ${demoData.comparison.summary.highestRated.name}\n`);

console.log('🎯 推荐选择:');
demoData.comparison.recommendations.forEach((rec, index) => {
  console.log(`  ${index + 1}. ${rec.title}`);
  console.log(`     酒店: ${rec.hotel.name}`);
  console.log(`     价格: ${rec.hotel.price} | 评分: ${rec.hotel.rating}`);
  console.log(`     理由: ${rec.reason}\n`);
});

console.log('=====================================');
console.log('💡 使用说明:');
console.log('1. 编辑 config.json 填入携程账号密码');
console.log('2. 运行: node tests/test-search.js');
console.log('3. 或在代码中调用: const { search } = require("./src/index")');
console.log('4. 根据推荐选择酒店，在携程官网完成预订');