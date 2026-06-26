#!/usr/bin/env node
/**
 * verify/index.js — NL2SQL 统一验证引擎
 *
 * 提供三种验证模式：
 *   1. mysql  : 直连 MySQL（独立工具 CLI / agent 本地调试）
 *   2. api    : 调后端 HTTP API（/api/dashboard/nl2sql/execute）
 *   3. unified: 同时尝试 mysql + api，以 mysql 为准
 *
 * 统一返回格式：
 * {
 *   ok: boolean,          // 是否通过验证
 *   rows: number,         // 返回行数
 *   fields: string[],     // 字段名列表
 *   sampleRows: any[],    // 样例数据
 *   sources: {            // 各验证源的结果明细
 *     mysql?: { ok, rows, fields, error },
 *     api?:   { ok, rows, error }
 *   },
 *   error?: string        // 综合错误信息（ok=false 时有）
 * }
 *
 * CLI 用法：
 *   node src/verify/index.js [--source db|api|unified] [--sql "SELECT ..."]
 *                            [--project-id <id>] [--params <json>]
 *
 * 模块用法：
 *   const { verify, batchVerifyHtml } = require('./verify/index.js');
 *   const result = await verify('SELECT ...', { projectId: 61, source: 'unified' });
 *   const batch = await batchVerifyHtml('/path/to/page.html', { projectId: 61 });
 */

const mysql = require('mysql2/promise');
const http = require('http');
const crypto = require('crypto');
const { encrypt } = require('../security/encryptSql.js');
const { aesEncrypt } = require('../security/passwordEncrypt.js');
const config = require('../core/config.js');
const { handleError, ValidationError, DatabaseError, ApiError } = require('../core/errors.js');
const { validateSql, validateParams } = require('../core/validator.js');
const { extractJsonFromAssignment } = require('../core/htmlUtils.js');

// ============================================================
// 数据库连接池
// ============================================================

// 创建 MySQL 连接池
const { type, ...dbConfig } = config.db;
const mysqlPool = mysql.createPool({
    ...dbConfig,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
});

// 关闭连接池的函数
function closePool() {
    return mysqlPool.end();
}

// 懒加载 dialect（避免循环依赖）
let _dialect = null;
function getDialect(dbType) {
    if (!_dialect || _dialect.type !== dbType) {
        const { createDialect } = require('../core/dialect.js');
        _dialect = createDialect(dbType || config.db.type);
    }
    return _dialect;
}

// ============================================================
// 增强错误处理：根据错误类型提供修复建议
function getErrorSuggestion(error, sql, dbType) {
  // 常见错误类型和对应的修复建议
  const errorPatterns = [
    {
      pattern: /Table '.*' doesn't exist/i,
      suggestion: '表名不存在，请检查 SQL 中的表名是否正确，或在 knowledge/{dbType}/tables.json 中确认表的实际名称'
    },
    {
      pattern: /Unknown column '.*' in 'field list'/i,
      suggestion: '字段名不存在，请检查 SQL 中的字段名是否正确，或在 knowledge/{dbType}/tables.json 中确认字段的实际名称'
    },
    {
      pattern: /You have an error in your SQL syntax/i,
      suggestion: 'SQL 语法错误，请检查 SQL 语句的语法是否正确，特别是关键字的拼写和使用'
    },
    {
      pattern: /Access denied for user/i,
      suggestion: '数据库权限不足，请检查数据库用户的权限设置'
    },
    {
      pattern: /Connection refused/i,
      suggestion: '数据库连接失败，请检查数据库地址、端口、用户名和密码是否正确'
    },
    {
      pattern: /timeout/i,
      suggestion: '数据库连接超时，请检查网络连接和数据库服务是否正常'
    },
    {
      pattern: /syntax error/i,
      suggestion: 'SQL 语法错误，请检查 SQL 语句的语法是否正确'
    },
    {
      pattern: /unknown column/i,
      suggestion: '字段名不存在，请检查 SQL 中的字段名是否正确'
    },
    {
      pattern: /no such table/i,
      suggestion: '表名不存在，请检查 SQL 中的表名是否正确'
    }
  ];
  
  // 检查 Oracle 特定错误
  if (dbType === 'oracle') {
    errorPatterns.push(
      {
        pattern: /ORA-00942/i,
        suggestion: '表或视图不存在，请检查 SQL 中的表名是否正确'
      },
      {
        pattern: /ORA-00904/i,
        suggestion: '无效的标识符，请检查 SQL 中的字段名是否正确'
      },
      {
        pattern: /ORA-00933/i,
        suggestion: 'SQL 命令未正确结束，请检查 SQL 语句的语法'
      }
    );
  }
  
  // 检查达梦特定错误
  if (dbType === 'dm') {
    errorPatterns.push(
      {
        pattern: /对象名.*不存在/i,
        suggestion: '表或视图不存在，请检查 SQL 中的表名是否正确'
      },
      {
        pattern: /列名.*无效/i,
        suggestion: '字段名不存在，请检查 SQL 中的字段名是否正确'
      }
    );
  }
  
  // 匹配错误模式并返回建议
  for (const { pattern, suggestion } of errorPatterns) {
    if (pattern.test(error)) {
      return suggestion;
    }
  }
  
  // 默认建议
  return 'SQL 验证失败，请检查 SQL 语句的语法和语义是否正确';
}

