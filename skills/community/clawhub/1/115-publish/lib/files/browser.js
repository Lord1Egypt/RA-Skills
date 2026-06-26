const HttpClient = require('../client/http-client');

/**
 * 115 文件浏览 API
 * 
 * 功能：
 * - 文件列表获取
 * - 分页处理
 * - 文件详情查询
 * - 目录导航
 */
class FileBrowser {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.apiBase = 'https://webapi.115.com';
  }

  /**
   * 获取文件列表
   * @param {string} cid - 目录 ID（0 表示根目录）
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 文件列表
   */
  async listFiles(cid = '0', options = {}) {
    const {
      page = 1,
      size = 100,
      order = 'file_name',
      asc = 1,
      showDir = 1,
      star = 0,
      source = '',
      format = 'json'
    } = options;

    const response = await this.http.get('/files', {
      cid,
      offset: (page - 1) * size,
      show_dir: showDir,
      order,
      asc,
      limit: size,
      source,
      star,
      format,
      _: Date.now()
    });

    if (!response.state) {
      return {
        success: false,
        message: response.error || '获取文件列表失败',
        files: [],
        totalCount: 0,
        currentPage: page,
        pageSize: size,
        hasMore: false
      };
    }

    return {
      success: true,
      files: response.data || [],
      totalCount: response.count || 0,
      currentPage: page,
      pageSize: size,
      hasMore: (page * size) < (response.count || 0)
    };
  }

  /**
   * 获取文件详情
   * @param {string} fileId - 文件 ID
   * @returns {Promise<Object>} 文件详情
   */
  async getFileDetail(fileId) {
    const response = await this.http.get('/files/get_info', {
      file_id: fileId,
      _: Date.now()
    });

    if (!response.state) {
      return { success: false, message: response.error || '获取文件详情失败' };
    }

    return {
      success: true,
      file: response.data || {}
    };
  }

  /**
   * 获取目录路径（面包屑）
   * @param {string} cid - 目录 ID
   * @returns {Promise<Object>} 路径信息
   */
  async getDirectoryPath(cid) {
    const response = await this.http.get('/files/get_path', {
      cid,
      _: Date.now()
    });

    if (!response.state) {
      return { success: false, message: response.error || '获取目录路径失败' };
    }

    return {
      success: true,
      path: response.path || [],
      currentName: response.current_name || ''
    };
  }

  /**
   * 递归获取所有文件（支持大目录）
   * @param {string} cid - 目录 ID
   * @param {Object} options - 选项
   * @returns {Promise<Array>} 所有文件
   */
  async getAllFiles(cid = '0', options = {}) {
    const { recursive = false, onProgress = null } = options;
    const allFiles = [];
    let page = 1;
    const pageSize = 1000;

    // eslint-disable-next-line no-constant-condition
    while (true) {
      const result = await this.listFiles(cid, { page, size: pageSize });
      allFiles.push(...result.files);

      onProgress?.({
        processed: allFiles.length,
        total: result.totalCount,
        page
      });

      if (!result.hasMore) {
        break;
      }

      page++;
      await this.http.sleep(500); // 避免速率限制
    }

    // 递归获取子目录
    if (recursive) {
      const directories = allFiles.filter(f => f.is_dir || f.category === 'directory');
      
      for (const dir of directories) {
        const subFiles = await this.getAllFiles(dir.cid || dir.file_id, {
          recursive: true,
          onProgress
        });
        allFiles.push(...subFiles);
      }
    }

    return allFiles;
  }

  /**
   * 搜索文件
   * @param {string} keyword - 搜索关键词
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 搜索结果
   */
  async searchFiles(keyword, options = {}) {
    const {
      cid = '0',
      date = '',
      fileType = '',
      sizeRange = '',
      page = 1,
      size = 100
    } = options;

    const response = await this.http.get('/files/search', {
      aid: 1,
      cid,
      keyword,
      date,
      file_type: fileType,
      size_range: sizeRange,
      offset: (page - 1) * size,
      limit: size,
      _: Date.now()
    });

    if (!response.state) {
      return { success: false, message: response.error || '搜索失败', files: [], totalCount: 0 };
    }

    return {
      success: true,
      files: response.data || [],
      totalCount: response.count || 0,
      currentPage: page,
      hasMore: (page * size) < (response.count || 0)
    };
  }

  /**
   * 获取文件分类统计
   * @param {string} cid - 目录 ID
   * @returns {Promise<Object>} 分类统计
   */
  async getCategoryStats(cid = '0') {
    const response = await this.http.get('/files/category_stats', {
      cid,
      _: Date.now()
    });

    if (!response.state) {
      return { success: false, message: response.error || '获取分类统计失败', stats: null };
    }

    return {
      success: true,
      stats: response.data || {}
    };
  }

  /**
   * 获取星标文件
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 星标文件列表
   */
  async getStarredFiles(options = {}) {
    return this.listFiles('0', { ...options, star: 1 });
  }

  /**
   * 获取最近访问的文件
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 最近文件列表
   */
  async getRecentFiles(options = {}) {
    const { days = 7, limit = 100 } = options;
    
    const response = await this.http.get('/files/recent', {
      days,
      limit,
      _: Date.now()
    });

    if (!response.state) {
      return { success: false, message: response.error || '获取最近文件失败', files: [] };
    }

    return {
      success: true,
      files: response.data || []
    };
  }

  /**
   * 检查文件是否存在
   * @param {string} fileName - 文件名
   * @param {string} cid - 目录 ID
   * @returns {Promise<Object>} 检查结果
   */
  async checkFileExists(fileName, cid = '0') {
    const result = await this.listFiles(cid, { page: 1, size: 100 });
    
    const exists = result.files.some(f => f.file_name === fileName);
    
    return {
      success: true,
      exists,
      file: exists ? result.files.find(f => f.file_name === fileName) : null
    };
  }
}

module.exports = FileBrowser;
