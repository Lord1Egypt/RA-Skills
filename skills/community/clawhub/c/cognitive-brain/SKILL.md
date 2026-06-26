# 🧠 Cognitive Brain

> **跨会话记忆与认知系统 v5.0** | Cross-Session Memory & Cognition System
> 
> 让 AI 拥有像人类一样的记忆、思考和预测能力

**Version: 7.0.1** | **License: MIT**

---

## ✨ 功能特性 | Features

| 功能 | Feature | 描述 |
|------|---------|------|
| 🔄 实时共享 | Real-time Sharing | 跨会话毫秒级记忆同步 |
| 🧠 四层记忆 | Four-Layer Memory | 感官/工作/情景/语义记忆架构 |
| 💭 自由思考 | Free Thinking | 非任务驱动的意识流思考 |
| 🔮 智能预测 | Prediction | 预测用户需求，预加载记忆 |
| 📊 可视化 | Visualization | 知识图谱、时间线、摘要 |
| 🔗 联想网络 | Association Network | 概念关联，激活扩散算法 |
| 🏗️ 分层架构 | Layered Architecture | Domain/Repository/Service 分层设计 |
| 🔒 事务安全 | Transaction Safety | UnitOfWork 确保数据一致性 |
| 📚 完整文档 | Documentation | API 文档 + 架构文档 |
| ✅ 测试覆盖 | Test Coverage | 自动化测试套件 |

---

## 🚀 快速开始 | Quick Start

### 一键安装 | Quick Install

```bash
# 方式1: ClawHub 安装（推荐）
clawhub install cognitive-brain
cd ~/.openclaw/workspace/skills/cognitive-brain
npm run setup:auto    # 非交互模式，自动安装所有依赖

# 方式2: 手动安装
cd ~/.openclaw/workspace/skills/cognitive-brain
npm install
npm run setup         # 交互式配置
```

### 安装模式 | Install Modes

| 命令 | 说明 |
|------|------|
| `npm run check` | 检查系统依赖（PostgreSQL, Redis, pgvector） |
| `npm run setup` | 交互式安装，会提示输入数据库配置 |
| `npm run setup:auto` | 自动安装，使用默认配置，自动安装缺失依赖 |
| `npm run setup:resume` | 从断点恢复安装（安装失败后使用） |
| `npm run health` | 健康检查 |
| `npm run reset` | 重置数据库（清空记忆，保留表结构） |
| `npm run uninstall` | 卸载（清理数据库、hooks、配置文件） |

### 安装特性 | Install Features

| 特性 | 说明 |
|------|------|
| 🔄 断点恢复 | 安装失败后运行 `npm run setup:resume` 继续 |
| 📋 安装日志 | 记录到 `install.log`，便于排查问题 |
| 🔍 已安装检测 | 自动检测是否已安装，避免重复 |
| ⚡ 一键安装 | `installCommand` 自动执行完整安装流程 |

### 系统要求 | Requirements

| 依赖 | 版本 | 安装命令 (Ubuntu) |
|------|------|-------------------|
| Node.js | >= 18 | `apt install nodejs npm` |
| PostgreSQL | >= 14 | `apt install postgresql` |
| Redis | >= 6 | `apt install redis-server` |
| pgvector | - | `apt install postgresql-16-pgvector` |

> 💡 `npm run setup:auto` 会自动安装这些依赖（需要 root 权限）

### 基础使用 | Basic Usage

```javascript
const { CognitiveBrain } = require('./src/index.js');
const brain = new CognitiveBrain();

// 存储记忆
const memory = await brain.encode('用户的项目叫 Alpha', {
  type: 'conversation',
  importance: 0.8
});

// 检索记忆
const memories = await brain.recall('项目');

// 获取统计
const stats = await brain.stats();
```

### CLI 工具

```bash
# 编码记忆
node scripts/core/encode.cjs "内容" -t conversation -i 0.8

# 检索记忆
node scripts/core/recall.cjs --query "关键词" --limit 5

# 健康检查
node scripts/tools/health_check.cjs

# 运行测试
./tests/run.sh
```

---

## 🏗️ 架构概览 | Architecture

### v5.0 分层架构

