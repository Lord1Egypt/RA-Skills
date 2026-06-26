// quick-control.js
// 直接连接已启动的 Chrome (端口 9222) 并执行操作
const puppeteer = require('puppeteer-core'); // 注意是 puppeteer-core (不下载浏览器)

async function run() {
    console.log('🦞 正在连接已打开的 Chrome...');
    
    // 连接到现有的 Chrome 实例
    const browser = await puppeteer.connect({
        browserURL: 'http://127.0.0.1:9222',
        defaultViewport: null
    });

    console.log('✅ 连接成功！获取当前标签页...');
    const pages = await browser.pages();
    const page = pages.length > 0 ? pages[0] : await browser.newPage();
    
    console.log('🌐 正在访问番茄作家后台...');
    await page.goto('https://fanqie.baidu.com/writer', { waitUntil: 'networkidle2', timeout: 30000 });
    
    console.log('📸 截图确认...');
    await page.screenshot({ path: 'fanqie_status.png', fullPage: true });
    
    const title = await page.title();
    console.log(`📄 当前页面标题：${title}`);
    console.log('🔗 当前 URL: ' + page.url());

    // 简单判断：如果包含"登录"或"登陆"，说明未登录
    const content = await page.content();
    if (content.includes('登录') || content.includes('登陆')) {
        console.log('⚠️  检测到登录页面，请老板手动登录，登录后告诉我“已登录”');
    } else {
        console.log('✅ 已登录状态！准备执行发布任务...');
        // 这里可以接后续自动发布逻辑
    }

    // 保持连接，等待后续指令
    console.log('🦞 浏览器已就绪，等待下一步指令...');
}

run().catch(console.error);
