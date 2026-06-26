/**
 * Figma文件信息获取模块
 */

const axios = require('axios');

/**
 * 从URL或直接ID解析文件ID
 * @param {string} fileInput - Figma文件URL或ID
 * @returns {string} 文件ID
 */
function parseFileId(fileInput) {
  if (fileInput.includes('figma.com')) {
    // 提取文件ID
    const url = new URL(fileInput);
    const pathParts = url.pathname.split('/');

    for (let i = 0; i < pathParts.length; i++) {
      if (pathParts[i] === 'file' || pathParts[i] === 'design') {
        return pathParts[i + 1];
      }
    }

    // 如果没有找到file/design，尝试其他格式
    const possibleId = pathParts[pathParts.length - 1];
    if (possibleId && possibleId.length > 10) {
      return possibleId;
    }
  }

  // 直接返回，假定已经是文件ID
  return fileInput;
}

/**
 * 获取Figma文件信息
 * @param {string} fileId - Figma文件ID
 * @param {string} token - Figma个人访问令牌
 * @returns {Promise<object>} 文件信息
 */
async function getFileInfo(fileId, token) {
  try {
    const headers = {
      'X-Figma-Token': token
    };

    // 1. 获取文件基础信息
    const fileResponse = await axios.get(`https://api.figma.com/v1/files/${fileId}`, { headers });
    const fileData = fileResponse.data;

    // 2. 获取文件版本信息
    const versionsResponse = await axios.get(`https://api.figma.com/v1/files/${fileId}/versions`, { headers });
    const versionsData = versionsResponse.data;

    // 3. 获取评论信息（可选）
    let commentsData = { comments: [] };
    try {
      const commentsResponse = await axios.get(`https://api.figma.com/v1/files/${fileId}/comments`, { headers });
      commentsData = commentsResponse.data;
    } catch (error) {
      // 忽略评论获取错误
    }

    // 构建结构化的文件信息
    const fileInfo = {
      file_id: fileId,
      metadata: {
        name: fileData.name,
        last_modified: fileData.lastModified,
        version: fileData.version,
        thumbnail_url: fileData.thumbnailUrl,
        document: {
          id: fileData.document?.id,
          type: fileData.document?.type,
          children_count: fileData.document?.children?.length || 0
        }
      },
      structure: {
        pages: [],
        components: {
          total: fileData.components ? Object.keys(fileData.components).length : 0,
          list: fileData.components ? Object.keys(fileData.components) : []
        },
        component_sets: {
          total: fileData.componentSets ? Object.keys(fileData.componentSets).length : 0,
          list: fileData.componentSets ? Object.keys(fileData.componentSets) : []
        },
        styles: {
          total: fileData.styles ? Object.keys(fileData.styles).length : 0,
          list: fileData.styles ? Object.keys(fileData.styles) : []
        }
      },
      versions: {
        total: versionsData.versions?.length || 0,
        latest: versionsData.versions?.[0] || null,
        list: versionsData.versions?.slice(0, 5) || [] // 只显示最近5个版本
      },
      collaboration: {
        comments: {
          total: commentsData.comments?.length || 0,
          resolved: commentsData.comments?.filter(c => c.resolved_at).length || 0
        }
      },
      api_info: {
        request_time: new Date().toISOString(),
        figma_api_version: 'v1'
      }
    };

    // 提取页面信息
    if (fileData.document?.children) {
      fileInfo.structure.pages = fileData.document.children.map(page => ({
        id: page.id,
        name: page.name,
        type: page.type,
        children_count: page.children?.length || 0,
        bounds: page.absoluteBoundingBox || null
      }));
    }

    return fileInfo;

  } catch (error) {
    console.error('获取文件信息失败:', error.message);

    // 提供详细的错误信息
    if (error.response) {
      const status = error.response.status;
      const errorData = error.response.data;

      switch (status) {
        case 401:
          throw new Error('认证失败: 无效的FIGMA_ACCESS_TOKEN');
        case 403:
          throw new Error('权限不足: 无法访问此文件');
        case 404:
          throw new Error('文件不存在: 请检查文件ID是否正确');
        case 429:
          throw new Error('API限制: 已达到请求限制，请稍后重试');
        default:
          throw new Error(`Figma API错误 (${status}): ${errorData?.message || '未知错误'}`);
      }
    } else if (error.request) {
      throw new Error('网络错误: 无法连接到Figma API');
    } else {
      throw new Error(`请求配置错误: ${error.message}`);
    }
  }
}

/**
 * 获取Figma文件节点详情
 * @param {string} fileId - Figma文件ID
 * @param {string} nodeId - 节点ID
 * @param {string} token - Figma个人访问令牌
 * @returns {Promise<object>} 节点信息
 */
async function getNodeInfo(fileId, nodeId, token) {
  try {
    const headers = {
      'X-Figma-Token': token
    };

    const response = await axios.get(
      `https://api.figma.com/v1/files/${fileId}/nodes?ids=${nodeId}`,
      { headers }
    );

    return response.data.nodes[nodeId] || null;

  } catch (error) {
    console.error('获取节点信息失败:', error.message);
    throw error;
  }
}

/**
 * 搜索文件中的节点
 * @param {string} fileId - Figma文件ID
 * @param {string} query - 搜索关键词
 * @param {string} token - Figma个人访问令牌
 * @returns {Promise<Array>} 搜索结果
 */
async function searchNodes(fileId, query, token) {
  try {
    const headers = {
      'X-Figma-Token': token
    };

    const response = await axios.get(
      `https://api.figma.com/v1/files/${fileId}/search?query=${encodeURIComponent(query)}`,
      { headers }
    );

    return response.data;

  } catch (error) {
    console.error('搜索节点失败:', error.message);
    throw error;
  }
}

module.exports = {
  parseFileId,
  getFileInfo,
  getNodeInfo,
  searchNodes
};