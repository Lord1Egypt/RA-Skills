#!/usr/bin/env node

/**
 * 钉钉 API 客户端封装
 * 
 * 功能：
 * - 获取 access_token
 * - 调用钉钉开放平台 API
 * - 错误处理和重试
 * 
 * 环境变量：
 * - DINGTALK_CLIENTID: 钉钉应用 Client ID (AppKey)
 * - DINGTALK_CLIENTSECRET: 钉钉应用 Client Secret (AppSecret)
 * - Token：POST /v1.0/oauth2/accessToken（api.dingtalk.com）
 * - operatorId：OPENCLAW_SENDER_ID / DINGTALK_SENDER_ID → oapi user/get → unionId
 */

const https = require('https');

// 配置
const DINGTALK_API_HOST = 'api.dingtalk.com';
let tokenCache = null;
let tokenExpiry = 0;

// 强制刷新（调试用）
const FORCE_REFRESH = process.argv.includes('--refresh');
if (FORCE_REFRESH) {
  tokenCache = null;
  tokenExpiry = 0;
}

// 用户缓存（避免重复查询）
const userCache = new Map();
const CACHE_TTL = 5 * 60 * 1000; // 5 分钟

// 调试模式
const DEBUG = process.argv.includes('--debug') || process.env.DINGTALK_DEBUG === 'true';

function maskValue(value, keep = 4) {
  if (!value) {
    return value;
  }
  const str = String(value);
  if (str.length <= keep) {
    return '*'.repeat(str.length);
  }
  return `${'*'.repeat(Math.max(0, str.length - keep))}${str.slice(-keep)}`;
}

function sanitizeDebugPath(path) {
  const [pathname, query = ''] = path.split('?');
  if (!query) {
    return pathname;
  }

  const sanitizedQuery = query
    .split('&')
    .filter(Boolean)
    .map(part => {
      const [key] = part.split('=');
      return `${key}=***`;
    })
    .join('&');

  return `${pathname}?${sanitizedQuery}`;
}

function summarizeBody(body) {
  if (!body || typeof body !== 'object' || Array.isArray(body)) {
    return 'body-present';
  }
  return `keys=${Object.keys(body).join(',')}`;
}

/**
 * 获取环境变量
 */
function getEnv() {
  const clientId = process.env.DINGTALK_CLIENTID;
  const clientSecret = process.env.DINGTALK_CLIENTSECRET;
  
  if (!clientId || !clientSecret) {
    throw new Error('缺少钉钉凭证配置：请设置 DINGTALK_CLIENTID 和 DINGTALK_CLIENTSECRET 环境变量');
  }
  
  return { clientId, clientSecret };
}

/**
 * 通过 userId 获取 unionId（operatorId）
 */
async function getUnionId(userId, token) {
  // 检查缓存
  const cached = userCache.get(userId);
  if (cached && Date.now() - cached.timestamp < CACHE_TTL) {
    return cached.unionId;
  }
  
  // 使用旧版 API
  return new Promise((resolve, reject) => {
    const req = https.request({
      hostname: 'oapi.dingtalk.com',
      port: 443,
      path: `/user/get?access_token=${token}&userid=${encodeURIComponent(userId)}`,
      method: 'GET'
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          if (result.errcode !== 0) {
            reject(new Error(`获取用户信息失败：${result.errmsg}`));
            return;
          }
          const unionId = result.unionid;
          userCache.set(userId, { unionId, timestamp: Date.now() });
          resolve(unionId);
        } catch (e) {
          reject(new Error(`解析响应失败：${e.message}`));
        }
      });
    });
    
    req.on('error', (e) => {
      reject(new Error(`请求失败：${e.message}`));
    });
    
    req.end();
  });
}

/**
 * 获取当前用户的 operatorId
 *
 * 优先级：
 * 1. 命令行参数 --senderId=（最高优先级，由 index.js 从消息上下文传入）
 * 2. 环境变量 OPENCLAW_SENDER_ID / DINGTALK_SENDER_ID（向后兼容）
 * 3. 抛出错误
 */
