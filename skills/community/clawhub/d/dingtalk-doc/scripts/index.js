#!/usr/bin/env node

/**
 * 钉钉知识库管理核心脚本
 * 
 * 功能：
 * - 文档增删改查
 * - 目录树管理
 * - 白名单权限校验
 * 
 * 白名单逻辑：
 * - 只有配置了白名单的知识库才允许写入（增/删/改）
 * - 读取操作不需要白名单
 * - 未配置白名单的知识库默认不允许写入
 */

const {
  getWorkspaceList,
  createDoc,
  getNode,
  listNodes,
  deleteDoc,
  queryBlocks,
  overwriteContent,
  deleteBlock,
  modifyBlock,
  insertBlock,
  getAccessToken,
  getCurrentOperatorId
} = require('./dingtalk-client');

const {
  loadConfig,
  checkWritePermission,
  findWorkspaceConfig,
  normalizePath
} = require('./whitelist');

function buildNodeWhitelistPath(nodeName, fallbackId = '') {
  const name = nodeName || fallbackId;
  if (!name) {
    throw new Error('无法获取节点名称，不能进行白名单校验');
  }
  return name.startsWith('/') ? name : '/' + name;
}

function hasWorkspaceWideWhitelist(whitelist) {
  return Array.isArray(whitelist) && whitelist.some(rule => normalizePath(rule) === '/');
}

function getWhitelistSetupHint(config) {
  const configPath = config && config._configPath ? config._configPath : 'config/whitelist.json';
  return `📝 解决方法：在 ${configPath} 中为目标知识库配置 whitelist`;
}

function assertWhitelistFileExists(config) {
  if (config && config._missingConfig) {
    throw new Error(
      `❌ 权限拒绝：未找到白名单配置文件，写入操作已被阻止\n` +
      `📄 配置文件：${config._configPath}\n` +
      `💡 安全策略：所有写入操作必须在白名单内\n` +
      `📝 解决方法：请先手动创建该文件并配置 workspaces / whitelist`
    );
  }
}

/**
 * 获取节点路径（从根节点到当前节点）
 */
async function getNodePath(workspaceId, nodeId, operatorId, options = {}, visited = new Set()) {
  const strict = Boolean(options.strict);
  if (visited.has(nodeId)) {
    if (strict) {
      throw new Error(`检测到节点路径循环：${nodeId}`);
    }
    return '/...';
  }
  visited.add(nodeId);
  
  try {
    const node = await getNode(nodeId, operatorId);
    if (!node || !node.node) {
      if (strict) {
        throw new Error(`节点不存在或无法访问：${nodeId}`);
      }
      return '/';
    }
    
    const nodeData = node.node;
    if (workspaceId && nodeData.workspaceId && nodeData.workspaceId !== workspaceId) {
      throw new Error(`节点 ${nodeId} 属于知识库 ${nodeData.workspaceId}，不是 ${workspaceId}`);
    }
    if (!nodeData.parentNodeId || nodeData.parentNodeId === 'root') return '/' + nodeData.name;
    
    const parentPath = await getNodePath(workspaceId, nodeData.parentNodeId, operatorId, options, visited);
    if (parentPath === '/') return '/' + nodeData.name;
    return parentPath + '/' + nodeData.name;
  } catch (e) {
    if (strict) {
      throw new Error(`无法解析节点路径：${nodeId}。${e.message}`);
    }
    return '/unknown/' + nodeId;
  }
}

/**
 * 获取文档的 workspaceId 和 nodeInfo（用于白名单检查）
 * 
 * 💡 重要：此函数要求传入 nodeId（用于 wiki_2.0 API）
 * workspaceId 只能作为额外一致性校验，不能绕过真实节点归属查询
 * 
 * @param {string} identifier - 节点 ID（从文档链接 /i/nodes/xxx 提取）
 * @param {string} operatorId - 操作者 ID
 * @param {string|null} workspaceId - 可选，如果传入则必须与节点真实 workspaceId 一致
 * @returns {Promise<{workspaceId: string, nodeInfo: Object|null, nodeId: string}>}
 */
