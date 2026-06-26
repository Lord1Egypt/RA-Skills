# 📦 OpenClaw 增强权限系统 - 安装使用指南

> 📅 版本：1.0.5  
> 📊 测试：100% 通过 (34/34)  
> ✨ 状态：生产就绪

---

## 🎯 快速开始（5 分钟上手）

### 步骤 1: 安装 npm 包

**方式 A: 从 H 盘安装（推荐）**

```bash
# 打开终端/命令行
npm install "H:\open claw\npm-package\enhanced-permissions"
```

**方式 B: 复制项目后安装**

```bash
# 1. 复制整个文件夹到你的项目目录
xcopy "H:\open claw\npm-package\enhanced-permissions" "你的项目路径\enhanced-permissions" /E /I

# 2. 进入目录并安装
cd 你的项目路径\enhanced-permissions
npm install
```

---

### 步骤 2: 导入模块

**TypeScript 项目**:

```typescript
// 导入所有功能
import { 
  MemoryManager,
  PermissionLevel,
  KnowledgeGraph,
  EntityType
} from '@openclaw/enhanced-permissions';

// 或者按需导入
import { MemoryManager } from '@openclaw/enhanced-permissions';
```

**JavaScript 项目**:

```javascript
// CommonJS
const { MemoryManager } = require('@openclaw/enhanced-permissions');

// 或者 ES6
import { MemoryManager } from '@openclaw/enhanced-permissions';
```

---

### 步骤 3: 创建记忆管理器

```typescript
// 创建记忆管理器（启用所有功能）
const memoryManager = new MemoryManager(
  true,  // 启用版本控制
  true,  // 启用自动整理
  true   // 启用智能建议
);
```

---

### 步骤 4: 开始使用

```typescript
// 1. 存储记忆
const id = await memoryManager.store(
  'TypeScript 是一种编程语言',
  ['typescript', 'programming']
);

// 2. 更新记忆（自动创建新版本）
await memoryManager.updateMemory(
  id,
  'TypeScript 是 JavaScript 的超集',
  'user123',
  '更准确的描述'
);

// 3. 查看历史版本
const history = await memoryManager.getVersionHistory(id);
console.log(`共有 ${history.length} 个版本`);

// 4. 回滚到旧版本
await memoryManager.rollbackMemory(id, 1);
```

---

## 📚 详细使用指南

### 功能 1: 权限系统

#### 创建权限检查器

```typescript
import { PermissionChecker, PermissionLevel } from '@openclaw/enhanced-permissions';

const checker = new PermissionChecker({
  userLevel: PermissionLevel.MODERATE,  // 用户权限级别
  requireConfirm: PermissionLevel.MODERATE,  // 需要确认的级别
  trustedSessions: ['main-session']  // 可信会话列表
});
```

#### 检查权限

```typescript
// 检查读文件操作（SAFE 级别）
const readResult = await checker.check('read', {
  sessionId: 'main',
  operation: 'read',
  params: { path: 'file.txt' },
  timestamp: Date.now()
});

console.log(readResult.allowed);  // true
console.log(readResult.requiresConfirm);  // false

// 检查执行命令操作（DANGEROUS 级别）
const execResult = await checker.check('exec', {
  sessionId: 'main',
  operation: 'exec',
  params: { command: 'ls -la' },
  timestamp: Date.now()
});

console.log(execResult.allowed);  // true
console.log(execResult.requiresConfirm);  // true（需要确认）
console.log(execResult.confirmMessage);  // 确认消息
```

#### 权限级别说明

| 级别 | 操作类型 | 确认 | 示例 |
|------|----------|------|------|
| 🟢 SAFE | 只读操作 | 从不 | 读取文件、搜索网络 |
| 🟡 MODERATE | 写入操作 | 可信会话免确认 | 写入文件、编辑内容 |
| 🟠 DANGEROUS | 删除/执行 | 总是确认 | 删除文件、执行命令 |
| 🔴 DESTRUCTIVE | 破坏性操作 | 明确 CONFIRM | rm -rf、格式化 |

