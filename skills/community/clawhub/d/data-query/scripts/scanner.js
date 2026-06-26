/**
 * knowledgeBaseScanner.js — 知识库扫描引擎
 *
 * 职责：
 * 1. 扫描 tables.json 定位业务表
 * 2. 读取表字段结构
 * 3. 根据业务域描述推断 SQL + spec
 *
 * 自动进化入口：
 *   const { resolveDomain } = require('{skillDir}/scripts/scanner.js');
 *   const entry = await resolveDomain('任务延期情况', { projectId: 61 });
 */

const fs = require('fs');
const path = require('path');
const { createDialect } = require('../src/core/dialect.js');
const config = require('../src/core/config.js');

// ============================================================
// 知识库路径（按数据库类型分离）
//
// 目录结构：
//   knowledge/
//   ├── mysql/          ← MySQL 表结构
//   │   ├── tables.json
//   │   └── field_mapping.json
//   ├── dm/             ← DaMeng 表结构
//   │   ├── tables.json
//   │   └── field_mapping.json
//   ├── oracle/          ← Oracle 表结构
//   │   ├── tables.json
//   │   └── field_mapping.json
//   └── shared/          ← 跨库共用
//       ├── kpi_formulas.json
//       ├── kpi_spec_schema.json
//       ├── sql_generation_rules.md
//       └── evolved_domains.json
// ============================================================

const SKILL_DIR = path.resolve(__dirname, '..');
const KNOWLEDGE_BASE = path.join(SKILL_DIR, 'knowledge');
const SHARED_DIR = path.join(KNOWLEDGE_BASE, 'shared');

/**
 * 根据 dbType 获取知识库子目录路径
 * @param {string} dbType - 数据库类型：mysql | dm | oracle
 */
function getDbKnowledgeDir(dbType) {
    return path.join(KNOWLEDGE_BASE, dbType || config.db.type);
}

/** 当前配置的 dbType 对应的知识库子目录 */
const KNOWLEDGE_DIR = getDbKnowledgeDir(config.db.type);

/** 当前数据库类型的 tables.json */
const TABLES_PATH = path.join(KNOWLEDGE_DIR, 'tables.json');

/** 当前数据库类型的 field_mapping.json */
const FIELD_MAPPING_PATH = path.join(KNOWLEDGE_DIR, 'field_mapping.json');

/** 跨库共用的 evolved_domains.json */
const EVOLVED_DOMAINS_PATH = path.join(SHARED_DIR, 'evolved_domains.json');

// ============================================================
// 知识库缓存（懒加载）
// ============================================================

let _tables = null;
let _fieldMapping = null;
let _evolvedDomains = null;

function loadTables() {
    if (_tables) return _tables;
    try {
        const raw = JSON.parse(fs.readFileSync(TABLES_PATH, 'utf-8'));
        // 归一化：所有 table key 转为大写（DM/Oracle 大写，MySQL 小写，统一大写查询）
        _tables = {};
        for (const [k, v] of Object.entries(raw)) {
            _tables[k.toUpperCase()] = v;
        }
    } catch (e) {
        _tables = {};
    }
    return _tables;
}

function loadFieldMapping() {
    if (_fieldMapping) return _fieldMapping;
    try {
        _fieldMapping = JSON.parse(fs.readFileSync(FIELD_MAPPING_PATH, 'utf-8'));
    } catch (e) {
        _fieldMapping = { '字段→中文名': {}, '枚举值映射': {} };
    }
    return _fieldMapping;
}

/**
 * 加载 auto-evolution 沉淀的 domain 条目（优先于 DOMAIN_TABLE_MAP）
 * @returns {{ [domainKey: string]: entry }}
 */
function loadEvolvedDomains() {
    if (_evolvedDomains !== null) return _evolvedDomains;
    try {
        const raw = fs.readFileSync(EVOLVED_DOMAINS_PATH, 'utf-8');
        _evolvedDomains = JSON.parse(raw);
    } catch (e) {
        _evolvedDomains = {};
    }
    return _evolvedDomains;
}

// ============================================================
// 核心表注册表（域 → 表名）
// ============================================================

