#!/usr/bin/env node
/**
 * NL2SQL 页面生成器
 *
 * 支持单图表和多图表（驾驶舱）模板
 *
 * 单图表用法:
 *   node generate_page.js "SELECT ..." --title "页面标题" --type bar
 *
 * 多图表用法（驾驶舱）:
 *   node generate_page.js \
 *     --template cockpit \
 *     --charts projectList.sql,kpi_health.sql,riskHeatmap.sql \
 *     --title "项目驾驶舱" \
 *     --project-id 61 \
 *     --output cockpit.html \
 *     --deploy        # 生成后自动部署到 acm_www/static/
 *
 * sqlMap 新格式（显式配置）：
 *   const sqlMap = {
 *     'kpi_health': {
 *       sql: 'SELECT ...',
 *       type: 'kpi',          // kpi | chart | sidebar
 *       title: '任务健康度',
 *       scope: 'project',    // project | global
 *       spec: {
 *         chartType: 'bar',   // bar | line | pie | scatter | timeline | kanban | gantt | number
 *         kpiType: 'health_score',
 *         valueField: 'health_score',
 *         unit: '分',
 *         thresholds: { green: 80, orange: 60 },
 *         xAxis: 'aftermath_level',
 *         yAxis: 'probability_level',
 *         valueField: 'count',
 *         width: 'third'      // third | half | full
 *       }
 *     }
 *   };
 */

const fs = require('fs');
const path = require('path');
const http = require('http');
const { encrypt } = require('../security/encryptSql.js');
const { createDialect } = require('../core/dialect.js');
const { verify, batchVerifyHtml } = require('../verify/index.js');
const { normalize, inferChartTypeFromEntry, validate } = require('./chartSpecSchema.js');
const { validateTemplates, validateTemplateContent } = require('../templates/validate.js');
const { validateHtml } = require('./validate_page.js');
const { deploy } = require('../deploy/index.js');

// 配置
const config = require('../core/config.js');

// DM 列名保留字（出现在 SQL 中作为独立标识符时需要加引号）
// 不包含 ORDER/GROUP 等 SQL 关键字（它们在 ORDER BY/GROUP BY 位置不会作为列名）
const DM_COL_RESERVED = new Set([
    'DATE', 'TIME', 'USER', 'INDEX', 'KEY', 'TABLE', 'VIEW',
    'VALUE', 'TEXT', 'COMMENT', 'SESSION', 'ROLE', 'DEL'
]);
const TEMPLATES_DIR = path.join(__dirname, '../../templates');
const SKILL_DIR = path.join(__dirname, '../..');
// 知识库路径：按 dbType 分离，shared 文件在 shared/ 子目录
const KNOWLEDGE_BASE = path.join(SKILL_DIR, 'knowledge');
const KNOWLEDGE_DIR = path.join(KNOWLEDGE_BASE, config.db.type);
const FIELD_MAPPING_PATH = path.join(KNOWLEDGE_DIR, 'field_mapping.json');
const WORKSPACE_TEMPLATES_DIR = path.join(config.workspace, 'templates');
const COCKPIT_CURRENT = path.join(WORKSPACE_TEMPLATES_DIR, 'cockpit_current.html');
const COCKPIT_HISTORY_DIR = path.join(WORKSPACE_TEMPLATES_DIR, 'cockpit_history');
const COCKPIT_BASE = path.join(TEMPLATES_DIR, 'cockpit_template.html');
const API_BASE = config.api.base;
// 认证 API 基础路径（从 API_BASE 派生，去掉 /api 前缀后的部分）
// 例如: http://localhost:8765 → http://localhost:8765/api/auth
// 用于 /api/auth/jwt/token 等认证接口
const API_AUTH_BASE = API_BASE.replace(/\/api\/.*$/, '') + '/api/auth';
const VERIFY_SOURCE = process.env.VERIFY_SOURCE || 'unified';
const DB_TYPE = config.db.type;
// 默认输出路径：遵循 config.workspace 配置
const DEFAULT_OUTPUT = path.join(config.workspace, 'nl2sql_output', 'cockpit.html');

// ================================================================
// HTTP 调用（用于页面嵌入 token，获取时 live 调用一次）
// ================================================================
function httpPost(pathname, body, token) {
    return new Promise((resolve, reject) => {
        const url = new URL(pathname, API_BASE);
        const postData = JSON.stringify(body);
        const options = {
            hostname: url.hostname, port: url.port || 80,
            path: url.pathname, method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': token || '',
                'Content-Length': Buffer.byteLength(postData)
            }
        };
        const req = http.request(options, res => {
            let data = '';
            res.on('data', c => data += c);
            res.on('end', () => {
                try { resolve(JSON.parse(data)); }
                catch (e) { reject(new Error(`解析响应失败: ${data.substring(0, 100)}`)); }
            });
        });
        req.on('error', reject);
        req.write(postData);
        req.end();
    });
}



