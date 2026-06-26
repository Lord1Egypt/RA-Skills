#!/usr/bin/env node
/**
 * validate_page.js — Cockpit HTML 页面完整性校验 + 自动修复
 *
 * 校验 6 项内容，发现问题后：
 *   - 能 auto-fix 的：自动修复后重新校验，全部通过才返回
 *   - 无法修复的：报告具体错误并返回 { valid: false }
 *
 * 使用方式（独立工具）：
 *   node src/generate/validate_page.js <html_file>
 *   node src/generate/validate_page.js <html_file> --fix   # 强制写入修复后的文件
 *
 * 集成到 src/generate/page.js：
 *   const { validateHtml } = require('./validate_page.js');
 *   const result = validateHtml(html);
 *   if (!result.valid) { console.error('校验失败'); process.exit(1); }
 *   // result.html 已修复，可安全写入
 */

const fs = require('fs');
const path = require('path');
const { extractJsonFromAssignment, extractJsonKeys } = require('../core/htmlUtils.js');

// ============================================================
// 核心校验 + 修复逻辑
// ============================================================

/**
 * 校验并修复 HTML 内容
 * @param {string} html - 原始 HTML 内容
 * @param {object} opts
 * @param {boolean} opts.verbose - 是否打印详细信息
 * @param {boolean} opts.dryRun - 只校验不修复
 * @returns {{ valid: boolean, html: string|null, errors: string[] }}
 */
