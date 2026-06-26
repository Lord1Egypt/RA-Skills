"use strict";
/**
 * 飞书API客户端
 * Feishu API Client with intelligent caching and retry
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.FeishuApiClient = void 0;
const axios_1 = __importDefault(require("axios"));
const node_cache_1 = __importDefault(require("node-cache"));
class FeishuApiClient {
    client;
    cache;
    config;
    tenantAccessToken = null;
    tokenExpireTime = 0;
    constructor(config) {
        this.config = config;
        // 初始化缓存
        this.cache = new node_cache_1.default({
            stdTTL: config.cache.ttl,
            checkperiod: config.cache.checkperiod,
            useClones: false
        });
        // 初始化HTTP客户端
        this.client = axios_1.default.create({
            baseURL: config.feishu.baseUrl || 'https://open.feishu.cn/open-apis',
            timeout: 30000,
            headers: {
                'Content-Type': 'application/json'
            }
        });
        // 请求拦截器 - 自动添加Token
        this.client.interceptors.request.use(async (config) => {
            const token = await this.getTenantAccessToken();
            config.headers.Authorization = `Bearer ${token}`;
            return config;
        });
        // 响应拦截器 - 统一错误处理
        this.client.interceptors.response.use((response) => response, async (error) => {
            return this.handleApiError(error);
        });
    }
    /**
     * 获取租户访问令牌
     */
    async getTenantAccessToken() {
        // 检查缓存的token是否有效
        if (this.tenantAccessToken && Date.now() < this.tokenExpireTime) {
            return this.tenantAccessToken;
        }
        try {
            const response = await axios_1.default.post('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
                app_id: this.config.feishu.appId,
                app_secret: this.config.feishu.appSecret
            });
            const { code, msg, tenant_access_token, expire } = response.data;
            if (code !== 0) {
                throw new Error(`Failed to get access token: ${msg}`);
            }
            this.tenantAccessToken = tenant_access_token;
            // 提前5分钟过期
            this.tokenExpireTime = Date.now() + (expire - 300) * 1000;
            return tenant_access_token;
        }
        catch (error) {
            throw new Error(`Authentication failed: ${error instanceof Error ? error.message : String(error)}`);
        }
    }
    /**
     * API错误处理
     */
    async handleApiError(error) {
        if (error.response) {
            const { status, data } = error.response;
            // Token过期，刷新后重试
            if (status === 401 || data?.code === 99991663) {
                this.tenantAccessToken = null;
                // 这里可以实现重试逻辑
            }
            // 限流处理
            if (status === 429 || data?.code === 99991400) {
                const retryAfter = parseInt(error.response.headers['retry-after'] || '1');
                console.log(`Rate limited, retrying after ${retryAfter} seconds...`);
                await this.sleep(retryAfter * 1000);
                // 重试原请求
                return this.client.request(error.config);
            }
            throw new Error(`API Error [${status}]: ${JSON.stringify(data)}`);
        }
        throw error;
    }
    sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }
    /**
     * 带重试的API请求
     */
    async requestWithRetry(requestFn, retries = this.config.retry.maxRetries) {
        try {
            return await requestFn();
        }
        catch (error) {
            if (retries > 0 && this.isRetryableError(error)) {
                await this.sleep(this.config.retry.delay * (this.config.retry.maxRetries - retries + 1));
                return this.requestWithRetry(requestFn, retries - 1);
            }
            throw error;
        }
    }
    isRetryableError(error) {
        if (axios_1.default.isAxiosError(error)) {
            const code = error.response?.data?.code;
            // 可重试的错误码
            const retryableCodes = [99991400, 99991663, 99991664, 99992001, 99992002];
            return retryableCodes.includes(code);
        }
        return false;
    }
    // ==================== Bitable API Methods ====================
    /**
     * 获取多维表格元数据
     */
    async getBitableMeta(appToken) {
        const cacheKey = `meta:${appToken}`;
        const cached = this.cache.get(cacheKey);
        if (cached) {
            return {
                success: true,
                data: cached,
                meta: { duration: 0 }
            };
        }
        const startTime = Date.now();
        try {
            const response = await this.requestWithRetry(() => this.client.get(`/bitable/v1/apps/${appToken}`));
            const { code, msg, data } = response.data;
            if (code !== 0) {
                return {
                    success: false,
                    error: { code: String(code), message: msg }
                };
            }
            // 缓存结果
            this.cache.set(cacheKey, data);
            return {
                success: true,
                data,
                meta: { duration: Date.now() - startTime }
            };
        }
        catch (error) {
            return {
                success: false,
                error: {
                    code: 'REQUEST_FAILED',
                    message: error instanceof Error ? error.message : String(error)
                }
            };
        }
    }
    /**
     * 获取表格字段列表
     */
    async getTableFields(appToken, tableId) {
        const cacheKey = `fields:${appToken}:${tableId}`;
        const cached = this.cache.get(cacheKey);
        if (cached) {
            return {
                success: true,
                data: cached,
                meta: { duration: 0 }
            };
        }
        const startTime = Date.now();
        try {
            const response = await this.requestWithRetry(() => this.client.get(`/bitable/v1/apps/${appToken}/tables/${tableId}/fields`));
            const { code, msg, data } = response.data;
            if (code !== 0) {
                return {
                    success: false,
                    error: { code: String(code), message: msg }
                };
            }
            this.cache.set(cacheKey, data?.items || []);
            return {
                success: true,
                data: data?.items || [],
                meta: { duration: Date.now() - startTime }
            };
        }
        catch (error) {
            return {
                success: false,
                error: {
                    code: 'REQUEST_FAILED',
                    message: error instanceof Error ? error.message : String(error)
                }
            };
        }
    }
    /**
     * 查询记录列表
     */
    async listRecords(appToken, tableId, options = {}) {
        const startTime = Date.now();
        try {
            const params = {
                page_size: options.pageSize || 500
            };
            if (options.filter) {
                params.filter = options.filter;
            }
            if (options.pageToken) {
                params.page_token = options.pageToken;
            }
            const response = await this.requestWithRetry(() => this.client.get(`/bitable/v1/apps/${appToken}/tables/${tableId}/records`, { params }));
            const { code, msg, data } = response.data;
            if (code !== 0) {
                return {
                    success: false,
                    error: { code: String(code), message: msg }
                };
            }
            return {
                success: true,
                data: {
                    records: data?.items || [],
                    hasMore: data?.has_more || false,
                    pageToken: data?.page_token
                },
                meta: {
                    duration: Date.now() - startTime,
                    affectedRows: data?.items?.length || 0
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: {
                    code: 'REQUEST_FAILED',
                    message: error instanceof Error ? error.message : String(error)
                }
            };
        }
    }
    /**
     * 获取单条记录
     */
    async getRecord(appToken, tableId, recordId) {
        const startTime = Date.now();
        try {
            const response = await this.requestWithRetry(() => this.client.get(`/bitable/v1/apps/${appToken}/tables/${tableId}/records/${recordId}`));
            const { code, msg, data } = response.data;
            if (code !== 0) {
                return {
                    success: false,
                    error: { code: String(code), message: msg }
                };
            }
            return {
                success: true,
                data,
                meta: { duration: Date.now() - startTime }
            };
        }
        catch (error) {
            return {
                success: false,
                error: {
                    code: 'REQUEST_FAILED',
                    message: error instanceof Error ? error.message : String(error)
                }
            };
        }
    }
    /**
     * 创建记录
     */
    async createRecord(appToken, tableId, fields) {
        const startTime = Date.now();
        try {
            const response = await this.requestWithRetry(() => this.client.post(`/bitable/v1/apps/${appToken}/tables/${tableId}/records`, { fields }));
            const { code, msg, data } = response.data;
            if (code !== 0) {
                return {
                    success: false,
                    error: { code: String(code), message: msg }
                };
            }
            // 清除相关缓存
            this.cache.del(`records:${appToken}:${tableId}`);
            return {
                success: true,
                data,
                meta: { duration: Date.now() - startTime }
            };
        }
        catch (error) {
            return {
                success: false,
                error: {
                    code: 'REQUEST_FAILED',
                    message: error instanceof Error ? error.message : String(error)
                }
            };
        }
    }
    /**
     * 更新记录
     */
    async updateRecord(appToken, tableId, recordId, fields) {
        const startTime = Date.now();
        try {
            const response = await this.requestWithRetry(() => this.client.put(`/bitable/v1/apps/${appToken}/tables/${tableId}/records/${recordId}`, { fields }));
            const { code, msg, data } = response.data;
            if (code !== 0) {
                return {
                    success: false,
                    error: { code: String(code), message: msg }
                };
            }
            // 清除相关缓存
            this.cache.del(`records:${appToken}:${tableId}`);
            return {
                success: true,
                data,
                meta: { duration: Date.now() - startTime }
            };
        }
        catch (error) {
            return {
                success: false,
                error: {
                    code: 'REQUEST_FAILED',
                    message: error instanceof Error ? error.message : String(error)
                }
            };
        }
    }
    /**
     * 删除记录
     */
    async deleteRecord(appToken, tableId, recordId) {
        const startTime = Date.now();
        try {
            const response = await this.requestWithRetry(() => this.client.delete(`/bitable/v1/apps/${appToken}/tables/${tableId}/records/${recordId}`));
            const { code, msg } = response.data;
            if (code !== 0) {
                return {
                    success: false,
                    error: { code: String(code), message: msg }
                };
            }
            // 清除相关缓存
            this.cache.del(`records:${appToken}:${tableId}`);
            return {
                success: true,
                meta: { duration: Date.now() - startTime }
            };
        }
        catch (error) {
            return {
                success: false,
                error: {
                    code: 'REQUEST_FAILED',
                    message: error instanceof Error ? error.message : String(error)
                }
            };
        }
    }
    /**
     * 批量创建记录
     */
    async batchCreateRecords(appToken, tableId, records) {
        const startTime = Date.now();
        try {
            const response = await this.requestWithRetry(() => this.client.post(`/bitable/v1/apps/${appToken}/tables/${tableId}/records/batch_create`, { records }));
            const { code, msg, data } = response.data;
            if (code !== 0) {
                return {
                    success: false,
                    error: { code: String(code), message: msg }
                };
            }
            // 清除相关缓存
            this.cache.del(`records:${appToken}:${tableId}`);
            return {
                success: true,
                data,
                meta: {
                    duration: Date.now() - startTime,
                    affectedRows: records.length
                }
            };
        }
        catch (error) {
            return {
                success: false,
                error: {
                    code: 'REQUEST_FAILED',
                    message: error instanceof Error ? error.message : String(error)
                }
            };
        }
    }
    /**
     * 清除缓存
     */
    clearCache() {
        this.cache.flushAll();
    }
}
exports.FeishuApiClient = FeishuApiClient;
//# sourceMappingURL=api-client.js.map