// ================================================================
// 加载字段映射
// ================================================================
function loadFieldMapping() {
    try {
        return JSON.parse(fs.readFileSync(FIELD_MAPPING_PATH, 'utf-8'));
    } catch (e) {
        return { '字段→中文名': {}, '枚举值映射': {} };
    }
}

// ================================================================
// 解析单条 SQL（SELECT 字段 FROM 表名）
// ================================================================
function parseSql(sql) {
    const m = sql.match(/SELECT\s+([\s\S]+?)\s+FROM\s+(\w+)/i);
    if (!m) throw new Error(`无法解析 SQL: ${sql.substring(0, 50)}`);
    const fieldsRaw = m[1].replace(/\n/g, ' ').trim();
    const tableName = m[2];
    const fields = fieldsRaw.split(',').map(f => {
        const as = f.match(/(\w+)\s+AS\s+\w+/i);
        if (as) return as[1];
        const dot = f.match(/(\w+)$/);
        return dot ? dot[1] : f.trim();
    });
    return { tableName, fields };
}

// ================================================================
// 读取 SQL 文件（支持 # 开头的注释）
// ================================================================
function readSqlFile(filePath) {
    const content = fs.readFileSync(filePath, 'utf-8');
    return content.split('\n').filter(l => !l.trim().startsWith('#')).join('\n').trim();
}

// ================================================================
// 解析 sqlMap — 核心：替代隐式 key 推断
//
// 输入: { key: entry }  其中 entry 可能是：
//   - 纯字符串（旧格式兼容）: 'SELECT ...'
//   - 新格式对象: { sql, type, title, scope, spec }
// 输出: { sidebarEntries: [], chartEntries: [], errors: [] }
// ================================================================
function parseSqlMap(sqlMap) {
    const sidebarEntries = [];
    const chartEntries = [];
    const errors = [];

    for (const [key, rawEntry] of Object.entries(sqlMap)) {
        try {
            // normalize 兼容旧格式，并补全缺失字段
            const entry = normalize({ key, ...(typeof rawEntry === 'string' ? { sql: rawEntry } : rawEntry) });

            if (entry.type === 'sidebar') {
                sidebarEntries.push(entry);
            } else {
                chartEntries.push(entry);
            }

            // 校验（错误不中断，仅记录）
            const v = validate(entry);
            if (!v.valid) {
                errors.push({ key, errors: v.errors });
            }
        } catch (err) {
            errors.push({ key, errors: [err.message] });
        }
    }

    return { sidebarEntries, chartEntries, errors };
}

// ================================================================
// 构建 cockpit CHART_CONFIG
// ================================================================

/**
 * 生成 CHART_CONFIG JSON（供 HTML 内 JS 使用）
 * @param {object[]} chartEntries - normalize() 后的图表条目
 * @returns {string} JSON 字符串
 */
function buildChartConfig(chartEntries) {
    return JSON.stringify(chartEntries.map(entry => buildSingleChartConfig(entry)), null, 2);
}

/**
 * 生成单个图表的 CHART_CONFIG 条目
 * @param {object} entry - normalize() 后的条目
 * @returns {object} 图表配置对象
 */
function buildSingleChartConfig(entry) {
    const { key, type, title, spec } = entry;

    // 通用字段（必须包含 scope，供 buildParams 使用）
    const cfg = {
        id: key,
        title: spec.title || title || key,
        scope: entry.scope || 'project'  // ← buildParams 据此决定是否传 currentProjectId
    };

    if (type === 'kpi') {
        return {
            ...cfg,
            type: 'kpi',
            kpiType: spec.kpiType || 'count',
            valueField: spec.valueField || 'value',
            unit: spec.unit || '',
            thresholds: spec.thresholds || { green: 80, orange: 60 },
            width: spec.width || 'third'
        };
    }

    // chart / table
    return {
        ...cfg,
        type: spec.type || 'chart',
        chartType: spec.chartType || inferChartTypeFromEntry(entry),
        width: spec.width || ((spec.chartType === 'scatter' || spec.chartType === 'timeline') ? 'full' : 'half'),
        // 热力图轴映射
        ...(spec.xAxis ? { xAxis: spec.xAxis } : {}),
        ...(spec.yAxis ? { yAxis: spec.yAxis } : {}),
        ...(spec.valueField ? { valueField: spec.valueField } : {}),
        // 看板列定义
        ...(spec.kanbanColumns ? { kanbanColumns: spec.kanbanColumns } : {}),
        // 时间线
        ...(spec.startField ? { startField: spec.startField } : {}),
        ...(spec.endField ? { endField: spec.endField } : {}),
        ...(spec.labelField ? { labelField: spec.labelField } : {})
    };
}

