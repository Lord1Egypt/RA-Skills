// Evolver Lifecycle Manager - Evolver Core Module
// Provides: start, stop, restart, status, log, health check
// The loop script to spawn is configurable via EVOLVER_LOOP_SCRIPT env var.
// Cross-platform: works on Linux/macOS (ps) and Windows (WMI via PowerShell).

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync, execSync, spawn } = require('child_process');
// 10 MB — prevents RangeError on large child process output (e.g. git log/diff
// on large repos). See GHSA reports / issue #451.
const MAX_EXEC_BUFFER = 10 * 1024 * 1024;

const { getRepoRoot, getWorkspaceRoot, getEvolverLogPath } = require('../gep/paths');

var WORKSPACE_ROOT = getWorkspaceRoot();
var LOG_FILE = getEvolverLogPath();
var PID_FILE = path.join(WORKSPACE_ROOT, 'memory', 'evolver_loop.pid');
var MAX_SILENCE_MS = require('../config').MAX_SILENCE_MS;

function getLoopScript() {
    // External supervisors / wrappers can override via EVOLVER_LOOP_SCRIPT.
    if (process.env.EVOLVER_LOOP_SCRIPT) return process.env.EVOLVER_LOOP_SCRIPT;
    return path.join(getRepoRoot(), 'index.js');
}

// --- Portable helpers ---

function sleepMs(ms) {
    var delay = Math.max(0, Math.floor(Number(ms) || 0));
    if (delay <= 0) return;
    // Atomics.wait blocks without spawning a subprocess; works on all platforms.
    Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, delay);
}

