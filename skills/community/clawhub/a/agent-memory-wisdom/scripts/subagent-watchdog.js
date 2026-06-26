#!/usr/bin/env node
/**
 * 工具调用看门狗 - 通用容错包装器
 * 功能1：exec超时自动重试 + 预检文件存在
 * 功能2：子agent看门狗（原有）
 */

const fs = require('fs');
const { execSync } = require('child_process');
const { exec } = require('child_process');
const path = require('path');

const WATCHDOG_LOG = path.join(process.env.HOME, '.openclaw/workspace/memory/watchdog-log.md');
const MAX_RETRIES = 3;
const DEFAULT_TIMEOUT = 120000; // 2分钟

function log(message) {
    const timestamp = new Date().toISOString().replace('T', ' ').substring(0, 19);
    const line = `[${timestamp}] ${message}\n`;
    try {
        fs.appendFileSync(WATCHDOG_LOG, line);
    } catch (e) {}
    console.log(line.trim());
}

// ============================================================
// 核心功能1：exec超时自动重试 + 预检
// ============================================================

/**
 * 预检文件/目录是否存在
 * @param {string} filePath - 文件路径
 * @returns {{exists: boolean, isFile: boolean, isDir: boolean}}
 */
function preCheck(filePath) {
    if (!filePath) return { exists: false, isFile: false, isDir: false, error: 'empty path' };
    try {
        const stat = fs.statSync(filePath);
        return { exists: true, isFile: stat.isFile(), isDir: stat.isDirectory(), error: null };
    } catch (e) {
        return { exists: false, isFile: false, isDir: false, error: e.code };
    }
}

/**
 * 执行命令（超时保护）
 * @param {string} cmd - 命令
 * @param {object} options - {timeout: ms, cwd: 工作目录, maxRetries: 次数}
 * @returns {{success: boolean, stdout: string, stderr: string, error: string, attempts: number}}
 */
function execWithRetry(cmd, options = {}) {
    const timeout = options.timeout || DEFAULT_TIMEOUT;
    const maxRetries = options.maxRetries || MAX_RETRIES;
    const cwd = options.cwd || process.cwd();
    let attempts = 0;

    for (let i = 1; i <= maxRetries; i++) {
        attempts = i;
        try {
            log(`[exec] 第${i}次尝试: ${cmd.substring(0, 60)}${cmd.length > 60 ? '...' : ''}`);
            const result = execSync(cmd, { 
                timeout, 
                encoding: 'utf8',
                cwd,
                stdio: ['pipe', 'pipe', 'pipe']
            });
            return { success: true, stdout: result, stderr: '', error: null, attempts };
        } catch (e) {
            const isTimeout = e.message && e.message.includes('ENOTEMPTY');
            const isKilled = e.killed || (e.status === null);
            log(`[exec] 第${i}次失败: ${isKilled ? '超时' : e.message.substring(0, 80)}`);
            
            if (i < maxRetries) {
                const delay = Math.min(1000 * Math.pow(2, i - 1), 10000);
                log(`[exec] 等待${delay}ms后重试...`);
                // busy wait
                const start = Date.now();
                while (Date.now() - start < delay) {}
            } else {
                return { 
                    success: false, 
                    stdout: e.stdout || '', 
                    stderr: e.stderr || '', 
                    error: isKilled ? 'TIMEOUT' : e.message,
                    attempts
                };
            }
        }
    }
    return { success: false, stdout: '', stderr: '', error: 'MAX_RETRIES', attempts };
}

/**
 * 通用工具调用包装器
 * @param {Function} fn - 要执行的函数
 * @param {object} options - {timeout, maxRetries, preCheck: ()=>boolean, name: string}
 * @returns {Promise<{success: boolean, data: any, error: string, attempts: number}>}
 */
async function wrapToolCall(fn, options = {}) {
    const name = options.name || 'unknown';
    const maxRetries = options.maxRetries || MAX_RETRIES;
    let attempts = 0;

    // 预检阶段
    if (options.preCheck) {
        log(`[${name}] 预检...`);
        const preResult = options.preCheck();
        if (!preResult.pass) {
            log(`[${name}] 预检失败: ${preResult.reason}`);
            return { success: false, data: null, error: 'PRECHECK_FAILED: ' + preResult.reason, attempts: 0 };
        }
        log(`[${name}] 预检通过`);
    }

    // 执行+重试阶段
    for (let i = 1; i <= maxRetries; i++) {
        attempts = i;
        try {
            log(`[${name}] 执行中 (第${i}次)...`);
            const result = await Promise.race([
                fn(),
                new Promise((_, reject) => 
                    setTimeout(() => reject(new Error('TIMEOUT')), options.timeout || DEFAULT_TIMEOUT)
                )
            ]);
            log(`[${name}] ✅ 成功`);
            return { success: true, data: result, error: null, attempts };
        } catch (e) {
            const isTimeout = e.message === 'TIMEOUT';
            log(`[${name}] ❌ 失败: ${isTimeout ? '超时' : e.message.substring(0, 100)}`);
            if (i < maxRetries) {
                const delay = Math.min(1000 * Math.pow(2, i - 1), 10000);
                log(`[${name}] ${delay}ms后重试...`);
                await new Promise(r => setTimeout(r, delay));
            } else {
                log(`[${name}] 💥 达到最大重试次数`);
                return { success: false, data: null, error: isTimeout ? 'TIMEOUT' : e.message, attempts };
            }
        }
    }
}