```
┌─────────────────────────────────────────────────────────────┐
│                      API / CLI 层                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  REST API  │  │   CLI      │  │   Hook     │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                   Service 层                                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   Memory   │  │   Concept  │  │ Association│            │
│  │   Service  │  │   Service  │  │   Service  │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                Repository 层                                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   Memory   │  │   Concept  │  │ Association│            │
│  │ Repository │  │ Repository │  │ Repository │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                      UnitOfWork (事务)                      │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                  Domain 层                                  │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   Memory   │  │   Concept  │  │ Association│            │
│  │   Entity   │  │   Entity   │  │   Entity   │            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│              持久层 | Persistence                           │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │  PostgreSQL│  │   Redis    │  │   Files    │            │
│  │  (主存储)   │  │  (缓存)     │  │  (配置/日志)│            │
│  └────────────┘  └────────────┘  └────────────┘            │
└─────────────────────────────────────────────────────────────┘
```

### 设计原则

1. **单一职责**: 每个模块只做一件事
2. **依赖注入**: 通过参数传入依赖，不直接创建
3. **接口隔离**: 清晰的模块边界
4. **事务安全**: 多表操作原子性保证

---

## 🧠 四层记忆模型 | Four-Layer Memory

| 层级 | Layer | Duration | Purpose | Description |
|------|-------|---------|---------|-------------|
| 感官记忆 | Sensory | Milliseconds | Buffer | Transient sensory buffer for immediate perception |
| 工作记忆 | Working | Minutes~Hours | Active Processing | Active processing workspace for current tasks |
| 情景记忆 | Episodic | Long-term | Experiences | Personal experiences and events with context |
| 语义记忆 | Semantic | Long-term | Knowledge | Facts, concepts, and structured knowledge |

---

## 📚 核心 API

### CognitiveBrain

主入口类，提供统一的操作接口。

```javascript
const { CognitiveBrain } = require('./src/index.js');
const brain = new CognitiveBrain();

// 编码记忆
const memory = await brain.encode(content, {
  type: 'conversation',
  importance: 0.8,
  sourceChannel: 'qq'
});

// 检索记忆
const memories = await brain.recall('关键词', { limit: 10 });

// 事务操作
await brain.transaction(async (uow) => {
  // 多表原子操作
});

// 获取统计
const stats = await brain.stats();
```

### 实体模型

#### Memory (记忆)
```javascript
{
  id: 'uuid',
  content: '记忆内容',
  type: 'episodic',
  importance: 0.5,
  sourceChannel: 'qq',
  role: 'user',
  entities: ['关键词'],
  emotions: { valence: 0, arousal: 0 },
  createdAt: Date,
  updatedAt: Date
}
```

#### Concept (概念)
```javascript
{
  id: 'uuid',
  name: '概念名称',
  type: 'general',
  importance: 0.5,
  activation: 0.0,
  accessCount: 0
}
```

#### Association (关联)
```javascript
{
  id: 'uuid',
  fromId: '概念A-ID',
  toId: '概念B-ID',
  type: 'related',
  weight: 0.5
}
```

---

## 🔒 事务管理

使用 UnitOfWork 模式确保数据一致性：

```javascript
const { UnitOfWork } = require('./src/repositories/UnitOfWork.js');
const { MemoryRepository } = require('./src/repositories/MemoryRepository.js');

// 自动事务
await UnitOfWork.withTransaction(pool, async (uow) => {
  const memRepo = new MemoryRepository(uow.getQueryClient());
  const conceptRepo = new ConceptRepository(uow.getQueryClient());
  
  await memRepo.create(memory);
  await conceptRepo.create(concept);
  // 自动 commit 或 rollback
});
```

---

## 🧪 测试

```bash
# 运行所有测试
./tests/run.sh

# 运行特定测试
node tests/v5.test.cjs
node tests/db.test.cjs
node tests/memory.test.cjs

# 健康检查
node scripts/tools/health_check.cjs
```

---

## 📖 文档

- [API 文档](./docs/README.md) - 完整 API 参考
- [架构文档](./docs/ARCHITECTURE.md) - 架构设计说明

---

## 🔄 共享工作区 | Shared Workspace