const DOMAIN_TABLE_MAP = {
    // 任务域
    task:         { table: 'WSD_PLAN_TASK',      comment: '任务' },
    tasks:        { table: 'WSD_PLAN_TASK',      comment: '任务' },
    任务:         { table: 'WSD_PLAN_TASK',      comment: '任务' },
    延期:         { table: 'WSD_PLAN_TASK',      comment: '任务' },
    延期任务:     { table: 'WSD_PLAN_TASK',      comment: '任务' },
    taskDelay:    { table: 'WSD_PLAN_TASK',      comment: '任务' },
    taskDelay2:   { table: 'WSD_PLAN_TASK',      comment: '任务' },

    // 项目域（仅全局，WSD_PLAN_PROJECT 主键是 ID 而非 PROJECT_ID，不适合 project scope）
    project:      { table: 'WSD_PLAN_PROJECT',  comment: '项目', scope: 'global' },
    projects:      { table: 'WSD_PLAN_PROJECT',  comment: '项目', scope: 'global' },
    项目:         { table: 'WSD_PLAN_PROJECT',   comment: '项目', scope: 'global' },

    // 总体/汇总/全局域 → 聚合查询（不加 ID 条件）
    总体:         { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    总体进度:     { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    汇总:         { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    全局:         { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    整体:         { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    overview:     { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    overall:      { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    项目总数:      { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    项目进度:      { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },
    项目列表:      { table: 'WSD_PLAN_PROJECT',  comment: '项目（聚合）', scope: 'global' },

    // 风险域
    risk:         { table: 'WSD_RISK_REGISTER', comment: '风险' },
    risks:        { table: 'WSD_RISK_REGISTER', comment: '风险' },
    风险:         { table: 'WSD_RISK_REGISTER', comment: '风险' },
    风险统计:     { table: 'WSD_RISK_REGISTER', comment: '风险', scope: 'global' },

    // 资源域
    resource:     { table: 'WSD_PLAN_TASKRSRC', comment: '资源分配' },
    resources:    { table: 'WSD_PLAN_TASKRSRC', comment: '资源分配' },
    资源:         { table: 'WSD_PLAN_TASKRSRC', comment: '资源分配' },
    资源负载:     { table: 'WSD_PLAN_TASKRSRC', comment: '资源分配' },
    resourceLoad: { table: 'WSD_PLAN_TASKRSRC', comment: '资源分配' },

    // 会议域
    meeting:      { table: 'WSD_COMU_MEETING',  comment: '会议' },
    会议:         { table: 'WSD_COMU_MEETING',  comment: '会议' },

    // 交付物域
    deliverable:  { table: 'WSD_PLAN_DELVASSIGN', comment: '交付物' },
    交付物:       { table: 'WSD_PLAN_DELVASSIGN', comment: '交付物' },

    // 里程碑（不是独立表，是 task_type IN (2,3) 的任务视图）
    milestone:    { table: 'WSD_PLAN_TASK',      comment: '里程碑', filter: "TASK_TYPE IN (2,3)" },
    里程碑:       { table: 'WSD_PLAN_TASK',      comment: '里程碑', filter: "TASK_TYPE IN (2,3)" },
};

// ============================================================
// 1. 搜索表（按名称/注释/字段）
// ============================================================

/**
 * 搜索知识库中匹配的表
 * @param {string} keyword - 搜索关键词（支持表名/注释/字段名）
 * @returns {Array<{ name, comment, module, matchedField? }>}
 */
function searchTables(keyword) {
    const tables = loadTables();
    const results = [];
    const kw = keyword.toLowerCase().trim();

    for (const [name, meta] of Object.entries(tables)) {
        if (!name.startsWith('WSD_')) continue;

        let matchedField = null;

        // 表名匹配
        if (name.toLowerCase().includes(kw)) {
            results.push({ name, comment: meta.comment || '', module: meta.module || '', matchedField: null });
            continue;
        }

        // 表注释匹配
        if ((meta.comment || '').toLowerCase().includes(kw)) {
            results.push({ name, comment: meta.comment || '', module: meta.module || '', matchedField: null });
            continue;
        }

        // 列名/列注释匹配
        if (meta.columns) {
            for (const col of meta.columns) {
                if ((col.name || '').toLowerCase().includes(kw) ||
                    (col.comment || '').toLowerCase().includes(kw)) {
                    matchedField = { name: col.name, type: col.type, comment: col.comment };
                    if (!results.find(r => r.name === name)) {
                        results.push({ name, comment: meta.comment || '', module: meta.module || '', matchedField });
                    }
                    break;
                }
            }
        }
    }

    return results;
}

// ============================================================
// 2. 获取表结构
// ============================================================

/**
 * 获取表的完整字段结构
 * @param {string} tableName
 * @returns {{ tableName, comment, columns: [{ name, type, comment, nullable, key }] }}
 */
function getTableSchema(tableName) {
    const tables = loadTables();
    const meta = tables[tableName.toUpperCase()];
    if (!meta || !meta.columns) {
        return { tableName, comment: '', columns: [] };
    }
    return {
        tableName: meta.name || tableName,
        comment: meta.comment || '',
        module: meta.module || '',
        columns: meta.columns.map(c => ({
            name: c.name,
            type: c.type,
            comment: c.comment || '',
            nullable: c.nullable === 'YES',
            primaryKey: c.key === 'PRI'
        }))
    };
}

// ============================================================
// 辅助：判断表是否有 DEL 字段（从知识库动态推断，不再硬编码）
// ============================================================

/**
 * 检查指定表在知识库中是否声明了 DEL 字段
 * @param {string} tableName
 * @returns {boolean}
 */
function hasDelField(tableName) {
    const schema = getTableSchema(tableName.toUpperCase());
    if (!schema.columns.length) {
        // 知识库无数据，默认不加 DEL（保守策略，避免误加）
        return false;
    }
    return schema.columns.some(c => c.name.toUpperCase() === 'DEL');
}

// ============================================================
// 3. 分类业务域
// ============================================================

/**
 * 根据域描述字符串分类
 * @param {string} domain - 用户描述的业务域（如"任务延期"、"资源负载"）
 * @returns {{ domain, category, table, filter?, suggestion? }}
 */
function classifyDomain(domain) {
    const d = domain.toLowerCase().trim();

    // 精确匹配 DOMAIN_TABLE_MAP
    if (DOMAIN_TABLE_MAP[d]) {
        return { domain, ...DOMAIN_TABLE_MAP[d] };
    }
    // 模糊匹配
    for (const [key, mapping] of Object.entries(DOMAIN_TABLE_MAP)) {
        if (d.includes(key) || key.includes(d)) {
            return { domain, ...mapping };
        }
    }

    // 兜底：搜知识库
    const searchResults = searchTables(domain);
    if (searchResults.length > 0) {
        const top = searchResults[0];
        return {
            domain,
            table: top.name,
            comment: top.comment,
            module: top.module,
            matchedField: top.matchedField,
            suggestion: `通过关键词"${domain}"匹配到表 ${top.name}`
        };
    }

    return { domain, table: null, comment: '', suggestion: `未找到匹配表，建议确认业务域名称` };
}

// ============================================================
// 4. 推断 spec（根据域 + 表结构）
// ============================================================

/**
 * 根据域类型 + 表结构推断 ChartSpec
 * @param {string} domain - 业务域描述
 * @param {{ table, comment, filter? }} domainInfo - 分类结果
 * @param {{ projectId? }} context - 上下文
 * @returns {{ type, scope, spec }}
 */
function inferSpecFromDomain(domain, domainInfo, context = {}) {
    const d = domain.toLowerCase();
    const { table, filter } = domainInfo;
    if (!table) {
        return { type: 'chart', scope: 'project', spec: {} };
    }

    // ── KPI 类型推断 ──────────────────────────────────────────

    // ⭐ 总体/汇总/全局类需求（最高优先级，最先匹配）
    // 不管有没有 projectId，只要语义是"总体"，scope 就必须是 'global'
    if (d.includes('总体') || d.includes('汇总') || d.includes('全局') || d.includes('整体') || d.includes('overview') || d.includes('overall')) {
        // 判断是 KPI 类还是 chart 类
        if (d.includes('进度') || d.includes('完成率') || d.includes('progress') || d.includes('rate')) {
            return {
                type: 'kpi',
                scope: 'global',   // 总体进度永远是 global，不受 projectId 影响
                spec: {
                    kpiType: 'avg_percent',
                    valueField: 'avg_complete_pct',
                    unit: '%',
                    thresholds: { green: 80, orange: 60 },
                    width: 'third'
                }
            };
        }
        // 其他总体类 → 默认 bar chart
        return {
            type: 'chart',
            scope: 'global',
            spec: {
                chartType: 'bar',
                width: 'full'
            }
        };
    }

    if (d.includes('健康度') || d.includes('health')) {
        return {
            type: 'kpi',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                kpiType: 'health_score',
                valueField: 'health_score',
                unit: '分',
                thresholds: { green: 80, orange: 60 },
                width: 'third'
            }
        };
    }
    if (d.includes('风险数') || d.includes('风险敞口') || (d.includes('风险') && d.includes('统计'))) {
        return {
            type: 'kpi',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                kpiType: 'count',
                valueField: 'count',
                unit: '项',
                thresholds: { green: 3, orange: 8 },
                width: 'third'
            }
        };
    }
    if ((d.includes('完成率') || d.includes('进度') || d.includes('progress')) && d.includes('指标')) {
        return {
            type: 'kpi',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                kpiType: 'avg_percent',
                valueField: 'complete_pct',
                unit: '%',
                thresholds: { green: 80, orange: 60 },
                width: 'third'
            }
        };
    }

    // ── chart 类型推断 ────────────────────────────────────────
    if (d.includes('热力') || d.includes('四象限') || (d.includes('风险') && (d.includes('分布') || d.includes('概率')))) {
        return {
            type: 'chart',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                chartType: 'scatter',
                xAxis: 'aftermath_level',
                yAxis: 'probability_level',
                valueField: 'count',
                width: 'full'
            }
        };
    }
    if (d.includes('时间线') || d.includes('timeline') || d.includes('里程碑') || d.includes('milestone')) {
        return {
            type: 'chart',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                chartType: 'timeline',
                startField: 'plan_start_time',
                endField: 'plan_end_time',
                labelField: 'task_name',
                width: 'full'
            }
        };
    }
    if (d.includes('看板') || d.includes('kanban')) {
        return {
            type: 'chart',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                chartType: 'kanban',
                kanbanColumns: [
                    { status: 'EDIT',     title: '待开始', color: '#999' },
                    { status: 'APPROVAL', title: '审批中', color: '#faad14' },
                    { status: 'CONFIRM',  title: '进行中', color: '#1890ff' },
                    { status: 'RELEASE',  title: '已发布', color: '#52c41a' }
                ]
            }
        };
    }
    if (d.includes('甘特') || d.includes('gantt')) {
        return {
            type: 'chart',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                chartType: 'gantt'
            }
        };
    }
    if (d.includes('资源负载') || d.includes('负载')) {
        return {
            type: 'chart',
            scope: 'global',
            spec: {
                chartType: 'bar',
                xAxis: 'org_name',
                yAxis: 'load_rate',
                valueField: 'plan_days',
                width: 'full'
            }
        };
    }
    if (d.includes('占比') || d.includes('pie') || d.includes('分布')) {
        return {
            type: 'chart',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                chartType: 'pie',
                labelField: 'label',
                valueField: 'value',
                width: 'half'
            }
        };
    }
    if (d.includes('趋势') || d.includes('trend') || d.includes('走势')) {
        return {
            type: 'chart',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                chartType: 'line',
                xAxis: 'month',
                yAxis: 'value',
                valueField: 'value',
                width: 'full'
            }
        };
    }
    if (d.includes('会议') || d.includes('meeting')) {
        return {
            type: 'chart',
            scope: context.projectId ? 'project' : 'global',
            spec: {
                chartType: 'timeline',
                startField: 'meeting_time',
                endField: 'plan_end_time',
                labelField: 'title',
                width: 'full'
            }
        };
    }

    // 默认：bar chart
    return {
        type: 'chart',
        scope: context.projectId ? 'project' : 'global',
        spec: {
            chartType: 'bar',
            width: 'half'
        }
    };
}