// ============================================================
// 核心功能2：子Agent看门狗（原有逻辑）
// ============================================================

function runSubagent(task, timeout = DEFAULT_TIMEOUT) {
    const taskJson = JSON.stringify(task);
    const tempFile = `/tmp/watchdog-task-${Date.now()}.json`;
    try {
        fs.writeFileSync(tempFile, taskJson);
        const result = execSync(
            `openclaw sessions_spawn --runtime subagent --task-file ${tempFile}`,
            { timeout, encoding: 'utf8' }
        );
        fs.unlinkSync(tempFile);
        return { success: true, output: result };
    } catch (error) {
        try { fs.unlinkSync(tempFile); } catch (e) {}
        return { success: false, error: error.message, code: error.status };
    }
}

function verifyResult(result) {
    if (!result.success) return { valid: false, reason: 'execution_failed' };
    if (!result.output || result.output.trim() === '') return { valid: false, reason: 'empty_output' };
    if (result.output.includes('ERROR') || result.output.includes('失败')) return { valid: false, reason: 'error_in_output' };
    return { valid: true };
}

async function watchdog(task, options = {}) {
    const maxRetries = options.maxRetries || MAX_RETRIES;
    const timeout = options.timeout || DEFAULT_TIMEOUT;
    const taskId = `task-${Date.now()}`;
    
    log(`[${taskId}] 开始执行任务: ${task.description || '未命名任务'}`);
    
    for (let attempt = 1; attempt <= maxRetries; attempt++) {
        log(`[${taskId}] 第${attempt}次尝试...`);
        const result = runSubagent(task, timeout);
        const verification = verifyResult(result);
        
        if (verification.valid) {
            log(`[${taskId}] ✅ 成功 (第${attempt}次)`);
            return { success: true, output: result.output, attempts: attempt };
        }
        
        log(`[${taskId}] ❌ 失败: ${verification.reason}`);
        if (attempt < maxRetries) {
            const delay = Math.min(1000 * Math.pow(2, attempt - 1), 10000);
            log(`[${taskId}] 等待${delay}ms后重试...`);
            await new Promise(r => setTimeout(r, delay));
        }
    }
    
    log(`[${taskId}] 💥 最终失败，已重试${maxRetries}次`);
    return { success: false, error: 'max_retries_exceeded', attempts: maxRetries };
}

// ============================================================
// 命令行入口
// ============================================================

const args = process.argv.slice(2);
const command = args[0];

if (command === 'exec') {
    // 用法: node subagent-watchdog.js exec "<cmd>" [timeout] [maxRetries]
    const cmd = args[1];
    const timeout = parseInt(args[2]) || DEFAULT_TIMEOUT;
    const maxRetries = parseInt(args[3]) || MAX_RETRIES;
    if (!cmd) {
        console.log('用法: node subagent-watchdog.js exec "<命令>" [超时ms] [最大重试]');
        process.exit(1);
    }
    const result = execWithRetry(cmd, { timeout, maxRetries });
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.success ? 0 : 1);
} else if (command === 'check') {
    // 用法: node subagent-watchdog.js check <文件路径>
    const filePath = args[1];
    if (!filePath) {
        console.log('用法: node subagent-watchdog.js check <文件路径>');
        process.exit(1);
    }
    const result = preCheck(filePath);
    console.log(JSON.stringify(result, null, 2));
    process.exit(result.exists ? 0 : 1);
} else if (command === 'wrap') {
    // 用法: node subagent-watchdog.js wrap "<js函数>" [超时ms]
    // 这个需要传入js代码 不太适合命令行 留作api调用
    console.log('wrap需要用require调用，不适合命令行');
    process.exit(1);
} else if (!command) {
    // 无参数：运行子agent看门狗
    const taskFile = args[1];
    if (!taskFile) {
        console.log(`用法:`);
        console.log(`  node subagent-watchdog.js exec "<命令>" [超时ms] [最大重试]`);
        console.log(`  node subagent-watchdog.js check <文件路径>`);
        console.log(`  node subagent-watchdog.js <task-file.json>`);
        process.exit(1);
    }
    const task = JSON.parse(fs.readFileSync(taskFile, 'utf8'));
    watchdog(task).then(result => {
        console.log(JSON.stringify(result, null, 2));
        process.exit(result.success ? 0 : 1);
    });
} else {
    // 当作task-file处理
    const task = JSON.parse(fs.readFileSync(command, 'utf8'));
    watchdog(task).then(result => {
        console.log(JSON.stringify(result, null, 2));
        process.exit(result.success ? 0 : 1);
    });
}

module.exports = { 
    execWithRetry,   // exec超时重试
    preCheck,        // 文件预检
    wrapToolCall,    // 通用包装器
    watchdog,        // 子agent看门狗
    runSubagent,
    verifyResult
};
