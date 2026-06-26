/**
 * 压缩模块
 * 负责文件压缩和 ZIP 生成
 * v1.1.0 - 新增加密压缩支持
 */

const fs = require('fs-extra');
const path = require('path');
const os = require('os');
const archiver = require('archiver');
const archiverZipEncrypted = require('archiver-zip-encrypted');
const dayjs = require('dayjs');
const { info, warn, error, debug } = require('./logger');

// 注册加密格式
archiver.registerFormat('zip-encrypted', archiverZipEncrypted);

// OpenClaw 根目录
const OPENCLAW_ROOT = path.join(os.homedir(), '.openclaw');

/**
 * 创建压缩器实例
 */
class Compressor {
  constructor(config) {
    this.config = config;
  }

  /**
   * 压缩文件列表到 ZIP
   * @param {Array} files 文件列表 [{path, relativePath}, ...]
   * @param {Object} outputConfig 输出配置
   * @returns {Promise<string>} ZIP 文件路径
   */
  async compress(files, outputConfig) {
    return new Promise(async (resolve, reject) => {
      try {
        // 生成 ZIP 文件路径
        const zipPath = await this.generateZipPath(outputConfig);

        // 确保输出目录存在
        await fs.ensureDir(path.dirname(zipPath));

        // 判断是否启用加密
        const useEncryption = outputConfig.encryption?.enabled;
        const password = outputConfig.encryption?.password;

        // 选择压缩格式
        const archiveType = useEncryption ? 'zip-encrypted' : 'zip';
        const archiveOptions = useEncryption ? {
          zlib: { level: 9 }, // 最高压缩级别
          encryptionMethod: 'aes256',
          password: password
        } : {
          zlib: { level: 9 } // 最高压缩级别
        };

        // 创建写入流
        const output = fs.createWriteStream(zipPath);
        const archive = archiver(archiveType, archiveOptions);

        let filesAdded = 0;
        let filesSkipped = 0;
        const skippedFiles = [];

        output.on('close', async () => {
          const size = this.formatSize(archive.pointer());
          await info('Compressor', `压缩完成: ${path.basename(zipPath)} (${size})`);
          await info('Compressor', `文件统计: 添加 ${filesAdded} 个，跳过 ${filesSkipped} 个`);

          if (useEncryption) {
            await info('Compressor', '加密方式: AES-256');
          }

          if (skippedFiles.length > 0) {
            await warn('Compressor', `跳过的文件: ${skippedFiles.slice(0, 10).join(', ')}${skippedFiles.length > 10 ? '...' : ''}`);
          }

          resolve(zipPath);
        });

        archive.on('error', async (err) => {
          await error('Compressor', `压缩错误: ${err.message}`);
          reject(err);
        });

        archive.on('warning', async (err) => {
          if (err.code === 'ENOENT') {
            await warn('Compressor', `文件不存在: ${err.message}`);
          } else {
            await error('Compressor', `压缩警告: ${err.message}`);
          }
        });

        archive.pipe(output);

        // 添加文件到压缩包
        for (const file of files) {
          try {
            // 检查文件是否存在
            if (!(await fs.pathExists(file.path))) {
              filesSkipped++;
              skippedFiles.push(file.relativePath);
              continue;
            }

            // 检查文件是否可读
            try {
              await fs.access(file.path, fs.constants.R_OK);
            } catch (accessErr) {
              if (accessErr.code === 'EBUSY') {
                // 文件被占用，跳过
                filesSkipped++;
                skippedFiles.push(file.relativePath);
                await warn('Compressor', `跳过被占用的文件: ${file.relativePath}`);
                continue;
              }
              throw accessErr;
            }

            // 添加文件到压缩包
            archive.file(file.path, { name: file.relativePath });
            filesAdded++;
          } catch (err) {
            filesSkipped++;
            skippedFiles.push(file.relativePath);
            await warn('Compressor', `跳过文件 ${file.relativePath}: ${err.message}`);
          }
        }

        // 完成压缩
        await archive.finalize();
      } catch (err) {
        await error('Compressor', `压缩失败: ${err.message}`);
        reject(err);
      }
    });
  }

