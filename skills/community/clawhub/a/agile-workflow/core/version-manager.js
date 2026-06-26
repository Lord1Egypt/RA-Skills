#!/usr/bin/env node
/**
 * 版本管理器 v6.0-Phase5
 * 
 * 核心功能:
 * 1. 版本创建 (自动/手动)
 * 2. 版本存储 (版本链/索引)
 * 3. 版本对比 (diff/统计)
 * 4. 版本操作 (回滚/标签/导出)
 */

const fs = require('fs');
const path = require('path');
const yaml = require('js-yaml');

// ============ 配置 ============

const CONFIG = {
  versionsDir: path.join(__dirname, '../versions'),
  maxVersions: 100,  // 最多保留 100 个版本
  autoVersion: true, // 自动创建版本
  versionFormat: 'v{major}.{minor}.{patch}'
};

// ============ 版本管理器类 ============

class VersionManager {
  constructor(options = {}) {
    this.config = { ...CONFIG, ...options };
    this.versionsDir = this.config.versionsDir;
    this.versions = new Map();
    this.currentVersion = null;
    this.versionCounter = { major: 1, minor: 0, patch: 0 };
    
    this.ensureDirs();
    this.loadVersions();
    
    console.log('📚 版本管理器已启动');
  }

  /**
   * 确保目录存在
   */
  ensureDirs() {
    const types = ['workflow', 'deliverable', 'config'];
    for (const type of types) {
      const dir = path.join(this.versionsDir, type);
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    }
  }

  /**
   * 加载现有版本
   */
  loadVersions() {
    console.log('📖 加载版本历史...');
    
    const types = ['workflow', 'deliverable', 'config'];
    
    for (const type of types) {
      const typeDir = path.join(this.versionsDir, type);
      if (!fs.existsSync(typeDir)) continue;
      
      const files = fs.readdirSync(typeDir)
        .filter(f => f.endsWith('.yaml') || f.endsWith('.yml'))
        .sort();
      
      for (const file of files) {
        try {
          const content = fs.readFileSync(path.join(typeDir, file), 'utf-8');
          const version = yaml.load(content);
          this.versions.set(version.id, version);
          
          // 设置当前版本为最新版本
          if (!this.currentVersion || version.createdAt > this.currentVersion.createdAt) {
            this.currentVersion = version;
          }
        } catch (error) {
          console.error(`⚠️ 加载版本文件失败：${file}`, error.message);
        }
      }
    }
    
    console.log(`✅ 已加载 ${this.versions.size} 个版本`);
  }

  /**
   * 生成版本号
   */
  generateVersionId(type) {
    const { major, minor, patch } = this.versionCounter;
    const versionId = `v${major}.${minor}.${patch}`;
    
    // 更新计数器
    this.versionCounter.patch++;
    if (this.versionCounter.patch > 9) {
      this.versionCounter.patch = 0;
      this.versionCounter.minor++;
      if (this.versionCounter.minor > 9) {
        this.versionCounter.minor = 0;
        this.versionCounter.major++;
      }
    }
    
    return `${versionId}-${type}`;
  }

  /**
   * 创建版本
   */
  async createVersion(type, content, description = '', options = {}) {
    console.log(`📝 创建版本：${type}`);
    
    const version = {
      id: this.generateVersionId(type),
      type,
      createdAt: new Date().toISOString(),
      createdBy: options.createdBy || 'system',
      parentVersion: this.currentVersion?.id || null,
      description: description || '',
      content: this.deepClone(content),
      changelog: this.generateChangelog(content, options.previousContent),
      tags: options.tags || [],
      metrics: this.calculateMetrics(content)
    };
    
    await this.saveVersion(version);
    this.versions.set(version.id, version);
    this.currentVersion = version;
    
    console.log(`✅ 版本已创建：${version.id}`);
    
    // 清理旧版本
    this.cleanupOldVersions();
    
    return version;
  }

  /**
   * 保存版本
   */
  async saveVersion(version) {
    const typeDir = path.join(this.versionsDir, version.type);
    const file = path.join(typeDir, `${version.id}.yaml`);
    
    const content = yaml.dump(version, {
      indent: 2,
      lineWidth: -1,
      noRefs: true
    });
    
    fs.writeFileSync(file, content, 'utf-8');
  }

  /**
   * 获取版本
   */
  async getVersion(versionId) {
    return this.versions.get(versionId) || await this.loadVersionFromFile(versionId);
  }

