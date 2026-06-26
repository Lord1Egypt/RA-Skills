const { delay } = require('./utils');

/**
 * 获取酒店详情
 * @param {object} page - Playwright 页面对象
 * @param {string} hotelUrl - 酒店详情页URL
 * @returns {Promise<object>} 酒店详情
 */
async function getHotelDetails(page, hotelUrl) {
  console.log(`📖 获取酒店详情: ${hotelUrl}`);
  
  try {
    await page.goto(hotelUrl, { waitUntil: 'networkidle' });
    await delay(2000);

    const details = await page.evaluate(() => {
      const info = {
        name: '',
        address: '',
        facilities: [],
        reviews: [],
        priceHistory: '',
        images: [],
        description: ''
      };

      // 酒店名称
      const nameEl = document.querySelector('h1, .hotel-name, .title');
      if (nameEl) info.name = nameEl.textContent.trim();

      // 地址
      const addressEl = document.querySelector('.address, .location, .hotel-address');
      if (addressEl) info.address = addressEl.textContent.trim();

      // 设施
      const facilityEls = document.querySelectorAll('.facility, .amenity, .service');
      info.facilities = Array.from(facilityEls).map(el => el.textContent.trim());

      // 评价（前5条）
      const reviewEls = document.querySelectorAll('.review-item, .comment-item');
      info.reviews = Array.from(reviewEls.slice(0, 5)).map(el => ({
        author: el.querySelector('.author, .user-name')?.textContent.trim() || '',
        content: el.querySelector('.content, .comment-text')?.textContent.trim() || '',
        rating: el.querySelector('.rating, .score')?.textContent.trim() || '',
        date: el.querySelector('.date, .time')?.textContent.trim() || ''
      }));

      // 图片
      const imageEls = document.querySelectorAll('.hotel-image, .photo-item img');
      info.images = Array.from(imageEls).map(el => el.src || el.dataset.src).filter(Boolean);

      // 描述
      const descEl = document.querySelector('.description, .hotel-desc');
      if (descEl) info.description = descEl.textContent.trim();

      return info;
    });

    console.log(`✅ 获取到详情: ${details.name}`);
    return details;

  } catch (error) {
    console.error('❌ 获取详情失败:', error.message);
    return null;
  }
}

/**
 * 获取酒店评价
 * @param {object} page - Playwright 页面对象
 * @param {string} hotelUrl - 酒店详情页URL
 * @returns {Promise<Array>} 评价列表
 */
async function getHotelReviews(page, hotelUrl) {
  console.log(`💬 获取酒店评价: ${hotelUrl}`);
  
  try {
    // 如果不在详情页，先跳转
    if (!page.url().includes(hotelUrl)) {
      await page.goto(hotelUrl, { waitUntil: 'networkidle' });
      await delay(2000);
    }

    // 点击评价标签（如果存在）
    const reviewTab = await page.$('.review-tab, .comment-tab, [data-tab="review"]');
    if (reviewTab) {
      await reviewTab.click();
      await delay(1000);
    }

    const reviews = await page.evaluate(() => {
      const reviewElements = document.querySelectorAll('.review-item, .comment-item, .comment-list li');
      
      return Array.from(reviewElements).map((el, index) => {
        try {
          return {
            id: index + 1,
            author: el.querySelector('.author, .user-name, .nick-name')?.textContent.trim() || '',
            content: el.querySelector('.content, .comment-text, .review-content')?.textContent.trim() || '',
            rating: el.querySelector('.rating, .score, .grade')?.textContent.trim() || '',
            date: el.querySelector('.date, .time, .review-date')?.textContent.trim() || '',
            helpful: el.querySelector('.helpful, .useful')?.textContent.trim() || '0'
          };
        } catch (e) {
          return null;
        }
      }).filter(Boolean);
    });

    console.log(`✅ 获取到 ${reviews.length} 条评价`);
    return reviews;

  } catch (error) {
    console.error('❌ 获取评价失败:', error.message);
    return [];
  }
}

/**
 * 对比多家酒店
 * @param {Array} hotels - 酒店列表
 * @returns {Promise<object>} 对比结果
 */
async function compareHotels(hotels) {
  console.log(`📊 开始对比 ${hotels.length} 家酒店...`);
  
  const comparison = {
    hotels: hotels,
    summary: {
      totalPrice: hotels.reduce((sum, h) => sum + (h.priceValue || 0), 0),
      avgPrice: 0,
      bestValue: null,
      bestLocation: null,
      highestRated: null
    },
    recommendations: []
  };

  // 计算平均价格
  if (hotels.length > 0) {
    comparison.summary.avgPrice = Math.round(comparison.summary.totalPrice / hotels.length);
  }

  // 找出最佳选择
  if (hotels.length > 0) {
    // 性价比最高（评分/价格比）
    const valueHotels = hotels
      .filter(h => h.priceValue > 0 && h.ratingValue > 0)
      .map(h => ({
        ...h,
        valueRatio: h.ratingValue / h.priceValue
      }))
      .sort((a, b) => b.valueRatio - a.valueRatio);
    
    if (valueHotels.length > 0) {
      comparison.summary.bestValue = valueHotels[0];
    }

    // 评分最高
    const ratedHotels = [...hotels].sort((a, b) => b.ratingValue - a.ratingValue);
    if (ratedHotels.length > 0) {
      comparison.summary.highestRated = ratedHotels[0];
    }

    // 生成推荐
    comparison.recommendations = generateRecommendations(hotels);
  }

  console.log('✅ 对比完成');
  return comparison;
}

/**
 * 生成酒店推荐
 * @param {Array} hotels - 酒店列表
 * @returns {Array} 推荐列表
 */
function generateRecommendations(hotels) {
  const recommendations = [];

  // 按价格排序
  const byPrice = [...hotels].sort((a, b) => a.priceValue - b.priceValue);
  if (byPrice.length > 0) {
    recommendations.push({
      type: 'budget',
      title: '最经济选择',
      hotel: byPrice[0],
      reason: `价格最低: ${byPrice[0].price}`
    });
  }

  // 按评分排序
  const byRating = [...hotels].sort((a, b) => b.ratingValue - a.ratingValue);
  if (byRating.length > 0) {
    recommendations.push({
      type: 'quality',
      title: '评分最高',
      hotel: byRating[0],
      reason: `评分: ${byRating[0].rating}`
    });
  }

  // 性价比最高
  const withValue = hotels
    .filter(h => h.priceValue > 0 && h.ratingValue > 0)
    .map(h => ({
      ...h,
      valueRatio: h.ratingValue / h.priceValue
    }))
    .sort((a, b) => b.valueRatio - a.valueRatio);
  
  if (withValue.length > 0) {
    recommendations.push({
      type: 'value',
      title: '性价比最高',
      hotel: withValue[0],
      reason: `评分/价格比最优`
    });
  }

  return recommendations;
}

module.exports = {
  getHotelDetails,
  getHotelReviews,
  compareHotels
};