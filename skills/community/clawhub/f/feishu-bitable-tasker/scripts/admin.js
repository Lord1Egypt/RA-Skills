#!/usr/bin/env node

/**
 * 飞书任务管理 - 管理工具
 *
 * 提供多维表格和知识库的管理功能：
 * - 添加字段到现有表格
 * - 列出表格字段
 * - 创建多维表格
 * - 创建数据表
 */

const fs = require('fs');
const path = require('path');
const { FeishuClient } = require('./feishu-client.js');

// ANSI 颜色
const colors = {
  reset: '\x1b[0m',
  green: '\x1b[32m',
  red: '\x1b[31m',
  yellow: '\x1b[33m',
  blue: '\x1b[34m'
};

function log(message, color = 'reset') {
  console.log(`${colors[color]}${message}${colors.reset}`);
}

/**
 * 从知识库中的多维表格链接提取完整信息
 * 只支持知识库中的多维表格链接格式：https://xxx.feishu.cn/wiki/<node_token>
 *
 * 返回: { nodeToken, appToken, spaceId, bitableName }
 */
async function extractBitableInfoFromWikiUrl(client, url) {
  // 检查是否为知识库链接
  const wikiMatch = url.match(/\/wiki\/([a-zA-Z0-9]+)/);
  if (!wikiMatch) {
    throw new Error(
      '链接格式不正确。\n' +
      '  • 必须是知识库中的多维表格链接（格式：https://xxx.feishu.cn/wiki/xxxxx）\n' +
      '  • 不支持独立的多维表格链接（/base/xxx 格式）\n' +
      '\n' +
      '请在知识库中创建多维表格，然后复制其知识库链接。'
    );
  }

  const nodeToken = wikiMatch[1];
  log('检测到知识库链接，查询多维表格节点信息...', 'blue');

  const response = await client.request('GET', '/open-apis/wiki/v2/spaces/get_node', null, {
    params: { token: nodeToken }
  });

  const node = response.data.node;
  if (node.obj_type !== 'bitable') {
    throw new Error(
      `该知识库节点不是多维表格（类型: ${node.obj_type}）。\n` +
      '请在知识库中创建多维表格，然后复制其知识库链接。'
    );
  }

  const result = {
    nodeToken: nodeToken,
    appToken: node.obj_token,
    spaceId: node.space_id,
    bitableName: node.title || ''
  };

  log(`✅ 多维表格信息提取成功`, 'green');
  log(`   节点 token: ${result.nodeToken}`, 'blue');
  log(`   App token: ${result.appToken}`, 'blue');
  log(`   Space ID: ${result.spaceId}`, 'blue');
  log(`   表格名称: ${result.bitableName}`, 'blue');

  return result;
}

/**
 * 确保任务文档根节点存在
 * 在多维表格节点下创建或查找 "{tableName}-任务文档" 文档节点
 *
 * @returns {string} 任务文档根节点的 node_token
 */
async function ensureTaskDocRoot(client, spaceId, bitableNodeToken, tableName) {
  const docName = `${tableName}-任务文档`;
  log(`\n检查任务文档根节点: "${docName}"`, 'blue');

  // 列出多维表格节点的子节点
  const nodesResponse = await client.getWikiNodes(spaceId, bitableNodeToken);
  const existingNode = nodesResponse.items?.find(n => n.title === docName);

  if (existingNode) {
    log(`♻️  任务文档根节点已存在`, 'yellow');
    log(`   node_token: ${existingNode.node_token}`, 'blue');
    return existingNode.node_token;
  }

  // 创建新的任务文档根节点
  log(`📝 创建任务文档根节点: "${docName}"`, 'blue');
  const docNode = await client.createWikiNode(spaceId, bitableNodeToken, docName, 'docx');
  const docNodeToken = docNode.node.node_token;

  // 为文档添加子页面列表块
  await client.createSubPageListBlock(docNode.node.obj_token, docNodeToken);

  log(`✅ 任务文档根节点创建成功`, 'green');
  log(`   node_token: ${docNodeToken}`, 'blue');

  return docNodeToken;
}

/**
 * 获取多维表格的名称
 * @param {object} client - FeishuClient 实例
 * @param {string} appToken - 多维表格 app_token
 * @returns {string} 多维表格名称
 */
