#!/usr/bin/env node

/**
 * 飞书 API 客户端（纯 JS 实现）
 *
 * 使用 Node.js 原生 https 模块，不依赖任何 npm 包
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

class FeishuClient {
  constructor(appId, appSecret) {
    this.appId = appId;
    this.appSecret = appSecret;
    this.baseUrl = 'open.feishu.cn';
    this.appTokenCache = null;
    this.appTokenExpireTime = 0;
  }

  /**
   * 获取应用访问令牌（app_access_token）- 用于应用级别的操作
   */
  async getAppAccessToken () {
    // 检查缓存是否有效
    if (this.appTokenCache && Date.now() < this.appTokenExpireTime) {
      return this.appTokenCache;
    }

    // 获取新的 token
    const data = {
      app_id: this.appId,
      app_secret: this.appSecret
    };

    const response = await this.requestNoAuth(
      'POST',
      '/open-apis/auth/v3/app_access_token/internal',
      data
    );

    if (response.code !== 0) {
      throw new Error(`获取应用访问令牌失败: ${response.msg}`);
    }

    // 缓存 token（提前 5 分钟过期）
    this.appTokenCache = response.app_access_token;
    this.appTokenExpireTime = Date.now() + (response.expire - 300) * 1000;

    return this.appTokenCache;
  }

  /**
   * 发送 HTTPS 请求（不需要认证）
   * @param {string} method - HTTP 方法
   * @param {string} path - 请求路径
   * @param {object} data - 请求体数据
   * @param {object} options - 额外选项
   */
  async requestNoAuth (method, path, data = null, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers
    };

    const requestOptions = {
      hostname: this.baseUrl,
      port: 443,
      path: path,
      method: method,
      headers: headers
    };

    // 添加查询参数
    if (options.params) {
      const queryString = Object.keys(options.params)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(options.params[key])}`)
        .join('&');
      requestOptions.path += `?${queryString}`;
    }

    return new Promise((resolve, reject) => {
      const req = https.request(requestOptions, (res) => {
        let body = '';

        res.on('data', (chunk) => {
          body += chunk;
        });

        res.on('end', () => {
          try {
            const response = JSON.parse(body);
            if (response.code !== 0 && !options.ignoreError) {
              reject(new Error(`API 请求失败: ${response.msg} (code: ${response.code})`));
            } else {
              resolve(response);
            }
          } catch (error) {
            reject(new Error(`解析响应失败: ${error.message}`));
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`请求失败: ${error.message}`));
      });

      if (data) {
        req.write(JSON.stringify(data));
      }

      req.end();
    });
  }

  /**
   * 发送 HTTPS 请求
   * @param {string} method - HTTP 方法
   * @param {string} path - 请求路径
   * @param {object} data - 请求体数据
   * @param {object} options - 额外选项（可包含 tokenType: 'app' | 'tenant'）
   */
  async request (method, path, data = null, options = {}) {
    const token = await this.getAppAccessToken();

    const headers = {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`,
      ...options.headers
    };

    const requestOptions = {
      hostname: this.baseUrl,
      port: 443,
      path: path,
      method: method,
      headers: headers
    };

    // 添加查询参数
    if (options.params) {
      const queryString = Object.keys(options.params)
        .map(key => `${encodeURIComponent(key)}=${encodeURIComponent(options.params[key])}`)
        .join('&');
      requestOptions.path += `?${queryString}`;
    }

    return new Promise((resolve, reject) => {
      const req = https.request(requestOptions, (res) => {
        let body = '';

        res.on('data', (chunk) => {
          body += chunk;
        });

        res.on('end', () => {
          try {
            const response = JSON.parse(body);
            if (response.code !== 0 && !options.ignoreError) {
              reject(new Error(`API 请求失败: ${response.msg} (code: ${response.code})`));
            } else {
              resolve(response);
            }
          } catch (error) {
            reject(new Error(`解析响应失败: ${error.message}`));
          }
        });
      });

      req.on('error', (error) => {
        reject(new Error(`请求失败: ${error.message}`));
      });

      if (data) {
        req.write(JSON.stringify(data));
      }

      req.end();
    });
  }

  // ==================== Bitable API ====================

  /**
   * 批量创建记录
   * @param {string} appToken - 多维表格 app_token
   * @param {string} tableId - 数据表 table_id
   * @param {array} records - 记录数组
   */
  async createRecords (appToken, tableId, records) {
    const response = await this.request(
      'POST',
      `/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/records/batch_create`,
      { records }
    );
    return response.data;
  }

  /**
   * 创建单条记录
   * @param {string} appToken - 多维表格 app_token
   * @param {string} tableId - 数据表 table_id
   * @param {object} fields - 记录字段
   */
  async createRecord (appToken, tableId, fields) {
    const response = await this.createRecords(appToken, tableId, [{ fields }]);
    return response.records[0];
  }

  /**
   * 获取记录列表
   * @param {string} appToken - 多维表格 app_token
   * @param {string} tableId - 数据表 table_id
   * @param {object} options - 查询选项
   */
  async getRecords (appToken, tableId, options = {}) {
    const params = {
      page_size: options.pageSize || 100,
      ...options.params
    };

    if (options.pageToken) {
      params.page_token = options.pageToken;
    }

    const response = await this.request(
      'GET',
      `/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/records`,
      null,
      { params }
    );

    return response.data;
  }

  /**
   * 获取所有记录（自动分页）
   * @param {string} appToken - 多维表格 app_token
   * @param {string} tableId - 数据表 table_id
   * @param {object} options - 查询选项
   */
  async getAllRecords (appToken, tableId, options = {}) {
    let allRecords = [];
    let pageToken = null;

    do {
      const response = await this.getRecords(appToken, tableId, {
        ...options,
        pageToken
      });

      allRecords = allRecords.concat(response.items);
      pageToken = response.page_token;
    } while (pageToken);

    return allRecords;
  }

  /**
   * 更新记录
   * @param {string} appToken - 多维表格 app_token
   * @param {string} tableId - 数据表 table_id
   * @param {string} recordId - 记录 record_id
   * @param {object} fields - 要更新的字段
   */
  async updateRecord (appToken, tableId, recordId, fields) {
    const response = await this.request(
      'PUT',
      `/open-apis/bitable/v1/apps/${appToken}/tables/${tableId}/records/${recordId}`,
      { fields }
    );
    return response.data;
  }

  // ==================== Wiki API ====================

  /**
   * 创建知识库节点（使用应用权限）
   * @param {string} spaceId - 知识库空间 ID
   * @param {string} parentNodeToken - 父节点 token（可选）
   * @param {string} title - 节点标题
   * @param {string} objType - 对象类型（docx, bitable 等）
   */
  async createWikiNode (spaceId, parentNodeToken, title, objType = 'docx') {
    const data = {
      node_type: 'origin',
      obj_type: objType,
      title: title
    };

    // 如果有父节点，添加父节点信息
    if (parentNodeToken) {
      data.parent_node_token = parentNodeToken;
    }

    const response = await this.request(
      'POST',
      `/open-apis/wiki/v2/spaces/${spaceId}/nodes`,
      data
    );

    return response.data;
  }

  /**
   * 获取文档的所有块
   * @param {string} documentId - 文档 ID（obj_token）
   */
  async getDocumentBlocks (documentId) {
    const response = await this.request(
      'GET',
      `/open-apis/docx/v1/documents/${documentId}/blocks`
    );

    return response.data;
  }

  /**
   * 为文档创建子页面列表块
   * @param {string} documentId - 文档 ID（obj_token）
   * @param {string} wikiToken - Wiki 节点 token（用于 sub_page_list）
   */
  async createSubPageListBlock (documentId, wikiToken) {
    // 1. 获取文档的所有块，找到根块
    const blocksData = await this.getDocumentBlocks(documentId);

    // 找到根块（parent_id 为空或者为 "0" 的块）
    const rootBlock = blocksData.items.find(block => !block.parent_id || block.parent_id === '' || block.parent_id === '0');

    if (!rootBlock) {
      throw new Error('无法找到文档的根块');
    }

    // 2. 在根块下创建子页面列表块
    // block_type: 51 表示 sub_page_list
    const data = {
      index: 0,
      children: [
        {
          block_type: 51,
          sub_page_list: {
            wiki_token: wikiToken
          }
        }
      ]
    };

    const response = await this.request(
      'POST',
      `/open-apis/docx/v1/documents/${documentId}/blocks/${rootBlock.block_id}/children`,
      data
    );

    return response.data;
  }

  /**
   * 获取知识库空间节点列表（使用应用权限）
   * @param {string} spaceId - 知识库空间 ID
   * @param {string} parentNodeToken - 父节点 token（可选）
   */
  async getWikiNodes (spaceId, parentNodeToken = null) {
    const params = {};

    if (parentNodeToken) {
      params.parent_node_token = parentNodeToken;
    }

    const response = await this.request(
      'GET',
      `/open-apis/wiki/v2/spaces/${spaceId}/nodes`,
      null,
      { params }
    );

    return response.data;
  }

  /**
   * 获取节点详情（使用应用权限）
   * @param {string} spaceId - 知识库空间 ID
   * @param {string} nodeId - 节点 ID
   */
  async getWikiNode (spaceId, nodeId) {
    const response = await this.request(
      'GET',
      `/open-apis/wiki/v2/spaces/${spaceId}/nodes/${nodeId}`,
      null
      // 使用应用权限（默认）
    );

    return response.data;
  }

}

/**
 * 从配置文件加载并创建客户端
 * @param {string} configPath - 配置文件路径
 */
function createClientFromConfig (configPath) {
  const fullPath = path.resolve(configPath);

  if (!fs.existsSync(fullPath)) {
    throw new Error(`配置文件不存在: ${fullPath}`);
  }

  const config = JSON.parse(fs.readFileSync(fullPath, 'utf8'));

  if (!config.app_id || !config.app_secret) {
    throw new Error('配置文件缺少 app_id 或 app_secret');
  }

  return new FeishuClient(config.app_id, config.app_secret);
}

module.exports = { FeishuClient, createClientFromConfig };
