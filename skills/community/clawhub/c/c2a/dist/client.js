import { createHash } from 'node:crypto';
import http from 'node:http';
import https from 'node:https';
export class AppStoreClient {
    baseUrl;
    apiKey;
    timeoutMs;
    maxRetries;
    retryDelay;
    constructor(config) {
        this.baseUrl = new URL(config.baseUrl);
        this.apiKey = config.apiKey;
        this.timeoutMs = config.timeoutMs ?? 30000;
        this.maxRetries = config.maxRetries ?? 3;
        this.retryDelay = config.retryDelay ?? 1000;
    }
    static fromEnv(env) {
        const baseUrl = env.ONEPANEL_BASE_URL || env.APPSTORE_BASE_URL;
        const apiKey = env.ONEPANEL_API_KEY || env.APPSTORE_API_KEY;
        const trimmedBaseUrl = baseUrl?.trim();
        const trimmedApiKey = apiKey?.trim();
        if (!trimmedBaseUrl) {
            throw new Error('缺少环境变量: ONEPANEL_BASE_URL 或 APPSTORE_BASE_URL');
        }
        if (!trimmedApiKey) {
            throw new Error('缺少环境变量: ONEPANEL_API_KEY 或 APPSTORE_API_KEY');
        }
        return new AppStoreClient({
            baseUrl: trimmedBaseUrl,
            apiKey: trimmedApiKey,
            timeoutMs: Number.parseInt(env.ONEPANEL_TIMEOUT_MS || env.APPSTORE_TIMEOUT_MS || '30000', 10),
            maxRetries: Number.parseInt(env.ONEPANEL_MAX_RETRIES || '3', 10),
            retryDelay: Number.parseInt(env.ONEPANEL_RETRY_DELAY || '1000', 10)
        });
    }
    async request(options) {
        let lastError = null;
        for (let attempt = 0; attempt <= this.maxRetries; attempt++) {
            try {
                if (attempt > 0) {
                    const delay = this.retryDelay * Math.pow(2, attempt - 1);
                    await this.sleep(delay);
                }
                return await this.executeRequest(options);
            }
            catch (error) {
                lastError = error;
                const shouldRetry = error instanceof Error &&
                    (error.message.includes('timeout') ||
                        error.message.includes('ECONNREFUSED') ||
                        error.message.includes('ETIMEDOUT') ||
                        (error instanceof Error && error.code?.startsWith('E')));
                if (!shouldRetry || attempt === this.maxRetries) {
                    throw new Error(`请求失败 (尝试 ${attempt + 1}/${this.maxRetries + 1}): ${lastError.message}`);
                }
            }
        }
        throw lastError;
    }
    async executeRequest(options) {
        const url = this.buildUrl(options.path, options.query);
        const body = options.body ? JSON.stringify(options.body) : undefined;
        const headers = this.buildHeaders(body);
        const isHttps = url.protocol === 'https:';
        const transport = isHttps ? https : http;
        return new Promise((resolve, reject) => {
            const req = transport.request({
                protocol: url.protocol,
                hostname: url.hostname,
                port: url.port || (isHttps ? 443 : 80),
                path: `${url.pathname}${url.search}`,
                method: options.method,
                headers,
                timeout: this.timeoutMs
            }, (res) => {
                const chunks = [];
                res.on('data', (chunk) => {
                    chunks.push(Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk));
                });
                res.on('end', () => {
                    const rawBody = Buffer.concat(chunks).toString('utf8');
                    const data = this.parseResponse(rawBody, res.headers['content-type']);
                    if (res.statusCode && res.statusCode >= 400) {
                        reject(new Error(`HTTP ${res.statusCode}: ${rawBody}`));
                        return;
                    }
                    resolve({
                        status: res.statusCode ?? 0,
                        headers: this.normalizeHeaders(res.headers),
                        data
                    });
                });
            });
            req.on('timeout', () => {
                req.destroy(new Error(`请求超时 (${this.timeoutMs}ms)`));
            });
            req.on('error', reject);
            if (body) {
                req.write(body);
            }
            req.end();
        });
    }
    buildUrl(path, query) {
        const normalizedPath = path.startsWith('/') ? path : `/${path}`;
        const url = new URL(normalizedPath, this.baseUrl);
        if (query) {
            for (const [key, value] of Object.entries(query)) {
                if (value !== undefined && value !== null && value !== '') {
                    url.searchParams.set(key, String(value));
                }
            }
        }
        return url;
    }
    buildHeaders(body) {
        const timestamp = `${Math.floor(Date.now() / 1000)}`;
        const token = createHash('md5')
            .update(`1panel${this.apiKey}${timestamp}`)
            .digest('hex');
        return {
            'Accept': 'application/json, text/plain, text/event-stream',
            'Content-Type': 'application/json',
            '1Panel-Token': token,
            '1Panel-Timestamp': timestamp,
            'Content-Length': body ? `${Buffer.byteLength(body)}` : '0'
        };
    }
    normalizeHeaders(headers) {
        const normalized = {};
        for (const [key, value] of Object.entries(headers)) {
            if (Array.isArray(value)) {
                normalized[key] = value.join(', ');
            }
            else if (value !== undefined) {
                normalized[key] = String(value);
            }
        }
        return normalized;
    }
    parseResponse(rawBody, contentType) {
        const ct = Array.isArray(contentType) ? contentType[0] : contentType;
        if (ct?.includes('application/json')) {
            try {
                return JSON.parse(rawBody);
            }
            catch {
                return rawBody;
            }
        }
        try {
            return JSON.parse(rawBody);
        }
        catch {
            return rawBody;
        }
    }
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
}
//# sourceMappingURL=client.js.map