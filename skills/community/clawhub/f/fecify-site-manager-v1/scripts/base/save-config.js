/**
 * 保存站点 URL + Token，并自动调用 /api/skill/base/init 获取站点信息
 * 
 * 用法: node scripts/base/save-config.js "<URL>" "<Token>"
 */

const config = require('../base/site-config');
const https = require('https');
const http = require('http');
const { URL } = require('url');

const url = process.argv[2];
const token = process.argv[3];

if (!url || !token) {
    console.log('用法: node save-config.js <URL> <TOKEN>');
    process.exit(1);
}

// 从 URL 提取域名
const domain = new URL(url).hostname;

// 1. 保存 URL + Token
config.saveConfig(domain, url, token);

// 2. 调用 /api/skill/base/init 获取站点信息
const baseUrl = new URL(url);
const apiPath = baseUrl.pathname.replace(/\/$/, '') + '/api/skill/base/init';

const options = {
    hostname: baseUrl.hostname,
    port: baseUrl.port || (baseUrl.protocol === 'https:' ? 443 : 80),
    path: apiPath,
    method: 'GET',
    headers: {
        'skill-access-token': token,
        'Content-Type': 'application/json'
    },
    timeout: 30000
};

const transport = baseUrl.protocol === 'https:' ? https : http;

const req = transport.request(options, (res) => {
    let data = '';
    res.on('data', chunk => data += chunk);
    res.on('end', () => {
        try {
            const json = JSON.parse(data);
            if (json.code === 200 && json.data) {
                // 3. 保存 init 返回的 data 对象
                config.saveInitData(domain, json.data);
                console.log(JSON.stringify({
                    success: true,
                    domain: domain,
                    hasInitData: true,
                    message: `站点 ${domain} 已绑定，init 数据已拉取，重启不丢失`
                }));
            } else {
                // API 返回异常但配置已保存
                console.log(JSON.stringify({
                    success: true,
                    domain: domain,
                    hasInitData: false,
                    apiCode: json.code,
                    apiMessage: json.message || 'API 返回异常',
                    message: `站点 ${domain} 已绑定，但 init 数据拉取失败: ${json.message || '未知错误'}`
                }));
            }
        } catch (e) {
            console.log(JSON.stringify({
                success: true,
                domain: domain,
                hasInitData: false,
                message: `站点 ${domain} 已绑定，但 init 数据解析失败: ${e.message}`
            }));
        }
    });
});

req.on('error', (err) => {
    console.log(JSON.stringify({
        success: true,
        domain: domain,
        hasInitData: false,
        message: `站点 ${domain} 已绑定，但 init API 请求失败: ${err.message}`
    }));
});

req.on('timeout', () => {
    req.destroy();
    console.log(JSON.stringify({
        success: true,
        domain: domain,
        hasInitData: false,
        message: `站点 ${domain} 已绑定，但 init API 请求超时`
    }));
});

req.end();
