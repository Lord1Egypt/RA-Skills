const FileBrowser = require('../files/browser');
const FileOperations = require('../files/operations');
const FileClassifier = require('./classifier');
const HttpClient = require('../client/http-client');
const { formatSize } = require('../utils/helpers');

/**
 * 智能整理模块
 * 
 * 功能：
 * - 自动按类型整理
 * - 按时间整理
 * - 重复文件检测
 * - AI 智能分类
 */
class SmartOrganizer {
  constructor(cookie) {
    this.http = new HttpClient(cookie);
    this.browser = new FileBrowser(cookie);
    this.operations = new FileOperations(cookie);
    this.classifier = new FileClassifier();
  }

  /**
   * 自动按类型整理
   * @param {string} sourceCid - 源目录 ID
   * @param {string} targetBase - 目标基础目录
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 整理结果
   */
  async autoOrganizeByType(sourceCid = '0', _targetBase = '/已整理', options = {}) {
    const { dryRun = false, onProgress = null } = options;

    // 1. 获取所有文件（分页处理）
    const allFiles = await this.browser.getAllFiles(sourceCid, { recursive: false, onProgress: null });
    
    // 2. 分类
    const classified = this.classifier.batchClassify(allFiles, 'type');

    // 3. 创建目标目录
    if (!dryRun) {
      for (const category of Object.keys(classified)) {
        try {
          await this.operations.createFolder(category, sourceCid);
        } catch (error) {
          // 目录可能已存在
        }
      }
    }

    // 4. 移动文件
    const results = {
      total: allFiles.length,
      moved: 0,
      failed: 0,
      skipped: 0,
      details: []
    };

    // 获取目录 ID 映射
    const dirMap = {};
    if (!dryRun) {
      const dirs = await this.browser.listFiles(sourceCid, { page: 1, size: 100 });
      dirs.files.filter(f => f.is_dir).forEach(dir => {
        dirMap[dir.file_name] = dir.file_id;
      });
    }

    for (const [category, categoryFiles] of Object.entries(classified)) {
      const targetCid = dirMap[category];
      
      for (const file of categoryFiles) {
        if (file.is_dir) {
          results.skipped++;
          continue;
        }

        try {
          if (!dryRun) {
            await this.operations.moveFiles(file.file_id, targetCid);
          }
          results.moved++;
          results.details.push({
            success: true,
            file: file.file_name,
            category
          });
        } catch (error) {
          results.failed++;
          results.details.push({
            success: false,
            file: file.file_name,
            error: error.message
          });
        }

        onProgress?.({
          processed: results.moved + results.failed + results.skipped,
          total: results.total
        });
      }
    }

    return results;
  }

  /**
   * 按时间整理
   * @param {string} sourceCid - 源目录 ID
   * @param {string} targetBase - 目标基础目录
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 整理结果
   */
  async autoOrganizeByTime(sourceCid = '0', _targetBase = '/按时间整理', options = {}) {
    const { dryRun = false, onProgress = null } = options;

    // 1. 获取文件列表
    const files = await this.browser.listFiles(sourceCid, { page: 1, size: 1000 });
    
    // 2. 按时间分类
    const classified = this.classifier.batchClassify(files.files, 'time');

    const results = {
      total: files.files.length,
      moved: 0,
      failed: 0,
      skipped: 0,
      details: []
    };

    // 缓存目录 ID 映射
    const dirMap = {};

    for (const [timeCategory, timeFiles] of Object.entries(classified)) {
      for (const file of timeFiles) {
        if (file.is_dir) {
          results.skipped++;
          continue;
        }

        try {
          if (!dryRun) {
            // 创建或获取年月目录
            if (!dirMap[timeCategory]) {
              const createResult = await this.operations.createFolder(timeCategory, sourceCid);
              dirMap[timeCategory] = createResult.folderId;
            }

            // 移动文件到对应目录
            await this.operations.moveFiles(file.file_id, dirMap[timeCategory]);
          }
          results.moved++;
          results.details.push({ success: true, file: file.file_name, category: timeCategory });
        } catch (error) {
          results.failed++;
          results.details.push({ success: false, file: file.file_name, error: error.message });
        }

        onProgress?.({
          processed: results.moved + results.failed + results.skipped,
          total: results.total
        });
      }
    }

    return results;
  }