// ================================================================
// 生成 cockpit 模板的 SQL 映射（明文 + 密文）
//
// 密文（ENCRYPTED_SQL）：供后端 execute 接口解密执行
// 明文（SQL_PLAIN）：供前端 buildParams 运行时校验 ? 占位符数量
//
// 两者 key 完全一一对应，缺一不可
// ================================================================
/**
 * 将 SQL 转换为目标数据库方言
 */
function applyDialect(sql) {
    const dbType = config.db && config.db.type ? config.db.type.toLowerCase() : 'mysql';
    if (dbType === 'dm' || dbType === 'dameng') {
        const dialect = createDialect('dm');
        // 0. 先移除 DEL = 0 条件（在加引号之前，避免后续匹配不到）
        //    DM 对 DEL 字段有 JDBC 解析问题，直接跳过软删除过滤
        let converted = sql
            .replace(/ AND p\.DEL = 0/gi, '')
            .replace(/ AND t\.DEL = 0/gi, '')
            .replace(/ AND DEL = 0/gi, '')
            .replace(/ p\.DEL = 0 AND /gi, ' ')
            .replace(/ t\.DEL = 0 AND /gi, ' ')
            .replace(/ DEL = 0 AND /gi, ' ')
            .replace(/ AND p\.DEL <> 1/gi, '')
            .replace(/ AND t\.DEL <> 1/gi, '')
            .replace(/ AND DEL <> 1/gi, '')
            .replace(/WHERE\s+p\.DEL = 0/gi, 'WHERE 1=1')
            .replace(/WHERE\s+t\.DEL = 0/gi, 'WHERE 1=1')
            .replace(/WHERE\s+DEL = 0/gi, 'WHERE 1=1')
            .replace(/\bDEL\b = 0(?=\s*(?:AND|OR|$))/gi, '1=1');
        // 清理连续 AND
        converted = converted.replace(/\bAND\s+AND\b/gi, 'AND').replace(/\s{2,}/g, ' ');
        // 1. 反引号 → 双引号（处理老 SQL 中的 `field` 写法）
        converted = converted.replace(/`([^`]+)`/g, (m, id) => dialect.quote(id));
        // 2. table.column 点标记：分别对每个标识符应用 dialect.quote()
        //    DEL → "DEL"（保留字）  ID → ID（普通标识符）  p → p（别名）
        converted = converted.replace(/([a-zA-Z_][a-zA-Z0-9_]*)\.([a-zA-Z_][a-zA-Z0-9_]*)/g,
            (m, left, right) => `${dialect.quote(left)}.${dialect.quote(right)}`);
        // 3. 裸保留字引号：处理单独出现的列名保留字（如 WHERE DEL = 0）
        //    不处理 SQL 关键字（SELECT/FROM/WHERE/AND 等词法位置已确保正确）
        converted = converted.replace(
            /(?<![a-zA-Z0-9_".`])([A-Za-z_][A-Za-z0-9_]*)(?![a-zA-Z0-9_".`])/g,
            (m, id) => {
                // 非保留字集合的标识符不处理
                if (!DM_COL_RESERVED.has(id.toUpperCase())) return id;
                // 保留字集合中的词（如 DEL/DATE/USER）→ 加引号
                return `"${id}"`;
            }
        );
        // 4. LIMIT 转换（转换为 DM 兼容的 FETCH FIRST）
        converted = converted.replace(/\s*LIMIT\s+(\d+)(?:\s*,\s*(\d+))?\s*(?:;\s*)?$/i, (m, a, b) => {
            if (b !== undefined) {
                return ` OFFSET ${a.trim()} ROWS FETCH NEXT ${b.trim()} ROWS ONLY`;
            }
            return ` FETCH FIRST ${a.trim()} ROWS ONLY`;
        });
        // 5. GROUP BY alias → 已知问题：progressTrend 的 month_label 在 DM 中须用表达式而非别名
        //    注：DATE_FORMAT 是 MySQL 语法，DM 需用 TO_CHAR，本修复仅避免报错
        converted = converted.replace(/GROUP BY month_label/gi, 'GROUP BY 1');
        return converted;
    }
    return sql;
}

function buildSqlMaps(sqlMap) {
    const encrypted = {};
    const plaintext = {};
    for (const [key, entry] of Object.entries(sqlMap)) {
        const sql = typeof entry === 'string' ? entry : entry.sql;
        const converted = applyDialect(sql);
        encrypted[key] = encrypt(converted);
        plaintext[key] = converted;  // 明文不经任何编码，供前端直接解析 ?
    }
    return {
        encrypted: JSON.stringify(encrypted, null, 2),
        plaintext: JSON.stringify(plaintext, null, 2)
    };
}