async function getBitableName(client, appToken) {
  const response = await client.request(
    'GET',
    `/open-apis/bitable/v1/apps/${appToken}`
  );
  return response.data && response.data.app && response.data.app.name || '';
}

/**
 * 在多维表格中创建数据表并添加所有字段
 * @param {object} client - FeishuClient 实例
 * @param {string} appToken - 多维表格 app_token
 * @param {string} tableName - 数据表名称
 * @returns {string} 新建的 table_id
 */
async function createTaskTable(client, appToken, tableName) {

  // 检查是否已存在同名数据表
  const tablesResponse = await client.request(
    'GET',
    `/open-apis/bitable/v1/apps/${appToken}/tables`
  );
  const tables = tablesResponse.data.items || [];
  const existing = tables.find(t => t.name === tableName);

  if (existing) {
    log(`ℹ️  数据表 "${tableName}" 已存在，直接使用`, 'yellow');
    return existing.table_id;
  }

  // 新建数据表
  const createResponse = await client.request(
    'POST',
    `/open-apis/bitable/v1/apps/${appToken}/tables`,
    { table: { name: tableName } }
  );

  if (createResponse.code !== 0) {
    throw new Error(`创建数据表失败: ${createResponse.msg}`);
  }

  const tableId = createResponse.data.table_id;
  log(`✅ 新建数据表 "${tableName}" 成功`, 'green');
  log(`   table_id: ${tableId}`, 'blue');

  // 把默认的"多行文本"字段重命名为"标题"
  const fieldsResponse = await client.request(
    'GET',
    `/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/fields`
  );
  const defaultField = (fieldsResponse.data.items || []).find(f => f.type === 1);
  if (defaultField) {
    await client.request(
      'PUT',
      `/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/fields/${defaultField.field_id}`,
      { field_name: '标题', type: 1 }
    );
    log(`   ✅ 重命名默认字段为: 标题`, 'green');
  }

  // 按顺序添加其余字段
  const { randomUUID } = require('crypto');
  const requiredFields = [
    { field_name: '描述', type: 1 },
    {
      field_name: '类型', type: 3,
      property: { options: [{ name: '探索' }, { name: '研究' }] }
    },
    {
      field_name: '状态', type: 3,
      property: { options: [{ name: '待确认' }, { name: '待处理' }, { name: '处理中' }, { name: '待审阅' }, { name: '已归档' }, { name: '已拒绝' }, { name: '待改进' }] }
    },
    { field_name: '优先级', type: 2 },
    { field_name: '文档', type: 15 },
    { field_name: '来源链接', type: 15 },
    { field_name: '备注', type: 1 },
    { field_name: '创建时间', type: 5 },
    { field_name: '更新时间', type: 5 }
  ];

  for (const field of requiredFields) {
    const resp = await client.request(
      'POST',
      `/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/fields`,
      field,
      { params: { client_token: randomUUID() } }
    );
    if (resp.code === 0) {
      log(`   ✅ 添加字段: ${field.field_name}`, 'green');
    } else {
      log(`   ⚠️  添加字段失败 ${field.field_name}: ${resp.msg}`, 'yellow');
    }
  }

  return tableId;
}

/**
 * 获取表格的第一个数据表 ID（仅用于 list-fields / add-fields 命令）
 */
async function getFirstTableId(client, appToken) {
  const response = await client.request(
    'GET',
    `/open-apis/bitable/v1/apps/${appToken}/tables`,
    null,
    { ignoreError: false }
  );

  if (response.code !== 0) {
    throw new Error(`获取数据表失败: ${response.msg} (code: ${response.code})`);
  }

  if (!response.data || !response.data.items || response.data.items.length === 0) {
    throw new Error('多维表格中没有数据表');
  }

  const tables = response.data.items;
  log(`找到 ${tables.length} 个数据表`, 'blue');

  return tables[0].table_id;
}

/**
 * 获取现有字段
 */
async function getExistingFields(client, appToken, tableId) {
  const response = await client.request(
    'GET',
    `/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/fields`,
    null,
    { params: { page_size: 100 } }
  );

  if (response.code !== 0) {
    throw new Error(`获取字段列表失败: ${response.msg}`);
  }

  return response.data.items || [];
}

