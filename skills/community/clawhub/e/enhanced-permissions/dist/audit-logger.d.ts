/**
 * Audit Logger Implementation
 * Records all DANGEROUS and DESTRUCTIVE operations
 */
import { PermissionLevel, AuditLogEntry } from './types';
/**
 * Audit Logger Class
 */
export declare class AuditLogger {
    private logFilePath;
    private buffer;
    private flushInterval;
    constructor(logFilePath?: string);
    log(entry: Omit<AuditLogEntry, 'timestamp'>): Promise<void>;
    getRecent(limit?: number): Promise<AuditLogEntry[]>;
    search(query: {
        operation?: string;
        riskLevel?: PermissionLevel;
        sessionId?: string;
        fromDate?: string;
        toDate?: string;
    }): Promise<AuditLogEntry[]>;
    exportToJson(filePath: string): Promise<void>;
    flush(): Promise<void>;
    private flushSync;
    private formatEntry;
    private startAutoFlush;
    private sendAlert;
    private parseLogFile;
    /**
     * Add entry to buffer (for testing)
     */
    addEntryToBuffer(entry: AuditLogEntry): void;
    /**
     * Get buffer entries (for testing)
     */
    getBufferEntries(): AuditLogEntry[];
    clear(): void;
}
export declare const defaultAuditLogger: AuditLogger;
//# sourceMappingURL=audit-logger.d.ts.map