// ================================================================
// 推断中文标题（保留，用于 spec 缺失时兜底）
// ================================================================
function inferTitle(key, sql, labels) {
    const { tableName } = parseSql(sql);
    const labelKey = `${tableName}.${key}`;
    if (labels[labelKey]) return labels[labelKey];
    const keyParts = key.replace(/_/g, ' ').split(' ');
    return keyParts.map(p => p.charAt(0).toUpperCase() + p.slice(1)).join(' ');
}

/**
 * 单图表生成流程
 *
 * @param {string} sql - SELECT 查询语句
 * @param {{ title?, chartType?, inspect? }} options
 * @returns {Promise<string>} 生成的 HTML 字符串
 */
async function generateSingleChart(sql, options = {}) {
    // 验证模板质量，发现问题直接抛错，不进入后续流程
    const errors = validateTemplates();
    if (errors.length > 0) {
        throw new Error('模板验证未通过，请先修复模板问题: ' + errors.join('; '));
    }

    const { title = '数据看板', chartType = 'table', inspect = true } = options;

    const { tableName, fields } = parseSql(sql);
    console.log(`解析 SQL: 表=${tableName}, 字段=${fields.join(', ')}`);

    const fieldMapping = loadFieldMapping();
    const labels = fieldMapping['字段→中文名'] || {};

    // 枚举值 + 字段标签
    const enumResult = {};
    const enumValues = fieldMapping['枚举值映射'] || {};
    for (const field of fields) {
        const key = `${tableName}.${field}`;
        if (enumValues[key]) {
            const v = { ...enumValues[key] };
            delete v._comment;
            enumResult[field] = v;
        }
    }

    const fieldLabels = {};
    for (const field of fields) {
        const key = `${tableName}.${field}`;
        fieldLabels[field] = labels[key] || field;
    }

    const converted = applyDialect(sql);
    const encrypted = encrypt(converted);

    // 验证（使用统一引擎）
    if (inspect) {
        const result = await verify(sql, { source: VERIFY_SOURCE, dbType: DB_TYPE });
        if (result.ok) {
            const mysqlSrc = result.sources?.mysql;
            const apiSrc = result.sources?.api;
            if (mysqlSrc) console.log(`  MySQL检查: ${mysqlSrc.rows} 行, 字段: ${mysqlSrc.fields.join(', ')}`);
            if (apiSrc && !apiSrc.ok) console.warn(`  API检查: ⚠️ ${apiSrc.error.substring(0, 80)}`);
        } else {
            console.warn(`  验证失败: ${result.error.substring(0, 80)}`);
        }
    }

    const templatePath = path.join(TEMPLATES_DIR, 'html_page_template.html');
    let template = fs.readFileSync(templatePath, 'utf-8');

    return template
        .replaceAll('{{CHART_TITLE}}', title)
        .replaceAll('{{ENCRYPTED_SQL}}', encrypted.ciphertext)
        .replaceAll('{{IV}}', encrypted.iv)
        .replaceAll('{{ENUM_MAP}}', JSON.stringify(enumResult))
        .replaceAll('{{FIELD_LABELS}}', JSON.stringify(fieldLabels))
        .replaceAll('{{API_DATA_PATH}}', 'result.data.data');
}

// ================================================================
// 模板解析 — 确定使用哪个模板文件
// ================================================================

/**
 * 模板加载优先级：
 *   1. 用户当前版本（workspace/templates/cockpit_current.html）
 *   2. 技能基线模板（skills/templates/cockpit_template.html）
 *
 * @param {object} options
 * @param {boolean} options.regenerate - 是否强制重新生成模板
 * @param {string|null} options.templateContent - 重新生成时的新模板内容
 * @returns {{ template: string, source: 'current'|'base'|'default' }}
 */
