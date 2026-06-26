"use strict";
/**
 * Audit Logger Implementation
 * Records all DANGEROUS and DESTRUCTIVE operations
 */
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.defaultAuditLogger = exports.AuditLogger = void 0;
const fs = __importStar(require("fs/promises"));
const fsSync = __importStar(require("fs"));
const path = __importStar(require("path"));
const types_1 = require("./types");
/**
 * Audit Logger Class
 */
class AuditLogger {
    constructor(logFilePath) {
        this.buffer = [];
        this.flushInterval = null;
        // Use absolute path
        if (logFilePath) {
            this.logFilePath = path.isAbsolute(logFilePath) ? logFilePath : path.resolve(process.cwd(), logFilePath);
        }
        else {
            this.logFilePath = path.resolve(process.cwd(), 'memory', 'audit-log.md');
        }
        // Ensure directory exists
        const dir = path.dirname(this.logFilePath);
        fsSync.mkdirSync(dir, { recursive: true });
        console.log(`📋 Audit log path: ${this.logFilePath}`);
        this.startAutoFlush();
    }
    async log(entry) {
        const fullEntry = {
            ...entry,
            timestamp: new Date().toISOString()
        };
        this.buffer.push(fullEntry);
        if (entry.riskLevel === types_1.PermissionLevel.DESTRUCTIVE) {
            await this.flush();
            await this.sendAlert(fullEntry);
        }
        console.log(`📝 Audit: ${entry.operation} (${entry.riskLevel})`);
    }
    async getRecent(limit = 50) {
        try {
            // First check buffer
            if (this.buffer.length > 0) {
                console.log(`📋 Returning ${this.buffer.length} entries from buffer`);
                return this.buffer.slice(-limit);
            }
            // Then try file
            const content = await fs.readFile(this.logFilePath, 'utf-8');
            const entries = this.parseLogFile(content);
            console.log(`📋 Read ${entries.length} audit entries from file`);
            return entries.slice(-limit);
        }
        catch (error) {
            console.log(`⚠️ Could not read audit log: ${error.message}`);
            return [];
        }
    }
    async search(query) {
        const entries = await this.getRecent(1000);
        return entries.filter(entry => {
            if (query.operation && !entry.operation.includes(query.operation))
                return false;
            if (query.riskLevel && entry.riskLevel !== query.riskLevel)
                return false;
            if (query.sessionId && entry.sessionId !== query.sessionId)
                return false;
            if (query.fromDate && entry.timestamp < query.fromDate)
                return false;
            if (query.toDate && entry.timestamp > query.toDate)
                return false;
            return true;
        });
    }
    async exportToJson(filePath) {
        const entries = await this.getRecent(10000);
        await fs.writeFile(filePath, JSON.stringify(entries, null, 2), 'utf-8');
    }
    async flush() {
        if (this.buffer.length === 0)
            return;
        const entries = [...this.buffer];
        this.buffer = [];
        try {
            const dir = path.dirname(this.logFilePath);
            await fs.mkdir(dir, { recursive: true });
            const content = entries.map(e => this.formatEntry(e)).join('\n\n');
            await fs.appendFile(this.logFilePath, content + '\n\n', 'utf-8');
            console.log(`💾 Flushed ${entries.length} audit entries`);
        }
        catch (error) {
            console.error('❌ Failed to flush audit log:', error.message);
            this.buffer.unshift(...entries);
        }
    }
    flushSync() {
        if (this.buffer.length === 0)
            return;
        try {
            const content = this.buffer.map(e => this.formatEntry(e)).join('\n\n');
            fsSync.appendFileSync(this.logFilePath, content + '\n\n', 'utf-8');
        }
        catch {
            // Ignore errors on exit
        }
    }
    formatEntry(entry) {
        const date = new Date(entry.timestamp).toLocaleString('zh-CN');
        return [
            `#### ${entry.riskLevel === types_1.PermissionLevel.DESTRUCTIVE ? '🔴' : '🟠'} ${date}`,
            `- **Operation**: \`${entry.operation}\``,
            `- **Risk Level**: ${entry.riskLevel.toUpperCase()}`,
            `- **Session**: ${entry.sessionId}`,
            `- **User Confirmed**: ${entry.userConfirmed ? '✅ Yes' : '❌ No'}`,
            `- **Result**: ${entry.result.success ? '✅ Success' : '❌ Failed'}`,
            entry.result.error ? `- **Error**: ${entry.result.error}` : '',
            '',
            '**Parameters**:',
            '```json',
            JSON.stringify(entry.params, null, 2),
            '```'
        ].filter(line => line).join('\n');
    }
    startAutoFlush() {
        if (this.flushInterval)
            clearInterval(this.flushInterval);
        this.flushInterval = setInterval(() => this.flush().catch(console.error), 5 * 60 * 1000);
        process.on('exit', () => this.flushSync());
        process.on('SIGINT', () => { this.flushSync(); process.exit(0); });
    }
    async sendAlert(entry) {
        console.log(`🚨 ALERT: DESTRUCTIVE operation: ${entry.operation}`);
    }
    parseLogFile(content) {
        // Simple parser - just return empty for now
        // In production, would parse the markdown format
        return [];
    }
    /**
     * Add entry to buffer (for testing)
     */
    addEntryToBuffer(entry) {
        this.buffer.push(entry);
    }
    /**
     * Get buffer entries (for testing)
     */
    getBufferEntries() {
        return [...this.buffer];
    }
    clear() {
        this.buffer = [];
    }
}
exports.AuditLogger = AuditLogger;
exports.defaultAuditLogger = new AuditLogger();
//# sourceMappingURL=audit-logger.js.map