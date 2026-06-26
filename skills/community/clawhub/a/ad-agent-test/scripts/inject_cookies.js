/**
 * Cookie注入脚本 - 投放Agent测试
 * 
 * 使用方法：
 *   1. 用户提供cookie字符串（从浏览器document.cookie获取）
 *   2. 修改下方 RAW_COOKIE 变量
 *   3. node scripts/inject_cookies.js
 * 
 * 输出：cookies.json（供后续测试脚本使用）
 */

const fs = require('fs');

// ====== 用户提供的Cookie字符串粘贴在这里 ======
const RAW_COOKIE = process.env.RAW_COOKIE || '';

/**
 * 解析cookie字符串为Playwright兼容格式
 * @param {string} cookieStr - document.cookie输出的原始字符串
 * @param {string} defaultDomain - 默认域名
 * @returns {Array} Playwright cookie数组
 */
function parseCookies(cookieStr, defaultDomain = '.ad.qq.com') {
  if (!cookieStr) {
    console.error('ERROR: Cookie字符串为空，请设置 RAW_COOKIE 环境变量或修改脚本');
    process.exit(1);
  }

  const cookies = [];
  const pairs = cookieStr.split(';').map(s => s.trim()).filter(Boolean);

  for (const pair of pairs) {
    const eqIdx = pair.indexOf('=');
    if (eqIdx === -1) continue;
    
    const name = pair.substring(0, eqIdx).trim();
    const value = pair.substring(eqIdx + 1).trim();
    
    if (!name) continue;

    // 根据cookie名推断域名
    let domain = defaultDomain;
    if (['ptcz', 'ptui_loginuin', 'RK', 'p_uin', 'p_skey', 'pt4_token'].includes(name)) {
      domain = '.qq.com';
    } else if (['RIO_TOKEN', 'RIO_TOKEN_HTTPS', 'x_host_key_access_https', 'x-client-ssid', 'DiggerTraceId', 'DiggerTraceIdTs'].includes(name)) {
      domain = '.woa.com';
    }

    const cookie = {
      name,
      value,
      domain,
      path: '/',
    };

    // 敏感cookie加安全属性
    if (['gdt_mlogin', 'gdt_protect', 'tap_free_login_token', 'RIO_TOKEN', 'RIO_TOKEN_HTTPS', 'x_host_key_access_https'].includes(name)) {
      cookie.secure = true;
      cookie.httpOnly = true;
      cookie.sameSite = 'None';
    }

    cookies.push(cookie);
  }

  return cookies;
}

/**
 * 验证Cookie是否包含必需字段
 */
function validateCookies(cookies) {
  const required = ['gdt_mlogin', 'gdt_owner'];
  const names = cookies.map(c => c.name);
  const missing = required.filter(r => !names.includes(r));
  
  if (missing.length > 0) {
    console.warn(`⚠️  缺少关键Cookie: ${missing.join(', ')}`);
    console.warn('   可能导致登录失败，但仍尝试继续');
  }

  const recommended = ['tap_free_login_token', 'tap_free_login_userid', 'RIO_TOKEN'];
  const missingRec = recommended.filter(r => !names.includes(r));
  if (missingRec.length > 0) {
    console.warn(`ℹ️  缺少推荐Cookie: ${missingRec.join(', ')}`);
  }

  return missing.length === 0;
}

// 主逻辑
const cookies = parseCookies(RAW_COOKIE);
console.log(`✅ 解析到 ${cookies.length} 个Cookie`);
validateCookies(cookies);

// 输出JSON文件
const outPath = process.argv[2] || './cookies.json';
fs.writeFileSync(outPath, JSON.stringify(cookies, null, 2));
console.log(`✅ Cookie已保存到 ${outPath}`);

// 摘要
const domains = {};
cookies.forEach(c => { domains[c.domain] = (domains[c.domain] || 0) + 1; });
console.log('   域名分布:', domains);

module.exports = { parseCookies, validateCookies };