function execText(command) {
    return execSync(command, { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'], maxBuffer: MAX_EXEC_BUFFER });
}

function execFileText(file, args) {
    return execFileSync(file, args, {
        encoding: 'utf8',
        stdio: ['ignore', 'pipe', 'ignore'],
        maxBuffer: MAX_EXEC_BUFFER,
        windowsHide: true
    });
}

function listProcesses() {
    if (process.platform === 'win32') {
        var out = execFileText('powershell', [
            '-NoProfile',
            '-Command',
            'Get-CimInstance Win32_Process | ForEach-Object { $cmd = if ($_.CommandLine) { $_.CommandLine } else { \'\'}; Write-Output (\'{0}\t{1}\' -f $_.ProcessId, $cmd) }'
        ]);
        var procs = [];
        for (var line of out.split(/\r?\n/)) {
            if (!line || !line.trim()) continue;
            var tabIndex = line.indexOf('\t');
            var pidText = tabIndex >= 0 ? line.slice(0, tabIndex).trim() : line.trim();
            var cmdText = tabIndex >= 0 ? line.slice(tabIndex + 1).trim() : '';
            var pid = parseInt(pidText, 10);
            if (!isNaN(pid)) procs.push({ pid: pid, args: cmdText });
        }
        return procs;
    }
    var psOut = execText('ps -e -o pid=,args=');
    var unixProcs = [];
    for (var psLine of psOut.split('\n')) {
        var trimmed = psLine.trim();
        if (!trimmed) continue;
        var parts = trimmed.split(/\s+/);
        var pidUnix = parseInt(parts[0], 10);
        if (isNaN(pidUnix)) continue;
        unixProcs.push({ pid: pidUnix, args: parts.slice(1).join(' ') });
    }
    return unixProcs;
}

// --- Process Discovery ---

function getRunningPids() {
    try {
        var pids = [];
        for (var proc of listProcesses()) {
            var pid = proc.pid;
            var cmd = (proc.args || '').trim();
            if (pid === process.pid) continue;
            var cmdLower = cmd.toLowerCase();
            // Match any `node ... index.js ... --loop` invocation.
            // Wrapper path prefix filters were removed so launchd/plist or direct
            // node invocations are also discovered (fixes #379, #403).
            if (cmdLower.includes('node') && cmdLower.includes('index.js') && cmdLower.includes('--loop')) {
                pids.push(pid);
            }
        }
        return [...new Set(pids)].filter(isPidRunning);
    } catch (e) {
        return [];
    }
}

function isPidRunning(pid) {
    try { process.kill(pid, 0); return true; } catch (e) { return false; }
}

function getCmdLine(pid) {
    try {
        const safePid = parseInt(pid, 10);
        if (isNaN(safePid)) return null;
        var proc = listProcesses().find(function(p) { return p.pid === safePid; });
        return proc ? (proc.args || '').trim() : null;
    } catch (e) {
        return null;
    }
}

// --- Lifecycle ---

function start(options) {
    var delayMs = (options && options.delayMs) || 0;
    var pids = getRunningPids();
    if (pids.length > 0) {
        console.log('[Lifecycle] Already running (PIDs: ' + pids.join(', ') + ').');
        return { status: 'already_running', pids: pids };
    }
    if (delayMs > 0) {
        sleepMs(delayMs);
    }

    var script = getLoopScript();
    console.log('[Lifecycle] Starting: node ' + path.relative(WORKSPACE_ROOT, script) + ' --loop');

    var out = fs.openSync(LOG_FILE, 'a');
    var err = fs.openSync(LOG_FILE, 'a');

    var env = Object.assign({}, process.env);
    // .npm-global/bin is a Unix-only convention; skip the PATH injection on Windows
    // to avoid polluting the environment with a path that does not exist.
    if (process.platform !== 'win32') {
        var npmGlobal = path.join(os.homedir(), '.npm-global', 'bin');
        if (env.PATH && !env.PATH.includes(npmGlobal)) {
            env.PATH = npmGlobal + ':' + env.PATH;
        }
    }

    var child = spawn(process.execPath, [script, '--loop'], {
        detached: true, stdio: ['ignore', out, err], cwd: WORKSPACE_ROOT, env: env, windowsHide: true
    });
    child.unref();
    fs.writeFileSync(PID_FILE, String(child.pid));
    console.log('[Lifecycle] Started PID ' + child.pid);
    return { status: 'started', pid: child.pid };
}

function stop() {
    var pids = getRunningPids();
    if (pids.length === 0) {
        console.log('[Lifecycle] No running evolver loops found.');
        // Wrap in try/catch: on Windows a concurrently-open file raises EBUSY
        // instead of succeeding silently as on Unix.
        try { if (fs.existsSync(PID_FILE)) fs.unlinkSync(PID_FILE); } catch (_) {}
        return { status: 'not_running' };
    }
    for (var i = 0; i < pids.length; i++) {
        console.log('[Lifecycle] Stopping PID ' + pids[i] + '...');
        try { process.kill(pids[i], 'SIGTERM'); } catch (e) {}
    }
    var attempts = 0;
    while (getRunningPids().length > 0 && attempts < 10) {
        sleepMs(500);
        attempts++;
    }
    var remaining = getRunningPids();
    for (var j = 0; j < remaining.length; j++) {
        console.log('[Lifecycle] Force-killing PID ' + remaining[j]);
        // Windows does not support SIGKILL; use taskkill /F instead.
        if (process.platform === 'win32') {
            try { execFileSync('taskkill', ['/F', '/PID', String(remaining[j])], { stdio: 'ignore', windowsHide: true }); } catch (e) {}
        } else {
            try { process.kill(remaining[j], 'SIGKILL'); } catch (e) {}
        }
    }
    // Wrap in try/catch: on Windows a just-killed process may still hold its
    // file handles open for a brief moment, causing EBUSY on unlinkSync.
    try { if (fs.existsSync(PID_FILE)) fs.unlinkSync(PID_FILE); } catch (_) {}
    var evolverLock = path.join(getRepoRoot(), 'evolver.pid');
    try { if (fs.existsSync(evolverLock)) fs.unlinkSync(evolverLock); } catch (_) {}
    console.log('[Lifecycle] All stopped.');
    return { status: 'stopped', killed: pids };
}

function restart(options) {
    stop();
    return start(Object.assign({ delayMs: 2000 }, options || {}));
}

function status() {
    var pids = getRunningPids();
    if (pids.length > 0) {
        return { running: true, pids: pids.map(function(p) { return { pid: p, cmd: getCmdLine(p) }; }), log: path.relative(WORKSPACE_ROOT, LOG_FILE) };
    }
    return { running: false };
}

function tailLog(lines) {
    if (!fs.existsSync(LOG_FILE)) return { error: 'No log file' };
    try {
        const n = parseInt(lines, 10) || 20;
        const fd = fs.openSync(LOG_FILE, 'r');
        var content = '';
        try {
            const stat = fs.fstatSync(fd);
            if (stat.size > 0) {
                const chunkSize = 64 * 1024;
                let position = stat.size;
                let collected = '';
                let lineCount = 0;
                while (position > 0 && lineCount <= n) {
                    const readSize = Math.min(chunkSize, position);
                    position -= readSize;
                    const buf = Buffer.alloc(readSize);
                    fs.readSync(fd, buf, 0, readSize, position);
                    collected = buf.toString('utf8') + collected;
                    lineCount = collected.split('\n').length - 1;
                }
                const rows = collected.split('\n');
                if (rows.length > 0 && rows[rows.length - 1] === '') rows.pop();
                content = rows.slice(-n).join('\n');
            }
        } finally {
            fs.closeSync(fd);
        }
        return {
            file: path.relative(WORKSPACE_ROOT, LOG_FILE),
            content: content
        };
    } catch (e) {
        return { error: e.message };
    }
}

function checkHealth() {
    var pids = getRunningPids();
    if (pids.length === 0) return { healthy: false, reason: 'not_running' };
    if (fs.existsSync(LOG_FILE)) {
        var silenceMs = Date.now() - fs.statSync(LOG_FILE).mtimeMs;
        if (silenceMs > MAX_SILENCE_MS) {
            return { healthy: false, reason: 'stagnation', silenceMinutes: Math.round(silenceMs / 60000) };
        }
    }
    return { healthy: true, pids: pids };
}

// --- CLI ---
if (require.main === module) {
    var action = process.argv[2];
    switch (action) {
        case 'start': console.log(JSON.stringify(start())); break;
        case 'stop': console.log(JSON.stringify(stop())); break;
        case 'restart': console.log(JSON.stringify(restart())); break;
        case 'status': console.log(JSON.stringify(status(), null, 2)); break;
        case 'log': var r = tailLog(); console.log(r.content || r.error); break;
        case 'check':
            var health = checkHealth();
            console.log(JSON.stringify(health, null, 2));
            if (!health.healthy) { console.log('[Lifecycle] Restarting...'); restart(); }
            break;
        // watch: continuous self-healing supervisor loop. Checks every
        // EVOLVER_WATCH_INTERVAL_S seconds (default 120) and restarts the
        // daemon if checkHealth() reports unhealthy (not running or log
        // stagnation beyond MAX_SILENCE_MS). Designed to be run as a
        // lightweight companion process or cron job so the daemon self-heals
        // without an external supervisor like pm2/launchd.
        //
        // Usage:
        //   node src/ops/lifecycle.js watch          # runs until killed
        //   node src/ops/lifecycle.js watch --once   # one check then exit
        case 'watch':
            var watchOnce = process.argv.slice(3).includes('--once');
            var watchIntervalMs = (parseInt(process.env.EVOLVER_WATCH_INTERVAL_S || '120', 10) || 120) * 1000;
            var prevWall = Date.now();
            var prevMono = process.hrtime.bigint();
            var skippedLastTick = false;
            var watchRun = function () {
                try {
                    var nowWall = Date.now();
                    var nowMono = process.hrtime.bigint();
                    var wallDelta = nowWall - prevWall;
                    var monoDeltaMs = Number((nowMono - prevMono) / 1000000n);
                    // Wall-clock can jump forward after macOS sleep/resume; monotonic
                    // clock does not. If the gap exceeds 60s, skip the stagnation
                    // restart this tick to give the daemon a grace period — but only
                    // once in a row, so a genuinely stuck daemon still gets restarted.
                    var clockJumped = (wallDelta - monoDeltaMs) > 60000 && !skippedLastTick;
                    var wh = checkHealth();
                    var ts = new Date().toISOString();
                    if (wh.healthy) {
                        console.log('[Watch] ' + ts + ' healthy pids=' + (wh.pids || []).join(','));
                        skippedLastTick = false;
                    } else if (clockJumped && wh.reason === 'stagnation') {
                        console.log('[watch] wall-clock jump detected (+' + Math.round((wallDelta - monoDeltaMs) / 1000) + 's), skipping stagnation check this cycle to give daemon a grace period');
                        skippedLastTick = true;
                    } else {
                        console.log('[Watch] ' + ts + ' unhealthy reason=' + wh.reason + ' restarting...');
                        var res = restart();
                        console.log('[Watch] restart result: ' + JSON.stringify(res));
                        skippedLastTick = false;
                    }
                    prevWall = nowWall;
                    prevMono = nowMono;
                } catch (e) {
                    console.error('[watch] tick error: ' + (e && e.stack || e));
                }
            };
            try { watchRun(); } catch (e) { console.error('[watch] tick error: ' + (e && e.stack || e)); }
            if (!watchOnce) {
                setInterval(function () {
                    try { watchRun(); } catch (e) { console.error('[watch] tick error: ' + (e && e.stack || e)); }
                }, watchIntervalMs);
                console.log('[Watch] Supervisor running every ' + Math.round(watchIntervalMs / 1000) + 's. Ctrl-C to stop.');
            }
            break;
        default: console.log('Usage: node lifecycle.js [start|stop|restart|status|log|check|watch]');
    }
}

module.exports = { start, stop, restart, status, tailLog, checkHealth, getRunningPids };