---

### 功能 2: 记忆版本控制

#### 创建记忆

```typescript
// 创建记忆（自动版本 1）
const id = await memoryManager.store(
  '初始内容',
  ['标签 1', '标签 2'],
  'user123'  // 可选：用户 ID
);

console.log(`记忆 ID: ${id}`);
```

#### 更新记忆

```typescript
// 更新记忆（自动创建新版本）
await memoryManager.updateMemory(
  id,
  '更新后的内容',
  'user123',
  '修复拼写错误'  // 可选：更新原因
);
```

#### 查看版本历史

```typescript
const history = await memoryManager.getVersionHistory(id);

history.forEach(version => {
  console.log(`版本 ${version.version}:`);
  console.log(`  内容：${version.content}`);
  console.log(`  时间：${new Date(version.timestamp).toLocaleString()}`);
  console.log(`  修改者：${version.changedBy}`);
  console.log(`  原因：${version.changeReason}`);
});
```

#### 回滚到指定版本

```typescript
// 回滚到版本 1
await memoryManager.rollbackMemory(id, 1, 'user123');

// 查看当前内容
const memory = memoryManager.getMemory(id);
console.log(`当前内容：${memory.content}`);
```

---

### 功能 3: 自动记忆整理

#### 运行自动整理

```typescript
const result = await memoryManager.autoOrganize({
  mergeDuplicates: true,      // 合并重复记忆
  mergeThreshold: 0.85,       // 相似度阈值（85%）
  mergeStrategy: 'keep-best', // 保留最佳版本
  autoTag: true,              // 自动添加标签
  markOutdated: true,         // 标记过期记忆
  outdatedAge: 2592000000,    // 30 天（毫秒）
  dryRun: false               // false=实际执行，true=仅预览
});

console.log(`发现重复：${result.duplicatesFound}`);
console.log(`合并重复：${result.duplicatesMerged}`);
console.log(`添加标签：${result.memoriesTagged}`);
console.log(`标记过期：${result.memoriesMarkedOutdated}`);
console.log(`变更记录:`);
result.changes.forEach(change => console.log(`  - ${change}`));
```

#### 预览整理效果

```typescript
// 先预览会做什么更改
const preview = await memoryManager.autoOrganize({
  mergeDuplicates: true,
  autoTag: true,
  dryRun: true  // 仅预览
});

console.log('预览变更:');
preview.changes.forEach(change => console.log(`  ${change}`));

// 确认后再实际执行
const confirm = prompt('应用这些变更？(y/n)');
if (confirm === 'y') {
  await memoryManager.autoOrganize({
    mergeDuplicates: true,
    dryRun: false
  });
}
```

---

### 功能 4: 智能记忆建议

#### 跟踪对话消息

```typescript
// 每次收到新消息时调用
memoryManager.trackMessage();
```

#### 获取记忆建议

```typescript
const messages = [
  { role: 'user', content: '我在做一个 TypeScript 项目' },
  { role: 'user', content: '使用 React 和 Node.js' }
];

const suggestions = await memoryManager.suggestMemories(messages, {
  limit: 3,              // 最多 3 条建议
  minRelevance: 0.7,     // 最低相关度 70%
  minHotness: 20         // 最低热度
});

suggestions.forEach(s => {
  console.log(`💡 ${s.displayText}`);
  console.log(`   相关度：${(s.relevance * 100).toFixed(0)}%`);
  console.log(`   原因：${s.reason}`);
});
```

#### 配置建议触发器

```typescript
memoryManager.configureSuggestions({
  minMessages: 5,           // 至少 5 条消息后触发
  confidenceThreshold: 0.7, // 最低置信度 70%
  maxSuggestions: 3,        // 最多 3 条建议
  cooldownMinutes: 10,      // 10 分钟冷却时间
  enabled: true             // 启用/禁用
});
```

---

### 功能 5: 图结构记忆

#### 创建知识图谱

