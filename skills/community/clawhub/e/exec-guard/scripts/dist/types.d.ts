/**
 * 类型定义
 * 包含请求、响应、进程状态等核心接口
 */
/**
 * 命令执行请求结构
 */
export interface ExecRequest {
    /** 要执行的系统命令（必填） */
    command: string;
    /** 工作目录，默认为当前目录（可选） */
    workingDir?: string;
    /** 超时时间（秒），默认 30 秒（可选） */
    timeoutSeconds?: number;
    /** 是否后台运行，默认 false（可选） */
    runInBackground?: boolean;
    /** 监控窗口时长（秒），仅后台模式有效 */
    watchDurationSeconds?: number;
    /** 自定义环境变量（可选） */
    env?: Record<string, string>;
}
/**
 * 命令执行响应结构
 */
export interface ExecResponse {
    /** 执行状态：success/failed/timeout/killed/running */
    status: string;
    /** 进程退出码，-1 表示异常或运行中 */
    exitCode: number;
    /** 标准输出（已截断处理，使用 Head-Tail 双端缓冲） */
    stdout: string;
    /** 标准错误（已截断处理，使用 Head-Tail 双端缓冲） */
    stderr: string;
    /** 系统消息/错误详情 */
    systemMessage: string;
}
/**
 * 后台进程状态
 */
export interface ProcessStatus {
    /** 进程 ID */
    pid: number;
    /** 进程状态：running/completed/failed */
    status: string;
    /** 退出码 */
    exitCode: number;
    /** 执行的命令 */
    command: string;
    /** 启动时间 */
    startTime: string;
    /** 结束时间（完成后填充） */
    endTime?: string;
    /** 监控窗口时长（如果设置了） */
    watchDurationSeconds?: number;
    /** 监控窗口是否已完成 */
    watchCompleted?: boolean;
}
/**
 * 后台进程完整信息（含输出）
 */
export interface ProcessInfo extends ProcessStatus {
    /** 标准输出（Head-Tail 双端缓冲拼接结果） */
    stdout: string;
    /** 标准错误（Head-Tail 双端缓冲拼接结果） */
    stderr: string;
}
/**
 * 后台进程内部结构
 */
export interface BackgroundProcess {
    /** 进程 ID */
    pid: number;
    /** 执行的命令 */
    command: string;
    /** 启动时间 */
    startTime: Date;
    /** 结束时间 */
    endTime?: Date;
    /** 进程状态 */
    status: string;
    /** 退出码 */
    exitCode: number;
    /** 监控窗口时长（秒） */
    watchDuration: number;
    /** 监控窗口是否已完成 */
    watchCompleted: boolean;
    /** 执行错误 */
    error?: Error;
    /** 子进程对象 */
    childProcess?: import('child_process').ChildProcess;
    /** 取消回调 */
    cancelCallback?: () => void;
}
/**
 * 流读取结果
 */
export interface ReadResult {
    /** 读取的数据（已拼接） */
    data: string;
    /** 总共读取的字节数（原始大小） */
    totalRead: number;
    /** 是否被截断 */
    truncated: boolean;
    /** 被丢弃的字节数 */
    omittedBytes: number;
}
/**
 * HTTP 错误响应
 */
export interface HttpErrorResponse {
    error: string;
}
/**
 * HTTP 成功响应
 */
export interface HttpSuccessResponse {
    status: string;
    message: string;
}
/**
 * 健康检查响应
 */
export interface HealthResponse {
    status: string;
}
//# sourceMappingURL=types.d.ts.map