async function getCurrentOperatorId(token = null, senderId = null) {
  // 优先使用传入的 senderId 参数
  if (!senderId) {
    senderId = process.env.OPENCLAW_SENDER_ID || process.env.DINGTALK_SENDER_ID;
  }

  if (!senderId) {
    throw new Error(
      '缺少 sender_id：请确保通过 --senderId= 参数传入，或设置 OPENCLAW_SENDER_ID / DINGTALK_SENDER_ID 环境变量'
    );
  }

  if (!token) {
    token = await getAccessToken();
  }

  if (DEBUG) {
    console.log(`[调试] 正在通过 sender_id 查询 unionId: ${maskValue(senderId)}`);
  }

  try {
    const unionId = await getUnionId(senderId, token);
    if (DEBUG) {
      console.error(`[用户识别] 已解析当前会话用户 (sender: ${maskValue(senderId)}, operator: ${maskValue(unionId)})`);
    }
    return unionId;
  } catch (e) {
    throw new Error(
      `获取 unionId 失败：${e.message}\n` +
      `sender_id: ${senderId}\n` +
      `可能原因：\n` +
      `  1. 钉钉应用缺少"通讯录读"权限\n` +
      `  2. sender_id 不是有效的钉钉用户 ID\n` +
      `  3. access_token 已过期`
    );
  }
}

/**
 * 获取 access_token（企业内部应用）
 * POST https://api.dingtalk.com/v1.0/oauth2/accessToken
 *
 * @returns {Promise<string>} 用于请求头 x-acs-dingtalk-access-token 的 accessToken
 */
async function getAccessToken() {
  if (FORCE_REFRESH) {
    tokenCache = null;
    tokenExpiry = 0;
  }

  if (tokenCache && Date.now() < tokenExpiry) {
    return tokenCache;
  }

  const { clientId, clientSecret } = getEnv();
  const body = JSON.stringify({ appKey: clientId, appSecret: clientSecret });

  return new Promise((resolve, reject) => {
    const req = https.request(
      {
        hostname: DINGTALK_API_HOST,
        port: 443,
        path: '/v1.0/oauth2/accessToken',
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Content-Length': Buffer.byteLength(body)
        }
      },
      (res) => {
        let data = '';

        res.on('data', (chunk) => {
          data += chunk;
        });

        res.on('end', () => {
          try {
            const result = JSON.parse(data);

            if (res.statusCode !== 200) {
              reject(
                new Error(
                  `获取 token 失败：HTTP ${res.statusCode} - ${result.message || result.code || res.statusMessage || data}`
                )
              );
              return;
            }

            if (result.code && result.code !== 0) {
              reject(new Error(`获取 token 失败：${result.message || JSON.stringify(result)}`));
              return;
            }

            const accessToken = result.accessToken;
            if (!accessToken) {
              reject(new Error('获取 token 失败：响应中无 accessToken'));
              return;
            }

            const expireInSec =
              result.expireIn != null
                ? Number(result.expireIn)
                : result.expiresIn != null
                  ? Number(result.expiresIn)
                  : 7200;

            tokenCache = accessToken;
            tokenExpiry = Date.now() + expireInSec * 1000 - 5 * 60 * 1000;

            resolve(tokenCache);
          } catch (e) {
            reject(new Error(`解析 token 响应失败：${e.message}`));
          }
        });
      }
    );

    req.on('error', (e) => {
      reject(new Error(`请求失败：${e.message}`));
    });

    req.write(body);
    req.end();
  });
}

/**
 * 调用钉钉 API
 * 
 * @param {string} method - HTTP 方法 (GET|POST|PUT|DELETE)
 * @param {string} path - API 路径
 * @param {Object} headers - 额外请求头
 * @param {Object} body - 请求体（POST/PUT 时）
 * @returns {Promise<Object>} API 响应
 */