async function getDocWorkspaceId(identifier, operatorId, workspaceId = null) {
  const nodeInfo = await getNode(identifier, operatorId);
  
  if (!nodeInfo || !nodeInfo.node || !nodeInfo.node.workspaceId) {
    throw new Error(
      `无法获取文档信息：nodeId = ${identifier}\n` +
      `💡 可能原因：\n` +
      `   - 传入的是 docKey 而不是 nodeId（getNode 需要 nodeId）\n` +
      `   - 当前用户没有读取该节点的权限\n` +
      `💡 解决方法：\n` +
      `   - 优先使用 nodeId（从文档链接 /i/nodes/xxx 提取）\n` +
      `   - 先运行 get-doc --nodeId=<nodeId> 确认文档可访问`
    );
  }

  const actualWorkspaceId = nodeInfo.node.workspaceId;
  if (workspaceId && workspaceId !== actualWorkspaceId) {
    throw new Error(
      `❌ 权限拒绝：传入的 workspaceId 与节点真实归属不一致\n` +
      `传入 workspaceId：${workspaceId}\n` +
      `真实 workspaceId：${actualWorkspaceId}\n` +
      `💡 安全策略：写入操作必须按节点真实所在知识库进行白名单校验`
    );
  }
  
  return { 
    workspaceId: actualWorkspaceId,
    nodeInfo,
    nodeId: identifier // 记录实际使用的 nodeId
  };
}

/**
 * 检查写入权限（白名单）并返回完整权限信息
 * 
 * @param {string} workspaceId - 知识库 ID
 * @param {string} nodeId - 节点 ID
 * @param {string} operatorId - 操作者 ID
 * @param {Object} config - 白名单配置
 * @param {Object|null} nodeInfo - 可选，已查询到的节点信息，避免重复请求
 * @returns {Promise<{docPath: string, permission: Object, wsConfig: Object}>}
 */
async function checkDocWritePermission(workspaceId, nodeId, operatorId, config, nodeInfo = null) {
  assertWhitelistFileExists(config);

  const wsConfig = findWorkspaceConfig(workspaceId, config);
  
  if (!wsConfig || !wsConfig.whitelist) {
    throw new Error(
      `❌ 权限拒绝：知识库 ${workspaceId} 未配置白名单\n` +
      `💡 安全策略：所有写入操作必须在白名单内\n` +
      getWhitelistSetupHint(config)
    );
  }

  const resolvedNodeInfo = nodeInfo || await getNode(nodeId, operatorId);
  const nodeData = resolvedNodeInfo && resolvedNodeInfo.node;
  if (!nodeData) {
    throw new Error(`无法获取节点信息，拒绝写入：${nodeId}`);
  }
  if (nodeData.workspaceId && nodeData.workspaceId !== workspaceId) {
    throw new Error(
      `❌ 权限拒绝：节点真实归属与白名单 workspace 不一致\n` +
      `节点 workspaceId：${nodeData.workspaceId}\n` +
      `白名单 workspaceId：${workspaceId}`
    );
  }

  const docPath = buildNodeWhitelistPath(nodeData.name, nodeId);
  if (hasWorkspaceWideWhitelist(wsConfig.whitelist)) {
    return {
      docPath,
      permission: {
        allowed: true,
        matchedRule: '/'
      },
      wsConfig
    };
  }

  const permission = checkWritePermission(docPath, wsConfig.whitelist, wsConfig.allowRootWrite);
  
  if (!permission.allowed) {
    throw new Error(
      `❌ 权限拒绝：${permission.reason}\n` +
      `📍 目标路径：${docPath}\n` +
      `🔒 安全策略：只有白名单内的路径允许写入\n` +
      `📝 解决方法：将路径添加到 ${config && config._configPath ? config._configPath : 'config/whitelist.json'} 的 whitelist 中`
    );
  }
  
  return { docPath, permission, wsConfig };
}

/**
 * 完整的写入权限检查流程（获取 workspaceId + 检查白名单）
 * 
 * @param {string} identifier - 文档标识符（优先传入 nodeId）
 * @param {string} operatorId - 操作者 ID
 * @param {Object} config - 白名单配置
 * @param {string|null} workspaceId - 可选，如果已知道 workspaceId 可直接传入
 * @returns {Promise<{workspaceId: string, nodeId: string, docPath: string, permission: Object, wsConfig: Object, nodeInfo: Object|null}>}
 */
