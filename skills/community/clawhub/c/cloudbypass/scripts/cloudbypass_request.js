/**
 * 穿云API OpenClaw Skill
 * 用于绕过Cloudflare等反爬虫保护，访问受保护的网站
 * 
 * 参考文档：
 * - https://docs.cloudbypass.com/api-quick-reference.md
 * - https://www.cloudbypass.com/
 */

const https = require('https');
const http = require('http');
const { URL } = require('url');

class CloudbypassSkill {
    constructor(config = {}) {
        // 从配置或环境变量获取API密钥
        this.apiKey = config.apiKey || process.env.CLOUDBYPASS_APIKEY;
        if (!this.apiKey) {
            throw new Error('CLOUDBYPASS_APIKEY is required. Please set it in config or environment variable.');
        }

        // API基础地址
        this.apiBaseUrl = config.apiBaseUrl || 'https://api.cloudbypass.com';
        
        // 代理配置（V2模式需要）
        this.proxy = config.proxy || process.env.CLOUDBYPASS_PROXY;
        
        // 默认模式
        this.defaultMode = config.mode || process.env.CLOUDBYPASS_MODE || 'v1';
        
        // 会话分区（Part模式）
        this.part = config.part || process.env.CLOUDBYPASS_PART || '0';
        
        // Turnstile sitekey
        this.sitekey = config.sitekey || process.env.CLOUDBYPASS_SITEKEY;
        
        // 请求超时
        this.timeout = config.timeout || 65000;
    }

    /**
     * 发起请求
     * @param {Object} options 请求选项
     * @param {string} options.url 目标URL
     * @param {string} [options.method='GET'] HTTP方法
     * @param {Object} [options.headers={}] 额外的请求头
     * @param {string|Buffer} [options.body] 请求体
     * @param {string} [options.mode] API模式（v1/v2/v2s），默认使用构造函数中的配置。v2s用于文件下载流式传输
     * @param {string} [options.proxy] 代理地址（V2模式），默认使用构造函数中的配置
     * @param {string} [options.part] 会话分区（Part模式），默认使用构造函数中的配置
     * @param {string} [options.sitekey] Turnstile sitekey
     * @param {string} [options.protocol] 协议类型（http/https），默认从URL自动检测
     * @param {string} [options.options] 额外选项，如 'long-timeout,force,ignore-lock'
     * @returns {Promise<Object>} 响应对象 { status, headers, data, cookies }
     */
    async request(options = {}) {
        const {
            url,
            method = 'GET',
            headers = {},
            body,
            mode = this.defaultMode,
            proxy = this.proxy,
            part = this.part,
            sitekey = this.sitekey,
            protocol,
            options: extraOptions
        } = options;

        if (!url) {
            throw new Error('URL is required');
        }

        // 解析目标URL
        let targetUrl;
        try {
            targetUrl = new URL(url);
        } catch (error) {
            throw new Error(`Invalid URL: ${url}`);
        }

        // 构建穿云API URL
        const apiUrl = new URL(this.apiBaseUrl);
        apiUrl.pathname = targetUrl.pathname;
        apiUrl.search = targetUrl.search;

        // 构建请求头
        const requestHeaders = {
            'x-cb-apikey': this.apiKey,
            'x-cb-host': targetUrl.hostname,
            ...headers
        };

        // 协议类型
        if (protocol || targetUrl.protocol === 'http:') {
            requestHeaders['x-cb-protocol'] = protocol || 'http';
        }

        // V2模式配置
        if (mode === 'v2' || mode === 'v2s') {
            // V2 stream模式用于文件下载
            requestHeaders['x-cb-version'] = mode === 'v2s' ? '2s' : '2';
            
            if (!proxy) {
                throw new Error('Proxy is required for V2 mode. Please set proxy in config or CLOUDBYPASS_PROXY environment variable.');
            }
            requestHeaders['x-cb-proxy'] = proxy;
            
            if (part) {
                requestHeaders['x-cb-part'] = part;
            }
            
            if (sitekey) {
                requestHeaders['x-cb-sitekey'] = sitekey;
            }
        }

        // 额外选项
        if (extraOptions) {
            requestHeaders['x-cb-options'] = extraOptions;
        }

        // 处理请求体，设置Content-Type
        let requestBody = null;
        if (body) {
            if (typeof body === 'object') {
                requestBody = JSON.stringify(body);
                if (!requestHeaders['Content-Type']) {
                    requestHeaders['Content-Type'] = 'application/json';
                }
            } else {
                requestBody = body;
            }
        }

        // 发起请求
        return new Promise((resolve, reject) => {
            const isHttps = apiUrl.protocol === 'https:';
            const httpModule = isHttps ? https : http;

            const requestOptions = {
                hostname: apiUrl.hostname,
                port: apiUrl.port || (isHttps ? 443 : 80),
                path: apiUrl.pathname + apiUrl.search,
                method: method,
                headers: requestHeaders,
                timeout: this.timeout
            };

            const req = httpModule.request(requestOptions, (res) => {
                const status = res.headers['x-cb-status'];
                let data = '';

                res.on('data', (chunk) => {
                    data += chunk;
                });

                res.on('end', () => {
                    if (status === 'ok') {
                        // 成功响应
                        const response = {
                            status: res.statusCode,
                            headers: res.headers,
                            data: data,
                            cookies: res.headers['set-cookie'] || []
                        };
                        resolve(response);
                    } else {
                        // 失败响应
                        try {
                            const error = JSON.parse(data);
                            reject(new CloudbypassError(
                                error.code || 'UNKNOWN_ERROR',
                                error.message || 'Unknown error',
                                error.id
                            ));
                        } catch (e) {
                            reject(new CloudbypassError(
                                'PARSE_ERROR',
                                `Failed to parse error response: ${data}`,
                                null
                            ));
                        }
                    }
                });
            });

            req.on('error', (error) => {
                reject(new CloudbypassError(
                    'REQUEST_ERROR',
                    error.message,
                    null
                ));
            });

            req.on('timeout', () => {
                req.destroy();
                reject(new CloudbypassError(
                    'TIMEOUT',
                    `Request timeout after ${this.timeout}ms`,
                    null
                ));
            });

            // 写入请求体
            if (requestBody) {
                req.write(requestBody);
            }

            req.end();
        });
    }

