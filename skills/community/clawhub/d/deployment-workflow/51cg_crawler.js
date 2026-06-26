/**
 * 51吃瓜爬取测试
 * 用途：从51cg网站解密提取图片
 * 使用方法：node 51cg_crawler.js <article_id>
 * 示例：node 51cg_crawler.js 174106
 */

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const BASE_URL = 'https://51cg1.com/archives/';
const OUTPUT_DIR = path.join(__dirname, 'downloads');

async function crawl51cg(articleId) {
  const url = `${BASE_URL}${articleId}/`;
  const outputPath = path.join(OUTPUT_DIR, `51cg_${articleId}`);
  
  // 创建输出目录
  if (!fs.existsSync(outputPath)) {
    fs.mkdirSync(outputPath, { recursive: true });
  }
  
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  console.log(`正在访问: ${url}`);
  await page.goto(url);
  await page.waitForTimeout(3000);
  
  // 提取页面中已解密的图片（data:image/jpeg;base64格式）
  const images = await page.evaluate(() => {
    const imgs = document.querySelectorAll('img');
    const results = [];
    // 从第40张开始是实际图片（前面是广告等）
    for (let i = 40; i < imgs.length; i++) {
      const img = imgs[i];
      if (img.src && img.src.startsWith('data:image/jpeg;base64,')) {
        results.push({
          index: i,
          src: img.src
        });
      }
    }
    return results;
  });
  
  console.log(`找到 ${images.length} 张图片`);
  
  // 保存图片
  images.forEach((img, idx) => {
    const base64Data = img.src.replace('data:image/jpeg;base64,', '');
    const buffer = Buffer.from(base64Data, 'base64');
    const filename = `img_${idx + 1}.jpg`;
    fs.writeFileSync(path.join(outputPath, filename), buffer);
    console.log(`保存: ${filename}`);
  });
  
  await browser.close();
  console.log(`完成！图片保存在: ${outputPath}`);
}

// 主入口
const articleId = process.argv[2] || '174106';
crawl51cg(articleId).catch(console.error);
