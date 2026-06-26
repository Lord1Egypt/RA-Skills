/**
 * Dreaming Guard Pro - Archiver Module
 * 
 * 智能归档策略，三级归档系统
 * hot(最近7天) → warm(7-30天) → cold(30天以上)
 * 纯Node.js实现，使用内置zlib进行gzip压缩
 */

const fs = require('fs');
const path = require('path');
const zlib = require('zlib');
const os = require('os');

// 默认配置
const DEFAULT_CONFIG = {
  archivePath: path.join(os.homedir(), '.openclaw', 'archive', 'dreaming'),
  compression: 'gzip',
  retention: {
    hot: 7,      // 保留最近7天在dreaming目录
    warm: 30,    // 7-30天的归档在warm区
    cold: 90     // 30天以上归档在cold区（之后可清理）
  },
  maxArchiveSize: 50 * 1024 * 1024, // 单个归档最大50MB
  indexFile: 'index.json'
};

/**
 * 归档层级
 */
const ARCHIVE_LEVELS = {
  HOT: 'hot',    // 最近数据，快速访问
  WARM: 'warm',  // 中期数据，压缩存储
  COLD: 'cold'   // 历史数据，深度压缩
};

/**
 * Archiver类 - 归档器
 */
class Archiver {
  constructor(options = {}) {
    // 合并配置
    this.config = { ...DEFAULT_CONFIG, ...options };
    
    // 确保归档目录存在
    this._ensureArchiveDirs();
    
    // 绑定日志器
    this.logger = options.logger || {
      debug: (...args) => console.debug('[Archiver]', ...args),
      info: (...args) => console.info('[Archiver]', ...args),
      warn: (...args) => console.warn('[Archiver]', ...args),
      error: (...args) => console.error('[Archiver]', ...args)
    };
    
    // 加载归档索引
    this.index = this._loadIndex();
  }

  /**
   * 确保归档目录结构存在
   */
  _ensureArchiveDirs() {
    const dirs = ['hot', 'warm', 'cold'];
    for (const level of dirs) {
      const dir = path.join(this.config.archivePath, level);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    }
  }

  /**
   * 加载归档索引
   * @returns {object} 索引数据
   */
  _loadIndex() {
    const indexPath = path.join(this.config.archivePath, this.config.indexFile);
    
    if (fs.existsSync(indexPath)) {
      try {
        return JSON.parse(fs.readFileSync(indexPath, 'utf-8'));
      } catch (err) {
        this.logger.warn('Failed to load index, creating new one:', err.message);
      }
    }
    
    return {
      version: '1.0.0',
      archives: [],
      lastUpdate: null
    };
  }

  /**
   * 保存归档索引
   */
  _saveIndex() {
    const indexPath = path.join(this.config.archivePath, this.config.indexFile);
    this.index.lastUpdate = Date.now();
    
    // 原子写入
    const tempPath = indexPath + '.tmp';
    fs.writeFileSync(tempPath, JSON.stringify(this.index, null, 2));
    fs.renameSync(tempPath, indexPath);
  }

  /**
   * 执行归档
   * @param {object} options - 归档选项
   * @returns {Promise<object>} 归档结果
   */
  async archive(options = {}) {
    const sourcePath = options.sourcePath || this._detectSourcePath();
    const dryRun = options.dryRun || false;
    const forceLevel = options.level || null; // 强制指定归档层级
    
    this.logger.info('Starting archive', { sourcePath, dryRun });
    
    // 检查源路径
    if (!fs.existsSync(sourcePath)) {
      throw new Error(`Source path does not exist: ${sourcePath}`);
    }
    
    // 扫描需要归档的文件
    const filesToArchive = this._scanFilesToArchive(sourcePath, forceLevel);
    
    if (filesToArchive.length === 0) {
      this.logger.info('No files to archive');
      return {
        archived: [],
        totalSaved: 0,
        skipped: true,
        reason: 'No files match archive criteria'
      };
    }
    
    // 按归档层级分组
    const grouped = this._groupFilesByLevel(filesToArchive, sourcePath);
    
    // 执行归档
    const results = {
      archived: [],
      totalSaved: 0,
      totalFiles: 0,
      indexFile: null,
      dryRun
    };
    
    for (const [level, files] of Object.entries(grouped)) {
      if (files.length === 0) continue;
      
      const archiveName = this._generateArchiveName(level);
      const levelPath = path.join(this.config.archivePath, level);
      const archivePath = path.join(levelPath, archiveName);
      
      if (!dryRun) {
        // 实际归档
        const archiveResult = await this._createArchive(files, archivePath, sourcePath);
        results.archived.push(archiveResult);
        results.totalSaved += archiveResult.saved;
        results.totalFiles += archiveResult.files.length;
        
        // 更新索引
        this.index.archives.push({
          name: archiveName,
          level,
          path: archivePath,
          createdAt: Date.now(),
          files: archiveResult.files.map(f => ({
            original: f.relativePath,
            size: f.size,
            compressedSize: f.compressedSize
          })),
          originalSize: archiveResult.originalSize,
          compressedSize: archiveResult.compressedSize
        });
      } else {
        // 试运行，只计算预估
        const estimated = this._estimateArchive(files);
        results.archived.push({
          level,
          archiveName,
          estimatedSize: estimated.totalSize,
          estimatedCompressedSize: estimated.compressedSize,
          files: files.length,
          dryRun: true
        });
        results.totalFiles += files.length;
      }
    }
    
    // 保存索引
    if (!dryRun) {
      this._saveIndex();
      results.indexFile = path.join(this.config.archivePath, this.config.indexFile);
    }
    
    this.logger.info('Archive completed', { 
      totalFiles: results.totalFiles, 
      totalSaved: results.totalSaved 
    });
    
    return results;
  }

