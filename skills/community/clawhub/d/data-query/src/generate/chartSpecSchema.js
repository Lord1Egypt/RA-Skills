/**
 * chartSpecSchema.js — CockpitMode 显式配置 Schema
 *
 * 定义 sqlMap 条目的标准格式（ChartSpec）
 * 替代原有的隐式 key 推断逻辑
 *
 * 使用方式：
 *   const schema = require('./chartSpecSchema.js');
 *   schema.validate(entry)    → 校验格式
 *   schema.normalize(entry)  → 兼容旧格式，转为标准格式
 *   schema.inferFromSql()    → 从 SQL 字符串推断 spec（兜底）
 *   schema.inferFromDomain() // 从业务域推断 spec（自动进化）
 */

const SPEC_TYPES = ['kpi', 'chart', 'sidebar', 'table'];
const CHART_TYPES = ['bar', 'line', 'pie', 'scatter', 'timeline', 'kanban', 'gantt', 'number'];
const KPI_TYPES = ['health_score', 'count', 'avg_percent', 'sum_money', 'ratio_percent'];
const WIDTHS = ['third', 'half', 'full'];
const SCOPES = ['project', 'global'];

// ============================================================
// 标准化入口（兼容旧格式）
// ============================================================

/**
 * 将任意 sqlMap 条目转为标准 ChartSpec 格式
 *  - 纯字符串: { sql: entry } → 走 inferFromSql 兜底
 *  - 对象但无 spec: { sql, type, ... } → 走 inferFromDomain 补全
 *  - 完整对象: { sql, type, spec: {...} } → 直接返回
 */
function normalize(entry) {
    if (!entry || typeof entry !== 'object') {
        throw new Error('sqlMap entry must be an object');
    }

    // 兼容纯字符串（旧格式）
    if (typeof entry.sql === 'string' && Object.keys(entry).length === 1) {
        return {
            ...entry,
            type: 'chart',
            title: entry.title || '',
            scope: 'project',
            spec: inferFromSql(entry.sql, entry.key || '')
        };
    }

    // 有 spec 但 type 未填
    if (!entry.type) {
        entry.type = entry.spec?.kpiType ? 'kpi' : 'chart';
    }

    // 有 type 但无 spec → 根据 domain + type 推断
    if (!entry.spec) {
        entry.spec = inferFromDomain(entry);
    }

    // spec 字段兜底
    const spec = entry.spec;
    if (!spec.chartType) {
        spec.chartType = inferChartTypeFromEntry(entry);
    }
    if (!spec.width) {
        spec.width = (spec.chartType === 'scatter' || spec.chartType === 'timeline') ? 'full' : 'half';
    }
    if (entry.type === 'kpi' && !spec.thresholds) {
        spec.thresholds = { green: 80, orange: 60 };
    }

    return entry;
}

// ============================================================
// 兜底推断：从 SQL 字符串内容推断 spec（旧格式兼容）
// ============================================================

function inferFromSql(sql, key = '') {
    const upperSql = sql.toUpperCase();
    const keyUpper = key.toUpperCase();

    // chartType 推断
    let chartType = 'bar';
    if (upperSql.includes('COUNT(') || upperSql.includes('SUM(') || upperSql.includes('AVG(')) {
        if (upperSql.includes('RATE') || upperSql.includes('PCT') || upperSql.includes('COMPLETE')) {
            chartType = 'line';
        } else if (upperSql.includes('PROBABILITY') || upperSql.includes('AFTERMATH')) {
            chartType = 'scatter';
        } else if (upperSql.includes('START_TIME') && upperSql.includes('END_TIME')) {
            chartType = 'timeline';
        }
    }
    if (keyUpper.includes('KANBAN')) chartType = 'kanban';
    if (keyUpper.includes('GANTT')) chartType = 'gantt';

    // kpiType 推断
    let kpiType = null;
    if (keyUpper.includes('HEALTH')) kpiType = 'health_score';
    else if (keyUpper.includes('RISK')) kpiType = 'count';
    else if (keyUpper.includes('PROGRESS') || keyUpper.includes('COMPLETE')) kpiType = 'avg_percent';

    const width = (chartType === 'scatter' || chartType === 'timeline') ? 'full' : 'half';

    return {
        chartType,
        kpiType,
        width,
        thresholds: kpiType ? { green: 80, orange: 60 } : null,
        xAxis: upperSql.includes('AFTERMATH') ? 'aftermath_level' : null,
        yAxis: upperSql.includes('PROBABILITY') ? 'probability_level' : null,
        valueField: 'count'
    };
}

// ============================================================
// 核心推断：从 entry 结构 + 业务域特征推断 spec
// ============================================================