  /**
   * 从文件加载版本
   */
  async loadVersionFromFile(versionId) {
    // 尝试在不同类型目录中查找
    const types = ['workflow', 'deliverable', 'config'];
    
    for (const type of types) {
      const file = path.join(this.versionsDir, type, `${versionId}.yaml`);
      if (fs.existsSync(file)) {
        const content = fs.readFileSync(file, 'utf-8');
        const version = yaml.load(content);
        this.versions.set(versionId, version);
        return version;
      }
    }
    
    return null;
  }

  /**
   * 版本对比
   */
  async diffVersions(versionId1, versionId2) {
    console.log(`🔍 对比版本：${versionId1} vs ${versionId2}`);
    
    const v1 = await this.getVersion(versionId1);
    const v2 = await this.getVersion(versionId2);
    
    if (!v1 || !v2) {
      throw new Error('版本不存在');
    }
    
    const diff = {
      version1: versionId1,
      version2: versionId2,
      createdAt: new Date().toISOString(),
      content: this.diffObjects(v1.content, v2.content),
      metrics: {
        added: 0,
        removed: 0,
        changed: 0
      }
    };
    
    // 统计变更
    diff.metrics.added = diff.content.added.length;
    diff.metrics.removed = diff.content.removed.length;
    diff.metrics.changed = diff.content.changed.length;
    
    return diff;
  }

  /**
   * 对象对比
   */
  diffObjects(obj1, obj2, prefix = '') {
    const diffs = {
      added: [],
      removed: [],
      changed: []
    };
    
    const allKeys = new Set([...Object.keys(obj1 || {}), ...Object.keys(obj2 || {})]);
    
    for (const key of allKeys) {
      const key1 = obj1?.[key];
      const key2 = obj2?.[key];
      const fullKey = prefix ? `${prefix}.${key}` : key;
      
      if (key1 === undefined && key2 !== undefined) {
        diffs.added.push({ key: fullKey, value: key2 });
      } else if (key1 !== undefined && key2 === undefined) {
        diffs.removed.push({ key: fullKey, value: key1 });
      } else if (typeof key1 === 'object' && typeof key2 === 'object' && 
                 !Array.isArray(key1) && !Array.isArray(key2)) {
        const nestedDiff = this.diffObjects(key1, key2, fullKey);
        diffs.added.push(...nestedDiff.added);
        diffs.removed.push(...nestedDiff.removed);
        diffs.changed.push(...nestedDiff.changed);
      } else if (key1 !== key2) {
        diffs.changed.push({
          key: fullKey,
          oldValue: key1,
          newValue: key2
        });
      }
    }
    
    return diffs;
  }

  /**
   * 版本回滚
   */
  async rollback(versionId, reason = '') {
    console.log(`↩️ 回滚到版本：${versionId}`);
    
    const version = await this.getVersion(versionId);
    if (!version) {
      throw new Error(`版本 ${versionId} 不存在`);
    }
    
    // 创建回滚前备份
    const backupVersion = await this.createVersion(
      version.type,
      this.currentVersion?.content || {},
      `回滚前备份：${versionId} - ${reason}`,
      { tags: ['rollback-backup'] }
    );
    
    console.log(`💾 已创建备份版本：${backupVersion.id}`);
    
    // 恢复指定版本
    this.currentVersion = version;
    
    // 创建回滚版本
    const rollbackVersion = await this.createVersion(
      version.type,
      version.content,
      `回滚到 ${versionId} - ${reason}`,
      { tags: ['rollback'], sourceVersion: versionId }
    );
    
    console.log(`✅ 回滚完成：${rollbackVersion.id}`);
    
    return rollbackVersion;
  }

  /**
   * 版本列表
   */
  listVersions(type = null, limit = 20) {
    let versions = Array.from(this.versions.values());
    
    if (type) {
      versions = versions.filter(v => v.type === type);
    }
    
    // 按创建时间排序
    versions.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
    
    return versions.slice(0, limit);
  }

  /**
   * 添加标签
   */
  addTag(versionId, tag) {
    const version = this.versions.get(versionId);
    if (!version) {
      throw new Error(`版本 ${versionId} 不存在`);
    }
    
    if (!version.tags) {
      version.tags = [];
    }
    
    if (!version.tags.includes(tag)) {
      version.tags.push(tag);
      this.saveVersion(version);
      console.log(`✅ 标签已添加：${tag}`);
    }
  }

  /**
   * 移除标签
   */
  removeTag(versionId, tag) {
    const version = this.versions.get(versionId);
    if (!version) {
      throw new Error(`版本 ${versionId} 不存在`);
    }
    
    if (version.tags) {
      version.tags = version.tags.filter(t => t !== tag);
      this.saveVersion(version);
      console.log(`✅ 标签已移除：${tag}`);
    }
  }

