#!/usr/bin/env node
/**
 * 写入域隔离管理器 v7.0
 * 
 * 核心职责：为每个并发 Agent 分配独立的写入域，防止数据污染
 * 
 * 第一性原理：
 * - 数据污染根源 = 多个写入者同时修改同一状态
 * - 解决方案 = 写入域隔离 + 边界验证
 */

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

class WriteDomainIsolator {
  constructor(config = {}) {
    this.baseDir = config.baseDir || '/tmp/agile-workflow-isolated';
    this.domains = new Map(); // taskId → domainInfo
    this.metadata = {
      createdAt: Date.now(),
      totalDomains: 0,
      activeDomains: 0
    };
    
    this.ensureBaseDir();
    this.saveMetadata();
  }

  /**
   * 确保基础目录存在
   */
  ensureBaseDir() {
    if (!fs.existsSync(this.baseDir)) {
      fs.mkdirSync(this.baseDir, { recursive: true });
    }
  }

  /**
   * 为任务创建隔离域
   * @param {string} taskId - 任务唯一标识
   * @param {object} options - 配置选项
   * @returns {string} 域路径
   */
  createDomain(taskId, options = {}) {
    if (this.domains.has(taskId)) {
      throw new Error(`任务 ${taskId} 的隔离域已存在`);
    }

    // 生成域路径（使用 hash 避免路径注入）
    const taskHash = crypto.createHash('md5').update(taskId).digest('hex').substring(0, 8);
    const domainPath = path.join(this.baseDir, `${taskHash}_${taskId.replace(/[^a-zA-Z0-9_-]/g, '_')}`);
    
    // 创建目录
    fs.mkdirSync(domainPath, { recursive: true });
    
    // 创建域元数据
    const metadata = {
      taskId,
      domainPath,
      createdAt: Date.now(),
      expiresAt: options.ttl ? Date.now() + options.ttl : null,
      basePath: domainPath,
      allowedPatterns: options.allowedPatterns || ['**/*'],
      forbiddenPatterns: options.forbiddenPatterns || ['../**', '/**', '..\\**'],
      maxFileSize: options.maxFileSize || 100 * 1024 * 1024, // 100MB
      quota: options.quota || null
    };
    
    // 保存元数据
    fs.writeFileSync(
      path.join(domainPath, '.domain.json'),
      JSON.stringify(metadata, null, 2)
    );
    
    // 创建标准子目录
    const standardDirs = ['output', 'temp', 'logs', 'data'];
    standardDirs.forEach(dir => {
      fs.mkdirSync(path.join(domainPath, dir), { recursive: true });
    });
    
    // 注册域
    this.domains.set(taskId, {
      ...metadata,
      status: 'active',
      writtenFiles: [],
      totalSize: 0
    });
    
    this.metadata.totalDomains++;
    this.metadata.activeDomains++;
    this.saveMetadata();
    
    console.log(`[WriteDomainIsolator] 为任务 ${taskId} 创建隔离域：${domainPath}`);
    
    return domainPath;
  }

  /**
   * 验证写入是否在域内
   * @param {string} taskId - 任务 ID
   * @param {string} targetPath - 目标路径
   * @returns {boolean} 是否合法
   */
  validateWrite(taskId, targetPath) {
    const domain = this.domains.get(taskId);
    
    if (!domain) {
      throw new Error(`[WriteDomainIsolator] 任务 ${taskId} 无隔离域，请先调用 createDomain()`);
    }
    
    if (domain.status !== 'active') {
      throw new Error(`[WriteDomainIsolator] 任务 ${taskId} 的隔离域已${domain.status}`);
    }
    
    // 检查是否过期
    if (domain.expiresAt && Date.now() > domain.expiresAt) {
      this.closeDomain(taskId, 'expired');
      throw new Error(`[WriteDomainIsolator] 任务 ${taskId} 的隔离域已过期`);
    }
    
    const resolved = path.resolve(targetPath);
    const domainPath = path.resolve(domain.domainPath);
    
    // 路径前缀检查
    if (!resolved.startsWith(domainPath + path.sep) && resolved !== domainPath) {
      throw new Error(
        `[WriteDomainIsolator] 写入越界：${targetPath} 不在域 ${domainPath} 内`
      );
    }
    
    // 检查禁止模式
    const relativePath = path.relative(domainPath, resolved);
    if (relativePath.startsWith('..') || path.isAbsolute(relativePath)) {
      throw new Error(
        `[WriteDomainIsolator] 禁止的路径模式：${relativePath}`
      );
    }
    
    return true;
  }

  /**
   * 安全的文件写入（自动验证）
   * @param {string} taskId - 任务 ID
   * @param {string} filePath - 文件路径
   * @param {string|Buffer} data - 数据
   * @param {object} options - 写入选项
   */
  safeWrite(taskId, filePath, data, options = {}) {
    // 验证写入权限
    this.validateWrite(taskId, filePath);
    
    const domain = this.domains.get(taskId);
    const resolvedPath = path.resolve(filePath);
    
    // 检查配额
    if (domain.quota) {
      const dataSize = Buffer.isBuffer(data) ? data.length : Buffer.byteLength(data, 'utf8');
      if (domain.totalSize + dataSize > domain.quota) {
        throw new Error(
          `[WriteDomainIsolator] 超出配额限制：${domain.totalSize + dataSize} > ${domain.quota}`
        );
      }
    }
    
    // 检查文件大小
    const maxFileSize = domain.maxFileSize;
    const dataSize = Buffer.isBuffer(data) ? data.length : Buffer.byteLength(data, 'utf8');
    if (dataSize > maxFileSize) {
      throw new Error(
        `[WriteDomainIsolator] 文件超出大小限制：${dataSize} > ${maxFileSize}`
      );
    }
    
    // 执行写入
    fs.writeFileSync(resolvedPath, data, options.encoding || 'utf8');
    
    // 更新域统计
    domain.writtenFiles.push({
      path: resolvedPath,
      size: dataSize,
      writtenAt: Date.now()
    });
    domain.totalSize += dataSize;
    
    return {
      path: resolvedPath,
      size: dataSize,
      success: true
    };
  }

