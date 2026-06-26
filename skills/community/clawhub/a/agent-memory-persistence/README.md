# agent-memory-persistence

为 AI Agent 提供长期记忆存储能力，基于 TypeScript、Node.js 和 SQLite 实现。

## 功能

- 记忆存储：文本、结构化元数据、向量嵌入
- 向量检索：基于余弦相似度的语义搜索
- 记忆管理：增删改查、过期清理、统计
- 会话关联：按 `userId`、`sessionId`、时间范围查询

## 安装

```bash
npm install
```

## 开发

```bash
npm run typecheck
npm test
npm run build
```

## 快速使用

```ts
import { MemoryManager } from "agent-memory-persistence";

const manager = new MemoryManager({ dbPath: "./agent-memory.db" });

const memory = manager.create({
  userId: "user-123",
  sessionId: "session-456",
  type: "fact",
  content: "用户偏好简洁回答",
  metadata: { source: "conversation", confidence: 0.92 },
  embedding: [0.12, 0.44, 0.91],
});

const related = manager.searchByVector([0.1, 0.4, 0.9], {
  userId: "user-123",
  limit: 5,
});

const sessionMemories = manager.listBySession("session-456");

manager.cleanupExpired();
manager.close();
```

## API 概览

### `MemoryManager`

- `create(input)`: 创建记忆
- `get(id)`: 根据 ID 查询
- `update(id, input)`: 更新记忆
- `delete(id)`: 删除记忆
- `list(filter)`: 按条件批量查询
- `listByUser(userId, limit?)`: 查询用户关联记忆
- `listBySession(sessionId, limit?)`: 查询会话关联记忆
- `searchByVector(embedding, options?)`: 语义检索
- `cleanupExpired(referenceTime?)`: 清理过期记忆
- `stats()`: 返回统计信息
- `close()`: 关闭数据库连接

## 数据模型

每条记忆记录包含：

- `id`: UUID
- `userId`: 用户 ID
- `sessionId`: 会话 ID
- `type`: 记忆类型，默认 `note`
- `content`: 文本内容
- `metadata`: 任意 JSON 结构化数据
- `embedding`: `number[]`
- `createdAt` / `updatedAt`
- `expiresAt`

## 设计说明

- 持久层使用 `better-sqlite3`，适合本地 Agent 场景下的低延迟同步访问。
- 向量数据以 JSON 数组形式存入 SQLite，便于迁移和调试。
- 当前语义检索采用全量扫描 + 余弦相似度，适合中小规模记忆库；未来可替换成 ANN 或 SQLite 向量扩展。
