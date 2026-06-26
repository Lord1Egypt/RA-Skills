/**
 * 常量定义
 * 包含默认配置、缓冲区大小、状态常量、错误类型
 */
export declare const DEFAULT_TIMEOUT_SECONDS = 30;
export declare const MAX_OUTPUT_BYTES = 8192;
export declare const TRUNCATE_HEAD_BYTES = 4096;
export declare const TRUNCATE_TAIL_BYTES = 4096;
export declare const DEFAULT_HTTP_PORT = 8080;
export declare const DEFAULT_MAX_PROCESSES = 100;
export declare const TRUNCATE_PLACEHOLDER = "\n... [TRUNCATED: %d bytes omitted] ...\n";
export declare const STATUS_SUCCESS = "success";
export declare const STATUS_FAILED = "failed";
export declare const STATUS_TIMEOUT = "timeout";
export declare const STATUS_KILLED = "killed";
export declare const STATUS_RUNNING = "running";
export declare const PROCESS_STATUS_RUNNING = "running";
export declare const PROCESS_STATUS_COMPLETED = "completed";
export declare const PROCESS_STATUS_FAILED = "failed";
export declare class ExecGuardError extends Error {
    constructor(message: string);
}
export declare class EmptyCommandError extends ExecGuardError {
    constructor();
}
export declare class ProcessNotFoundError extends ExecGuardError {
    constructor(pid?: number);
}
export declare class TimeoutExceededError extends ExecGuardError {
    constructor(timeout?: number);
}
export declare class ProcessAlreadyExistsError extends ExecGuardError {
    constructor(pid: number);
}
export declare class InvalidWorkingDirError extends ExecGuardError {
    constructor(dir: string);
}
export declare class MaxProcessesReachedError extends ExecGuardError {
    constructor(max: number);
}
export declare const ErrEmptyCommand: EmptyCommandError;
export declare const ErrProcessNotFound: ProcessNotFoundError;
export declare const ErrTimeoutExceeded: TimeoutExceededError;
export declare const ErrProcessAlreadyExists: ProcessAlreadyExistsError;
export declare const ErrInvalidWorkingDir: InvalidWorkingDirError;
//# sourceMappingURL=constants.d.ts.map