function inferFromDomain(entry) {
    const { type, scope, key = '', sql = '' } = entry;
    const upperKey = key.toUpperCase();
    const upperSql = sql.toUpperCase();

    const spec = {};

    if (type === 'kpi') {
        // KPI 推断 kpiType
        spec.kpiType = upperKey.includes('HEALTH') ? 'health_score'
            : upperKey.includes('RISK') ? 'count'
            : upperKey.includes('PROGRESS') || upperKey.includes('COMPLETE') ? 'avg_percent'
            : upperKey.includes('COST') || upperKey.includes('SUM') ? 'sum_money'
            : 'count';

        // thresholds 默认值（可被 caller 覆盖）
        if (spec.kpiType === 'health_score') {
            spec.thresholds = { green: 80, orange: 60 };
        } else if (spec.kpiType === 'count') {
            spec.thresholds = { green: 3, orange: 8 };  // 风险项数
        } else {
            spec.thresholds = null;
        }
        spec.width = 'third';
        spec.valueField = inferValueField(sql);
        spec.unit = spec.kpiType === 'health_score' ? '分' : spec.kpiType === 'count' ? '项' : '%';
        return spec;
    }

    if (type === 'chart') {
        // chartType 推断
        spec.chartType = inferChartTypeFromEntry(entry);
        spec.width = (spec.chartType === 'scatter' || spec.chartType === 'timeline') ? 'full' : 'half';

        // 轴字段推断（热力图）
        if (spec.chartType === 'scatter') {
            spec.xAxis = upperSql.includes('AFTERMATH') ? 'aftermath_level' : null;
            spec.yAxis = upperSql.includes('PROBABILITY') ? 'probability_level' : null;
            spec.valueField = 'count';
        }

        // 时间线
        if (spec.chartType === 'timeline') {
            spec.startField = 'plan_start_time';
            spec.endField = 'plan_end_time';
            spec.labelField = 'task_name';
        }

        // 看板
        if (spec.chartType === 'kanban') {
            spec.kanbanColumns = [
                { status: 'EDIT', title: '待开始', color: '#999' },
                { status: 'APPROVAL', title: '审批中', color: '#faad14' },
                { status: 'CONFIRM', title: '进行中', color: '#1890ff' },
                { status: 'RELEASE', title: '已发布', color: '#52c41a' }
            ];
        }

        return spec;
    }

    return spec;
}

// ============================================================
// 辅助推断函数
// ============================================================

function inferChartTypeFromEntry(entry) {
    const { key = '', sql = '' } = entry;
    const upperKey = key.toUpperCase();
    const upperSql = sql.toUpperCase();

    if (upperKey.includes('KANBAN')) return 'kanban';
    if (upperKey.includes('GANTT')) return 'gantt';
    if (upperKey.includes('MILESTONE') || upperKey.includes('时间线')) return 'timeline';
    if (upperSql.includes('PROBABILITY') && upperSql.includes('AFTERMATH')) return 'scatter';
    if (upperKey.includes('TREND') || upperKey.includes('趋势')) return 'line';
    if (upperKey.includes('PIE') || upperKey.includes('占比') || upperKey.includes('分布')) return 'pie';
    if (upperSql.includes('COUNT(') || upperSql.includes('SUM(')) {
        if (upperSql.includes('RATE') || upperSql.includes('PCT')) return 'line';
        return 'bar';
    }
    return 'bar';
}

function inferValueField(sql) {
    const upper = sql.toUpperCase();
    // 从 SELECT 子句中提取别名或字段名
    const m = sql.match(/SELECT\s+(.*?)\s+FROM/i);
    if (!m) return 'value';
    const selectPart = m[1];
    const asMatch = selectPart.match(/\bAS\b\s+(\w+)/i);
    if (asMatch) return asMatch[1].toLowerCase();
    const lastField = selectPart.split(',').pop().trim().replace(/^\w+\./, '').trim();
    return lastField.toLowerCase() || 'value';
}

// ============================================================
// Schema 校验（debug / 未来扩展用）
// ============================================================

function validate(entry) {
    const errors = [];

    if (!entry || typeof entry !== 'object') return { valid: false, errors: ['entry must be an object'] };
    if (!entry.sql || typeof entry.sql !== 'string') errors.push('entry.sql is required and must be a string');
    if (entry.type && !SPEC_TYPES.includes(entry.type)) errors.push(`entry.type must be one of: ${SPEC_TYPES.join(', ')}`);
    if (entry.scope && !SCOPES.includes(entry.scope)) errors.push(`entry.scope must be one of: ${SCOPES.join(', ')}`);
    if (entry.spec?.chartType && !CHART_TYPES.includes(entry.spec.chartType)) {
        errors.push(`spec.chartType must be one of: ${CHART_TYPES.join(', ')}`);
    }
    if (entry.spec?.kpiType && !KPI_TYPES.includes(entry.spec.kpiType)) {
        errors.push(`spec.kpiType must be one of: ${KPI_TYPES.join(', ')}`);
    }
    if (entry.spec?.width && !WIDTHS.includes(entry.spec.width)) {
        errors.push(`spec.width must be one of: ${WIDTHS.join(', ')}`);
    }

    return { valid: errors.length === 0, errors };
}

module.exports = {
    normalize,
    inferFromSql,
    inferFromDomain,
    inferChartTypeFromEntry,
    validate,
    SPEC_TYPES,
    CHART_TYPES,
    KPI_TYPES,
    WIDTHS,
    SCOPES
};
