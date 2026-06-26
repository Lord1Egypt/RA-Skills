#!/usr/bin/env node

/**
 * 长期记忆 Skill - memory.js (Node.js 版本)
 * 使用原生 https/http 模块，无外部依赖
 */

const crypto = require('crypto');  // 已有 - 加密签名
const fs = require('fs');          // 已有 - 文件读取
const path = require('path');      // 已有 - 路径处理
const os = require('os');          // 已有 - 获取 home 目录
const https = require('https');    // 已有 - HTTPS 请求
const http = require('http');      // 已有 - HTTP 请求
const { URL } = require('url');    // 已有 - URL 解析

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
    const paths = [path.join(__dirname, '.env')]; // 当前 skill 目录优先
    paths.push(path.join(__dirname, '..', '.env'));

    // 判断当前目录是否包含 mobileclaw
    const cwd = process.cwd();
    const isMobileClaw = cwd.includes('mobileclaw');
    if (isMobileClaw) {
        paths.push(path.join(os.homedir(), '.config', 'mobileclaw', '.env'));
    }
    // else {
    //     paths.push(path.join(os.homedir(), '.openclaw', '.env'));
    // }

    return paths;
}

// ── 环境变量加载 ──────────────────────────────────────────
function getEnv(key, defaultValue = null) {
    // 1. 进程环境变量优先
    if (process.env[key]) return process.env[key];

    // 2. 按优先级读取 .env 文件
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
const HOST = getEnv('MEMORY_BASE_URL', 'https://console.ecloud.10086.cn');
const AK = getEnv('MEMORY_AK', '');
const SK = getEnv('MEMORY_SK', '');
const MEMORY_LIBRARY_ID = getEnv('MEMORY_LIBRARY_ID', '');
const USER_ID = getEnv('MEMORY_USER_ID', '');
const POOL_ID = getEnv('MEMORY_POOL_ID', 'CIDC-RP-48');

log('INFO', `配置: HOST=${HOST} USER_ID=${USER_ID} LIBRARY_ID=${MEMORY_LIBRARY_ID}`);
log('INFO', `AK=${AK ? AK.slice(0, 6) + '***' : '(empty)'}`);

// ── 签名工具函数 ──────────────────────────────────────────
function percentEncode(str) {
    // 1. encodeURIComponent 会对 : / ? & = + 空格 进行编码
    // 2. 它保留了 - _ . ! ~ * ' ( )
    // 3. 我们只需要手动把 ! ' ( ) * 转义为 16 进制，就能和 Python 的 quote_plus 行为完全一致
    return encodeURIComponent(str)
        .replace(/[!'()*]/g, function(c) {
            return '%' + c.charCodeAt(0).toString(16).toUpperCase();
        });
}

function sha256Hex(text) {
    return crypto.createHash('sha256').update(text, 'utf-8').digest('hex');
}

function hmacSha1Hex(text, key) {
    return crypto.createHmac('sha1', key).update(text, 'utf-8').digest('hex');
}

const SECRET_KEY_PREFIX = 'BC_SIGNATURE&';


// 获取本地时间，然后格式化（不加时区转换）
function getLocalTimestamp() {
    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    return `${year}-${month}-${day}T${hours}:${minutes}:${seconds}Z`;
}


/**
 * 生成移动云签名（与 Python 版本完全一致）
 */
function generateSignature(method, pathStr, queryParams) {
    // 1. 构建参数
    const params = {};
    for (const [k, v] of Object.entries(queryParams)) {
        if (v === null || v === undefined) continue;
        params[k] = typeof v === 'object' ? JSON.stringify(v) : String(v);
    }

    const now = new Date();
    const year = now.getFullYear();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');

    params.AccessKey = AK;
    params.SignatureMethod = 'HmacSHA1';
    params.SignatureVersion = 'V2.0';
    params.Timestamp = `${year}-${month}-${day}T${hours}:${minutes}:${seconds}Z`;
    params.SignatureNonce = crypto.randomBytes(16).toString('hex');

    // 2. 按 key 排序
    const sortedKeys = Object.keys(params).sort();

    // 3. 构建 canonical string（这里重点！）
    const parts = [];
    for (const k of sortedKeys) {
        const encodedKey = percentEncode(k);
        const encodedValue = percentEncode(params[k]);
        parts.push(`${encodedKey}=${encodedValue}`);
    }
    const canonicalQs = parts.join('&');

    // 4. SHA256
    const hashString = crypto.createHash('sha256').update(canonicalQs).digest('hex');

    // 5. stringToSign
    const servletPath = decodeURIComponent(pathStr);
    const encodedPath = percentEncode(servletPath);
    const stringToSign = `${method.toUpperCase()}\n${encodedPath}\n${hashString}`;

    // 6. 签名
    const signature = crypto.createHmac('sha1', SECRET_KEY_PREFIX + SK)
        .update(stringToSign)
        .digest('hex');

    return { signature, canonicalQs };
}

// ── HTTP 请求 ─────────────────────────────────────────────
function sendRequest(method, pathStr, payload = null, isGetWithParams = false) {
    return new Promise((resolve, reject) => {
        const requestId = crypto.randomBytes(4).toString('hex');
        log('INFO', `[${requestId}] >>> ${method} ${pathStr}`);

        // 对于 GET 请求，payload 实际上是 URL 参数
        const queryParams = (method === 'GET' && payload) ? payload : {};

        const { signature, canonicalQs } = generateSignature(method, pathStr, queryParams);
        const signedQs = `Signature=${percentEncode(signature)}`;

        let url;
        if (method === 'GET' && canonicalQs) {
            url = `${HOST}${pathStr}?${canonicalQs}&${signedQs}`;
        } else {
            url = `${HOST}${pathStr}?${canonicalQs}&${signedQs}`;
        }

        log('DEBUG', `[${requestId}] URL: ${url.substring(0, 300)}${url.length > 300 ? '...' : ''}`);

        const parsedUrl = new URL(url);
        const isHttps = parsedUrl.protocol === 'https:';

        const options = {
            hostname: parsedUrl.hostname,
            port: parsedUrl.port || (isHttps ? 443 : 80),
            path: parsedUrl.pathname + parsedUrl.search,
            method: method.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
                'Pool-Id': POOL_ID,
            },
            timeout: 15000,
        };

        // 禁用 SSL 验证（如果需要）
        if (isHttps && HOST.includes('31015')) {
            options.rejectUnauthorized = false;
        }

        const req = (isHttps ? https : http).request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => {
                log('INFO', `[${requestId}] <<< HTTP ${res.statusCode} (${data.length} bytes)`);
                log('DEBUG', `[${requestId}] 响应: ${data.substring(0, 500)}`);

                if (!data.trim()) {
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
            log('ERROR', `[${requestId}] 请求失败: ${err.message}`);
            resolve({ error: err.message });
        });

        req.on('timeout', () => {
            req.destroy();
            log('ERROR', `[${requestId}] 请求超时`);
            resolve({ error: '请求超时' });
        });

        // 发送请求体
        if (payload && (method === 'POST' || method === 'PUT')) {
            const body = JSON.stringify(payload);
            req.write(body);
            log('DEBUG', `[${requestId}] 请求体: ${body.substring(0, 500)}`);
        }

        req.end();
    });
}