// ============================================================
// 5. 生成 SQL（根据域 + 表结构）
// ============================================================

/**
 * 根据域描述推断 SELECT 字段列表
 * @param {string} domain
 * @param {{ table, comment, filter? }} domainInfo
 * @param {{ projectId? }} context
 * @returns {string[]} 字段名列表
 */
function inferSelectFields(domain, domainInfo, context = {}) {
    const { table, filter } = domainInfo;
    if (!table) return ['*'];

    const d = domain.toLowerCase();

    // 任务表
    if (table === 'WSD_PLAN_TASK') {
        if (d.includes('延期')) {
            return ['t.ID', 't.TASK_NAME', 't.STATUS', 't.FEEDBACK_STATUS', 't.PLAN_END_TIME', 't.ACT_END_TIME', 't.COMPLETE_PCT', 'u.USER_NAME AS assignee_name', 'o.ORG_NAME'];
        }
        if (d.includes('里程碑') || filter?.includes('task_type')) {
            return ['t.ID', 't.TASK_CODE', 't.TASK_NAME', 't.TASK_TYPE', 't.PLAN_START_TIME', 't.PLAN_END_TIME', 't.ACT_END_TIME', 't.FEEDBACK_STATUS', 'u.USER_NAME', 'o.ORG_NAME'];
        }
        if (d.includes('看板')) {
            return ['t.ID', 't.TASK_NAME', 't.STATUS', 't.FEEDBACK_STATUS', 't.COMPLETE_PCT', 't.PLAN_END_TIME', 'u.USER_NAME AS assignee_name', 't.CRITICAL'];
        }
        return ['t.ID', 't.TASK_NAME', 't.STATUS', 't.FEEDBACK_STATUS', 't.COMPLETE_PCT', 't.PLAN_START_TIME', 't.PLAN_END_TIME', 'u.USER_NAME'];
    }

    // 项目表
    if (table === 'WSD_PLAN_PROJECT') {
        // 总体/汇总/全局类 → 聚合字段
        if (d.includes('总体') || d.includes('汇总') || d.includes('全局') || d.includes('整体') || d.includes('overview') || d.includes('overall')) {
            return [
                'COUNT(*) AS project_count',
                'AVG(p.COMPLETE_PCT) AS avg_complete_pct',
                'SUM(p.PLAN_SUM) AS total_plan_sum',
                'SUM(p.ACT_SUM) AS total_act_sum',
                'MAX(p.NAME) AS sample_project_name'
            ];
        }
        if (d.includes('列表')) {
            return ['p.ID', 'p.NAME', 'p.CODE', 'p.STATUS', 'p.COMPLETE_PCT', 'p.PLAN_START_TIME', 'p.PLAN_END_TIME', 'o.ORG_NAME AS org_name', 'u.USER_NAME AS pm_name'];
        }
        return ['p.ID', 'p.NAME', 'p.COMPLETE_PCT', 'p.PLAN_SUM', 'p.ACT_SUM', 'p.PLAN_RATE', 'p.ACT_RATE'];
    }

    // 风险表
    if (table === 'WSD_RISK_REGISTER') {
        if (d.includes('热力') || d.includes('四象限')) {
            return ['PROBABILITY_LEVEL AS prob', 'AFTERMATH_LEVEL AS impact', 'COUNT(*) AS count'];
        }
        return ['r.ID', 'r.RISK_CODE', 'r.RISK_NAME', 'r.RISK_STATUS', 'r.PROBABILITY_LEVEL', 'r.AFTERMATH_LEVEL', 'r.RISK_LEVEL', 'u.USER_NAME'];
    }

    // 资源表
    if (table === 'WSD_PLAN_TASKRSRC') {
        return ['r.ORG_ID', 'o.ORG_NAME AS org_name', 'SUM(t.BUDGET_QTY)/8 AS plan_days', 'COUNT(DISTINCT r.ID) AS resource_count', 'SUM(t.BUDGET_QTY)/8 / (COUNT(DISTINCT r.ID) * 30) * 100 AS load_rate'];
    }

    // 会议表
    if (table === 'WSD_COMU_MEETING') {
        return ['m.ID', 'm.TITLE', 'm.MEETING_TIME', 'm.STATUS', 'u.USER_NAME AS duty_name', 'ma.ACTION_NAME', 'ma.PLAN_END_TIME', 'ma.COMPLETED'];
    }

    // 交付物表
    if (table === 'WSD_PLAN_DELVASSIGN') {
        return ['d.ID', 'd.DELV_TITLE', 'd.DELV_CODE', 'd.DELV_STATUS', 'd.PLAN_END_TIME', 'd.COMPLETE_TIME', 'u.USER_NAME'];
    }

    // 默认
    return ['*'];
}

