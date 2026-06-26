// file-organizer 文件整理器
const fs = require('fs');
const path = require('path');

// 文件类型分类
const FILE_TYPES = {
  images: ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg', '.ico', '.tiff'],
  documents: ['.doc', '.docx', '.pdf', '.txt', '.md', '.xls', '.xlsx', '.ppt', '.pptx', '.odt', '.rtf'],
  code: ['.js', '.ts', '.jsx', '.tsx', '.py', '.java', '.cpp', '.c', '.h', '.html', '.css', '.scss', '.json', '.xml', '.yaml', '.yml', '.go', '.rs', '.php', '.rb', '.swift', '.kt'],
  videos: ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.mkv', '.webm', '.m4v'],
  audio: ['.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'],
  archives: ['.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz']
};

// 获取文件类型
function getFileType(ext) {
  ext = ext.toLowerCase();
  for (const [type, extensions] of Object.entries(FILE_TYPES)) {
    if (extensions.includes(ext)) {
      return type;
    }
  }
  return 'others';
}

// 扫描目录
function scanDirectory(dirPath) {
  const results = {
    files: [],
    folders: [],
    totalSize: 0
  };
  
  try {
    const items = fs.readdirSync(dirPath);
    
    for (const item of items) {
      const fullPath = path.join(dirPath, item);
      try {
        const stats = fs.statSync(fullPath);
        
        if (stats.isDirectory()) {
          results.folders.push({
            name: item,
            path: fullPath,
            size: 0
          });
        } else {
          const ext = path.extname(item);
          results.files.push({
            name: item,
            path: fullPath,
            ext: ext,
            type: getFileType(ext),
            size: stats.size,
            modified: stats.mtime
          });
          results.totalSize += stats.size;
        }
      } catch (e) {
        // 跳过无法访问的文件
      }
    }
  } catch (e) {
    return null;
  }
  
  return results;
}

// 整理文件
function organizeFiles(files, targetDir) {
  const results = {
    moved: [],
    errors: []
  };
  
  // 创建分类目录
  const categories = [...new Set(files.map(f => f.type))];
  
  for (const category of categories) {
    const categoryDir = path.join(targetDir, category);
    if (!fs.existsSync(categoryDir)) {
      fs.mkdirSync(categoryDir, { recursive: true });
    }
  }
  
  // 移动文件
  for (const file of files) {
    try {
      const targetPath = path.join(targetDir, file.type, file.name);
      
      // 如果目标文件已存在，添加数字后缀
      let finalPath = targetPath;
      let counter = 1;
      while (fs.existsSync(finalPath)) {
        const nameWithoutExt = path.basename(file.name, file.ext);
        finalPath = path.join(targetDir, file.type, `${nameWithoutExt}_${counter}${file.ext}`);
        counter++;
      }
      
      fs.renameSync(file.path, finalPath);
      results.moved.push({
        from: file.path,
        to: finalPath,
        type: file.type
      });
    } catch (e) {
      results.errors.push({
        file: file.path,
        error: e.message
      });
    }
  }
  
  return results;
}

// 生成统计报告
function generateReport(scanResults) {
  const typeStats = {};
  
  for (const file of scanResults.files) {
    if (!typeStats[file.type]) {
      typeStats[file.type] = { count: 0, size: 0 };
    }
    typeStats[file.type].count++;
    typeStats[file.type].size += file.size;
  }
  
  return typeStats;
}

// 格式化文件大小
function formatSize(bytes) {
  if (bytes === 0) return '0 B';
  const k = 1024;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

module.exports = {
  name: 'file-organizer',
  description: '文件整理器，按类型自动分类',
  version: '1.0.0',
  author: '黄豆豆',
  
  // 激活条件
  activate(message) {
    const keywords = ['整理', '分类'];
    return keywords.some(k => message.includes(k));
  },
  
  async handle(context) {
    const message = context.message || '';
    const lowerMessage = message.toLowerCase();
    
    // 解析目标路径
    let targetPath = null;
    
    // 常见路径快捷方式
    if (lowerMessage.includes('桌面')) {
      targetPath = path.join(process.env.USERPROFILE || '', 'Desktop');
    } else if (lowerMessage.includes('下载')) {
      targetPath = path.join(process.env.USERPROFILE || '', 'Downloads');
    } else if (lowerMessage.includes('文档')) {
      targetPath = path.join(process.env.USERPROFILE || '', 'Documents');
    } else {
      // 尝试提取路径
      const pathMatch = message.match(/[A-Za-z]:\\[^:*?"<>|\r\n]+/);
      if (pathMatch) {
        targetPath = pathMatch[0];
      }
    }
    
    if (!targetPath) {
      return {
        message: `📁 文件整理器

请指定要整理的文件夹：
- 整理桌面
- 整理下载
- 整理 D:\\Downloads

文件将按类型自动分类到以下文件夹：
📷 images - 图片
📄 documents - 文档
💻 code - 代码
🎬 videos - 视频
🎵 audio - 音频
📦 archives - 压缩包
📁 others - 其他`
      };
    }
    
    // 检查路径是否存在
    if (!fs.existsSync(targetPath)) {
      return { message: `❌ 路径不存在：${targetPath}` };
    }
    
    // 扫描目录
    const scanResults = scanDirectory(targetPath);
    
    if (!scanResults) {
      return { message: `❌ 无法访问路径：${targetPath}` };
    }
    
    if (scanResults.files.length === 0) {
      return { message: `📂 该文件夹为空：${targetPath}` };
    }
    
    // 如果只是查询，显示统计信息
    if (lowerMessage.includes('统计') || lowerMessage.includes('查看')) {
      const stats = generateReport(scanResults);
      let msg = `📊 文件统计：${targetPath}\n\n`;
      msg += `总文件数：${scanResults.files.length}\n`;
      msg += `总大小：${formatSize(scanResults.totalSize)}\n\n`;
      
      for (const [type, data] of Object.entries(stats)) {
        const emoji = {
          images: '📷', documents: '📄', code: '💻',
          videos: '🎬', audio: '🎵', archives: '📦', others: '📁'
        }[type] || '📄';
        msg += `${emoji} ${type}: ${data.count} 个 (${formatSize(data.size)})\n`;
      }
      
      return { message: msg };
    }
    
    // 执行整理
    const organizeResults = organizeFiles(scanResults.files, targetPath);
    
    let msg = `✅ 整理完成！\n\n`;
    msg += `📁 目录：${targetPath}\n`;
    msg += `📊 总文件数：${scanResults.files.length}\n`;
    msg += `✅ 已移动：${organizeResults.moved.length} 个\n`;
    
    if (organizeResults.errors.length > 0) {
      msg += `❌ 错误：${organizeResults.errors.length} 个\n`;
    }
    
    msg += `\n📂 分类结果：\n`;
    const typeCount = {};
    for (const moved of organizeResults.moved) {
      typeCount[moved.type] = (typeCount[moved.type] || 0) + 1;
    }
    for (const [type, count] of Object.entries(typeCount)) {
      const emoji = {
        images: '📷', documents: '📄', code: '💻',
        videos: '🎬', audio: '🎵', archives: '📦', others: '📁'
      }[type] || '📄';
      msg += `  ${emoji} ${type}: ${count} 个\n`;
    }
    
    return { message: msg };
  }
};