### 核心表 | Core Tables

| 表名 | 用途 | 说明 |
|------|------|------|
| `episodes` | 情景记忆 | 存储对话和事件 |
| `concepts` | 概念节点 | 提取的实体和关键词 |
| `associations` | 概念关联 | 概念间的关系 |
| `system_memory` | 系统配置 | 全局设置和状态 |

### Hook 集成

自动集成到 OpenClaw 消息流程：

```
用户消息 → Hook(cognitive-recall) → 检索记忆 → 注入上下文 → AI回复 → 编码记忆
```

---

## 🔧 配置

```json
{
  "version": "5.3.25",
  "storage": {
    "primary": {
      "type": "postgresql",
      "host": "localhost",
      "port": 5432,
      "database": "cognitive_brain"
    },
    "cache": {
      "type": "redis",
      "host": "localhost",
      "port": 6379
    }
  }
}
```

---

## 📈 版本历史

### v7.0.1 (2026-03-21)
- 🔧 **记忆系统重构** - 修复 Hook 触发问题，改用 Cron 方案
- ✨ **记忆读取** - `agent:bootstrap` Hook 即时注入记忆
- ✨ **记忆写入** - Cron 每 1 分钟扫描会话文件
- 🗑️ **清理无用脚本** - 删除 20+ 不常用脚本
- 📝 **文档更新** - 简化架构说明

### v5.3.32 (2026-03-21)
- 🐛 **修复类型验证** - `type: 'conversation'` 改为有效类型 `'episodic'`
- 🐛 **修复 Embedding 路径** - embed.py 路径错误导致 embedding 生成失败

### v5.3.22 (2026-03-20)
- 发布版本更新

### v5.3.11 (2026-03-18)
- 🧪 **测试覆盖率提升** - 新增 Repository/Service/API 测试 (7个测试文件)
- 🧹 **事件监听器清理** - 优雅关闭时清理所有监听器，防止内存泄漏
- 💓 **WebSocket 心跳** - 30秒 ping/pong 检测，120秒无响应自动断开
- ⚡ **N+1 查询优化** - 批量插入从 O(N) 优化为 O(1)
- 🔒 **API 速率限制** - 100 req/min 限流保护

### v5.3.7 (2026-03-18)
- 🗑️ **删除重复文档** - 删除 README.md，统一文档入口
- 🔧 **统一代码规范** - 修复 80+ 文件缺少换行符
- 🔧 **统一 Logger** - Winston logger 替代 console.log
- 🔒 **事务安全** - 隔离级别 + 死锁重试 + 熔断器
- ⚙️ **配置增强** - 连接池可配置 + 日志配置

### v5.3.20 (2026-03-19)
- ✨ **安装流程优化** - 非交互模式、断点恢复、安装日志
- ✨ **Skill.json installCommand** - 支持一键自动安装
- ✨ **卸载脚本** - `npm run uninstall` 清理所有组件
- ✨ **重置脚本** - `npm run reset` 清空记忆数据
- 🔧 **修复 create_indexes.cjs** - 模块路径错误
- 🔧 **修复 health_check.cjs** - SQL 语法错误
- 📝 **文档更新** - 安装指南、命令说明

### v5.0.0 (2026-03-18)
- ✨ 重构为分层架构 (Domain/Repository/Service)
- ✨ 添加 UnitOfWork 事务管理
- ✨ 添加领域模型验证
- ✨ 添加测试框架 (13个测试)
- ✨ 添加统一日志模块
- ✨ 添加配置管理器
- ✅ 修复 Pool 连接泄漏
- ✅ 修复空 catch 块
- ✅ 移除文件 fallback，强制数据库优先

### v4.1.0 (Previous)
- 基础记忆功能
- 联想网络
- 预测预加载
- 心跳反思
- 自由思考

---

## 🤝 贡献

1. Fork 仓库
2. 创建分支 (`git checkout -b feature/xxx`)
3. 提交修改 (`git commit -m 'Add feature'`)
4. 推送分支 (`git push origin feature/xxx`)
5. 创建 Pull Request

---

## 📄 许可

MIT License

---

**让 AI 拥有记忆，让对话更有温度** ❤️