/**
 * 构建完整的 SQL 字符串
 * @param {string} domain
 * @param {{ table, filter? }} domainInfo
 * @param {{ projectId? }} context
 * @returns {string}
 */
function buildSQL(domain, domainInfo, context = {}) {
    const { table, filter } = domainInfo;
    if (!table) return 'SELECT NULL WHERE 1=0';  // 空结果

    const fields = inferSelectFields(domain, domainInfo, context);
    const hasJoin = fields.some(f => f.includes('.'));
    const alias = { WSD_PLAN_TASK: 't', WSD_PLAN_PROJECT: 'p', WSD_RISK_REGISTER: 'r', WSD_PLAN_TASKRSRC: 't', WSD_COMU_MEETING: 'm', WSD_PLAN_DELVASSIGN: 'd' }[table] || 'x';

    let sql = `SELECT ${fields.join(', ')} FROM ${table} ${alias}`;

    // 追加 JOIN
    if (table === 'WSD_PLAN_TASK' && (domain.includes('责任人') || domain.includes('延期') || domain.includes('看板'))) {
        sql += ` LEFT JOIN WSD_SYS_USER u ON ${alias}.USER_ID = u.ID LEFT JOIN WSD_SYS_ORG o ON ${alias}.ORG_ID = o.ID`;
    }
    if (table === 'WSD_PLAN_PROJECT') {
        sql += ` LEFT JOIN WSD_SYS_ORG o ON ${alias}.ORG_ID = o.ID LEFT JOIN WSD_SYS_USER u ON ${alias}.USER_ID = u.ID`;
    }
    if (table === 'WSD_RISK_REGISTER') {
        sql += ` LEFT JOIN WSD_SYS_USER u ON ${alias}.USER_ID = u.ID`;
    }
    if (table === 'WSD_PLAN_TASKRSRC') {
        sql += ` LEFT JOIN WSD_RSRC_USER rsrc ON ${alias}.RSRC_ID = rsrc.ID LEFT JOIN WSD_SYS_ORG o ON rsrc.ORG_ID = o.ID`;
    }
    if (table === 'WSD_COMU_MEETING') {
        sql += ` LEFT JOIN WSD_SYS_USER u ON ${alias}.DUTY_ID = u.ID LEFT JOIN WSD_COMU_MEETINGACTION ma ON ma.MEETING_ID = ${alias}.ID`;
    }

    // WHERE 条件
    const where = [];

    // task_type 过滤（里程碑），TASK_TYPE 已是大写
    if (filter) {
        where.push(`${alias}.${filter}`);
    }

    // DEL 过滤（从知识库动态判断，不再硬编码）
    if (hasDelField(table)) {
        where.push(`${alias}.DEL = 0`);
    }

    // projectId 过滤（scope=global 时跳过，scope 不明确时仍按原有逻辑）
    // domainInfo.scope 由 DOMAIN_TABLE_MAP 传入，表示需求是否针对全局
    const isGlobalScope = domainInfo.scope === 'global';
    if (!isGlobalScope && context.projectId && (domain.includes('任务') || domain.includes('风险') || domain.includes('项目') || domain.includes('会议') || domain.includes('交付物'))) {
        where.push(`${alias}.PROJECT_ID = ?`);
    }

    if (where.length > 0) {
        sql += ` WHERE ${where.join(' AND ')}`;
    }

    // GROUP BY（资源/风险热力/统计类）
    if (table === 'WSD_PLAN_TASKRSRC') {
        sql = sql.replace(/SELECT (.+?) FROM/, 'SELECT $1 FROM').replace(', o.ORG_NAME AS org_name', '').replace(/GROUP BY .+?(HAVING|$)/, '');
        if (!sql.includes('GROUP BY')) sql += ` GROUP BY ${alias}.ORG_ID, o.ORG_NAME`;
    }
    if (domain.includes('热力') || domain.includes('四象限')) {
        if (!sql.includes('GROUP BY')) sql += ` GROUP BY PROBABILITY_LEVEL, AFTERMATH_LEVEL`;
    }
    // 总体/汇总类聚合查询：不加 GROUP BY
    // 原因：skill 生成的 SQL 不再包含 TENANT_ID = ?，后端会自动注入 WHERE TENANT_ID = ? 条件。
    //       因此不需要 GROUP BY TENANT_ID 来做租户隔离。
    //       加 GROUP BY 反而会导致返回多行（每个租户一行），破坏 KPI 单值展示。

    // ORDER BY（总体类聚合查询不加 ORDER BY，汇总结果无需排序）
    const isOverallType = domain.includes('总体') || domain.includes('汇总') || domain.includes('全局') || domain.includes('整体') || domain.includes('overview') || domain.includes('overall');
    if (!sql.includes('ORDER BY') && !domain.includes('热力') && !isOverallType) {
        sql += ` ORDER BY ${alias}.PLAN_END_TIME`;
    }

    // LIMIT（总体类聚合查询不加 LIMIT，结果就是一行）
    // 注意：LIMIT 由 resolveDomain() 通过 dialect.applyPagination() 统一添加
    // buildSQL 只负责返回不含 LIMIT 的基础 SQL，保持纯粹的 SELECT 逻辑

    return sql;
}