  /**
   * 获取域内所有文件
   * @param {string} taskId - 任务 ID
   * @returns {string[]} 文件列表
   */
  getDomainFiles(taskId) {
    const domain = this.domains.get(taskId);
    
    if (!domain) {
      throw new Error(`任务 ${taskId} 无隔离域`);
    }
    
    const files = [];
    const walk = (dir) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });
      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);
        if (entry.name === '.domain.json') continue; // 跳过元数据
        
        if (entry.isDirectory()) {
          walk(fullPath);
        } else {
          files.push(path.relative(domain.domainPath, fullPath));
        }
      }
    };
    
    walk(domain.domainPath);
    return files;
  }

  /**
   * 获取域统计信息
   * @param {string} taskId - 任务 ID
   * @returns {object} 统计信息
   */
  getDomainStats(taskId) {
    const domain = this.domains.get(taskId);
    
    if (!domain) {
      return null;
    }
    
    return {
      taskId,
      status: domain.status,
      fileCount: domain.writtenFiles.length,
      totalSize: domain.totalSize,
      createdAt: domain.createdAt,
      expiresAt: domain.expiresAt
    };
  }

  /**
   * 关闭域（标记为完成）
   * @param {string} taskId - 任务 ID
   * @param {string} reason - 关闭原因
   */
  closeDomain(taskId, reason = 'completed') {
    const domain = this.domains.get(taskId);
    
    if (!domain) {
      return;
    }
    
    domain.status = reason;
    this.metadata.activeDomains--;
    this.saveMetadata();
    
    console.log(`[WriteDomainIsolator] 任务 ${taskId} 的隔离域已关闭：${reason}`);
  }

  /**
   * 清理域（删除文件）
   * @param {string} taskId - 任务 ID
   * @param {boolean} force - 强制删除
   */
  cleanupDomain(taskId, force = false) {
    const domain = this.domains.get(taskId);
    
    if (!domain) {
      return;
    }
    
    if (domain.status === 'active' && !force) {
      throw new Error(`不能清理活跃域，请先调用 closeDomain()`);
    }
    
    try {
      fs.rmSync(domain.domainPath, { recursive: true, force: true });
      this.domains.delete(taskId);
      console.log(`[WriteDomainIsolator] 已清理域：${taskId}`);
    } catch (error) {
      console.error(`[WriteDomainIsolator] 清理域失败：${error.message}`);
    }
  }

  /**
   * 保存元数据
   */
  saveMetadata() {
    const metadataPath = path.join(this.baseDir, '.isolator-metadata.json');
    fs.writeFileSync(metadataPath, JSON.stringify(this.metadata, null, 2));
  }

  /**
   * 加载元数据
   */
  loadMetadata() {
    const metadataPath = path.join(this.baseDir, '.isolator-metadata.json');
    if (fs.existsSync(metadataPath)) {
      this.metadata = JSON.parse(fs.readFileSync(metadataPath, 'utf8'));
    }
  }

  /**
   * 获取所有活跃域
   * @returns {Array} 活跃域列表
   */
  getActiveDomains() {
    const active = [];
    for (const [taskId, domain] of this.domains) {
      if (domain.status === 'active') {
        active.push({
          taskId,
          ...this.getDomainStats(taskId)
        });
      }
    }
    return active;
  }

  /**
   * 批量验证（用于预检查）
   * @param {Array} tasks - 任务列表 [{taskId, paths: []}]
   * @returns {object} 验证结果
   */
  batchValidate(tasks) {
    const results = {
      valid: [],
      invalid: []
    };
    
    for (const task of tasks) {
      for (const targetPath of task.paths) {
        try {
          this.validateWrite(task.taskId, targetPath);
          results.valid.push({ taskId: task.taskId, path: targetPath });
        } catch (error) {
          results.invalid.push({
            taskId: task.taskId,
            path: targetPath,
            error: error.message
          });
        }
      }
    }
    
    return results;
  }
}

module.exports = WriteDomainIsolator;

// CLI 入口
if (require.main === module) {
  const isolator = new WriteDomainIsolator({ baseDir: '/tmp/test-isolator' });
  
  // 测试
  const taskId = 'test-task-001';
  const domainPath = isolator.createDomain(taskId);
  
  console.log('域路径:', domainPath);
  
  // 测试写入
  isolator.safeWrite(taskId, path.join(domainPath, 'output', 'test.txt'), 'Hello World');
  
  // 测试越界写入（应该失败）
  try {
    isolator.safeWrite(taskId, '/tmp/outside.txt', 'Should fail');
  } catch (error) {
    console.log('越界写入被阻止:', error.message);
  }
  
  // 获取文件列表
  console.log('域内文件:', isolator.getDomainFiles(taskId));
  
  // 关闭域
  isolator.closeDomain(taskId);
}
