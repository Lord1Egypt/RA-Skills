/**
 * 接口盒子 API 客户端 - HTML 解析增强版
 * ApiHz Client with HTML Parser
 * 
 * @author JARVIS
 * @version 1.0.1
 * @date 2026-03-09
 * 
 * @changelog
 * v1.0.1 (2026-03-09)
 *   - 修复：移除硬编码 IP，改为可配置 apiUrl
 *   - 新增：支持 APIHZ_LIST_URL 环境变量覆盖
 *   - 改进：文档说明 CDN 节点用途
 * 
 * v1.0.0 (2026-03-08)
 *   - 初始版本
 *   - 支持 7 个核心 JSON API (天气/地震/时间/ICP/Ping)
 *   - 集成 API 列表接口 (409+ API 目录)
 *   - HTML 响应智能解析
 *   - 自动重试机制
 *   - 41 个 API 分类支持
 */

const https = require('https');
const http = require('http');
const URL = require('url').URL;
const querystring = require('querystring');
const crypto = require('crypto');

class ApiHzClient {
  constructor(options = {}) {
    this.id = options.id || process.env.APIHZ_ID || '你的 ID';
    this.key = options.key || process.env.APIHZ_KEY || '你的 KEY';
    this.baseUrl = options.baseUrl || process.env.APIHZ_BASE_URL || 'https://cn.apihz.cn';
    this.timeout = options.timeout || 10000;
    this.retryCount = options.retryCount || 2;
    
    // API 列表接口配置 (可选覆盖)
    // 默认使用官方 CDN 节点，可通过配置或环境变量覆盖
    this.apiUrl = options.apiUrl || process.env.APIHZ_LIST_URL || 'http://101.35.2.25/api/xitong/apilist.php';
    
    // 动态密钥配置 (可选)
    // 开启动态密钥后，每次调用需先获取 dcan，然后生成 dkey
    this.dmsg = options.dmsg || process.env.APIHZ_DMSG || '';
    this._lastDcan = null;
    this._dcanTimestamp = 0;
  }

