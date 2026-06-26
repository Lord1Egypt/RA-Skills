/**
 * errors.js — 错误类型定义与处理
 *
 * 职责：定义技能内所有错误类型，提供统一的错误处理入口
 *
 * 错误类层次：
 *   BaseError
 *   ├── ValidationError   — 参数/SQL/配置校验失败
 *   ├── DatabaseError     — 数据库连接或执行错误
 *   ├── ApiError          — HTTP API 调用失败
 *   └── ConfigurationError — 配置文件错误
 */

class BaseError extends Error {
  constructor(message, code, details = {}) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.details = details;
    Error.captureStackTrace(this, this.constructor);
  }
}

class ValidationError extends BaseError {
  constructor(message, details = {}) {
    super(message, 'VALIDATION_ERROR', details);
  }
}

class DatabaseError extends BaseError {
  constructor(message, details = {}) {
    super(message, 'DATABASE_ERROR', details);
  }
}

class ApiError extends BaseError {
  constructor(message, details = {}) {
    super(message, 'API_ERROR', details);
  }
}

class ConfigurationError extends BaseError {
  constructor(message, details = {}) {
    super(message, 'CONFIGURATION_ERROR', details);
  }
}

// 错误处理工具
function handleError(err) {
  if (err instanceof BaseError) {
    return {
      ok: false,
      error: err.message,
      code: err.code,
      details: err.details
    };
  }
  // 处理未知错误
  return {
    ok: false,
    error: err.message || 'Unknown error',
    code: 'UNKNOWN_ERROR',
    details: {}
  };
}

module.exports = {
  BaseError,
  ValidationError,
  DatabaseError,
  ApiError,
  ConfigurationError,
  handleError
};