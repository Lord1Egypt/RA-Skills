/**
 * 115 分享管理模块
 * 
 * 功能：
 * - 创建分享
 * - 获取分享信息
 * - 更新分享时长
 * - 获取访问列表
 * - 取消分享
 * - 分享码解析
 * - 转存
 */

const HttpClient = require('../client/http-client');
const ErrorHandler = require('../error/error-handler');

class ShareManager {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.apiBase = 'https://webapi.115.com';
    this.errorHandler = new ErrorHandler();
  }

  /**
   * 创建分享
   * @param {string|Array} fileIds - 文件 ID 或 ID 数组
   * @returns {Object} 分享结果
   */
  async createShare(fileIds) {
    try {
      // 转换为数组
      const ids = Array.isArray(fileIds) ? fileIds : [fileIds];
      
      // 获取用户 ID
      const userInfo = await this.http.get('/user/setting');
      const userId = userInfo.data?.user_id || userInfo.data?.uid;
      
      if (!userId) {
        throw new Error('无法获取用户 ID');
      }

      const params = {
        user_id: userId,
        file_ids: ids.join(','),
        ignore_warn: '0',
        is_asc: '0',
        order: 'user_ptime'
      };

      const response = await this.http.post('/share/send', params);

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        if (error) {
          throw error;
        }
        throw new Error(response.error || '创建分享失败');
      }

      return {
        success: true,
        data: response.data,
        message: '分享创建成功'
      };
    } catch (error) {
      if (error.type) {
        throw error;
      }
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 获取分享信息
   * @param {string} shareCode - 分享码
   * @returns {Object} 分享信息
   */
  async getShareInfo(shareCode) {
    try {
      const response = await this.http.get('/share/shareinfo', {
        share_code: shareCode
      });

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error ? error : new Error(response.error || '获取分享信息失败');
      }

      return {
        success: true,
        data: response.data,
        message: '获取成功'
      };
    } catch (error) {
      if (error.type) {
        throw error;
      }
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 更新分享时长
   * @param {string} shareCode - 分享码
   * @param {number} duration - 时长（1/3/5/7/15/-1）
   * @returns {Object} 更新结果
   */
  async updateShareDuration(shareCode, duration) {
    try {
      // 验证时长参数
      const validDurations = [1, 3, 5, 7, 15, -1];
      if (!validDurations.includes(duration)) {
        throw this.errorHandler.createError('INVALID_PARAM', '无效的时长参数', {
          context: { duration, valid: validDurations }
        });
      }

      const params = {
        share_code: shareCode,
        share_duration: duration.toString()
      };

      const response = await this.http.post('/share/updateshare', params);

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error ? error : new Error(response.error || '更新分享时长失败');
      }

      const durationMap = {
        '1': '1 天',
        '3': '3 天',
        '5': '5 天',
        '7': '7 天',
        '15': '15 天',
        '-1': '长期'
      };

      return {
        success: true,
        data: response.data,
        message: `分享时长已更新为 ${durationMap[duration.toString()]}`,
        newDuration: durationMap[duration.toString()]
      };
    } catch (error) {
      if (error.type) {
        throw error;
      }
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 获取分享访问用户列表
   * @param {string} shareCode - 分享码
   * @returns {Object} 访问列表
   */
  async getAccessList(shareCode) {
    try {
      const response = await this.http.get('/share/access_user_list', {
        share_code: shareCode
      });

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error ? error : new Error(response.error || '获取访问列表失败');
      }

      return {
        success: true,
        data: response.data || [],
        count: (response.data || []).length,
        message: '获取成功'
      };
    } catch (error) {
      if (error.type) {
        throw error;
      }
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 取消/删除分享
   * @param {string} shareCode - 分享码
   * @returns {Object} 取消结果
   */
  async cancelShare(shareCode) {
    try {
      const params = {
        share_code: shareCode
      };

      const response = await this.http.post('/share/cancel', params);

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error ? error : new Error(response.error || '取消分享失败');
      }

      return {
        success: true,
        message: '分享已取消'
      };
    } catch (error) {
      if (error.type) {
        throw error;
      }
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 获取用户分享列表
   * @param {Object} options - 选项
   * @returns {Object} 分享列表
   */
  async getShareList(options = {}) {
    try {
      const params = {
        offset: options.offset || '0',
        limit: options.limit || '20'
      };

      const response = await this.http.get('/usershare/list', params);

      if (!response.state) {
        const error = this.errorHandler.fromApiResponse(response);
        throw error ? error : new Error(response.error || '获取分享列表失败');
      }

      return {
        success: true,
        data: response.data || [],
        count: (response.data || []).length,
        total: response.count || 0,
        message: '获取成功'
      };
    } catch (error) {
      if (error.type) {
        throw error;
      }
      throw this.errorHandler.fromHttpError(error);
    }
  }

  /**
   * 解析分享码
   * @param {string} input - 分享链接或码
   * @returns {Object} 解析结果
   */
  parseShareCode(input) {
    let code = input.trim();
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
    const paramMatch = input.match(/[?&]password=([a-zA-Z0-9]{4})/i);
    if (paramMatch) {
      password = paramMatch[1];
    }

    // 从口令格式提取：/abc123-xyzw/
    const koulingMatch = input.match(/\/([a-zA-Z0-9]+)-([a-zA-Z0-9]+)\//i);
    if (koulingMatch) {
      code = koulingMatch[1];
      password = koulingMatch[2];
    }

    return {
      shareCode: code,
      password: password,
      valid: code.length > 0
    };
  }

  /**
   * 格式化分享信息
   * @param {Object} shareInfo - 分享信息
   * @returns {string} 格式化文本
   */
  formatShareInfo(shareInfo) {
    if (!shareInfo || !shareInfo.data) {
      return '分享信息不可用';
    }

    const data = shareInfo.data;
    
    let output = `📦 分享详情\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;
    output += `📝 标题：${data.share_title || '无标题'}\n`;
    output += `🔗 链接：${data.share_url || '无'}\n`;
    
    if (data.receive_code) {
      output += `🔑 提取码：${data.receive_code}\n`;
    }
    
    output += `📁 文件：${data.file_count || 0} 个\n`;
    output += `📂 文件夹：${data.folder_count || 0} 个\n`;
    output += `💾 大小：${this._formatSize(data.total_size || 0)}\n`;
    
    if (data.share_duration) {
      output += `⏰ 有效期：${data.share_duration}\n`;
    }
    
    if (data.receive_count !== undefined) {
      output += `👁️ 访问：${data.receive_count} 次\n`;
    }

    return output;
  }

  /**
   * 格式化分享列表
   * @param {Array} shares - 分享列表
   * @returns {string} 格式化文本
   */
  formatShareList(shares) {
    if (!shares || shares.length === 0) {
      return '暂无分享';
    }

    let output = `📋 我的分享 (${shares.length}个)\n`;
    output += `━━━━━━━━━━━━━━━━━━━━\n`;

    shares.forEach((share, index) => {
      output += `${index + 1}. ${share.share_title || '无标题'}\n`;
      output += `   🔗 ${share.share_code}\n`;
      output += `   📁 ${share.file_count}个文件 | 👁️ ${share.receive_count || 0}次访问\n`;
    });

    return output;
  }

  /**
   * 格式化文件大小
   * @param {number} bytes - 字节数
   * @returns {string} 格式化文本
   */
  _formatSize(bytes) {
    if (bytes === 0) return '0 B';
    
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    const k = 1024;
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    
    return (bytes / Math.pow(k, i)).toFixed(2) + ' ' + units[i];
  }
}

module.exports = ShareManager;
