import { AppStoreClient } from './client.js';
import { searchApps, listInstalledApps, uninstallApp, getAppByKey, installAppByKey, batchInstallApps, batchUninstallApps, batchUninstallByName } from './modules/appstore.js';
// 从配置创建客户端
function createClientFromConfig(config) {
    // 优先从 Gateway 配置中读取
    const baseUrl = String(config?.config?.baseUrl || config?.baseUrl || process.env.ONEPANEL_BASE_URL || process.env.APPSTORE_BASE_URL || '');
    const apiKey = String(config?.config?.apiKey || config?.apiKey || process.env.ONEPANEL_API_KEY || process.env.APPSTORE_API_KEY || '');
    const timeoutMs = typeof config?.config?.timeoutMs === 'number'
        ? config.config.timeoutMs
        : (typeof config?.timeoutMs === 'number'
            ? config.timeoutMs
            : Number.parseInt(process.env.ONEPANEL_TIMEOUT_MS || process.env.APPSTORE_TIMEOUT_MS || '30000', 10));
    const maxRetries = typeof config?.config?.maxRetries === 'number'
        ? config.config.maxRetries
        : (typeof config?.maxRetries === 'number'
            ? config.maxRetries
            : Number.parseInt(process.env.ONEPANEL_MAX_RETRIES || '3', 10));
    const retryDelay = typeof config?.config?.retryDelay === 'number'
        ? config.config.retryDelay
        : (typeof config?.retryDelay === 'number'
            ? config.retryDelay
            : Number.parseInt(process.env.ONEPANEL_RETRY_DELAY || '1000', 10));
    return new AppStoreClient({ baseUrl, apiKey, timeoutMs, maxRetries, retryDelay });
}
// 文本结果格式化
function textResult(payload) {
    return {
        content: [
            {
                type: 'text',
                text: JSON.stringify(payload, null, 2)
            }
        ]
    };
}
// 错误结果格式化
function errorResult(message, details) {
    return textResult({
        success: false,
        error: message,
        ...details
    });
}
// Skill 定义
export default {
    id: 'appstore-skill',
    name: 'App Store Skill',
    description: '1Panel 应用商店管理 Skill。支持搜索、安装、卸载和查看已安装应用。包含批量操作功能。',
    version: '0.3.0',
    configSchema: {
        type: 'object',
        additionalProperties: false,
        properties: {
            baseUrl: {
                type: 'string',
                minLength: 1,
                description: '1Panel 服务器地址'
            },
            apiKey: {
                type: 'string',
                minLength: 1,
                description: '1Panel API 认证密钥'
            },
            timeoutMs: {
                type: 'integer',
                minimum: 1000,
                default: 30000,
                description: '请求超时时间（毫秒）'
            },
            maxRetries: {
                type: 'integer',
                minimum: 0,
                maximum: 10,
                default: 3,
                description: '请求失败最大重试次数'
            },
            retryDelay: {
                type: 'integer',
                minimum: 100,
                maximum: 10000,
                default: 1000,
                description: '重试延迟（毫秒）'
            }
        },
        required: ['baseUrl', 'apiKey']
    },
    register(api) {
        // 配置管理工具
        api.registerTool({
            name: 'set_appstore_config',
            description: '设置并保存 1Panel API 配置（服务器地址和密钥）。此配置会被持久化保存，后续对话会自动使用。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    baseUrl: {
                        type: 'string',
                        description: '1Panel 服务器地址，如 http://192.168.1.100:10086'
                    },
                    apiKey: {
                        type: 'string',
                        description: '1Panel API 认证密钥'
                    },
                    timeoutMs: {
                        type: 'number',
                        description: '请求超时时间（毫秒），可选，默认 30000'
                    },
                    maxRetries: {
                        type: 'number',
                        description: '最大重试次数，可选，默认 3'
                    },
                    retryDelay: {
                        type: 'number',
                        description: '重试延迟（毫秒），可选，默认 1000'
                    }
                },
                required: ['baseUrl', 'apiKey']
            },
            async execute(config, params) {
                try {
                    const newConfig = {
                        baseUrl: String(params.baseUrl),
                        apiKey: String(params.apiKey)
                    };
                    if (typeof params.timeoutMs === 'number') {
                        newConfig.timeoutMs = params.timeoutMs;
                    }
                    if (typeof params.maxRetries === 'number') {
                        newConfig.maxRetries = params.maxRetries;
                    }
                    if (typeof params.retryDelay === 'number') {
                        newConfig.retryDelay = params.retryDelay;
                    }
                    // 验证配置是否有效
                    const testClient = new AppStoreClient(newConfig);
                    // 尝试连接以验证配置
                    const testResult = await testClient.request({
                        method: 'GET',
                        path: '/api/v1/apps/search',
                        query: { name: '', pageSize: 1 }
                    });
                    if (!testResult.data || testResult.status !== 200) {
                        return errorResult('配置验证失败，请检查地址和密钥是否正确', {
                            status: testResult.status,
                            data: testResult.data
                        });
                    }
                    return textResult({
                        success: true,
                        message: '配置已保存，后续对话将自动使用此配置',
                        config: {
                            baseUrl: newConfig.baseUrl,
                            timeoutMs: newConfig.timeoutMs,
                            maxRetries: newConfig.maxRetries,
                            retryDelay: newConfig.retryDelay
                        }
                    });
                }
                catch (error) {
                    return errorResult('配置保存失败', {
                        error: error instanceof Error ? error.message : String(error)
                    });
                }
            }
        });
        // 搜索应用商店
        api.registerTool({
            name: 'search_apps',
            description: '搜索 1Panel 应用商店中的应用。当用户想要查找某个应用（如 "搜索 Redis"、"有哪些数据库应用"）时使用。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    query: {
                        type: 'string',
                        description: '搜索关键词，如 "redis"、"mysql"、"database"'
                    },
                    pageSize: {
                        type: 'number',
                        description: '返回结果数量，默认 20'
                    }
                }
            },
            async execute(config, params) {
                try {
                    const client = createClientFromConfig(config);
                    const apps = await searchApps(client, {
                        name: typeof params.query === 'string' ? params.query : undefined,
                        pageSize: typeof params.pageSize === 'number' ? params.pageSize : 20
                    });
                    return textResult({
                        success: true,
                        count: apps.length,
                        apps: apps.map(app => ({
                            name: app.name,
                            key: app.key,
                            description: app.shortDescZh || app.shortDescEn || app.description,
                            installed: app.installed,
                            versions: app.versions ? app.versions.slice(0, 3) : []
                        }))
                    });
                }
                catch (error) {
                    return errorResult('搜索失败', { error: error instanceof Error ? error.message : String(error) });
                }
            }
        });
        // 列出已安装应用
        api.registerTool({
            name: 'list_installed_apps',
            description: '列出所有已安装的应用。当用户想要查看已安装的应用列表（如 "我安装了哪些应用"、"列出所有应用"、"查看应用状态"）时使用。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {}
            },
            async execute(config) {
                try {
                    const client = createClientFromConfig(config);
                    const apps = await listInstalledApps(client);
                    return textResult({
                        success: true,
                        count: apps.length,
                        apps: apps.map(app => ({
                            id: app.id,
                            name: app.name,
                            key: app.key,
                            status: app.status,
                            version: app.version
                        }))
                    });
                }
                catch (error) {
                    return errorResult('获取已安装应用失败', { error: error instanceof Error ? error.message : String(error) });
                }
            }
        });
        // 获取应用详情
        api.registerTool({
            name: 'get_app_info',
            description: '获取应用的详细信息，包括可用版本列表。当用户想要了解应用的版本信息（如 "Redis 有什么版本"、"查看 mysql 详情"）时使用。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    key: {
                        type: 'string',
                        description: '应用的 key，如 "mysql"、"redis"、"nginx"'
                    }
                },
                required: ['key']
            },
            async execute(config, params) {
                try {
                    const client = createClientFromConfig(config);
                    const result = await getAppByKey(client, String(params.key));
                    if (!result || !result.data) {
                        return errorResult(`未找到应用: ${params.key}`);
                    }
                    const app = result.data;
                    return textResult({
                        success: true,
                        app: {
                            name: app.name,
                            key: app.key,
                            description: app.description,
                            versions: app.versions,
                            installed: app.installed
                        }
                    });
                }
                catch (error) {
                    return errorResult('获取应用详情失败', { error: error instanceof Error ? error.message : String(error) });
                }
            }
        });
        // 安装应用（简化版，自动处理 appDetailId 获取）
        api.registerTool({
            name: 'install_app',
            description: '从应用商店安装应用。当用户想要安装应用（如 "帮我安装 Redis"、"安装 mysql"）时使用。会自动选择最新版本。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    key: {
                        type: 'string',
                        description: '应用的 key，如 "mysql"、"redis"、"nginx"'
                    },
                    name: {
                        type: 'string',
                        description: '安装后的应用实例名称，可选，默认使用应用 key'
                    },
                    version: {
                        type: 'string',
                        description: '指定版本，可选，默认使用最新版本'
                    }
                },
                required: ['key']
            },
            async execute(config, params) {
                try {
                    const client = createClientFromConfig(config);
                    const key = String(params.key);
                    const name = typeof params.name === 'string' ? params.name : key;
                    const version = typeof params.version === 'string' ? params.version : undefined;
                    const result = await installAppByKey(client, key, { name, version });
                    if (result.success) {
                        return textResult({
                            success: true,
                            message: '安装成功',
                            app: {
                                key,
                                name,
                                version: version || 'latest',
                                id: result.data?.id
                            }
                        });
                    }
                    else {
                        return errorResult(result.message || '安装失败');
                    }
                }
                catch (error) {
                    return errorResult('安装失败', { error: error instanceof Error ? error.message : String(error) });
                }
            }
        });
        // 卸载应用
        api.registerTool({
            name: 'uninstall_app',
            description: '卸载已安装的应用。当用户想要卸载应用（如 "卸载 Redis"、"删除 mysql"）时使用。需要先通过 list_installed_apps 获取 installId。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    installId: {
                        type: 'number',
                        description: '应用的安装 ID（从 list_installed_apps 获取）'
                    }
                },
                required: ['installId']
            },
            async execute(config, params) {
                try {
                    const client = createClientFromConfig(config);
                    const result = await uninstallApp(client, typeof params.installId === 'number' ? params.installId : Number(params.installId));
                    if (result.success) {
                        return textResult({
                            success: true,
                            message: '卸载成功'
                        });
                    }
                    else {
                        return errorResult(result.message || '卸载失败');
                    }
                }
                catch (error) {
                    return errorResult('卸载失败', { error: error instanceof Error ? error.message : String(error) });
                }
            }
        });
        // ========== 新增：批量操作工具 ==========
        // 批量安装应用
        api.registerTool({
            name: 'batch_install_apps',
            description: '批量安装多个应用。当用户想要一次安装多个应用（如 "帮我安装 Redis 和 MySQL"、"安装数据库应用"）时使用。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    apps: {
                        type: 'array',
                        description: '要安装的应用列表',
                        items: {
                            type: 'object',
                            properties: {
                                key: { type: 'string', description: '应用 key' },
                                name: { type: 'string', description: '实例名称（可选）' },
                                version: { type: 'string', description: '版本（可选）' }
                            },
                            required: ['key']
                        }
                    }
                },
                required: ['apps']
            },
            async execute(config, params) {
                try {
                    const client = createClientFromConfig(config);
                    const apps = params.apps;
                    if (!Array.isArray(apps) || apps.length === 0) {
                        return errorResult('请提供要安装的应用列表');
                    }
                    const result = await batchInstallApps(client, apps);
                    return textResult({
                        success: result.failed === 0,
                        summary: `总计 ${result.total} 个，成功 ${result.succeeded} 个，失败 ${result.failed} 个`,
                        details: result.results
                    });
                }
                catch (error) {
                    return errorResult('批量安装失败', { error: error instanceof Error ? error.message : String(error) });
                }
            }
        });
        // 批量卸载应用（按 ID）
        api.registerTool({
            name: 'batch_uninstall_apps',
            description: '批量卸载多个应用（按 ID）。当用户想要一次卸载多个应用时使用。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    installIds: {
                        type: 'array',
                        description: '要卸载的应用 ID 列表',
                        items: { type: 'number' }
                    }
                },
                required: ['installIds']
            },
            async execute(config, params) {
                try {
                    const client = createClientFromConfig(config);
                    const installIds = params.installIds;
                    if (!Array.isArray(installIds) || installIds.length === 0) {
                        return errorResult('请提供要卸载的应用 ID 列表');
                    }
                    const result = await batchUninstallApps(client, installIds);
                    return textResult({
                        success: result.failed === 0,
                        summary: `总计 ${result.total} 个，成功 ${result.succeeded} 个，失败 ${result.failed} 个`,
                        details: result.results
                    });
                }
                catch (error) {
                    return errorResult('批量卸载失败', { error: error instanceof Error ? error.message : String(error) });
                }
            }
        });
        // 按名称批量卸载
        api.registerTool({
            name: 'batch_uninstall_by_name',
            description: '按应用名称批量卸载。当用户想要按名称卸载多个应用（如 "卸载 Redis 和 MySQL"）时使用，更方便。',
            parameters: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    names: {
                        type: 'array',
                        description: '要卸载的应用名称列表',
                        items: { type: 'string' }
                    }
                },
                required: ['names']
            },
            async execute(config, params) {
                try {
                    const client = createClientFromConfig(config);
                    const names = params.names;
                    if (!Array.isArray(names) || names.length === 0) {
                        return errorResult('请提供要卸载的应用名称列表');
                    }
                    const result = await batchUninstallByName(client, names);
                    return textResult({
                        success: result.failed === 0,
                        summary: `总计 ${result.total} 个，成功 ${result.succeeded} 个，失败 ${result.failed} 个`,
                        details: result.results
                    });
                }
                catch (error) {
                    return errorResult('批量卸载失败', { error: error instanceof Error ? error.message : String(error) });
                }
            }
        });
    }
};
//# sourceMappingURL=plugin.js.map