async function request(method, path, headers = {}, body = null) {
  const accessToken = await getAccessToken();
  
  if (DEBUG) {
    console.log(`[调试] ${method} ${sanitizeDebugPath(path)}`);
    if (body) {
      console.log(`[调试] 请求体已省略 (${summarizeBody(body)})`);
    }
  }
  
  return new Promise((resolve, reject) => {
    const defaultHeaders = {
      'Content-Type': 'application/json',
      'x-acs-dingtalk-access-token': accessToken
    };
    
    const options = {
      hostname: DINGTALK_API_HOST,
      port: 443,
      path: path,
      method: method,
      headers: { ...defaultHeaders, ...headers }
    };
    
    const req = https.request(options, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          
          if (DEBUG) {
            console.log(`[调试] 响应状态：HTTP ${res.statusCode}, requestId=${result.requestId || res.headers['x-acs-request-id'] || 'no-request-id'}`);
          }
          
          // 检查错误码
          if (result.code && !result.success) {
            let friendlyMessage = result.message || result.code;
            
            // 常见错误的友好提示
            if (result.code === 'paramError' && result.message?.includes('operatorId')) {
              friendlyMessage = 'operatorId 格式无效或用户不在组织内';
            } else if (result.code === 'forbidden.accessDenied') {
              friendlyMessage = '权限不足：请检查钉钉应用权限和白名单配置';
            } else if (result.code === 'invalidRequest.workspaceNode.notFound') {
              friendlyMessage = '文档或知识库不存在';
            }
            
            const error = new Error(
              `API 调用失败：${friendlyMessage}\n` +
              `错误码：${result.code}\n` +
              `请求 ID：${result.requestId || 'no-request-id'}`
            );
            error.code = result.code;
            error.requestId = result.requestId;
            reject(error);
            return;
          }
          
          resolve(result);
        } catch (e) {
          reject(new Error(`解析响应失败：${e.message}`));
        }
      });
    });
    
    req.on('error', (e) => {
      reject(new Error(`请求失败：${e.message}`));
    });
    
    if (body) {
      req.write(JSON.stringify(body));
    }
    
    req.end();
  });
}

/**
 * 创建知识库文档
 */
async function createDoc(workspaceId, params) {
  const path = `/v1.0/doc/workspaces/${workspaceId}/docs`;
  return await request('POST', path, {}, params);
}

/**
 * 获取节点详情 (wiki_2.0)
 * API: GET /v2.0/wiki/nodes/{nodeId}
 */
async function getNode(nodeId, operatorId, options = {}) {
  let path = `/v2.0/wiki/nodes/${nodeId}?operatorId=${encodeURIComponent(operatorId)}`;
  if (options.withStatisticalInfo) {
    path += '&withStatisticalInfo=true';
  }
  if (options.withPermissionRole) {
    path += '&withPermissionRole=true';
  }
  return await request('GET', path);
}

/**
 * 获取节点列表 (wiki_2.0)
 * API: GET /v2.0/wiki/nodes?workspaceId=xxx&parentNodeId=xxx
 */
async function listNodes(workspaceId, parentNodeId, operatorId) {
  let path = `/v2.0/wiki/nodes?workspaceId=${workspaceId}&operatorId=${encodeURIComponent(operatorId)}`;
  if (parentNodeId && parentNodeId !== 'root') {
    path += `&parentNodeId=${parentNodeId}`;
  } else {
    path += '&parentNodeId=root';
  }
  return await request('GET', path);
}

/**
 * 删除知识库文档 (doc_1.0)
 * API: DELETE /v1.0/doc/workspaces/{workspaceId}/docs/{nodeId}
 */
async function deleteDoc(workspaceId, nodeId, operatorId) {
  const path = `/v1.0/doc/workspaces/${workspaceId}/docs/${nodeId}?operatorId=${encodeURIComponent(operatorId)}`;
  return await request('DELETE', path);
}

/**
 * 通过链接获取节点 (wiki_2.0)
 * API: GET /v2.0/wiki/nodes/url
 */
async function getNodeByLink(workspaceId, url, operatorId) {
  const path = `/v2.0/wiki/nodes/url?workspaceId=${workspaceId}&operatorId=${encodeURIComponent(operatorId)}&url=${encodeURIComponent(url)}`;
  return await request('GET', path);
}

/**
 * 复制文档 (wiki_2.0)
 * API: POST /v2.0/wiki/nodes/{nodeId}/copy
 */
async function copyNode(nodeId, targetWorkspaceId, targetParentNodeId, operatorId) {
  const path = `/v2.0/wiki/nodes/${nodeId}/copy`;
  const body = {
    targetWorkspaceId: targetWorkspaceId,
    targetParentNodeId: targetParentNodeId,
    operatorId: operatorId
  };
  return await request('POST', path, {}, body);
}

/**
 * 获取知识库列表
 * 优先使用 wiki_2.0 API（只需要 Document.WorkspaceDocument.Read 权限）
 * API: GET /v2.0/wiki/mineWorkspaces
 */
