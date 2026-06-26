const { loginCtrip, checkLoginStatus, logout } = require('./login');
const { searchHotels, searchHomestays } = require('./search');
const { getHotelDetails, getHotelReviews, compareHotels } = require('./details');
const { validateConfig, formatDate } = require('./utils');
const config = require('../config.json');

/**
 * 主函数 - 携程酒店搜索
 * @param {object} searchParams - 搜索参数
 * @returns {Promise<object>} 搜索结果
 */
async function ctripHotelSearch(searchParams) {
  console.log('🏨 携程酒店搜索 Skill 启动');
  console.log('=====================================');

  // 验证配置
  if (!validateConfig(config)) {
    throw new Error('配置验证失败');
  }

  let browser = null;
  let page = null;
  let context = null;

  try {
    // 1. 登录携程
    console.log('\n1️⃣ 登录携程账号...');
    const loginResult = await loginCtrip(
      config.ctrip.username,
      config.ctrip.password,
      config.browser
    );
    browser = loginResult.browser;
    page = loginResult.page;
    context = loginResult.context;

    // 2. 搜索酒店
    console.log('\n2️⃣ 搜索酒店...');
    const searchResult = await searchHotels(page, {
      city: searchParams.city,
      checkInDate: searchParams.checkInDate,
      checkOutDate: searchParams.checkOutDate,
      priceRange: searchParams.priceRange || config.search.defaultPriceRange,
      hotelType: searchParams.hotelType || 'all'
    });

    // 3. 如果需要，获取更多详情
    let detailedHotels = [];
    if (searchParams.getDetails && searchResult.length > 0) {
      console.log('\n3️⃣ 获取酒店详情...');
      detailedHotels = [];
      
      // 只获取前3家酒店的详情（避免过多请求）
      const hotelsToDetail = searchResult.slice(0, 3);
      
      for (const hotel of hotelsToDetail) {
        if (hotel.link) {
          const details = await getHotelDetails(page, hotel.link);
          if (details) {
            detailedHotels.push({
              ...hotel,
              ...details
            });
          }
          await new Promise(resolve => setTimeout(resolve, 1000)); // 避免请求过快
        }
      }
    } else {
      detailedHotels = searchResult;
    }

    // 4. 对比分析
    console.log('\n4️⃣ 对比分析...');
    const comparison = await compareHotels(detailedHotels);

    // 5. 生成报告
    console.log('\n5️⃣ 生成报告...');
    const report = generateReport(searchParams, comparison);

    console.log('\n=====================================');
    console.log('✅ 搜索完成！');
    console.log(`📊 找到 ${searchResult.length} 家酒店`);
    console.log(`🎯 推荐: ${comparison.recommendations.length} 个`);

    return {
      success: true,
      searchParams,
      hotels: searchResult,
      detailedHotels,
      comparison,
      report
    };

  } catch (error) {
    console.error('\n❌ 搜索失败:', error.message);
    return {
      success: false,
      error: error.message
    };
  } finally {
    // 关闭浏览器
    if (browser) {
      console.log('\n🔒 关闭浏览器...');
      await browser.close();
    }
  }
}

/**
 * 生成搜索报告
 * @param {object} searchParams - 搜索参数
 * @param {object} comparison - 对比结果
 * @returns {object} 报告
 */
function generateReport(searchParams, comparison) {
  const report = {
    summary: {
      city: searchParams.city,
      date: `${searchParams.checkInDate} 至 ${searchParams.checkOutDate}`,
      totalHotels: comparison.hotels.length,
      priceRange: `${searchParams.priceRange?.min || 200}-${searchParams.priceRange?.max || 400}元`
    },
    recommendations: comparison.recommendations,
    topPicks: []
  };

  // 选择3个最佳推荐
  if (comparison.recommendations.length > 0) {
    report.topPicks = comparison.recommendations.slice(0, 3).map(rec => ({
      name: rec.hotel.name,
      price: rec.hotel.price,
      rating: rec.hotel.rating,
      reason: rec.reason,
      type: rec.type
    }));
  }

  return report;
}

/**
 * 便捷搜索函数 - 适合直接调用
 * @param {object} params - 搜索参数
 */
async function search(params) {
  const defaultParams = {
    city: '建水古城',
    checkInDate: formatDate(new Date('2026-04-09')),
    checkOutDate: formatDate(new Date('2026-04-10')),
    priceRange: { min: 200, max: 400 },
    hotelType: 'all',
    getDetails: false
  };

  const searchParams = { ...defaultParams, ...params };
  return await ctripHotelSearch(searchParams);
}

// 如果直接运行此文件
if (require.main === module) {
  console.log('请通过 Skill 调用此功能，或使用 search() 函数');
  console.log('示例:');
  console.log('  const { search } = require("./src/index");');
  console.log('  search({ city: "建水古城", checkInDate: "2026-04-09" });');
}

module.exports = {
  ctripHotelSearch,
  search,
  loginCtrip,
  searchHotels,
  getHotelDetails,
  compareHotels
};