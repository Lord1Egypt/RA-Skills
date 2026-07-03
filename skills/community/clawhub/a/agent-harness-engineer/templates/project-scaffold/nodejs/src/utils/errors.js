/**
 * ============================================
 * 类型: 核心框架
 * 模块: utils.errors
 * 说明: 错误定义
 * 修改建议: 如需扩展，添加新的错误类型
 * ============================================

class AgentError extends Error {
  constructor(message) {
    super(message);
    this.name = 'AgentError';
  }
}

class LLMError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'LLMError';
  }
}

class ToolError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'ToolError';
  }
}

class PermissionDeniedError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'PermissionDeniedError';
  }
}

class ContextOverflowError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'ContextOverflowError';
  }
}

class SessionNotFoundError extends AgentError {
  constructor(message) {
    super(message);
    this.name = 'SessionNotFoundError';
  }
}

module.exports = {
  AgentError,
  LLMError,
  ToolError,
  PermissionDeniedError,
  ContextOverflowError,
  SessionNotFoundError
};
