# ADD - 敏捷工作流 v6.0 Phase 5: 版本管理

**版本**: v6.0-Phase5  
**状态**: 设计完成 → 实施中  
**原则**: 效率优先，保质保量（无时间计划）

---

## 1. 架构概述

### 1.1 设计目标

**核心目标**：实现工作流和成果的版本管理、变更追溯、版本对比、版本回滚

**核心价值**：
- 版本追溯 100%
- 回滚成功 100%
- 变更可审计
- 历史可对比

### 1.2 质量标准

- 版本创建时间：< 1 秒
- 版本查询时间：< 100ms
- 回滚成功率：100%
- 文档完整度：100%
- 质量评分：≥85 分

---

## 2. 系统架构

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────┐
│                  版本管理界面                            │
│  (CLI / Web / API)                                      │
│  ├─ 版本列表  ├─ 版本对比  ├─ 版本回滚  ├─ 版本导出    │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│                  版本管理器                             │
│  VersionManager                                         │
│  ├─ 版本创建  ├─ 版本存储  ├─ 版本对比  ├─ 版本回滚    │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┘
│                  版本存储层                              │
│  ├─ 版本元数据  ├─ 版本内容  ├─ 版本链  ├─ 版本索引    │
└─────────────────────────────────────────────────────────┘
```

### 2.2 版本结构

```yaml
# 版本元数据
version:
  id: v1.0.0
  type: workflow  # workflow/deliverable/config
  createdAt: 2026-03-13T00:00:00Z
  createdBy: system
  parentVersion: v0.9.0
  description: 初始版本
  tags: [initial, stable]
  
# 版本内容
content:
  tasks: [...]
  config: {...}
  metrics: {...}
  
# 变更日志
changelog:
  - type: added
    description: 新增质量验证模块
  - type: changed
    description: 优化任务分配算法
```

---

## 3. 核心功能

### 3.1 版本创建

**创建时机**：
- 任务完成时（自动）
- 配置变更时（自动）
- 用户手动触发（手动）
- 定时快照（自动）

**版本类型**：
| 类型 | 说明 | 示例 |
|------|------|------|
| **工作流版本** | 任务/流程状态 | v1.0.0-workflow |
| **成果版本** | 交付成果 | v1.0.0-deliverable |
| **配置版本** | 系统配置 | v1.0.0-config |

### 3.2 版本存储

**存储结构**：
```
versions/
├── workflow/
│   ├── v1.0.0.yaml
│   ├── v1.0.1.yaml
│   └── ...
├── deliverable/
│   ├── v1.0.0.yaml
│   └── ...
└── config/
    ├── v1.0.0.yaml
    └── ...
```

**版本链**：
```
v1.0.0 → v1.0.1 → v1.0.2 → v1.1.0 → v2.0.0
           ↓           ↓
        v1.0.1-fix  v1.1.0-beta
```

### 3.3 版本对比

**对比维度**：
- 任务差异（新增/删除/修改）
- 配置差异（变更项）
- 指标差异（性能变化）
- 成果差异（内容变更）

**对比输出**：
```yaml
diff:
  added:
    - task: task-005
    - config: quality.thresholds.pass
  removed:
    - task: task-002
  changed:
    - config: agent.maxConcurrent (5 → 10)
    - metric: avgQuality (85 → 88)
```

### 3.4 版本回滚

**回滚策略**：
- 完全回滚（恢复所有状态）
- 部分回滚（恢复指定模块）
- 选择性回滚（恢复指定内容）

**回滚流程**：
```
选择版本 → 验证版本 → 备份当前 → 恢复版本 → 验证结果
```

---

## 4. 技术实现

### 4.1 版本管理器类

```javascript
class VersionManager {
  constructor(options = {}) {
    this.versionsDir = options.versionsDir || './versions';
    this.versions = new Map();
    this.currentVersion = null;
    
    this.ensureDirs();
  }

  // 创建版本
  async createVersion(type, content, description = '') {
    const version = {
      id: this.generateVersionId(type),
      type,
      createdAt: new Date().toISOString(),
      createdBy: 'system',
      parentVersion: this.currentVersion?.id,
      description,
      content,
      changelog: this.generateChangelog(content)
    };
    
    await this.saveVersion(version);
    this.currentVersion = version;
    
    return version;
  }

  // 获取版本
  async getVersion(versionId) {
    return await this.loadVersion(versionId);
  }