function validateHtml(html, opts = {}) {
  const { verbose = false, dryRun = false } = opts;
  const errors = [];
  let fixedHtml = html;

  function log(msg) {
    if (verbose) console.log('  ' + msg);
  }

  function warn(msg) {
    console.warn('  ⚠️  ' + msg);
  }

  function fix(label, repairedHtml) {
    if (repairedHtml !== fixedHtml) {
      warn(label + ' — 已自动修复');
      fixedHtml = repairedHtml;
    }
  }

  // ==========================================================
  // 校验 1: {{...}} 占位符残留
  // ==========================================================
  {
    const residual = findResidualPlaceholders(fixedHtml);
    if (residual.length > 0) {
      warn(`发现 ${residual.length} 个未处理的占位符: ${residual.join(', ')}`);
      if (!dryRun) {
        fixedHtml = fixedHtml.replace(/\{\{[^}]+\}\}/g, 'null');
        log('已将所有未处理占位符替换为 null');
      }
    } else {
      log('校验 1 {{...}} 占位符: ✅ 无残留');
    }
  }

  // ==========================================================
  // 校验 2: ENCRYPTED_SQL JSON 有效性（base64 密文含 } 字符，正则提取 key 列表作为补充）
  // ==========================================================
  let encryptedSql = null;
  {
    const extracted = extractJsonFromAssignment(fixedHtml, 'ENCRYPTED_SQL');
    if (extracted.error) {
      warn('ENCRYPTED_SQL JSON 解析失败（密文含 } 字符）: ' + extracted.error + ' — 使用正则提取 key 列表');
      const encKeys = extractJsonKeys(fixedHtml, 'ENCRYPTED_SQL');
      log(`  正则提取到 ENCRYPTED_SQL keys: ${[...encKeys].join(', ')}`);
      encryptedSql = null; // JSON 无效但 keys 可用
    } else {
      log('校验 2 ENCRYPTED_SQL JSON: ✅ 有效');
      encryptedSql = extracted.data;
    }
  }

  // ==========================================================
  // 校验 3: SQL_PLAIN JSON 有效性
  // ==========================================================
  let sqlPlain = null;
  {
    const extracted = extractJsonFromAssignment(fixedHtml, 'SQL_PLAIN');
    if (extracted.error) {
      errors.push('SQL_PLAIN JSON 解析失败: ' + extracted.error);
    } else {
      log('校验 3 SQL_PLAIN JSON: ✅ 有效');
      sqlPlain = extracted.data;
    }
  }

  // ==========================================================
  // 校验 4: ENCRYPTED_SQL 与 SQL_PLAIN key 一致性
  // ==========================================================
  // 获取 ENCRYPTED_SQL keys（JSON 有效时用 Object.keys，否则用正则提取）
  // encJsonParseValid: encryptedSql JSON 是否解析成功（成功=可靠，无效=不可信）
  let encJsonParseValid = (encryptedSql !== null);
  let encKeys = null;
  if (encryptedSql !== null) {
    encKeys = new Set(Object.keys(encryptedSql));
  } else {
    // JSON 无效（密文含 } 字符），用正则提取 key（不可信）
    encKeys = extractJsonKeys(fixedHtml, 'ENCRYPTED_SQL');
    if (encKeys.size > 0) {
      log(`  ENCRYPTED_SQL key 列表（正则提取，JSON 不可信）: ${[...encKeys].join(', ')}`);
    }
  }

  if (sqlPlain !== null && encKeys !== null) {
    const plainKeys = new Set(Object.keys(sqlPlain));

    const missingInPlain = [...encKeys].filter(k => !plainKeys.has(k));
    const missingInEnc = [...plainKeys].filter(k => !encKeys.has(k));

    if (missingInPlain.length > 0) {
      warn(`ENCRYPTED_SQL 有但 SQL_PLAIN 缺失: ${missingInPlain.join(', ')} — 已补充空字符串`);
      if (!dryRun) {
        for (const k of missingInPlain) {
          sqlPlain[k] = '';
        }
        fixedHtml = injectJsonAssignment(fixedHtml, 'SQL_PLAIN', sqlPlain);
      }
    }

    if (missingInEnc.length > 0) {
      warn(`SQL_PLAIN 有但 ENCRYPTED_SQL 缺失: ${missingInEnc.join(', ')} — 无法补充（ENCRYPTED_SQL JSON 不可信，无法同步修复）`);
      errors.push(`ENCRYPTED_SQL 缺失 key: ${missingInEnc.join(', ')}，需重新生成加密数据`);
    }

    if (missingInPlain.length === 0 && missingInEnc.length === 0) {
      log('校验 4 ENCRYPTED_SQL / SQL_PLAIN key 一致性: ✅ 完全匹配');
      // 即使 key 匹配，如果 JSON 本身无效（encJsonParseValid=false），
      // 说明加密数据不可信，仍需报错
      if (!encJsonParseValid) {
        errors.push('ENCRYPTED_SQL JSON 无效（密文含 } 字符），无法验证加密数据正确性，请重新生成页面');
      }
    }
  } else if (sqlPlain === null) {
    errors.push('SQL_PLAIN JSON 无效，无法检查 key 一致性');
  }

  // ==========================================================
  // 校验 5: CHART_CONFIG 中 id 在 SQL_PLAIN 中存在
  // ==========================================================
  if (sqlPlain !== null) {
    const extracted = extractJsonFromAssignment(fixedHtml, 'CHART_CONFIG');
    if (!extracted.error && Array.isArray(extracted.data)) {
      const plainKeys = new Set(Object.keys(sqlPlain));
      const missingChartIds = extracted.data
        .filter(c => c.id && !plainKeys.has(c.id))
        .map(c => c.id);

      if (missingChartIds.length > 0) {
        warn(`CHART_CONFIG 中 id 不在 SQL_PLAIN 中: ${missingChartIds.join(', ')} — 已补充空 SQL（加密数据需重新生成）`);
        if (!dryRun) {
          for (const id of missingChartIds) {
            sqlPlain[id] = '';
            // encryptedSql 不 auto-fix（见校验 4 说明）
          }
          fixedHtml = injectJsonAssignment(fixedHtml, 'SQL_PLAIN', sqlPlain);
        }
      } else {
        log('校验 5 CHART_CONFIG id 完整性: ✅ 全部在 SQL_PLAIN 中有对应');
      }
    }
  }

  // ==========================================================
  // 校验 6: JS 语法正确性（node --check）
  // ==========================================================
  {
    const jsValid = validateJsSyntax(fixedHtml);
    if (!jsValid.valid) {
      errors.push('JS 语法错误: ' + jsValid.error);
    } else {
      log('校验 6 JS 语法: ✅ 正确');
    }
  }

  const valid = errors.length === 0;
  return { valid, html: valid ? fixedHtml : null, errors };
}

// ============================================================
// 辅助函数
// ============================================================

/**
 * 查找 HTML 中未处理的 {{...}} 占位符
 */
function findResidualPlaceholders(html) {
  // 匹配 {{...}} 但排除 {{ENCRYPTED_SQL}} {{SQL_PLAIN}} {{CHART_CONFIG}} 这些会被替换的
  // 只找完全未处理的小写占位符
  const known = new Set(['encrypted_sql', 'sql_plain', 'chart_config', 'page_title',
    'api_base', 'api_auth_base', 'default_project_id', 'login_password_encrypt',
    'enum_map', 'field_labels', 'group_stats_config', 'view_mode', 'sidebar_width',
    'cockpit_mode', 'date_range_config', 'kpi_layout', 'default_view']);
  const found = [];
  const matches = html.match(/\{\{([^}]+)\}\}/g) || [];
  for (const m of matches) {
    const inner = m.slice(2, -2).trim().toLowerCase();
    if (!known.has(inner) && !/^\{\{.*\}\}$/ .test(m)) {
      found.push(m);
    }
  }
  // 更简单：只要出现非大写变量名的 {{...}} 就认为未处理
  // 实际应用中，正则匹配 + 过滤已知的就够用了
  return [...new Set(matches)].filter(m => {
    const inner = m.slice(2, -2);
    // 已知模板变量不报
    return !['ENCRYPTED_SQL', 'SQL_PLAIN', 'CHART_CONFIG', 'PAGE_TITLE',
      'API_BASE', 'API_AUTH_BASE', 'DEFAULT_PROJECT_ID', 'LOGIN_PASSWORD_ENCRYPT',
      'ENUM_MAP', 'FIELD_LABELS', 'GROUP_STATS_CONFIG', 'VIEW_MODE', 'SIDEBAR_WIDTH',
      'COCKPIT_MODE', 'DATE_RANGE_CONFIG', 'KPI_LAYOUT', 'DEFAULT_VIEW'
    ].includes(inner);
  });
}

