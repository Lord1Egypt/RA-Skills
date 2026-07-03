// Evolver Lifecycle Manager - Evolver Core Module
// Provides: start, stop, restart, status, log, health check
// The loop script to spawn is configurable via EVOLVER_LOOP_SCRIPT env var.
// Cross-platform: works on Linux/macOS (ps) and Windows (WMI via PowerShell).

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execFileSync, execSync, spawn } = require('child_process');
const { readSettings } = require('../proxy/server/settings');
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

// --- Test-only process-table injection -------------------------------------
// Lets the lifecycle proxy-health tests run hermetically on a host that already
// has REAL `node index.js --loop` processes (CI runners, or a live agent box).
// Without it, getRunningPids()/checkHealth()/stopOwnedLoops() read the actual
// process table via ps/proc and would (a) fail their "not_running" assertions
// against unrelated real loops and (b) risk SIGTERM-ing real production loops.
// Production never installs a table; listProcesses()/getPidCwd()/isPidRunning()
// consult it only when one has been set. Entries are { pid, args, cwd }.
var _processTableForTest = null;
function _setProcessTableForTest(table) {
    _processTableForTest = Array.isArray(table) ? table.map(function (p) {
        return {
            pid: parseInt(p.pid, 10),
            args: String(p.args || ''),
            cwd: p.cwd != null ? String(p.cwd) : null,
        };
    }) : null;
}
function _resetProcessTableForTest() { _processTableForTest = null; }

function listProcesses() {
    if (_processTableForTest) {
        return _processTableForTest.map(function (p) { return { pid: p.pid, args: p.args }; });
    }
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
    if (_processTableForTest) {
        var spRun = parseInt(pid, 10);
        return _processTableForTest.some(function (p) { return p.pid === spRun; });
    }
    try { process.kill(pid, 0); return true; } catch (e) { return false; }
}

function boolEnv(value) {
    var raw = String(value || '').trim().toLowerCase();
    return raw === '1' || raw === 'true' || raw === 'yes' || raw === 'on';
}

function isLoopbackProxyUrl(value) {
    var raw = String(value || '').trim().replace(/\/+$/, '');
    if (!raw) return false;
    try {
        var parsed = new URL(raw);
        if (parsed.protocol !== 'http:') return false;
        var host = parsed.hostname.toLowerCase();
        return host === '127.0.0.1' || host === 'localhost' || host === '::1' || host === '[::1]';
    } catch (_) {
        return false;
    }
}

function readJsonFile(file) {
    try {
        if (!file || !fs.existsSync(file)) return null;
        return JSON.parse(fs.readFileSync(file, 'utf8'));
    } catch (_) {
        return null;
    }
}

function getClaudeSettingsFile(env) {
    var e = env || process.env;
    var explicit = String(e.CLAUDE_SETTINGS_FILE || e.EVOMAP_CLAUDE_SETTINGS_FILE || '').trim();
    if (explicit) return explicit;
    var home = e.HOME || os.homedir();
    return home ? path.join(home, '.claude', 'settings.json') : null;
}

function getCodexConfigFile(env) {
    var e = env || process.env;
    var explicit = String(e.CODEX_CONFIG_FILE || e.EVOMAP_CODEX_CONFIG_FILE || '').trim();
    if (explicit) return explicit;
    var home = e.HOME || os.homedir();
    return home ? path.join(home, '.codex', 'config.toml') : null;
}

function stripTomlComment(line) {
    var out = '';
    var quote = null;
    var escaped = false;
    for (var i = 0; i < String(line || '').length; i++) {
        var ch = line[i];
        if (escaped) {
            out += ch;
            escaped = false;
            continue;
        }
        if (ch === '\\' && quote === '"') {
            out += ch;
            escaped = true;
            continue;
        }
        if ((ch === '"' || ch === "'") && !quote) {
            quote = ch;
            out += ch;
            continue;
        }
        if (ch === quote) {
            quote = null;
            out += ch;
            continue;
        }
        if (ch === '#' && !quote) break;
        out += ch;
    }
    return out.trim();
}