/**
 * 命令：列出字段
 */
async function listFields(configPath) {
  log('📋 查看多维表格字段', 'blue');
  log('================================', 'blue');

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const client = new FeishuClient(config.app_id, config.app_secret);
  const { app_token, table_id } = config.bitable;

  const fields = await getExistingFields(client, app_token, table_id);

  log('\n字段列表：', 'blue');
  log('字段ID\t\t\t\t字段名称\t\t类型', 'blue');
  log(''.padEnd(80, '-'), 'blue');

  const typeNames = {
    0: 'N/A', 1: 'text', 2: 'number', 3: 'singleSelect',
    4: 'multiSelect', 5: 'datetime', 6: 'user', 7: 'lookup',
    11: 'phone', 13: 'url', 14: 'email', 15: 'text',
    17: 'url', 18: 'currency', 19: 'percent', 20: 'rating',
    21: 'checkbox', 22: 'progress', 23: 'level', 24: 'decimal',
    25: 'group', 26: 'formula', 27: 'relation', 28: 'button',
    29: 'modifiedTime', 30: 'createdTime', 31: 'lastModifiedBy',
    32: 'createdBy', 33: 'attachment'
  };

  fields.forEach(field => {
    const typeName = typeNames[field.type] || field.type;
    console.log(`${field.field_id}\t${field.field_name}\t\t${typeName}`);
  });

  log('\n✅ 完成', 'green');
}

/**
 * 命令：添加字段
 */
async function addFields(configPath, bitableUrl) {
  log('📝 添加字段到多维表格', 'blue');
  log('================================', 'blue');

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const client = new FeishuClient(config.app_id, config.app_secret);

  // 验证认证
  await client.getAppAccessToken();
  log('✅ 认证成功', 'green');

  // 提取 app_token（从知识库链接）
  const { appToken } = await extractBitableInfoFromWikiUrl(client, bitableUrl);

  // 获取 table_id
  const tableId = await getFirstTableId(client, appToken);
  log(`✅ 使用 table_id: ${tableId}`, 'green');

  // 获取现有字段
  const existingFields = await getExistingFields(client, appToken, tableId);
  const existingFieldNames = new Set(existingFields.map(f => f.field_name));

  log(`\n现有字段: ${Array.from(existingFieldNames).join(', ') || '(无)'}`, 'blue');

  // 定义需要的字段
  const requiredFields = [
    { field_name: '标题', type: 1 },
    { field_name: '描述', type: 1 },
    {
      field_name: '类型',
      type: 3,
      property: { options: [{ name: '探索' }, { name: '研究' }] }
    },
    {
      field_name: '状态',
      type: 3,
      property: {
        options: [
          { name: '待确认' },
          { name: '待处理' },
          { name: '处理中' },
          { name: '待审阅' },
          { name: '已归档' },
          { name: '已拒绝' },
          { name: '待改进' }
        ]
      }
    },
    { field_name: '优先级', type: 2 },
    { field_name: '文档', type: 15 },
    { field_name: '来源链接', type: 15 },
    { field_name: '备注', type: 1 },
    { field_name: '创建时间', type: 5 },
    { field_name: '更新时间', type: 5 }
  ];

  // 添加缺失的字段
  let addedCount = 0;
  let skippedCount = 0;

  for (const field of requiredFields) {
    if (existingFieldNames.has(field.field_name)) {
      log(`⏭️  跳过已存在的字段: ${field.field_name}`, 'yellow');
      skippedCount++;
      continue;
    }

    try {
      const response = await client.request(
        'POST',
        `/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/fields`,
        field,
        { ignoreError: true }
      );

      if (response.code === 0) {
        log(`✅ 添加字段: ${field.field_name}`, 'green');
        addedCount++;
      } else {
        log(`⚠️  添加字段失败 ${field.field_name}: ${response.msg}`, 'yellow');
      }
    } catch (error) {
      log(`⚠️  添加字段出错 ${field.field_name}: ${error.message}`, 'yellow');
    }
  }

  log(`\n📊 字段添加完成！`, 'blue');
  log(`   新增: ${addedCount} 个`, 'green');
  log(`   跳过: ${skippedCount} 个`, 'yellow');

  // 更新配置文件
  config.bitable.app_token = appToken;
  config.bitable.table_id = tableId;

  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
  log('\n✅ 配置文件已更新', 'green');
}

