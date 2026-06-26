# Cognitive Brain v5.0 架构文档

## 架构目标

1. **单一职责**: 每个模块只做一件事
2. **依赖注入**: 不直接创建依赖，通过参数传入
3. **接口隔离**: 清晰的模块边界
4. **事务安全**: 多表操作原子性

## 分层架构

### Domain Layer (领域层)

**职责**: 定义业务实体和规则

**实体**:
- `Memory`: 记忆实体，包含内容、类型、重要性等
- `Concept`: 概念实体，表示提取的关键词
- `Association`: 关联实体，表示概念间关系

**特点**:
- 纯数据 + 业务逻辑
- 自带验证
- 不依赖外部服务

```javascript
class Memory extends BaseEntity {
  constructor(data) {
    this.validate(); // 构造时自动验证
  }
  
  validate() {
    if (this.content.length < 3) {
      throw new ValidationError('Content too short');
    }
  }
}
```

### Repository Layer (仓储层)

**职责**: 数据访问，隔离数据库细节

**组件**:
- `BaseRepository`: 基础 CRUD
- `MemoryRepository`: 记忆查询
- `ConceptRepository`: 概念查询
- `AssociationRepository`: 关联查询
- `UnitOfWork`: 事务管理

**特点**:
- 每个实体对应一个 Repository
- 支持复杂查询
- 事务由 UnitOfWork 管理

```javascript
class MemoryRepository extends BaseRepository {
  async search(query, options) {
    // 实现搜索逻辑
  }
  
  async findImportant(minImportance, types) {
    // 实现高重要性查询
  }
}
```

### Service Layer (服务层)

**职责**: 业务逻辑编排

**服务**:
- `MemoryService`: 记忆业务逻辑
- `ConceptService`: 概念业务逻辑
- `AssociationService`: 关联业务逻辑

**特点**:
- 组合多个 Repository 操作
- 实现跨实体的业务规则
- 使用 UnitOfWork 确保事务

```javascript
class MemoryService {
  async encode(content, metadata) {
    // 1. 创建记忆实体
    // 2. 提取概念
    // 3. 事务保存
    await UnitOfWork.withTransaction(this.pool, async (uow) => {
      await memRepo.create(memory);
      await conceptRepo.create(concept);
    });
  }
}
```

## 数据流

```
用户请求
   ↓
CognitiveBrain (入口)
   ↓
Service (业务逻辑)
   ↓
Repository (数据访问) → UnitOfWork (事务)
   ↓
Database (PostgreSQL)
```

## 事务管理

### 自动事务 (推荐)

```javascript
await UnitOfWork.withTransaction(pool, async (uow) => {
  const memRepo = new MemoryRepository(uow.getQueryClient());
  const conceptRepo = new ConceptRepository(uow.getQueryClient());
  
  await memRepo.create(memory);
  await conceptRepo.create(concept);
  // 成功自动 commit，失败自动 rollback
});
```

### 手动事务

```javascript
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

## 实体关系

```
Memory (1) --- (N) Concept (通过 entities 字段)
Concept (N) --- (N) Concept (通过 Association)
```

## 扩展性设计

### 添加新实体

1. 创建 Domain 实体
2. 创建 Repository
3. 创建 Service
4. 注册到 CognitiveBrain

### 添加新功能

1. 在相应 Service 添加方法
2. 如需新查询，在 Repository 添加
3. 更新文档

## 性能考虑

1. **连接池**: 使用单例 Pool
2. **查询优化**: Repository 提供专用查询方法
3. **批量操作**: 支持批量插入/删除
4. **事务范围**: 最小化事务范围

## 错误处理

```
Domain Layer: ValidationError
Repository Layer: DatabaseError
Service Layer: BusinessError
API Layer: HTTPError
```

## 测试策略

- **单元测试**: Domain 实体逻辑
- **集成测试**: Repository + Database
- **E2E测试**: 完整业务流程

## 与其他组件的关系

```
OpenClaw
  ↓ (hook)
CognitiveBrain
  ↓ (recall/encode)
Hook (cognitive-recall/handler.js)
  ↓ (调用)
Service/Repository
```

