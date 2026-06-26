const { delay, formatDate, parsePrice, parseRating } = require('./utils');

/**
 * 搜索酒店
 * @param {object} page - Playwright 页面对象
 * @param {object} searchParams - 搜索参数
 * @returns {Promise<Array>} 酒店列表
 */
async function searchHotels(page, searchParams) {
  const {
    city,
    checkInDate,
    checkOutDate,
    priceRange = { min: 200, max: 400 },
    hotelType = 'all' // 'all', 'hotel', 'homestay'
  } = searchParams;

  console.log(`🔍 开始搜索: ${city} ${checkInDate} - ${checkOutDate}`);

  try {
    // 打开携程酒店搜索页
    await page.goto('https://hotels.ctrip.com', { waitUntil: 'networkidle' });
    await delay(2000);

    // 输入城市
    console.log('📍 输入城市:', city);
    await page.click('#cityName', { clickCount: 3 }); // 全选
    await page.keyboard.press('Backspace');
    await page.fill('#cityName', city);
    await delay(1000);

    // 选择城市（等待下拉列表出现并选择第一个）
    await page.waitForSelector('.city-list', { timeout: 5000 }).catch(() => {});
    await page.keyboard.press('Enter');
    await delay(500);

    // 设置入住日期
    console.log('📅 设置入住日期:', checkInDate);
    await page.click('#checkInDate');
    await delay(500);
    await page.fill('#checkInDate', checkInDate);
    await delay(500);

    // 设置退房日期
    console.log('📅 设置退房日期:', checkOutDate);
    await page.click('#checkOutDate');
    await delay(500);
    await page.fill('#checkOutDate', checkOutDate);
    await delay(500);

    // 设置价格范围
    console.log(`💰 设置价格范围: ${priceRange.min} - ${priceRange.max}元`);
    await page.click('.price-filter');
    await delay(500);
    
    // 选择价格区间（根据页面结构调整）
    const priceOption = await page.$(`.price-option:has-text("${priceRange.min}-${priceRange.max}")`);
    if (priceOption) {
      await priceOption.click();
    } else {
      // 如果没有精确匹配，尝试选择相近区间
      await page.click('.price-option:first-child');
    }
    await delay(500);

    // 点击搜索按钮
    console.log('🖱️ 点击搜索...');
    await page.click('#searchBtn');
    
    // 等待搜索结果加载
    console.log('⏳ 等待搜索结果...');
    await page.waitForSelector('.hotel-list, .hotel-item', { timeout: 15000 });
    await delay(2000);

    // 提取酒店信息
    console.log('📊 提取酒店数据...');
    const hotels = await extractHotelList(page);
    
    console.log(`✅ 找到 ${hotels.length} 家酒店`);
    return hotels;

  } catch (error) {
    console.error('❌ 搜索失败:', error.message);
    throw error;
  }
}

/**
 * 提取酒店列表
 * @param {object} page - Playwright 页面对象
 * @returns {Promise<Array>} 酒店列表
 */
async function extractHotelList(page) {
  return await page.evaluate(() => {
    const hotels = [];
    
    // 尝试多种选择器（携程页面结构可能变化）
    const selectors = [
      '.hotel-item',
      '.hotel-list .item',
      '[data-testid="hotel-item"]',
      '.search-result-list .hotel-item'
    ];

    let hotelElements = [];
    for (const selector of selectors) {
      hotelElements = document.querySelectorAll(selector);
      if (hotelElements.length > 0) break;
    }

    hotelElements.forEach((el, index) => {
      try {
        const name = el.querySelector('.hotel-name, .name, .title')?.textContent?.trim() || '';
        const price = el.querySelector('.price, .price-num, .price-tag')?.textContent?.trim() || '';
        const rating = el.querySelector('.rating, .score, .grade')?.textContent?.trim() || '';
        const location = el.querySelector('.location, .address')?.textContent?.trim() || '';
        const link = el.querySelector('a')?.href || '';

        if (name) {
          hotels.push({
            id: index + 1,
            name: name,
            price: price,
            priceValue: parseInt(price.replace(/[^\d]/g, '')) || 0,
            rating: rating,
            ratingValue: parseFloat(rating.replace(/[^\d.]/g, '')) || 0,
            location: location,
            link: link,
            source: 'ctrip'
          });
        }
      } catch (e) {
        // 跳过无法解析的元素
      }
    });

    return hotels;
  });
}

/**
 * 搜索特定类型的住宿（民宿/客栈）
 * @param {object} page - Playwright 页面对象
 * @param {object} searchParams - 搜索参数
 * @returns {Promise<Array>} 酒店列表
 */
async function searchHomestays(page, searchParams) {
  console.log('🏠 搜索民宿/客栈...');
  
  // 先进行普通搜索
  const hotels = await searchHotels(page, searchParams);
  
  // 筛选包含"民宿"、"客栈"、"精品"等关键词的酒店
  const homestays = hotels.filter(hotel => {
    const name = hotel.name.toLowerCase();
    return name.includes('民宿') || 
           name.includes('客栈') || 
           name.includes('精品') || 
           name.includes('设计') ||
           name.includes('庭院');
  });
  
  console.log(`✅ 找到 ${homestays.length} 家民宿/客栈`);
  return homestays;
}

module.exports = {
  searchHotels,
  searchHomestays,
  extractHotelList
};