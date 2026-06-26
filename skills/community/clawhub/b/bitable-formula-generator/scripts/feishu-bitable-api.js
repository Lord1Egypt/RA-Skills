/**
 * 飞书多维表格 API 工具脚本
 *
 * 功能：
 *   1. 获取 tenant_access_token（通过环境变量 FEISHU_APP_ID / FEISHU_APP_SECRET）
 *   2. 列出多维表格中所有表（tables）
 *   3. 列出指定表的所有字段（fields）
 *   4. 查看指定字段的完整 property
 *   5. 创建/更新公式字段
 *
 * 用法：
 *   node feishu-bitable-api.js <command> [args...]
 *
 * 命令：
 *   list-tables  <app_token>                                        列出所有表
 *   list-fields  <app_token> <table_name>                          列出指定表的所有字段（公式字段显示当前公式预览）
 *   get-field    <app_token> <table_name> <field_name>             查看指定字段的完整 property（含公式内容）
 *   set-formula  <app_token> <table_name> <field_name> <formula> [formatter]
 *                                                                   设置/更新公式字段
 *
 * 环境变量：
 *   FEISHU_APP_ID       飞书应用 App ID
 *   FEISHU_APP_SECRET   飞书应用 App Secret
 *
 * 示例：
 *   node feishu-bitable-api.js list-tables <your_app_token>
 *   node feishu-bitable-api.js list-fields <your_app_token> 客户档案表
 *   node feishu-bitable-api.js get-field   <your_app_token> 客户档案表 学习投入分数
 *   node feishu-bitable-api.js set-formula <your_app_token> 客户档案表 热爱得分 "(时间投入+想做什么)/15*100"
 *   node feishu-bitable-api.js set-formula <your_app_token> 客户档案表 热爱得分 "(A+B)/C*100" "0.00"
 *
 * ⚠️  公式含 <、>、|、& 等特殊字符时，PowerShell 会截断参数，请改用 .js 脚本文件传入公式。
 */

const https = require('https');

// ==================== 帮助文档 ====================

const USAGE = `
飞书多维表格 API 工具

用法：
  node feishu-bitable-api.js <command> [args...]

命令：
  list-tables  <app_token>
      列出所有表

  list-fields  <app_token> <table_name>
      列出指定表的所有字段（公式字段显示当前公式预览）

  get-field    <app_token> <table_name> <field_name>
      查看指定字段的完整 property（含公式内容 / 选项列表）

  set-formula  <app_token> <table_name> <field_name> <formula> [formatter]
      设置/更新公式字段，formatter 默认 "0.0"

环境变量：
  FEISHU_APP_ID       飞书应用 App ID
  FEISHU_APP_SECRET   飞书应用 App Secret

注意事项：
  ⚠️ 公式含 <、>、|、& 等字符时，PowerShell 会截断参数，
     请改用 .js 脚本文件传入公式（见 SKILL.md 方法 C）。
`.trim();

// 参数数量要求（不含命令本身）
const REQUIRED_ARGS = {
  'list-tables': 1,
  'list-fields': 2,
  'get-field':   3,
  'set-formula': 4,
};

// ==================== 通用 HTTP 请求 ====================

/**
 * 发送 HTTPS 请求到飞书开放平台。
 * @param {string} method  HTTP 方法（GET / POST / PUT）
 * @param {string} path    API 路径
 * @param {object} [body]  请求体（可选）
 * @param {string} [token] Bearer token；若不传则不添加 Authorization 头（用于获取 token 本身）
 */
function request(method, path, body, token) {
  return new Promise((resolve, reject) => {
    const payload = body ? JSON.stringify(body) : null;
    const headers = { 'Content-Type': 'application/json' };

    // 只在 token 明确传入时才加 Authorization 头，避免携带 undefined
    if (token) {
      headers['Authorization'] = 'Bearer ' + token;
    }
    if (payload) {
      headers['Content-Length'] = Buffer.byteLength(payload, 'utf8');
    }

    const options = {
      hostname: 'open.feishu.cn',
      path,
      method,
      headers,
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.code === 0) {
            resolve(result);
          } else {
            reject(new Error(`API Error [${result.code}]: ${result.msg}`));
          }
        } catch (e) {
          reject(new Error('Invalid JSON response: ' + data));
        }
      });
    });

    req.on('error', reject);
    if (payload) req.write(payload, 'utf8');
    req.end();
  });
}

// ==================== 获取 Access Token ====================

/**
 * 从飞书获取 tenant_access_token 并存入 global.accessToken。
 * 同时记录过期时间，供后续自动刷新使用。
 */
