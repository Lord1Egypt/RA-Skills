#!/usr/bin/env node
/**
 * init_skill.cjs — AIDR-XClaw-Security-Sentinel 统一初始化脚本
 *
 * 在首次使用时执行，将以下两项合并为一次操作：
 *   1. AGENTS.md 注入安全脚本 (inject_security_quickref.cjs)
 *   2. API Key 获取与保存 (fingerprint.mjs + API 调用)
 *   3. 安装 aidr-xclaw-security-sentinel 插件 (install_aidr_xclaw_plugin.cjs)
 *
 * 已执行过初始化则自动跳过。
 *
 * 使用方式：
 *   node init_skill.cjs
 *
 * 状态文件：
 *   {baseDir}/.state/init_state.json
 *   {baseDir}/.state/api_state.json
 */

'use strict';

const { spawn, execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// ── Config ────────────────────────────────────────────────────────────────────

const API_BASE = process.env.AIDR_SECURITY_API_BASE || 'https://venustech-ai.online:28200';

// ── Paths ─────────────────────────────────────────────────────────────────────

const scriptDir = __dirname;
const baseDir = path.dirname(scriptDir);
const stateDir = path.join(baseDir, '.state');
const initStateFile = path.join(stateDir, 'init_state.json');
const apiStateFile = path.join(stateDir, 'api_state.json');
const fingerprintScript = path.join(scriptDir, 'fingerprint.mjs');

const REPO_ROOT = path.resolve(baseDir, '..', '..');
const AGENTS_MD = path.join(REPO_ROOT, 'AGENTS.md');

const INJECT_SCRIPT = path.join(scriptDir, 'inject_security_quickref.cjs');
const PLUGIN_SCRIPT = path.join(scriptDir, 'install_aidr_xclaw_plugin.cjs');

// ── Logging ──────────────────────────────────────────────────────────────────

function log(prefix, message) {
  const ts = new Date().toISOString().substring(11, 19);
  console.log(`[${ts}] [${prefix}] ${message}`);
}

// ── State management ─────────────────────────────────────────────────────────

function loadInitState() {
  if (!fs.existsSync(initStateFile)) return null;
  try {
    return JSON.parse(fs.readFileSync(initStateFile, 'utf8'));
  } catch {
    return null;
  }
}

function saveInitState(data) {
  if (!fs.existsSync(stateDir)) {
    fs.mkdirSync(stateDir, { recursive: true });
  }
  fs.writeFileSync(initStateFile, JSON.stringify(data, null, 2), 'utf8');
  log('OK', `状态已写入: ${initStateFile}`);
}

function markInitialized(apiKeyConfigured, pluginConfigured) {
  saveInitState({
    initialized: true,
    initialized_at: new Date().toISOString(),
    api_key_configured: apiKeyConfigured,
    plugin_configured: pluginConfigured
  });
}

function isAlreadyInitialized() {
  const state = loadInitState();
  return state && state.initialized === true;
}

// ── exec helpers ─────────────────────────────────────────────────────────────

function execNode(scriptPath, args, cwd) {
  return new Promise((resolve, reject) => {
    const allArgs = args || [];
    log('CMD', `node "${scriptPath}" ${allArgs.join(' ') || '(no args)'}`);
    const proc = spawn('node', [scriptPath, ...allArgs], {
      cwd: cwd || process.cwd(),
      shell: true,
      stdio: 'inherit'
    });
    proc.on('close', (code) => {
      if (code === 0) {
        resolve(code);
      } else {
        reject(new Error(`Script exited with code ${code}`));
      }
    });
    proc.on('error', (err) => reject(err));
  });
}

// ── Stage 1: AGENTS.md 注入 ──────────────────────────────────────────────────

async function stage1_injectQuickref() {
  console.log('');
  console.log('┌─────────────────────────────────────────────────────────┐');
  console.log('│ [AIDR-XClaw-Sentinel][Init][Stage 1/3] AGENTS.md 注入 │');
  console.log('├─────────────────────────────────────────────────────────┤');
  console.log('│ 操作: 运行 inject_security_quickref.cjs                │');

  if (!fs.existsSync(INJECT_SCRIPT)) {
    console.log('│ 结果: SKIP — inject_security_quickref.cjs 不存在        │');
    console.log('└─────────────────────────────────────────────────────────┘');
    log('SKIP', 'inject_security_quickref.cjs 不存在，跳过');
    return true;
  }

  if (!fs.existsSync(AGENTS_MD)) {
    console.log('│ 结果: SKIP — AGENTS.md 不存在                           │');
    console.log('└─────────────────────────────────────────────────────────┘');
    log('SKIP', 'AGENTS.md 不存在，跳过');
    return true;
  }

  const content = fs.readFileSync(AGENTS_MD, 'utf8');
  if (content.includes('SecurityQuickRef.md') || content.includes('## SecurityQuickRef')) {
    console.log('│ 结果: SKIP — SecurityQuickRef 已存在                     │');
    console.log('└─────────────────────────────────────────────────────────┘');
    log('SKIP', 'AGENTS.md 已注入 SecurityQuickRef，跳过');
    return true;
  }

  try {
    await execNode(INJECT_SCRIPT, [], path.dirname(INJECT_SCRIPT));
    console.log('│ 结果: OK — AGENTS.md 注入完成                           │');
    console.log('└─────────────────────────────────────────────────────────┘');
    return true;
  } catch (err) {
    console.log(`│ 结果: FAIL — ${err.message.substring(0, 36).padEnd(36)} │`);
    console.log('└─────────────────────────────────────────────────────────┘');
    return false;
  }
}

// ── Stage 2: API Key 获取 ───────────────────────────────────────────────────

async function stage2_getApiKey() {
  console.log('');
  console.log('┌─────────────────────────────────────────────────────────┐');
  console.log('│ [AIDR-XClaw-Sentinel][Init][Stage 2/3] API Key 获取     │');
  console.log('├─────────────────────────────────────────────────────────┤');
  console.log('│ 操作: 生成设备指纹并申请 API Key                         │');

  if (fs.existsSync(apiStateFile)) {
    try {
      const existing = JSON.parse(fs.readFileSync(apiStateFile, 'utf8'));
      if (existing.api_key && existing.api_key.length > 0) {
        console.log('│ 结果: SKIP — API Key 已存在                              │');
        console.log('└─────────────────────────────────────────────────────────┘');
        log('SKIP', 'API Key 已存在，跳过');
        return true;
      }
    } catch { /* ignore */ }
  }

  let fingerprint;
  try {
    if (!fs.existsSync(fingerprintScript)) {
      console.log('│ 结果: SKIP — fingerprint.mjs 不存在                      │');
      console.log('└─────────────────────────────────────────────────────────┘');
      log('SKIP', 'fingerprint.mjs 不存在，跳过');
      return false;
    }

    console.log('│ 步骤 2.1: 生成设备指纹...                              │');
    fingerprint = execSync(`node "${fingerprintScript}"`, {
      encoding: 'utf8',
      cwd: scriptDir
    }).trim();

    if (!fingerprint || fingerprint.length !== 64) {
      throw new Error(`Invalid fingerprint: ${fingerprint}`);
    }
    console.log(`│   指纹: ${fingerprint.substring(0, 16)}...                │`);
    log('OK', `设备指纹: ${fingerprint}`);
  } catch (err) {
    console.log(`│ 结果: FAIL — 指纹生成失败: ${err.message.substring(0, 28).padEnd(28)} │`);
    console.log('└─────────────────────────────────────────────────────────┘');
    log('FAIL', `指纹生成失败: ${err.message}`);
    return false;
  }

  console.log('│ 步骤 2.2: 申请 API Key...                              │');
  let apiKey;
  try {
    const body = JSON.stringify({ fingerprint });
    const url = new URL(`${API_BASE}/api/baseline/api_key/distribute`);

    const response = await new Promise((resolve, reject) => {
      const lib = url.protocol === 'https:' ? https : http;
      const reqOptions = {
        hostname: url.hostname,
        port: url.port,
        path: url.pathname,
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body)
        },
        timeout: 10000
      };
      // 跳过 SSL 证书验证（适用于自签名证书环境）
      if (url.protocol === 'https:') {
        reqOptions.rejectUnauthorized = false;
      }
      const req = lib.request(reqOptions, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => resolve({ status: res.statusCode, data }));
      });
      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('Request timeout')); });
      req.write(body);
      req.end();
    });

    if (response.status !== 200) {
      throw new Error(`HTTP ${response.status}: ${response.data}`);
    }

    const parsed = JSON.parse(response.data);
    apiKey = parsed.api_key;

    if (!apiKey) {
      throw new Error('API Key not in response');
    }

    console.log(`│   API Key: ${apiKey.substring(0, 16)}...                │`);
    log('OK', `API Key 获取成功`);
  } catch (err) {
    console.log(`│ 结果: FAIL — API Key 申请失败: ${err.message.substring(0, 26).padEnd(26)} │`);
    console.log('└─────────────────────────────────────────────────────────┘');
    log('FAIL', `API Key 申请失败: ${err.message}`);
    return false;
  }

  console.log('│ 步骤 2.3: 保存到本地状态文件...                       │');
  try {
    if (!fs.existsSync(stateDir)) {
      fs.mkdirSync(stateDir, { recursive: true });
    }
    const state = {
      api_key: apiKey,
      created_at: new Date().toISOString()
    };
    fs.writeFileSync(apiStateFile, JSON.stringify(state, null, 2), 'utf8');
    console.log('│ 结果: OK — API Key 已保存                               │');
    console.log('└─────────────────────────────────────────────────────────┘');
    log('OK', `API Key 已保存到: ${apiStateFile}`);
    return true;
  } catch (err) {
    console.log(`│ 结果: FAIL — 保存失败: ${err.message.substring(0, 32).padEnd(32)} │`);
    console.log('└─────────────────────────────────────────────────────────┘');
    log('FAIL', `API Key 保存失败: ${err.message}`);
    return false;
  }
}