  /**
   * 生成 ZIP 文件路径
   */
  async generateZipPath(outputConfig) {
    const now = dayjs();
    const date = now.format('YYYYMMDD');
    const time = now.format('HHmm');
    
    // 获取 OpenClaw 版本
    const version = await this.getOpenClawVersion();
    
    // 获取当日序号
    const sequence = await this.getNextSequence(date, outputConfig.path);
    
    // 构建文件名
    const parts = [outputConfig.naming.prefix, date, time];
    
    if (outputConfig.naming.includeVersion) {
      parts.push(version);
    }
    
    if (outputConfig.naming.includeSequence) {
      parts.push(sequence);
    }
    
    const filename = parts.join('_') + '.zip';
    
    return path.join(outputConfig.path, filename);
  }

  /**
   * 获取 OpenClaw 版本
   */
  async getOpenClawVersion() {
    try {
      // 尝试从 package.json 获取版本
      const packagePath = path.join(
        process.env.APPDATA || path.join(os.homedir(), '.config'),
        'npm/node_modules/openclaw/package.json'
      );
      
      if (await fs.pathExists(packagePath)) {
        const pkg = await fs.readJson(packagePath);
        return `v${pkg.version}`;
      }
      
      // 备用：从命令行获取
      // 这里使用默认版本
      return 'v2026.3.23-2';
    } catch (err) {
      return 'v2026.3.23-2';
    }
  }

  /**
   * 获取当日备份序号
   */
  async getNextSequence(date, outputPath) {
    try {
      await fs.ensureDir(outputPath);
      
      // 获取目录下所有备份文件
      const files = await fs.readdir(outputPath);
      
      // 过滤出当天的备份文件
      const todayBackups = files.filter(f => 
        f.includes(`_${date}_`) && f.endsWith('.zip')
      );
      
      // 序号从 01 开始
      const nextSequence = todayBackups.length + 1;
      
      return String(nextSequence).padStart(2, '0');
    } catch (err) {
      return '01';
    }
  }

  /**
   * 格式化文件大小
   */
  formatSize(bytes) {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
    if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
    return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
  }

  /**
   * 压缩目录
   * @param {string} dirPath 目录路径
   * @param {string} outputPath 输出路径
   * @param {Object} options 选项
   */
  async compressDirectory(dirPath, outputPath, options = {}) {
    const files = await this.collectFiles(dirPath, options.exclude || [], options.excludePatterns || []);
    
    // 转换为相对路径
    const filesWithRelativePath = files.map(filePath => ({
      path: filePath,
      relativePath: path.relative(path.dirname(dirPath), filePath)
    }));
    
    return this.compress(filesWithRelativePath, { path: outputPath, naming: options.naming || {} });
  }

  /**
   * 收集目录下的所有文件
   */
  async collectFiles(dirPath, excludeDirs = [], excludePatterns = []) {
    const files = [];
    
    async function walk(currentPath) {
      try {
        const entries = await fs.readdir(currentPath, { withFileTypes: true });
        
        for (const entry of entries) {
          const fullPath = path.join(currentPath, entry.name);
          
          // 检查是否在排除目录中
          if (excludeDirs.includes(entry.name)) {
            continue;
          }
          
          // 检查是否匹配排除模式
          if (excludePatterns.some(pattern => matchPattern(entry.name, pattern))) {
            continue;
          }
          
          if (entry.isDirectory()) {
            await walk(fullPath);
          } else if (entry.isFile()) {
            files.push(fullPath);
          }
        }
      } catch (err) {
        // 忽略无法访问的目录
      }
    }
    
    await walk(dirPath);
    return files;
  }
}

/**
 * 简单的模式匹配
 */
function matchPattern(filename, pattern) {
  // 将通配符模式转换为正则表达式
  const regex = new RegExp('^' + pattern
    .replace(/\./g, '\\.')
    .replace(/\*/g, '.*')
    .replace(/\?/g, '.') + '$');
  
  return regex.test(filename);
}

module.exports = { Compressor, matchPattern };