async function getWorkspaceList(operatorId) {
  const path = `/v2.0/wiki/mineWorkspaces?operatorId=${encodeURIComponent(operatorId)}`;
  const result = await request('GET', path);
  
  // 返回格式统一化
  if (result.workspace) {
    return { workspaces: [result.workspace] };
  }
  return result;
}

/**
 * 获取知识库详情 (doc_1.0)
 * API: GET /v1.0/doc/workspaces/{workspaceId}
 */
async function getWorkspace(workspaceId, operatorId) {
  const path = `/v1.0/doc/workspaces/${workspaceId}?operatorId=${encodeURIComponent(operatorId)}`;
  return await request('GET', path);
}

/**
 * 新建知识库 (doc_1.0)
 * API: POST /v1.0/doc/workspaces
 */
async function createWorkspace(name, operatorId, description = '') {
  const path = `/v1.0/doc/workspaces`;
  const body = {
    name: name,
    operatorId: operatorId,
    description: description
  };
  return await request('POST', path, {}, body);
}

// ============ 文档企业 API (suites/documents) ============

/**
 * 查询文档块结构
 * API: GET /v1.0/doc/suites/documents/{docKey}/blocks
 */
async function queryBlocks(docKey, operatorId) {
  const path = `/v1.0/doc/suites/documents/${docKey}/blocks?operatorId=${encodeURIComponent(operatorId)}`;
  return await request('GET', path);
}

/**
 * 覆写文档内容
 * API: POST /v1.0/doc/suites/documents/{docKey}/overwriteContent
 */
async function overwriteContent(docKey, markdown, operatorId) {
  const path = `/v1.0/doc/suites/documents/${docKey}/overwriteContent?operatorId=${encodeURIComponent(operatorId)}`;
  const body = {
    dataType: 'markdown',
    content: markdown
  };
  return await request('POST', path, {}, body);
}

/**
 * 插入块元素
 * API: POST /v1.0/doc/suites/documents/{docKey}/blocks
 * 
 * @param {Object} element - 块元素对象（已经是 parsed 的 JSON 对象）
 * @param {number|null} position - 插入位置（数字，支持 0）
 */
async function insertBlock(docKey, element, operatorId, position = null) {
  const path = `/v1.0/doc/suites/documents/${docKey}/blocks?operatorId=${encodeURIComponent(operatorId)}`;
  const body = { element };
  if (position !== null) {
    body.position = position; // 此时 position 已经是数字类型
  }
  return await request('POST', path, {}, body);
}

/**
 * 删除块元素
 * API: DELETE /v1.0/doc/suites/documents/{docKey}/blocks/{blockId}
 */
async function deleteBlock(docKey, blockId, operatorId) {
  const path = `/v1.0/doc/suites/documents/${docKey}/blocks/${blockId}?operatorId=${encodeURIComponent(operatorId)}`;
  return await request('DELETE', path);
}

/**
 * 修改、更新块元素
 * API: PUT /v1.0/doc/suites/documents/{docKey}/blocks/{blockId}
 * 
 * @param {Object} element - 块元素对象（已经是 parsed 的 JSON 对象）
 */
async function modifyBlock(docKey, blockId, element, operatorId) {
  const path = `/v1.0/doc/suites/documents/${docKey}/blocks/${blockId}?operatorId=${encodeURIComponent(operatorId)}`;
  const body = { element }; // element 已经是对象，不需要再处理
  return await request('PUT', path, {}, body);
}

