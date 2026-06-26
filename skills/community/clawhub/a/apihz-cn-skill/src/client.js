/**
 * 接口盒子 API 客户端
 * ApiHz Client for OpenClaw
 * 
 * @author JARVIS
 * @version 1.0.0
 * @date 2026-03-08
 */

const https = require('https');
const http = require('http');
const URL = require('url').URL;
const querystring = require('querystring');

class ApiHzClient {
  constructor(options = {}) {
    this.id = options.id || process.env.APIHZ_ID || '你的 ID';
    this.key = options.key || process.env.APIHZ_KEY || '你的 KEY';
    this.baseUrl = options.baseUrl || process.env.APIHZ_BASE_URL || 'https://cn.apihz.cn';
    this.timeout = options.timeout || 10000; // 10 秒超时
    this.retryCount = options.retryCount || 2; // 重试 2 次
  }

  /**
   * 通用请求方法
   * @param {string} endpoint - API 端点
   * @param {object} params - 请求参数
   * @param {string} method - GET/POST
   * @returns {Promise<object>}
   */
  async request(endpoint, params = {}, method = 'POST') {
    const url = new URL(endpoint, this.baseUrl);
    const defaultParams = { id: this.id, key: this.key };
    const allParams = { ...defaultParams, ...params };

    return new Promise((resolve, reject) => {
      const options = {
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: url.pathname + (method === 'GET' ? '?' + querystring.stringify(allParams) : ''),
        method: method,
        timeout: this.timeout,
        agent: false, // 不使用连接池，避免 socket hang up
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'OpenClaw-ApiHz-Client/1.0',
          'Connection': 'close'
        }
      };

      const req = (url.protocol === 'https:' ? https : http).request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const result = JSON.parse(data);
            if (result.code === 200) {
              resolve(result);
            } else {
              reject(new Error(`API Error: ${result.msg || result.message || 'Unknown error'}`));
            }
          } catch (e) {
            reject(new Error(`Parse Error: ${e.message}`));
          }
        });
      });

      req.on('error', reject);
      req.on('timeout', () => {
        req.destroy();
        reject(new Error('Request timeout'));
      });

      if (method === 'POST') {
        req.write(querystring.stringify(allParams));
      }

      req.end();
    });
  }

  /**
   * 带重试的请求
   */
  async requestWithRetry(endpoint, params, method = 'POST') {
    let lastError;
    for (let i = 0; i < this.retryCount; i++) {
      try {
        return await this.request(endpoint, params, method);
      } catch (error) {
        lastError = error;
        if (i < this.retryCount - 1) {
          await new Promise(r => setTimeout(r, 1000 * (i + 1)));
        }
      }
    }
    throw lastError;
  }

  // ==================== 天气相关 ====================

  /**
   * 国内天气预报 - 城市查询
   * @param {string} province - 省份
   * @param {string} city - 城市
   */
  async weather({ province, city }) {
    return await this.requestWithRetry('/api/tianqi/tqyb.php', {
      sheng: province,
      place: city,
      day: 7,
      hourtype: 1
    });
  }

  /**
   * 国内天气预报 - IP 查询
   * @param {string} ip - IP 地址
   */
  async weatherByIP(ip) {
    return await this.requestWithRetry('/api/tianqi/tqybip.php', { ip });
  }

  /**
   * 国外城市天气
   * @param {string} city - 城市英文名
   */
  async weatherInternational(city) {
    return await this.requestWithRetry('/api/tianqi/tqybun.php', { city });
  }

  /**
   * 地震数据
   */
  async earthquake() {
    return await this.requestWithRetry('/api/tianqi/dizhen.php', {});
  }

  /**
   * 地震速报
   */
  async earthquakeQuick() {
    return await this.requestWithRetry('/api/tianqi/dizhensu.php', {});
  }

  // ==================== 网络工具 ====================

  /**
   * Ping 测试
   * @param {string} host - 主机地址
   */
  async ping(host) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 6,
      words1: host
    });
  }

  /**
   * 端口扫描
   * @param {string} ip - IP 地址
   * @param {string} ports - 端口范围
   */
  async portScan(ip, ports = '1-1000') {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 2,
      words1: ip,
      words2: ports
    });
  }

  /**
   * WHOIS 查询
   * @param {string} domain - 域名
   */
  async whois(domain) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 7,
      words1: domain
    });
  }

  /**
   * ICP 备案查询
   * @param {string} domain - 域名
   */
  async icp(domain) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 4,
      words1: domain
    });
  }

  /**
   * SSL 证书查询
   * @param {string} domain - 域名
   */
  async ssl(domain) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 52,
      words1: domain
    });
  }

  // ==================== 数据查询 ====================

  /**
   * IP 归属地查询
   * @param {string} ip - IP 地址
   */
  async ipLookup(ip) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 12,
      words1: ip
    });
  }

  /**
   * 手机号归属地
   * @param {string} phone - 手机号
   */
  async phoneLookup(phone) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 11,
      words1: phone
    });
  }

  /**
   * 身份证归属地
   * @param {string} idcard - 身份证号
   */
  async idcardLookup(idcard) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 13,
      words1: idcard
    });
  }

  // ==================== 内容采集 ====================

  /**
   * 头条热榜
   */
  async newsHot() {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 66
    });
  }

  /**
   * 网页 TDK 采集
   * @param {string} url - 网址
   */
  async tdk(url) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 18,
      words1: url
    });
  }

  /**
   * 网页链接采集
   * @param {string} url - 网址
   */
  async linkExtract(url) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 5,
      words1: url
    });
  }

  // ==================== 工具服务 ====================

  /**
   * 临时邮箱生成
   */
  async tempEmailCreate() {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 35
    });
  }

  /**
   * 临时邮箱查询
   * @param {string} email - 邮箱地址
   */
  async tempEmailInbox(email) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 36,
      words1: email
    });
  }

  /**
   * 二维码生成
   * @param {string} content - 内容
   */
  async qrcodeGenerate(content) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 25,
      words1: content
    });
  }

  /**
   * 翻译
   * @param {string} text - 文本
   * @param {string} from - 源语言
   * @param {string} to - 目标语言
   */
  async translate(text, from = 'auto', to = 'zh') {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 41,
      words1: text,
      words2: from,
      words3: to
    });
  }

  /**
   * 文字转拼音
   * @param {string} text - 文本
   */
  async pinyin(text) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 37,
      words1: text
    });
  }

  // ==================== 时间服务 ====================

  /**
   * 当前时间戳
   */
  async timestamp() {
    return await this.request('/api/time/getapi.php', { type: 1 }, 'GET');
  }

  /**
   * 万年历
   * @param {number} year - 年
   * @param {number} month - 月
   * @param {number} day - 日
   */
  async calendar(year, month, day) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 20,
      words1: year.toString(),
      words2: month.toString(),
      words3: day.toString()
    });
  }

  // ==================== 金融服务 ====================

  /**
   * 货币汇率
   */
  async exchangeRate() {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 82
    });
  }

  /**
   * 彩票开奖
   * @param {string} type - 彩票类型
   */
  async lottery(type = 'ssq') {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 30,
      words1: type
    });
  }

  // ==================== 文化教育 ====================

  /**
   * 成语接龙
   * @param {string} idiom - 成语
   */
  async idiom(idiom) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 43,
      words1: idiom
    });
  }

  /**
   * 诗词查询
   * @param {string} keyword - 关键词
   */
  async poetry(keyword) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 61,
      words1: keyword
    });
  }

  /**
   * 历史上的今天
   */
  async historyToday() {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 42
    });
  }

  /**
   * 随机谜语
   */
  async riddle() {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 44
    });
  }

  // ==================== 娱乐测试 ====================

  /**
   * MBTI 测试
   */
  async mbti() {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 77
    });
  }

  /**
   * 周公解梦
   * @param {string} keyword - 梦境关键词
   */
  async dream(keyword) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 71,
      words1: keyword
    });
  }

  /**
   * 随机壁纸
   */
  async wallpaper() {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 27
    });
  }

  /**
   * 随机头像
   */
  async avatar() {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 40
    });
  }
}

module.exports = { ApiHzClient };