// 统一返回格式工厂
// ============================================================

function okResult({ rows = 0, fields = [], sampleRows = [], sources = {} } = {}) {
    return { ok: true, rows, fields, sampleRows, sources, error: null, suggestion: null };
}

function failResult(error, sources = {}, suggestion = null) {
    return { ok: false, rows: 0, fields: [], sampleRows: [], sources, error, suggestion };
}

// ============================================================
// 模式一：数据库直连验证（MySQL / Oracle / 达梦）
// ============================================================

async function verifyByDb(sql, { projectId, extraParams, dbType = 'mysql' } = {}) {
    if (dbType === 'oracle') {
        return verifyByOracle(sql, { projectId, extraParams });
    }
    // MySQL / 达梦（达梦连接参数与 MySQL 兼容）
    return verifyByMysql(sql, { projectId, extraParams, dbType });
}

async function verifyByMysql(sql, { projectId, extraParams, dbType = 'mysql' } = {}) {
    // ⚠️ 注意：达梦(DM)和Oracle需专用驱动，当前使用 mysql2 驱动
    // 对于 dm/oracle，mysql2 会连不上而超时（30秒）
    // 因此 unified 模式会对这两种类型加 5 秒超时限制，超时后 fallback 到 API 验证
    let connection = null;
    try {
        // 验证 SQL
        validateSql(sql);

        // 从连接池获取连接
        connection = await mysqlPool.getConnection();

        // 使用 dialect 移除了原有分页，替换为验证专用 LIMIT
        const dialect = getDialect(dbType);
        let execSql = sql.trim();
        if (execSql.endsWith(';')) execSql = execSql.slice(0, -1);
        execSql = dialect.stripPagination(execSql);
        execSql = dialect.limit(execSql, 0, config.security.verifyLimit);

        // tenantId 由后端自动注入，verifySql 不需要传
        const params = [];
        if (projectId !== null && projectId !== undefined) params.push(projectId);
        if (Array.isArray(extraParams) && extraParams.length > 0) {
            validateParams(extraParams);
            params.push(...extraParams);
        }

        const [rows, fields] = await connection.query(execSql, params);
        const fieldNames = fields ? fields.map(f => f.name) : Object.keys(rows[0] || {});

        return { ok: true, rows: rows.length, fields: fieldNames, sampleRows: rows, error: null };
    } catch (err) {
        const errorResult = handleError(err);
        return { 
            ok: false, 
            rows: 0, 
            fields: [], 
            sampleRows: [], 
            error: errorResult.error 
        };
    } finally {
        if (connection) connection.release(); // 释放连接回池
    }
}

// ============================================================
// Oracle 直连验证
// 注意：需要安装 oracledb：npm install oracledb
// ============================================================

async function verifyByOracle(sql, { projectId, extraParams } = {}) {
    let connection = null;
    try {
        // 验证 SQL
        validateSql(sql);

        // 动态加载 oracledb（避免未安装时加载报错）
        let oracledb;
        try {
            oracledb = require('oracledb');
        } catch (e) {
            throw new DatabaseError('Oracle driver not installed. Run: npm install oracledb');
        }

        const connStr = `${config.oracle.host}:${config.oracle.port}/${config.oracle.serviceName}`;
        connection = await oracledb.getConnection({
            user: config.oracle.user,
            password: config.oracle.password,
            connectString: connStr
        });

        // Oracle 分页由 dialect 处理，verify 时用 ROWNUM 限制行数
        const dialect = getDialect('oracle');
        let execSql = sql.trim();
        if (execSql.endsWith(';')) execSql = execSql.slice(0, -1);
        execSql = dialect.stripPagination(execSql);
        // 简单粗暴：外层嵌套 ROWNUM 限制
        execSql = `SELECT * FROM (${execSql}) WHERE ROWNUM <= ${config.security.verifyLimit}`;

        const params = [];
        if (projectId !== null && projectId !== undefined) params.push(projectId);
        if (Array.isArray(extraParams) && extraParams.length > 0) {
            validateParams(extraParams);
            params.push(...extraParams);
        }

        const [rows, fields] = await connection.execute(execSql, params, { outFormat: oracledb.OUT_FORMAT_OBJECT });
        const fieldNames = fields ? fields.map(f => f.name) : Object.keys(rows[0] || {});

        return { ok: true, rows: rows.length, fields: fieldNames, sampleRows: rows, error: null };
    } catch (err) {
        const errorResult = handleError(err);
        return { 
            ok: false, 
            rows: 0, 
            fields: [], 
            sampleRows: [], 
            error: errorResult.error 
        };
    } finally {
        if (connection) await connection.close();
    }
}

