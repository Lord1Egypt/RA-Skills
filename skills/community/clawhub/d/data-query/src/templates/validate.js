#!/usr/bin/env node
/**
 * src/templates/validate.js — 模板质量验证
 *
 * 职责：确保模板包含所有 Token 管理所需的 JS 逻辑和占位符。
 * 在任何模板被加载/生成之前，必须通过本验证。
 *
 * 用法：
 *   node src/templates/validate.js
 *   node src/templates/validate.js --verbose
 *
 * 集成到生成流程：
 *   const { validateTemplates, validateTemplateContent } = require('./templates/validate.js');
 *   const errors = validateTemplates();
 *   if (errors.length > 0) throw new Error('模板验证失败: ' + errors.join('; '));
 *
 * 校验 regenerate 新模板（ cockpit 或 single-chart）：
 *   const errors = validateTemplateContent(html, { type: 'cockpit' });
 *   if (errors.length > 0) throw new Error('...');
 */

const fs = require('fs');
const path = require('path');

const TEMPLATES_DIR = path.join(__dirname, '../../templates');

// ============================================================
// 规则定义
// ============================================================

// ── 所有模板通用（cockpit + single-chart）─────────────────────
const COMMON_RULES = [
  {
    id: 'sessionStorage_setItem',
    pattern: /sessionStorage\.setItem\s*\(\s*['"]token['"]\s*,/,
    desc: 'doLogin() 必须写入 sessionStorage.setItem("token", ...) 实现持久化',
    templates: ['cockpit_template.html', 'html_page_template.html']
  },
  {
    id: 'sessionStorage_getItem',
    pattern: /sessionStorage\.getItem\s*\(\s*(['"]token['"]|TOKEN_KEY)\s*\)/,
    desc: 'getToken() 必须读取 sessionStorage.getItem("token") 复用 ACM token',
    templates: ['cockpit_template.html', 'html_page_template.html']
  },
  {
    id: 'login_modal_dom',
    pattern: /id\s*=\s*["']loginModal["']/,
    desc: '必须包含 id="loginModal" 登录弹窗 DOM',
    templates: ['cockpit_template.html', 'html_page_template.html']
  },
  {
    id: 'crypto_js_cdn',
    pattern: /crypto-js[@/][\d.]+/,
    desc: '必须引入 CryptoJS CDN（用于 AES 密码加密）',
    templates: ['cockpit_template.html', 'html_page_template.html']
  },
  {
    id: 'no_hardcoded_password_in_dologin',
    pattern: /password:\s*['"][^'"]{1,80}['"]\s*[,\}]/,
    anti: true,
    desc: '禁止在 doLogin 的 body 中硬编码 password 字符串字面量',
    templates: ['cockpit_template.html', 'html_page_template.html']
  },
  {
    id: 'getToken_concurrent_guard',
    pattern: /if\s*\(\s*tokenPromise\s*\)\s*return\s+tokenPromise/,
    desc: 'getToken() 必须有并发保护（if (tokenPromise) return tokenPromise）防止重复请求',
    templates: ['cockpit_template.html', 'html_page_template.html']
  },
  {
    id: 'login_fetch_uses_api_auth_base',
    pattern: /fetch\s*\(\s*`\$\{API_AUTH_BASE\}\/jwt\/token/,
    desc: '登录 fetch 必须使用 ${API_AUTH_BASE}/jwt/token，禁止字符串拼接 API_BASE',
    templates: ['cockpit_template.html', 'html_page_template.html']
  },
  {
    id: 'api_auth_base_declared',
    pattern: /const\s+API_AUTH_BASE\s*=\s*['"]\{\{API_AUTH_BASE\}\}['"]/,
    desc: '必须声明 const API_AUTH_BASE = "{{API_AUTH_BASE}}" 并在 fetch 中使用它',
    templates: ['cockpit_template.html', 'html_page_template.html']
  },
];

// ── 驾驶舱模板专用 ────────────────────────────────────────────
const COCKPIT_ONLY_RULES = [
  {
    id: 'cockpit_placeholder_encrypted_sql',
    pattern: /\{\{ENCRYPTED_SQL\}\}/,
    desc: '必须包含 {{ENCRYPTED_SQL}} 占位符（加密 SQL 注入点）',
    templates: ['cockpit_template.html']
  },
  {
    id: 'cockpit_placeholder_sql_plain',
    pattern: /\{\{SQL_PLAIN\}\}/,
    desc: '必须包含 {{SQL_PLAIN}} 占位符（明文 SQL，用于 buildParams 校验）',
    templates: ['cockpit_template.html']
  },
  {
    id: 'cockpit_placeholder_chart_config',
    pattern: /\{\{CHART_CONFIG\}\}/,
    desc: '必须包含 {{CHART_CONFIG}} 占位符（图表配置数组）',
    templates: ['cockpit_template.html']
  },
  {
    id: 'cockpit_placeholder_api_base',
    pattern: /\{\{API_BASE\}\}/,
    desc: '必须包含 {{API_BASE}} 占位符（API 基础路径）',
    templates: ['cockpit_template.html']
  },
];

// ── 单图表模板专用 ────────────────────────────────────────────
const SINGLE_CHART_ONLY_RULES = [
  {
    id: 'single_placeholder_encrypted_sql',
    pattern: /\{\{ENCRYPTED_SQL\}\}/,
    desc: '必须包含 {{ENCRYPTED_SQL}} 占位符（加密 SQL）',
    templates: ['html_page_template.html']
  },
  {
    id: 'single_placeholder_iv',
    pattern: /\{\{IV\}\}/,
    desc: '必须包含 {{IV}} 占位符（AES 加密 IV）',
    templates: ['html_page_template.html']
  },
  {
    id: 'single_placeholder_api_base',
    pattern: /\{\{API_BASE\}\}/,
    desc: '必须包含 {{API_BASE}} 占位符（API 基础路径）',
    templates: ['html_page_template.html']
  },
  {
    id: 'single_placeholder_charts_config',
    pattern: /\{\{CHARTS_CONFIG\}\}/,
    desc: '必须包含 {{CHARTS_CONFIG}} 占位符（图表配置）',
    templates: ['html_page_template.html']
  },
];

// 全部内置模板规则
const ALL_BUILTIN_RULES = [...COMMON_RULES, ...COCKPIT_ONLY_RULES, ...SINGLE_CHART_ONLY_RULES];

// ============================================================
// 新模板内容校验规则（regenerate 生成时校验）
// ============================================================

// cockpit 新模板：必须有 executeQuery / buildParams / loadAllData
const NEW_COCKPIT_RULES = [
  {
    id: 'nt_sessionStorage_setItem',
    pattern: /sessionStorage\.setItem\s*\(\s*['"]token['"]\s*,/,
    desc: '登录成功后必须写入 sessionStorage.setItem("token", ...)'
  },
  {
    id: 'nt_sessionStorage_getItem',
    pattern: /sessionStorage\.getItem\s*\(\s*(['"]token['"]|TOKEN_KEY)\s*\)/,
    desc: 'getToken() 必须读取 sessionStorage.getItem("token")'
  },
  {
    id: 'nt_api_auth_base_declared',
    pattern: /const\s+API_AUTH_BASE\s*=\s*['"]\{\{API_AUTH_BASE\}\}['"]/,
    desc: '必须声明 const API_AUTH_BASE = "{{API_AUTH_BASE}}"（占位符）'
  },
  {
    id: 'nt_dologin_function',
    pattern: /function\s+doLogin\s*\(/,
    desc: '必须定义 doLogin() 函数用于执行登录'
  },
  {
    id: 'nt_login_modal_dom',
    pattern: /id\s*=\s*["']loginModal["']/,
    desc: '必须包含 id="loginModal" 登录弹窗 DOM'
  },
  {
    id: 'nt_crypto_js_cdn',
    pattern: /crypto-js[@/][\d.]+/,
    desc: '必须引入 CryptoJS CDN（用于 AES 密码加密）'
  },
  {
    id: 'nt_login_fetch_uses_api_auth_base',
    pattern: /fetch\s*\(\s*`\$\{API_AUTH_BASE\}\/jwt\/token/,
    desc: '登录 fetch 必须使用 ${API_AUTH_BASE}/jwt/token'
  },
  {
    id: 'nt_getToken_concurrent_guard',
    pattern: /if\s*\(\s*tokenPromise\s*\)\s*return\s+tokenPromise/,
    desc: 'getToken() 必须有并发保护（if (tokenPromise) return tokenPromise）'
  },
  {
    id: 'nt_executeQuery_function',
    pattern: /function\s+executeQuery\s*\(/,
    desc: '必须定义 executeQuery() 函数用于调用后端 execute 接口'
  },
  {
    id: 'nt_buildParams_function',
    pattern: /function\s+buildParams\s*\(/,
    desc: '必须定义 buildParams() 函数用于组装查询参数'
  },
  {
    id: 'nt_loadAllData_function',
    pattern: /function\s+loadAllData\s*\(/,
    desc: '必须定义 loadAllData() 函数用于加载所有图表数据'
  },
  {
    id: 'nt_placeholder_encrypted_sql',
    pattern: /\{\{ENCRYPTED_SQL\}\}/,
    desc: '必须包含 {{ENCRYPTED_SQL}} 占位符'
  },
  {
    id: 'nt_placeholder_sql_plain',
    pattern: /\{\{SQL_PLAIN\}\}/,
    desc: '必须包含 {{SQL_PLAIN}} 占位符'
  },
  {
    id: 'nt_placeholder_chart_config',
    pattern: /\{\{CHART_CONFIG\}\}/,
    desc: '必须包含 {{CHART_CONFIG}} 占位符'
  },
  {
    id: 'nt_placeholder_api_base',
    pattern: /\{\{API_BASE\}\}/,
    desc: '必须包含 {{API_BASE}} 占位符'
  },
  {
    id: 'nt_placeholder_api_auth_base',
    pattern: /\{\{API_AUTH_BASE\}\}/,
    desc: '必须包含 {{API_AUTH_BASE}} 占位符'
  },
];

// single-chart 新模板：必须有 fetchData（不需要 executeQuery/buildParams/loadAllData）
const NEW_SINGLE_CHART_RULES = [
  {
    id: 'nt_sessionStorage_setItem',
    pattern: /sessionStorage\.setItem\s*\(\s*['"]token['"]\s*,/,
    desc: '登录成功后必须写入 sessionStorage.setItem("token", ...)'
  },
  {
    id: 'nt_sessionStorage_getItem',
    pattern: /sessionStorage\.getItem\s*\(\s*(['"]token['"]|TOKEN_KEY)\s*\)/,
    desc: 'getToken() 必须读取 sessionStorage.getItem("token")'
  },
  {
    id: 'nt_api_auth_base_declared',
    pattern: /const\s+API_AUTH_BASE\s*=\s*['"]\{\{API_AUTH_BASE\}\}['"]/,
    desc: '必须声明 const API_AUTH_BASE = "{{API_AUTH_BASE}}"'
  },
  {
    id: 'nt_login_modal_dom',
    pattern: /id\s*=\s*["']loginModal["']/,
    desc: '必须包含 id="loginModal" 登录弹窗 DOM'
  },
  {
    id: 'nt_crypto_js_cdn',
    pattern: /crypto-js[@/][\d.]+/,
    desc: '必须引入 CryptoJS CDN（用于 AES 密码加密）'
  },
  {
    id: 'nt_login_fetch_uses_api_auth_base',
    pattern: /fetch\s*\(\s*`\$\{API_AUTH_BASE\}\/jwt\/token/,
    desc: '登录 fetch 必须使用 ${API_AUTH_BASE}/jwt/token'
  },
  {
    id: 'nt_getToken_concurrent_guard',
    pattern: /if\s*\(\s*tokenPromise\s*\)\s*return\s+tokenPromise/,
    desc: 'getToken() 必须有并发保护'
  },
  {
    id: 'nt_dologin_function',
    pattern: /function\s+doLogin\s*\(/,
    desc: '必须定义 doLogin() 函数用于执行登录'
  },
  {
    id: 'nt_fetchData_function',
    pattern: /function\s+fetchData\s*\(/,
    desc: '必须定义 fetchData() 函数用于获取数据'
  },
  {
    id: 'nt_placeholder_encrypted_sql',
    pattern: /\{\{ENCRYPTED_SQL\}\}/,
    desc: '必须包含 {{ENCRYPTED_SQL}} 占位符'
  },
  {
    id: 'nt_placeholder_iv',
    pattern: /\{\{IV\}\}/,
    desc: '必须包含 {{IV}} 占位符'
  },
  {
    id: 'nt_placeholder_api_base',
    pattern: /\{\{API_BASE\}\}/,
    desc: '必须包含 {{API_BASE}} 占位符'
  },
  {
    id: 'nt_placeholder_api_auth_base',
    pattern: /\{\{API_AUTH_BASE\}\}/,
    desc: '必须包含 {{API_AUTH_BASE}} 占位符'
  },
  {
    id: 'nt_placeholder_charts_config',
    pattern: /\{\{CHARTS_CONFIG\}\}/,
    desc: '必须包含 {{CHARTS_CONFIG}} 占位符'
  },
];

// ============================================================
// 通用验证逻辑
// ============================================================

function applyRule(rule, content) {
  const found = rule.pattern.test(content);
  return rule.anti ? !found : found;
}

function printResults(title, results) {
  const passed = results.filter(r => r.ok).length;
  const failed = results.filter(r => !r.ok);
  console.log(`\n${'='.repeat(60)}`);
  console.log(title);
  console.log('='.repeat(60));
  for (const name of [...new Set(results.map(r => r.name))]) {
    const tplResults = results.filter(r => r.name === name);
    const tplPassed = tplResults.filter(r => r.ok).length;
    const tplFailed = tplResults.filter(r => !r.ok);
    const status = tplFailed.length === 0 ? '✅' : '❌';
    console.log(`\n${status} ${name}  — 通过 ${tplPassed}/${tplResults.length}`);
    if (tplFailed.length > 0) {
      tplFailed.forEach(r => console.log(`    ${r.error}`));
    }
  }
  console.log(`\n总计: 通过 ${passed}/${results.length}`);
  console.log('='.repeat(60));
  return failed.map(r => `[${r.name}] ${r.error}`);
}

// ============================================================
// 验证内置模板文件
// ============================================================

function validateTemplate(name, verbose = false) {
  const file = path.join(TEMPLATES_DIR, name);
  if (!fs.existsSync(file)) {
    return [{ id: 'FILE_NOT_FOUND', ok: false, name, error: `文件不存在: ${file}` }];
  }

  const content = fs.readFileSync(file, 'utf-8');
  const results = [];

  for (const rule of ALL_BUILTIN_RULES) {
    if (!rule.templates.includes(name)) continue;
    const ok = applyRule(rule, content);
    results.push({
      id: rule.id,
      ok,
      name,
      desc: rule.desc,
      error: ok ? null : `❌ 未通过: ${rule.desc}`
    });
  }

  return results;
}

// ============================================================
// 验证新生成的模板 HTML 字符串
//
// @param {string} htmlContent - HTML 字符串
// @param {{ type: 'cockpit' | 'single-chart', verbose?: boolean }} options
//   type='cockpit'      → 校验 cockpit 新模板规则（需要 executeQuery/buildParams/loadAllData）
//   type='single-chart' → 校验单图表新模板规则（只需要 fetchData）
// ============================================================

function validateTemplateContent(htmlContent, options = {}) {
  const { type = 'cockpit', verbose = false } = options;

  if (!htmlContent || typeof htmlContent !== 'string') {
    return [{ id: 'EMPTY_CONTENT', ok: false, name: '(新模板)', error: '模板内容为空' }];
  }

  const rules = type === 'cockpit' ? NEW_COCKPIT_RULES : NEW_SINGLE_CHART_RULES;
  const typeLabel = type === 'cockpit' ? '驾驶舱' : '单图表';

  const results = [];
  for (const rule of rules) {
    const ok = applyRule(rule, htmlContent);
    results.push({
      id: rule.id,
      ok,
      name: `(新模板-${typeLabel})`,
      desc: rule.desc,
      error: ok ? null : `❌ 未通过: ${rule.desc}`
    });
  }

  const passed = results.filter(r => r.ok).length;
  const failed = results.filter(r => !r.ok);

  if (verbose || failed.length > 0) {
    printResults(`新模板内容验证结果（${typeLabel}）`, results);
  }

  return failed.map(r => `[新模板-${typeLabel}] ${r.error}`);
}

// ============================================================
// 验证内置模板文件集合（CLI / 原有调用方式）
// ============================================================

function validateTemplates(templateNames = null, verbose = false) {
  const templates = templateNames || fs.readdirSync(TEMPLATES_DIR).filter(f => f.endsWith('.html'));
  const allResults = [];

  for (const name of templates) {
    const results = validateTemplate(name);
    allResults.push(...results);
  }

  const passed = allResults.filter(r => r.ok).length;
  const failed = allResults.filter(r => !r.ok);

  if (verbose || failed.length > 0) {
    printResults('模板验证结果', allResults);
  } else {
    console.log(`\n${'='.repeat(60)}`);
    console.log('模板验证结果');
    console.log('='.repeat(60));
    for (const name of templates) {
      const tplResults = allResults.filter(r => r.name === name);
      const tplPassed = tplResults.filter(r => r.ok).length;
      const status = tplPassed === tplResults.length ? '✅' : '❌';
      console.log(`  ${status} ${name}  — 通过 ${tplPassed}/${tplResults.length}`);
    }
    console.log(`\n总计: 通过 ${passed}/${allResults.length}`);
    console.log('='.repeat(60));
  }

  return failed.map(r => `[${r.name}] ${r.error}`);
}

// ============================================================
// CLI 入口
// ============================================================

if (require.main === module) {
  const args = process.argv.slice(2);
  const verbose = args.includes('--verbose') || args.includes('-v');
  const templates = args.filter(a => a.endsWith('.html') && !a.startsWith('--'));

  const failed = validateTemplates(templates.length > 0 ? templates : null, verbose);

  if (failed.length > 0) {
    console.error('\n❌ 模板验证未通过，请修复后再继续:');
    failed.forEach(e => console.error('  -', e));
    process.exit(1);
  } else {
    console.log('\n✅ 所有检查通过');
    process.exit(0);
  }
}

module.exports = { validateTemplates, validateTemplate, validateTemplateContent };
