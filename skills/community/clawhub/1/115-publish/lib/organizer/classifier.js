const path = require('path');

/**
 * 文件分类器
 * 
 * 功能：
 * - 按文件类型分类
 * - 按时间分类
 * - 按大小分类
 */
class FileClassifier {
  constructor() {
    // 文件类型分类规则
    this.categories = {
      '📷 图片': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff'],
      '🎬 视频': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.rmvb', '.rm'],
      '🎵 音乐': ['.mp3', '.flac', '.wav', '.aac', '.ogg', '.wma', '.m4a'],
      '📄 文档': ['.pdf', '.doc', '.docx', '.xls', '.xlsx', '.ppt', '.pptx', '.txt', '.md'],
      '📦 压缩包': ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'],
      '💻 代码': ['.js', '.ts', '.py', '.java', '.go', '.cpp', '.c', '.h', '.html', '.css', '.php', '.rb'],
      '📱 应用': ['.apk', '.exe', '.dmg', '.pkg', '.deb', '.rpm'],
      '📚 书籍': ['.epub', '.mobi', '.azw', '.azw3', '.fb2'],
      '🎮 游戏': ['.iso', '.gho', '.img'],
      '📊 数据': ['.csv', '.json', '.xml', '.sql', '.db']
    };
  }

  /**
   * 根据文件类型分类
   * @param {string} fileName - 文件名
   * @returns {string} 分类名称
   */
  classifyByType(fileName) {
    const ext = path.extname(fileName).toLowerCase();
    
    for (const [category, extensions] of Object.entries(this.categories)) {
      if (extensions.includes(ext)) {
        return category;
      }
    }

    return '📁 其他';
  }

  /**
   * 根据时间分类（按年月）
   * @param {number} timestamp - 时间戳
   * @returns {string} 分类名称（格式：2026/03-三月）
   */
  classifyByTime(timestamp) {
    const date = new Date(timestamp);
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const monthNames = ['一月', '二月', '三月', '四月', '五月', '六月', '七月', '八月', '九月', '十月', '十一月', '十二月'];
    const monthName = monthNames[date.getMonth()];

    return `${year}/${month}-${monthName}`;
  }

  /**
   * 根据文件大小分类
   * @param {number} bytes - 文件大小（字节）
   * @returns {string} 分类名称
   */
  classifyBySize(bytes) {
    const KB = 1024;
    const MB = KB * 1024;
    const GB = MB * 1024;

    if (bytes < KB) {
      return '🐜 小于 1KB';
    } else if (bytes < 100 * KB) {
      return '📝 小文件 (<100KB)';
    } else if (bytes < MB) {
      return '📄 普通文件 (<1MB)';
    } else if (bytes < 100 * MB) {
      return '📦 中等文件 (<100MB)';
    } else if (bytes < GB) {
      return '🎬 大文件 (<1GB)';
    } else if (bytes < 10 * GB) {
      return '🎥 超大文件 (<10GB)';
    } else {
      return '💾 巨型文件 (>10GB)';
    }
  }

  /**
   * 批量分类
   * @param {Array<Object>} files - 文件数组
   * @param {string} by - 分类依据（type/time/size）
   * @returns {Object} 分类结果
   */
  batchClassify(files, by = 'type') {
    const result = {};

    for (const file of files) {
      let category;

      switch (by) {
        case 'type': {
          category = this.classifyByType(file.file_name || file.name);
          break;
        }
        case 'time': {
          const timestamp = file.upload_time || file.create_time || Date.now();
          category = this.classifyByTime(timestamp);
          break;
        }
        case 'size': {
          category = this.classifyBySize(file.file_size || file.size || 0);
          break;
        }
        default: {
          category = '未知';
        }
      }

      if (!result[category]) {
        result[category] = [];
      }
      result[category].push(file);
    }

    return result;
  }

  /**
   * 获取分类统计
   * @param {Array<Object>} files - 文件数组
   * @returns {Object} 统计信息
   */
  getStats(files) {
    const byType = this.batchClassify(files, 'type');
    
    const stats = {
      total: files.length,
      byCategory: {},
      totalSize: 0
    };

    for (const [category, categoryFiles] of Object.entries(byType)) {
      stats.byCategory[category] = {
        count: categoryFiles.length,
        size: categoryFiles.reduce((sum, f) => sum + (f.file_size || f.size || 0), 0)
      };
      stats.totalSize += stats.byCategory[category].size;
    }

    return stats;
  }
}

module.exports = FileClassifier;