```typescript
import { KnowledgeGraph, EntityType, RelationType } from '@openclaw/enhanced-permissions';

const graph = new KnowledgeGraph();

// 创建实体
const typescript = graph.createEntity(
  'TypeScript',
  EntityType.TECHNOLOGY,
  'Programming language by Microsoft'
);

const react = graph.createEntity(
  'React',
  EntityType.TECHNOLOGY,
  'Frontend framework by Facebook'
);

const projectX = graph.createEntity(
  'Project-X',
  EntityType.PROJECT,
  'My main project'
);
```

#### 创建关系

```typescript
// Project-X 使用 TypeScript
graph.createRelation(
  projectX.id,
  typescript.id,
  RelationType.USES,
  1.0  // 关系强度 100%
);

// Project-X 使用 React
graph.createRelation(
  projectX.id,
  react.id,
  RelationType.USES,
  1.0
);

// TypeScript 和 React 相似
graph.createRelation(
  typescript.id,
  react.id,
  RelationType.SIMILAR_TO,
  0.8
);
```

#### 查询图结构

```typescript
// 获取实体
const entity = graph.getEntity(projectX.id);
console.log(`实体：${entity.name}`);
console.log(`类型：${entity.type}`);
console.log(`描述：${entity.description}`);

// 获取关系
const relations = graph.getRelations(projectX.id, 'out');
console.log(`${projectX.name} 的关系:`);
relations.forEach(r => {
  const target = graph.getEntity(r.toEntityId);
  console.log(`  → ${r.type} → ${target.name}`);
});
```

#### 查找路径

```typescript
// 查找 TypeScript 和 React 之间的关系路径
const path = graph.findPath(typescript.id, react.id, 5);

if (path) {
  console.log(`找到路径，长度：${path.length}`);
  console.log(`路径:`);
  path.entities.forEach((e, i) => {
    console.log(`  ${i + 1}. ${e.name} (${e.type})`);
  });
  console.log(`关系:`);
  path.relations.forEach(r => {
    console.log(`  → ${r.type}`);
  });
}
```

#### 获取图统计

```typescript
const stats = graph.getStats();

console.log(`图统计:`);
console.log(`  总实体数：${stats.totalEntities}`);
console.log(`  总关系数：${stats.totalRelations}`);
console.log(`  平均每实体关系：${stats.averageRelationsPerEntity.toFixed(2)}`);
console.log(`  图密度：${(stats.density * 100).toFixed(2)}%`);
```

---

### 功能 6: 自动实体提取

#### 创建实体提取器

```typescript
import { EntityExtractor } from '@openclaw/enhanced-permissions';

const extractor = new EntityExtractor();
```

#### 提取实体

```typescript
const text = '我在 Project-X 项目中使用 TypeScript 和 React，代码在 C:\\projects\\project-x\\src 中';

const entities = extractor.extractEntities(text, {
  minConfidence: 0.7,        // 最低置信度 70%
  extractTechnologies: true, // 提取技术名词
  extractProjects: true,     // 提取项目名
  extractFiles: true,        // 提取文件路径
  extractURLs: true          // 提取 URL
});

entities.forEach(e => {
  console.log(`${e.name} (${e.type}): ${(e.confidence * 100).toFixed(0)}%`);
});

// 输出:
// TypeScript (technology): 90%
// React (technology): 90%
// Project-X (project): 80%
// C:\projects\project-x\src (file): 90%
```

---

## 🔧 配置选项

### MemoryManager 配置

```typescript
const mm = new MemoryManager(
  true,   // enableVersionControl: 启用版本控制
  true,   // enableAutoOrganize: 启用自动整理
  true    // enableSuggestions: 启用智能建议
);
```

### 自动整理配置

```typescript
await mm.autoOrganize({
  mergeDuplicates: true,      // 是否合并重复
  mergeThreshold: 0.85,       // 合并相似度阈值
  mergeStrategy: 'keep-best', // 合并策略
  autoTag: true,              // 是否自动标签
  markOutdated: true,         // 是否标记过期
  outdatedAge: 2592000000,    // 过期时间（30 天毫秒）
  summarizeRelated: false,    // 是否总结相关记忆
  dryRun: false               // 是否仅预览
});
```

