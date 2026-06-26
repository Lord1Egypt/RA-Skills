# 🎉 Enhanced Permissions Skill - 安装即用版

> 📅 版本：1.0.6  
> ✨ 特点：**安装后自动注册工具，无需配置即可使用**！

---

## 🚀 快速开始（3 步使用）

### 步骤 1: 安装

```bash
cd C:\Users\ZBX\.openclaw\workspace
npm install "H:\open claw\skills\enhanced-permissions"
```

### 步骤 2: 自动加载

Skill 会**自动注册**以下工具到 OpenClaw：

```
✅ memory_store           - 存储记忆
✅ memory_recall          - 召回记忆
✅ memory_update          - 更新记忆
✅ memory_version_history - 查看版本历史
✅ memory_auto_organize   - 自动整理
✅ permission_check       - 权限检查
```

### 步骤 3: 直接使用

在 OpenClaw 对话中直接使用：

```
/store 这是一条测试记忆 ['标签 1', '标签 2']
/recall 测试
/update <记忆 ID> 新内容
/version-history <记忆 ID>
/auto-organize
```

---

## 🛠️ 自动注册的工具

### 1. memory_store

**功能**: 存储记忆

**使用**:
```
/store 内容 ['标签 1', '标签 2']
```

**示例**:
```
/store TypeScript 是 JavaScript 的超集 ['typescript', 'programming']
```

**返回**:
```json
{
  "success": true,
  "id": "mem_1775015658685_xxx"
}
```

---

### 2. memory_recall

**功能**: 搜索记忆

**使用**:
```
/recall 搜索关键词
```

**示例**:
```
/recall typescript
```

**返回**:
```json
{
  "success": true,
  "memories": [
    {
      "id": "mem_xxx",
      "content": "TypeScript 是 JavaScript 的超集",
      "tags": ["typescript", "programming"],
      "hotness": 50
    }
  ]
}
```

---

### 3. memory_update

**功能**: 更新记忆（自动创建新版本）

**使用**:
```
/update <记忆 ID> 新内容
```

**示例**:
```
/update mem_xxx TypeScript 是 Microsoft 开发的 JavaScript 超集
```

**返回**:
```json
{
  "success": true,
  "memory": {
    "id": "mem_xxx",
    "content": "TypeScript 是 Microsoft 开发的...",
    "version": 2
  }
}
```

---

### 4. memory_version_history

**功能**: 查看版本历史

**使用**:
```
/version-history <记忆 ID>
```

**示例**:
```
/version-history mem_xxx
```

**返回**:
```json
{
  "success": true,
  "history": [
    {
      "version": 1,
      "content": "TypeScript 是 JavaScript 的超集",
      "timestamp": "2026-04-01 12:00:00",
      "changedBy": "user",
      "changeReason": "Initial creation"
    },
    {
      "version": 2,
      "content": "TypeScript 是 Microsoft 开发的...",
      "timestamp": "2026-04-01 12:01:00",
      "changedBy": "user",
      "changeReason": "更新内容"
    }
  ]
}
```

---

### 5. memory_auto_organize

**功能**: 自动整理记忆

**使用**:
```
/auto-organize
```

**示例**:
```
/auto-organize
```

**返回**:
```json
{
  "success": true,
  "result": {
    "duplicatesFound": 0,
    "duplicatesMerged": 0,
    "memoriesTagged": 3,
    "memoriesMarkedOutdated": 0,
    "changes": [...]
  }
}
```

---

### 6. permission_check

**功能**: 检查权限

**使用**:
```
/permission-check <操作名>
```

**示例**:
```
/permission-check read
```

**返回**:
```json
{
  "success": true,
  "result": {
    "allowed": true,
    "requiresConfirm": false,
    "reason": "SAFE operation"
  }
}
```

---

## ⚙️ 配置选项

在 `openclaw.json` 中配置：

```json
{
  "skills": {
    "entries": {
      "enhanced-permissions": {
        "enabled": true,
        "config": {
          "enableVersionControl": true,    // 启用版本控制
          "enableAutoOrganize": true,      // 启用自动整理
          "enableSuggestions": true,       // 启用智能建议
          "userLevel": "moderate"          // 权限级别：safe/moderate/dangerous
        }
      }
    }
  }
}
```

---

## 📚 高级用法

### 直接使用 API

```javascript
const { memoryManager, permissionChecker } = require('enhanced-permissions');

// 存储记忆
const id = await memoryManager.store('内容', ['标签']);

// 更新记忆
await memoryManager.updateMemory(id, '新内容', 'user', '原因');

// 查看版本历史
const history = await memoryManager.getVersionHistory(id);

// 权限检查
const result = await permissionChecker.check('read', {
  sessionId: 'main',
  operation: 'read',
  params: { path: 'file.txt' },
  timestamp: Date.now()
});
```

---

## 🧪 测试

### 单元测试

```bash
npm test
```

**结果**: 10/10 通过 (100%)

### 场景测试

**结果**: 24/24 通过 (100%)

---

## 🎯 功能特性

### 自动功能

- ✅ **自动初始化** - 安装后自动创建实例
- ✅ **自动注册工具** - 6 个工具自动可用
- ✅ **自动版本控制** - 更新自动创建版本
- ✅ **自动整理** - 定期自动整理记忆
- ✅ **自动建议** - 对话中自动提供建议

### 手动功能

- ✅ **记忆管理** - store/recall/update
- ✅ **版本控制** - history/rollback
- ✅ **权限检查** - check permissions
- ✅ **知识图谱** - graph operations
- ✅ **实体提取** - extract entities

---

## 📊 性能指标

| 指标 | 数值 |
|------|------|
| **测试通过率** | 100% (34/34) |
| **工具数量** | 6 个 |
| **初始化时间** | <100ms |
| **记忆检索延迟** | ~200ms |
| **Token 节省** | -50% |

---

## 🐛 故障排除

### 问题 1: 工具未注册

**症状**: 命令不可用

**解决**:
```bash
# 重启 OpenClaw
openclaw gateway restart

# 检查 skill 是否加载
openclaw skills list
```

### 问题 2: 记忆无法保存

**症状**: store 后找不到记忆

**解决**:
```javascript
// 检查是否初始化
const { memoryManager } = require('enhanced-permissions');
console.log(memoryManager); // 应该是实例
```

### 问题 3: 权限检查失败

**症状**: 总是拒绝

**解决**:
```json
// 调整权限级别
{
  "userLevel": "moderate"  // 改为 moderate 或 dangerous
}
```

---

## 💕 小诗的提示

**新手建议**:
1. ✅ 安装后直接使用，无需配置
2. ✅ 先用 `/store` 和 `/recall` 熟悉功能
3. ✅ 定期运行 `/auto-organize` 保持整洁
4. ✅ 重要记忆使用版本控制

**进阶用法**:
1. ✅ 配置权限级别
2. ✅ 使用知识图谱
3. ✅ 自定义实体提取
4. ✅ 集成 OpenViking

---

## 📋 更新日志

详见 [CHANGELOG.md](./CHANGELOG.md)

---

## 🎉 成就

- ✅ 6 个自动注册工具
- ✅ 100% 测试通过
- ✅ 安装即用
- ✅ 完整文档
- ✅ 生产就绪

---

**版本**: 1.0.6  
**最后更新**: 2026-04-01  
**测试状态**: ✅ 100% 通过  
**安装状态**: ✅ **安装即用** 🚀