  /**
   * 版本导出
   */
  exportVersion(versionId, format = 'yaml') {
    const version = this.versions.get(versionId);
    if (!version) {
      throw new Error(`版本 ${versionId} 不存在`);
    }
    
    if (format === 'yaml') {
      return yaml.dump(version, { indent: 2 });
    } else if (format === 'json') {
      return JSON.stringify(version, null, 2);
    } else {
      throw new Error(`不支持的格式：${format}`);
    }
  }

  /**
   * 版本导入
   */
  async importVersion(versionData, format = 'yaml') {
    let version;
    
    if (format === 'yaml') {
      version = yaml.load(versionData);
    } else if (format === 'json') {
      version = JSON.parse(versionData);
    } else {
      throw new Error(`不支持的格式：${format}`);
    }
    
    await this.saveVersion(version);
    this.versions.set(version.id, version);
    
    console.log(`✅ 版本已导入：${version.id}`);
    
    return version;
  }

  /**
   * 生成变更日志
   */
  generateChangelog(content, previousContent = null) {
    const changelog = [];
    
    if (!previousContent) {
      changelog.push({
        type: 'added',
        description: '初始版本'
      });
      return changelog;
    }
    
    const diff = this.diffObjects(previousContent, content);
    
    if (diff.added.length > 0) {
      changelog.push({
        type: 'added',
        count: diff.added.length,
        items: diff.added.slice(0, 5).map(i => i.key)
      });
    }
    
    if (diff.removed.length > 0) {
      changelog.push({
        type: 'removed',
        count: diff.removed.length,
        items: diff.removed.slice(0, 5).map(i => i.key)
      });
    }
    
    if (diff.changed.length > 0) {
      changelog.push({
        type: 'changed',
        count: diff.changed.length,
        items: diff.changed.slice(0, 5).map(i => i.key)
      });
    }
    
    return changelog;
  }

  /**
   * 计算指标
   */
  calculateMetrics(content) {
    const metrics = {
      taskCount: 0,
      configCount: 0,
      agentCount: 0
    };
    
    if (content.tasks) {
      metrics.taskCount = Array.isArray(content.tasks) ? content.tasks.length : 0;
    }
    
    if (content.config) {
      metrics.configCount = Object.keys(content.config).length;
    }
    
    if (content.agents) {
      metrics.agentCount = Object.keys(content.agents).length;
    }
    
    return metrics;
  }

  /**
   * 深度克隆
   */
  deepClone(obj) {
    return JSON.parse(JSON.stringify(obj));
  }

  /**
   * 清理旧版本
   */
  cleanupOldVersions() {
    for (const type of ['workflow', 'deliverable', 'config']) {
      const typeVersions = Array.from(this.versions.values())
        .filter(v => v.type === type)
        .sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt));
      
      if (typeVersions.length > this.config.maxVersions) {
        const toDelete = typeVersions.slice(this.config.maxVersions);
        for (const version of toDelete) {
          const file = path.join(this.versionsDir, type, `${version.id}.yaml`);
          if (fs.existsSync(file)) {
            fs.unlinkSync(file);
          }
          this.versions.delete(version.id);
        }
        console.log(`🧹 已清理 ${toDelete.length} 个旧版本 (${type})`);
      }
    }
  }

  /**
   * 获取版本链
   */
  getVersionChain(versionId) {
    const chain = [];
    let current = this.versions.get(versionId);
    
    while (current) {
      chain.push({
        id: current.id,
        createdAt: current.createdAt,
        description: current.description
      });
      
      if (current.parentVersion) {
        current = this.versions.get(current.parentVersion);
      } else {
        current = null;
      }
    }
    
    return chain;
  }

  /**
   * 获取当前版本
   */
  getCurrentVersion() {
    return this.currentVersion;
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const stats = {
      total: this.versions.size,
      byType: {
        workflow: 0,
        deliverable: 0,
        config: 0
      },
      latest: this.currentVersion?.id,
      createdAt: this.currentVersion?.createdAt
    };
    
    for (const version of this.versions.values()) {
      stats.byType[version.type]++;
    }
    
    return stats;
  }
}

// ============ CLI 接口 ============

function printHelp() {
  console.log(`
版本管理器 v6.0-Phase5

用法：node version-manager.js <命令> [选项]

命令:
  create <type>       创建版本 (workflow/deliverable/config)
  list [type]         查看版本列表
  get <versionId>     获取版本详情
  diff <v1> <v2>      对比版本
  rollback <version>  回滚版本
  tag <version> <tag> 添加标签
  export <version>    导出版本
  import <file>       导入版本
  stats               查看统计
  chain <version>     查看版本链

示例:
  node version-manager.js create workflow
  node version-manager.js list workflow
  node version-manager.js diff v1.0.0-workflow v1.0.1-workflow
  node version-manager.js rollback v1.0.0-workflow
`);
}