// ============================================================
// 6. 主入口：resolveDomain — 业务域 → sqlMap entry
// ============================================================

/**
 * 将业务域描述解析为完整的 sqlMap entry
 *
 * @param {string} domain - 业务域描述（如"任务延期情况"）
 * @param {{ projectId?, epsId? }} context
 * @returns {{
 *   found: boolean,
 *   entry: { key, sql, type, title, scope, spec } | null,
 *   domainInfo: object,
 *   suggestion?: string
 * }}
 */
function resolveDomain(domain, context = {}) {
    const { persist = true } = context;
    
    // 0. 优先从 evolved_domains.json 查找（auto-evolution 沉淀的结果）
    const evolved = loadEvolvedDomains();
    const domainKey = domainToKey(domain);
    if (evolved[domainKey]) {
        return {
            found: true,
            entry: { ...evolved[domainKey], dbType: evolved[domainKey].dbType || 'mysql' },
            domainInfo: { domain, key: domainKey, source: 'evolved' },
            suggestion: null
        };
    }

    // 1. 分类域
    const domainInfo = classifyDomain(domain);

    if (!domainInfo.table) {
        return {
            found: false,
            entry: null,
            domainInfo,
            suggestion: domainInfo.suggestion
        };
    }

    // 2. 获取表结构（供未来扩展）
    const schema = getTableSchema(domainInfo.table);

    // 3. 推断 spec
    const { type, scope, spec } = inferSpecFromDomain(domain, domainInfo, context);

    // 4. 生成 SQL（不含 LIMIT）
    const baseSQL = buildSQL(domain, domainInfo, context);

    // 5. 应用数据库方言-specific LIMIT 分页
    const dbType = context.dbType || 'mysql';
    const dialect = createDialect(dbType);

    // ORDER BY 字段（与 buildSQL 内部逻辑保持一致）
    const table = domainInfo.table;
    const alias = { WSD_PLAN_TASK: 't', WSD_PLAN_PROJECT: 'p', WSD_RISK_REGISTER: 'r', WSD_PLAN_TASKRSRC: 't', WSD_COMU_MEETING: 'm', WSD_PLAN_DELVASSIGN: 'd' }[table] || 'x';
    const orderByField = `${alias}.PLAN_END_TIME`;

    // 判断是否加 ORDER BY 和 LIMIT（总体类不加）
    const isOverallType = domain.includes('总体') || domain.includes('汇总') ||
        domain.includes('全局') || domain.includes('整体') ||
        domain.includes('overview') || domain.includes('overall');

    let finalSQL = baseSQL;
    if (!isOverallType && !domain.includes('统计') && !domain.includes('load') && !domain.includes('热力')) {
        finalSQL = dialect.applyPagination(baseSQL, 0, 20, orderByField);
    } else if (!isOverallType) {
        // 有 ORDER BY 但不加 LIMIT（如 load 类已有 LIMIT）
        if (!baseSQL.includes('ORDER BY')) {
            finalSQL = `${baseSQL} ORDER BY ${orderByField}`;
        }
    }

    // 6. 构建 key（domain 转为 camelCase）
    const key = domainToKey(domain);
    
    const result = {
        found: true,
        entry: {
            key,
            sql: finalSQL,
            type,
            title: domain,
            scope,
            spec,
            dbType  // 记录该 SQL 对应的数据库类型
        },
        domainInfo,
        schema,
        suggestion: domainInfo.suggestion || null
    };
    
    // 7. 自动持久化（如果 persist 为 true 且不是从 evolved 加载）
    if (persist && result.found) {
        updateSqlMap(domain, result.entry);
    }
    
    return result;
}