function resolveCockpitTemplate(options = {}) {
    const { regenerate = false, templateContent = null } = options;

    // 强制重新生成：保存新模板并覆盖两级文件
    if (regenerate && templateContent) {
        ensureDir(WORKSPACE_TEMPLATES_DIR);
        ensureDir(COCKPIT_HISTORY_DIR);

        // 存档旧版本（如果当前版本存在）
        if (fs.existsSync(COCKPIT_CURRENT)) {
            const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
            const historyPath = path.join(COCKPIT_HISTORY_DIR, `cockpit_${timestamp}.html`);
            fs.copyFileSync(COCKPIT_CURRENT, historyPath);
            console.log(`  📦 历史版本已存档: ${path.basename(historyPath)}`);
        }

        // 写入两级文件
        fs.writeFileSync(COCKPIT_CURRENT, templateContent, 'utf-8');
        fs.writeFileSync(COCKPIT_BASE, templateContent, 'utf-8');
        console.log(`  ✅ 模板已更新（强制重构）`);

        return { template: templateContent, source: 'regenerated' };
    }

    // 优先使用用户当前版本
    if (fs.existsSync(COCKPIT_CURRENT)) {
        return { template: fs.readFileSync(COCKPIT_CURRENT, 'utf-8'), source: 'current' };
    }

    // 降级到技能基线模板
    if (fs.existsSync(COCKPIT_BASE)) {
        return { template: fs.readFileSync(COCKPIT_BASE, 'utf-8'), source: 'base' };
    }

    throw new Error(
        `找不到 cockpit 模板文件。\n` +
        `  - 用户当前版本: ${COCKPIT_CURRENT}（${fs.existsSync(COCKPIT_CURRENT) ? '存在' : '不存在'}）\n` +
        `  - 技能基线模板: ${COCKPIT_BASE}（${fs.existsSync(COCKPIT_BASE) ? '存在' : '不存在'}）\n` +
        `  请确保已生成过驾驶舱模板，或传入 regenerate=true 重新生成。`
    );
}

// ================================================================
// 微调 — 将用户描述的局部调整应用到 HTML
// ================================================================

/**
 * 将 tweak 关键词转换为 HTML 修改，作用于内存中的模板字符串
 * 修改后写回 cockpit_current.html（不影响基线模板）
 *
 * @param {string} html - 模板 HTML 字符串
 * @param {string|null} tweak - 用户描述的微调关键词
 * @returns {string} 应用微调后的 HTML
 */