// ============================================================
// 模式二：HTTP API 验证
// ============================================================

function httpPost(pathname, body, token) {
    return new Promise((resolve, reject) => {
        const url = new URL(pathname, config.api.base);
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
                catch (e) { reject(new ApiError(`HTTP parse error: ${data.substring(0, 100)}`)); }
            });
        });
        req.on('error', reject);
        req.write(postData);
        req.end();
    });
}

// Token 缓存：避免连续调用时重复 login
let _cachedToken = null;

async function getApiToken() {
    if (_cachedToken) return _cachedToken;
    const authConfig = config.security.apiAuth || {};
    const username = authConfig.username || 'admin@wisdomidata';
    const password = authConfig.password;

    if (!password) {
        throw new ApiError('API: password not configured in security.apiAuth');
    }

    const passwordField = config.api.loginPasswordEncrypt ? aesEncrypt(password) : password;
    const r = await httpPost('/api/auth/jwt/token', { userName: username, password: passwordField, lastTenantId: null });
    if (!r.data) throw new ApiError('API: failed to get token');
    _cachedToken = r.data;
    return _cachedToken;
}

async function verifyByApi(sql, { params = [] } = {}) {
    try {
        // 验证 SQL
        validateSql(sql);
        // 验证参数
        if (params && params.length > 0) {
            validateParams(params);
        }
        
        const { ciphertext, iv } = encrypt(sql);
        const token = await getApiToken();
        const r = await httpPost('/api/dashboard/nl2sql/execute', {
            encryptedSql: ciphertext, iv, params, description: 'verify'
        }, token);
        if (r.data?.error) {
            throw new ApiError(`API error: ${r.data.error}`);
        }
        return {
            ok: true,
            rows: r.data?.data?.length || 0,
            fields: r.data?.fields || [],
            error: null
        };
    } catch (err) {
        const errorResult = handleError(err);
        return { 
            ok: false, 
            rows: 0, 
            error: errorResult.error 
        };
    }
}

// ============================================================
// HTML 批量端到端验证
// ============================================================

const fs = require('fs');

/**
 * 从 HTML 中提取 CHART_CONFIG 的 id 和 scope
 */
function parseChartConfig(html) {
    const match = html.match(/const CHART_CONFIG = \[([\s\S]*?)\];/);
    if (!match) return [];
    const block = match[1];
    const results = [];
    // 提取每个对象的 id 和 scope
    const entryRe = /\"id\":\s*\"([^\"]+)\"[^}]+\"scope\":\s*\"([^\"]+)\"/g;
    let m;
    while ((m = entryRe.exec(block)) !== null) {
        results.push({ id: m[1], scope: m[2] });
    }
    return results;
}

/**
 * 批量端到端验证：解析 HTML，对每条 SQL 调后端 API 验证
 *
 * @param {string} htmlPath - HTML 文件路径
 * @param {{ projectId?: number, verbose?: boolean }} options
 * @returns {Promise<{ passed, failed, skipped, results: Record<string,object> }>}
 */
