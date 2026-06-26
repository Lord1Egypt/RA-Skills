import { v4 as uuidv4 } from 'uuid';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { loadConfig } from '../config/loader.js';
let activeSession = null;
export function createSecureSession(site, maxDurationMs) {
    const config = loadConfig();
    const id = `bs-${Date.now()}-${uuidv4().slice(0, 8)}`;
    const workDir = path.join(os.tmpdir(), `browser-secure-${id}`);
    const screenshotDir = path.join(workDir, 'screenshots');
    // Create isolated work directory
    if (config.isolation.secureWorkdir) {
        fs.mkdirSync(screenshotDir, { recursive: true });
    }
    activeSession = {
        id,
        workDir,
        screenshotDir,
        startTime: Date.now(),
        maxDuration: maxDurationMs || config.security.defaultTtl * 1000,
        site
    };
    return activeSession;
}
export function getActiveSession() {
    return activeSession;
}
export function isSessionExpired() {
    if (!activeSession)
        return true;
    const elapsed = Date.now() - activeSession.startTime;
    return elapsed > activeSession.maxDuration;
}
export function getSessionTimeRemaining() {
    if (!activeSession)
        return 0;
    const elapsed = Date.now() - activeSession.startTime;
    return Math.max(0, activeSession.maxDuration - elapsed);
}
export function secureCleanup() {
    if (!activeSession)
        return true;
    const config = loadConfig();
    let success = true;
    if (config.isolation.autoCleanup && config.isolation.secureWorkdir) {
        try {
            // Secure wipe: overwrite files before deletion
            secureWipeDirectory(activeSession.workDir);
            // Remove directory
            fs.rmSync(activeSession.workDir, { recursive: true, force: true });
        }
        catch (e) {
            console.error(`Cleanup warning: ${e}`);
            success = false;
        }
    }
    activeSession = null;
    return success;
}
function secureWipeDirectory(dir) {
    try {
        const entries = fs.readdirSync(dir, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);
            if (entry.isDirectory()) {
                secureWipeDirectory(fullPath);
            }
            else {
                // Overwrite file with random data before deletion
                const size = fs.statSync(fullPath).size;
                const randomData = Buffer.alloc(size);
                for (let i = 0; i < 3; i++) { // 3 passes
                    fs.writeFileSync(fullPath, randomData);
                }
            }
        }
    }
    catch (e) {
        // Best effort - continue with deletion even if wipe fails
    }
}
export function getScreenshotPath(actionIndex, action) {
    if (!activeSession) {
        throw new Error('No active session');
    }
    const paddedIndex = String(actionIndex).padStart(3, '0');
    const safeAction = action.replace(/[^a-z0-9]/gi, '_').slice(0, 30);
    return path.join(activeSession.screenshotDir, `${activeSession.id}-${paddedIndex}-${safeAction}.png`);
}
export function setupTimeoutWatcher(onTimeout) {
    if (!activeSession)
        return;
    const checkInterval = setInterval(() => {
        if (!activeSession) {
            clearInterval(checkInterval);
            return;
        }
        if (isSessionExpired()) {
            clearInterval(checkInterval);
            console.log('\n⚠️  Session timed out. Closing browser...');
            onTimeout();
        }
    }, 5000); // Check every 5 seconds
}
