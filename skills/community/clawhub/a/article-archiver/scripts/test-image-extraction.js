const { chromium } = require('playwright');

const articleUrl = 'https://x.com/mkdir700/status/2020652753190887566';
const cookieString = require('fs').readFileSync('../config/twitter-cookies.txt', 'utf8');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();

  const cookies = cookieString.split('; ').map(cookie => {
    const [name, value] = cookie.split('=');
    return { name: name.trim(), value: value.trim(), domain: '.x.com', path: '/' };
  });
  await context.addCookies(cookies);

  const page = await context.newPage();
  await page.goto(articleUrl, { waitUntil: 'networkidle', timeout: 60000 });
  
  console.log('等待页面加载...');
  await page.waitForTimeout(5000);
  
  // 滚动到底部
  console.log('滚动页面...');
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let totalHeight = 0;
      const distance = 500;
      const timer = setInterval(() => {
        const scrollHeight = document.body.scrollHeight;
        window.scrollBy(0, distance);
        totalHeight += distance;
        if (totalHeight >= scrollHeight) {
          clearInterval(timer);
          resolve();
        }
      }, 200);
    });
  });
  
  await page.waitForTimeout(5000);
  
  // 尝试多种选择器
  const imageData = await page.evaluate(() => {
    const results = {
      method1_img_src: [],
      method2_background: [],
      method3_data_testid: [],
      method4_all_pbs: []
    };
    
    // 方法1：所有 img 标签
    document.querySelectorAll('img').forEach(img => {
      const src = img.src || img.getAttribute('src');
      if (src && src.includes('pbs.twimg.com/media')) {
        results.method1_img_src.push(src.split('?')[0]);
      }
    });
    
    // 方法2：background-image
    document.querySelectorAll('*').forEach(el => {
      const bg = window.getComputedStyle(el).backgroundImage;
      if (bg && bg.includes('pbs.twimg.com/media')) {
        const match = bg.match(/url\("?([^"]+)"?\)/);
        if (match) results.method2_background.push(match[1].split('?')[0]);
      }
    });
    
    // 方法3：data-testid
    document.querySelectorAll('[data-testid*="photo"], [data-testid*="image"]').forEach(el => {
      const img = el.querySelector('img');
      if (img) {
        const src = img.src || img.getAttribute('src');
        if (src && src.includes('pbs.twimg.com')) {
          results.method3_data_testid.push(src.split('?')[0]);
        }
      }
    });
    
    // 方法4：所有包含 pbs.twimg.com 的 URL
    document.querySelectorAll('img[src*="pbs.twimg.com"]').forEach(img => {
      const src = img.src;
      if (src) results.method4_all_pbs.push(src.split('?')[0]);
    });
    
    return results;
  });
  
  console.log(JSON.stringify(imageData, null, 2));
  
  await browser.close();
})();