/**
 * 命令：创建多维表格
 */
async function createBitable(configPath, name = '飞书任务管理') {
  log('🔨 创建多维表格', 'blue');
  log('================================', 'blue');

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const client = new FeishuClient(config.app_id, config.app_secret);

  const response = await client.request(
    'POST',
    '/open-apis/bitable/v1/apps',
    { name: name, folder: '' }
  );

  if (response.code !== 0) {
    throw new Error(`创建多维表格失败: ${response.msg}`);
  }

  const appToken = response.data.app.app_token;
  log(`✅ 多维表格创建成功！`, 'green');
  log(`   App Token: ${appToken}`, 'blue');
  log(`   链接: https://feishu.cn/base/${appToken}`, 'blue');

  // 更新配置
  if (!config.bitable) config.bitable = {};
  config.bitable.app_token = appToken;
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');

  return appToken;
}

/**
 * 命令：创建数据表
 */
async function createTable(configPath, appToken, tableName = '任务表') {
  log('📋 创建数据表', 'blue');
  log('================================', 'blue');

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const client = new FeishuClient(config.app_id, config.app_secret);

  const response = await client.request(
    'POST',
    `/open-apis/bitable/v1/apps/${appToken}/tables`,
    { table: { name: tableName } }
  );

  if (response.code !== 0) {
    throw new Error(`创建数据表失败: ${response.msg}`);
  }

  const tableId = response.data.table_id;
  log(`✅ 数据表创建成功！`, 'green');
  log(`   Table ID: ${tableId}`, 'blue');

  // 更新配置
  if (!config.bitable) config.bitable = {};
  config.bitable.table_id = tableId;
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');

  return tableId;
}

/**
 * 检查并提示用户添加应用到资源
 * @param {string} resourceType - 资源类型（仅支持 'bitable'）
 * @param {string} resourceName - 资源名称/标识
 */
async function checkAndPromptPermission(resourceType, resourceName) {
  log(`\n📋 权限检查提示`, 'yellow');
  log('='.repeat(60), 'blue');

  if (resourceType === 'bitable') {
    log(`⚠️  无法访问知识库中的多维表格`, 'yellow');
    log('', 'reset');
    log('请按以下步骤添加应用到多维表格：', 'blue');
    log('1. 打开知识库中的多维表格', 'reset');
    log('2. 点击右上角 "..."', 'reset');
    log('3. 选择 "更多" → "添加文档应用"', 'reset');
    log('4. 搜索并选择你的应用', 'reset');
    log('5. ⚠️  将权限设置为 "可管理"（默认"可编辑"权限不足）', 'reset');
    log('6. 添加完成后，请重新运行配置命令', 'reset');
  }

  log('', 'reset');
  log('重要提示：', 'yellow');
  log('• 需要在多维表格资源级别添加应用', 'reset');
  log('• 权限必须设置为 "可管理"，默认的 "可编辑" 权限不足', 'reset');
  log('• 如果找不到应用，请检查飞书开放平台中的应用名称', 'reset');
  log('• 添加后可能需要等待几分钟才能生效', 'reset');
  log('='.repeat(60), 'blue');
}

/**
 * 命令：从链接配置
 *
 * 新方案：只需要知识库中的多维表格链接
 * - 多维表格本身作为 Wiki 树的节点
 * - 自动在其下创建 "{表格名字}-任务文档" 作为任务文档的根节点
 */