async function checkFullWritePermission(identifier, operatorId, config, workspaceId = null) {
  const { workspaceId: actualWorkspaceId, nodeInfo, nodeId } = await getDocWorkspaceId(identifier, operatorId, workspaceId);
  const { docPath, permission, wsConfig } = await checkDocWritePermission(actualWorkspaceId, nodeId, operatorId, config, nodeInfo);
  
  return {
    workspaceId: actualWorkspaceId,
    nodeId,
    docPath,
    permission,
    wsConfig,
    nodeInfo
  };
}

/**
 * 列出文档（读取操作，不需要白名单）
 */
async function listDocsWithPermission(workspaceId, parentNodeId = 'root', config = null, senderId = null) {
  if (!config) {
    config = loadConfig();
  }
  
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  const result = await listNodes(workspaceId, parentNodeId, operatorId);
  
  // 为每个节点添加路径信息（只读，不需要权限检查）
  if (result.nodes) {
    for (const node of result.nodes) {
      const nodePath = await getNodePath(workspaceId, node.nodeId, operatorId);
      node.path = nodePath;
    }
  }
  
  return {
    success: true,
    data: {
      workspaceId: workspaceId,
      parentNodeId: parentNodeId,
      nodes: result.nodes || [],
      totalCount: result.nodes ? result.nodes.length : 0
    }
  };
}

/**
 * 创建文档（带白名单检查）
 */
async function createDocWithPermission(workspaceId, name, docType, parentNodeId = 'root', config = null, senderId = null) {
  if (!config) {
    config = loadConfig();
  }
  assertWhitelistFileExists(config);

  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  // 查找该知识库的白名单配置
  const wsConfig = findWorkspaceConfig(workspaceId, config);
  
  // 如果知识库没有配置白名单，不允许写入
  if (!wsConfig || !wsConfig.whitelist) {
    throw new Error(`权限拒绝：知识库 ${workspaceId} 未配置白名单，不允许写入操作\n💡 提示：${getWhitelistSetupHint(config)}`);
  }
  
  // 钉钉 getNode 当前不返回完整父目录链路，白名单按节点名匹配。
  const targetPath = buildNodeWhitelistPath(name);
  
  // 检查写入权限
  const permission = checkWritePermission(targetPath, wsConfig.whitelist, wsConfig.allowRootWrite);
  
  if (!permission.allowed) {
    throw new Error(`权限拒绝：${permission.reason}\n目标路径：${targetPath}`);
  }
  
  // 创建文档
  const params = {
    name: name,
    docType: docType,
    operatorId: operatorId
  };
  
  if (parentNodeId && parentNodeId !== 'root') {
    params.parentNodeId = parentNodeId;
  }
  
  const result = await createDoc(workspaceId, params);
  
  // 💡 重要提示：钉钉 API 返回的 docKey 可能不能直接用于 update-content
  // 后续更新内容时，建议使用 nodeId 作为 docKey 参数
  return {
    success: true,
    data: {
      ...result,
      path: targetPath,
      permissionRule: permission.matchedRule,
      _tip: '后续更新内容时，请使用 nodeId 作为 --docKey 参数（如果 docKey 更新失败）'
    }
  };
}

/**
 * 删除文档（带白名单检查）
 */
async function deleteDocWithPermission(workspaceId, nodeId, config = null, senderId = null) {
  if (!config) {
    config = loadConfig();
  }
  assertWhitelistFileExists(config);

  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  // 查找该知识库的白名单配置
  const wsConfig = findWorkspaceConfig(workspaceId, config);
  
  // 如果知识库没有配置白名单，不允许写入
  if (!wsConfig || !wsConfig.whitelist) {
    throw new Error(`权限拒绝：知识库 ${workspaceId} 未配置白名单，不允许删除操作\n💡 提示：${getWhitelistSetupHint(config)}`);
  }
  
  const nodeInfo = await getNode(nodeId, operatorId);
  const nodeData = nodeInfo && nodeInfo.node;
  if (!nodeData) {
    throw new Error(`无法获取节点信息，拒绝删除：${nodeId}`);
  }
  if (nodeData.workspaceId && nodeData.workspaceId !== workspaceId) {
    throw new Error(`权限拒绝：节点 ${nodeId} 属于知识库 ${nodeData.workspaceId}，不是 ${workspaceId}`);
  }

  const docPath = buildNodeWhitelistPath(nodeData.name, nodeId);
  const permission = hasWorkspaceWideWhitelist(wsConfig.whitelist)
    ? { allowed: true, matchedRule: '/' }
    : checkWritePermission(docPath, wsConfig.whitelist, wsConfig.allowRootWrite);
  
  if (!permission.allowed) {
    throw new Error(`权限拒绝：${permission.reason}\n目标路径：${docPath}`);
  }
  
  const result = await deleteDoc(workspaceId, nodeId, operatorId);
  
  return {
    success: true,
    data: {
      ...result,
      path: docPath
    }
  };
}

