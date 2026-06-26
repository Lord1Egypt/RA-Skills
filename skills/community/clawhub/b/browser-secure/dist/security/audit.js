import fs from 'fs';
import path from 'path';
import crypto from 'crypto';
import { getAuditLogPath, loadConfig } from '../config/loader.js';
let currentSession = null;
let previousHash = '';
export function startAuditSession(site) {
    const sessionId = `bs-${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;
    currentSession = {
        event: 'BROWSER_SECURE_SESSION',
        timestamp: new Date().toISOString(),
        sessionId,
        site,
        actions: [],
        session: {
            duration: 0,
            autoClosed: false,
            cleanupSuccess: false
        },
        chainHash: ''
    };
    previousHash = '';
    return sessionId;
}
export function logAction(action, details, options) {
    if (!currentSession) {
        throw new Error('No active audit session');
    }
    const actionEntry = {
        action,
        timestamp: new Date().toISOString(),
        details,
        ...options
    };
    currentSession.actions.push(actionEntry);
}
export function finalizeAuditSession(duration, cleanupSuccess) {
    if (!currentSession)
        return;
    currentSession.session.duration = duration;
    currentSession.session.autoClosed = true;
    currentSession.session.cleanupSuccess = cleanupSuccess;
    // Compute chain hash for tamper evidence
    const data = JSON.stringify(currentSession.actions);
    const actionHash = crypto.createHash('sha256').update(data).digest('hex');
    const chainData = {
        previousHash: previousHash || 'genesis',
        sessionId: currentSession.sessionId,
        timestamp: currentSession.timestamp,
        actionHash
    };
    currentSession.chainHash = crypto.createHash('sha256')
        .update(JSON.stringify(chainData))
        .digest('hex');
    // Write to audit log
    writeAuditLog(currentSession);
    // Send to webhook if configured
    sendAuditWebhook(currentSession);
    currentSession = null;
}
function writeAuditLog(session) {
    const logPath = getAuditLogPath();
    const logDir = path.dirname(logPath);
    if (!fs.existsSync(logDir)) {
        fs.mkdirSync(logDir, { recursive: true, mode: 0o700 });
    }
    const line = JSON.stringify(session) + '\n';
    // Create file with 0600 if missing; appendFileSync respects existing mode.
    if (!fs.existsSync(logPath)) {
        fs.writeFileSync(logPath, line, { encoding: 'utf-8', mode: 0o600 });
    }
    else {
        fs.appendFileSync(logPath, line, 'utf-8');
    }
}
async function sendAuditWebhook(session) {
    const config = loadConfig();
    const auditConfig = config.security.audit;
    // Check if webhook is enabled
    if (auditConfig.mode === 'file') {
        return;
    }
    const webhookUrl = auditConfig.webhook?.url;
    if (!webhookUrl) {
        return;
    }
    try {
        const headers = {
            'Content-Type': 'application/json',
            ...(auditConfig.webhook?.headers || {})
        };
        const response = await fetch(webhookUrl, {
            method: 'POST',
            headers,
            body: JSON.stringify(session)
        });
        if (!response.ok) {
            console.error(`Audit webhook failed: ${response.status} ${response.statusText}`);
        }
    }
    catch (e) {
        // Log but don't fail - audit to file already succeeded
        console.error(`Audit webhook error: ${e}`);
    }
}
export function readAuditLog(sessionId) {
    const logPath = getAuditLogPath();
    if (!fs.existsSync(logPath)) {
        return [];
    }
    const content = fs.readFileSync(logPath, 'utf-8');
    const lines = content.trim().split('\n').filter(Boolean);
    const sessions = lines.map(line => JSON.parse(line));
    if (sessionId) {
        return sessions.filter((s) => s.sessionId === sessionId);
    }
    return sessions;
}
export function getCurrentSessionId() {
    return currentSession?.sessionId || null;
}
export function rotateAuditLog(retentionDays) {
    const logPath = getAuditLogPath();
    if (!fs.existsSync(logPath))
        return;
    const cutoff = Date.now() - (retentionDays * 24 * 60 * 60 * 1000);
    const content = fs.readFileSync(logPath, 'utf-8');
    const lines = content.trim().split('\n').filter(Boolean);
    const recent = lines.filter(line => {
        try {
            const session = JSON.parse(line);
            const timestamp = new Date(session.timestamp).getTime();
            return timestamp > cutoff;
        }
        catch {
            return false;
        }
    });
    fs.writeFileSync(logPath, recent.join('\n') + '\n', { encoding: 'utf-8', mode: 0o600 });
}
