#!/usr/bin/env node

/**
 * mem0 长期记忆 Skill - memory.js (Node.js 版本)
 * 使用原生 https/http 模块，无外部依赖
 * 通过 mem0 自部署 REST API 服务器实现持久化长期记忆
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// ── 日志配置 ──────────────────────────────────────────────
const LOG_DIR = path.join(__dirname, 'logs');
if (!fs.existsSync(LOG_DIR)) fs.mkdirSync(LOG_DIR, { recursive: true });
const LOG_FILE = path.join(LOG_DIR, 'ltm-handler.log');

function log(level, message, ...args) {
    const timestamp = new Date().toISOString();
    const formatted = `${timestamp} | ${level.padEnd(5)} | ${message}`;
    fs.appendFileSync(LOG_FILE, formatted + '\n');
    if (args.length) console.error(...args);
}

function getEnvPaths() {
    const paths = [path.join(__dirname, '.env')];
    paths.push(path.join(__dirname, '..', '.env'));
    return paths;
}

// ── 环境变量加载 ──────────────────────────────────────────
function getEnv(key, defaultValue = null) {
    if (process.env[key]) return process.env[key];

    const envPaths = getEnvPaths();
    for (const envPath of envPaths) {
        if (fs.existsSync(envPath)) {
            const content = fs.readFileSync(envPath, 'utf-8');
            for (const line of content.split('\n')) {
                const trimmed = line.trim();
                if (!trimmed || trimmed.startsWith('#')) continue;
                const eqIndex = trimmed.indexOf('=');
                if (eqIndex === -1) continue;
                const k = trimmed.slice(0, eqIndex).trim();
                if (k === key) {
                    let value = trimmed.slice(eqIndex + 1).trim();
                    if ((value.startsWith('"') && value.endsWith('"')) ||
                        (value.startsWith("'") && value.endsWith("'"))) {
                        value = value.slice(1, -1);
                    }
                    return value;
                }
            }
        }
    }

    return defaultValue;
}

// ── 配置 ──────────────────────────────────────────────────
const BASE_URL = getEnv('MEM0_BASE_URL', '');
const API_KEY = getEnv('MEM0_API_KEY', '');
const USER_ID = getEnv('MEM0_USER_ID', '');

log('INFO', `配置: BASE_URL=${BASE_URL || '(empty)'} USER_ID=${USER_ID}`);
log('INFO', `API_KEY=${API_KEY ? API_KEY.slice(0, 6) + '***' : '(empty)'}`);

function validateBaseUrl(url) {
    if (!url) return 'MEM0_BASE_URL 未配置';
    try {
        const parsed = new URL(url);
        if (!['http:', 'https:'].includes(parsed.protocol)) {
            return 'MEM0_BASE_URL 必须以 http:// 或 https:// 开头';
        }
        if (!parsed.hostname) {
            return 'MEM0_BASE_URL 缺少主机名';
        }
        return null;
    } catch (e) {
        return `MEM0_BASE_URL 格式无效: ${e.message}`;
    }
}

// ── 认证请求头 ────────────────────────────────────────────
function getAuthHeaders() {
    const headers = { 'Content-Type': 'application/json' };
    if (API_KEY) {
        headers['X-API-Key'] = API_KEY;
    }
    return headers;
}

// ── HTTP 请求 ─────────────────────────────────────────────
function sendRequest(method, pathStr, payload = null) {
    return new Promise((resolve, reject) => {
        const requestId = crypto.randomBytes(4).toString('hex');
        log('INFO', `[${requestId}] >>> ${method} ${pathStr}`);

        let url;
        if (method === 'GET' && payload) {
            const params = new URLSearchParams();
            for (const [k, v] of Object.entries(payload)) {
                if (v !== null && v !== undefined) params.append(k, v);
            }
            url = `${BASE_URL}${pathStr}?${params.toString()}`;
        } else if (method === 'DELETE' && payload) {
            const params = new URLSearchParams();
            for (const [k, v] of Object.entries(payload)) {
                if (v !== null && v !== undefined) params.append(k, v);
            }
            url = `${BASE_URL}${pathStr}?${params.toString()}`;
        } else {
            url = `${BASE_URL}${pathStr}`;
        }

        log('DEBUG', `[${requestId}] URL: ${url.substring(0, 300)}${url.length > 300 ? '...' : ''}`);

        const parsedUrl = new URL(url);
        const isHttps = parsedUrl.protocol === 'https:';

        const options = {
            hostname: parsedUrl.hostname,
            port: parsedUrl.port || (isHttps ? 443 : 80),
            path: parsedUrl.pathname + parsedUrl.search,
            method: method.toUpperCase(),
            headers: getAuthHeaders(),
            timeout: 60000,
        };

        const req = (isHttps ? https : http).request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                log('INFO', `[${requestId}] <<< HTTP ${res.statusCode} (${data.length} bytes)`);
                log('DEBUG', `[${requestId}] 响应: ${data.substring(0, 500)}`);

                if (res.statusCode === 401) {
                    resolve({ error: '认证失败：API Key 无效或缺失', status: 401 });
                    return;
                }

                if (res.statusCode === 204 || !data.trim()) {
                    resolve({ status: 'success' });
                    return;
                }

                try {
                    const jsonData = JSON.parse(data);
                    resolve(jsonData);
                } catch (e) {
                    log('ERROR', `[${requestId}] JSON解析失败: ${e.message}`);
                    resolve({ error: `响应解析失败: ${e.message}`, raw: data.substring(0, 500) });
                }
            });
        });

        req.on('error', (err) => {
            const errMsg = err.message || err.code || 'Unknown error';
            log('ERROR', `[${requestId}] 请求失败: ${errMsg}`);
            resolve({ error: errMsg });
        });

        req.on('timeout', () => {
            req.destroy();
            log('ERROR', `[${requestId}] 请求超时`);
            resolve({ error: '请求超时' });
        });

        if (payload && (method === 'POST' || method === 'PUT')) {
            const body = JSON.stringify(payload);
            req.write(body);
            log('DEBUG', `[${requestId}] 请求体: ${body.substring(0, 500)}`);
        }

        req.end();
    });
}

// ── API 函数 ─────────────────────────────────────────────
async function saveMemory(message) {
    log('INFO', `===== save_memory | ${message.length} 字符 =====`);

    const payload = {
        messages: [
            { role: 'user', content: message },
            { role: 'assistant', content: '好的' }
        ],
        user_id: USER_ID
    };

    return await sendRequest('POST', '/memories', payload);
}

async function searchMemory(query, limit = 5) {
    log('INFO', `===== search_memory | query="${query}" limit=${limit} =====`);

    // 重要：user_id 必须放在 filters 内，不能放在顶层
    // 服务端 Memory.search() 通过 _reject_top_level_entity_params 拒绝顶层 user_id
    const payload = {
        query: query,
        filters: { user_id: USER_ID },
        top_k: limit
    };

    return await sendRequest('POST', '/search', payload);
}

async function listAll() {
    log('INFO', `===== list_all =====`);

    return await sendRequest('GET', '/memories', { user_id: USER_ID });
}

async function getMemory(id) {
    log('INFO', `===== get_memory | id=${id} =====`);

    return await sendRequest('GET', `/memories/${id}`);
}

async function updateMemory(id, text) {
    log('INFO', `===== update_memory | id=${id} =====`);

    const payload = { text: text };
    return await sendRequest('PUT', `/memories/${id}`, payload);
}

async function deleteMemory(id) {
    log('INFO', `===== delete_memory | id=${id} =====`);

    return await sendRequest('DELETE', `/memories/${id}`);
}

async function deleteAll() {
    log('INFO', `===== delete_all =====`);

    return await sendRequest('DELETE', '/memories', { user_id: USER_ID });
}

async function checkConfig() {
    const missing = [];
    const errors = [];
    if (!BASE_URL) {
        missing.push('MEM0_BASE_URL');
    } else {
        const urlError = validateBaseUrl(BASE_URL);
        if (urlError) errors.push(urlError);
    }
    if (!API_KEY) missing.push('MEM0_API_KEY');
    if (!USER_ID) missing.push('MEM0_USER_ID');

    if (missing.length || errors.length) {
        const parts = [];
        if (missing.length) parts.push(`缺少必填配置: ${missing.join(', ')}`);
        if (errors.length) parts.push(errors.join('; '));
        return {
            configured: false,
            missing,
            errors,
            message: parts.join('; ')
        };
    }

    try {
        const result = await sendRequest('GET', '/auth/setup-status');
        if (result && result.error) {
            return { configured: false, error: result.error };
        }
        return { configured: true, message: '配置正确，连接正常' };
    } catch (error) {
        return { configured: false, error: error.message };
    }
}

// ── 命令行入口 ─────────────────────────────────────────────
async function main() {
    const args = process.argv.slice(2);
    const command = args[0];

    if (!command) {
        console.log('用法:');
        console.log('  node memory.js save "<message>"');
        console.log('  node memory.js search "<query>" [limit]');
        console.log('  node memory.js list');
        console.log('  node memory.js get <id>');
        console.log('  node memory.js update <id> "<text>"');
        console.log('  node memory.js delete <id>');
        console.log('  node memory.js delete-all');
        console.log('  node memory.js check-config');
        process.exit(0);
    }

    try {
        let result;
        switch (command) {
            case 'save':
                const message = args.slice(1).join(' ');
                if (!message) throw new Error('缺少消息内容');
                result = await saveMemory(message);
                break;
            case 'search':
                const query = args[1];
                const limit = parseInt(args[2]) || 5;
                if (!query) throw new Error('缺少查询词');
                result = await searchMemory(query, limit);
                break;
            case 'list':
                result = await listAll();
                break;
            case 'get':
                const getId = args[1];
                if (!getId) throw new Error('缺少记忆 ID');
                result = await getMemory(getId);
                break;
            case 'update':
                const updateId = args[1];
                const updateText = args.slice(2).join(' ');
                if (!updateId) throw new Error('缺少记忆 ID');
                if (!updateText) throw new Error('缺少更新内容');
                result = await updateMemory(updateId, updateText);
                break;
            case 'delete':
                const deleteId = args[1];
                if (!deleteId) throw new Error('缺少记忆 ID');
                result = await deleteMemory(deleteId);
                break;
            case 'delete-all':
                result = await deleteAll();
                break;
            case 'check-config':
                result = await checkConfig();
                break;
            default:
                console.log(`未知命令: ${command}`);
                process.exit(1);
        }
        console.log(JSON.stringify(result, null, 2));
    } catch (error) {
        console.log(JSON.stringify({ error: error.message }));
        process.exit(1);
    }
}

if (require.main === module) {
    main();
}

module.exports = { saveMemory, searchMemory, listAll, getMemory, updateMemory, deleteMemory, deleteAll, checkConfig };
