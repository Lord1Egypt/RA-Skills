"use strict";
/**
 * FeishuBitable-Plus 技能核心
 * Main Skill Coordinator
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.FeishuBitableSkill = void 0;
const api_client_1 = require("./core/api-client");
const intent_engine_1 = require("./intelligence/intent-engine");
const config_manager_1 = require("./security/config-manager");
class FeishuBitableSkill {
    client = null;
    intentEngine;
    configManager;
    isInitialized = false;
    constructor() {
        this.intentEngine = new intent_engine_1.IntentEngine();
        this.configManager = new config_manager_1.ConfigManager();
    }
    /**
     * 初始化技能
     */
    async initialize() {
        if (this.isInitialized)
            return;
        const credentials = await this.configManager.getCredentials();
        if (!credentials) {
            throw new Error('未配置飞书凭证，请先运行: fbt config');
        }
        const config = {
            feishu: {
                appId: credentials.appId,
                appSecret: credentials.appSecret,
                baseUrl: 'https://open.feishu.cn/open-apis'
            },
            cache: {
                ttl: 300, // 5分钟
                checkperiod: 60
            },
            retry: {
                maxRetries: 3,
                delay: 1000
            }
        };
        this.client = new api_client_1.FeishuApiClient(config);
        this.isInitialized = true;
    }
    /**
     * 执行自然语言命令
     */
    async executeNaturalLanguage(text, options = {}) {
        if (!this.client) {
            return {
                success: false,
                error: { code: 'NOT_INITIALIZED', message: '技能未初始化' }
            };
        }
        // 解析意图
        const intent = this.intentEngine.parse(text);
        // 执行对应的操作
        return this.executeByIntent(intent, options);
    }
    /**
     * 根据意图执行操作
     */
    async executeByIntent(intent, options) {
        const { client } = this;
        if (!client) {
            return {
                success: false,
                error: { code: 'NOT_INITIALIZED', message: '技能未初始化' }
            };
        }
        const appToken = options.appToken || intent.entities.appToken;
        const tableId = options.tableId || intent.entities.tableId;
        switch (intent.intent) {
            case 'LIST_RECORDS':
                if (!appToken || !tableId) {
                    // 尝试从表名查找
                    if (intent.entities.tableName) {
                        const tableInfo = await this.findTableByName(appToken, intent.entities.tableName);
                        if (!tableInfo.success)
                            return tableInfo;
                        return client.listRecords(appToken, tableInfo.data.table_id, {
                            filter: this.intentEngine.buildFilterExpression(intent.entities.conditions || [])
                        });
                    }
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数: appToken 或 tableId' }
                    };
                }
                return client.listRecords(appToken, tableId, {
                    filter: this.intentEngine.buildFilterExpression(intent.entities.conditions || [])
                });
            case 'GET_RECORD':
                if (!appToken || !tableId || !intent.entities.recordId) {
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数' }
                    };
                }
                return client.getRecord(appToken, tableId, intent.entities.recordId);
            case 'CREATE_RECORD':
                if (!appToken || !tableId) {
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数: appToken 或 tableId' }
                    };
                }
                return client.createRecord(appToken, tableId, intent.entities.data || {});
            case 'UPDATE_RECORD':
                if (!appToken || !tableId || !intent.entities.recordId) {
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数' }
                    };
                }
                return client.updateRecord(appToken, tableId, intent.entities.recordId, intent.entities.data || {});
            case 'DELETE_RECORD':
                if (!appToken || !tableId || !intent.entities.recordId) {
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数' }
                    };
                }
                return client.deleteRecord(appToken, tableId, intent.entities.recordId);
            case 'BATCH_CREATE':
                if (!appToken || !tableId) {
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数' }
                    };
                }
                // 批量创建需要外部提供数据
                return {
                    success: false,
                    error: { code: 'NOT_IMPLEMENTED', message: '批量创建请使用 import 命令' }
                };
            case 'SYNC_TABLES':
                if (!appToken || !intent.entities.tableName || !intent.entities.targetTable) {
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数' }
                    };
                }
                return this.syncTables(appToken, intent.entities.tableName, intent.entities.targetTable);
            case 'GENERATE_REPORT':
                if (!appToken || !tableId) {
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数' }
                    };
                }
                return this.generateReport(appToken, tableId, intent.entities.reportType || 'general');
            case 'ANALYZE_DATA':
                if (!appToken || !tableId) {
                    return {
                        success: false,
                        error: { code: 'MISSING_PARAMS', message: '缺少必要的参数' }
                    };
                }
                return this.analyzeData(appToken, tableId);
            case 'UNKNOWN':
            default:
                return {
                    success: false,
                    error: {
                        code: 'UNKNOWN_INTENT',
                        message: `无法理解的命令: "${intent.originalText}"\n请尝试使用更明确的表达，如：\n- "列出XX表的所有记录"\n- "查找XX表中状态为进行中的记录"\n- "在XX表中添加记录"`
                    }
                };
        }
    }
    /**
     * 根据表名查找表格
     */
    async findTableByName(appToken, tableName) {
        const meta = await this.client.getBitableMeta(appToken);
        if (!meta.success || !meta.data) {
            return meta;
        }
        const table = meta.data.tables.find(t => t.name === tableName ||
            t.name.includes(tableName) ||
            tableName.includes(t.name));
        if (!table) {
            return {
                success: false,
                error: { code: 'TABLE_NOT_FOUND', message: `未找到表格: ${tableName}` }
            };
        }
        return {
            success: true,
            data: table
        };
    }
    /**
     * 列出所有表格
     */
    async listTables(appToken) {
        const meta = await this.client.getBitableMeta(appToken);
        if (meta.success && meta.data) {
            return {
                success: true,
                data: meta.data.tables
            };
        }
        return meta;
    }
    /**
     * 列出记录
     */
    async listRecords(appToken, tableId, options = {}) {
        return this.client.listRecords(appToken, tableId, options);
    }
    /**
     * 创建记录
     */
    async createRecord(appToken, tableId, fields) {
        return this.client.createRecord(appToken, tableId, fields);
    }
    /**
     * 更新记录
     */
    async updateRecord(appToken, tableId, recordId, fields) {
        return this.client.updateRecord(appToken, tableId, recordId, fields);
    }
    /**
     * 删除记录
     */
    async deleteRecord(appToken, tableId, recordId) {
        return this.client.deleteRecord(appToken, tableId, recordId);
    }
    /**
     * 批量创建记录
     */
    async batchCreateRecords(appToken, tableId, records) {
        return this.client.batchCreateRecords(appToken, tableId, records);
    }
    /**
     * 同步两个表格
     */
    async syncTables(appToken, sourceTableName, targetTableName) {
        // 查找源表和目标表
        const sourceResult = await this.findTableByName(appToken, sourceTableName);
        const targetResult = await this.findTableByName(appToken, targetTableName);
        if (!sourceResult.success)
            return sourceResult;
        if (!targetResult.success)
            return targetResult;
        const sourceTableId = sourceResult.data.table_id;
        const targetTableId = targetResult.data.table_id;
        // 获取源表所有记录
        const allRecords = [];
        let pageToken;
        let hasMore = true;
        while (hasMore) {
            const result = await this.client.listRecords(appToken, sourceTableId, { pageToken });
            if (result.success && result.data) {
                allRecords.push(...result.data.records);
                hasMore = result.data.hasMore;
                pageToken = result.data.pageToken;
            }
            else {
                return result;
            }
        }
        // 批量创建到目标表
        const recordsToCreate = allRecords.map(r => ({ fields: r.fields }));
        // 分批导入
        const batchSize = 500;
        let successCount = 0;
        for (let i = 0; i < recordsToCreate.length; i += batchSize) {
            const batch = recordsToCreate.slice(i, i + batchSize);
            const result = await this.client.batchCreateRecords(appToken, targetTableId, batch);
            if (result.success) {
                successCount += batch.length;
            }
        }
        return {
            success: true,
            data: {
                sourceTable: sourceTableName,
                targetTable: targetTableName,
                totalRecords: allRecords.length,
                syncedRecords: successCount
            }
        };
    }
    /**
     * 生成报表
     */
    async generateReport(appToken, tableId, reportType) {
        // 获取所有记录
        const allRecords = [];
        let pageToken;
        let hasMore = true;
        while (hasMore) {
            const result = await this.client.listRecords(appToken, tableId, { pageToken });
            if (result.success && result.data) {
                allRecords.push(...result.data.records);
                hasMore = result.data.hasMore;
                pageToken = result.data.pageToken;
            }
            else {
                return result;
            }
        }
        // 根据报表类型生成不同的统计
        const report = {
            totalRecords: allRecords.length,
            generatedAt: new Date().toISOString(),
            type: reportType
        };
        if (allRecords.length === 0) {
            return {
                success: true,
                data: report
            };
        }
        // 分析字段统计
        const fieldStats = {};
        for (const record of allRecords) {
            for (const [field, value] of Object.entries(record.fields)) {
                if (!fieldStats[field]) {
                    fieldStats[field] = { type: typeof value, values: [], unique: 0 };
                }
                fieldStats[field].values.push(value);
            }
        }
        // 计算唯一值数量
        for (const field of Object.keys(fieldStats)) {
            const uniqueValues = new Set(fieldStats[field].values.map(v => JSON.stringify(v)));
            fieldStats[field].unique = uniqueValues.size;
        }
        report.fieldStats = fieldStats;
        // 根据报表类型添加特定统计
        switch (reportType) {
            case 'summary':
                report.summary = this.generateSummaryStats(allRecords, fieldStats);
                break;
            case 'distribution':
                report.distribution = this.generateDistributionStats(allRecords, fieldStats);
                break;
            default:
                report.fields = Object.keys(fieldStats);
        }
        return {
            success: true,
            data: report
        };
    }
    /**
     * 生成汇总统计
     */
    generateSummaryStats(records, fieldStats) {
        const summary = {
            recordCount: records.length,
            fields: Object.keys(fieldStats).length
        };
        // 查找可能的数值字段进行统计
        for (const [field, stats] of Object.entries(fieldStats)) {
            const values = stats.values.filter((v) => typeof v === 'number');
            if (values.length > 0) {
                summary[field] = {
                    sum: values.reduce((a, b) => a + b, 0),
                    avg: values.reduce((a, b) => a + b, 0) / values.length,
                    min: Math.min(...values),
                    max: Math.max(...values)
                };
            }
        }
        return summary;
    }
    /**
     * 生成分布统计
     */
    generateDistributionStats(records, fieldStats) {
        const distribution = {};
        for (const [field, stats] of Object.entries(fieldStats)) {
            const valueCounts = {};
            for (const value of stats.values) {
                const key = typeof value === 'object' ? JSON.stringify(value) : String(value);
                valueCounts[key] = (valueCounts[key] || 0) + 1;
            }
            // 只显示前10个最常见的值
            const sorted = Object.entries(valueCounts)
                .sort((a, b) => b[1] - a[1])
                .slice(0, 10);
            distribution[field] = sorted;
        }
        return distribution;
    }
    /**
     * 数据分析
     */
    async analyzeData(appToken, tableId) {
        // 获取所有记录
        const allRecords = [];
        let pageToken;
        let hasMore = true;
        while (hasMore) {
            const result = await this.client.listRecords(appToken, tableId, { pageToken });
            if (result.success && result.data) {
                allRecords.push(...result.data.records);
                hasMore = result.data.hasMore;
                pageToken = result.data.pageToken;
            }
            else {
                return result;
            }
        }
        // 数据质量分析
        const analysis = {
            totalRecords: allRecords.length,
            fields: {},
            quality: {
                score: 100,
                issues: []
            }
        };
        if (allRecords.length === 0) {
            return {
                success: true,
                data: analysis
            };
        }
        // 分析每个字段
        const fieldValues = {};
        for (const record of allRecords) {
            for (const [field, value] of Object.entries(record.fields)) {
                if (!fieldValues[field]) {
                    fieldValues[field] = [];
                }
                fieldValues[field].push(value);
            }
        }
        for (const [field, values] of Object.entries(fieldValues)) {
            const emptyCount = values.filter(v => v === null || v === undefined || v === '').length;
            const uniqueValues = new Set(values.map(v => JSON.stringify(v)));
            analysis.fields[field] = {
                total: values.length,
                empty: emptyCount,
                emptyRate: (emptyCount / values.length * 100).toFixed(2) + '%',
                unique: uniqueValues.size,
                type: this.inferFieldType(values)
            };
            // 数据质量问题
            if (emptyCount > values.length * 0.5) {
                analysis.quality.issues.push({
                    field,
                    type: 'high_empty_rate',
                    message: `字段 "${field}" 空值率超过50%`
                });
                analysis.quality.score -= 10;
            }
        }
        analysis.quality.score = Math.max(0, analysis.quality.score);
        return {
            success: true,
            data: analysis
        };
    }
    /**
     * 推断字段类型
     */
    inferFieldType(values) {
        const nonEmpty = values.filter(v => v !== null && v !== undefined && v !== '');
        if (nonEmpty.length === 0)
            return 'unknown';
        const firstValue = nonEmpty[0];
        if (typeof firstValue === 'number')
            return 'number';
        if (typeof firstValue === 'boolean')
            return 'boolean';
        if (firstValue instanceof Array)
            return 'array';
        if (firstValue instanceof Object)
            return 'object';
        // 检查是否是日期
        if (/^\d{4}-\d{2}-\d{2}/.test(String(firstValue)))
            return 'date';
        return 'text';
    }
}
exports.FeishuBitableSkill = FeishuBitableSkill;
//# sourceMappingURL=skill.js.map