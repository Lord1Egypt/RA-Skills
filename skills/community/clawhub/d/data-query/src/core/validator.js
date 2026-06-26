/**
 * validator.js — SQL 与参数校验
 *
 * 职责：对 SQL 文本和参数进行规则校验，校验失败抛出 ValidationError
 *
 * 导出：
 *   validateSql(sql)     — SQL 语法/长度/关键词校验
 *   validateParams(params) — 参数类型/长度校验
 *   validateConfig(cfg)   — 数据库配置完整性校验
 */
const { ValidationError } = require('./errors');

// SQL 验证规则
const SQL_RULES = {
  allowedKeywords: ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'GROUP', 'ORDER', 'LIMIT', 'OFFSET'],
  forbiddenKeywords: ['UPDATE', 'DELETE', 'INSERT', 'DROP', 'TRUNCATE', 'ALTER', 'CREATE', 'GRANT', 'REVOKE', 'EXEC', 'EXECUTE', 'CALL', 'INTO OUTFILE', 'INTO DUMPFILE'],
  maxLength: 10000,
  maxParameters: 50
};

// 验证 SQL 语句
function validateSql(sql) {
  if (!sql || typeof sql !== 'string' || sql.trim() === '') {
    throw new ValidationError('SQL 不能为空');
  }

  const trimmed = sql.trim();
  if (trimmed.length > SQL_RULES.maxLength) {
    throw new ValidationError(`SQL 长度不能超过 ${SQL_RULES.maxLength} 字符`);
  }

  const upperSql = trimmed.toUpperCase();
  if (!upperSql.startsWith('SELECT')) {
    throw new ValidationError('只允许 SELECT 查询');
  }

  // 检查禁用关键词
  for (const kw of SQL_RULES.forbiddenKeywords) {
    if (new RegExp(`\\b${kw}\\b`, 'i').test(sql)) {
      throw new ValidationError(`禁止使用关键词: ${kw}`);
    }
  }

  // 检查参数数量
  const paramCount = (sql.match(/\?/g) || []).length;
  if (paramCount > SQL_RULES.maxParameters) {
    throw new ValidationError(`参数数量不能超过 ${SQL_RULES.maxParameters} 个`);
  }

  return true;
}

// 验证参数
function validateParams(params) {
  if (!Array.isArray(params)) {
    throw new ValidationError('参数必须是数组');
  }

  for (let i = 0; i < params.length; i++) {
    const param = params[i];
    if (param === undefined || param === null) {
      throw new ValidationError(`参数 ${i} 不能为 null 或 undefined`);
    }
    // 检查参数类型
    if (typeof param === 'string' && param.length > 1000) {
      throw new ValidationError(`参数 ${i} 长度不能超过 1000 字符`);
    }
  }

  return true;
}

// 验证配置参数
function validateConfig(config) {
  if (!config) {
    throw new ValidationError('配置不能为空');
  }

  // 验证数据库配置
  if (config.db) {
    if (!config.db.host || !config.db.user || !config.db.password) {
      throw new ValidationError('数据库配置不完整');
    }
  }

  return true;
}

module.exports = {
  validateSql,
  validateParams,
  validateConfig
};