/**
 * dialect.js — SQL 方言适配层
 *
 * 职责：将数据库特定语法（LIMIT、分页、字符串拼接、时间函数等）
 *       全部抽象到 Dialect 接口中，使核心 SQL 生成逻辑与数据库解耦。
 *
 * 使用方式：
 *   const { createDialect } = require('./dialect.js');
 *   const dialect = createDialect('mysql');  // mysql | oracle | dm
 *
 *   dialect.quote('field_name')     // `field_name` / "field_name"
 *   dialect.applyPagination(sql, 0, 20, 't.PLAN_END_TIME')
 *   dialect.concat('a', 'b')        // CONCAT(a,b) / a || b
 *   dialect.now()                  // NOW() / SYSDATE / SYSTIMESTAMP
 */

const DB_TYPE = process.env.DB_TYPE || process.env.DB_SOURCE || 'mysql';

// ============================================================
// 接口定义
// ============================================================

class SqlDialect {
    constructor(type) {
        this.type = type;
    }

    /** 标识符转义（字段名、表名） */
    quote(identifier) {
        throw new Error('Not implemented');
    }

    /** LIMIT 子句 */
    limit(sql, offset, count) {
        throw new Error('Not implemented');
    }

    /** 字符串拼接 */
    concat(...parts) {
        throw new Error('Not implemented');
    }

    /** 当前时间 */
    now() {
        throw new Error('Not implemented');
    }

    /** NULL 替换函数 */
    ifNull(expr, replacement) {
        throw new Error('Not implemented');
    }

    /** 日期减法：date - days */
    dateSub(date, days) {
        throw new Error('Not implemented');
    }

    /** 字符串截取 */
    substring(col, from, len) {
        throw new Error('Not implemented');
    }

    /** 类型转换：字符串转整数 */
    castToInt(expr) {
        throw new Error('Not implemented');
    }

    /**
     * 完整分页 SQL
     * @param {string} sql - 原始 SQL（已含 ORDER BY）
     * @param {number} offset - 偏移量
     * @param {number} count - 每页条数
     * @param {string} orderBy - 排序字段（如 't.PLAN_END_TIME'）
     */
    applyPagination(sql, offset, count, orderBy) {
        throw new Error('Not implemented');
    }

    /** 元数据查询 SQL（用于 generate_knowledge.py） */
    getMetadataQuery() {
        throw new Error('Not implemented');
    }

    /** 驱动类型名 */
    getDriverName() {
        return this.type;
    }

    /**
     * 移除 SQL 中的分页子句（用于验证时替换为固定 LIMIT）
     * @param {string} sql - 含分页的 SQL
     * @returns {string} - 移除分页后的基础 SQL
     */
    stripPagination(sql) {
        throw new Error('Not implemented');
    }
}

// ============================================================
// MySQL Dialect
// ============================================================

class MySqlDialect extends SqlDialect {
    constructor() {
        super('mysql');
    }

    quote(identifier) {
        return `\`${identifier}\``;
    }

    limit(sql, offset, count) {
        return `${sql} LIMIT ${offset}, ${count}`;
    }

    concat(...parts) {
        return `CONCAT(${parts.join(', ')})`;
    }

    now() {
        return 'NOW()';
    }

    ifNull(expr, replacement) {
        return `IFNULL(${expr}, ${replacement})`;
    }

    dateSub(date, days) {
        return `DATE_SUB(${date}, INTERVAL ${days} DAY)`;
    }

    substring(col, from, len) {
        return `SUBSTRING(${col}, ${from}, ${len})`;
    }

    castToInt(expr) {
        return `CAST(${expr} AS SIGNED)`;
    }

    applyPagination(sql, offset, count, orderBy) {
        // 幂等：先移除已有分页，再追加，避免叠加
        let base = this.stripPagination(sql);
        if (orderBy && !base.includes('ORDER BY')) {
            base = `${base} ORDER BY ${orderBy}`;
        }
        return this.limit(base, offset, count);
    }

    stripPagination(sql) {
        // 移除 MySQL LIMIT 和达梦兼容 LIMIT...OFFSET 形式
        return sql
            .replace(/\bLIMIT\s+\d+\s+OFFSET\s+\d+/i, '')          // DM: LIMIT n OFFSET m
            .replace(/\bLIMIT\s+\d+\s*(,\s*\d+)?\s*/i, '')         // MySQL: LIMIT n 或 LIMIT n, m
            .trim();
    }

    getMetadataQuery() {
        return `
            SELECT
                c.TABLE_NAME,
                c.COLUMN_NAME,
                c.COLUMN_TYPE,
                c.IS_NULLABLE,
                c.COLUMN_KEY,
                c.COLUMN_DEFAULT,
                c.COLUMN_COMMENT,
                t.TABLE_COMMENT
            FROM information_schema.COLUMNS c
            JOIN information_schema.TABLES t
              ON c.TABLE_NAME = t.TABLE_NAME AND c.TABLE_SCHEMA = t.TABLE_SCHEMA
            WHERE c.TABLE_SCHEMA = :schema
              AND t.TABLE_TYPE = 'BASE TABLE'
            ORDER BY c.TABLE_NAME, c.ORDINAL_POSITION
        `;
    }
}