async function batchVerifyHtml(htmlPath, { projectId = null, verbose = true } = {}) {
    const html = fs.readFileSync(htmlPath, 'utf-8');

    const encResult = extractJsonFromAssignment(html, 'ENCRYPTED_SQL');
    const plainResult = extractJsonFromAssignment(html, 'SQL_PLAIN');
    const chartConfigs = parseChartConfig(html);
    const chartMap = Object.fromEntries(chartConfigs.map(c => [c.id, c]));

    if (encResult.error || plainResult.error) {
        throw new Error(`HTML 解析失败: ENCRYPTED_SQL=${encResult.error}, SQL_PLAIN=${plainResult.error}`);
    }

    const encryptedSql = encResult.data;
    const sqlPlain = plainResult.data;
    const encKeys = Object.keys(encryptedSql);

    if (verbose) {
        console.log(`\n=== HTML 端到端验证 (batchVerifyHtml) ===`);
        console.log(`  文件: ${htmlPath}`);
        console.log(`  SQL 数量: ${encKeys.length}`);
    }

    const results = {};
    let passed = 0, failed = 0, skipped = 0;

    for (const id of encKeys) {
        const enc = encryptedSql[id];
        const sql = sqlPlain[id] || '';
        const cfg = chartMap[id] || {};
        const scope = cfg.scope || 'project';

        // 统计 ? 占位符数量
        const placeholderCount = (sql.match(/\?/g) || []).length;

        // scope=project → 需要 projectId 作为 params[0]
        const params = (scope === 'project' && projectId) ? [projectId] : [];
        let status, msg, rows = 0;
        try {
            const token = await getApiToken();
            const r = await httpPost('/api/dashboard/nl2sql/execute', {
                encryptedSql: enc.ciphertext,
                iv: enc.iv,
                params,
                description: id
            }, token);

            if (r.data?.error) {
                status = 'FAIL';
                msg = r.data.error;
            } else {
                status = 'PASS';
                msg = `${(r.data?.data || []).length} rows`;
                rows = (r.data?.data || []).length;
            }
        } catch (err) {
            status = 'FAIL';
            msg = err.message || String(err);
        }

        results[id] = { status, msg, rows, scope, placeholderCount };

        if (status === 'PASS') passed++;
        else if (status === 'FAIL') failed++;
        else skipped++;

        if (verbose) {
            const icon = status === 'PASS' ? '✅' : status === 'SKIP' ? '⏭️' : '❌';
            console.log(`  ${icon} [${id}] (${scope}) ?=${placeholderCount}: ${status} — ${msg}`);
        }
    }

    if (verbose) {
        console.log(`\n  📊 汇总: ✅ ${passed} 通过, ❌ ${failed} 失败, ⏭️ ${skipped} 跳过`);
    }

    return { passed, failed, skipped, results };
}

// ============================================================
// 统一验证入口
// ============================================================

/**
 * 统一验证（推荐入口）
 *
 * @param {string} sql - 要验证的 SQL（不含 TENANT_ID 条件，后端自动注入）
 * @param {{ projectId?, extraParams?, source?: 'db'|'api'|'unified', dbType?: string }} options
 * @returns {Promise<{ ok, rows, fields, sampleRows, sources, error }>}
 */
async function verify(sql, options = {}) {
    const {
        projectId = null,
        extraParams = null,
        source = 'unified',  // DB 直连 + API 同时验证；不传 source 时默认 unified
        dbType = config.db.type    // 数据库类型：mysql | oracle | dm
    } = options;

    try {
        // 验证 SQL
        validateSql(sql);
        
        if (source === 'db') {
            const result = await verifyByDb(sql, { projectId, extraParams, dbType });
            const label = dbType === 'oracle' ? 'oracle' : 'mysql';
            if (result.ok) {
                return okResult({ ...result, sources: { [label]: result } });
            } else {
                const suggestion = getErrorSuggestion(result.error, sql, dbType);
                return failResult(result.error, { [label]: result }, suggestion);
            }
        }

        if (source === 'api') {
            const result = await verifyByApi(sql, {
                params: [projectId, ...(extraParams || [])].filter(v => v !== null && v !== undefined)
            });
            if (result.ok) {
                return okResult({ ...result, sources: { api: result } });
            } else {
                const suggestion = getErrorSuggestion(result.error, sql, dbType);
                return failResult(result.error, { api: result }, suggestion);
            }
        }

        // unified: 目标数据库为主，api 为备
        // DB 类型不支持 mysql2 时（oracle/dm），给 DB 验证加 5 秒超时，超时则跳过
        const DB_TIMEOUT_MS = (dbType === 'oracle' || dbType === 'dm') ? 5000 : 30000;
        const dbPromise = verifyByDb(sql, { projectId, extraParams, dbType });
        const apiPromise = verifyByApi(sql, {
            params: [projectId, ...(extraParams || [])].filter(v => v !== null && v !== undefined)
        });

        const timeoutPromise = new Promise(resolve =>
            setTimeout(() => resolve({ ok: false, error: 'DB验证超时（已跳过）', skipped: true }), DB_TIMEOUT_MS)
        );

        const dbResult = await Promise.race([dbPromise, timeoutPromise]);
        const apiResult = await apiPromise;

        const sources = { [dbType]: dbResult, api: apiResult };
        if (dbResult.ok) {
            return okResult({ rows: dbResult.rows, fields: dbResult.fields, sampleRows: dbResult.sampleRows, sources });
        } else if (apiResult.ok) {
            // DB 失败但 API 通过：视为通过（DB 驱动不可用时 fallback 到 API）
            const warn = dbResult.skipped ? `[${dbType}] DB验证超时，已 fallback 到 API` : `[${dbType}] DB验证失败: ${dbResult.error}，已 fallback 到 API`;
            console.warn(`  ⚠️ ${warn}`);
            return okResult({ rows: apiResult.rows, fields: apiResult.fields || [], sampleRows: apiResult.sampleRows || [], sources });
        } else {
            const suggestion = getErrorSuggestion(dbResult.error || apiResult.error, sql, dbType);
            return failResult(`DB: ${dbResult.error || 'timeout'}；API: ${apiResult.error}`, sources, suggestion);
        }
    } catch (err) {
        const errorResult = handleError(err);
        const suggestion = getErrorSuggestion(errorResult.error, sql, dbType);
        return failResult(errorResult.error, {}, suggestion);
    }
}