/**
 * 获取文档详情（读取操作，不需要白名单）
 */
async function getDocDetail(nodeId, config = null, senderId = null) {
  if (!config) {
    config = loadConfig();
  }
  
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  const result = await getNode(nodeId, operatorId, {
    withStatisticalInfo: true,
    withPermissionRole: true
  });
  
  // 获取路径
  let docPath = '/unknown';
  if (result.node && result.node.workspaceId) {
    docPath = await getNodePath(result.node.workspaceId, nodeId, operatorId);
  }
  
  return {
    success: true,
    data: {
      ...result,
      path: docPath
    }
  };
}

/**
 * 搜索文档（读取操作，不需要白名单）
 */
async function searchDocs(workspaceId, keyword, config = null, senderId = null) {
  if (!config) {
    config = loadConfig();
  }
  
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  async function getAllNodes(parentNodeId = 'root') {
    try {
      const result = await listNodes(workspaceId, parentNodeId, operatorId);
      const nodes = result.nodes || [];
      
      const allNodes = [...nodes];
      
      for (const node of nodes) {
        if (node.type === 'FOLDER' || node.category === 'FOLDER') {
          const childNodes = await getAllNodes(node.nodeId);
          allNodes.push(...childNodes);
        }
      }
      
      return allNodes;
    } catch (e) {
      return [];
    }
  }
  
  const allNodes = await getAllNodes();
  
  const matchedNodes = allNodes.filter(node => 
    node.name && node.name.toLowerCase().includes(keyword.toLowerCase())
  );
  
  for (const node of matchedNodes) {
    const nodePath = await getNodePath(workspaceId, node.nodeId, operatorId);
    node.path = nodePath;
  }
  
  return {
    success: true,
    data: {
      keyword: keyword,
      total: matchedNodes.length,
      nodes: matchedNodes
    }
  };
}

/**
 * 获取知识库列表（读取操作，不需要白名单）
 */
async function listWorkspaces(senderId = null) {
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  const result = await getWorkspaceList(operatorId);
  
  return {
    success: true,
    data: result.workspaces || result || []
  };
}

/**
 * 获取文档内容（读取操作，不需要白名单）
 * API: GET /v1.0/doc/suites/documents/{docKey}/blocks
 */
async function getDocContent(docKey, senderId = null) {
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  const result = await queryBlocks(docKey, operatorId);
  
  return {
    success: true,
    data: result
  };
}

/**
 * 更新文档内容（写入操作，强制白名单检查）
 * API: POST /v1.0/doc/suites/documents/{docKey}/overwriteContent
 * 
 * ⚠️ 硬性规定：所有写入操作必须先通过白名单检查，无法绕过！
 * 
 * 💡 重要：nodeId vs docKey
 * - 参数 `nodeId`: 用于 getNode / getNodePath / 白名单路径定位（wiki_2.0 API）
 * - 参数 `docKey`: 用于 overwriteContent 实际写入（suites/documents API）
 * - createDoc 返回的 docKey 和 nodeId 可能不同
 * - 经验：大多数情况下 nodeId 可以直接用作 docKey，如果失败请传入真实的 docKey
 * 
 * @param {string} nodeId - 节点 ID（从文档链接 /i/nodes/xxx 提取，用于白名单检查）
 * @param {string} markdown - 新的文档内容（markdown 格式）
 * @param {Object|null} config - 白名单配置
 * @param {string|null} senderId - 发送者 ID
 * @param {string|null} workspaceId - 可选，如果已知道 workspaceId 可直接传入
 * @param {string|null} docKey - 可选，真实的 docKey（如果不传则使用 nodeId 代替）
 */
