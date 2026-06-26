# Cognitive Brain v5.0 文档

## 概述

Cognitive Brain 是 OpenClaw 的记忆系统，提供跨会话的记忆存储、检索、联想和学习能力。

**版本**: 5.3.25  
**架构**: 分层架构（Domain → Repository → Service → API）

---

## 快速开始

```javascript
const { CognitiveBrain } = require('./src/index.js');

// 创建实例
const brain = new CognitiveBrain();

// 编码记忆
const memory = await brain.encode('今天学习了 Node.js', {
  type: 'conversation',
  importance: 0.8,
  sourceChannel: 'qq'
});

// 检索记忆
const memories = await brain.recall('Node.js');

// 获取统计
const stats = await brain.stats();
```

---

## 架构

### 分层设计

```
┌─────────────────────────────────────┐
│           API / CLI Layer           │  ← 对外接口
├─────────────────────────────────────┤
│         Service Layer               │  ← 业务逻辑
│   Memory / Concept / Association    │
├─────────────────────────────────────┤
│       Repository Layer              │  ← 数据访问
│   Repository + UnitOfWork           │
├─────────────────────────────────────┤
│        Domain Layer                 │  ← 领域模型
│   Memory / Concept / Association    │
├─────────────────────────────────────┤
│         Database                    │  ← PostgreSQL
└─────────────────────────────────────┘
```

### 目录结构

```
cognitive-brain/
├── src/
│   ├── domain/              # 领域模型
│   │   ├── BaseEntity.js    # 实体基类
│   │   ├── Memory.js        # 记忆实体
│   │   ├── Concept.js       # 概念实体
│   │   └── Association.js   # 关联实体
│   │
│   ├── repositories/        # 数据访问层
│   │   ├── BaseRepository.js       # 基础 CRUD
│   │   ├── MemoryRepository.js     # 记忆仓储
│   │   ├── ConceptRepository.js    # 概念仓储
│   │   ├── AssociationRepository.js # 关联仓储
│   │   └── UnitOfWork.js           # 事务管理
│   │
│   ├── services/            # 业务逻辑层
│   │   ├── MemoryService.js      # 记忆服务
│   │   ├── ConceptService.js     # 概念服务
│   │   └── AssociationService.js # 关联服务
│   │
│   ├── utils/               # 工具
│   │   └── logger.js        # 日志模块
│   │
│   └── index.js             # 主入口
│
├── tests/                   # 测试
├── migrations/              # 数据库迁移
└── docs/                    # 文档
```

---

## 核心概念

### 记忆 (Memory)

记忆是系统的核心实体，代表一条存储的信息。

```javascript
{
  id: 'uuid',
  content: '记忆内容',
  summary: '摘要',
  type: 'episodic',        // episodic|semantic|working|reflection|lesson|...
  importance: 0.5,         // 0-1
  sourceChannel: 'qq',     // 来源渠道
  role: 'user',            // user|assistant
  entities: ['关键词'],     // 提取的实体
  emotions: { valence: 0, arousal: 0 },
  accessCount: 0,
  lastAccessed: Date,
  createdAt: Date,
  updatedAt: Date
}
```

### 概念 (Concept)

概念是从记忆中提取的关键词或实体。

```javascript
{
  id: 'uuid',
  name: '概念名称',
  type: 'general',
  importance: 0.5,
  activation: 0.0,         // 激活度
  accessCount: 0,
  embedding: [...]         // 向量嵌入
}
```

### 关联 (Association)

关联表示概念之间的关系。

```javascript
{
  id: 'uuid',
  fromId: '概念A-ID',
  toId: '概念B-ID',
  type: 'related',         // related|causes|part-of|...
  weight: 0.5,             // 关联强度 0-1
  bidirectional: true
}
```

---

## API 参考

### CognitiveBrain

主入口类，提供统一的操作接口。

#### `encode(content, metadata)`

编码新记忆。

**参数:**
- `content` (string): 记忆内容
- `metadata` (object): 元数据
  - `type` (string): 记忆类型
  - `importance` (number): 重要性 0-1
  - `sourceChannel` (string): 来源渠道
  - `role` (string): 角色
  - `entities` (array): 实体列表

**返回:** `Memory` 实体

**示例:**
```javascript
const memory = await brain.encode('今天学习了 Node.js', {
  type: 'conversation',
  importance: 0.8,
  sourceChannel: 'qq',
  role: 'user',
  entities: ['Node.js', '学习']
});
```

#### `recall(query, options)`

检索记忆。

**参数:**
- `query` (string): 搜索关键词
- `options` (object):
  - `limit` (number): 返回数量，默认10
  - `type` (string): 过滤类型
  - `minImportance` (number): 最小重要性

**返回:** `Memory[]` 数组

**示例:**
```javascript
const memories = await brain.recall('Node.js', {
  limit: 5,
  type: 'conversation'
});
```

#### `transaction(fn)`

执行事务操作。