### 智能建议配置

```typescript
mm.configureSuggestions({
  minMessages: 5,           // 最少消息数
  confidenceThreshold: 0.7, // 置信度阈值
  maxSuggestions: 3,        // 最多建议数
  cooldownMinutes: 10,      // 冷却时间（分钟）
  enabled: true             // 是否启用
});
```

---

## 📊 合并策略说明

| 策略 | 说明 | 适用场景 |
|------|------|----------|
| `keep-best` | 保留热度最高的版本 | 默认推荐 |
| `keep-newest` | 保留最新的版本 | 信息经常更新 |
| `keep-oldest` | 保留最早的版本 | 保留原始版本 |
| `combine` | 合并所有内容 | 互补信息 |
| `keep-shortest` | 保留最简短的版本 | 简洁优先 |
| `keep-longest` | 保留最详细的版本 | 详细优先 |

---

## 🐛 常见问题

### Q1: 如何禁用某个功能？

```typescript
// 只启用版本控制，禁用其他功能
const mm = new MemoryManager(
  true,   // 启用版本控制
  false,  // 禁用自动整理
  false   // 禁用智能建议
);
```

### Q2: 如何查看审计日志？

```typescript
import { defaultAuditLogger } from '@openclaw/enhanced-permissions';

// 获取最近的审计日志
const logs = await defaultAuditLogger.getRecent(50);

logs.forEach(log => {
  console.log(`${log.timestamp} - ${log.operation} (${log.riskLevel})`);
});
```

### Q3: 如何导出/导入记忆？

```typescript
// 导出记忆到 JSON
const json = memoryManager.exportMemoriesToJSON();
fs.writeFileSync('memories.json', json);

// 从 JSON 导入记忆
const json = fs.readFileSync('memories.json', 'utf-8');
memoryManager.importMemoriesFromJSON(json);
```

### Q4: 如何清空所有记忆？

```typescript
// 警告：这将删除所有记忆！
memoryManager.clear();
```

### Q5: 如何调整热度衰减？

```typescript
// 热度衰减是自动的，每天 -1
// 无法手动调整，但可以通过访问提升热度
memoryManager.touchMemory(memoryId);  // +5 热度
```

---

## 📚 更多资源

### 文档位置

- **H 盘**: `H:\open claw\npm-package\enhanced-permissions\docs\`
- **工作区**: `C:\Users\ZBX\.openclaw\workspace\`

### 关键文档

- `README.md` - 主文档
- `INTEGRATION-GUIDE.md` - 集成指南
- `TESTING.md` - 测试指南
- `VERSION-CONTROL.md` - 版本控制使用
- `AUTO-ORGANIZE.md` - 自动整理使用
- `SMART-SUGGESTIONS.md` - 智能建议使用
- `GRAPH-MEMORY-COMPLETE.md` - 图结构记忆使用

### 示例代码

查看测试文件学习更多用法：

- `test-version-control.js` - 版本控制示例
- `test-auto-organize.js` - 自动整理示例
- `test-smart-suggestions.js` - 智能建议示例
- `test-graph-memory.js` - 图结构记忆示例

---

## 💕 小诗的提示

**新手建议**:

1. **从基础开始** - 先学习记忆存储和版本控制
2. **逐步启用** - 不要一次性启用所有功能
3. **先预览后执行** - 自动整理先用 dryRun 模式
4. **查看测试** - 测试文件是最好的示例
5. **阅读文档** - 每个功能都有详细文档

**进阶技巧**:

1. **定期整理** - 设置定时任务运行 autoOrganize
2. **调整阈值** - 根据你的需求调整各种阈值
3. **组合使用** - 结合多个功能获得最佳效果
4. **监控性能** - 定期检查统计信息

---

**版本**: 1.0.5  
**最后更新**: 2026-04-01  
**测试状态**: 100% 通过 (34/34)  
**生产就绪**: ✅