// ============================================================
// 辅助函数
// ============================================================

/**
 * 将业务域字符串转为合法的 js key（camelCase）
 */
function domainToKey(domain) {
    return domain
        .replace(/[^a-zA-Z0-9\u4e00-\u9fa5]+/g, '_')
        .replace(/([a-z])([A-Z])/g, '$1$2')
        .replace(/([A-Z])([A-Z][a-z])/g, '$1$2')
        .replace(/^([A-Z])/, m => m.toLowerCase())
        .replace(/_([a-z])/g, (m, c) => c.toUpperCase())
        .slice(0, 40);
}

// ============================================================
// 7. sqlMap 持久化：将新条目写入 evolved_domains.json
// ============================================================

/**
 * 将新的 domain → entry 条目持久化到 evolved_domains.json
 *
 * 策略：
 * 1. 读取现有 evolved_domains.json（如不存在则为空对象）
 * 2. 用 domainToKey(domain) 作为 key，合并新条目（同名 key 覆盖）
 * 3. 写回 evolved_domains.json（保持 JSON 格式化）
 *
 * 注意：不修改 SKILL.md，保持技能规范文档的稳定性。
 *
 * @param {string} domain - 业务域描述（如"总体进度"）
 * @param {{ key, sql, type, title, scope, spec }} entry - sqlMap 条目
 * @returns {{ success: boolean, message: string }}
 */