  /**
   * 查找重复文件
   * @param {string} sourceCid - 目录 ID
   * @param {Object} options - 选项
   * @returns {Promise<Object>} 重复文件信息
   */
  async findDuplicates(sourceCid = '0', options = {}) {
    const { recursive = false, onProgress = null } = options;

    // 1. 获取所有文件（分页处理）
    const allFiles = await this.browser.getAllFiles(sourceCid, { recursive, onProgress });

    // 2. 按大小分组
    const sizeGroups = {};
    for (const file of allFiles) {
      if (file.is_dir) continue;
      
      const size = file.file_size || file.size || 0;
      if (!sizeGroups[size]) {
        sizeGroups[size] = [];
      }
      sizeGroups[size].push(file);
    }

    // 3. 找出可能的重复（大小相同）
    const duplicates = [];
    for (const [size, group] of Object.entries(sizeGroups)) {
      if (group.length > 1) {
        duplicates.push({
          size: parseInt(size),
          sizeFormatted: this.formatSize(parseInt(size)),
          count: group.length,
          files: group
        });
      }
    }

    // 4. 按重复数量排序
    duplicates.sort((a, b) => b.count - a.count);

    return {
      success: true,
      totalFiles: allFiles.length,
      duplicateGroups: duplicates.length,
      duplicates,
      potentialSavings: duplicates.reduce((sum, d) => sum + d.size * (d.count - 1), 0)
    };
  }

  /**
   * 获取清理建议
   * @param {string} sourceCid - 目录 ID
   * @returns {Promise<Object>} 清理建议
   */
  async getCleanupSuggestions(sourceCid = '0') {
    const suggestions = [];

    // 1. 获取容量信息
    const userInfo = await this.http.get('/user/info');
    const usageRate = userInfo.data?.used_capacity / userInfo.data?.capacity || 0;

    if (usageRate > 0.9) {
      suggestions.push({
        type: 'critical',
        title: '存储空间严重不足',
        message: `已使用 ${Math.round(usageRate * 100)}%，建议立即清理`,
        priority: 1
      });
    } else if (usageRate > 0.8) {
      suggestions.push({
        type: 'warning',
        title: '存储空间紧张',
        message: `已使用 ${Math.round(usageRate * 100)}%，建议清理`,
        priority: 2
      });
    }

    // 2. 查找大文件
    const files = await this.browser.listFiles(sourceCid, { page: 1, size: 1000 });
    const largeFiles = files.files.filter(f => (f.file_size || 0) > 500 * 1024 * 1024);
    
    if (largeFiles.length > 0) {
      suggestions.push({
        type: 'info',
        title: '发现大文件',
        message: `${largeFiles.length} 个文件大于 500MB`,
        files: largeFiles.slice(0, 10),
        priority: 3
      });
    }

    // 3. 查找重复文件
    const duplicates = await this.findDuplicates(sourceCid);
    if (duplicates.duplicateGroups > 0) {
      suggestions.push({
        type: 'info',
        title: '发现重复文件',
        message: `${duplicates.duplicateGroups} 组重复文件，可释放 ${this.formatSize(duplicates.potentialSavings)}`,
        priority: 4
      });
    }

    return {
      success: true,
      suggestions,
      storageUsage: {
        used: userInfo.data?.used_capacity || 0,
        total: userInfo.data?.capacity || 0,
        usageRate
      }
    };
  }
  /**
   * 格式化文件大小（使用工具函数）
   */
  formatSize(bytes) {
    return formatSize(bytes);
  }
}

module.exports = SmartOrganizer;
