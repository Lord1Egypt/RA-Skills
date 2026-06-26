const puppeteer = require('puppeteer');
// const QRCode = require('qrcode'); // 暂时未使用，注释掉
const CookieStore = require('./storage/cookie-store');

/**
 * 115 自动化扫码登录模块（使用 Puppeteer）
 * 
 * 通过自动化浏览器打开 115 登录页面，截取二维码供用户扫描
 */
class AuthPuppeteer {
  constructor(cookieStore = null) {
    this.cookieStore = cookieStore || new CookieStore();
    this.browser = null;
    this.page = null;
    this.pollInterval = 3000;
    this.maxPollCount = 100;
  }

  /**
   * 启动浏览器并生成登录二维码
   * @returns {Promise<Object>} 二维码数据
   */
  async generateQRCode() {
    try {
      // 启动无头浏览器
      this.browser = await puppeteer.launch({
        headless: 'new',
        args: [
          '--no-sandbox',
          '--disable-setuid-sandbox',
          '--disable-dev-shm-usage',
          '--disable-gpu'
        ]
      });

      this.page = await this.browser.newPage();
      
      // 设置 User-Agent
      await this.page.setUserAgent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');

      // 访问 115 登录页面
      await this.page.goto('https://115.com/', {
        waitUntil: 'networkidle2',
        timeout: 30000
      });

      // 等待登录二维码出现
      await this.page.waitForSelector('canvas, img[src*="qrcode"], .qrcode', {
        timeout: 10000
      }).catch(async () => {
        // 如果没找到，尝试点击登录按钮
        await this.page.click('.login-btn, [class*="login"]').catch(() => {});
        await this.page.waitForSelector('canvas, img[src*="qrcode"], .qrcode', {
          timeout: 10000
        });
      });

      // 截取二维码区域
      const qrcodeElement = await this.page.$('canvas, img[src*="qrcode"], .qrcode');
      
      if (!qrcodeElement) {
        throw new Error('未找到二维码元素');
      }

      // 获取二维码截图
      const screenshot = await qrcodeElement.screenshot();
      const qrImageBase64 = screenshot.toString('base64');
      
      // 生成 DataURL
      const qrImage = `data:image/png;base64,${qrImageBase64}`;

      // 生成二维码文本（用于解析）
      const qrcodeText = await this.page.evaluate(() => {
        /* eslint-disable no-undef */
        const img = document.querySelector('img[src*="qrcode"]');
        if (img) return img.src;
        const canvas = document.querySelector('canvas');
        if (canvas) {
          // 从 canvas 获取数据
          return canvas.toDataURL();
        }
        return null;
        /* eslint-enable no-undef */
      });

      return {
        success: true,
        qrcode: qrcodeText || qrImage,
        image: qrImage,
        key: await this._extractQRKey(),
        expireAt: Date.now() + 300000,
        expireSeconds: 300
      };

    } catch (error) {
      await this.close();
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * 从页面提取二维码 Key
   * @private
   */
  async _extractQRKey() {
    try {
      const key = await this.page.evaluate(() => {
        /* eslint-disable no-undef */
        // 尝试从各种位置获取 key
        const img = document.querySelector('img[src*="qrcode"]');
        if (img) {
          const src = img.src;
          const match = src.match(/key=([^&]+)/);
          if (match) return match[1];
        }
        
        // 尝试从 data 属性获取
        const qrcodeDiv = document.querySelector('[data-key], [qrcode-key]');
        if (qrcodeDiv) {
          return qrcodeDiv.dataset.key || qrcodeDiv.getAttribute('qrcode-key');
        }
        
        // 尝试从全局变量获取
        if (window.qrcodeKey) return window.qrcodeKey;
        if (window.loginData?.key) return window.loginData.key;
        /* eslint-enable no-undef */
        
        return '';
      });
      
      return key || '';
    } catch {
      return '';
    }
  }

  /**
   * 检查扫码状态
   * @param {string} _qrcodeKey - 二维码密钥（未使用，保留用于兼容）
   * @returns {Promise<Object>} 状态结果
   */
  async checkQRStatus(_qrcodeKey) {
    try {
      if (!this.page) {
        return {
          success: false,
          error: '浏览器未初始化',
          status: 'error'
        };
      }

      // 检查页面 URL 是否已跳转（登录成功）
      const currentUrl = this.page.url();
      if (currentUrl.includes('115.com/user') || currentUrl.includes('115.com/?ct=home')) {
        // 登录成功，获取 Cookie
        const cookies = await this.page.cookies();
        const cookie = this._parseCookies(cookies);
        
        await this.close();
        
        return {
          success: true,
          cookie,
          status: 'logged_in',
          message: '登录成功'
        };
      }

      // 检查是否有登录成功的提示
      const isLoggedIn = await this.page.evaluate(() => {
        /* eslint-disable no-undef */
        const userMenu = document.querySelector('.user-menu, .username, [class*="user"]');
        const logoutBtn = document.querySelector('[class*="logout"], .logout');
        /* eslint-enable no-undef */
        return !!(userMenu || logoutBtn);
      });

      if (isLoggedIn) {
        const cookies = await this.page.cookies();
        const cookie = this._parseCookies(cookies);
        
        await this.close();
        
        return {
          success: true,
          cookie,
          status: 'logged_in',
          message: '登录成功'
        };
      }

      // 检查是否过期
      const isExpired = await this.page.evaluate(() => {
        /* eslint-disable no-undef */
        const expiredMsg = document.querySelector('[class*="expire"], [class*="timeout"]');
        /* eslint-enable no-undef */
        return !!expiredMsg;
      });

      if (isExpired) {
        await this.close();
        return {
          success: false,
          error: '二维码已过期，请重新登录',
          status: 'expired'
        };
      }

      // 仍在等待扫码
      return {
        success: false,
        pending: true,
        status: 'waiting',
        message: '等待扫码'
      };

    } catch (error) {
      return {
        success: false,
        error: error.message,
        status: 'error'
      };
    }
  }

  /**
   * 解析浏览器 Cookie
   * @private
   */
  _parseCookies(cookies) {
    const cookieMap = {};
    cookies.forEach(c => {
      cookieMap[c.name.toLowerCase()] = c.value;
    });

    return {
      uid: cookieMap.uid || cookieMap['115_uid'] || '',
      cid: cookieMap.cid || cookieMap['115_cid'] || '',
      seid: cookieMap.seid || cookieMap.se || cookieMap['115_seid'] || '',
      kid: cookieMap.kid || cookieMap['115_kid'] || '',
      expireAt: Date.now() + 7776000000 // 90 天
    };
  }

  /**
   * 关闭浏览器
   */
  async close() {
    try {
      if (this.browser) {
        await this.browser.close();
        this.browser = null;
        this.page = null;
      }
    } catch (error) {
      // console.error('关闭浏览器失败:', error); // 静默失败
    }
  }

  /**
   * 等待登录（轮询检查）
   * @returns {Promise<Object>} 登录结果
   */
  async waitForLogin() {
    let count = 0;
    
    while (count < this.maxPollCount) {
      const status = await this.checkQRStatus('');
      
      if (status.status === 'logged_in') {
        // 保存 Cookie
        await this.cookieStore.save(status.cookie);
        return status;
      }
      
      if (status.status === 'expired' || status.status === 'cancelled') {
        return status;
      }
      
      await this._sleep(this.pollInterval);
      count++;
    }
    
    await this.close();
    return {
      success: false,
      error: '登录超时',
      status: 'timeout'
    };
  }

  /**
   * 睡眠
   * @private
   */
  _sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = AuthPuppeteer;