async function updateDocContent(nodeId, markdown, config = null, senderId = null, workspaceId = null, docKey = null) {
  if (!config) {
    config = loadConfig();
  }
  
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  // ✅ 复用 helper：完整的权限检查流程
  const { docPath, permission } = await checkFullWritePermission(nodeId, operatorId, config, workspaceId);
  
  // ========== 白名单检查通过，允许写入 ==========
  
  // 使用真实的 docKey（如果传入），否则用 nodeId 代替
  const actualDocKey = docKey || nodeId;
  const result = await overwriteContent(actualDocKey, markdown, operatorId);
  
  return {
    success: true,
    data: {
      ...result,
      path: docPath,
      permissionRule: permission.matchedRule
    }
  };
}

/**
 * 删除块元素（写入操作，需要白名单）
 * API: DELETE /v1.0/doc/suites/documents/{docKey}/blocks/{blockId}
 * 
 * @param {string} nodeId - 节点 ID（用于白名单检查）
 * @param {string} blockId - 块 ID
 * @param {Object|null} config - 白名单配置
 * @param {string|null} senderId - 发送者 ID
 * @param {string|null} workspaceId - 可选，知识库 ID
 * @param {string|null} docKey - 可选，真实的 docKey（如果不传则使用 nodeId 代替）
 */
async function deleteBlockWithPermission(nodeId, blockId, config = null, senderId = null, workspaceId = null, docKey = null) {
  if (!config) {
    config = loadConfig();
  }
  
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  await checkFullWritePermission(nodeId, operatorId, config, workspaceId);
  
  const actualDocKey = docKey || nodeId;
  const result = await deleteBlock(actualDocKey, blockId, operatorId);
  
  return { success: true, data: result };
}

/**
 * 修改块元素（写入操作，需要白名单）
 * API: PUT /v1.0/doc/suites/documents/{docKey}/blocks/{blockId}
 * 
 * @param {string} nodeId - 节点 ID（用于白名单检查）
 * @param {string} blockId - 块 ID
 * @param {Object} element - 块元素对象
 * @param {Object|null} config - 白名单配置
 * @param {string|null} senderId - 发送者 ID
 * @param {string|null} workspaceId - 可选，知识库 ID
 * @param {string|null} docKey - 可选，真实的 docKey（如果不传则使用 nodeId 代替）
 */
async function modifyBlockWithPermission(nodeId, blockId, element, config = null, senderId = null, workspaceId = null, docKey = null) {
  if (!config) {
    config = loadConfig();
  }
  
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  await checkFullWritePermission(nodeId, operatorId, config, workspaceId);
  
  const actualDocKey = docKey || nodeId;
  const result = await modifyBlock(actualDocKey, blockId, element, operatorId);
  
  return { success: true, data: result };
}

/**
 * 插入块元素（写入操作，需要白名单）
 * API: POST /v1.0/doc/suites/documents/{docKey}/blocks
 * 
 * @param {string} nodeId - 节点 ID（用于白名单检查）
 * @param {Object} element - 块元素对象
 * @param {number|null} position - 插入位置（数字，支持 0）
 * @param {Object|null} config - 白名单配置
 * @param {string|null} senderId - 发送者 ID
 * @param {string|null} workspaceId - 可选，知识库 ID
 * @param {string|null} docKey - 可选，真实的 docKey（如果不传则使用 nodeId 代替）
 */
async function insertBlockWithPermission(nodeId, element, position = null, config = null, senderId = null, workspaceId = null, docKey = null) {
  if (!config) {
    config = loadConfig();
  }
  
  const token = await getAccessToken();
  const operatorId = await getCurrentOperatorId(token, senderId);
  
  await checkFullWritePermission(nodeId, operatorId, config, workspaceId);
  
  const actualDocKey = docKey || nodeId;
  const result = await insertBlock(actualDocKey, element, operatorId, position);
  
  return { success: true, data: result };
}