// ============ 主程序 ============

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === '--help' || command === '-h') {
    printHelp();
    return;
  }

  const manager = new VersionManager();

  try {
    switch (command) {
      case 'create':
        const type = args[1] || 'workflow';
        const description = args.slice(2).join(' ') || '手动创建版本';
        const version = await manager.createVersion(type, { sample: 'content' }, description);
        console.log('\n✅ 版本创建成功:');
        console.log(`   ID: ${version.id}`);
        console.log(`   类型：${version.type}`);
        console.log(`   时间：${version.createdAt}`);
        break;

      case 'list':
        const listType = args[1];
        const versions = manager.listVersions(listType);
        console.log(`\n📚 版本列表${listType ? ` (${listType})` : ''}:`);
        versions.forEach((v, i) => {
          console.log(`   ${i + 1}. ${v.id} (${v.type}) - ${v.createdAt}`);
          if (v.description) {
            console.log(`      ${v.description}`);
          }
        });
        break;

      case 'get':
        const versionId = args[1];
        if (!versionId) {
          console.log('❌ 请指定版本 ID');
          return;
        }
        const version_detail = await manager.getVersion(versionId);
        if (version_detail) {
          console.log('\n📖 版本详情:');
          console.log(yaml.dump(version_detail, { indent: 2 }));
        } else {
          console.log('❌ 版本不存在');
        }
        break;

      case 'diff':
        const v1 = args[1];
        const v2 = args[2];
        if (!v1 || !v2) {
          console.log('❌ 请指定两个版本 ID');
          return;
        }
        const diff = await manager.diffVersions(v1, v2);
        console.log('\n🔍 版本对比:');
        console.log(`   新增：${diff.metrics.added} 项`);
        console.log(`   删除：${diff.metrics.removed} 项`);
        console.log(`   修改：${diff.metrics.changed} 项`);
        break;

      case 'rollback':
        const rollbackVersion = args[1];
        const reason = args.slice(2).join(' ') || '手动回滚';
        if (!rollbackVersion) {
          console.log('❌ 请指定版本 ID');
          return;
        }
        const result = await manager.rollback(rollbackVersion, reason);
        console.log('\n✅ 回滚成功:');
        console.log(`   新 ID: ${result.id}`);
        console.log(`   时间：${result.createdAt}`);
        break;

      case 'tag':
        const tagVersion = args[1];
        const tag = args[2];
        if (!tagVersion || !tag) {
          console.log('❌ 请指定版本 ID 和标签');
          return;
        }
        manager.addTag(tagVersion, tag);
        break;

      case 'export':
        const exportVersion = args[1];
        const format = args[2] || 'yaml';
        if (!exportVersion) {
          console.log('❌ 请指定版本 ID');
          return;
        }
        const exported = manager.exportVersion(exportVersion, format);
        console.log(exported);
        break;

      case 'import':
        const importFile = args[1];
        if (!importFile) {
          console.log('❌ 请指定文件路径');
          return;
        }
        const importData = fs.readFileSync(importFile, 'utf-8');
        const format_import = importFile.endsWith('.json') ? 'json' : 'yaml';
        await manager.importVersion(importData, format_import);
        break;

      case 'stats':
        const stats = manager.getStats();
        console.log('\n📊 版本统计:');
        console.log(`   总数：${stats.total}`);
        console.log(`   Workflow: ${stats.byType.workflow}`);
        console.log(`   Deliverable: ${stats.byType.deliverable}`);
        console.log(`   Config: ${stats.byType.config}`);
        console.log(`   最新：${stats.latest}`);
        break;

      case 'chain':
        const chainVersion = args[1];
        if (!chainVersion) {
          console.log('❌ 请指定版本 ID');
          return;
        }
        const chain = manager.getVersionChain(chainVersion);
        console.log('\n🔗 版本链:');
        chain.forEach((v, i) => {
          console.log(`   ${i + 1}. ${v.id} - ${v.createdAt}`);
          if (v.description) {
            console.log(`      ${v.description}`);
          }
        });
        break;

      default:
        console.log(`未知命令：${command}`);
        printHelp();
    }
  } catch (error) {
    console.error('❌ 错误:', error.message);
    process.exit(1);
  }
}

// 导出 API
module.exports = { VersionManager, CONFIG };

// 运行 CLI
if (require.main === module) {
  main().catch(console.error);
}
