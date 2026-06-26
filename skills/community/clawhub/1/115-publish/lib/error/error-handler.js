/**
 * 错误处理模块
 * 
 * 统一错误分类、友好提示和恢复建议
 */

class ErrorHandler {
  constructor() {
    // 错误分类
    this.errorTypes = {
      // 网络错误
      NETWORK: 'network',
      TIMEOUT: 'timeout',
      
      // 认证错误
      AUTH: 'auth',
      COOKIE_EXPIRED: 'cookie_expired',
      NOT_LOGGED_IN: 'not_logged_in',
      
      // 权限错误
      PERMISSION: 'permission',
      ACCESS_DENIED: 'access_denied',
      
      // 参数错误
      PARAM: 'param',
      INVALID_PARAM: 'invalid_param',
      MISSING_PARAM: 'missing_param',
      
      // 资源错误
      NOT_FOUND: 'not_found',
      FILE_NOT_FOUND: 'file_not_found',
      DIR_NOT_FOUND: 'dir_not_found',
      
      // 服务器错误
      SERVER: 'server',
      SERVER_ERROR: 'server_error',
      
      // 业务错误
      BUSINESS: 'business',
      SPACE_FULL: 'space_full',
      FILE_EXISTS: 'file_exists',
      
      // 未知错误
      UNKNOWN: 'unknown'
    };

    // 错误消息模板
    this.messages = {
      [this.errorTypes.NETWORK]: '网络不稳定，请稍后重试',
      [this.errorTypes.TIMEOUT]: '请求超时，请检查网络连接',
      [this.errorTypes.AUTH]: '认证失败，请重新登录',
      [this.errorTypes.COOKIE_EXPIRED]: '登录已过期，请重新扫码登录',
      [this.errorTypes.NOT_LOGGED_IN]: '请先登录',
      [this.errorTypes.PERMISSION]: '权限不足，无法执行此操作',
      [this.errorTypes.ACCESS_DENIED]: '访问被拒绝',
      [this.errorTypes.PARAM]: '参数错误',
      [this.errorTypes.INVALID_PARAM]: '参数格式不正确',
      [this.errorTypes.MISSING_PARAM]: '缺少必要参数',
      [this.errorTypes.NOT_FOUND]: '资源不存在',
      [this.errorTypes.FILE_NOT_FOUND]: '文件不存在或已删除',
      [this.errorTypes.DIR_NOT_FOUND]: '目录不存在',
      [this.errorTypes.SERVER]: '服务器开小差了，请稍后再试',
      [this.errorTypes.SERVER_ERROR]: '服务器错误',
      [this.errorTypes.BUSINESS]: '操作失败',
      [this.errorTypes.SPACE_FULL]: '存储空间不足',
      [this.errorTypes.FILE_EXISTS]: '文件已存在',
      [this.errorTypes.UNKNOWN]: '未知错误，请稍后重试'
    };

    // 恢复建议
    this.recoveries = {
      [this.errorTypes.NETWORK]: [
        '检查网络连接',
        '稍后重试',
        '切换网络环境'
      ],
      [this.errorTypes.TIMEOUT]: [
        '检查网络速度',
        '减少请求数据量',
        '稍后重试'
      ],
      [this.errorTypes.AUTH]: [
        '重新扫码登录',
        '检查 Cookie 是否有效'
      ],
      [this.errorTypes.COOKIE_EXPIRED]: [
        '回复"登录 115"重新扫码',
        '使用 /115 登录 命令'
      ],
      [this.errorTypes.NOT_LOGGED_IN]: [
        '回复"登录 115"开始登录',
        '使用 /115 登录 命令'
      ],
      [this.errorTypes.PERMISSION]: [
        '联系管理员获取权限',
        '检查文件所有权'
      ],
      [this.errorTypes.ACCESS_DENIED]: [
        '检查文件分享状态',
        '联系文件所有者'
      ],
      [this.errorTypes.PARAM]: [
        '检查参数格式',
        '查看使用帮助'
      ],
      [this.errorTypes.INVALID_PARAM]: [
        '检查参数格式是否正确',
        '参考示例用法'
      ],
      [this.errorTypes.MISSING_PARAM]: [
        '补充必要参数',
        '查看命令帮助'
      ],
      [this.errorTypes.NOT_FOUND]: [
        '检查路径是否正确',
        '使用搜索功能查找'
      ],
      [this.errorTypes.FILE_NOT_FOUND]: [
        '使用"搜索"功能查找文件',
        '检查文件是否被移动'
      ],
      [this.errorTypes.DIR_NOT_FOUND]: [
        '使用"文件"命令浏览目录',
        '检查目录路径'
      ],
      [this.errorTypes.SERVER]: [
        '稍后重试',
        '如持续失败请联系客服'
      ],
      [this.errorTypes.SERVER_ERROR]: [
        '稍后重试',
        '查看 115 服务状态'
      ],
      [this.errorTypes.BUSINESS]: [
        '查看具体错误信息',
        '检查操作条件'
      ],
      [this.errorTypes.SPACE_FULL]: [
        '回复"清理建议"获取清理方案',
        '使用 /115 清理 命令',
        '删除不需要的文件'
      ],
      [this.errorTypes.FILE_EXISTS]: [
        '使用其他文件名',
        '先删除已存在的文件'
      ],
      [this.errorTypes.UNKNOWN]: [
        '稍后重试',
        '查看详细错误日志'
      ]
    };

    // 错误日志
    this.errorLog = [];
    this.maxLogSize = 100;
  }