**参数:**
- `fn` (function): 事务函数，接收 UnitOfWork 实例

**示例:**
```javascript
await brain.transaction(async (uow) => {
  const memRepo = new MemoryRepository(uow.getQueryClient());
  const conceptRepo = new ConceptRepository(uow.getQueryClient());
  
  await memRepo.create(memory);
  await conceptRepo.create(concept);
});
```

#### `stats()`

获取系统统计信息。

**返回:**
```javascript
{
  memory: { total: 100, recentCount: 10, avgImportance: 0.6 },
  concept: { total: 50, topConcepts: [...], orphanCount: 5 }
}
```

---

### MemoryService

记忆相关的业务逻辑。

#### `encode(content, metadata)`

创建记忆并提取概念（事务包裹）。

#### `recall(query, options)`

搜索记忆并标记访问。

#### `getImportantMemories(types, limit)`

获取高重要性记忆（教训、反思等）。

#### `updateImportance(id, delta)`

更新记忆重要性。

#### `delete(id)` / `deleteMany(ids)`

删除记忆。

#### `getStats()`

获取记忆统计。

---

### ConceptService

概念相关的业务逻辑。

#### `getOrCreate(name, type)`

获取或创建概念。

#### `getTopConcepts(limit)`

获取热门概念。

#### `getOrphanConcepts(limit)`

获取孤立概念（无关联）。

#### `activate(id, value)`

更新概念激活度。

---

### AssociationService

关联相关的业务逻辑。

#### `create(fromId, toId, type, weight)`

创建关联。

#### `createFromEntities(entities)`

从实体列表批量创建关联。

#### `getNetwork(conceptId, depth)`

获取概念的关联网络。

#### `findPath(fromId, toId, maxDepth)`

查找概念间的路径。

---

## 事务管理

使用 UnitOfWork 模式确保数据一致性。

```javascript
const { UnitOfWork } = require('./src/repositories/UnitOfWork.js');

// 方式1: 自动事务
await UnitOfWork.withTransaction(pool, async (uow) => {
  const memRepo = new MemoryRepository(uow.getQueryClient());
  const conceptRepo = new ConceptRepository(uow.getQueryClient());
  
  await memRepo.create(memory);
  await conceptRepo.create(concept);
  // 自动提交或回滚
});

// 方式2: 手动控制
const uow = new UnitOfWork(pool);
try {
  await uow.begin();
  // ... 操作
  await uow.commit();
} catch (e) {
  await uow.rollback();
  throw e;
}
```

---

## 测试

### 运行测试

```bash
# 运行所有测试
./tests/run.sh

# 运行特定测试
node tests/v5.test.cjs
```

### 测试覆盖

- 数据库连接
- 记忆编码/检索
- 概念管理
- 关联网络

---

## 配置

配置文件: `config.json`

```json
{
  "version": "5.3.25",
  "storage": {
    "primary": {
      "type": "postgresql",
      "host": "${PGHOST}",
      "port": "${PGPORT}",
      "database": "${PGDATABASE}",
      "user": "${PGUSER}",
      "password": "${PGPASSWORD}"
    },
    "cache": {
      "type": "redis",
      "host": "${REDIS_HOST}",
      "port": "${REDIS_PORT}"
    }
  },
  "memory": { ... },
  "forgetting": { ... },
  "proactive": { ... }
}
```

---

## 最佳实践

### 1. 错误处理

```javascript
try {
  const memory = await brain.encode(content, metadata);
} catch (e) {
  logger.error('brain', 'encode failed', { error: e.message });
}
```

### 2. 批量操作

```javascript
// 使用事务包裹批量操作
await brain.transaction(async (uow) => {
  for (const item of items) {
    await memRepo.create(item);
  }
});
```

### 3. 性能优化

- 使用 `recall` 而非 `findAll` 进行搜索
- 限制返回数量 (`limit`)
- 使用事务减少数据库往返

---

## 迁移指南

### 从 v4.x 迁移到 v5.0

1. **数据库**: 无需修改，表结构兼容
2. **代码**: 更新导入路径
   ```javascript
   // v4.x
   const { encode } = require('./scripts/core/encode.cjs');
   
   // v5.0
   const { CognitiveBrain } = require('./src/index.js');
   const brain = new CognitiveBrain();
   await brain.encode(...);
   ```
3. **CLI**: 命令保持不变

---

## 常见问题

### Q: 如何清理测试数据？

```sql
DELETE FROM episodes WHERE type = 'test';
DELETE FROM concepts WHERE name LIKE 'test-%';
```

### Q: 如何备份记忆？

```bash
pg_dump cognitive_brain > backup.sql
```

### Q: 如何调试？

```javascript
const logger = require('./src/utils/logger.js');
logger.setLevel('DEBUG');
```

---

## 贡献

1. Fork 仓库
2. 创建分支 (`git checkout -b feature/xxx`)
3. 提交修改 (`git commit -m 'Add feature'`)
4. 推送分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

---

## 许可

MIT License

