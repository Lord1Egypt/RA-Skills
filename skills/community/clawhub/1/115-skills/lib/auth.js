const axios = require('axios');
const QRCode = require('qrcode');
const CookieStore = require('./storage/cookie-store');

/**
 * 115 扫码登录模块
 * 
 * 支持聊天内扫码登录，自动轮询状态，Cookie 自动保存
 */
class Auth115 {
  constructor(cookieStore = null) {
    this.cookieStore = cookieStore || new CookieStore();
    this.apiBase = 'https://passportapi.115.com';
    this.webApiBase = 'https://webapi.115.com';
    this.pollInterval = 3000; // 3 秒轮询
    this.maxPollCount = 100;  // 最多轮询 100 次（5 分钟）
    
    // 请求头 - 使用 115 浏览器 UA
    this.headers = {
      'User-Agent': 'Mozilla/5.0 115Browser/23.9.3.2',
      'Accept': 'application/json',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
      'Referer': 'https://115.com/'
    };
  }

  /**
   * 生成登录二维码
   * @returns {Promise<Object>} 二维码数据
   */
  async generateQRCode() {
    try {
      // 使用 115 生活 APP 的二维码 API
      const response = await axios.get(`${this.webApiBase}/qrcode/login`, {
        params: {
          client: 'web',
          _: Date.now()
        },
        headers: this.headers,
        timeout: 10000
      });

      const { data } = response;
      
      // 兼容多种响应格式
      const qrData = data.data || data;
      const qrcode = qrData.qrcode || qrData.qr_code || qrData.url;
      const key = qrData.key || qrData.qrcode_key || '';
      
      if (!qrcode) {
        throw new Error(data.error || data.message || '获取二维码失败');
      }

      // 生成二维码图片（Base64）
      const qrImage = await QRCode.toDataURL(qrcode, {
        width: 300,
        margin: 2,
        color: {
          dark: '#000000',
          light: '#ffffff'
        }
      });

      return {
        success: true,
        qrcode: qrcode,
        image: qrImage,
        key: key,
        expireAt: Date.now() + 300000, // 5 分钟后过期
        expireSeconds: 300
      };
    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  /**
   * 检查扫码状态
   * @param {string} qrcodeKey - 二维码密钥
   * @returns {Promise<Object>} 状态结果
   */
  async checkQRStatus(qrcodeKey) {
    try {
      const response = await axios.get(`${this.webApiBase}/qrcode/login/status`, {
        params: { 
          key: qrcodeKey,
          _: Date.now()
        },
        headers: this.headers,
        timeout: 10000
      });

      const { data } = response;
      const qrData = data.data || data;
      const status = qrData.status;

      // status: 0-等待扫码，1-已扫码待确认，2-登录成功，-1-过期，-2-取消
      switch (status) {
        case 2: { // 登录成功
          const cookie = this.parseCookie(qrData.cookie || qrData.cookies);
          return {
            success: true,
            cookie,
            status: 'logged_in',
            message: '登录成功'
          };
        }
        
        case 1: // 已扫码待确认
          return {
            success: false,
            pending: true,
            status: 'scanned',
            message: '已扫码，请在手机上确认'
          };
        
        case 0: // 等待扫码
          return {
            success: false,
            pending: true,
            status: 'waiting',
            message: '等待扫码'
          };
        
        case -1: // 二维码过期
          return {
            success: false,
            error: '二维码已过期，请重新登录',
            status: 'expired'
          };
        
        case -2: // 扫码取消
          return {
            success: false,
            error: '扫码已取消',
            status: 'cancelled'
          };
        
        default:
          return {
            success: false,
            pending: true,
            status: 'unknown',
            message: '未知状态'
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
   * @param {string} cookieString - Cookie 字符串
   * @returns {Object} Cookie 对象
   */
  parseCookie(cookieString) {
    const cookies = cookieString.split(';');
    const result = { uid: '', cid: '', se: '' };

    for (const cookie of cookies) {
      const [key, value] = cookie.trim().split('=');
      if (key === 'UID') result.uid = value;
      else if (key === 'CID') result.cid = value;
      else if (key === 'SE') result.se = value;
    }

    return result;
  }

  /**
   * 完整登录流程
   * @param {Object} callbacks - 回调函数
   * @param {Function} callbacks.onQRCode - 二维码生成回调
   * @param {Function} callbacks.onStatus - 状态更新回调
   * @param {Function} callbacks.onComplete - 完成回调
   * @param {Function} callbacks.onError - 错误回调
   * @returns {Promise<Object>} 登录结果
   */
  async login(callbacks = {}) {
    const { onQRCode, onStatus, onComplete, onError } = callbacks;

    try {
      // 1. 生成二维码
      const qrData = await this.generateQRCode();
      if (!qrData.success) {
        throw new Error(qrData.error || '生成二维码失败');
      }
      
      await onQRCode?.(qrData);

      // 2. 轮询扫码状态
      for (let i = 0; i < this.maxPollCount; i++) {
        await this.sleep(this.pollInterval);
        
        const status = await this.checkQRStatus(qrData.key);
        await onStatus?.(status);

        if (status.success && status.cookie) {
          // 3. 保存 Cookie
          const saveResult = await this.cookieStore.save({
            ...status.cookie,
            loginTime: Date.now(),
            expireAt: Date.now() + 90 * 24 * 60 * 60 * 1000 // 90 天
          });

          if (!saveResult.success) {
            throw new Error('保存 Cookie 失败：' + saveResult.error);
          }

          await onComplete?.({ 
            success: true, 
            cookie: status.cookie,
            saveResult 
          });
          
          return { 
            success: true, 
            cookie: status.cookie,
            saveResult 
          };
        }

        if (status.error && !status.pending) {
          throw new Error(status.error);
        }
      }

      throw new Error('登录超时，请重新尝试');
    } catch (error) {
      await onError?.(error);
      return { success: false, error: error.message };
    }
  }

  /**
   * 验证 Cookie 是否有效
   * @param {Object} cookie - Cookie 对象
   * @returns {Promise<boolean>} 是否有效
   */
  async validateCookie(cookie) {
    try {
      const response = await axios.get('https://my.115.com/?ct=ajax&ac=nav', {
        headers: {
          'Cookie': `UID=${cookie.uid}; CID=${cookie.cid}; SE=${cookie.se}`,
          ...this.headers
        },
        timeout: 10000
      });
      
      return response.data?.state === true;
    } catch {
      return false;
    }
  }

  /**
   * 检查登录状态
   * @returns {Promise<Object>} 登录状态
   */
  async checkLoginStatus() {
    const cookie = await this.cookieStore.load();
    
    if (!cookie) {
      return { 
        loggedIn: false, 
        reason: 'no_cookie' 
      };
    }

    const isValid = await this.validateCookie(cookie);
    
    if (!isValid) {
      await this.cookieStore.clear();
      return { 
        loggedIn: false, 
        reason: 'cookie_expired' 
      };
    }

    return {
      loggedIn: true,
      cookie,
      uid: cookie.uid,
      loginTime: cookie.loginTime,
      expireAt: cookie.expireAt
    };
  }

  /**
   * 退出登录
   * @returns {Promise<Object>} 退出结果
   */
  async logout() {
    return await this.cookieStore.clear();
  }

  /**
   * 休眠函数
   * @param {number} ms - 毫秒数
   * @returns {Promise<void>}
   */
  sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }
}

module.exports = Auth115;