  /**
   * 创建错误对象
   * @param {string} type - 错误类型
   * @param {string} message - 错误消息
   * @param {Object} options - 选项
   * @returns {Object} 错误对象
   */
  createError(type, message = null, options = {}) {
    const errorType = this.errorTypes[type.toUpperCase()] || this.errorTypes.UNKNOWN;
    
    const error = {
      type: errorType,
      message: message || this.messages[errorType],
      recoveries: this.recoveries[errorType] || [],
      timestamp: Date.now(),
      stack: options.stack || null,
      originalError: options.originalError || null,
      context: options.context || {}
    };

    // 记录日志
    this._logError(error);

    return error;
  }

  /**
   * 从 HTTP 错误创建错误对象
   * @param {Error} error - HTTP 错误
   * @returns {Object} 错误对象
   */
  fromHttpError(error) {
    const status = error.response?.status;
    const data = error.response?.data;
    
    // 根据状态码分类
    if (!status) {
      return this.createError('NETWORK', error.message, {
        originalError: error
      });
    }

    if (status === 401 || status === 403) {
      return this.createError('AUTH', '认证失败', {
        originalError: error,
        context: { status, data }
      });
    }

    if (status === 404) {
      return this.createError('NOT_FOUND', '资源不存在', {
        originalError: error,
        context: { status, data }
      });
    }

    if (status === 400) {
      return this.createError('PARAM', data?.error || '参数错误', {
        originalError: error,
        context: { status, data }
      });
    }

    if (status >= 500) {
      return this.createError('SERVER', '服务器错误', {
        originalError: error,
        context: { status, data }
      });
    }

    return this.createError('UNKNOWN', error.message, {
      originalError: error,
      context: { status, data }
    });
  }

  /**
   * 从 API 响应创建错误对象
   * @param {Object} response - API 响应
   * @returns {Object} 错误对象
   */
  fromApiResponse(response) {
    const errno = response.errno || response.errNo || response.code;
    const message = response.error || response.message || response.msg;

    // 115 API 特定错误码
    if (errno === 990001 || errno === 990002) {
      return this.createError('COOKIE_EXPIRED', '登录已过期', {
        context: { errno, message, response }
      });
    }

    if (errno === 90008) {
      return this.createError('FILE_NOT_FOUND', '文件不存在或已删除', {
        context: { errno, message, response }
      });
    }

    if (errno === 430003) {
      return this.createError('DIR_NOT_FOUND', '目录不存在', {
        context: { errno, message, response }
      });
    }

    if (errno === 980005) {
      return this.createError('PERMISSION', '权限不足', {
        context: { errno, message, response }
      });
    }

    // 通用错误
    if (errno !== 0 && errno !== '0' && response.state !== true) {
      return this.createError('BUSINESS', message || '操作失败', {
        context: { errno, message, response }
      });
    }

    return null; // 不是错误
  }

