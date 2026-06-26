/**
 * 115 分享转存模块
 * 
 * 功能：
 * - 分享码解析（支持多种格式）
 * - 分享详情获取
 * - 单文件/批量转存
 * - 一键转存全部
 * - 创建分享
 */
const HttpClient = require('../client/http-client');

class ShareTransfer {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.apiBase = 'https://webapi.115.com';
  }

  /**
   * 解析分享码
   * 支持格式：
   * - 纯分享码：abc123
   * - 完整链接：https://115.com/s/abc123
   * - 带提取码：abc123#xyzw
   * - URL 参数：https://115.com/s/abc123?password=xyzw
   * 
   * @param {string} shareCode - 分享码或链接
   * @returns {Object} 解析结果
   */
  parseShareCode(shareCode) {
    let code = shareCode.trim();
    let password = '';

    // 提取完整链接中的分享码
    const urlMatch = code.match(/115\.com\/s\/([a-zA-Z0-9]+)/i);
    if (urlMatch) {
      code = urlMatch[1];
    }

    // 提取提取码（#号分隔）
    const hashMatch = code.match(/#([a-zA-Z0-9]{4})$/i);
    if (hashMatch) {
      password = hashMatch[1];
      code = code.replace(hashMatch[0], '');
    }

    // 从 URL 参数提取
    const paramMatch = shareCode.match(/[?&]password=([a-zA-Z0-9]{4})/i);
    if (paramMatch) {
      password = paramMatch[1];
    }

    // 从 URL 参数提取 receive_code
    const receiveMatch = shareCode.match(/[?&]receive_code=([a-zA-Z0-9]{4})/i);
    if (receiveMatch) {
      password = receiveMatch[1];
    }

    return {
      success: true,
      code,
      password,
      original: shareCode
    };
  }

  /**
   * 获取分享详情
   * @param {string} shareCode - 分享码
   * @param {string} password - 提取码
   * @returns {Promise<Object>} 分享详情
   */
  async getShareInfo(shareCode, password = '') {
    const { code } = this.parseShareCode(shareCode);

    const response = await this.http.get('/share/snap', {
      share_code: code,
      receive_code: password,
      _: Date.now()
    });

    if (!response.state) {
      return { success: false, message: response.error || '获取分享信息失败' };
    }

    return {
      success: true,
      shareCode: code,
      title: response.data?.title || '',
      description: response.data?.desc || '',
      userId: response.data?.user_id,
      userName: response.data?.user_name,
      files: response.data?.list || [],
      totalCount: response.data?.count || 0,
      totalSize: response.data?.size || 0,
      hasPassword: !!response.data?.need_password
    };
  }

  /**
   * 转存单个文件
   * @param {string} fileId - 文件 ID
   * @param {string} shareCode - 分享码
   * @param {string} targetCid - 目标目录 ID
   * @param {string} password - 提取码
   * @returns {Promise<Object>} 转存结果
   */
  async transferFile(fileId, shareCode, targetCid = '0', password = '') {
    const { code } = this.parseShareCode(shareCode);

    const response = await this.http.post('/share/receive', {
      share_code: code,
      receive_code: password,
      fid: fileId,
      cid: targetCid
    });

    if (!response.state) {
      return { success: false, message: response.error || '转存失败' };
    }

    return {
      success: true,
      fileId,
      newFileId: response.data?.fid,
      fileName: response.data?.file_name
    };
  }

  /**
   * 批量转存
   * @param {Array<string>} fileIds - 文件 ID 数组
   * @param {string} shareCode - 分享码
   * @param {string} targetCid - 目标目录 ID
   * @param {string} password - 提取码
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 转存结果
   */
  async batchTransfer(fileIds, shareCode, targetCid = '0', password = '', options = {}) {
    const { onProgress = null } = options;
    const results = {
      total: fileIds.length,
      success: 0,
      failed: 0,
      details: []
    };

    const batchSize = 50;
    for (let i = 0; i < fileIds.length; i += batchSize) {
      const batch = fileIds.slice(i, i + batchSize);
      
      const batchResults = await Promise.all(
        batch.map(async (fid) => {
          try {
            const result = await this.transferFile(fid, shareCode, targetCid, password);
            results.success++;
            return { success: true, fileId: fid, ...result };
          } catch (error) {
            results.failed++;
            return { success: false, fileId: fid, error: error.message };
          }
        })
      );

      results.details.push(...batchResults);

      onProgress?.({
        processed: Math.min(i + batchSize, fileIds.length),
        total: fileIds.length,
        success: results.success,
        failed: results.failed
      });

      // 避免速率限制
      if (i + batchSize < fileIds.length) {
        await this.http.sleep(1000);
      }
    }

    return results;
  }

  /**
   * 一键转存整个分享
   * @param {string} shareCode - 分享码
   * @param {string} targetCid - 目标目录 ID
   * @param {string} password - 提取码
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 转存结果
   */
  async transferAll(shareCode, targetCid = '0', password = '', options = {}) {
    const { onProgress = null } = options;

    // 1. 获取分享详情
    const shareInfo = await this.getShareInfo(shareCode, password);
    
    if (shareInfo.totalCount === 0) {
      throw new Error('分享中没有文件');
    }

    // 2. 收集所有文件 ID
    const fileIds = shareInfo.files.map(f => f.fid || f.file_id);

    // 3. 批量转存
    return this.batchTransfer(fileIds, shareCode, targetCid, password, onProgress);
  }

  /**
   * 创建分享
   * @param {string|array} fid - 文件 ID 或 ID 数组
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 分享信息
   */
  async createShare(fid, options = {}) {
    const {
      shareTime = 0,  // 0=永久，1=1 天，7=7 天
      needPassword = false,
      password = ''
    } = options;

    const fids = Array.isArray(fid) ? fid : [fid];

    const response = await this.http.post('/share/send', {
      fid: fids.join(','),
      share_time: shareTime,
      need_password: needPassword ? 1 : 0,
      password
    });

    if (!response.state) {
      return { success: false, message: response.error || '创建分享失败' };
    }

    return {
      success: true,
      shareCode: response.data?.share_code,
      shareUrl: `https://115.com/s/${response.data?.share_code}`,
      password: response.data?.receive_code || '',
      expireTime: shareTime === 0 ? '永久' : `${shareTime}天`,
      fileCount: fids.length
    };
  }

  /**
   * 获取分享列表
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 分享列表
   */
  async getShareList(options = {}) {
    const { page = 1, size = 100 } = options;

    const response = await this.http.get('/share/list', {
      offset: (page - 1) * size,
      limit: size,
      _: Date.now()
    });

    if (!response.state) {
      throw new Error(response.error || '获取分享列表失败');
    }

    return {
      success: true,
      shares: response.data || [],
      totalCount: response.count || 0,
      currentPage: page
    };
  }

  /**
   * 删除分享
   * @param {string} shareId - 分享 ID
   * @returns {Promise<Object>} 删除结果
   */
  async deleteShare(shareId) {
    const response = await this.http.post('/share/delete', {
      share_id: shareId
    });

    if (!response.state) {
      throw new Error(response.error || '删除分享失败');
    }

    return {
      success: true,
      shareId
    };
  }

  /**
   * 修改分享
   * @param {string} shareId - 分享 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 修改结果
   */
  async updateShare(shareId, options = {}) {
    const { shareTime, needPassword, password } = options;

    const params = { share_id: shareId };
    if (shareTime !== undefined) params.share_time = shareTime;
    if (needPassword !== undefined) params.need_password = needPassword ? 1 : 0;
    if (password !== undefined) params.password = password;

    const response = await this.http.post('/share/update', params);

    if (!response.state) {
      throw new Error(response.error || '修改分享失败');
    }

    return {
      success: true,
      shareId
    };
  }
}

module.exports = ShareTransfer;
