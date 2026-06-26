const HttpClient = require('../client/http-client');

/**
 * 115 文件操作 API
 * 
 * 功能：
 * - 移动文件
 * - 复制文件
 * - 删除文件
 * - 重命名文件
 * - 创建文件夹
 */
class FileOperations {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
  }

  /**
   * 移动文件/文件夹
   * @param {string|array} fid - 文件 ID 或 ID 数组
   * @param {string} targetCid - 目标目录 ID
   * @returns {Promise<Object>} 操作结果
   */
  async moveFiles(fid, targetCid = '0') {
    const fids = Array.isArray(fid) ? fid : [fid];

    const response = await this.http.post('/files/move', {
      fid: fids.join(','),
      pid: targetCid
    });

    if (!response.state) {
      return { success: false, message: response.error || '移动文件失败', movedCount: 0, targetCid, fileIds: fids };
    }

    return {
      success: true,
      movedCount: fids.length,
      targetCid,
      fileIds: fids
    };
  }

  /**
   * 复制文件/文件夹
   * @param {string|array} fid - 文件 ID 或 ID 数组
   * @param {string} targetCid - 目标目录 ID
   * @returns {Promise<Object>} 操作结果
   */
  async copyFiles(fid, targetCid = '0') {
    const fids = Array.isArray(fid) ? fid : [fid];

    const response = await this.http.post('/files/copy', {
      fid: fids.join(','),
      pid: targetCid
    });

    if (!response.state) {
      return { success: false, message: response.error || '复制文件失败', copiedCount: 0, targetCid, fileIds: fids };
    }

    return {
      success: true,
      copiedCount: fids.length,
      targetCid,
      fileIds: fids
    };
  }

  /**
   * 删除文件/文件夹
   * @param {string|array} fid - 文件 ID 或 ID 数组
   * @returns {Promise<Object>} 操作结果
   */
  async deleteFiles(fid) {
    const fids = Array.isArray(fid) ? fid : [fid];

    const response = await this.http.post('/files/delete', {
      fid: fids.join(',')
    });

    if (!response.state) {
      return { success: false, message: response.error || '删除文件失败', deletedCount: 0, fileIds: fids };
    }

    return {
      success: true,
      deletedCount: fids.length,
      fileIds: fids
    };
  }

  /**
   * 重命名文件/文件夹
   * @param {string} fid - 文件 ID
   * @param {string} newName - 新名称
   * @returns {Promise<Object>} 操作结果
   */
  async renameFile(fid, newName) {
    const response = await this.http.post('/files/edit', {
      fid,
      file_name: newName
    });

    if (!response.state) {
      return { success: false, message: response.error || '重命名失败', fileId: fid };
    }

    return {
      success: true,
      fileId: fid,
      oldName: response.data?.file_name || '',
      newName
    };
  }

  /**
   * 创建文件夹
   * @param {string} folderName - 文件夹名称
   * @param {string} parentCid - 父目录 ID
   * @returns {Promise<Object>} 操作结果
   */
  async createFolder(folderName, parentCid = '0') {
    const response = await this.http.post('/files/add', {
      pid: parentCid,
      cname: folderName
    });

    if (!response.state) {
      return { success: false, message: response.error || '创建文件夹失败', folderName, parentCid };
    }

    return {
      success: true,
      folderId: response.data?.cid || response.cid,
      folderName,
      parentCid,
      createTime: response.data?.create_time || Date.now()
    };
  }

  /**
   * 批量操作（移动/复制/删除）
   * @param {Array<Object>} operations - 操作数组
   * @returns {Promise<Object>} 操作结果
   */
  async batchOperations(operations) {
    const results = {
      total: operations.length,
      success: 0,
      failed: 0,
      details: []
    };

    const batchSize = 50;
    for (let i = 0; i < operations.length; i += batchSize) {
      const batch = operations.slice(i, i + batchSize);
      
      const batchResults = await Promise.all(
        batch.map(async (op) => {
          try {
            let result;
            switch (op.action) {
              case 'move':
                result = await this.moveFiles(op.fid, op.targetCid);
                break;
              case 'copy':
                result = await this.copyFiles(op.fid, op.targetCid);
                break;
              case 'delete':
                result = await this.deleteFiles(op.fid);
                break;
              case 'rename':
                result = await this.renameFile(op.fid, op.newName);
                break;
              default:
                return { success: false, message: `未知操作：${op.action}` };
            }
            results.success++;
            return { success: true, ...result };
          } catch (error) {
            results.failed++;
            return { success: false, error: error.message, operation: op };
          }
        })
      );

      results.details.push(...batchResults);

      // 避免速率限制
      if (i + batchSize < operations.length) {
        await this.http.sleep(1000);
      }
    }

    return results;
  }

  /**
   * 设置星标
   * @param {string} fid - 文件 ID
   * @param {boolean} star - 是否星标
   * @returns {Promise<Object>} 操作结果
   */
  async setStar(fid, star = true) {
    const response = await this.http.post('/files/star', {
      fid,
      star: star ? 1 : 0
    });

    if (!response.state) {
      return { success: false, message: response.error || '设置星标失败', fileId: fid };
    }

    return {
      success: true,
      fileId: fid,
      starred: star
    };
  }

  /**
   * 获取回收站文件列表
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 回收站文件列表
   */
  async getRecycleBin(options = {}) {
    const { page = 1, size = 100 } = options;

    const response = await this.http.get('/files/recycle', {
      offset: (page - 1) * size,
      limit: size,
      _: Date.now()
    });

    if (!response.state) {
      return { success: false, message: response.error || '获取回收站失败', files: [] };
    }

    return {
      success: true,
      files: response.data || [],
      totalCount: response.count || 0,
      currentPage: page
    };
  }

  /**
   * 从回收站恢复文件
   * @param {string|array} fid - 文件 ID 或 ID 数组
   * @returns {Promise<Object>} 操作结果
   */
  async restoreFiles(fid) {
    const fids = Array.isArray(fid) ? fid : [fid];

    const response = await this.http.post('/files/restore', {
      fid: fids.join(',')
    });

    if (!response.state) {
      return { success: false, message: response.error || '恢复文件失败', fileIds: fids };
    }

    return {
      success: true,
      restoredCount: fids.length,
      fileIds: fids
    };
  }

  /**
   * 清空回收站
   * @returns {Promise<Object>} 操作结果
   */
  async clearRecycleBin() {
    const response = await this.http.post('/files/clear_recycle');

    if (!response.state) {
      return { success: false, message: response.error || '清空回收站失败' };
    }

    return {
      success: true,
      message: '回收站已清空'
    };
  }
}

module.exports = FileOperations;
