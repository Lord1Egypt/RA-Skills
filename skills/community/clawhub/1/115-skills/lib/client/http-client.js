const axios = require('axios');
const crypto = require('crypto');
const qs = require('qs');

/**
 * 115 API HTTP 请求封装
 * 
 * 功能：
 * - 统一请求签名
 * - 速率限制控制
 * - 自动重试机制
 * - 错误处理
 */
class HttpClient {
  constructor(cookie) {
    this.cookie = cookie;
    this.apiBase = 'https://webapi.115.com';
    
    // 速率限制配置
    this.rateLimit = {
      maxRequests: 100,        // 每分钟最大请求数
      windowMs: 60 * 1000,     // 时间窗口
      currentRequests: [],     // 当前窗口内的请求
      concurrentLimit: 5       // 并发限制
    };

    // 重试配置
    this.retryConfig = {
      maxRetries: 3,
      retryDelay: 1000,
      retryableStatus: [429, 500, 502, 503, 504]
    };

    // 默认请求头
    this.defaultHeaders = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
      'Accept': 'application/json',
      'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8'
    };

    // 并发控制
    this.activeRequests = 0;
    this.requestQueue = [];
  }

  /**
   * 生成请求签名
   * @param {Object} params - 请求参数
   * @returns {string} 签名
   */
  generateSign(params = {}) {
    const timestamp = Date.now();
    const signString = Object.keys(params)
      .sort()
      .map(key => `${key}=${params[key]}`)
      .join('&');
    
    return crypto.createHash('md5')
      .update(signString + timestamp + (this.cookie.se || ''))
      .digest('hex');
  }

  /**
   * 获取 Cookie 头
   * @returns {string} Cookie 字符串
   */
  getCookieHeader() {
    if (!this.cookie) return '';
    return `UID=${this.cookie.uid || ''}; CID=${this.cookie.cid || ''}; SE=${this.cookie.se || ''}`;
  }

  /**
   * 检查速率限制
   * @returns {Promise<void>}
   */
  async checkRateLimit() {
    const now = Date.now();
    
    // 清理过期请求
    this.rateLimit.currentRequests = this.rateLimit.currentRequests.filter(
      time => now - time < this.rateLimit.windowMs
    );

    // 检查是否超限
    if (this.rateLimit.currentRequests.length >= this.rateLimit.maxRequests) {
      const oldestRequest = this.rateLimit.currentRequests[0];
      const waitTime = this.rateLimit.windowMs - (now - oldestRequest);
      
      if (waitTime > 0) {
        await this.sleep(waitTime);
      }
    }

    // 记录请求
    this.rateLimit.currentRequests.push(Date.now());
  }

  /**
   * 并发控制 - 获取槽位
   * @returns {Promise<Function>} 释放函数
   */
  async acquireSlot() {
    if (this.activeRequests < this.rateLimit.concurrentLimit) {
      this.activeRequests++;
      return this.createReleaseFunction();
    }

    // 等待可用槽位
    return new Promise(resolve => {
      this.requestQueue.push(() => {
        this.activeRequests++;
        resolve(this.createReleaseFunction());
      });
    });
  }

  /**
   * 创建释放函数
   * @returns {Function} 释放函数
   */
  createReleaseFunction() {
    let released = false;
    return () => {
      if (released) return;
      released = true;
      this.activeRequests--;
      this.processQueue();
    };
  }

  /**
   * 处理队列
   */
  processQueue() {
    while (this.requestQueue.length > 0 && this.activeRequests < this.rateLimit.concurrentLimit) {
      const next = this.requestQueue.shift();
      if (next) next();
    }
  }

  /**
   * 发送请求
   * @param {string} endpoint - API 端点
   * @param {Object} options - 请求选项
   * @returns {Promise<Object>} 响应数据
   */
  async request(endpoint, options = {}) {
    const {
      method = 'GET',
      params = {},
      data = {},
      headers = {},
      useSign = false,
      retryCount = 0
    } = options;

    let release = null;

    try {
      // 速率限制
      await this.checkRateLimit();

      // 获取并发槽位
      release = await this.acquireSlot();

      // 构建完整 URL
      const url = endpoint.startsWith('http') ? endpoint : `${this.apiBase}${endpoint}`;

      // 准备请求头
      const requestHeaders = {
        ...this.defaultHeaders,
        ...headers,
        'Cookie': this.getCookieHeader()
      };

      // 添加签名
      if (useSign && method === 'POST') {
        params.sign = this.generateSign(params);
      }

      // POST 请求使用 form-urlencoded
      let requestData = data;
      if (method === 'POST' && typeof data === 'object') {
        requestHeaders['Content-Type'] = 'application/x-www-form-urlencoded';
        requestData = qs.stringify(data);
      }

      // 发送请求
      const response = await axios({
        method,
        url,
        params: method === 'GET' ? { ...params, _: Date.now() } : params,
        data: method === 'POST' ? requestData : undefined,
        headers: requestHeaders,
        timeout: 30000
      });

      // 处理响应
      const responseData = response.data;

      // 检查 HTTP 状态码
      if (response.status >= 400) {
        const error = new Error(`HTTP ${response.status}`);
        error.status = response.status;
        error.response = response;
        
        // 检查是否需要重试
        if (this.retryConfig.retryableStatus.includes(response.status)) {
          if (retryCount < this.retryConfig.maxRetries) {
            const delay = this.retryConfig.retryDelay * Math.pow(2, retryCount);
            await this.sleep(delay);
            return this.request(endpoint, { ...options, retryCount: retryCount + 1 });
          }
        }
        
        throw error;
      }

      // 检查业务错误
      if (responseData && responseData.state === false) {
        const error = new Error(responseData.error || 'API 请求失败');
        error.code = responseData.errno || 'API_ERROR';
        error.data = responseData;
        throw error;
      }

      return responseData;

    } catch (error) {
      // 网络错误重试
      if (!error.response && retryCount < this.retryConfig.maxRetries) {
        if (error.code === 'ECONNRESET' || 
            error.code === 'ETIMEDOUT' || 
            error.code === 'ECONNREFUSED' ||
            error.code === 'ENOTFOUND') {
          const delay = this.retryConfig.retryDelay * Math.pow(2, retryCount);
          await this.sleep(delay);
          return this.request(endpoint, { ...options, retryCount: retryCount + 1 });
        }
      }
      
      throw error;
    } finally {
      // 确保释放槽位
      if (release) {
        release();
      }
    }
  }

  /**
   * GET 请求
   * @param {string} endpoint - API 端点
   * @param {Object} params - 请求参数
   * @returns {Promise<Object>} 响应数据
   */
  async get(endpoint, params = {}) {
    return this.request(endpoint, { method: 'GET', params });
  }

  /**
   * POST 请求
   * @param {string} endpoint - API 端点
   * @param {Object} data - 请求数据
   * @param {Object} params - URL 参数
   * @returns {Promise<Object>} 响应数据
   */
  async post(endpoint, data = {}, params = {}) {
    return this.request(endpoint, { method: 'POST', data, params, useSign: true });
  }

  /**
   * 批量请求
   * @param {Array<Object>} requests - 请求数组
   * @returns {Promise<Array<Object>>} 响应数组
   */
  async batch(requests) {
    const results = [];
    const batchSize = 10;

    for (let i = 0; i < requests.length; i += batchSize) {
      const batch = requests.slice(i, i + batchSize);
      const batchResults = await Promise.all(
        batch.map(req => this.request(req.endpoint, req.options).catch(err => ({ error: err.message })))
      );
      results.push(...batchResults);
      
      // 避免速率限制
      if (i + batchSize < requests.length) {
        await this.sleep(500);
      }
    }

    return results;
  }

  /**
   * 延迟函数
   * @param {number} ms - 毫秒数
   * @returns {Promise<void>}
   */
  async sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  /**
   * 设置 Cookie
   * @param {Object} cookie - Cookie 对象
   */
  setCookie(cookie) {
    this.cookie = cookie;
  }
}

module.exports = HttpClient;