// ============================================================
// Oracle Dialect
// ============================================================

class OracleDialect extends SqlDialect {
    constructor() {
        super('oracle');
    }

    quote(identifier) {
        return `"${identifier}"`;
    }

    limit(sql, offset, count) {
        // Oracle 分页由 applyPagination 统一处理，limit() 仅作占位
        return sql;
    }

    concat(...parts) {
        return parts.join(' || ');
    }

    now() {
        return 'SYSDATE';
    }

    ifNull(expr, replacement) {
        return `NVL(${expr}, ${replacement})`;
    }

    dateSub(date, days) {
        return `${date} - ${days}`;
    }

    substring(col, from, len) {
        return `SUBSTR(${col}, ${from}, ${len})`;
    }

    castToInt(expr) {
        return `TO_NUMBER(${expr})`;
    }

    applyPagination(sql, offset, count, orderBy) {
        // 幂等：先移除已有分页，再追加
        const base = this.stripPagination(sql);
        const start = offset + 1;
        const end = offset + count;
        const orderedSql = (orderBy && !base.includes('ORDER BY'))
            ? `${base} ORDER BY ${orderBy}`
            : base;
        return [
            `SELECT * FROM (`,
            `  SELECT t.*, ROWNUM rn FROM (`,
            `    ${orderedSql}`,
            `  ) t WHERE ROWNUM <= ${end}`,
            `) WHERE rn >= ${start}`
        ].join('\n');
    }

    stripPagination(sql) {
        // 移除 Oracle 三层分页子查询结构
        //
        // 结构：
        //   SELECT * FROM (                     ← 外层
        //     SELECT t.*, ROWNUM rn FROM (      ← 中层
        //       base_sql                        ← 目标
        //     ) t WHERE ROWNUM <= N
        //   ) WHERE rn >= M
        //
        // 思路：找到内层 base_sql 的起止位置并截取
        // 步骤：
        //   1. 找到外层闭括号 ) WHERE rn >= N
        //   2. 在其之前找 ) t WHERE ROWNUM <= N  → 中层结束
        //   3. 在 ) t 之前找最后一个 FROM (       → 内层开始
        //   4. 截取内层内容

        try {
            const norm = sql.replace(/\s+/g, ' ').trim();

            // 1. 外层闭括号
            const outerMatch = /\)\s*WHERE\s+rn\s*>='?\s*\d+'?\s*$/i.exec(norm);
            if (!outerMatch) return norm; // 兜底：没有标准分页结构
            const outerCloseIdx = outerMatch.index;

            // 2. 中层结束：在外层闭括号之前，找 ) t WHERE ROWNUM <= N
            const beforeOuter = norm.substring(0, outerCloseIdx);
            const middlePattern = /\)\s*[a-zA-Z0-9_]+\s*WHERE\s+ROWNUM\s*<='?\s*\d+'?/i;
            const middleMatch = middlePattern.exec(beforeOuter);
            if (!middleMatch) return norm; // 兜底
            const middleCloseIdx = middleMatch.index;

            // 3. 内层开始：在中层结束之前，找最后一个 FROM (
            const beforeMiddle = beforeOuter.substring(0, middleCloseIdx);
            // 从后往前找 FROM (
            const fromMatches = [...beforeMiddle.matchAll(/FROM\s*\(/gi)];
            if (fromMatches.length === 0) return norm;
            const lastFrom = fromMatches[fromMatches.length - 1];
            const innerStart = lastFrom.index + lastFrom[0].length;

            // 4. 内层结束 = middleCloseIdx
            const baseSql = beforeMiddle.substring(innerStart);
            return baseSql.trim();
        } catch (error) {
            // 任何错误都返回原始 SQL，确保函数的鲁棒性
            return sql;
        }
    }


    getMetadataQuery() {
        return `
            SELECT
                utc.table_name,
                utc.column_name,
                utc.data_type,
                CASE WHEN utc.nullable = 'Y' THEN 'YES' ELSE 'NO' END AS is_nullable,
                CASE WHEN utc.column_name IN (
                    SELECT ucc.column_name FROM user_constraints uc
                    JOIN user_cons_columns ucc ON uc.constraint_name = ucc.constraint_name
                    WHERE uc.table_name = utc.table_name AND uc.constraint_type = 'P'
                ) THEN 'PRI' ELSE NULL END AS column_key,
                utc.data_default,
                ucc.comments AS column_comment,
                utc.table_name
            FROM user_tab_columns utc
            LEFT JOIN user_col_comments ucc
              ON utc.table_name = ucc.table_name AND utc.column_name = ucc.column_name
            ORDER BY utc.table_name, utc.column_id
        `;
    }
}