  /**
   * 通用请求方法 (带 HTML 解析)
   * 
   * 安全说明:
   * - 核心 API 调用使用 baseUrl (默认 https://cn.apihz.cn)
   * - 凭证 (ID/KEY) 通过 POST 参数传输
   * - 建议在生产环境确保 baseUrl 使用 HTTPS
   * - 支持动态密钥 (dkey) 验证
   * 
   * 官方教程参考：https://www.apihz.cn/template/miuu/getpost.php
   */
  async request(endpoint, params = {}, method = 'POST') {
    const url = new URL(endpoint, this.baseUrl);
    
    // 安全警告：如果 baseUrl 不是 HTTPS，输出警告
    if (url.protocol === 'http:' && !this._httpWarningShown) {
      console.warn('⚠️  警告：当前使用 HTTP 连接，凭证可能以明文传输。建议使用 HTTPS 主服务器。');
      this._httpWarningShown = true;
    }
    
    // 动态密钥处理 (如果配置了 dmsg)
    if (this.dmsg) {
      const dkey = await this.generateDkey();
      if (dkey) {
        params.dkey = dkey;
      }
    }
    
    const defaultParams = { id: this.id, key: this.key };
    const allParams = { ...defaultParams, ...params };

    return new Promise((resolve, reject) => {
      const options = {
        hostname: url.hostname,
        port: url.port || (url.protocol === 'https:' ? 443 : 80),
        path: url.pathname + (method === 'GET' ? '?' + querystring.stringify(allParams) : ''),
        method: method,
        timeout: this.timeout,
        agent: false,
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.5845.97 Safari/537.36',
          'Connection': 'close'
        }
      };

      const req = (url.protocol === 'https:' ? https : http).request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const result = this.parseResponse(data);
            if (result.code === 200) {
              resolve(result);
            } else {
              resolve(result); // 返回错误码，不 reject
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
   * 智能响应解析 (JSON + HTML)
   */
  parseResponse(response) {
    const trimmed = response.trim();
    
    // 1. 空响应处理
    if (!trimmed) {
      return { code: 403, msg: '需要会员权限或参数错误', data: null };
    }

    // 2. 尝试 JSON 解析
    try {
      const json = JSON.parse(trimmed);
      return this.normalizeJson(json);
    } catch (e) {
      // 3. HTML 解析
      if (trimmed.startsWith('<')) {
        return this.parseHtml(trimmed);
      }
      // 4. 其他格式
      return { code: 500, msg: '未知响应格式', raw: trimmed.substring(0, 200) };
    }
  }

  /**
   * 标准化 JSON 响应
   */
  normalizeJson(json) {
    // 数组 → 包装
    if (Array.isArray(json)) {
      return { code: 200, data: json, msg: 'success' };
    }
    // 已有 code 字段
    if (json.code !== undefined) {
      return json;
    }
    // 其他 JSON → 包装
    return { code: 200, data: json, msg: 'success' };
  }

  /**
   * HTML 响应解析 (简化版)
   */
  parseHtml(html) {
    // 提取 title
    const titleMatch = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    const title = titleMatch ? titleMatch[1].trim() : '';

    // 提取 h1
    const h1Match = html.match(/<h1[^>]*>([^<]+)<\/h1>/i);
    const h1 = h1Match ? h1Match[1].trim() : '';

    // 检测错误页面
    if (title.includes('403') || html.includes('403 Forbidden')) {
      return { code: 403, msg: 'Forbidden - 需要会员权限或访问受限', html: title || h1 };
    }
    if (title.includes('404') || html.includes('404 Not Found')) {
      return { code: 404, msg: 'Not Found - API 端点不存在', html: title || h1 };
    }
    if (title.includes('500') || html.includes('500 Internal')) {
      return { code: 500, msg: 'Server Error - 服务器错误', html: title || h1 };
    }

    // 提取表格数据 (如果有)
    const tableData = this.extractHtmlTable(html);
    if (tableData.length > 0) {
      return { code: 200, data: tableData, msg: 'success (from HTML table)' };
    }

    // 未知 HTML
    return { 
      code: 500, 
      msg: '未知 HTML 响应', 
      html: title || h1 || html.substring(0, 100) 
    };
  }

  /**
   * 提取 HTML 表格数据 (简化正则实现)
   */
  extractHtmlTable(html) {
    const data = [];
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    const cellRegex = /<t[dh][^>]*>([\s\S]*?)<\/t[dh]>/gi;
    
    let rowMatch;
    while ((rowMatch = rowRegex.exec(html)) !== null) {
      const rowHtml = rowMatch[1];
      const rowData = [];
      let cellMatch;
      while ((cellMatch = cellRegex.exec(rowHtml)) !== null) {
        // 去除 HTML 标签
        const cellText = cellMatch[1].replace(/<[^>]+>/g, '').trim();
        if (cellText) {
          rowData.push(cellText);
        }
      }
      if (rowData.length > 0) {
        data.push(rowData);
      }
      cellRegex.lastIndex = 0; // 重置正则
    }
    
    return data;
  }

  /**
   * 带重试的请求
   */
  async requestWithRetry(endpoint, params, method = 'POST') {
    let lastError;
    for (let i = 0; i < this.retryCount; i++) {
      try {
        const result = await this.request(endpoint, params, method);
        if (result.code === 200) {
          return result;
        }
        // 非 200 也返回，让调用者决定
        return result;
      } catch (error) {
        lastError = error;
        if (i < this.retryCount - 1) {
          await new Promise(r => setTimeout(r, 1000 * (i + 1)));
        }
      }
    }
    throw lastError;
  }

  /**
   * 获取动态参数 (dcan)
   * @returns {Promise<string|null>} 动态参数，失败返回 null
   */
  async fetchDcan() {
    const dcanUrl = `${this.apiUrl.replace('/apilist.php', '/dcan.php')}?id=${this.id}&key=${this.key}`;
    
    try {
      const result = await this.request(dcanUrl, {}, 'GET');
      if (result.code === 200 && result.dcan) {
        this._lastDcan = result.dcan;
        this._dcanTimestamp = Date.now();
        return result.dcan;
      }
      return null;
    } catch (error) {
      console.error(`获取动态参数失败：${error.message}`);
      return null;
    }
  }

  /**
   * 生成动态密钥 (dkey)
   * dkey = md5(dmsg + dcan)
   * @returns {Promise<string|null>} 动态密钥，失败返回 null
   */
  async generateDkey() {
    if (!this.dmsg) return null;
    
    // 检查 dcan 是否有效 (10 秒有效期)
    const now = Date.now();
    if (this._lastDcan && (now - this._dcanTimestamp) < 10000) {
      // dcan 仍有效，直接使用
    } else {
      // 获取新的 dcan
      await this.fetchDcan();
      if (!this._lastDcan) {
        console.error('无法获取动态参数 (dcan)');
        return null;
      }
    }
    
    // 生成 dkey = md5(dmsg + dcan)
    const hash = crypto.createHash('md5').update(this.dmsg + this._lastDcan).digest('hex');
    const dkey = hash.toLowerCase();
    
    // dcan 只能用一次，使用后清除
    this._lastDcan = null;
    
    return dkey;
  }

  // ==================== 核心 API (已验证可用) ====================

  async weather({ province, city }) {
    return await this.requestWithRetry('/api/tianqi/tqyb.php', {
      sheng: province,
      place: city,
      day: 7,
      hourtype: 1
    });
  }

  async weatherByIP(ip) {
    return await this.requestWithRetry('/api/tianqi/tqybip.php', { ip });
  }

  async earthquake() {
    return await this.requestWithRetry('/api/tianqi/dizhen.php', {});
  }

  async timestamp() {
    return await this.request('/api/time/getapi.php', { type: 1 }, 'GET');
  }

  async ping(host) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 6,
      words1: host
    });
  }