function updateSqlMap(domain, entry) {
    try {
        const evolved = loadEvolvedDomains();
        const key = entry.key || domainToKey(domain);
        evolved[key] = { ...entry, key }; // 确保 key 字段存在

        // 格式化写入（保持 JSON 结构化）
        const content = JSON.stringify(evolved, null, 2);
        fs.writeFileSync(EVOLVED_DOMAINS_PATH, content, 'utf-8');

        // 清除缓存，下次 loadEvolvedDomains() 会重新读取
        _evolvedDomains = null;

        console.log(`  💾 sqlMap 已更新: '${key}' → evolved_domains.json`);
        return { success: true, message: `evolved_domains['${key}'] 已写入` };
    } catch (e) {
        return { success: false, message: `updateSqlMap 失败: ${e.message}` };
    }
}

// ============================================================
// 8. resolveDomain 的增强版：推理成功后自动持久化
// ============================================================

/**
 * 将业务域描述解析为 sqlMap entry，并将新条目持久化到 evolved_domains.json
 * 等同于 resolveDomain() + updateSqlMap()
 *
 * @param {string} domain
 * @param {{ projectId?, persist?: boolean }} context
 *   - persist: 是否持久化（默认 true）。设为 false 则只推理不写文件
 * @returns {resolveDomain 返回值 + persistResult}
 */
function resolveAndPersist(domain, context = {}) {
    const { persist = true } = context;
    const result = resolveDomain(domain, context);

    if (!result.found) {
        return { ...result, persistResult: { success: false, message: '未找到匹配域，无法持久化' } };
    }

    if (!persist) {
        return { ...result, persistResult: null };
    }

    // 只有 evolved_domains.json 中不存在的 key 才会持久化
    // resolveDomain() 返回 found=true 时：
    //   - source=evolved：来自已有沉淀，跳过写入
    //   - 其他：来自推理生成，写入 evolved_domains.json
    if (result.domainInfo.source === 'evolved') {
        return { ...result, persistResult: { success: true, message: '已存在于 evolved_domains，跳过写入' } };
    }

    const persistResult = updateSqlMap(domain, result.entry);
    return { ...result, persistResult };
}


// ============================================================
// 辅助函数
// ============================================================

module.exports = {
    searchTables,
    getTableSchema,
    hasDelField,
    classifyDomain,
    inferSpecFromDomain,
    inferSelectFields,
    buildSQL,
    resolveDomain,
    resolveAndPersist,
    updateSqlMap,
    domainToKey,
    DOMAIN_TABLE_MAP
};
