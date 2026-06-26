const { search } = require('../src/index');

async function searchJianshui() {
  console.log('🏨 建水古城酒店搜索（4月9日，1晚）');
  console.log('=====================================');
  console.log('');

  try {
    const result = await search({
      city: '建水古城',
      checkInDate: '2026-04-09',
      checkOutDate: '2026-04-10',
      priceRange: { min: 200, max: 400 },
      hotelType: 'homestay'
    });

    if (result.success && result.hotels.length > 0) {
      console.log('✅ 找到 ' + result.hotels.length + ' 家酒店');
      console.log('');

      // 显示前5家酒店
      result.hotels.slice(0, 5).forEach((hotel, index) => {
        console.log((index + 1) + '. ' + hotel.name);
        console.log('   价格: ' + hotel.price + ' | 评分: ' + hotel.rating);
        console.log('   位置: ' + hotel.location);
        console.log('');
      });

      // 显示推荐
      console.log('🎯 推荐选择:');
      result.report.topPicks.forEach((pick, index) => {
        console.log((index + 1) + '. ' + pick.name);
        console.log('   价格: ¥' + pick.price + ' | 评分: ' + pick.rating);
        console.log('   理由: ' + pick.reason);
        console.log('');
      });
    } else {
      console.log('❌ 暂时无法获取实时数据');
      console.log('建议：手动在携程搜索建水古城，筛选：');
      console.log('- 日期：4月9日（1晚）');
      console.log('- 房型：双床');
      console.log('- 筛选：3钻及以上、4.5分以上、特色民宿');
    }
  } catch (error) {
    console.log('❌ 搜索失败: ' + error.message);
    console.log('建议：手动在携程搜索建水古城酒店');
  }
}

// 运行搜索
searchJianshui();