async function configFromLinks(configPath, bitableUrl, tableName) {
  log('🔗 从链接配置', 'blue');
  log('================================', 'blue');

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const client = new FeishuClient(config.app_id, config.app_secret);

  try {
    // 验证认证
    await client.getAppAccessToken();
    log('✅ 认证成功', 'green');
  } catch (error) {
    log('❌ 认证失败', 'red');
    log('   请检查 app_id 和 app_secret 是否正确', 'yellow');
    return;
  }

  if (!bitableUrl) {
    log('❌ 缺少多维表格链接', 'red');
    log('   请提供知识库中的多维表格链接', 'yellow');
    return;
  }

  try {
    // 从知识库链接提取完整信息
    const { nodeToken, appToken, spaceId, bitableName } = await extractBitableInfoFromWikiUrl(client, bitableUrl);

    // 如果未指定表名，使用多维表格自身的名称作为默认值
    if (!tableName) {
      tableName = bitableName || '任务表';
      if (!bitableName) {
        log(`ℹ️  多维表格无名称，使用默认表名: "${tableName}"`, 'yellow');
      } else {
        log(`ℹ️  使用多维表格名称作为表名: "${tableName}"`, 'blue');
      }
    }

    // 创建数据表
    const tableId = await createTaskTable(client, appToken, tableName);

    // 创建或获取任务文档根节点
    const taskDocRootToken = await ensureTaskDocRoot(client, spaceId, nodeToken, tableName);

    // 更新配置
    if (!config.bitable) config.bitable = {};
    config.bitable.app_token = appToken;
    config.bitable.table_id = tableId;
    config.bitable.table_name = tableName;
    config.bitable.field_names = {
      title: '标题',
      description: '描述',
      type: '类型',
      status: '状态',
      priority: '优先级',
      document: '文档',
      source_url: '来源链接',
      notes: '备注',
      created_time: '创建时间',
      updated_time: '更新时间'
    };

    if (!config.wiki) config.wiki = {};
    config.wiki.space_id = spaceId;
    config.wiki.bitable_node_token = nodeToken;
    config.wiki.parent_node_token = taskDocRootToken;

    log('\n✅ 配置完成', 'green');
    log(`   多维表格 app_token: ${appToken}`, 'blue');
    log(`   数据表 table_id: ${tableId}`, 'blue');
    log(`   数据表名称: ${tableName}`, 'blue');
    log(`   知识库 space_id: ${spaceId}`, 'blue');
    log(`   任务文档根节点: ${taskDocRootToken}`, 'blue');

  } catch (error) {
    if (error.message.includes('permission denied') || error.message.includes('Forbidden') || error.message.includes('RolePermNotAllow')) {
      await checkAndPromptPermission('bitable', bitableUrl);
      return;
    }
    throw error;
  }

  // 保存配置
  fs.writeFileSync(configPath, JSON.stringify(config, null, 2), 'utf8');
  log('\n✅ 配置文件已更新', 'green');

  // 创建配置完成标记
  const configDir = path.dirname(configPath);
  const markerPath = path.join(configDir, '.configured');
  fs.writeFileSync(markerPath, new Date().toISOString(), 'utf8');
  log('✅ 配置标记已创建', 'green');

  // 提示下一步
  log('\n📝 下一步操作：', 'blue');
  log('1. 运行验证脚本确保所有功能正常：', 'reset');
  log('   node scripts/validate.js config/credentials.json', 'reset');
  log('2. 创建第一个任务：', 'reset');
  log('   node scripts/task-manager.js config/credentials.json create "我的第一个任务"', 'reset');
}

/**
 * 命令：检查权限
 */