async function getAccessToken() {
  const appId = process.env.FEISHU_APP_ID;
  const appSecret = process.env.FEISHU_APP_SECRET;

  if (!appId || !appSecret) {
    console.error('❌ 请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET');
    process.exit(1);
  }

  // 注意：获取 token 的接口不需要 Bearer 认证，不传 token 参数
  const result = await request('POST', '/open-apis/auth/v3/tenant_access_token/internal', {
    app_id: appId,
    app_secret: appSecret,
  });

  global.accessToken = result.tenant_access_token;
  // 记录过期时间（提前 60 秒刷新）
  global.tokenExpireAt = Date.now() + (result.expire - 60) * 1000;
  console.log(`✅ Access Token 获取成功 (有效期 ${result.expire}s)\n`);
}

/**
 * 确保 token 有效，过期则自动刷新。
 */
async function ensureToken() {
  if (!global.accessToken || Date.now() >= (global.tokenExpireAt || 0)) {
    await getAccessToken();
  }
}

/**
 * 带 token 的 API 请求（自动刷新 token）。
 */
async function apiRequest(method, path, body) {
  await ensureToken();
  return request(method, path, body, global.accessToken);
}

// ==================== 分页请求封装 ====================

/**
 * 自动翻页，返回所有 items。
 * @param {string} basePath  API 路径（不含 page_token 参数）
 */
async function fetchAllPages(basePath) {
  let items = [];
  let pageToken = null;

  do {
    const path = pageToken
      ? `${basePath}${basePath.includes('?') ? '&' : '?'}page_token=${encodeURIComponent(pageToken)}`
      : basePath;

    const res = await apiRequest('GET', path);
    const data = res.data || {};
    items = items.concat(data.items || []);
    pageToken = data.has_more ? data.page_token : null;
  } while (pageToken);

  return items;
}

// ==================== 公共辅助：查找 table_id ====================

/**
 * 根据表名找到对应的 table 对象，找不到时打印可用表并退出。
 */
async function resolveTable(appToken, tableName) {
  const tables = await fetchAllPages(`/open-apis/bitable/v1/apps/${appToken}/tables`);
  const table = tables.find(t => t.name === tableName);

  if (!table) {
    console.error(`❌ 未找到表「${tableName}」`);
    console.log('可用的表：');
    tables.forEach((t, i) => console.log(`  ${i + 1}. ${t.name}`));
    process.exit(1);
  }

  return table;
}

// ==================== 列出所有表 ====================

async function listTables(appToken) {
  console.log(`📋 获取多维表格 [${appToken}] 的所有表...\n`);
  const tables = await fetchAllPages(`/open-apis/bitable/v1/apps/${appToken}/tables`);

  console.log('序号\tTable ID\t\t\t表名');
  console.log('─'.repeat(60));
  tables.forEach((t, i) => {
    console.log(`${i + 1}\t${t.table_id}\t${t.name}`);
  });
  console.log(`\n共 ${tables.length} 个表`);
  return tables;
}

// ==================== 列出指定表的所有字段 ====================

async function listFields(appToken, tableName) {
  const table = await resolveTable(appToken, tableName);
  console.log(`📋 获取表「${tableName}」(${table.table_id}) 的所有字段...\n`);

  const fields = await fetchAllPages(
    `/open-apis/bitable/v1/apps/${appToken}/tables/${table.table_id}/fields`
  );

  console.log('字段名\t\t\t\tField ID\t\t类型\t\t公式预览');
  console.log('─'.repeat(100));
  fields.forEach(f => {
    // type 20 = 公式字段
    let formulaHint = '';
    if (f.type === 20 && f.property && f.property.formula_expression) {
      const expr = f.property.formula_expression;
      if (expr === '0' || expr.trim() === '0') {
        formulaHint = '⚠️  0（未设置公式！）';
      } else {
        formulaHint = expr.length > 60 ? expr.slice(0, 60) + '…' : expr;
      }
    }
    const typeName = f.ui_type || (f.type === 20 ? 'Formula' : String(f.type));
    console.log(`${f.field_name.padEnd(20)}\t${f.field_id}\t${typeName.padEnd(12)}\t${formulaHint}`);
  });
  console.log(`\n共 ${fields.length} 个字段`);
  return fields;
}

// ==================== 查看指定字段的完整 property ====================