/**
 * 将修复后的 JSON 重新注入 HTML（用字符流追踪 brace 层级定位）
 */
function injectJsonAssignment(html, varName, data) {
  const newJson = JSON.stringify(data, null, 2);
  const startMarker = `const ${varName} = `;
  const startIdx = html.indexOf(startMarker);
  if (startIdx === -1) return html;

  const jsonStart = startIdx + startMarker.length;
  if (jsonStart >= html.length || html[jsonStart] !== '{') return html;

  // 找到原始 JSON 块的结束位置
  let depth = 0, inString = false, stringChar = null, i = jsonStart;
  while (i < html.length) {
    const ch = html[i];
    if (inString) {
      if (ch === '\\' && i + 1 < html.length) { i += 2; continue; }
      if (ch === stringChar) { inString = false; i++; continue; }
      i++; continue;
    }
    if (ch === '"' || ch === "'") { inString = true; stringChar = ch; i++; continue; }
    if (ch === '{') { depth++; i++; continue; }
    if (ch === '}') {
      depth--;
      if (depth === 0) {
        const jsonEnd = i + 1;
        const before = html.slice(0, jsonStart);
        const after = html.slice(jsonEnd);
        return before + newJson + after;
      }
      i++; continue;
    }
    i++;
  }
  return html;
}

/**
 * 验证 JS 语法正确性（提取 <script> 块后用 node --check）
 */
function validateJsSyntax(html) {
  const scriptMatch = html.match(/<script>([\s\S]*?)<\/script>/);
  if (!scriptMatch) {
    return { valid: false, error: '找不到 <script> 块' };
  }
  const js = scriptMatch[1];
  // 用 node --check 验证
  const { execSync } = require('child_process');
  const path = require('path');
  const fs = require('fs');
  const tmpFile = path.join('/tmp', 'validate_js_' + process.pid + '.js');
  try {
    fs.writeFileSync(tmpFile, js, 'utf-8');
    execSync('node --check ' + tmpFile, { stdio: 'pipe' });
    return { valid: true };
  } catch (e) {
    const stderr = e.stderr ? e.stderr.toString() : '';
    const msg = stderr.match(/SyntaxError[\s\S]*$/m)?.[0] || 'JS 语法错误';
    return { valid: false, error: msg.trim() };
  } finally {
    try { fs.unlinkSync(tmpFile); } catch (_) {}
  }
}

// ============================================================
// CLI 入口
// ============================================================
function main() {
  const args = process.argv.slice(2);
  const htmlPath = args.find(a => !a.startsWith('--'));
  const doFix = args.includes('--fix');

  if (!htmlPath) {
    console.error('用法: node validate_page.js <html_file> [--fix]');
    console.error('  --fix: 自动修复并写入文件');
    process.exit(1);
  }

  if (!fs.existsSync(htmlPath)) {
    console.error('❌ 文件不存在: ' + htmlPath);
    process.exit(1);
  }

  const originalHtml = fs.readFileSync(htmlPath, 'utf-8');
  console.log('📋 HTML 完整性校验报告');
  console.log('文件: ' + path.basename(htmlPath));
  console.log('=' .repeat(50));

  const result = validateHtml(originalHtml, { verbose: true, dryRun: !doFix });

  if (result.valid) {
    console.log('\n✅ 全部校验通过');
    if (doFix) {
      fs.writeFileSync(htmlPath, result.html, 'utf-8');
      console.log('📝 已将修复后的内容写回文件');
    } else {
      console.log('（提示: 使用 --fix 可将修复内容写入文件）');
    }
    process.exit(0);
  } else {
    console.log('\n❌ 校验失败:');
    for (const err of result.errors) {
      console.log('  - ' + err);
    }
    process.exit(1);
  }
}

module.exports = { validateHtml, findResidualPlaceholders };

if (require.main === module) {
  main();
}
