/**
 * claw-janitor
 * A safe, multi-platform system cleaner designed for OpenClaw & AI Dev Environments.
 * 
 * Safety & Architecture Rules:
 * 1. ZERO external dependencies. Must run on raw Node.js.
 * 2. Whitelist driven. Hardcoded blacklists for extreme safety.
 * 3. Graceful degradation: If a permission is denied, it skips silently.
 * 4. Symlink protection: Does not traverse or delete through symbolic links.
 * 5. Cross-Platform Root protection: Adapts to Windows (C:\) and POSIX (/).
 * 6. AI Model Awareness: Detects massive AI caches but NEVER deletes them automatically.
 * 7. Workspace Sealing: Will never modify the current working directory or OpenClaw workspace.
 * 8. Env-Aware: Respects XDG_CACHE_HOME, NVM_DIR, HF_HOME, etc.
 * 9. Perf-Optimized: Uses withFileTypes for fast directory traversal.
 * 10. Mount-Point Protection: Stops traversal if it detects crossing into a different mounted device.
 */

const fs = require('fs');
const path = require('path');
const os = require('os');
const { execSync } = require('child_process');

const args = process.argv.slice(2);

function getArgValue(flag) {
    const idx = args.indexOf(flag);
    if (idx === -1) return null;
    return args[idx + 1] && !args[idx + 1].startsWith('--') ? args[idx + 1] : null;
}

const DRY_RUN = args.includes('--dry-run');
const DEEP_CLEAN = args.includes('--deep');
const JSON_OUT = args.includes('--json');
const NO_COLOR = args.includes('--no-color') || process.env.NO_COLOR === '1';
const REPORT_FILE = getArgValue('--report-file');
const ONLY_GROUP = (getArgValue('--only') || '').trim();
const SKIP_GROUP = (getArgValue('--skip') || '').trim();
const HELP = args.includes('--help') || args.includes('-h');

const HOME = os.homedir();
const PLATFORM = os.platform();
const IS_ROOT = process.getuid ? process.getuid() === 0 : false;
const CWD = process.cwd();

// Environment fallbacks
const NVM_DIR = process.env.NVM_DIR || path.join(HOME, '.nvm');
const HF_HOME = process.env.HF_HOME || path.join(HOME, '.cache', 'huggingface');
const OLLAMA_MODELS = process.env.OLLAMA_MODELS || path.join(HOME, '.ollama', 'models');
const CACHE_HOME = process.env.XDG_CACHE_HOME || path.join(HOME, '.cache');

// Dynamically determine system root
const SYS_ROOT = path.parse(HOME).root;

// Node version compat for fs.rmSync
const nodeMajor = parseInt(process.versions.node.split('.')[0], 10);
const FS_RM_SUPPORTED = nodeMajor >= 14;

// ==========================================
// 🛡️ SECURITY: ABSOLUTE BLACKLIST & SEALING
// ==========================================
const BLACKLIST_TREE = [
    path.join(HOME, '.ssh'),
    path.join(HOME, '.aws'),
    path.join(HOME, '.gnupg'),
    path.join(HOME, '.config'),
    path.join(HOME, '.local', 'share'),
    path.join(HOME, '.kube'),
    path.join(HOME, '.openclaw', 'workspace'), // Seal OpenClaw workspace
    CWD, // Seal current working directory tree
    path.join(SYS_ROOT, 'etc'),
    path.join(SYS_ROOT, 'boot'),
    path.join(SYS_ROOT, 'var'),
    path.join(SYS_ROOT, 'usr'),
    path.join(SYS_ROOT, 'bin'),
    path.join(SYS_ROOT, 'Windows'),
    path.join(SYS_ROOT, 'Program Files'),
    path.join(SYS_ROOT, 'Program Files (x86)')
].map((p) => path.resolve(p));

const BLACKLIST_EXACT = [
    path.resolve(SYS_ROOT),
    path.resolve(HOME),
    path.resolve(path.join(HOME, '.docker', 'config.json'))
];