async function getField(appToken, tableName, fieldName) {
  const table = await resolveTable(appToken, tableName);

  const fields = await fetchAllPages(
    `/open-apis/bitable/v1/apps/${appToken}/tables/${table.table_id}/fields`
  );
  const field = fields.find(f => f.field_name === fieldName);

  if (!field) {
    console.error(`❌ 未找到字段「${fieldName}」`);
    console.log('可用的字段：');
    fields.forEach((f, i) => console.log(`  ${i + 1}. ${f.field_name}`));
    process.exit(1);
  }

  console.log(`📋 字段「${fieldName}」详情：\n`);
  console.log(`  字段 ID   : ${field.field_id}`);
  console.log(`  类型      : ${field.type}（${field.ui_type || ''}）`);

  if (field.type === 20) {
    const expr = field.property && field.property.formula_expression;
    const fmt  = field.property && field.property.formatter;
    console.log(`  格式      : ${fmt || '（无）'}`);
    if (!expr || expr === '0' || expr.trim() === '0') {
      console.log(`  公式      : ⚠️  "${expr}"（未设置有效公式！）`);
    } else {
      console.log(`  公式      :\n${expr}`);
    }
  } else if (field.property && field.property.options) {
    console.log(`\n  选项列表（共 ${field.property.options.length} 个）：`);
    field.property.options.forEach((o, i) => {
      console.log(`    ${i + 1}. [${o.id}] ${o.name}`);
    });
  } else {
    console.log(`\n  property  :\n${JSON.stringify(field.property, null, 2)}`);
  }

  return field;
}

// ==================== 设置/更新公式字段 ====================

async function setFormula(appToken, tableName, fieldName, formula, formatter) {
  const table = await resolveTable(appToken, tableName);

  // 检查字段是否已存在
  const fields = await fetchAllPages(
    `/open-apis/bitable/v1/apps/${appToken}/tables/${table.table_id}/fields`
  );
  const existingField = fields.find(f => f.field_name === fieldName);

  // 根据是否提供 formatter 决定 property 结构：
  //   - 有 formatter（数字格式）：添加 type 和格式信息
  //   - 无 formatter（文本/自动）：只写 formula_expression，避免类型冲突
  const hasFormatter = formatter && formatter.trim() !== '';
  const property = hasFormatter
    ? {
        formatter: formatter,
        formula_expression: formula,
        type: {
          data_type: 2,
          ui_property: { formatter: formatter },
          ui_type: 'Number',
        },
      }
    : {
        formula_expression: formula,
      };

  const body = {
    field_name: fieldName,
    type: 20, // 20 = 公式类型
    property,
  };

  let method, path, action;

  if (existingField) {
    method = 'PUT';
    path = `/open-apis/bitable/v1/apps/${appToken}/tables/${table.table_id}/fields/${existingField.field_id}`;
    action = '更新';
  } else {
    method = 'POST';
    path = `/open-apis/bitable/v1/apps/${appToken}/tables/${table.table_id}/fields`;
    action = '创建';
  }

  console.log(`${action}公式字段「${fieldName}」...`);
  console.log(`表: ${tableName} (${table.table_id})`);
  console.log(`公式: ${formula}`);
  console.log(`格式: ${hasFormatter ? formatter : '（自动）'}\n`);

  const result = await apiRequest(method, path, body);
  console.log(`✅ ${action}成功！`);
  console.log(`   字段 ID: ${result.data.field.field_id}`);
  console.log(`   字段名: ${result.data.field.field_name}`);
  console.log(`   公式: ${result.data.field.property.formula_expression}`);

  return result.data.field;
}

// ==================== 主入口 ====================

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  // 帮助
  if (!command || command === 'help' || command === '--help' || command === '-h') {
    console.log(USAGE);
    process.exit(0);
  }

  // 参数数量校验
  const minArgs = REQUIRED_ARGS[command];
  if (minArgs === undefined) {
    console.error(`❌ 未知命令: ${command}`);
    console.log('可用命令: list-tables, list-fields, get-field, set-formula, help');
    process.exit(1);
  }
  if (args.length - 1 < minArgs) {
    console.error(`❌ 命令 "${command}" 需要 ${minArgs} 个参数，实际提供了 ${args.length - 1} 个`);
    console.log(`\n运行 "node feishu-bitable-api.js help" 查看用法`);
    process.exit(1);
  }

  // 获取 token（仅一次，后续通过 ensureToken 自动刷新）
  await getAccessToken();

  try {
    switch (command) {
      case 'list-tables':
        await listTables(args[1]);
        break;

      case 'list-fields':
        await listFields(args[1], args[2]);
        break;

      case 'get-field':
        await getField(args[1], args[2], args[3]);
        break;

      case 'set-formula':
        // args[5] 为可选的 formatter，不传则默认 undefined（由 setFormula 判断）
        await setFormula(args[1], args[2], args[3], args[4], args[5]);
        break;
    }
  } catch (err) {
    console.error(`❌ ${err.message}`);
    process.exit(1);
  }
}

main();
