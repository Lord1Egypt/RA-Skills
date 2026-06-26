const axios = require('axios');
const https = require('https');
const CookieStore = require('./storage/cookie-store');

/**
 * 115 网页版登录模块
 * 
 * 通过模拟 115 网页版的登录流程实现扫码登录
 */
class AuthWeb {
  constructor(cookieStore = null) {
    this.cookieStore = cookieStore || new CookieStore();
    
    // 创建 axios 实例
    this.httpClient = axios.create({
      baseURL: 'https://115.com',
      timeout: 10000,
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'Referer': 'https://115.com/'
      },
      httpsAgent: new https.Agent({
        rejectUnauthorized: false
      })
    });

    this.pollInterval = 3000;
    this.maxPollCount = 100;
    this.qrcodeKey = null;
  }

  /**
   * 生成登录二维码
   * @returns {Promise<Object>} 二维码数据
   */
  async generateQRCode() {
    try {
      // 方案 1: 使用 webapi.115.com
      const response = await this.httpClient.get('/qrcode/login', {
        params: {
          client: 'web',
          _: Date.now()
        }
      });

      const { data } = response;
      
      if (data.state === false && data.code) {
        throw new Error(data.message || data.error || '获取二维码失败');
      }

      const qrData = data.data || data;
      const qrcode = qrData.qrcode || qrData.qr_code || qrData.url || '';
      const key = qrData.key || qrData.qrcode_key || '';

      if (!qrcode) {
        throw new Error('无法获取二维码数据');
      }

      this.qrcodeKey = key;

      return {
        success: true,
        qrcode: qrcode,
        key: key,
        expireAt: Date.now() + 300000,
        expireSeconds: 300
      };

    } catch (error) {
      // 方案 2: 尝试 passport.115.com
      try {
        return await this._generateQRCodePassport();
      } catch (e) {
        return {
          success: false,
          error: error.message
        };
      }
    }
  }

  /**
   * 使用 passport.115.com 生成二维码
   * @private
   */
  async _generateQRCodePassport() {
    const response = await axios.get('https://passport.115.com/qrcode/generate', {
      params: {
        client: 'web',
        _: Date.now()
      },
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
      }
    });

    const { data } = response;
    const qrData = data.data || data;

    this.qrcodeKey = qrData.key || '';

    return {
      success: true,
      qrcode: qrData.qrcode || qrData.url,
      key: this.qrcodeKey,
      expireAt: Date.now() + 300000,
      expireSeconds: 300
    };
  }

  /**
   * 检查扫码状态
   * @param {string} qrcodeKey - 二维码密钥
   * @returns {Promise<Object>} 状态结果
   */
  async checkQRStatus(qrcodeKey) {
    try {
      const key = qrcodeKey || this.qrcodeKey;

      const response = await this.httpClient.get('/qrcode/login/status', {
        params: {
          key: key,
          _: Date.now()
        }
      });

      const { data } = response;
      const qrData = data.data || data;
      const status = qrData.status;

      switch (status) {
        case 2: { // 登录成功
          const cookie = this._parseCookie(qrData.cookie || qrData.cookies);
          return {
            success: true,
            cookie,
            status: 'logged_in',
            message: '登录成功'
          };
        }

        case 1: { // 已扫码待确认
          return {
            success: false,
            pending: true,
            status: 'scanned',
            message: '已扫码，请在手机上确认'
          };
        }

        case 0: { // 等待扫码
          return {
            success: false,
            pending: true,
            status: 'waiting',
            message: '等待扫码'
          };
        }

        case -1: { // 过期
          return {
            success: false,
            error: '二维码已过期，请重新登录',
            status: 'expired'
          };
        }

        case -2: { // 取消
          return {
            success: false,
            error: '扫码已取消',
            status: 'cancelled'
          };
        }

        default:
          return {
            success: false,
            pending: true,
            status: 'unknown',
            message: '等待扫码确认'
          };
      }

    } catch (error) {
      return {
        success: false,
        error: error.message,
        status: 'error'
      };
    }
  }

  /**
   * 解析 Cookie 字符串
   * @private
   */
  _parseCookie(cookieStr) {
    if (!cookieStr) return {};

    const cookies = {};
    const pairs = cookieStr.split(';');

    pairs.forEach(pair => {
      const [key, value] = pair.trim().split('=');
      if (key && value) {
        cookies[key.toLowerCase()] = value;
      }
    });

    return {
      uid: cookies.uid || cookies['115_uid'] || '',
      cid: cookies.cid || cookies['115_cid'] || '',
      seid: cookies.seid || cookies.se || cookies['115_seid'] || '',
      kid: cookies.kid || cookies['115_kid'] || '',
      expireAt: Date.now() + 7776000000
    };
  }

  /**
   * 等待登录（轮询检查）
   * @returns {Promise<Object>} 登录结果
   */
  async waitForLogin() {
    let count = 0;

    while (count < this.maxPollCount) {
      const status = await this.checkQRStatus(this.qrcodeKey);

      if (status.status === 'logged_in') {
        await this.cookieStore.save(status.cookie);
        return status;
      }

      if (status.status === 'expired' || status.status === 'cancelled') {
        return status;
      }

      await this._sleep(this.pollInterval);
      count++;
    }

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

module.exports = AuthWeb;