// ── Stage 3: 插件安装 ────────────────────────────────────────────────────────

async function stage3_installPlugin() {
  console.log('');
  console.log('┌─────────────────────────────────────────────────────────┐');
  console.log('│ [AIDR-XClaw-Sentinel][Init][Stage 3/3] 插件安装         │');
  console.log('├─────────────────────────────────────────────────────────┤');
  console.log('│ 操作: 运行 install_aidr_xclaw_plugin.cjs                 │');

  if (!fs.existsSync(PLUGIN_SCRIPT)) {
    console.log('│ 结果: SKIP — install_aidr_xclaw_plugin.cjs 不存在         │');
    console.log('└─────────────────────────────────────────────────────────┘');
    log('SKIP', 'install_aidr_xclaw_plugin.cjs 不存在，跳过');
    return true;
  }

  try {
    await execNode(PLUGIN_SCRIPT, [], path.dirname(PLUGIN_SCRIPT));
    console.log('│ 结果: OK — 插件安装完成                                  │');
    console.log('└─────────────────────────────────────────────────────────┘');
    return true;
  } catch (err) {
    console.log(`│ 结果: FAIL — ${err.message.substring(0, 36).padEnd(36)} │`);
    console.log('└─────────────────────────────────────────────────────────┘');
    return false;
  }
}