    /**
     * V1模式请求（便捷方法）
     */
    async requestV1(options) {
        return this.request({ ...options, mode: 'v1' });
    }

    /**
     * V2模式请求（便捷方法）
     */
    async requestV2(options) {
        return this.request({ ...options, mode: 'v2' });
    }

    /**
     * V2 stream模式请求（便捷方法，用于文件下载）
     */
    async requestV2Stream(options) {
        return this.request({ ...options, mode: 'v2s' });
    }

    /**
     * GET请求（便捷方法）
     */
    async get(url, options = {}) {
        return this.request({ ...options, url, method: 'GET' });
    }

    /**
     * POST请求（便捷方法）
     */
    async post(url, body, options = {}) {
        return this.request({ ...options, url, method: 'POST', body });
    }

    /**
     * PUT请求（便捷方法）
     */
    async put(url, body, options = {}) {
        return this.request({ ...options, url, method: 'PUT', body });
    }

    /**
     * DELETE请求（便捷方法）
     */
    async delete(url, options = {}) {
        return this.request({ ...options, url, method: 'DELETE' });
    }

    /**
     * 下载文件（使用V2 stream模式）
     * @param {string} url 目标URL
     * @param {Object} [options={}] 请求选项
     * @param {string} [options.proxy] 代理地址，默认使用构造函数中的配置
     * @param {string} [options.part] 会话分区，默认使用构造函数中的配置
     * @param {string} [options.sitekey] Turnstile sitekey
     * @param {string} [options.protocol] 协议类型（http/https）
     * @param {string} [options.options] 额外选项
     * @returns {Promise<Object>} 响应对象 { status, headers, stream, cookies }
     *                            stream是Node.js的ReadableStream，可直接用于文件保存
     */
    async download(url, options = {}) {
        const {
            proxy = this.proxy,
            part = this.part,
            sitekey = this.sitekey,
            protocol,
            options: extraOptions,
            headers = {}
        } = options;

        if (!url) {
            throw new Error('URL is required');
        }

        if (!proxy) {
            throw new Error('Proxy is required for download. Please set proxy in config or CLOUDBYPASS_PROXY environment variable.');
        }

        // 解析目标URL
        let targetUrl;
        try {
            targetUrl = new URL(url);
        } catch (error) {
            throw new Error(`Invalid URL: ${url}`);
        }

        // 构建穿云API URL
        const apiUrl = new URL(this.apiBaseUrl);
        apiUrl.pathname = targetUrl.pathname;
        apiUrl.search = targetUrl.search;

        // 构建请求头
        const requestHeaders = {
            'x-cb-apikey': this.apiKey,
            'x-cb-host': targetUrl.hostname,
            'x-cb-version': '2s',  // V2 stream模式
            'x-cb-proxy': proxy,
            ...headers
        };

        // 协议类型
        if (protocol || targetUrl.protocol === 'http:') {
            requestHeaders['x-cb-protocol'] = protocol || 'http';
        }

        // 会话分区
        if (part) {
            requestHeaders['x-cb-part'] = part;
        }

        // Turnstile sitekey
        if (sitekey) {
            requestHeaders['x-cb-sitekey'] = sitekey;
        }

        // 额外选项
        if (extraOptions) {
            requestHeaders['x-cb-options'] = extraOptions;
        }

        // 发起请求，返回stream
        return new Promise((resolve, reject) => {
            const isHttps = apiUrl.protocol === 'https:';
            const httpModule = isHttps ? https : http;

            const requestOptions = {
                hostname: apiUrl.hostname,
                port: apiUrl.port || (isHttps ? 443 : 80),
                path: apiUrl.pathname + apiUrl.search,
                method: 'GET',
                headers: requestHeaders,
                timeout: this.timeout
            };

            const req = httpModule.request(requestOptions, (res) => {
                const status = res.headers['x-cb-status'];

                if (status === 'ok') {
                    // 成功响应，返回stream
                    const response = {
                        status: res.statusCode,
                        headers: res.headers,
                        stream: res,  // 直接返回响应流
                        cookies: res.headers['set-cookie'] || []
                    };
                    resolve(response);
                } else {
                    // 失败响应，读取错误信息
                    let errorData = '';
                    res.on('data', (chunk) => {
                        errorData += chunk;
                    });
                    res.on('end', () => {
                        try {
                            const error = JSON.parse(errorData);
                            reject(new CloudbypassError(
                                error.code || 'UNKNOWN_ERROR',
                                error.message || 'Unknown error',
                                error.id
                            ));
                        } catch (e) {
                            reject(new CloudbypassError(
                                'PARSE_ERROR',
                                `Failed to parse error response: ${errorData}`,
                                null
                            ));
                        }
                    });
                }
            });

            req.on('error', (error) => {
                reject(new CloudbypassError(
                    'REQUEST_ERROR',
                    error.message,
                    null
                ));
            });

            req.on('timeout', () => {
                req.destroy();
                reject(new CloudbypassError(
                    'TIMEOUT',
                    `Request timeout after ${this.timeout}ms`,
                    null
                ));
            });

            req.end();
        });
    }
}

/**
 * 穿云API错误类
 */
class CloudbypassError extends Error {
    constructor(code, message, id) {
        super(message);
        this.name = 'CloudbypassError';
        this.code = code;
        this.id = id;
    }

    toString() {
        return `CloudbypassError [${this.code}]: ${this.message}${this.id ? ` (id: ${this.id})` : ''}`;
    }
}

// 导出
module.exports = CloudbypassSkill;
module.exports.CloudbypassError = CloudbypassError;
