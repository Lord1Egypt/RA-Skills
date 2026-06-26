const https = require('https');
const http = require('http');

module.exports = {
  name: 'emily-web-fetch',
  description: 'Fetch a web page and return its content',
  tools: {
    fetch: async (url) => {
      return new Promise((resolve, reject) => {
        const isHttps = url.startsWith('https://');
        const protocol = isHttps ? https : http;

        const options = {
          headers: {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
          }
        };

        protocol.get(url, options, (res) => {
          if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
            const newUrl = new URL(res.headers.location, url).href;
            resolve(`<redirect>页面已重定向至: ${newUrl}</redirect>`);
            return;
          }
          if (res.statusCode !== 200) {
            reject(new Error(`HTTP ${res.statusCode}: ${res.statusMessage}`));
            return;
          }
          let data = '';
          res.on('data', chunk => data += chunk);
          res.on('end', () => {
            if (data.length > 5000) {
              data = data.substring(0, 5000) + '\n...（内容过长，已截断）';
            }
            resolve(data);
          });
        }).on('error', (err) => {
          reject(new Error(`抓取失败: ${err.message}`));
        });

        setTimeout(() => {
          reject(new Error('请求超时（10秒）'));
        }, 10000);
      });
    }
  }
};