// 命令行入口
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  // 获取 senderId（优先级：命令行参数 > 环境变量）
  const getSenderId = () => {
    const senderIdArg = args.find(a => a.startsWith('--senderId='));
    if (senderIdArg) {
      return senderIdArg.slice('--senderId='.length);
    }
    return process.env.OPENCLAW_SENDER_ID || process.env.DINGTALK_SENDER_ID || null;
  };
  const senderId = getSenderId();
  
  if (!command) {
    console.log(`
钉钉知识库管理工具

用法:
  node index.js <command> [options]

命令:
  知识库管理:
    list-workspaces           获取知识库列表
    list-docs                 列出文档
    create-doc                创建文档
    delete-doc                删除文档
    get-doc                   获取文档详情
    search                    搜索文档

  文档内容:
    get-content               获取文档内容（块结构）
    update-content            更新文档内容（整篇覆写）

  块级操作:
    delete-block              删除块元素
    modify-block              修改块元素
    insert-block              插入块元素

参数说明:
  --senderId    钉钉用户 ID
  --nodeId      节点 ID（必填，用于白名单检查；从文档链接 /i/nodes/xxx 提取）
  --docKey      文档标识符（可选，用于实际写入；不传则使用 nodeId 代替）
  --workspaceId 知识库 ID（可选，当自动获取失败时手动指定）
  --name        文档名称
  --content     文档内容（markdown 格式）
  --docType     文档类型：DOC, WORKBOOK, MIND, FOLDER
  --parentNodeId 父节点 ID（默认 root）
  --blockId     块 ID（用于块级操作，通过 get-content 获取）
  --element     块元素 JSON（用于 modify-block, insert-block）
  --position    插入位置（用于 insert-block，可选，数字，支持 0）

💡 提示:
  - senderId 会自动从钉钉连接器获取，无需手动指定
  - **nodeId vs docKey**: 
    - nodeId 用于 getNode / 白名单路径定位（wiki_2.0 API）
    - docKey 用于 overwriteContent / modifyBlock 等实际写入（suites API）
    - createDoc 返回的 docKey 和 nodeId 可能不同
    - 经验：大多数情况下 nodeId 可直接用作 docKey，如果失败再传入真实的 docKey
  - 块级操作前，先用 get-content 获取文档结构，找到目标 blockId

白名单规则:
  - 只有配置了白名单的知识库才允许写入（增/删/改）
  - 未配置白名单的知识库默认不允许写入
  - 读取操作不需要白名单
`);
    process.exit(0);
  }
  
  try {
    let result;
    
    const getParam = (name) => {
      const prefix = `--${name}=`;
      const arg = args.find(a => a.startsWith(prefix));
      return arg ? arg.slice(prefix.length) : null;
    };
    
    const decodeCliValue = (value) => {
      if (value == null) {
        return value;
      }
      
      try {
        return decodeURIComponent(value);
      } catch {
        return value;
      }
    };
    
    /**
     * 解析 JSON 字符串为对象
     * 用于 --element 等 JSON 参数
     */
    const parseJsonParam = (paramName, value) => {
      if (value == null) {
        return value;
      }
      
      const decoded = decodeCliValue(value);
      
      try {
        return JSON.parse(decoded);
      } catch (e) {
        throw new Error(`参数解析失败：--${paramName} 的值不是合法的 JSON 格式\n原始值：${value}\n错误：${e.message}`);
      }
    };
    
    /**
     * 解析数字参数
     * 用于 --position 等数字参数
     */
    const parseNumberParam = (paramName, value) => {
      if (value == null || value === '') {
        return null;
      }
      
      const num = Number(value);
      if (isNaN(num)) {
        throw new Error(`参数解析失败：--${paramName} 的值不是合法的数字：${value}`);
      }
      return num;
    };
    
    const workspaceId = getParam('workspaceId');
    
    let config;
    try {
      config = loadConfig();
    } catch (e) {
      config = {};
    }
    
    const effectiveWorkspaceId = workspaceId || (config.workspaces && config.workspaces[0] ? config.workspaces[0].workspaceId : null);
    
    switch (command) {
      case 'list-workspaces':
        result = await listWorkspaces(senderId);
        break;
        
      case 'list-docs':
        const parentNodeId1 = getParam('parentNodeId') || 'root';
        if (!effectiveWorkspaceId) throw new Error('缺少必填参数：--workspaceId=');
        result = await listDocsWithPermission(effectiveWorkspaceId, parentNodeId1, config, senderId);
        break;
        
      case 'create-doc':
        const name = getParam('name');
        const docType = getParam('docType') || 'DOC';
        const parentNodeId2 = getParam('parentNodeId') || 'root';
        
        if (!name) throw new Error('缺少必填参数：--name=');
        if (!effectiveWorkspaceId) throw new Error('缺少必填参数：--workspaceId=');
        
        result = await createDocWithPermission(effectiveWorkspaceId, decodeCliValue(name), docType, parentNodeId2, config, senderId);
        break;
        
      case 'delete-doc':
        const nodeId1 = getParam('nodeId');
        
        if (!nodeId1) throw new Error('缺少必填参数：--nodeId=');
        if (!effectiveWorkspaceId) throw new Error('缺少必填参数：--workspaceId=');
        
        result = await deleteDocWithPermission(effectiveWorkspaceId, nodeId1, config, senderId);
        break;
        
      case 'get-doc':
        const nodeId2 = getParam('nodeId');
        
        if (!nodeId2) throw new Error('缺少必填参数：--nodeId=');
        
        result = await getDocDetail(nodeId2, config, senderId);
        break;
        
      case 'search':
        const keyword = getParam('keyword');
        
        if (!keyword) throw new Error('缺少必填参数：--keyword=');
        if (!effectiveWorkspaceId) throw new Error('缺少必填参数：--workspaceId=');
        
        result = await searchDocs(effectiveWorkspaceId, decodeCliValue(keyword), config, senderId);
        break;
        
      case 'get-content':
        const docKey1 = getParam('docKey') || getParam('nodeId');
        
        if (!docKey1) throw new Error('缺少必填参数：--docKey=');
        
        result = await getDocContent(docKey1, senderId);
        break;
        
      case 'update-content':
        // ✅ 明确拆分：--nodeId 用于白名单检查，--docKey 用于实际写入（可选）
        const nodeId_uc = getParam('nodeId');
        const docKey_uc = getParam('docKey'); // 可选，真实的 docKey
        const content = getParam('content');
        const workspaceIdParam = getParam('workspaceId');
        
        if (!nodeId_uc) throw new Error('缺少必填参数：--nodeId=');
        if (!content) throw new Error('缺少必填参数：--content=');
        
        result = await updateDocContent(nodeId_uc, decodeCliValue(content), config, senderId, workspaceIdParam, docKey_uc);
        break;
        
      case 'delete-block':
        const nodeId_db = getParam('nodeId');
        const docKey_db = getParam('docKey'); // 可选
        const blockId2 = getParam('blockId');
        const workspaceId4 = getParam('workspaceId');
        
        if (!nodeId_db) throw new Error('缺少必填参数：--nodeId=');
        if (!blockId2) throw new Error('缺少必填参数：--blockId=');
        
        result = await deleteBlockWithPermission(nodeId_db, blockId2, config, senderId, workspaceId4, docKey_db);
        break;
        
      case 'modify-block':
        const nodeId_mb = getParam('nodeId');
        const docKey_mb = getParam('docKey'); // 可选
        const blockId3 = getParam('blockId');
        const element = getParam('element');
        const workspaceId5 = getParam('workspaceId');
        
        if (!nodeId_mb) throw new Error('缺少必填参数：--nodeId=');
        if (!blockId3) throw new Error('缺少必填参数：--blockId=');
        if (!element) throw new Error('缺少必填参数：--element=');
        
        const elementObj = parseJsonParam('element', element);
        result = await modifyBlockWithPermission(nodeId_mb, blockId3, elementObj, config, senderId, workspaceId5, docKey_mb);
        break;
        
      case 'insert-block':
        const nodeId_ib = getParam('nodeId');
        const docKey_ib = getParam('docKey'); // 可选
        const element2 = getParam('element');
        const positionParam = getParam('position');
        const workspaceId6 = getParam('workspaceId');
        
        if (!nodeId_ib) throw new Error('缺少必填参数：--nodeId=');
        if (!element2) throw new Error('缺少必填参数：--element=');
        
        const elementObj2 = parseJsonParam('element', element2);
        const positionNum = parseNumberParam('position', positionParam);
        result = await insertBlockWithPermission(nodeId_ib, elementObj2, positionNum, config, senderId, workspaceId6, docKey_ib);
        break;
        
      default:
        console.error(`未知命令：${command}`);
        process.exit(1);
    }
    
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      success: false,
      error: error.message,
      code: error.code
    }, null, 2));
    process.exit(1);
  }
}

module.exports = {
  getNodePath,
  listDocsWithPermission,
  createDocWithPermission,
  deleteDocWithPermission,
  getDocDetail,
  searchDocs,
  listWorkspaces,
  getDocContent,
  updateDocContent,
  deleteBlockWithPermission,
  modifyBlockWithPermission,
  insertBlockWithPermission
};

if (require.main === module) {
  main();
}