// ── API 函数 ─────────────────────────────────────────────
const SEARCH_PATH = '/api/web/routes/long-memory-api/memories/search/';
const ADD_PATH = '/api/web/routes/long-memory-api/memories';
const LIST_PATH = '/api/web/routes/long-memory-api/memories';

async function saveMemory(message) {
    log('INFO', `===== save_memory | ${message.length} 字符 =====`);

    const messages = [
        { role: 'user', content: message },
        { role: 'assistant', content: '好的' }
    ];

    const payload = {
        user_id: USER_ID,
        run_id: '',
        memory_library_id: MEMORY_LIBRARY_ID,
        agent_id: '',
        meta_data: { source: 'openclaw' },
        message: messages,
    };

    return await sendRequest('POST', ADD_PATH, payload);
}

async function searchMemory(query, limit = 5) {
    log('INFO', `===== search_memory | query="${query}" limit=${limit} =====`);

    const payload = {
        user_id: USER_ID,
        run_id: '',
        agent_id: '',
        query: query,
        memory_library_id: MEMORY_LIBRARY_ID,
        limit: limit,
        time_start: null,
        time_end: null,
    };

    return await sendRequest('POST', SEARCH_PATH, payload);
}

async function listAll(page = 1, size = 50) {
    log('INFO', `===== list_all | page=${page} size=${size} =====`);

    // GET 请求，参数作为 query string
    const params = {
        memory_library_id: MEMORY_LIBRARY_ID,
        user_id: USER_ID,
        page: page,
        size: size,
    };

    return await sendRequest('GET', LIST_PATH, params);
}

async function checkConfig() {
    const missing = [];
    if (!AK) missing.push('MEMORY_AK');
    if (!SK) missing.push('MEMORY_SK');
    if (!MEMORY_LIBRARY_ID) missing.push('MEMORY_LIBRARY_ID');
    if (!USER_ID) missing.push('MEMORY_USER_ID');

    if (missing.length) {
        return {
            configured: false,
            missing,
            message: `缺少: ${missing.join(', ')}`
        };
    }

    try {
        const result = await listAll(1, 1);
        if (result && result.errorMessage) {
            return { configured: false, error: result.errorMessage };
        }
        return { configured: true, message: '配置正确' };
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
        console.log('  node memory.js search <query> [limit]');
        console.log('  node memory.js save "<message>"');
        console.log('  node memory.js list-all [page] [size]');
        console.log('  node memory.js check-config');
        process.exit(0);
    }

    try {
        let result;
        switch (command) {
            case 'search':
                const query = args[1];
                const limit = parseInt(args[2]) || 5;
                if (!query) throw new Error('缺少查询词');
                result = await searchMemory(query, limit);
                break;
            case 'save':
                const message = args.slice(1).join(' ');
                if (!message) throw new Error('缺少消息');
                result = await saveMemory(message);
                break;
            case 'list-all':
                const page = parseInt(args[1]) || 1;
                const size = parseInt(args[2]) || 50;
                result = await listAll(page, size);
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

module.exports = { saveMemory, searchMemory, listAll, checkConfig };