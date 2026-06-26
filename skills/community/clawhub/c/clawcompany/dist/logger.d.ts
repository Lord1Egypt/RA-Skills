/**
 * 日志系统
 */
export declare enum LogLevel {
    DEBUG = 0,
    INFO = 1,
    WARN = 2,
    ERROR = 3
}
export declare class Logger {
    private level;
    private prefix;
    constructor(prefix?: string, level?: LogLevel);
    setLevel(level: LogLevel): void;
    debug(message: string, ...args: any[]): void;
    info(message: string, ...args: any[]): void;
    warn(message: string, ...args: any[]): void;
    error(message: string, error?: Error): void;
    success(message: string): void;
    step(step: number, total: number, message: string): void;
}
export declare const logger: Logger;