async function checkPermissions(configPath) {
  log('🔍 检查权限配置', 'blue');
  log('================================', 'blue');

  const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
  const client = new FeishuClient(config.app_id, config.app_secret);

  let allGood = true;

  // 1. 检查认证
  try {
    await client.getAppAccessToken();
    log('✅ 认证 - 正常', 'green');
  } catch (error) {
    log('❌ 认证 - 失败', 'red');
    log('   请检查 app_id 和 app_secret', 'yellow');
    allGood = false;
  }

  // 2. 检查多维表格权限
  if (config.bitable && config.bitable.app_token) {
    try {
      await client.getRecords(
        config.bitable.app_token,
        config.bitable.table_id,
        { pageSize: 1 }
      );
      log('✅ 多维表格访问 - 正常', 'green');
    } catch (error) {
      if (error.message.includes('permission denied') || error.message.includes('Forbidden')) {
        log('❌ 多维表格访问 - 权限不足', 'red');
        await checkAndPromptPermission('bitable', config.bitable.app_token);
        allGood = false;
      } else {
        log('❌ 多维表格访问 - 失败', 'red');
        log('   ' + error.message, 'yellow');
        allGood = false;
      }
    }
  } else {
    log('⚠️  多维表格 - 未配置', 'yellow');
  }

  // 3. 检查知识库权限（通过任务文档根节点验证）
  if (config.wiki && config.wiki.space_id && config.wiki.parent_node_token) {
    try {
      // 通过 get_node 接口验证任务文档根节点是否可访问
      await client.request('GET', `/open-apis/wiki/v2/spaces/${config.wiki.space_id}/nodes/${config.wiki.parent_node_token}`);
      log('✅ 知识库访问 - 正常', 'green');
    } catch (error) {
      if (error.message.includes('permission denied') || error.message.includes('space_id is not int')) {
        log('❌ 知识库访问 - 权限不足', 'red');
        await checkAndPromptPermission('bitable', config.bitable.app_token);
        allGood = false;
      } else {
        log('❌ 知识库访问 - 失败', 'red');
        log('   ' + error.message, 'yellow');
        allGood = false;
      }
    }
  } else {
    log('⚠️  知识库 - 未配置', 'yellow');
  }

  // 总结
  log('\n' + '='.repeat(60), 'blue');
  if (allGood) {
    log('🎉 所有权限检查通过！配置正确。', 'green');
    log('\n下一步：', 'blue');
    log('运行验证脚本测试所有功能：', 'reset');
    log('node scripts/validate.js ' + configPath, 'reset');
  } else {
    log('⚠️  发现权限问题，请按照上述提示完成配置后重新检查。', 'yellow');
  }
  log('='.repeat(60), 'blue');
}

/**
 * 显示帮助
 */
function showHelp() {
  console.log(`
飞书任务管理 - 管理工具

用法: node scripts/admin.js <命令> [参数...]

命令:
  list-fields <configPath>              列出多维表格的所有字段
  add-fields <configPath> <bitableUrl>  添加字段到现有表格
  create-bitable <configPath> [name]    创建新的多维表格
  create-table <configPath> <appToken>  创建新的数据表
  config-from-links <configPath>        从链接配置
    <bitableUrl> [tableName]            知识库中的多维表格链接、可选的数据表名称
  check-permissions <configPath>         检查配置的权限是否正确

多维表格链接格式:
  https://xxx.feishu.cn/wiki/<node_token>  （知识库中的多维表格）

注意: 必须使用知识库中的多维表格链接（/wiki/ 格式），不支持独立的多维表格（/base/ 格式）

示例:
  # 列出字段
  node scripts/admin.js list-fields config/credentials.json

  # 添加字段
  node scripts/admin.js add-fields config/credentials.json \\
    "https://xxx.feishu.cn/wiki/node_token"

  # 从链接配置（使用默认表名）
  node scripts/admin.js config-from-links config/credentials.json \\
    "https://xxx.feishu.cn/wiki/node_token"

  # 从链接配置（指定表名）
  node scripts/admin.js config-from-links config/credentials.json \\
    "https://xxx.feishu.cn/wiki/node_token" "我的任务表"

  # 创建新表格
  node scripts/admin.js create-bitable config/credentials.json "任务管理"
`);
}

/**
 * 主函数
 */
async function main() {
  const command = process.argv[2];

  if (!command || command === '--help' || command === '-h') {
    showHelp();
    return;
  }

  try {
    switch (command) {
      case 'list-fields':
        await listFields(process.argv[3]);
        break;

      case 'add-fields':
        await addFields(process.argv[3], process.argv[4]);
        break;

      case 'create-bitable':
        await createBitable(process.argv[3], process.argv[4]);
        break;

      case 'create-table':
        await createTable(process.argv[3], process.argv[4], process.argv[5]);
        break;

      case 'config-from-links':
        await configFromLinks(process.argv[3], process.argv[4], process.argv[5]);
        break;

      case 'check-permissions':
        await checkPermissions(process.argv[3]);
        break;

      default:
        log(`未知命令: ${command}`, 'red');
        showHelp();
        process.exit(1);
    }
  } catch (error) {
    log(`\n❌ 错误: ${error.message}`, 'red');
    console.error(error);
    process.exit(1);
  }
}

// 运行
if (require.main === module) {
  main();
}

module.exports = {
  listFields,
  addFields,
  createBitable,
  createTable,
  configFromLinks
};
