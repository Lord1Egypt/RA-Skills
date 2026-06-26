export type ErrorLevel = 'ERROR' | 'WARN' | 'INFO' | 'DEBUG';
export interface ErrorLogEntry {
    timestamp: string;
    level: ErrorLevel;
    errorType: string;
    message: string;
    stack?: string;
    sessionId?: string;
    command?: string;
    context?: Record<string, unknown>;
    recoverable: boolean;
}
/**
 * Log an error. Always writes to file (never throws).
 */
export declare function logError(errorType: string, message: string, options?: {
    error?: Error;
    level?: ErrorLevel;
    context?: Record<string, unknown>;
    recoverable?: boolean;
}): void;
export declare function logLaunchError(msg: string, err?: Error, context?: Record<string, unknown>): void;
export declare function logNavigationError(url: string, msg: string, err?: Error, recoverable?: boolean): void;
export declare function logVaultError(msg: string, err?: Error, recoverable?: boolean): void;
export declare function logApprovalError(msg: string, err?: Error): void;
export declare function logDaemonError(msg: string, err?: Error, recoverable?: boolean): void;
export declare function logCredentialError(msg: string, err?: Error, recoverable?: boolean): void;
export declare function logCAPTCHAError(url: string, msg: string, err?: Error): void;
export declare function logSessionError(msg: string, err?: Error): void;
export declare function readErrorLog(options?: {
    level?: ErrorLevel;
    errorType?: string;
    since?: string;
    limit?: number;
}): ErrorLogEntry[];
export declare function getErrorStats(): {
    total: number;
    byType: Record<string, number>;
    byLevel: Record<string, number>;
    recent: ErrorLogEntry[];
};
export declare function clearErrorLog(): void;
