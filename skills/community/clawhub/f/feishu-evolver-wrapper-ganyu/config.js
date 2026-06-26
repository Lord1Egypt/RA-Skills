/**
 * feishu-evolver-wrapper 配置模块
 *
 * 所有路径使用显式配置，不依赖相对路径猜测。
 * 缺失配置时必须降级，不允许崩溃退出。
 *
 * 用法:
 *   const config = require('./config.js');
 *   const EVOLVER_CORE_DIR = config.EVOLVER_CORE_DIR;
 */

const path = require('path');
const fs = require('fs');

// ─── 显式配置（可通过环境变量覆盖） ───────────────────────────────────────

const DEFAULT_EVOLVER_CORE_DIR = '/Users/foras/.openclaw/workspace/evolver';
const DEFAULT_OPENCLAW_WORKSPACE = '/Users/foras/.openclaw/workspace';

/**
 * Wrapper 是否自动管理 cron 任务
 * 默认为 0（不自动管理，避免与官方 evolver cron 冲突）
 */
const WRAPPER_AUTO_CRON = String(process.env.WRAPPER_AUTO_CRON || '0') === '1';

/**
 * 飞书功能开关
 * 默认为 0（无飞书模式，降级到本地日志）
 */
const FEISHU_ENABLED = String(process.env.FEISHU_ENABLED || '0') === '1';

// ─── 路径解析 ─────────────────────────────────────────────────────────────

const OPENCLAW_WORKSPACE = process.env.OPENCLAW_WORKSPACE || DEFAULT_OPENCLAW_WORKSPACE;
const EVOLVER_CORE_DIR = process.env.EVOLVER_CORE_DIR || DEFAULT_EVOLVER_CORE_DIR;

const WRAPPER_DIR = __dirname;
const WORKSPACE_ROOT = path.resolve(WRAPPER_DIR, '../..');

const LOGS_DIR = path.resolve(WORKSPACE_ROOT, 'logs');
const MEMORY_DIR = path.resolve(WORKSPACE_ROOT, 'memory');
const ASSETS_DIR = path.resolve(WORKSPACE_ROOT, 'assets');
const EVENTS_FILE = path.resolve(ASSETS_DIR, 'gep/events.jsonl');
const EVOLUTION_STATE_FILE = path.resolve(MEMORY_DIR, 'evolution/evolution_solidify_state.json');
const WRAPPER_PID_FILE = path.resolve(MEMORY_DIR, 'evolver_wrapper.pid');
const DAEMON_PID_FILE = path.resolve(MEMORY_DIR, 'evolver_daemon.pid');
const WRAPPER_LIFECYCLE_LOG = path.resolve(LOGS_DIR, 'wrapper_lifecycle.log');
const CYCLE_COUNT_FILE = path.resolve(LOGS_DIR, 'cycle_count.txt');
const WRAPPER_OUT_LOG = path.resolve(LOGS_DIR, 'wrapper_out.log');
const WRAPPER_ERR_LOG = path.resolve(LOGS_DIR, 'wrapper_err.log');
const DAEMON_OUT_LOG = path.resolve(LOGS_DIR, 'daemon_out.log');
const DAEMON_ERR_LOG = path.resolve(LOGS_DIR, 'daemon_err.log');

// ─── 核心演进程序路径验证 ─────────────────────────────────────────────────

function resolveEvolverCore() {
    const candidate = EVOLVER_CORE_DIR;
    const indexPath = path.join(candidate, 'index.js');

    if (fs.existsSync(indexPath)) {
        let version = null;
        try {
            const pkgPath = path.join(candidate, 'package.json');
            if (fs.existsSync(pkgPath)) {
                const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8'));
                version = pkg.version || null;
            }
        } catch (_) {}
        return { exists: true, path: candidate, indexPath, version };
    }

    const fallbacks = [
        '/Users/foras/.openclaw/workspace/evolver_main_clean',
        '/Users/foras/.openclaw/workspace/evolver',
    ];

    for (const fb of fallbacks) {
        if (fb === candidate) continue;
        const fbIndex = path.join(fb, 'index.js');
        if (fs.existsSync(fbIndex)) {
            let version = null;
            try {
                const pkg = JSON.parse(fs.readFileSync(path.join(fb, 'package.json'), 'utf8'));
                version = pkg.version || null;
            } catch (_) {}
            return { exists: true, path: fb, indexPath: fbIndex, version, degraded: true };
        }
    }

    return { exists: false, path: candidate, indexPath, version: null };
}

// ─── 飞书配置解析 ─────────────────────────────────────────────────────────

function getFeishuCredentials() {
    return {
        appId: process.env.FEISHU_APP_ID || process.env.OPENCLAW_FEISHU_APP_ID || null,
        appSecret: process.env.FEISHU_APP_SECRET || process.env.OPENCLAW_FEISHU_APP_SECRET || null,
    };
}

function isFeishuConfigured() {
    if (!FEISHU_ENABLED) return false;
    const creds = getFeishuCredentials();
    return !!(creds.appId && creds.appSecret);
}

module.exports = {
    EVOLVER_CORE_DIR, OPENCLAW_WORKSPACE, WORKSPACE_ROOT,
    WRAPPER_AUTO_CRON, FEISHU_ENABLED,
    WRAPPER_DIR, LOGS_DIR, MEMORY_DIR, ASSETS_DIR,
    EVENTS_FILE, EVOLUTION_STATE_FILE,
    WRAPPER_PID_FILE, DAEMON_PID_FILE,
    WRAPPER_LIFECYCLE_LOG, CYCLE_COUNT_FILE,
    WRAPPER_OUT_LOG, WRAPPER_ERR_LOG,
    DAEMON_OUT_LOG, DAEMON_ERR_LOG,
    resolveEvolverCore, getFeishuCredentials, isFeishuConfigured,
};