function applyTweak(html, tweak) {
    if (!tweak || typeof tweak !== 'string') return html;

    const allTweaks = [
        // 左侧边栏宽度
        { pattern: /sidebar-width:\s*\d+px/g,          replacement: 'sidebar-width: 180px',     keywords: ['左侧宽度调窄', '侧边栏调窄', 'sidebar.*narrow', 'sidebar.*small'] },
        { pattern: /sidebar-width:\s*\d+px/g,          replacement: 'sidebar-width: 280px',     keywords: ['左侧宽度调宽', '侧边栏调宽', 'sidebar.*wide', 'sidebar.*large'] },
        // KPI 卡片尺寸
        { pattern: /kpi-card.*width:\s*\d+px/g,         replacement: 'kpi-card-width: 220px',    keywords: ['kpi.*放大', '指标卡.*放大'] },
        { pattern: /kpi-card.*width:\s*\d+px/g,         replacement: 'kpi-card-width: 160px',    keywords: ['kpi.*缩小', '指标卡.*缩小'] },
        // 主色调加深
        { pattern: /--color-primary:\s*[^;]+;/g,        replacement: '--color-primary: #1a3a5c;', keywords: ['颜色加深', '主色调加深', '深色', 'dark'] },
        // 主色调调浅
        { pattern: /--color-primary:\s*[^;]+;/g,        replacement: '--color-primary: #4a90d9;', keywords: ['颜色调浅', '主色调调浅', '浅色', 'light'] },
        // 去掉右侧活动流
        { pattern: /<div[^>]*id=["']?activity[^\n]*[\s\S]*?<\/div>\s*/gi, replacement: '', keywords: ['去掉右侧', '去掉活动流', '隐藏活动流', 'remove.*activity'] },
        // 去掉顶部导航
        { pattern: /<div[^>]*class=["'][^"']*navbar[^\n]*[\s\S]*?<\/div>\s*/gi, replacement: '', keywords: ['去掉顶部', '去掉导航', '隐藏导航', 'remove.*navbar'] },
    ];

    let applied = [];
    for (const t of allTweaks) {
        const match = t.keywords.some(k => tweak.toLowerCase().includes(k.toLowerCase()));
        if (match) {
            const newHtml = html.replace(t.pattern, t.replacement);
            if (newHtml !== html) {
                applied.push(t.keywords[0]);
                html = newHtml;
            }
        }
    }

    if (applied.length > 0) {
        console.log(`  🎨 微调已应用: ${applied.join(', ')}`);
    }

    return html;
}

// ================================================================
// 目录创建辅助
// ================================================================

function ensureDir(dir) {
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
}

// ================================================================
// 多图表生成流程（驾驶舱）
//
// 正确顺序：
//   1. 验证 SQL（失败则重试，治本；重试耗尽则抛错，停止一切）
//   2. 重试耗尽 → 抛错，不继续生成坏页面
//   3. 全部 SQL 验证通过 → parseSqlMap → buildChartConfig
//   4. 加密 → 填充模板
// ================================================================


/**
 * 驾驶舱生成流程（多图表）
 *
 * @param {Object} sqlMap - sqlMap 对象
 * @param {{
 *   title?: string,
 *   projectId?: number,
 *   verify?: boolean,
 *   tweak?: string,
 *   regenerate?: boolean,
 *   templateContent?: string
 * }} options
 * @returns {Promise<string>} 生成的 HTML 字符串
 */
async function generateCockpitChart(sqlMap, options = {}) {
    const {
        title = '项目驾驶舱',
        projectId = 61,
        verify: shouldVerify = true,
        tweak = null,           // 局部微调关键词，如 "左侧宽度调窄"
        regenerate = false,      // 是否强制重新生成模板
        templateContent = null,   // 重新生成时的新模板内容（由调用方从材料生成后传入）
        deploy: _shouldDeploy = false,  // 已废弃，部署由 CLI 侧处理
    } = options;

    console.log(`\n=== 驾驶舱生成 ===`);
    console.log(`图表数量: ${Object.keys(sqlMap).length}`);
    console.log(`默认项目: ${projectId}`);

    // ── 0. 模板校验（最先执行）────────────────────────────────────
    // 新生成模板内容（regenerate 模式）优先校验
    if (regenerate && templateContent) {
        console.log(`\n=== 新模板内容校验 ===`);
        const newTplErrors = validateTemplateContent(templateContent, { type: 'cockpit', verbose: true });
        if (newTplErrors.length > 0) {
            throw new Error('新模板验证未通过，缺少必要的鉴权/运行时组件: ' + newTplErrors.join('; '));
        }
    } else {
        // 验证内置模板质量（日常数据更新场景）
        const errors = validateTemplates();
        if (errors.length > 0) {
            throw new Error('内置模板验证未通过: ' + errors.join('; '));
        }
    }

    // ── 1. 模板解析（决定使用哪个模板文件）────────────
    const { template: cockpitTemplate, source: templateSource } = resolveCockpitTemplate({ regenerate, templateContent });
    console.log(`  模板来源: ${templateSource === 'current' ? 'workspace/templates/cockpit_current.html（用户当前版本）' : templateSource === 'base' ? 'skills/templates/cockpit_template.html（技能基线）' : '新生成'}`);

    // ── 1. 验证 + 重试 SQL（全部通过后才进入下一步）───────────────
    if (shouldVerify) {
        console.log(`\n=== SQL 验证 + 重试 (source=${VERIFY_SOURCE}, max_retries=${MAX_SQL_VERIFY_RETRIES}) ===`);

        const verifiedSqlMap = {};  // 最终确认可用的 sqlMap

        for (const [key, rawEntry] of Object.entries(sqlMap)) {
            const entry = typeof rawEntry === 'string'
                ? { sql: rawEntry, type: 'chart', title: key, scope: 'project', spec: {} }
                : rawEntry;

            const sql = entry.sql;
            // scope=global 或 SQL 中没有 ? 时不传 projectId
            const scope = entry.scope || (sql.includes('PROJECT_ID') ? 'project' : 'global');
            const params = scope === 'project' && sql.includes('?') ? [projectId] : [];

            let lastError = null;
            let success = false;

            for (let attempt = 1; attempt <= MAX_SQL_VERIFY_RETRIES; attempt++) {
                const result = await verify(sql, { projectId: params[0] || null, source: VERIFY_SOURCE, dbType: entry.dbType || DB_TYPE });

                if (result.ok) {
                    const srcStatus = result.sources
                        ? Object.entries(result.sources).map(([s, r]) => `${s}:${r.ok ? '✅' : '❌'}`).join(' ')
                        : '';
                    console.log(`  ✅ ${key}: ${result.rows} 行 ${srcStatus}${attempt > 1 ? ` (重试${attempt-1}次后成功)` : ''}`);
                    verifiedSqlMap[key] = entry;
                    success = true;
                    break;
                } else {
                    lastError = result.error;
                    const srcStatus = result.sources
                        ? Object.entries(result.sources).map(([s, r]) => `${s}:${r.ok ? '✅' : '❌'}`).join(' ')
                        : '';
                    console.log(`  ❌ ${key} [第${attempt}次]: ${result.error.substring(0, 80)}`);
                    if (result.sources?.api && !result.sources.api.ok) {
                        console.log(`     ↳ API: ${result.sources.api.error.substring(0, 60)}`);
                    }
                    if (attempt < MAX_SQL_VERIFY_RETRIES) {
                        console.log(`  ↳ 第 ${attempt} 次失败，${attempt < MAX_SQL_VERIFY_RETRIES ? `重试...` : ''}`);
                    }
                }
            }

            // 重试全部耗尽 → 抛错，停止整个生成流程
            if (!success) {
                console.error(`\n❌ ${key} 重试 ${MAX_SQL_VERIFY_RETRIES} 次后仍失败，停止生成`);
                console.error(`   错误原因: ${lastError}`);
                console.error(`   请检查：字段名是否正确、表是否存在、WHERE 条件是否合法`);
                throw new Error(`[SQL验证失败] ${key}: ${lastError}`);
            }
        }

        // 验证全部通过，用已验证的 sqlMap 替换
        sqlMap = verifiedSqlMap;
        console.log(`\n✅ 所有 SQL 验证通过（${Object.keys(sqlMap).length} 个），继续生成页面`);
    }

    // ── 2. 解析 sqlMap（只有在 SQL 全部验证通过后才执行）────────────
    const { sidebarEntries, chartEntries, errors: parseErrors } = parseSqlMap(sqlMap);

    if (parseErrors && parseErrors.length > 0) {
        console.warn(`⚠️  ${parseErrors.length} 个条目解析异常:`);
        parseErrors.forEach(e => console.warn(`  ⚠️  ${e.key}: ${e.errors.join(', ')}`));
    }

    console.log(`\n  sidebar: ${sidebarEntries.map(e => e.key).join(', ') || '(无)'}`);
    console.log(`  charts:  ${chartEntries.map(e => `${e.key}(${e.type}/${e.spec?.chartType || '-'})`).join(', ')}`);

    // ── 3. 构建 CHART_CONFIG ──────────────────────────────────────
    const chartConfig = buildChartConfig(chartEntries);
    console.log(`\n  CHART_CONFIG 生成完成（${chartEntries.length} 个图表）`);

    // ── 4. 生成 SQL 映射（明文 + 密文）─────────────────────────────
    // plaintext 用于前端 buildParams 运行时校验；
    // encrypted 用于后端 execute 接口解密执行。
    const { encrypted: encryptedSqlMap, plaintext: plaintextSqlMap } = buildSqlMaps(sqlMap);

    // ── 5. 填充 cockpit 模板 ───────────────────────────────────────
    // 登录密码是否加密（true=ACM老系统加密，false=明文）
    const loginPasswordEncrypt = config.api?.loginPasswordEncrypt !== false;

    let outputHtml = cockpitTemplate
        .replaceAll('{{PAGE_TITLE}}', title)
        .replaceAll('{{CHART_CONFIG}}', chartConfig)
        .replaceAll('{{ENCRYPTED_SQL}}', encryptedSqlMap)
        .replaceAll('{{SQL_PLAIN}}', plaintextSqlMap)
        .replaceAll('{{DEFAULT_PROJECT_ID}}', String(projectId))
        .replaceAll('{{API_BASE}}', API_BASE)
        .replaceAll('{{API_AUTH_BASE}}', API_AUTH_BASE)
        .replaceAll('{{LOGIN_PASSWORD_ENCRYPT}}', String(loginPasswordEncrypt));

    // ── 5. 应用局部微调（如用户有描述）────────────────────────────
    if (tweak) {
        outputHtml = applyTweak(outputHtml, tweak);
    }

    console.log(`\n✅ 驾驶舱 HTML 生成完成`);

    return outputHtml;
}

// ================================================================
// CLI 入口
// ================================================================
if (require.main === module) {
    const args = process.argv.slice(2);

    if (args.length === 0) {
        console.log(`NL2SQL 页面生成器`);
        console.log(`用法:`);
        console.log(`  单图表: node generate_page.js "SELECT ..." --title "标题"`);
        console.log(`  驾驶舱: node generate_page.js --charts sql1.sql,sql2.sql --title "标题"`);
        console.log(`  驾驶舱: node generate_page.js --sqlmap sqlmap.json --title "标题"`);
        console.log(`选项:`);
        console.log(`  --charts <文件>   SQL 文件列表（逗号分隔）`);
        console.log(`  --sqlmap <文件>   SQL 配置映射 JSON 文件`);
        console.log(`  --title <标题>    页面标题`);
        console.log(`  --project-id <ID> 默认项目ID`);
        console.log(`  --output <文件>   输出文件（single-chart 默认 nl2sql_output/cockpit.html；cockpit 忽略，固定路径）`);
        console.log(`  --no-verify       跳过 SQL 验证`);
        console.log(`  --tweak <关键词>   局部微调（如"左侧宽度调窄"）`);
        console.log(`  --regenerate       强制重新生成模板（覆盖 cockpit_current.html）`);
        console.log(`  --deploy           生成后自动部署到 acm_www/static/`);
        process.exit(1);
    }

    let sql = null;
    let title = '数据看板';
    let chartFiles = null;
    let sqlMapFile = null;
    let projectId = 61;
    let outputFile = DEFAULT_OUTPUT;
    let verify = true;
    let tweak = null;
    let regenerate = false;
    let deployFlag = false;

    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--charts' && args[i + 1]) chartFiles = args[++i].split(',');
        else if (args[i] === '--sqlmap' && args[i + 1]) sqlMapFile = args[++i];
        else if (args[i] === '--title' && args[i + 1]) title = args[++i];
        else if (args[i] === '--project-id' && args[i + 1]) projectId = Number(args[++i]);
        else if (args[i] === '--output' && args[i + 1]) outputFile = args[++i];
        else if (args[i] === '--no-verify') verify = false;
        else if (args[i] === '--tweak' && args[i + 1]) tweak = args[++i];
        else if (args[i] === '--regenerate') regenerate = true;
        else if (args[i] === '--deploy') deployFlag = true;
        else if (!args[i].startsWith('--')) sql = args[i];
    }

    (async () => {
        try {
            let html;

            if (chartFiles) {
                // 多图表模式（CLI 还是从文件读，每个文件内容作为纯 SQL 字符串）
                const sqlMap = {};
                chartFiles.forEach(file => {
                    const key = path.basename(file.trim(), '.sql');
                    sqlMap[key] = readSqlFile(file.trim());
                });
                html = await generateCockpitChart(sqlMap, { title, projectId, verify, tweak, regenerate });
            } else if (sqlMapFile) {
                // 从 JSON 文件读取 sqlMap
                const sqlMap = JSON.parse(fs.readFileSync(sqlMapFile, 'utf-8'));
                html = await generateCockpitChart(sqlMap, { title, projectId, verify, tweak, regenerate });
            } else if (sql) {
                html = await generateSingleChart(sql, { title, inspect: verify });
            } else {
                console.error('错误: 请提供 SQL、--charts 或 --sqlmap 参数');
                process.exit(1);
            }

            // ── 保存预览版 + 验证 ──────────────────────────────────────
            // cockpit: 预览版固定路径 nl2sql_output/preview_cockpit.html
            // single-chart: 预览版为 outputFile
            const isCockpit = !!(chartFiles || sqlMapFile);
            const previewFile = isCockpit
                ? path.join(config.workspace, 'nl2sql_output', 'cockpit_preview.html')
                : outputFile;

            ensureDir(path.dirname(previewFile));

            // 生成后完整性校验（auto-fix 失败则报错退出）
            const validation = validateHtml(html, { verbose: true });
            if (!validation.valid) {
                console.error('❌ HTML 完整性校验失败，请重新生成');
                process.exit(1);
            }
            if (validation.html !== html) {
                html = validation.html;
                console.log('  🔧 已自动修复 HTML 完整性问题');
            }

            // 写入预览版（保留 CDN URLs）
            fs.writeFileSync(previewFile, html, 'utf-8');
            console.log(`  💾 预览版: ${previewFile}`);

            // HTML 端到端 API 验证（全部 PASS 才算成功）
            if (shouldVerify) {
                const batchResult = await batchVerifyHtml(previewFile, { projectId });
                if (batchResult.failed > 0) {
                    console.error(`\n❌ HTML 端到端验证失败（${batchResult.failed}/${batchResult.passed + batchResult.failed} 条 SQL API 执行失败）`);
                    console.error('  文件已删除，请重新生成');
                    try { fs.unlinkSync(previewFile); } catch (_) {}
                    process.exit(1);
                }
                console.log(`\n✅ 已生成: ${previewFile}`);
            } else {
                console.log(`\n✅ 已生成（跳过 API 验证）: ${previewFile}`);
            }

            // ── 部署（CDN→本地路径，保留部署版 + 拷贝到 static）───────────
            if (deployFlag) {
                // cockpit: preview=cockpit_preview.html, deploy=cockpit.html
                // single-chart: preview=outputFile, deploy=outputFile（同名覆盖）
                const deployLocalName = path.basename(outputFile);
                const staticName = isCockpit ? 'cockpit.html' : path.basename(outputFile);
                const result = deploy(previewFile, {
                    localOutput: deployLocalName,  // nl2sql_output/cockpit.html
                    outputName: staticName         // acm_www/static/cockpit.html
                });
                if (result.deployedTo === 'fallback') {
                    console.log(`  ⚠️  acm_www/static/ 不存在，部署版在: ${result.nlOutput}`);
                } else {
                    console.log(`  ✅ 部署版: ${result.nlOutput}`);
                }
                console.log(`  📍 访问路径: ${result.url}`);
            }
        } catch (e) {
            console.error(`❌ 生成失败: ${e.message}`);
            process.exit(1);
        }
    })();
}

module.exports = {
    generatePage: generateSingleChart,
    generateCockpitChart,
    encrypt,
    verify,
    parseSqlMap,
    buildChartConfig,
    resolveCockpitTemplate,
    applyTweak
};