  // 版本对比
  async diffVersions(versionId1, versionId2) {
    const v1 = await this.getVersion(versionId1);
    const v2 = await this.getVersion(versionId2);
    
    return this.diffObjects(v1.content, v2.content);
  }

  // 版本回滚
  async rollback(versionId) {
    const version = await this.getVersion(versionId);
    if (!version) {
      throw new Error(`版本 ${versionId} 不存在`);
    }
    
    // 备份当前版本
    await this.createVersion(
      version.type,
      this.currentVersion.content,
      `回滚前备份：${versionId}`
    );
    
    // 恢复指定版本
    this.currentVersion = version;
    await this.applyVersion(version);
    
    return version;
  }

  // 版本列表
  listVersions(type = null) {
    const versions = Array.from(this.versions.values());
    
    if (type) {
      return versions.filter(v => v.type === type);
    }
    
    return versions;
  }

  // 版本标签
  addTag(versionId, tag) {
    const version = this.versions.get(versionId);
    if (!version) {
      throw new Error(`版本 ${versionId} 不存在`);
    }
    
    if (!version.tags) {
      version.tags = [];
    }
    
    version.tags.push(tag);
  }

  // 版本导出
  exportVersion(versionId) {
    const version = this.versions.get(versionId);
    if (!version) {
      throw new Error(`版本 ${versionId} 不存在`);
    }
    
    return JSON.stringify(version, null, 2);
  }

  // 版本导入
  async importVersion(versionData) {
    const version = JSON.parse(versionData);
    await this.saveVersion(version);
    return version;
  }
}
```

### 4.2 版本对比算法

```javascript
function diffObjects(obj1, obj2, prefix = '') {
  const diffs = {
    added: [],
    removed: [],
    changed: []
  };
  
  const allKeys = new Set([...Object.keys(obj1), ...Object.keys(obj2)]);
  
  for (const key of allKeys) {
    const key1 = obj1[key];
    const key2 = obj2[key];
    const fullKey = prefix ? `${prefix}.${key}` : key;
    
    if (key1 === undefined) {
      diffs.added.push({ key: fullKey, value: key2 });
    } else if (key2 === undefined) {
      diffs.removed.push({ key: fullKey, value: key1 });
    } else if (typeof key1 === 'object' && typeof key2 === 'object') {
      const nestedDiff = diffObjects(key1, key2, fullKey);
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
```

---

## 5. 实施计划

### 阶段 5.1: 版本创建
- [ ] 版本管理器核心
- [ ] 自动版本创建
- [ ] 手动版本创建
- [ ] 版本元数据

### 阶段 5.2: 版本存储
- [ ] 版本存储结构
- [ ] 版本链管理
- [ ] 版本索引
- [ ] 版本清理

### 阶段 5.3: 版本对比
- [ ] 版本差异算法
- [ ] 变更统计
- [ ] 影响分析
- [ ] 可视化对比

### 阶段 5.4: 版本操作
- [ ] 版本回滚
- [ ] 版本标签
- [ ] 版本导出/导入
- [ ] 文档完善

---

## 6. 验收标准

### 功能验收

- [ ] 版本创建正常
- [ ] 版本存储正常
- [ ] 版本对比正常
- [ ] 版本回滚正常
- [ ] 版本标签正常

### 性能验收

- [ ] 版本创建 < 1 秒
- [ ] 版本查询 < 100ms
- [ ] 回滚成功 100%
- [ ] 版本追溯 100%

### 质量验收

- [ ] 质量评分 ≥ 85 分
- [ ] 测试覆盖率 > 80%
- [ ] 文档完整度 100%
- [ ] 无严重缺陷

---

## 7. 交付物

### 代码

- [ ] version-manager.js (版本管理器)
- [ ] version-diff.js (版本对比)
- [ ] version-cli.js (CLI 工具)
- [ ] version-storage.js (版本存储)

### 文档

- [ ] 版本管理文档
- [ ] API 文档
- [ ] CLI 使用手册
- [ ] 最佳实践

### 测试

- [ ] 单元测试
- [ ] 集成测试
- [ ] 验收测试报告

---

**ADD 设计完成，开始实施 Phase 5！** 🚀

**原则**: 效率优先，保质保量  
**时间计划**: ❌ 禁止  
**质量标准**: ✅ ≥85 分  
**验证机制**: ✅ 自动测试
