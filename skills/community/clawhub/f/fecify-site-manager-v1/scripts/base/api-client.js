/**
 * Fecify API 通用客户端
 * 
 * 自动读取当前会话绑定的 URL 和 Token，封装 HTTP 请求。
 * 所有业务脚本通过此模块访问 API，无需重复处理鉴权。
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');
const { getCurrentConfig, isConfigured, getCurrentInitData } = require('./site-config');

/**
 * 校验 /api/apps/{addon}/... 路径中的插件是否存在
 * @param {string} path - API 路径
 * @returns {{ valid: boolean, addon?: string, message?: string }}
 */
function validateAddon(path) {
    const match = path.match(/^\/api\/apps\/([^/]+)/);
    if (!match) return { valid: true };  // 非 apps 路径，无需校验

    const addon = match[1];
    const init = getCurrentInitData();
    if (!init || !init.data || !init.data.addons) {
        return { valid: false, addon, message: `无法获取插件列表（init 数据缺失），请重新提交 URL 和 Token` };
    }

    const addons = init.data.addons;
    if (!addons.includes(addon)) {
        return { valid: false, addon, message: `插件 "${addon}" 未安装，无法执行此 API。已安装插件列表可通过 init 数据查询。` };
    }

    return { valid: true, addon };
}

/**
 * 发起 HTTP 请求
 * @param {string} method - GET | POST | PUT | DELETE
 * @param {string} path - API 路径，如 '/api/skill/base/init'
 * @param {object} [body] - 请求体（仅 POST/PUT 需要）
 * @param {object} [extraHeaders] - 额外 header
 * @returns {Promise<{code: number, data: any, message: string}>}
 */
function request(method, path, body = null, extraHeaders = {}) {
    return new Promise((resolve, reject) => {
        const config = getCurrentConfig();
        if (!config || !config.url || !config.token) {
            return reject(new Error('未配置站点信息，请先提交 URL 和 Access Token。'));
        }

        // 校验 /api/apps/{addon}/... 路径：插件必须已安装
        const validation = validateAddon(path);
        if (!validation.valid) {
            return reject(new Error(validation.message));
        }

        const baseUrl = new URL(config.url);
        // 拼接完整路径：baseUrl 可能包含子路径（如 /apimanager666），必须保留
        const fullPath = baseUrl.pathname.replace(/\/$/, '') + '/' + path.replace(/^\//, '');

        const options = {
            hostname: baseUrl.hostname,
            port: baseUrl.port || (baseUrl.protocol === 'https:' ? 443 : 80),
            path: fullPath + (baseUrl.search || ''),
            method: method.toUpperCase(),
            headers: {
                'skill-access-token': config.token,
                'Content-Type': 'application/json',
                ...extraHeaders
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
                    resolve(json);
                } catch (e) {
                    const isHtml = /<\/?html|<!DOCTYPE|<title/i.test(data);
                    const errMsg = isHtml
                        ? `服务端返回 HTML 异常（PHP ErrorException / 致命错误），非 JSON 响应。前 300 字符: ${data.substring(0, 300)}`
                        : `JSON 解析失败。前 300 字符: ${data.substring(0, 300)}`;
                    resolve({ code: -1, message: errMsg, _raw: data.substring(0, 500) });
                }
            });
        });

        req.on('error', (err) => reject(new Error(`请求失败: ${err.message}`)));
        req.on('timeout', () => { req.destroy(); reject(new Error('请求超时 (30s)')); });

        if (body !== null) {
            req.write(JSON.stringify(body));
        }
        req.end();
    });
}

/** GET 请求 */
function get(path, extraHeaders = {}) {
    return request('GET', path, null, extraHeaders);
}

/** POST 请求 */
function post(path, body, extraHeaders = {}) {
    return request('POST', path, body, extraHeaders);
}

/** PUT 请求 */
function put(path, body, extraHeaders = {}) {
    return request('PUT', path, body, extraHeaders);
}

/** DELETE 请求 */
function del(path, extraHeaders = {}) {
    return request('DELETE', path, null, extraHeaders);
}

module.exports = { request, get, post, put, del, isConfigured };
