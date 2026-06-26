const { search } = require('../src/index');

/**
 * 测试携程酒店搜索功能
 */
async function testSearch() {
  console.log('🧪 开始测试携程酒店搜索功能');
  console.log('=====================================');

  try {
    // 测试1：搜索建水古城酒店
    console.log('\n📝 测试1: 搜索建水古城酒店');
    const result1 = await search({
      city: '建水古城',
      checkInDate: '2026-04-09',
      checkOutDate: '2026-04-10',
      priceRange: { min: 200, max: 400 }
    });

    if (result1.success) {
      console.log(`✅ 找到 ${result1.hotels.length} 家酒店`);
      console.log('前3家酒店:');
      result1.hotels.slice(0, 3).forEach((hotel, index) => {
        console.log(`  ${index + 1}. ${hotel.name} - ${hotel.price} - ${hotel.rating}`);
      });
    } else {
      console.log('❌ 搜索失败:', result1.error);
    }

    // 测试2：搜索南沙镇酒店
    console.log('\n📝 测试2: 搜索南沙镇酒店');
    const result2 = await search({
      city: '南沙镇',
      checkInDate: '2026-04-12',
      checkOutDate: '2026-04-13',
      priceRange: { min: 150, max: 300 }
    });

    if (result2.success) {
      console.log(`✅ 找到 ${result2.hotels.length} 家酒店`);
      console.log('前3家酒店:');
      result2.hotels.slice(0, 3).forEach((hotel, index) => {
        console.log(`  ${index + 1}. ${hotel.name} - ${hotel.price} - ${hotel.rating}`);
      });
    } else {
      console.log('❌ 搜索失败:', result2.error);
    }

    console.log('\n=====================================');
    console.log('✅ 测试完成！');

  } catch (error) {
    console.error('\n❌ 测试失败:', error.message);
    console.error(error.stack);
  }
}

// 运行测试
if (require.main === module) {
  testSearch();
}

module.exports = { testSearch };