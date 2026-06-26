import fs from 'fs';
import path from 'path';
import os from 'os';
import { getCurrentSessionId } from '../security/audit.js';
const ERROR_LOG_FILE = '.browser-secure/error.log';
const ERROR_LOG_ROTATE_SIZE_MB = 10;
function getErrorLogPath() {
    return path.join(os.homedir(), ERROR_LOG_FILE);
}
function getErrorLogRotatePath() {
    return path.join(os.homedir(), '.browser-secure/error.log.old');
}
// ---------------------------------------------------------------------------
// Core logging API
// ---------------------------------------------------------------------------
/**
 * Log an error. Always writes to file (never throws).
 */
export function logError(errorType, message, options) {
    const entry = {
        timestamp: new Date().toISOString(),
        level: options?.level ?? 'ERROR',
        errorType,
        message,
        stack: options?.error?.stack,
        sessionId: getCurrentSessionId() ?? undefined,
        command: process.argv.slice(2).join(' ') || undefined,
        context: options?.context,
        recoverable: options?.recoverable ?? false,
    };
    writeErrorEntry(entry);
}
// ---------------------------------------------------------------------------
// Convenience wrappers for common error types
// ---------------------------------------------------------------------------
export function logLaunchError(msg, err, context) {
    logError('LaunchError', msg, { error: err, context, recoverable: false });
}
export function logNavigationError(url, msg, err, recoverable = false) {
    logError('NavigationError', msg, {
        error: err,
        context: { url },
        recoverable,
    });
}
export function logVaultError(msg, err, recoverable = false) {
    logError('VaultError', msg, { error: err, recoverable });
}
export function logApprovalError(msg, err) {
    logError('ApprovalError', msg, { error: err, recoverable: false });
}
export function logDaemonError(msg, err, recoverable = false) {
    logError('DaemonError', msg, { error: err, recoverable });
}
export function logCredentialError(msg, err, recoverable = false) {
    logError('CredentialError', msg, { error: err, recoverable });
}
export function logCAPTCHAError(url, msg, err) {
    logError('CAPTCHAError', msg, { error: err, context: { url }, recoverable: false });
}
export function logSessionError(msg, err) {
    logError('SessionError', msg, { error: err, recoverable: false });
}
// ---------------------------------------------------------------------------
// Write + rotate
// ---------------------------------------------------------------------------
function writeErrorEntry(entry) {
    try {
        const logPath = getErrorLogPath();
        const dir = path.dirname(logPath);
        if (!fs.existsSync(dir)) {
            fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
        }
        // Rotate if file is too large
        try {
            const stat = fs.statSync(logPath);
            if (stat.size > ERROR_LOG_ROTATE_SIZE_MB * 1024 * 1024) {
                if (fs.existsSync(getErrorLogRotatePath())) {
                    fs.unlinkSync(getErrorLogRotatePath());
                }
                fs.renameSync(logPath, getErrorLogRotatePath());
            }
        }
        catch { /* rotate check failed, proceed */ }
        const line = JSON.stringify(entry) + '\n';
        fs.appendFileSync(logPath, line, 'utf-8');
    }
    catch {
        // Never let logging itself throw — silently fail
    }
}
// ---------------------------------------------------------------------------
// Read / query
// ---------------------------------------------------------------------------
export function readErrorLog(options) {
    const logPath = getErrorLogPath();
    if (!fs.existsSync(logPath))
        return [];
    const content = fs.readFileSync(logPath, 'utf-8');
    const lines = content.trim().split('\n').filter(Boolean);
    let entries = lines.map(line => {
        try {
            return JSON.parse(line);
        }
        catch {
            return null;
        }
    }).filter(Boolean);
    if (options?.level) {
        entries = entries.filter(e => e.level === options.level);
    }
    if (options?.errorType) {
        entries = entries.filter(e => e.errorType === options.errorType);
    }
    if (options?.since) {
        const cutoff = new Date(options.since).getTime();
        entries = entries.filter(e => new Date(e.timestamp).getTime() >= cutoff);
    }
    if (options?.limit) {
        entries = entries.slice(-options.limit);
    }
    return entries;
}
export function getErrorStats() {
    const entries = readErrorLog({ limit: 1000 });
    const byType = {};
    const byLevel = {};
    for (const e of entries) {
        byType[e.errorType] = (byType[e.errorType] ?? 0) + 1;
        byLevel[e.level] = (byLevel[e.level] ?? 0) + 1;
    }
    return {
        total: entries.length,
        byType,
        byLevel,
        recent: entries.slice(-20),
    };
}
export function clearErrorLog() {
    const logPath = getErrorLogPath();
    if (fs.existsSync(logPath)) {
        fs.unlinkSync(logPath);
    }
    if (fs.existsSync(getErrorLogRotatePath())) {
        fs.unlinkSync(getErrorLogRotatePath());
    }
}