const BLACKLIST_REGEX = /([\\/]\.git[\\/]|[\\/]\.env($|[\\/])|[\\/]\.ssh[\\/]|[\\/]\.kube[\\/]|[\\/]node_modules[\\/])/i;

function isSafeToClean(targetPath) {
    if (!targetPath) return false;
    const normalized = path.resolve(targetPath);

    for (const blacklisted of BLACKLIST_EXACT) {
        if (normalized === blacklisted) return false;
    }

    for (const blacklisted of BLACKLIST_TREE) {
        if (normalized === blacklisted || normalized.startsWith(blacklisted + path.sep)) {
            return false;
        }
    }

    if (BLACKLIST_REGEX.test(normalized + path.sep)) return false;
    return true;
}

// ==========================================
// 🛠️ UTILS & PERF & MOUNT PROTECTION
// ==========================================
let totalSavedBytes = 0;
let report = [];
let aiAlerts = [];

const VALID_GROUPS = new Set(['ai-scan', 'packages', 'docker', 'system']);

function shouldRunGroup(group) {
    if (!VALID_GROUPS.has(group)) return false;
    if (ONLY_GROUP && group !== ONLY_GROUP) return false;
    if (SKIP_GROUP && group === SKIP_GROUP) return false;
    return true;
}

function formatBytes(bytes) {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// Optimized directory size calculation with Mount Point boundary protection
function getDirSize(dirPath, rootDev = null) {
    let size = 0;
    try {
        if (!fs.existsSync(dirPath)) return 0;
        
        const stat = fs.lstatSync(dirPath);
        if (stat.isSymbolicLink()) return 0; 
        
        // Mount point protection (do not cross device boundaries)
        if (rootDev === null) {
            rootDev = stat.dev;
        } else if (stat.dev !== rootDev) {
            return 0; // Crossed a mount point, stop traversing this branch
        }

        if (stat.isFile()) return stat.size;

        const entries = fs.readdirSync(dirPath, { withFileTypes: true });
        for (const entry of entries) {
            const fullPath = path.join(dirPath, entry.name);
            try {
                if (entry.isDirectory()) {
                    size += getDirSize(fullPath, rootDev);
                } else if (entry.isFile()) {
                    const childStat = fs.statSync(fullPath);
                    if (childStat.dev === rootDev) {
                         size += childStat.size;
                    }
                }
            } catch(subE) {
                // Ignore transient file locks
            }
        }
    } catch (e) {
        return 0; 
    }
    return size;
}

function safeRemoveDir(targetPath, rootDev) {
    try {
        if (!fs.existsSync(targetPath)) return;
        // Defense in depth: re-check safety at every recursion level.
        if (!isSafeToClean(targetPath)) return;

        const stat = fs.lstatSync(targetPath);

        if (stat.isSymbolicLink()) return;
        if (stat.dev !== rootDev) return; // Never cross mount point

        if (stat.isDirectory()) {
            const entries = fs.readdirSync(targetPath, { withFileTypes: true });
            for (const entry of entries) {
                safeRemoveDir(path.join(targetPath, entry.name), rootDev);
            }
            try { fs.rmdirSync(targetPath); } catch (e) {}
        } else {
            try { fs.unlinkSync(targetPath); } catch (e) {}
        }
    } catch (e) {
        // ignore locked/vanished paths
    }
}

function removePath(targetPath, description) {
    if (!fs.existsSync(targetPath)) return;
    
    let rootDev = null;
    try {
        const stat = fs.lstatSync(targetPath);
        if (stat.isSymbolicLink()) {
             logAction('SKIP', `Symlink detected (Protected): ${targetPath}`, 0);
             return;
        }
        rootDev = stat.dev;
    } catch(e) { return; }

    if (!isSafeToClean(targetPath)) {
        logAction('SKIP', `Blacklisted/Workspace path: ${targetPath}`, 0);
        return;
    }

    const size = getDirSize(targetPath, rootDev);
    
    if (DRY_RUN) {
        logAction('DRY-RUN', `Would delete ${description}: ${targetPath}`, size);
        totalSavedBytes += size;
        return;
    }

    try {
        // Always use mount-aware deletion to avoid crossing filesystem boundaries.
        // Keep fs.rmSync support only for non-directory paths.
        if (FS_RM_SUPPORTED && fs.lstatSync(targetPath).isFile()) {
            fs.rmSync(targetPath, { force: true, maxRetries: 3, retryDelay: 100 });
        } else {
            safeRemoveDir(targetPath, rootDev);
        }

        logAction('CLEANED', `${description}: ${targetPath}`, size);
        totalSavedBytes += size;
    } catch (e) {
        logAction('WARN', `Failed to delete ${targetPath} (Locked or Denied)`, 0);
    }
}

function hasCommand(bin) {
    try {
        if (PLATFORM === 'win32') {
            execSync(`where ${bin}`, { stdio: 'ignore', timeout: 5000 });
        } else {
            execSync(`command -v ${bin}`, { stdio: 'ignore', timeout: 5000 });
        }
        return true;
    } catch {
        return false;
    }
}

function execCommand(cmd, description, fallbackSize = 0) {
    const bin = cmd.split(' ')[0];
    if (!hasCommand(bin)) {
        logAction('SKIP', `Command not installed: ${bin}`, 0);
        return;
    }

    try {
        if (DRY_RUN) {
            logAction('DRY-RUN', `Would execute: ${cmd} (${description})`, 0);
            return;
        }

        const output = execSync(cmd, { stdio: ['ignore', 'pipe', 'ignore'], encoding: 'utf-8', timeout: 60000 });

        let estimatedSize = fallbackSize;
        if (cmd.includes('docker') && output.includes('Total reclaimed space:')) {
            const match = output.match(/Total reclaimed space: ([\d\.]+) ([A-Z]+)/);
            if (match) {
                const val = parseFloat(match[1]);
                const unit = match[2];
                if (unit === 'GB') estimatedSize = val * 1024 * 1024 * 1024;
                if (unit === 'MB') estimatedSize = val * 1024 * 1024;
                if (unit === 'KB') estimatedSize = val * 1024;
            }
        }

        logAction('EXEC', `${description}`, estimatedSize);
        totalSavedBytes += estimatedSize;
    } catch (e) {
        logAction('SKIP', `Command unavailable or failed: ${bin}`, 0);
    }
}

function colorize(text, colorCode) {
    if (NO_COLOR) return text;
    return `${colorCode}${text}\x1b[0m`;
}

function logAction(status, message, size) {
    const sizeStr = size > 0 ? ` [${formatBytes(size)}]` : '';
    report.push({ status, message, size });
    if (!JSON_OUT) {
        let color = '\x1b[0m';
        if (status === 'CLEANED' || status === 'EXEC') color = '\x1b[32m';
        if (status === 'DRY-RUN') color = '\x1b[36m';
        if (status === 'WARN') color = '\x1b[33m';
        if (status === 'SKIP') color = '\x1b[90m';
        console.log(`${colorize(`[${status}]`, color)} ${message}${sizeStr}`);
    }
}

// ==========================================
// 🤖 AI AWARENESS: PASSIVE SCAN ONLY
// ==========================================
function scanAITitans() {
    const aiPaths = [
        { path: HF_HOME, name: 'Hugging Face Cache' },
        { path: OLLAMA_MODELS, name: 'Ollama Models' },
        { path: path.join(CACHE_HOME, 'torch'), name: 'PyTorch Cache' }
    ];

    for (const item of aiPaths) {
        if (fs.existsSync(item.path)) {
            const stat = fs.statSync(item.path);
            const size = getDirSize(item.path, stat.dev); // Safe scan
            if (size > 1024 * 1024 * 500) { // Alert if > 500MB
                aiAlerts.push(`Found massive AI cache: ${item.name} (${formatBytes(size)}) at ${item.path}. Untouched for safety. Handle manually if needed.`);
            }
        }
    }
}

// ==========================================
// 🚀 CLEANUP ROUTINES
// ==========================================
function cleanPackageManagers() {
    execCommand('npm cache clean --force', 'NPM Cache');
    execCommand('yarn cache clean', 'Yarn Cache');
    execCommand('pnpm store prune', 'PNPM Store');
    execCommand('bun pm cache rm', 'Bun Cache');
    
    removePath(path.join(NVM_DIR, '.cache'), 'NVM Version Zip Cache');
    execCommand('pip cache purge', 'Python PIP Cache');
    execCommand('go clean -cache -modcache', 'Go Module Cache');
    removePath(path.join(HOME, '.cargo', 'registry', 'cache'), 'Rust Cargo Cache');
    
    if (PLATFORM === 'win32') {
        removePath(path.join(process.env.LOCALAPPDATA || '', 'ms-playwright'), 'Playwright Browser Binaries (Win)');
        removePath(path.join(process.env.LOCALAPPDATA || '', 'puppeteer'), 'Puppeteer Browser Binaries (Win)');
    } else {
        removePath(path.join(CACHE_HOME, 'ms-playwright'), 'Playwright Browser Binaries');
        removePath(path.join(CACHE_HOME, 'puppeteer'), 'Puppeteer Browser Binaries');
    }
    removePath(path.join(os.tmpdir(), 'openclaw-tmp'), 'OpenClaw Temp Artifacts');
}

function cleanDocker() {
    try {
        execSync('docker ps', { stdio: 'ignore', timeout: 5000 });
        if (DEEP_CLEAN) {
            execCommand('docker system prune -a -f', 'Docker System Prune (All Unused Images & Containers)');
            execCommand('docker builder prune -a -f', 'Docker Buildx/BuildKit Cache (Deep)');
        } else {
            execCommand('docker system prune -f', 'Docker System Prune (Dangling Images Only)');
            execCommand('docker builder prune -f', 'Docker Buildx/BuildKit Cache (Dangling)');
        }
    } catch (e) {
        logAction('SKIP', 'Docker not found or daemon not running', 0);
    }
}

function cleanSystem() {
    if (PLATFORM === 'linux') {
        if (!IS_ROOT) {
            logAction('SKIP', 'Linux System-level cleanup skipped (Run with sudo/root to enable)', 0);
            return;
        }
        if (fs.existsSync('/usr/bin/apt-get')) {
            execCommand('apt-get clean', 'APT Package Cache');
            execCommand('apt-get autoremove -y', 'APT Autoremove Unused Dependencies');
        }
        if (fs.existsSync('/usr/bin/yum')) {
            execCommand('yum clean all', 'YUM Package Cache');
        }
        if (fs.existsSync('/bin/journalctl')) {
            execCommand('journalctl --vacuum-time=3d', 'Systemd Journal Cleanup (Keep 3 days)');
        }
    } else if (PLATFORM === 'darwin') {
        removePath(path.join(HOME, 'Library', 'Caches', 'CocoaPods'), 'macOS CocoaPods Cache');
        try {
            execSync('which brew', { stdio: 'ignore' });
            execCommand('brew cleanup', 'Homebrew Cache');
            execCommand('brew autoremove', 'Homebrew Unused Dependencies');
        } catch(e) {
            logAction('SKIP', 'Homebrew not found on macOS', 0);
        }
    }
}

function printHelp() {
    console.log(`claw-janitor\n\nUsage:\n  node janitor.js [options]\n\nOptions:\n  --dry-run               Preview only, do not delete\n  --deep                  More aggressive cleanup (docker/images etc.)\n  --json                  Output machine-readable JSON\n  --no-color              Disable ANSI colors\n  --report-file <path>    Write JSON report to file\n  --only <group>          Run only one group: ai-scan|packages|docker|system\n  --skip <group>          Skip one group: ai-scan|packages|docker|system\n  -h, --help              Show this help\n`);
}

function run() {
    if (HELP) {
        printHelp();
        return;
    }

    if ((ONLY_GROUP && !VALID_GROUPS.has(ONLY_GROUP)) || (SKIP_GROUP && !VALID_GROUPS.has(SKIP_GROUP))) {
        const bad = ONLY_GROUP && !VALID_GROUPS.has(ONLY_GROUP) ? ONLY_GROUP : SKIP_GROUP;
        throw new Error(`Invalid group: ${bad}. Use one of: ${Array.from(VALID_GROUPS).join(', ')}`);
    }

    if (!JSON_OUT) {
        console.log(`\n🧹 Starting ${colorize('claw-janitor', '\x1b[36m')}...`);
        if (DRY_RUN) console.log(`⚠️  ${colorize('DRY RUN MODE', '\x1b[33m')} - No files will be modified.`);
        if (ONLY_GROUP) console.log(`ℹ️  Running only group: ${ONLY_GROUP}`);
        if (SKIP_GROUP) console.log(`ℹ️  Skipping group: ${SKIP_GROUP}`);
        if (PLATFORM === 'linux' && !IS_ROOT) console.log(`ℹ️  Running as non-root. Deep system files will be skipped safely.\n`);
        else console.log();
    }

    if (shouldRunGroup('ai-scan')) scanAITitans();
    if (shouldRunGroup('packages')) cleanPackageManagers();
    if (shouldRunGroup('docker')) cleanDocker();
    if (shouldRunGroup('system')) cleanSystem();

    const sortedActions = report
        .map((a) => ({ message: a.message, size: a.size, status: a.status }))
        .sort((a, b) => (a.status + a.message).localeCompare(b.status + b.message));

    const summary = {
        actions: sortedActions,
        aiCacheAlerts: [...aiAlerts].sort((a, b) => a.localeCompare(b)),
        deepClean: DEEP_CLEAN,
        dryRun: DRY_RUN,
        isRoot: IS_ROOT,
        onlyGroup: ONLY_GROUP || null,
        platform: PLATFORM,
        reclaimedBytes: totalSavedBytes,
        reclaimedFormatted: formatBytes(totalSavedBytes),
        skipGroup: SKIP_GROUP || null
    };

    if (REPORT_FILE) {
        try {
            fs.writeFileSync(path.resolve(REPORT_FILE), JSON.stringify(summary, null, 2));
            if (!JSON_OUT) console.log(`📝 Report written to: ${path.resolve(REPORT_FILE)}`);
        } catch (e) {
            logAction('WARN', `Failed to write report file: ${REPORT_FILE}`, 0);
        }
    }

    if (!JSON_OUT) {
        if (aiAlerts.length > 0) {
            console.log(`\n🤖 ${colorize('AI CACHE RADAR', '\x1b[35m')}`);
            aiAlerts.forEach(alert => console.log(`   ${colorize(alert, '\x1b[33m')}`));
        }

        console.log(`\n=================================================`);
        console.log(`✨ Total Space ${DRY_RUN ? 'Can Be Reclaimed' : 'Reclaimed'}: ${colorize(formatBytes(totalSavedBytes), '\x1b[32m')}`);
        console.log(`=================================================\n`);
    } else {
        console.log(JSON.stringify(summary, null, 2));
    }
}

if (require.main === module) {
    run();
} else {
    module.exports = {
        cleanPackageManagers,
        cleanDocker,
        cleanSystem,
        run,
        __private: {
            isSafeToClean,
            getDirSize,
            safeRemoveDir,
            shouldRunGroup,
            BLACKLIST_EXACT,
            BLACKLIST_TREE,
            BLACKLIST_REGEX,
            VALID_GROUPS
        }
    };
}