// ============================================================
// CLI 入口
// ============================================================

function parseArgs() {
    const args = process.argv.slice(2);
    const config = {
        sql: null, source: 'db', projectId: null,
        extraParams: null, output: 'json', help: false
    };
    for (let i = 0; i < args.length; i++) {
        const arg = args[i];
        if (arg === '--sql' || arg === '-s') config.sql = args[++i];
        else if (arg === '--source') config.source = args[++i];
        else if (arg === '--db-type' || arg === '-d') config.dbType = args[++i];
        else if (arg === '--tenant-id' || arg === '-t') { /* no-op: tenantId 由后端自动注入 */ }
        else if (arg === '--project-id' || arg === '-p') config.projectId = Number(args[++i]);
        else if (arg === '--params' || arg === '-P') {
            try { config.extraParams = JSON.parse(args[++i]); } catch { config.extraParams = args[++i].split(','); }
        } else if (arg === '--output') config.output = args[++i];
        else if (arg === '--help' || arg === '-h') config.help = true;
        else if (!arg.startsWith('--') && !config.sql) config.sql = arg;
    }
    return config;
}

async function main() {
    const config = parseArgs();
    if (config.help) {
        console.log(`
verifySql.js — NL2SQL 统一验证引擎

用法:
  node verifySql.js [--db-type mysql|oracle|dm] [--source db|api|unified]
    [--sql "SELECT ..."] [--project-id <id>] [--params <json>]

示例:
  node verifySql.js "SELECT * FROM wsd_plan_task LIMIT 3"
  node verifySql.js --db-type oracle "SELECT * FROM wsd_plan_task WHERE ROWNUM <= 3"
  node verifySql.js --db-type dm "SELECT * FROM wsd_plan_task LIMIT 3 OFFSET 0"
  node verifySql.js --source unified --sql "SELECT ..." --project-id 61

--db-type 说明:
  mysql   : MySQL（默认）
  oracle  : Oracle（需安装 oracledb 包）
  dm      : 达梦数据库

--source 说明:
  db      : 直连数据库（默认，支持 MySQL、Oracle、达梦）
  api     : 调 HTTP API
  unified : 同时尝试两者，以目标数据库为准
`);
        process.exit(0);
    }

    if (!config.sql) {
        console.error('错误: 请提供 --sql 参数');
        process.exit(1);
    }

    const result = await verify(config.sql, {
        projectId: config.projectId,
        extraParams: config.extraParams,
        source: config.source,
        dbType: config.dbType || process.env.DB_TYPE || 'mysql'
    });

    if (config.output === 'json') {
        console.log(JSON.stringify(result, null, 2));
    } else {
        if (result.ok) {
            console.log(`✅ OK | ${result.rows} rows | fields: ${result.fields.join(', ')}`);
        } else {
            console.log(`❌ FAIL | ${result.error}`);
        }
        for (const [src, sr] of Object.entries(result.sources || {})) {
            const sym = sr.ok ? '✅' : '❌';
            console.log(`  ${sym} ${src}: ${sr.error || `${sr.rows} rows`}`);
        }
    }
    process.exit(result.ok ? 0 : 1);
}

// 只有直接运行 CLI 时才执行 main()
// 被 require 时不触发 CLI
if (require.main === module) {
    main();
}

module.exports = { verify, verifyByMysql, verifyByApi, batchVerifyHtml, closePool };
