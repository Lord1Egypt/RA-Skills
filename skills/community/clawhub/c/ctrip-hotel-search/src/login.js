const { chromium } = require('playwright');
const { delay } = require('./utils');

/**
 * 登录携程账号
 * @param {string} username - 用户名
 * @param {string} password - 密码
 * @param {object} options - 浏览器选项
 * @returns {Promise<object>} 浏览器和页面对象
 */
async function loginCtrip(username, password, options = {}) {
  const {
    headless = false,
    slowMo = 100,
    timeout = 30000
  } = options;

  console.log('🚀 启动浏览器...');
  const browser = await chromium.launch({
    headless: headless,
    slowMo: slowMo
  });

  const context = await browser.newContext({
    viewport: { width: 1280, height: 720 },
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });

  const page = await context.newPage();
  page.setDefaultTimeout(timeout);

  try {
    console.log('📝 打开携程登录页...');
    await page.goto('https://passport.ctrip.com/login', { waitUntil: 'networkidle' });

    // 等待登录表单加载
    await page.waitForSelector('#username', { timeout: 10000 });
    console.log('✅ 登录页加载完成');

    // 输入用户名
    console.log('🔑 输入用户名...');
    await page.fill('#username', username);
    await delay(500);

    // 输入密码
    console.log('🔐 输入密码...');
    await page.fill('#password', password);
    await delay(500);

    // 点击登录按钮
    console.log('🖱️ 点击登录按钮...');
    await page.click('#loginBtn');
    
    // 等待登录完成（检查是否跳转或出现错误）
    await Promise.race([
      page.waitForNavigation({ waitUntil: 'networkidle', timeout: 15000 }),
      page.waitForSelector('.user-name', { timeout: 15000 }).catch(() => {})
    ]);

    // 验证登录是否成功
    const isLoggedIn = await page.evaluate(() => {
      return document.querySelector('.user-name') !== null || 
             window.location.href.includes('ctrip.com') && 
             !window.location.href.includes('login');
    });

    if (isLoggedIn) {
      console.log('✅ 登录成功！');
      return { browser, page, context };
    } else {
      console.log('⚠️ 登录可能需要验证码，请手动完成');
      console.log('💡 提示：可以截图验证码并手动输入');
      return { browser, page, context };
    }

  } catch (error) {
    console.error('❌ 登录失败:', error.message);
    await browser.close();
    throw error;
  }
}

/**
 * 检查登录状态
 * @param {object} page - Playwright 页面对象
 * @returns {Promise<boolean>} 是否已登录
 */
async function checkLoginStatus(page) {
  try {
    const isLoggedIn = await page.evaluate(() => {
      return document.querySelector('.user-name') !== null;
    });
    return isLoggedIn;
  } catch (error) {
    return false;
  }
}

/**
 * 退出登录
 * @param {object} page - Playwright 页面对象
 */
async function logout(page) {
  try {
    console.log('🚪 退出登录...');
    await page.goto('https://passport.ctrip.com/logout');
    console.log('✅ 已退出登录');
  } catch (error) {
    console.error('❌ 退出登录失败:', error.message);
  }
}

module.exports = {
  loginCtrip,
  checkLoginStatus,
  logout
};