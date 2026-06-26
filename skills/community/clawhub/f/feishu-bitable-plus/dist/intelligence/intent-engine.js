"use strict";
/**
 * 意图识别引擎
 * Intent Recognition Engine
 * 基于规则 + 模式匹配的轻量级NLP
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.IntentEngine = void 0;
class IntentEngine {
    patterns;
    constructor() {
        this.patterns = this.initializePatterns();
    }
    /**
     * 初始化识别模式
     * 注意：按优先级排序，更具体的模式在前
     */
    initializePatterns() {
        return [
            // ========== 批量操作（带明确关键词）==========
            {
                regex: /(?:批量|大量|多[个条])[：:]?(?:添加|创建|新增)[了入]?\s*(?:到)?\s*["']?([^"']*?)["']?(?:表|表格)?/i,
                intent: 'BATCH_CREATE',
                priority: 10,
                extractors: [
                    (match) => ({ tableName: match[1]?.trim() })
                ]
            },
            {
                regex: /(?:批量|大量|多[个条])[：:]?(?:更新|修改)[了改]?\s*["']?([^"']*?)["']?(?:表|表格)?/i,
                intent: 'BATCH_UPDATE',
                priority: 10,
                extractors: [
                    (match) => ({ tableName: match[1]?.trim() })
                ]
            },
            {
                regex: /(?:批量|大量|多[个条])[：:]?(?:删除|移除)[了除]?\s*["']?([^"']*?)["']?(?:表|表格)?/i,
                intent: 'BATCH_DELETE',
                priority: 10,
                extractors: [
                    (match) => ({ tableName: match[1]?.trim() })
                ]
            },
            // ========== 跨表同步 ==========
            {
                regex: /(?:同步|复制|转移|导入)[了到]?\s*(?:从)?\s*["']?([^"']*?)["']?(?:表|表格)?(?:到|至|进)?\s*["']?([^"']*?)["']?(?:表|表格)?/i,
                intent: 'SYNC_TABLES',
                priority: 10,
                extractors: [
                    (match) => ({
                        tableName: match[1]?.trim(),
                        targetTable: match[2]?.trim()
                    })
                ]
            },
            // ========== 报表生成（在数据分析之前）==========
            {
                regex: /(?:生成|创建|导出)[了出]?\s*(?:一个|一份)?(?:报表|报告)(?:关于|针对)?\s*["']?([^"']*?)["']?(?:的)?(?:统计|分析)?(?:报表|报告)?/i,
                intent: 'GENERATE_REPORT',
                priority: 9,
                extractors: [
                    (match) => ({
                        tableName: match[1]?.trim(),
                        reportType: this.extractReportType(match[0])
                    })
                ]
            },
            // ========== 单条记录操作 ==========
            {
                regex: /(?:获取|查看|显示|打开)[了出]?\s*["']?([^"']*?)["']?(?:表|表格)?(?:中)?的?(?:记录|行)?\s*([a-zA-Z0-9]+)/i,
                intent: 'GET_RECORD',
                priority: 8,
                extractors: [
                    (match) => ({
                        tableName: match[1]?.trim(),
                        recordId: match[2]?.trim()
                    })
                ]
            },
            {
                regex: /(?:更新|修改|编辑|更改)[了改]?\s*["']?([^"']*?)["']?(?:表|表格)?(?:中)?(?:的|ID为|编号为)?\s*([a-zA-Z0-9]+)/i,
                intent: 'UPDATE_RECORD',
                priority: 8,
                extractors: [
                    (match, text) => ({
                        tableName: match[1]?.trim(),
                        recordId: match[2]?.trim(),
                        data: this.extractDataFields(text)
                    })
                ]
            },
            {
                regex: /(?:删除|移除|去掉)[了除]?\s*["']?([^"']*?)["']?(?:表|表格)?(?:中)?(?:的|ID为|编号为)?\s*([a-zA-Z0-9]+)/i,
                intent: 'DELETE_RECORD',
                priority: 8,
                extractors: [
                    (match) => ({
                        tableName: match[1]?.trim(),
                        recordId: match[2]?.trim()
                    })
                ]
            },
            // ========== 创建记录（在批量之后）==========
            {
                regex: /(?:在|往)?\s*["']?([^"']*?)["']?(?:表|表格)?(?:中)?(?:添加|创建|新增|插入)[了入]?\s*(?:一条|一个)?(?:记录|数据|行)/i,
                intent: 'CREATE_RECORD',
                priority: 7,
                extractors: [
                    (match, text) => ({
                        tableName: match[1]?.trim(),
                        data: this.extractDataFields(text)
                    })
                ]
            },
            // ========== 带条件的查询 ==========
            {
                regex: /(?:查找|搜索|查询)[了出]?\s*["']?([^"']*?)["']?(?:表|表格)?(?:中)?(?:的|满足|符合)?(.+?)(?:的)?(?:记录|数据|行)/i,
                intent: 'LIST_RECORDS',
                priority: 6,
                extractors: [
                    (match) => ({
                        tableName: match[1]?.trim(),
                        conditions: this.extractConditions(match[2])
                    })
                ]
            },
            // ========== 简单查询 ==========
            {
                regex: /(?:列出|查找|搜索|查询|显示|查看|获取|找一下?)[了出]?\s*["']?([^"']*?)["']?(?:表|表格)?(?:中)?的?(?:所有|全部)?(?:记录|数据|行)?/i,
                intent: 'LIST_RECORDS',
                priority: 5,
                extractors: [
                    (match) => ({ tableName: match[1]?.trim() })
                ]
            },
            // ========== 数据分析 ==========
            {
                regex: /(?:分析|统计|计算|汇总)[了计]?\s*["']?([^"']*?)["']?(?:表|表格)?(?:的|中)?(?:数据|信息|情况)?/i,
                intent: 'ANALYZE_DATA',
                priority: 4,
                extractors: [
                    (match) => ({ tableName: match[1]?.trim() })
                ]
            },
        ];
    }
    /**
     * 解析用户输入
     */
    parse(input) {
        const text = input.trim();
        let bestMatch = null;
        let highestPriority = -1;
        // 遍历所有模式，找到优先级最高的匹配
        for (const pattern of this.patterns) {
            const match = text.match(pattern.regex);
            if (match) {
                const priority = pattern.priority || 0;
                if (priority > highestPriority) {
                    highestPriority = priority;
                    bestMatch = { pattern, match };
                }
            }
        }
        if (bestMatch) {
            const entities = this.extractEntities(bestMatch.match, text, bestMatch.pattern.extractors);
            return {
                intent: bestMatch.pattern.intent,
                confidence: this.calculateConfidence(bestMatch.match, text),
                entities,
                originalText: text
            };
        }
        // 无法识别
        return {
            intent: 'UNKNOWN',
            confidence: 0,
            entities: { originalText: text },
            originalText: text
        };
    }
    /**
     * 提取实体
     */
    extractEntities(match, text, extractors) {
        const entities = { originalText: text };
        for (const extractor of extractors) {
            const extracted = extractor(match, text);
            Object.assign(entities, extracted);
        }
        // 清理表名中的"表"字后缀
        if (entities.tableName) {
            entities.tableName = this.cleanTableName(entities.tableName);
        }
        if (entities.targetTable) {
            entities.targetTable = this.cleanTableName(entities.targetTable);
        }
        return entities;
    }
    /**
     * 清理表名，移除"表"、"表格"等后缀
     */
    cleanTableName(name) {
        if (!name)
            return name;
        // 移除"表"或"表格"后缀（如果在末尾）
        return name.replace(/(表|表格)$/, '').trim() || name.trim();
    }
    /**
     * 从文本中提取条件
     */
    extractConditions(conditionText) {
        const conditions = [];
        const text = conditionText?.trim();
        if (!text)
            return conditions;
        // 解析常见条件模式
        const patterns = [
            // "X等于/是/为Y"
            { regex: /([^\s]+)\s*(?:等于|是|为)\s*["']?([^"']+?)["']?(?:\s+|$|的|的?记录)/i, operator: 'equals' },
            // "X不等于/不是"
            { regex: /([^\s]+)\s*(?:不等于|不是|不为)\s*["']?([^"']+?)["']?(?:\s+|$|的|的?记录)/i, operator: 'notEquals' },
            // "X包含"
            { regex: /([^\s]+)\s*包含\s*["']?([^"']+?)["']?(?:\s+|$|的|的?记录)/i, operator: 'contains' },
            // "X大于"
            { regex: /([^\s]+)\s*大于\s*["']?([^"']+?)["']?(?:\s+|$|的|的?记录)/i, operator: 'greaterThan' },
            // "X小于"
            { regex: /([^\s]+)\s*小于\s*["']?([^"']+?)["']?(?:\s+|$|的|的?记录)/i, operator: 'lessThan' },
            // "X为空/没有"
            { regex: /([^\s]+)\s*(?:为空|没有|未填写)/i, operator: 'isEmpty' },
            // "X不为空/有"
            { regex: /([^\s]+)\s*(?:不为空|有|已填写)/i, operator: 'isNotEmpty' }
        ];
        for (const pattern of patterns) {
            const match = text.match(pattern.regex);
            if (match) {
                conditions.push({
                    field: match[1]?.trim(),
                    operator: pattern.operator,
                    value: match[2]?.trim()
                });
            }
        }
        return conditions;
    }
    /**
     * 从文本中提取数据字段
     */
    extractDataFields(text) {
        const data = {};
        // 匹配 "字段名 是/为/等于 值" 模式
        const fieldPattern = /["']?([^"']+?)["']?\s*(?:是|为|等于)\s*["']?([^"']+?)["']?(?:[,，;；]|\s*$)/gi;
        let match;
        while ((match = fieldPattern.exec(text)) !== null) {
            const fieldName = match[1]?.trim();
            const value = match[2]?.trim();
            if (fieldName && value) {
                data[fieldName] = this.parseValue(value);
            }
        }
        return data;
    }
    /**
     * 解析值类型
     */
    parseValue(value) {
        // 尝试解析数字
        if (/^-?\d+$/.test(value)) {
            return parseInt(value, 10);
        }
        if (/^-?\d+\.\d+$/.test(value)) {
            return parseFloat(value);
        }
        // 尝试解析布尔值
        if (value === 'true' || value === '是' || value === '真') {
            return true;
        }
        if (value === 'false' || value === '否' || value === '假') {
            return false;
        }
        // 默认字符串
        return value;
    }
    /**
     * 提取报表类型
     */
    extractReportType(text) {
        if (/统计|汇总|总计|sum|count/i.test(text))
            return 'summary';
        if (/趋势|变化|趋势图|折线图/i.test(text))
            return 'trend';
        if (/对比|比较|vs/i.test(text))
            return 'comparison';
        if (/分布|占比|饼图/i.test(text))
            return 'distribution';
        return 'general';
    }
    /**
     * 计算置信度
     */
    calculateConfidence(match, text) {
        // 基础置信度
        let confidence = 0.7;
        // 匹配长度越长，置信度越高
        const matchLength = match[0]?.length || 0;
        confidence += Math.min(matchLength / text.length * 0.2, 0.2);
        // 包含明确的动作词，增加置信度
        const actionWords = /(列出|查找|搜索|查询|添加|创建|更新|修改|删除|同步|生成|分析)/;
        if (actionWords.test(text)) {
            confidence += 0.1;
        }
        return Math.min(confidence, 1.0);
    }
    /**
     * 将条件转换为飞书filter表达式
     */
    buildFilterExpression(conditions) {
        if (!conditions || conditions.length === 0) {
            return '';
        }
        const parts = conditions.map(cond => {
            const { field, operator, value } = cond;
            switch (operator) {
                case 'equals':
                    return `CurrentValue.[${field}] = "${value}"`;
                case 'notEquals':
                    return `CurrentValue.[${field}] != "${value}"`;
                case 'contains':
                    return `FIND("${value}", CurrentValue.[${field}]) > 0`;
                case 'notContains':
                    return `FIND("${value}", CurrentValue.[${field}]) = 0`;
                case 'greaterThan':
                    return `CurrentValue.[${field}] > ${value}`;
                case 'lessThan':
                    return `CurrentValue.[${field}] < ${value}`;
                case 'greaterThanOrEqual':
                    return `CurrentValue.[${field}] >= ${value}`;
                case 'lessThanOrEqual':
                    return `CurrentValue.[${field}] <= ${value}`;
                case 'isEmpty':
                    return `ISBLANK(CurrentValue.[${field}])`;
                case 'isNotEmpty':
                    return `NOT(ISBLANK(CurrentValue.[${field}]))`;
                default:
                    return '';
            }
        }).filter(Boolean);
        if (parts.length === 1) {
            return parts[0];
        }
        return parts.join(' AND ');
    }
}
exports.IntentEngine = IntentEngine;
//# sourceMappingURL=intent-engine.js.map