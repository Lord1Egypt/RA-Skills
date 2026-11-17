/**
 * Proxy loading, shared by amazon_handler / main_handler / full_extract.
 *
 * Precedence is env-var first so that `-e AMAZON_PROXIES=...` actually works.
 * The previous file-first order silently ignored the env var that every doc
 * and example used, which let several containers hammer one exit IP.
 *
 * Credentials are never printed: redact() is the only approved way to log a proxy.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const DEFAULT_CONFIG_PATH = path.join(__dirname, '..', 'config', 'proxies.json');

function parseList(raw) {
    return raw.split(',').map(s => s.trim()).filter(Boolean);
}

function readProxyFile(filePath) {
    const cfg = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    if (!Array.isArray(cfg.proxies)) {
        throw new Error(`${filePath}: "proxies" must be an array`);
    }
    return cfg.proxies.map(s => String(s).trim()).filter(Boolean);
}

function loadProxies({ configPath = DEFAULT_CONFIG_PATH } = {}) {
    if (process.env.AMAZON_PROXIES) return parseList(process.env.AMAZON_PROXIES);
    if (process.env.AMAZON_PROXY) return [process.env.AMAZON_PROXY.trim()];

    const filePath = process.env.AMAZON_PROXY_FILE || configPath;
    if (fs.existsSync(filePath)) {
        try {
            return readProxyFile(filePath);
        } catch (e) {
            throw new Error(`Failed to load ${filePath}: ${e.message}`);
        }
    }
    return [];
}

/** Host:port only. Safe to log, store, and put in error messages. */
function redact(proxyUrl) {
    if (!proxyUrl) return 'none';
    try {
        const u = new URL(proxyUrl);
        return `${u.protocol}//${u.host}`;
    } catch {
        return 'invalid-proxy-url';
    }
}

function parseProxy(proxyUrl) {
    const u = new URL(proxyUrl);
    if (!/^https?:$/.test(u.protocol)) {
        throw new Error(`unsupported proxy protocol "${u.protocol}" (use http:// or https://)`);
    }
    return {
        server: `${u.protocol}//${u.host}`,
        username: decodeURIComponent(u.username),
        password: decodeURIComponent(u.password)
    };
}

/**
 * Rotates proxies and refuses to run without one, so a misconfigured setup fails
 * loudly instead of scraping from the host IP and getting it blocked.
 */
function createProxyPool({ configPath, allowDirect = process.env.AMAZON_ALLOW_DIRECT === '1' } = {}) {
    const list = loadProxies({ configPath });

    if (list.length === 0 && !allowDirect) {
        throw new Error(
            'No proxy configured. Set AMAZON_PROXIES="http://user:pass@host:port[,...]" ' +
            'or create config/proxies.json from config/proxies.example.json. ' +
            'To scrape from this host\'s own IP anyway, set AMAZON_ALLOW_DIRECT=1.'
        );
    }

    const parsed = list.map(raw => {
        try {
            return { raw, parsed: parseProxy(raw) };
        } catch (e) {
            throw new Error(`Invalid proxy entry ${redact(raw)}: ${e.message}`);
        }
    });

    let idx = 0;
    return {
        size: parsed.length,
        next() {
            if (parsed.length === 0) return null;
            return parsed[idx++ % parsed.length];
        }
    };
}

module.exports = { loadProxies, parseProxy, createProxyPool, redact, DEFAULT_CONFIG_PATH };