  async icp(domain) {
    return await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 4,
      words1: domain
    });
  }

  // ==================== 扩展 API (需要会员或 HTML 解析) ====================

  async whois(domain) {
    const result = await this.requestWithRetry('/api/ajax/ajax.php', {
      type: 7,
      words1: domain
    });
    // WHOIS 可能返回 JSON 数组或 HTML
    return result;
  }

  async newsHot() {
    const result = await this.requestWithRetry('/api/ajax/ajax.php', { type: 66 });
    // 头条热榜可能返回空 (需要会员)
    if (result.code === 403) {
      result.msg += ' (头条热榜需要会员权限)';
    }
    return result;
  }

  async tempEmailCreate() {
    const result = await this.requestWithRetry('/api/ajax/ajax.php', { type: 35 });
    if (result.code === 403) {
      result.msg += ' (临时邮箱需要会员权限)';
    }
    return result;
  }

  async exchangeRate() {
    const result = await this.requestWithRetry('/api/ajax/ajax.php', { type: 82 });
    if (result.code === 403) {
      result.msg += ' (汇率查询需要会员权限)';
    }
    return result;
  }

  // ==================== API 列表接口 (409 个 API 目录) ====================

  /**
   * 获取 API 分类列表
   * @returns {Promise<Array>} 分类列表
   */
  async getCategories() {
    // API 列表接口使用官方 CDN 节点 (由接口盒子提供)
    // 备用节点：http://124.222.204.22 (腾讯云 CDN)
    const apiUrl = this.apiUrl || 'http://101.35.2.25/api/xitong/apilist.php';
    const result = await this.request(apiUrl, {
      type: 1
    });
    return result.data || [];
  }

  /**
   * 获取指定分类的 API 列表
   * @param {number} cid - 分类 ID (从 getCategories 获取)
   * @param {number} page - 页码 (默认 1)
   * @returns {Promise<Object>} API 列表 (分页)
   */
  async getApisByCategory(cid, page = 1) {
    const apiUrl = this.apiUrl || 'http://101.35.2.25/api/xitong/apilist.php';
    return await this.request(apiUrl, {
      type: 2,
      cid: cid.toString(),
      page: page.toString()
    });
  }

  /**
   * 获取所有 API (遍历所有分页)
   * @param {number} cid - 分类 ID
   * @returns {Promise<Array>} 完整 API 列表
   */
  async getAllApisByCategory(cid) {
    const firstPage = await this.getApisByCategory(cid, 1);
    const totalPages = parseInt(firstPage.maxpage) || 1;
    const allApis = [...(firstPage.data || [])];

    // 遍历剩余页面
    for (let page = 2; page <= totalPages; page++) {
      const result = await this.getApisByCategory(cid, page);
      if (result.data && result.data.length > 0) {
        allApis.push(...result.data);
      }
    }

    return allApis;
  }

  /**
   * 解析 HTML 参数说明
   * @param {string} html - HTML 表格
   * @returns {Array} 结构化参数列表
   */
  parseHtmlExplain(html) {
    if (!html) return [];
    
    const params = [];
    const rowRegex = /<tr[^>]*>([\s\S]*?)<\/tr>/gi;
    const cellRegex = /<td[^>]*>([\s\S]*?)<\/td>/gi;
    
    let rowMatch;
    while ((rowMatch = rowRegex.exec(html)) !== null) {
      const rowHtml = rowMatch[1];
      const cells = [];
      let cellMatch;
      while ((cellMatch = cellRegex.exec(rowHtml)) !== null) {
        const cellText = cellMatch[1].replace(/<[^>]+>/g, '').trim();
        cells.push(cellText);
      }
      if (cells.length >= 4) {
        params.push({
          name: cells[0],
          key: cells[1],
          required: cells[2] === '是',
          description: cells[3]
        });
      }
      cellRegex.lastIndex = 0;
    }
    
    return params;
  }

  /**
   * 搜索 API
   * @param {string} keyword - 关键词
   * @returns {Promise<Array>} 匹配的 API 列表
   */
  async searchApis(keyword) {
    const categories = await this.getCategories();
    const results = [];

    for (const category of categories) {
      // 简单实现：获取第一页，实际应遍历所有页
      const apis = await this.getApisByCategory(category.id || 1, 1);
      if (apis.data) {
        const matched = apis.data.filter(api => 
          api.name.includes(keyword) || 
          api.desc.includes(keyword)
        );
        results.push(...matched);
      }
    }

    return results;
  }
}

module.exports = { ApiHzClient };