// ── DONE block ────────────────────────────────────────────────────────────────

function printDONE(injectResult, apiKeyResult, pluginResult) {
  const allOk = injectResult && apiKeyResult && pluginResult;
  const icon = allOk ? '✅' : '⚠️';
  const conclusion = allOk ? '初始化成功' : '部分失败（见上方日志）';

  console.log('');
  console.log('════════════════════════════════════════════════════════════');
  console.log('[AIDR-XClaw-Sentinel][Init] 初始化完成');
  console.log('安装结论: ' + conclusion);
  console.log('════════════════════════════════════════════════════════════');
  console.log('');
  console.log(`${icon} AIDR-XClaw-Security-Sentinel 初始化 ${allOk ? '成功' : '部分成功'}`);
  console.log('');
  console.log('初始化项目:');
  console.log(`  [1/3] AGENTS.md 安全脚本注入  — ${injectResult ? '✅ 完成' : '⚠️ 失败/跳过'}`);
  console.log(`  [2/3] API Key 获取与保存     — ${apiKeyResult ? '✅ 完成' : '⚠️ 失败/跳过'}`);
  console.log(`  [3/3] aidr-xclaw-security-sentinel 插件   — ${pluginResult ? '✅ 完成' : '⚠️ 失败/跳过'}`);
  console.log('');
  console.log('提示：AGENTS.md 变更需要开启新会话（/new）才能生效。');
  console.log('');
}

// ── Main ─────────────────────────────────────────────────────────────────────

async function main() {
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('  AIDR-XClaw-Security-Sentinel 初始化程序');
  console.log('═══════════════════════════════════════════════════════════════');
  console.log('');

  if (isAlreadyInitialized()) {
    console.log('[INFO] 已完成初始化，跳过。');
    console.log('[INFO] 如需重新初始化，请先删除:');
    console.log(`       ${initStateFile}`);
    console.log('');
    return;
  }

  // Stage 1: AGENTS.md 注入
  const injectOk = await stage1_injectQuickref();

  // Stage 2: API Key 获取
  const apiKeyOk = await stage2_getApiKey();

  // Stage 3: 插件安装
  const pluginOk = await stage3_installPlugin();

  // 标记完成
  markInitialized(apiKeyOk, pluginOk);

  // DONE
  printDONE(injectOk, apiKeyOk, pluginOk);
}

main().catch((err) => {
  console.error('初始化过程出错:', err.message);
  process.exit(1);
});
