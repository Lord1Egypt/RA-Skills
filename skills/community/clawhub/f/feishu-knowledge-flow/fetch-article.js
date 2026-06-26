const { chromium } = require('playwright');

const url = process.argv[2];
if (!url) {
  console.error('Usage: node fetch-article.js <url>');
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781(0x6700143B) NetType/WIFI MiniProgramEnv/Windows WindowsWechat/3.9.10.19 XWEB/11275',
    viewport: { width: 1280, height: 900 },
  });
  const page = await context.newPage();

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(2000);

    const data = await page.evaluate(() => {
      const title = document.querySelector('#activity-name')?.innerText?.trim()
        || document.querySelector('.rich_media_title')?.innerText?.trim()
        || document.title || '';

      const author = document.querySelector('#js_name')?.innerText?.trim()
        || document.querySelector('.rich_media_meta_nickname')?.innerText?.trim()
        || '';

      const date = document.querySelector('#publish_time')?.innerText?.trim()
        || document.querySelector('.rich_media_meta_date')?.innerText?.trim()
        || '';

      const content = document.querySelector('#js_content')?.innerText?.trim()
        || document.querySelector('.rich_media_content')?.innerText?.trim()
        || document.body.innerText?.trim() || '';

      return { title, author, date, content };
    });

    const output = JSON.stringify(data, null, 2);
    process.stdout.write(output);
  } catch (e) {
    console.error('Error:', e.message);
    process.exit(1);
  } finally {
    await browser.close();
  }
})();
