const fs = require('fs');
const path = require('path');

// 共享数据目录，独立于 skill 版本。发布新版本不会覆盖用户配置。
// __dirname = .../SKILLs/fecify_skills/scripts/base
// LOBSTER_AI_DIR = .../LobsterAI
// SESSIONS_DIR = .../LobsterAI/data/fecify-shared/sessions
const LOBSTER_AI_DIR = path.join(__dirname, '..', '..', '..', '..');
const SESSIONS_DIR = path.join(LOBSTER_AI_DIR, 'data', 'fecify-shared', 'sessions');
const SITES_ROOT = SESSIONS_DIR;
const DEFAULT_SESSION = path.join(SESSIONS_DIR, 'current_default.txt');

// ---- 获取当前会话的域名绑定文件 ----
// 每个会话通过 FECIFY_SESSION 环境变量标识自己
// FECIFY_SESSION=agent-a → 读写 current_agent-a.txt
// FECIFY_SESSION=agent-b → 读写 current_agent-b.txt
// 未设 FECIFY_SESSION → 用默认会话文件 current_default.txt（不走全局共享）
function _sessionFile() {
    const sid = process.env.FECIFY_SESSION;
    return sid
        ? path.join(SESSIONS_DIR, `current_${sid.replace(/[\\/]/g, '_')}.txt`)
        : DEFAULT_SESSION;
}

// ---- 获取当前会话的域名 ----
// 优先级: env FECIFY_DOMAIN > 会话文件
function getDomain() {
    // 1. 环境变量优先（临时覆盖）
    if (process.env.FECIFY_DOMAIN) {
        return process.env.FECIFY_DOMAIN.trim();
    }
    // 2. 会话绑定文件
    const sf = _sessionFile();
    try {
        const d = fs.readFileSync(sf, 'utf8').trim();
        if (d) return d;
    } catch { /* 不存在 */ }
    return null;
}

// ---- 设置当前会话的域名 ----
function setDomain(domain) {
    const sf = _sessionFile();
    fs.writeFileSync(sf, domain, 'utf8');
}

// ---- 获取指定域名的配置 ----
function getConfig(domain) {
    const file = path.join(SITES_ROOT, domain, 'config.json');
    if (!fs.existsSync(file)) return null;
    return JSON.parse(fs.readFileSync(file, 'utf8'));
}

// ---- 获取当前会话的配置 ----
function getCurrentConfig() {
    const domain = getDomain();
    if (!domain) return null;
    return getConfig(domain);
}

// ---- 保存配置（自动绑定到当前会话）----
function saveConfig(domain, url, token) {
    const dir = path.join(SITES_ROOT, domain);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    fs.writeFileSync(
        path.join(dir, 'config.json'),
        JSON.stringify({ url, token, updatedAt: new Date().toISOString() }, null, 2),
        'utf8'
    );

    // 写入会话绑定文件（每个 session 独立存储，不共享）
    const sf = _sessionFile();
    fs.writeFileSync(sf, domain, 'utf8');
}

// ---- 检查当前会话是否已配置 ----
function isConfigured() {
    const cfg = getCurrentConfig();
    return !!(cfg && cfg.url && cfg.token);
}

// ---- 检查指定域名是否已配置 ----
function isDomainConfigured(domain) {
    const cfg = getConfig(domain);
    return !!(cfg && cfg.url && cfg.token);
}

// ---- 保存 init 数据（/api/skill/base/init 返回的 data 对象）----
function saveInitData(domain, data) {
    const dir = path.join(SITES_ROOT, domain);
    if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });

    fs.writeFileSync(
        path.join(dir, 'init-data.json'),
        JSON.stringify({ data, updatedAt: new Date().toISOString() }, null, 2),
        'utf8'
    );
}

// ---- 获取指定域名的 init 数据 ----
function getInitData(domain) {
    const file = path.join(SITES_ROOT, domain, 'init-data.json');
    if (!fs.existsSync(file)) return null;
    return JSON.parse(fs.readFileSync(file, 'utf8'));
}

// ---- 获取当前会话的 init 数据 ----
function getCurrentInitData() {
    const domain = getDomain();
    if (!domain) return null;
    return getInitData(domain);
}

// ---- 检查当前会话是否已有 init 数据 ----
function hasInitData() {
    return !!getCurrentInitData();
}

module.exports = {
    getDomain, setDomain,
    getConfig, getCurrentConfig,
    saveConfig,
    saveInitData, getInitData, getCurrentInitData, hasInitData,
    isConfigured, isDomainConfigured
};