/**
 * 主函数 - 命令行入口
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];
  
  if (!command) {
    console.log('钉钉 API 客户端');
    console.log('');
    console.log('用法:');
    console.log('  node dingtalk-client.js <command> [options]');
    console.log('');
    console.log('命令:');
    console.log('  get-token                 获取 access_token');
    console.log('  get-workspace-list        获取知识库列表');
    console.log('  get-workspace             获取知识库详情');
    console.log('  create-doc                创建文档');
    console.log('  get-node                  获取节点详情');
    console.log('  list-nodes                获取节点列表');
    console.log('  delete-doc                删除文档');
    console.log('');
    console.log('环境变量:');
    console.log('  DINGTALK_CLIENTID         钉钉应用 Client ID');
    console.log('  DINGTALK_CLIENTSECRET     钉钉应用 Client Secret');
    process.exit(0);
  }
  
  try {
    let result;
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
    
    switch (command) {
      case 'get-token':
        const token = await getAccessToken();
        result = { accessToken: token };
        break;
        
      case 'get-workspace-list':
        const operatorId1 = args.find(a => a.startsWith('--operatorId='))?.split('=')[1];
        if (!operatorId1) {
          throw new Error('缺少参数：--operatorId=');
        }
        result = await getWorkspaceList(operatorId1);
        break;
        
      case 'get-workspace':
        const workspaceId1 = args.find(a => a.startsWith('--workspaceId='))?.split('=')[1];
        const operatorId2 = args.find(a => a.startsWith('--operatorId='))?.split('=')[1];
        if (!workspaceId1 || !operatorId2) {
          throw new Error('缺少参数：--workspaceId= 和 --operatorId=');
        }
        result = await getWorkspace(workspaceId1, operatorId2);
        break;
        
      case 'create-doc':
        const workspaceId2 = args.find(a => a.startsWith('--workspaceId='))?.split('=')[1];
        const name = args.find(a => a.startsWith('--name='))?.split('=')[1];
        const docType = args.find(a => a.startsWith('--docType='))?.split('=')[1];
        const operatorId3 = args.find(a => a.startsWith('--operatorId='))?.split('=')[1];
        const parentNodeId = args.find(a => a.startsWith('--parentNodeId='))?.split('=')[1];
        
        if (!workspaceId2 || !name || !docType || !operatorId3) {
          throw new Error('缺少必填参数：--workspaceId=, --name=, --docType=, --operatorId=');
        }
        
        const createParams = {
          name: decodeCliValue(name),
          docType: docType,
          operatorId: operatorId3
        };
        
        if (parentNodeId) {
          createParams.parentNodeId = parentNodeId;
        }
        
        result = await createDoc(workspaceId2, createParams);
        break;
        
      case 'get-node':
        const nodeId1 = args.find(a => a.startsWith('--nodeId='))?.split('=')[1];
        const operatorId4 = args.find(a => a.startsWith('--operatorId='))?.split('=')[1];
        if (!nodeId1 || !operatorId4) {
          throw new Error('缺少参数：--nodeId= 和 --operatorId=');
        }
        result = await getNode(nodeId1, operatorId4);
        break;
        
      case 'list-nodes':
        const workspaceId3 = args.find(a => a.startsWith('--workspaceId='))?.split('=')[1];
        const parentNodeId2 = args.find(a => a.startsWith('--parentNodeId='))?.split('=')[1];
        const operatorId5 = args.find(a => a.startsWith('--operatorId='))?.split('=')[1];
        if (!workspaceId3 || !operatorId5) {
          throw new Error('缺少参数：--workspaceId= 和 --operatorId=');
        }
        result = await listNodes(workspaceId3, parentNodeId2, operatorId5);
        break;
        
      case 'delete-doc':
        const workspaceId4 = args.find(a => a.startsWith('--workspaceId='))?.split('=')[1];
        const nodeId2 = args.find(a => a.startsWith('--nodeId='))?.split('=')[1];
        const operatorId6 = args.find(a => a.startsWith('--operatorId='))?.split('=')[1];
        if (!workspaceId4 || !nodeId2 || !operatorId6) {
          throw new Error('缺少参数：--workspaceId=, --nodeId=, --operatorId=');
        }
        result = await deleteDoc(workspaceId4, nodeId2, operatorId6);
        break;
        
      default:
        console.error(`未知命令：${command}`);
        process.exit(1);
    }
    
    console.log(JSON.stringify(result, null, 2));
  } catch (error) {
    console.error(JSON.stringify({
      error: error.message,
      code: error.code,
      requestId: error.requestId
    }, null, 2));
    process.exit(1);
  }
}

// 导出函数供其他模块使用
module.exports = {
  getAccessToken,
  getCurrentOperatorId,
  getUnionId,
  request,
  getWorkspaceList,
  getWorkspace,
  createWorkspace,
  createDoc,
  getNode,
  listNodes,
  deleteDoc,
  getNodeByLink,
  copyNode,
  // 文档企业 API
  queryBlocks,
  overwriteContent,
  insertBlock,
  modifyBlock,
  deleteBlock
};

// 命令行执行
if (require.main === module) {
  main();
}
