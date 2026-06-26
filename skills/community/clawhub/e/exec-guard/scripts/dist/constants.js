"use strict";
/**
 * 常量定义
 * 包含默认配置、缓冲区大小、状态常量、错误类型
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.ErrInvalidWorkingDir = exports.ErrProcessAlreadyExists = exports.ErrTimeoutExceeded = exports.ErrProcessNotFound = exports.ErrEmptyCommand = exports.MaxProcessesReachedError = exports.InvalidWorkingDirError = exports.ProcessAlreadyExistsError = exports.TimeoutExceededError = exports.ProcessNotFoundError = exports.EmptyCommandError = exports.ExecGuardError = exports.PROCESS_STATUS_FAILED = exports.PROCESS_STATUS_COMPLETED = exports.PROCESS_STATUS_RUNNING = exports.STATUS_RUNNING = exports.STATUS_KILLED = exports.STATUS_TIMEOUT = exports.STATUS_FAILED = exports.STATUS_SUCCESS = exports.TRUNCATE_PLACEHOLDER = exports.DEFAULT_MAX_PROCESSES = exports.DEFAULT_HTTP_PORT = exports.TRUNCATE_TAIL_BYTES = exports.TRUNCATE_HEAD_BYTES = exports.MAX_OUTPUT_BYTES = exports.DEFAULT_TIMEOUT_SECONDS = void 0;
// 默认配置常量
exports.DEFAULT_TIMEOUT_SECONDS = 30;
exports.MAX_OUTPUT_BYTES = 8192; // 8KB
exports.TRUNCATE_HEAD_BYTES = 4096; // 4KB
exports.TRUNCATE_TAIL_BYTES = 4096; // 4KB
exports.DEFAULT_HTTP_PORT = 8080;
exports.DEFAULT_MAX_PROCESSES = 100;
// 截断提示模板
exports.TRUNCATE_PLACEHOLDER = '\n... [TRUNCATED: %d bytes omitted] ...\n';
// 执行状态常量
exports.STATUS_SUCCESS = 'success';
exports.STATUS_FAILED = 'failed';
exports.STATUS_TIMEOUT = 'timeout';
exports.STATUS_KILLED = 'killed';
exports.STATUS_RUNNING = 'running';
// 后台进程状态常量
exports.PROCESS_STATUS_RUNNING = 'running';
exports.PROCESS_STATUS_COMPLETED = 'completed';
exports.PROCESS_STATUS_FAILED = 'failed';
// 预定义错误类
class ExecGuardError extends Error {
    constructor(message) {
        super(message);
        this.name = 'ExecGuardError';
    }
}
exports.ExecGuardError = ExecGuardError;
class EmptyCommandError extends ExecGuardError {
    constructor() {
        super('command cannot be empty');
        this.name = 'EmptyCommandError';
    }
}
exports.EmptyCommandError = EmptyCommandError;
class ProcessNotFoundError extends ExecGuardError {
    constructor(pid) {
        super(pid ? `process ${pid} not found` : 'process not found');
        this.name = 'ProcessNotFoundError';
    }
}
exports.ProcessNotFoundError = ProcessNotFoundError;
class TimeoutExceededError extends ExecGuardError {
    constructor(timeout) {
        super(timeout ? `execution timeout exceeded (${timeout}s)` : 'execution timeout exceeded');
        this.name = 'TimeoutExceededError';
    }
}
exports.TimeoutExceededError = TimeoutExceededError;
class ProcessAlreadyExistsError extends ExecGuardError {
    constructor(pid) {
        super(`process ${pid} already exists`);
        this.name = 'ProcessAlreadyExistsError';
    }
}
exports.ProcessAlreadyExistsError = ProcessAlreadyExistsError;
class InvalidWorkingDirError extends ExecGuardError {
    constructor(dir) {
        super(`invalid working directory: ${dir}`);
        this.name = 'InvalidWorkingDirError';
    }
}
exports.InvalidWorkingDirError = InvalidWorkingDirError;
class MaxProcessesReachedError extends ExecGuardError {
    constructor(max) {
        super(`max process limit reached: ${max}`);
        this.name = 'MaxProcessesReachedError';
    }
}
exports.MaxProcessesReachedError = MaxProcessesReachedError;
// 导出错误实例（便于直接使用）
exports.ErrEmptyCommand = new EmptyCommandError();
exports.ErrProcessNotFound = new ProcessNotFoundError();
exports.ErrTimeoutExceeded = new TimeoutExceededError();
exports.ErrProcessAlreadyExists = new ProcessAlreadyExistsError(0);
exports.ErrInvalidWorkingDir = new InvalidWorkingDirError('');
//# sourceMappingURL=constants.js.map