  /**
   * 获取友好的错误消息
   * @param {Object} error - 错误对象
   * @returns {string} 友好消息
   */
  getFriendlyMessage(error) {
    if (!error) return '未知错误';
    return error.message || this.messages[error.type] || '发生错误';
  }

  /**
   * 获取恢复建议
   * @param {Object} error - 错误对象
   * @returns {Array<string>} 建议列表
   */
  getRecoveries(error) {
    if (!error) return [];
    return error.recoveries || this.recoveries[error.type] || [];
  }

  /**
   * 格式化错误输出
   * @param {Object} error - 错误对象
   * @returns {string} 格式化文本
   */
  formatError(error) {
    if (!error) return '';

    let output = `❌ ${this.getFriendlyMessage(error)}\n`;
    
    const recoveries = this.getRecoveries(error);
    if (recoveries.length > 0) {
      output += '\n💡 建议：\n';
      recoveries.forEach((rec, i) => {
        output += `   ${i + 1}. ${rec}\n`;
      });
    }

    return output;
  }

  /**
   * 是否需要重新登录
   * @param {Object} error - 错误对象
   * @returns {boolean}
   */
  needsRelogin(error) {
    if (!error) return false;
    return [
      this.errorTypes.AUTH,
      this.errorTypes.COOKIE_EXPIRED,
      this.errorTypes.NOT_LOGGED_IN
    ].includes(error.type);
  }

  /**
   * 是否可重试
   * @param {Object} error - 错误对象
   * @returns {boolean}
   */
  isRetryable(error) {
    if (!error) return false;
    return [
      this.errorTypes.NETWORK,
      this.errorTypes.TIMEOUT,
      this.errorTypes.SERVER,
      this.errorTypes.SERVER_ERROR
    ].includes(error.type);
  }

  /**
   * 记录错误日志
   * @param {Object} error - 错误对象
   */
  _logError(error) {
    this.errorLog.push(error);
    
    // 限制日志大小
    if (this.errorLog.length > this.maxLogSize) {
      this.errorLog = this.errorLog.slice(-this.maxLogSize);
    }
  }

  /**
   * 获取错误日志
   * @param {number} limit - 限制数量
   * @returns {Array} 错误日志
   */
  getErrorLog(limit = 20) {
    return this.errorLog.slice(-limit);
  }

  /**
   * 清除错误日志
   */
  clearErrorLog() {
    this.errorLog = [];
  }

  /**
   * 获取错误统计
   * @returns {Object} 统计信息
   */
  getErrorStats() {
    const stats = {};
    
    this.errorLog.forEach(error => {
      const type = error.type;
      stats[type] = (stats[type] || 0) + 1;
    });
    
    return {
      total: this.errorLog.length,
      byType: stats,
      mostCommon: Object.entries(stats)
        .sort((a, b) => b[1] - a[1])[0]?.[0] || null
    };
  }

  /**
   * 注册自定义错误消息
   * @param {string} type - 错误类型
   * @param {string} message - 消息
   * @param {Array} recoveries - 恢复建议
   */
  registerError(type, message, recoveries = []) {
    const errorType = type.toLowerCase();
    this.errorTypes[type.toUpperCase()] = errorType;
    this.messages[errorType] = message;
    this.recoveries[errorType] = recoveries;
  }

  /**
   * 判断是否是特定类型的错误
   * @param {Object} error - 错误对象
   * @param {string} type - 错误类型
   * @returns {boolean}
   */
  isErrorType(error, type) {
    if (!error) return false;
    return error.type === this.errorTypes[type.toUpperCase()];
  }

  /**
   * 获取所有错误类型
   * @returns {Object} 错误类型映射
   */
  getErrorTypes() {
    return { ...this.errorTypes };
  }
}

module.exports = ErrorHandler;
