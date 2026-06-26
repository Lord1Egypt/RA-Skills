/**
 * 统一错误处理模块
 */

class SkillError extends Error {
  constructor(code, message) {
    super(message);
    this.code = code;
    this.name = "SkillError";
    Error.captureStackTrace(this, this.constructor);
  }
}

class ApiError extends SkillError {
  constructor(code, message) {
    super(code, message);
    this.name = "ApiError";
  }
}

class NetworkError extends SkillError {
  constructor(message) {
    super("NETWORK_ERROR", message);
    this.name = "NetworkError";
  }
}

class TimeoutError extends SkillError {
  constructor(message) {
    super("TIMEOUT_ERROR", message);
    this.name = "TimeoutError";
  }
}

class AuthError extends SkillError {
  constructor(message) {
    super("AUTH_ERROR", message);
    this.name = "AuthError";
  }
}

module.exports = {
  SkillError,
  ApiError,
  NetworkError,
  TimeoutError,
  AuthError,
};
