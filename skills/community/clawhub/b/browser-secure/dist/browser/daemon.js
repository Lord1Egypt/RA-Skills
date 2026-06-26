import { execFileSync, spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import os from 'os';
import { getChromeUserDataDir, copyChromeProfileToTemp } from './chrome-lifecycle.js';
// ---------------------------------------------------------------------------
// State file management
// ---------------------------------------------------------------------------
function getDaemonDir() {
    const dir = path.join(os.homedir(), '.browser-secure');
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true, mode: 0o700 });
    }
    return dir;
}
export function getDaemonStatePath() {
    return path.join(getDaemonDir(), 'daemon.json');
}
export function loadDaemonState() {
    const statePath = getDaemonStatePath();
    if (!fs.existsSync(statePath))
        return null;
    try {
        const content = fs.readFileSync(statePath, 'utf-8');
        const state = JSON.parse(content);
        if (state.version !== 1 || !state.pid || !state.wsUrl)
            return null;
        return state;
    }
    catch {
        return null;
    }
}
function saveDaemonState(state) {
    fs.writeFileSync(getDaemonStatePath(), JSON.stringify(state, null, 2), 'utf-8');
}
export function clearDaemonState() {
    const p = getDaemonStatePath();
    if (fs.existsSync(p))
        fs.unlinkSync(p);
}
export function isDaemonRunning(state) {
    const s = state ?? loadDaemonState();
    if (!s || !s.pid)
        return false;
    // process.kill(pid, 0) is a probe — sends no signal, throws if the
    // process is gone. Avoids shelling out to curl/ps.
    try {
        process.kill(s.pid, 0);
        return true;
    }
    catch {
        clearDaemonState();
        return false;
    }
}
// ---------------------------------------------------------------------------
// Chrome binary detection
// ---------------------------------------------------------------------------
function getChromePath() {
    const platform = process.platform;
    if (platform === 'darwin') {
        const p = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
        if (fs.existsSync(p))
            return p;
    }
    else if (platform === 'linux') {
        for (const p of ['/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium']) {
            if (fs.existsSync(p))
                return p;
        }
    }
    else if (platform === 'win32') {
        for (const p of [
            'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
            'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe',
        ]) {
            if (fs.existsSync(p))
                return p;
        }
    }
    return undefined;
}
// ---------------------------------------------------------------------------
// Wait for Chrome to expose WebSocket endpoint
// ---------------------------------------------------------------------------
async function waitForChromeReady(port, maxWaitMs = 20000) {
    const deadline = Date.now() + maxWaitMs;
    const jsonUrl = `http://localhost:${port}/json/version`;
    while (Date.now() < deadline) {
        try {
            const res = await fetch(jsonUrl);
            if (res.ok) {
                const data = await res.json();
                if (data.webSocketDebuggerUrl)
                    return data.webSocketDebuggerUrl;
            }
        }
        catch { /* not ready yet */ }
        await new Promise(r => setTimeout(r, 500));
    }
    return null;
}
export async function startDaemon(optsOrProfile) {
    const opts = typeof optsOrProfile === 'string' ? { profileId: optsOrProfile } : (optsOrProfile ?? {});
    if (isDaemonRunning()) {
        const existing = loadDaemonState();
        if (!opts.profileId || existing.profileId === opts.profileId) {
            console.log(`🔁 Daemon already running on profile: ${existing.profile} [${existing.profileId}]`);
            return { state: existing };
        }
        throw new Error(`Daemon already running with profile "${existing.profile}" [${existing.profileId}].\n` +
            `Close the current daemon first: browser-secure daemon stop\n` +
            `Then restart with the desired profile.`);
    }
    const profile = opts.profileId ?? 'Default';
    const realProfileDir = path.join(getChromeUserDataDir(), profile);
    if (!fs.existsSync(realProfileDir)) {
        throw new Error(`Chrome profile "${profile}" does not exist.\n` +
            `Create it first:  browser-secure profile --create "${profile}"`);
    }
    const chromePath = getChromePath();
    if (!chromePath) {
        throw new Error('System Chrome not found. Cannot start daemon.');
    }
    // Copy the real profile to a temp dir so we don't conflict with the user's
    // running Chrome and don't need to force-quit it.
    const userDataDir = copyChromeProfileToTemp(profile);
    // Allocate a random CDP port
    const port = 9222 + Math.floor(Math.random() * 1000);
    console.log(`🚀 Starting Chrome daemon...`);
    console.log(`   Profile: ${profile}`);
    console.log(`   Temp user data dir: ${userDataDir}`);
    console.log(`   CDP port: ${port}`);
    const profileArgs = profile === 'Default' ? [] : [`--profile-directory=${profile}`];
    const chromeArgs = [
        `--remote-debugging-port=${port}`,
        `--user-data-dir=${userDataDir}`,
        ...profileArgs,
        '--enable-automation',
        '--disable-gpu',
        '--disable-dev-shm-usage',
        '--disable-software-rasterizer',
        '--disable-webgl',
        '--disable-accelerated-2d-canvas',
    ];
    // Launch Chrome directly. On macOS we used to use `open -n`, but that
    // fails to pass args through when Chrome is already running. Spawning the
    // binary directly is more reliable.
    const child = spawn(chromePath, chromeArgs, { detached: true, stdio: 'ignore' });
    child.unref();
    // Wait for Chrome to expose the WebSocket URL
    const wsUrl = await waitForChromeReady(port, 20000);
    if (!wsUrl) {
        try {
            process.kill(child.pid, 0);
        }
        catch { /* */ }
        throw new Error('Chrome daemon failed to start.\n' +
            'Try: browser-secure daemon start --profile ' + profile);
    }
    // child.pid is the actual Chrome PID when we spawn the binary directly.
    const chromePid = child.pid ?? 0;
    const state = {
        version: 1,
        pid: chromePid,
        port,
        wsUrl,
        profile,
        profileId: profile,
        profilePath: userDataDir,
        startedAt: new Date().toISOString(),
        browserPath: chromePath,
    };
    saveDaemonState(state);
    console.log(`✅ Daemon started`);
    console.log(`   Profile: ${state.profile} [${state.profileId}]`);
    console.log(`   PID: ${state.pid}`);
    return { state };
}
export async function stopDaemon() {
    const state = loadDaemonState();
    if (!state) {
        console.log('No daemon running.');
        return;
    }
    // Kill the Chrome PID tracked at start (resolved via lsof on the debug port,
    // so it's the real Chrome process, not the `open` wrapper). Fall back to
    // looking up the pid on the CDP port if the tracked pid is stale.
    const chromePids = new Set();
    if (state.pid)
        chromePids.add(state.pid);
    try {
        const out = execFileSync('lsof', ['-i', `:${state.port}`, '-t'], {
            encoding: 'utf-8',
            stdio: ['ignore', 'pipe', 'ignore'],
        }).trim();
        for (const line of out.split('\n')) {
            const pid = parseInt(line, 10);
            if (!isNaN(pid))
                chromePids.add(pid);
        }
    }
    catch { /* port already free */ }
    for (const pid of chromePids) {
        try {
            process.kill(pid, 'SIGTERM');
        }
        catch (_) { /* */ }
    }
    if (chromePids.size > 0) {
        await new Promise(r => setTimeout(r, 2000));
        for (const pid of chromePids) {
            try {
                process.kill(pid, 'SIGKILL');
            }
            catch (_) { /* */ }
        }
    }
    // Clean up temp profile dir
    if (state.profilePath) {
        try {
            fs.rmSync(state.profilePath, { recursive: true, force: true });
        }
        catch { /* */ }
    }
    clearDaemonState();
    console.log('🛑 Daemon stopped.');
}
export function getDaemonStatus() {
    const state = loadDaemonState();
    if (!state || !isDaemonRunning(state))
        return null;
    return state;
}
export function printDaemonStatus() {
    const state = loadDaemonState();
    if (!state) {
        console.log('Daemon: NOT RUNNING');
        return;
    }
    if (!isDaemonRunning(state)) {
        console.log('Daemon: STALE (run: browser-secure daemon stop to clean up)');
        return;
    }
    const elapsed = Math.floor((Date.now() - new Date(state.startedAt).getTime()) / 1000);
    const mins = Math.floor(elapsed / 60);
    const secs = elapsed % 60;
    console.log('Daemon: RUNNING');
    console.log(`  Profile: ${state.profile} [${state.profileId}]`);
    console.log(`  PID: ${state.pid}`);
    console.log(`  Uptime: ${mins}m ${secs}s`);
    console.log(`  Started: ${state.startedAt}`);
}