  /**
   * 自动检测源路径
   * @returns {string} 源路径
   */
  _detectSourcePath() {
    const homeDir = os.homedir();
    const defaultPath = path.join(homeDir, '.openclaw', 'workspace', 'memory', '.dreams');
    
    if (fs.existsSync(defaultPath)) {
      return defaultPath;
    }
    
    // 尝试查找其他workspace
    const openclawDir = path.join(homeDir, '.openclaw');
    if (fs.existsSync(openclawDir)) {
      const dirs = fs.readdirSync(openclawDir).filter(d => d.startsWith('workspace'));
      for (const dir of dirs) {
        const dreamPath = path.join(openclawDir, dir, 'memory', '.dreams');
        if (fs.existsSync(dreamPath)) {
          return dreamPath;
        }
      }
    }
    
    return defaultPath;
  }

  /**
   * 扫描需要归档的文件
   * @param {string} sourcePath - 源路径
   * @param {string} forceLevel - 强制层级
   * @returns {array} 文件列表
   */
  _scanFilesToArchive(sourcePath, forceLevel) {
    const files = [];
    const now = Date.now();
    const retention = this.config.retention;
    
    const scanDir = (dir) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        
        if (entry.isDirectory()) {
          scanDir(fullPath);
        } else if (entry.isFile() && (entry.name.endsWith('.json') || entry.name.endsWith('.jsonl'))) {
          try {
            const stats = fs.statSync(fullPath);
            const ageDays = (now - stats.mtimeMs) / (24 * 60 * 60 * 1000);
            
            // 确定归档层级
            let level = null;
            if (forceLevel) {
              level = forceLevel;
            } else if (ageDays < retention.hot) {
              // 保留在hot（dreaming目录），不归档
              continue;
            } else if (ageDays < retention.warm) {
              level = ARCHIVE_LEVELS.WARM;
            } else {
              level = ARCHIVE_LEVELS.COLD;
            }
            
            files.push({
              fullPath,
              relativePath: path.relative(sourcePath, fullPath),
              name: entry.name,
              size: stats.size,
              modified: stats.mtimeMs,
              ageDays,
              level
            });
          } catch (err) {
            this.logger.debug('Failed to stat file:', fullPath);
          }
        }
      }
    };
    
    scanDir(sourcePath);
    
    return files;
  }

  /**
   * 按归档层级分组文件
   * @param {array} files - 文件列表
   * @param {string} sourcePath - 源路径
   * @returns {object} 分组结果
   */
  _groupFilesByLevel(files, sourcePath) {
    const grouped = {
      [ARCHIVE_LEVELS.WARM]: [],
      [ARCHIVE_LEVELS.COLD]: []
    };
    
    for (const file of files) {
      if (file.level && grouped[file.level]) {
        grouped[file.level].push(file);
      }
    }
    
    return grouped;
  }

  /**
   * 生成归档文件名
   * @param {string} level - 归档层级
   * @returns {string} 归档文件名
   */
  _generateArchiveName(level) {
    const date = new Date().toISOString().slice(0, 10);
    const timestamp = Date.now();
    return `dreams-${date}-${timestamp}-${level}.tar.gz`;
  }

  /**
   * 创建归档
   * @param {array} files - 文件列表
   * @param {string} archivePath - 归档路径
   * @param {string} sourcePath - 源路径
   * @returns {Promise<object>} 归档结果
   */
  async _createArchive(files, archivePath, sourcePath) {
    const result = {
      archivePath,
      files: [],
      originalSize: 0,
      compressedSize: 0,
      saved: 0
    };
    
    // 创建临时目录存放要归档的文件
    const tempDir = path.join(this.config.archivePath, 'temp-' + Date.now());
    fs.mkdirSync(tempDir, { recursive: true });
    
    try {
      // 复制文件到临时目录（保持相对路径结构）
      for (const file of files) {
        const targetPath = path.join(tempDir, file.relativePath);
        const targetDir = path.dirname(targetPath);
        
        if (!fs.existsSync(targetDir)) {
          fs.mkdirSync(targetDir, { recursive: true });
        }
        
        fs.copyFileSync(file.fullPath, targetPath);
        
        // 压缩单个文件
        const compressedPath = targetPath + '.gz';
        await this._compressFile(targetPath, compressedPath);
        
        const compressedStats = fs.statSync(compressedPath);
        
        result.files.push({
          ...file,
          compressedSize: compressedStats.size,
          compressedPath
        });
        
        result.originalSize += file.size;
        result.compressedSize += compressedStats.size;
        result.saved += file.size - compressedStats.size;
        
        // 删除原临时文件，保留压缩文件
        fs.unlinkSync(targetPath);
      }
      
      // 创建归档manifest
      const manifest = {
        createdAt: Date.now(),
        sourcePath,
        files: result.files.map(f => ({
          path: f.relativePath,
          originalSize: f.size,
          compressedSize: f.compressedSize,
          modified: f.modified
        }))
      };
      
      const manifestPath = path.join(tempDir, 'manifest.json');
      fs.writeFileSync(manifestPath, JSON.stringify(manifest, null, 2));
      
      // 将所有压缩文件打包成一个tar.gz（简化版：直接合并）
      // 这里我们用更简单的方式：将所有.gz文件合并成一个归档目录
      // 然后压缩整个目录
      
      // 创建最终归档目录
      const finalArchiveDir = archivePath.replace('.tar.gz', '');
      fs.mkdirSync(finalArchiveDir, { recursive: true });
      
      // 移动压缩文件到最终目录
      for (const file of result.files) {
        const finalPath = path.join(finalArchiveDir, file.relativePath + '.gz');
        const finalDir = path.dirname(finalPath);
        if (!fs.existsSync(finalDir)) {
          fs.mkdirSync(finalDir, { recursive: true });
        }
        fs.renameSync(file.compressedPath, finalPath);
        file.finalPath = finalPath;
      }
      
      // 移动manifest
      const finalManifestPath = path.join(finalArchiveDir, 'manifest.json');
      fs.renameSync(manifestPath, finalManifestPath);
      
      // 清理临时目录
      fs.rmSync(tempDir, { recursive: true, force: true });
      
      result.archivePath = finalArchiveDir;
      
    } catch (err) {
      // 清理临时目录
      if (fs.existsSync(tempDir)) {
        fs.rmSync(tempDir, { recursive: true, force: true });
      }
      throw err;
    }
    
    return result;
  }

  /**
   * 压缩单个文件
   * @param {string} source - 源文件
   * @param {string} target - 目标文件
   * @returns {Promise<void>}
   */
  async _compressFile(source, target) {
    return new Promise((resolve, reject) => {
      const gzip = zlib.createGzip();
      const input = fs.createReadStream(source);
      const output = fs.createWriteStream(target);
      
      input.pipe(gzip).pipe(output);
      
      output.on('finish', resolve);
      output.on('error', reject);
      input.on('error', reject);
    });
  }

  /**
   * 预估归档大小
   * @param {array} files - 文件列表
   * @returns {object} 预估结果
   */
  _estimateArchive(files) {
    const totalSize = files.reduce((sum, f) => sum + f.size, 0);
    // gzip通常能压缩到30-50%大小
    const estimatedRatio = 0.4;
    const compressedSize = Math.floor(totalSize * estimatedRatio);
    
    return { totalSize, compressedSize };
  }

  /**
   * 列出所有归档
   * @returns {Promise<array>} 归档列表
   */
  async listArchives() {
    const archives = [];
    const levels = ['hot', 'warm', 'cold'];
    
    for (const level of levels) {
      const levelPath = path.join(this.config.archivePath, level);
      
      if (!fs.existsSync(levelPath)) continue;
      
      const entries = fs.readdirSync(levelPath, { withFileTypes: true });
      
      for (const entry of entries) {
        if (entry.isDirectory() && entry.name.startsWith('dreams-')) {
          const fullPath = path.join(levelPath, entry.name);
          
          try {
            // 加载manifest
            const manifestPath = path.join(fullPath, 'manifest.json');
            let manifest = null;
            if (fs.existsSync(manifestPath)) {
              manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
            }
            
            // 计算归档大小
            const size = this._calculateDirSize(fullPath);
            
            archives.push({
              name: entry.name,
              level,
              path: fullPath,
              size,
              createdAt: manifest?.createdAt || null,
              files: manifest?.files?.length || 0,
              manifest
            });
          } catch (err) {
            archives.push({
              name: entry.name,
              level,
              path: fullPath,
              error: err.message
            });
          }
        }
      }
    }
    
    return archives;
  }

  /**
   * 计算目录大小
   * @param {string} dir - 目录路径
   * @returns {number} 总大小
   */
  _calculateDirSize(dir) {
    let totalSize = 0;
    
    const scan = (d) => {
      const entries = fs.readdirSync(d, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(d, entry.name);
        if (entry.isDirectory()) {
          scan(fullPath);
        } else if (entry.isFile()) {
          totalSize += fs.statSync(fullPath).size;
        }
      }
    };
    
    scan(dir);
    return totalSize;
  }

  /**
   * 恢复归档
   * @param {object} checkpoint - 检查点（归档信息）
   * @param {string} targetPath - 目标路径
   * @returns {Promise<object>} 恢复结果
   */
  async restore(checkpoint, targetPath = null) {
    const archivePath = checkpoint.path || checkpoint.archivePath;
    
    if (!archivePath || !fs.existsSync(archivePath)) {
      throw new Error(`Archive not found: ${archivePath}`);
    }
    
    const restorePath = targetPath || this._detectSourcePath();
    
    this.logger.info('Restoring archive', { archivePath, restorePath });
    
    // 加载manifest
    const manifestPath = path.join(archivePath, 'manifest.json');
    if (!fs.existsSync(manifestPath)) {
      throw new Error('Archive manifest not found');
    }
    
    const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
    
    // 确保目标目录存在
    if (!fs.existsSync(restorePath)) {
      fs.mkdirSync(restorePath, { recursive: true });
    }
    
    const result = {
      restored: [],
      failed: [],
      totalRestored: 0
    };
    
    // 解压并恢复文件
    for (const fileInfo of manifest.files) {
      try {
        const compressedPath = path.join(archivePath, fileInfo.path + '.gz');
        const targetFile = path.join(restorePath, fileInfo.path);
        const targetDir = path.dirname(targetFile);
        
        if (!fs.existsSync(targetDir)) {
          fs.mkdirSync(targetDir, { recursive: true });
        }
        
        // 解压
        await this._decompressFile(compressedPath, targetFile);
        
        result.restored.push({
          path: fileInfo.path,
          size: fileInfo.originalSize,
          restoredTo: targetFile
        });
        result.totalRestored++;
        
      } catch (err) {
        result.failed.push({
          path: fileInfo.path,
          error: err.message
        });
      }
    }
    
    this.logger.info('Restore completed', { 
      totalRestored: result.totalRestored, 
      failed: result.failed.length 
    });
    
    return result;
  }

  /**
   * 解压单个文件
   * @param {string} source - 压缩文件
   * @param {string} target - 目标文件
   * @returns {Promise<void>}
   */
  async _decompressFile(source, target) {
    return new Promise((resolve, reject) => {
      const gunzip = zlib.createGunzip();
      const input = fs.createReadStream(source);
      const output = fs.createWriteStream(target);
      
      input.pipe(gunzip).pipe(output);
      
      output.on('finish', resolve);
      output.on('error', reject);
      input.on('error', reject);
    });
  }

  /**
   * 清理过期归档
   * @returns {Promise<object>} 清理结果
   */
  async cleanup() {
    const result = {
      removed: [],
      totalSaved: 0
    };
    
    const now = Date.now();
    const retention = this.config.retention;
    
    // 清理cold区的过期归档（超过cold天数）
    const coldPath = path.join(this.config.archivePath, 'cold');
    
    if (fs.existsSync(coldPath)) {
      const archives = fs.readdirSync(coldPath, { withFileTypes: true });
      
      for (const archive of archives) {
        if (archive.isDirectory() && archive.name.startsWith('dreams-')) {
          const fullPath = path.join(coldPath, archive.name);
          const manifestPath = path.join(fullPath, 'manifest.json');
          
          if (fs.existsSync(manifestPath)) {
            const manifest = JSON.parse(fs.readFileSync(manifestPath, 'utf-8'));
            const ageDays = (now - manifest.createdAt) / (24 * 60 * 60 * 1000);
            
            if (ageDays > retention.cold) {
              // 删除过期归档
              const size = this._calculateDirSize(fullPath);
              fs.rmSync(fullPath, { recursive: true, force: true });
              
              result.removed.push({
                name: archive.name,
                ageDays,
                size
              });
              result.totalSaved += size;
              
              // 从索引中移除
              this.index.archives = this.index.archives.filter(
                a => a.path !== fullPath
              );
            }
          }
        }
      }
    }
    
    // 更新索引
    if (result.removed.length > 0) {
      this._saveIndex();
    }
    
    this.logger.info('Cleanup completed', { removed: result.removed.length });
    
    return result;
  }
}

module.exports = Archiver;