// ============================================================
// 达梦（DM Database）Dialect
// ============================================================

// DM 保留字（列名如果命中这些词，必须加双引号）
const DM_RESERVED = new Set([
    'DATE', 'TIME', 'USER', 'ORDER', 'GROUP', 'INDEX', 'TABLE',
    'VIEW', 'NULL', 'TRUE', 'FALSE', 'ALL', 'ANY', 'SOME', 'KEY',
    'PRIMARY', 'FOREIGN', 'CHECK', 'UNIQUE', 'DEFAULT', 'CONSTRAINT',
    'EXISTS', 'BETWEEN', 'LIKE', 'IN', 'IS', 'AND', 'OR', 'NOT',
    'SELECT', 'FROM', 'WHERE', 'HAVING', 'JOIN', 'LEFT', 'RIGHT',
    'INNER', 'OUTER', 'ON', 'AS', 'DISTINCT', 'UNION', 'MINUS',
    'INTERSECT', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END', 'ASC', 'DESC',
    'DEL'
]);

class DmDialect extends SqlDialect {
    constructor() {
        super('dm');
    }

    quote(identifier) {
        // 达梦：只有保留字才需要加双引号，普通标识符不引号
        if (DM_RESERVED.has(identifier.toUpperCase())) {
            return `"${identifier}"`;
        }
        return identifier;
    }

    limit(sql, offset, count) {
        return `${sql} LIMIT ${count} OFFSET ${offset}`;
    }

    concat(...parts) {
        // 达梦兼容 || 和 CONCAT
        return parts.join(' || ');
    }

    now() {
        return 'SYSTIMESTAMP';
    }

    ifNull(expr, replacement) {
        // 达梦兼容 IFNULL
        return `IFNULL(${expr}, ${replacement})`;
    }

    dateSub(date, days) {
        return `${date} - ${days}`;
    }

    substring(col, from, len) {
        return `SUBSTR(${col}, ${from}, ${len})`;
    }

    castToInt(expr) {
        return `CAST(${expr} AS INT)`;
    }

    applyPagination(sql, offset, count, orderBy) {
        // 幂等：先移除已有分页，再追加
        let base = this.stripPagination(sql);
        if (orderBy && !base.includes('ORDER BY')) {
            base = `${base} ORDER BY ${orderBy}`;
        }
        return this.limit(base, offset, count);
    }

    stripPagination(sql) {
        // 移除达梦分页：LIMIT count OFFSET offset 或 LIMIT offset, count
        return sql
            .replace(/\bLIMIT\s+\d+\s+OFFSET\s+\d+/i, '')
            .replace(/\bLIMIT\s+\d+\s*(,\s*\d+)?\s*/i, '')
            .trim();
    }

    getMetadataQuery() {
        // 达梦兼容 information_schema（DM7/8 兼容模式）
        return `
            SELECT
                c.TABLE_NAME,
                c.COLUMN_NAME,
                c.DATA_TYPE AS column_type,
                CASE WHEN c.NULLABLE = 'YES' THEN 'YES' ELSE 'NO' END AS is_nullable,
                CASE WHEN c.COLUMN_NAME IN (
                    SELECT cu.COLUMN_NAME FROM USER_CONSTRAINTS cs
                    JOIN USER_CONS_COLUMNS cu ON cs.CONSTRAINT_NAME = cu.CONSTRAINT_NAME
                    WHERE cs.TABLE_NAME = c.TABLE_NAME AND cs.CONSTRAINT_TYPE = 'P'
                ) THEN 'PRI' ELSE NULL END AS column_key,
                c.DATA_DEFAULT AS column_default,
                c.COMMENTS AS column_comment,
                t.COMMENTS AS table_comment
            FROM USER_TAB_COLUMNS c
            LEFT JOIN USER_TAB_COMMENTS t ON c.TABLE_NAME = t.TABLE_NAME
            ORDER BY c.TABLE_NAME, c.COLUMN_ID
        `;
    }
}

// ============================================================
// Factory
// ============================================================

const DIALECTS = {
    mysql: () => new MySqlDialect(),
    oracle: () => new OracleDialect(),
    dm: () => new DmDialect(),
    dameng: () => new DmDialect(), // 达梦别名
};

function createDialect(type) {
    const normalized = (type || DB_TYPE || 'mysql').toLowerCase();
    const factory = DIALECTS[normalized];
    if (!factory) {
        throw new Error(
            `不支持的数据库类型: ${type}，` +
            `可选: ${Object.keys(DIALECTS).join(', ')}`
        );
    }
    return factory();
}

module.exports = {
    createDialect,
    SqlDialect,
    MySqlDialect,
    OracleDialect,
    DmDialect,
};