function readTomlStringValue(value) {
    var raw = stripTomlComment(value);
    var match = raw.match(/^(['"])([\s\S]*)\1$/);
    if (match) return match[2];
    return raw.trim();
}

function codexConfigExpectsProxy(env) {
    var file = getCodexConfigFile(env);
    if (!file || !fs.existsSync(file)) return false;
    var selectedProvider = null;
    var section = '';
    var providerUrls = {};
    try {
        var content = fs.readFileSync(file, 'utf8');
        for (var line of content.split(/\r?\n/)) {
            var clean = stripTomlComment(line);
            if (!clean) continue;
            var sectionMatch = clean.match(/^\[([^\]]+)\]$/);
            if (sectionMatch) {
                section = sectionMatch[1].trim();
                continue;
            }
            var kv = clean.match(/^([A-Za-z0-9_.-]+)\s*=\s*([\s\S]+)$/);
            if (!kv) continue;
            var key = kv[1].trim();
            var val = readTomlStringValue(kv[2]);
            if (!section && key === 'model_provider') {
                selectedProvider = val;
                continue;
            }
            var providerMatch = section.match(/^model_providers\.([A-Za-z0-9_.-]+)$/);
            if (providerMatch && key === 'base_url') {
                providerUrls[providerMatch[1]] = val;
                continue;
            }
            if (!section && key === 'base_url' && isLoopbackProxyUrl(val)) {
                return true;
            }
        }
    } catch (_) {
        return false;
    }
    if (selectedProvider && isLoopbackProxyUrl(providerUrls[selectedProvider])) return true;
    return Object.keys(providerUrls).some(function(name) {
        return /(?:evomap|proxy)/i.test(name) && isLoopbackProxyUrl(providerUrls[name]);
    });
}

function clientSettingsExpectProxy(env) {
    var settings = readJsonFile(getClaudeSettingsFile(env));
    var cfg = settings && settings.env;
    if (!cfg || typeof cfg !== 'object') return false;
    if (isLoopbackProxyUrl(cfg.EVOMAP_PROXY_URL)) return true;
    if (String(cfg.EVOMAP_PROXY_AUTO_INJECTED || '') === '1' && isLoopbackProxyUrl(cfg.ANTHROPIC_BASE_URL)) return true;
    return !!(settings._evomap_proxy_client_env && settings._evomap_proxy_client_env.managed_by === 'evomap-proxy'
        && isLoopbackProxyUrl(cfg.ANTHROPIC_BASE_URL));
}

function expectsProxy(env) {
    var e = env || process.env;
    if (boolEnv(e.EVOMAP_PROXY)) return true;
    if (String(e.A2A_TRANSPORT || '').trim().toLowerCase() === 'mailbox') return true;
    if (isLoopbackProxyUrl(e.EVOMAP_PROXY_URL) || isLoopbackProxyUrl(e.ANTHROPIC_BASE_URL)) return true;
    if (codexConfigExpectsProxy(e)) return true;
    return clientSettingsExpectProxy(e);
}

function prepareStartEnv(env) {
    var next = Object.assign({}, env || process.env);
    if (expectsProxy(next)) {
        next.EVOMAP_PROXY = '1';
    }
    return next;
}

function isProxyUrlReachable(url, token) {
    if (!url || !token) return false;
    try {
        execFileSync(process.execPath, ['-e', `
const fs = require('fs');
const http = require('http');
const url = process.argv[1];
const token = fs.readFileSync(0, 'utf8').trim();
if (!token) process.exit(1);
const req = http.get(url.replace(/\\/+$/, '') + '/proxy/status', {
  headers: { Authorization: 'Bearer ' + token },
}, (res) => {
  let body = '';
  res.setEncoding('utf8');
  res.on('data', (chunk) => {
    body += chunk;
    if (body.length > 1024 * 1024) req.destroy(new Error('response too large'));
  });
  res.on('end', () => {
    if (res.statusCode < 200 || res.statusCode >= 300) process.exit(1);
    let parsed;
    try { parsed = JSON.parse(body); } catch (_) { process.exit(1); }
    if (parsed && parsed.status === 'running' && (parsed.proxy_protocol_version || parsed.schema_version || parsed.node_id != null)) {
      process.exit(0);
    }
    process.exit(1);
  });
});
req.setTimeout(800, () => { req.destroy(new Error('timeout')); });
req.on('error', () => process.exit(1));
`, url], { input: String(token), stdio: ['pipe', 'ignore', 'ignore'], timeout: 1500, windowsHide: true });
        return true;
    } catch (_) {
        return false;
    }
}

function checkProxyHealth(env) {
    if (!expectsProxy(env)) return { healthy: true, expected: false };
    var proxy = readSettings().proxy || {};
    if (!proxy.url) {
        return { healthy: false, expected: true, reason: 'proxy_not_configured' };
    }
    if (proxy.pid && !isPidRunning(proxy.pid)) {
        return { healthy: false, expected: true, reason: 'proxy_pid_stale', proxyPid: proxy.pid, proxyUrl: proxy.url };
    }
    if (!proxy.token) {
        return { healthy: false, expected: true, reason: 'proxy_token_missing', proxyPid: proxy.pid, proxyUrl: proxy.url };
    }
    if (!isProxyUrlReachable(proxy.url, proxy.token)) {
        return { healthy: false, expected: true, reason: 'proxy_unreachable', proxyPid: proxy.pid, proxyUrl: proxy.url };
    }
    return { healthy: true, expected: true, proxyPid: proxy.pid, proxyUrl: proxy.url };
}

function shouldRestartForProxy(pids, env) {
    if (!pids || pids.length === 0) return false;
    var proxyHealth = checkProxyHealth(env);
    return proxyHealth.expected === true && proxyHealth.healthy === false;
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

function getPidCwd(pid) {
    const safePid = parseInt(pid, 10);
    if (!Number.isFinite(safePid) || safePid <= 0) return null;
    if (_processTableForTest) {
        var cwdEntry = _processTableForTest.find(function (p) { return p.pid === safePid; });
        return cwdEntry ? cwdEntry.cwd : null;
    }
    if (process.platform === 'win32') return null;
    if (process.platform === 'linux') {
        try { return fs.realpathSync('/proc/' + safePid + '/cwd'); } catch (_) {}
    }
    try {
        var lsofOut = execFileSync('lsof', ['-a', '-p', String(safePid), '-d', 'cwd', '-Fn'], {
            encoding: 'utf8',
            stdio: ['ignore', 'pipe', 'ignore'],
            maxBuffer: MAX_EXEC_BUFFER,
            timeout: 1000,
            windowsHide: true
        });
        for (var line of lsofOut.split(/\r?\n/)) {
            if (line && line[0] === 'n') {
                try { return fs.realpathSync(line.slice(1)); } catch (_) { return path.resolve(line.slice(1)); }
            }
        }
    } catch (_) {}
    try {
        var pwdxOut = execFileText('pwdx', [String(safePid)]).trim();
        var match = pwdxOut.match(/^\d+:\s*(.+)$/);
        if (match) {
            try { return fs.realpathSync(match[1]); } catch (_) { return path.resolve(match[1]); }
        }
    } catch (_) {}
    return null;
}

function commandIncludesPath(cmd, targetPath) {
    if (!cmd || !targetPath) return false;
    var cmdNorm = String(cmd).replace(/\\/g, '/');
    var candidates = [targetPath];
    try { candidates.push(fs.realpathSync(targetPath)); } catch (_) {}
    return candidates.some(function(candidate) {
        var normalized = path.resolve(candidate).replace(/\\/g, '/');
        return normalized && cmdNorm.includes(normalized);
    });
}

function splitCommandLine(cmd) {
    var tokens = [];
    var current = '';
    var quote = null;
    var escaped = false;
    var raw = String(cmd || '');
    for (var i = 0; i < raw.length; i++) {
        var ch = raw[i];
        if (escaped) {
            current += ch;
            escaped = false;
            continue;
        }
        if (ch === '\\') {
            escaped = true;
            continue;
        }
        if ((ch === '"' || ch === "'") && !quote) {
            quote = ch;
            continue;
        }
        if (ch === quote) {
            quote = null;
            continue;
        }
        if (/\s/.test(ch) && !quote) {
            if (current) {
                tokens.push(current);
                current = '';
            }
            continue;
        }
        current += ch;
    }
    if (escaped) current += '\\';
    if (current) tokens.push(current);
    return tokens;
}

function looksLikeNodeToken(token) {
    var base = path.basename(String(token || '').replace(/\\/g, '/')).toLowerCase();
    return base === 'node' || base === 'node.exe';
}

function nodeOptionTakesValue(option) {
    var name = String(option || '').split('=')[0];
    return name === '-r' || name === '--require' ||
        name === '--import' ||
        name === '--loader' || name === '--experimental-loader' ||
        name === '--icu-data-dir' ||
        name === '--openssl-config' ||
        name === '--redirect-warnings';
}

function nodeOptionIsEvalMode(option) {
    var name = String(option || '').split('=')[0];
    return name === '-e' || name === '--eval' ||
        name === '-p' || name === '--print' ||
        name === '-c' || name === '--check';
}

function getNodeScriptToken(tokens) {
    for (var i = 0; i < tokens.length; i++) {
        if (!looksLikeNodeToken(tokens[i])) continue;
        for (var j = i + 1; j < tokens.length; j++) {
            var token = tokens[j];
            if (!token) continue;
            if (token === '--') return tokens[j + 1] || null;
            if (token[0] === '-') {
                if (nodeOptionIsEvalMode(token)) return null;
                if (nodeOptionTakesValue(token) && !token.includes('=')) j++;
                continue;
            }
            return token;
        }
    }
    return null;
}

function sameRealPath(left, right) {
    try {
        return fs.realpathSync(left) === fs.realpathSync(right);
    } catch (_) {
        return false;
    }
}

function commandUsesCurrentRepoRelativeIndex(cmd, cwd) {
    if (!cwd) return false;
    var script = getNodeScriptToken(splitCommandLine(cmd));
    if (!script || path.isAbsolute(script)) return false;
    if (path.basename(script.replace(/\\/g, '/')).toLowerCase() !== 'index.js') return false;
    return sameRealPath(path.resolve(cwd, script), path.join(getRepoRoot(), 'index.js'));
}

function isCurrentLoopCommand(cmd, cwd) {
    var raw = String(cmd || '');
    var lower = raw.toLowerCase();
    if (!lower.includes('node') || !lower.includes('--loop')) return false;
    if (commandIncludesPath(raw, getLoopScript())) return true;
    if (commandIncludesPath(raw, path.join(getRepoRoot(), 'index.js'))) return true;
    return commandUsesCurrentRepoRelativeIndex(raw, cwd);
}

function readPidFile(file) {
    try {
        if (!file || !fs.existsSync(file)) return null;
        var raw = fs.readFileSync(file, 'utf8').trim();
        var pid = parseInt(raw, 10);
        return Number.isFinite(pid) && pid > 0 ? pid : null;
    } catch (_) {
        return null;
    }
}

function getOwnedLoopPids(discoveredPids) {
    var candidates = new Set();
    function addPid(pid) {
        var parsed = parseInt(pid, 10);
        if (Number.isFinite(parsed) && parsed > 0) candidates.add(parsed);
    }
    (discoveredPids || []).forEach(addPid);
    addPid(readPidFile(PID_FILE));
    try {
        var proxyPid = (readSettings().proxy || {}).pid;
        addPid(proxyPid);
    } catch (_) {}
    return Array.from(candidates).filter(function(pid) {
        if (!isPidRunning(pid)) return false;
        var cmd = getCmdLine(pid);
        if (isCurrentLoopCommand(cmd)) return true;
        return isCurrentLoopCommand(cmd, getPidCwd(pid));
    });
}

function stopPids(pids, options) {
    var targets = Array.from(new Set(pids || [])).map(function(pid) {
        return parseInt(pid, 10);
    }).filter(Number.isFinite);
    for (var i = 0; i < targets.length; i++) {
        console.log('[Lifecycle] Stopping PID ' + targets[i] + '...');
        try { process.kill(targets[i], 'SIGTERM'); } catch (e) {}
    }
    var attempts = 0;
    while (targets.some(isPidRunning) && attempts < 10) {
        sleepMs(500);
        attempts++;
    }
    var remaining = targets.filter(isPidRunning);
    for (var j = 0; j < remaining.length; j++) {
        console.log('[Lifecycle] Force-killing PID ' + remaining[j]);
        if (process.platform === 'win32') {
            try { execFileSync('taskkill', ['/F', '/PID', String(remaining[j])], { stdio: 'ignore', windowsHide: true }); } catch (e) {}
        } else {
            try { process.kill(remaining[j], 'SIGKILL'); } catch (e) {}
        }
    }
    if (options && options.unlinkPidFile) {
        try { if (fs.existsSync(PID_FILE)) fs.unlinkSync(PID_FILE); } catch (_) {}
    }
    if (options && options.unlinkLock) {
        var evolverLock = path.join(getRepoRoot(), 'evolver.pid');
        try { if (fs.existsSync(evolverLock)) fs.unlinkSync(evolverLock); } catch (_) {}
    }
    return { status: 'stopped', killed: targets };
}

// --- Lifecycle ---

function start(options) {
    var delayMs = (options && options.delayMs) || 0;
    var pids = getRunningPids();
    var ownedPids = getOwnedLoopPids(pids);
    if (ownedPids.length > 0) {
        if (shouldRestartForProxy(ownedPids, process.env)) {
            console.log('[Lifecycle] Loop running but proxy is unhealthy; restarting.');
            stopPids(ownedPids, { unlinkPidFile: true, unlinkLock: true });
            ownedPids = getOwnedLoopPids(getRunningPids());
        }
    }
    if (ownedPids.length > 0) {
        console.log('[Lifecycle] Already running (PIDs: ' + ownedPids.join(', ') + ').');
        return { status: 'already_running', pids: ownedPids };
    }
    if (delayMs > 0) {
        sleepMs(delayMs);
    }

    var script = getLoopScript();
    console.log('[Lifecycle] Starting: node ' + path.relative(WORKSPACE_ROOT, script) + ' --loop');

    var out = fs.openSync(LOG_FILE, 'a');
    var err = fs.openSync(LOG_FILE, 'a');

    var env = prepareStartEnv(process.env);
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
    // Preserve the existing CLI stop semantics: stop every discoverable loop.
    stopPids(pids, { unlinkPidFile: true, unlinkLock: true });
    console.log('[Lifecycle] All stopped.');
    return { status: 'stopped', killed: pids };
}

function stopOwnedLoops() {
    var ownedPids = getOwnedLoopPids(getRunningPids());
    if (ownedPids.length === 0) {
        try { if (fs.existsSync(PID_FILE)) fs.unlinkSync(PID_FILE); } catch (_) {}
        return { status: 'not_running' };
    }
    return stopPids(ownedPids, { unlinkPidFile: true, unlinkLock: true });
}

function restart(options) {
    stopOwnedLoops();
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
    var pids = getOwnedLoopPids(getRunningPids());
    if (pids.length === 0) return { healthy: false, reason: 'not_running' };
    var proxyHealth = checkProxyHealth(process.env);
    if (!proxyHealth.healthy) {
        return Object.assign({ healthy: false }, proxyHealth);
    }
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

module.exports = {
    start,
    stop,
    restart,
    status,
    tailLog,
    checkHealth,
    getRunningPids,
    expectsProxy,
    prepareStartEnv,
    checkProxyHealth,
    shouldRestartForProxy,
    isProxyUrlReachable,
    isCurrentLoopCommand,
    getOwnedLoopPids,
    stopOwnedLoops,
    _setProcessTableForTest,
    _resetProcessTableForTest,
};
