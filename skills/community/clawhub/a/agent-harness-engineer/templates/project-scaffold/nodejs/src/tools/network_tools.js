/**
 * ============================================
 * 类型: 核心框架
 * 模块: tools.network_tools
 * 说明: 网络请求工具实现
 * 修改建议: 如需扩展，添加新的工具方法并注册
 * ============================================

const axios = require('axios');

class NetworkTools {
  constructor() {
    this.webFetchSchema = {
      type: 'object',
      properties: {
        url: { type: 'string', description: '网页URL' },
        selector: { type: 'string', description: 'CSS选择器（可选）' }
      },
      required: ['url']
    };
    
    this.httpRequestSchema = {
      type: 'object',
      properties: {
        url: { type: 'string', description: '请求URL' },
        method: { type: 'string', description: 'HTTP方法', enum: ['GET', 'POST', 'PUT', 'DELETE'] },
        headers: { type: 'object', description: '请求头' },
        body: { type: 'string', description: '请求体' }
      },
      required: ['url', 'method']
    };
  }
  
  async webFetch(inputData) {
    const url = inputData.url;
    const selector = inputData.selector;
    
    try {
      const response = await axios.get(url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        },
        timeout: 10000
      });
      
      if (selector) {
        const cheerio = require('cheerio');
        const $ = cheerio.load(response.data);
        const elements = $(selector);
        return elements.map((i, el) => $(el).text()).get().join('\n');
      }
      
      return response.data;
    } catch (error) {
      return `Error: ${error.message}`;
    }
  }
  
  async httpRequest(inputData) {
    const url = inputData.url;
    const method = inputData.method || 'GET';
    const headers = inputData.headers || {};
    const body = inputData.body;
    
    try {
      let response;
      switch (method) {
        case 'GET':
          response = await axios.get(url, { headers, timeout: 10000 });
          break;
        case 'POST':
          response = await axios.post(url, body, { headers, timeout: 10000 });
          break;
        case 'PUT':
          response = await axios.put(url, body, { headers, timeout: 10000 });
          break;
        case 'DELETE':
          response = await axios.delete(url, { headers, timeout: 10000 });
          break;
        default:
          return { error: `Unsupported method: ${method}` };
      }
      
      return {
        status: response.status,
        headers: response.headers,
        body: response.data
      };
    } catch (error) {
      return { error: error.message };
    }
  }
}

module.exports = { NetworkTools };
