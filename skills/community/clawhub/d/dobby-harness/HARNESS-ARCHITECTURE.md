# Harness Engineering 架构文档

> 多 Agent 编排、任务分解、并行执行、生产级工作流

## 📋 目录

- [概述](#概述)
- [核心组件](#核心组件)
- [任务分解模式](#任务分解模式)
- [通信协议](#通信协议)
- [执行流程](#执行流程)
- [错误处理](#错误处理)
- [使用示例](#使用示例)

---

## 概述

Harness Engineering 是一个多 Agent 编排系统，用于将复杂任务分解为可并行执行的子任务，协调多个子 Agent 协同工作，并聚合验证最终结果。

### 设计原则

1. **单一职责** - 每个 Agent 只负责一个明确的子任务
2. **并行优先** - 能并行的任务绝不串行
3. **容错设计** - 单个子任务失败不影响整体流程
4. **可追溯** - 所有执行过程有完整日志
5. **可复用** - 模式库支持快速组装新工作流

---

## 核心组件

### 1. Orchestrator (编排器)

**位置**: `harness/orchestrator.js`

核心职责：
- 接收复杂任务，进行任务分解
- 创建和管理子 Agent 会话
- 调度任务执行（并行/串行）
- 聚合子任务结果
- 验证最终输出质量

```javascript
// 核心 API
const orchestrator = new HarnessOrchestrator({
  maxParallel: 5,           // 最大并行数
  timeoutSeconds: 300,      // 单个任务超时
  retryAttempts: 2,         // 失败重试次数
});

// 执行任务
const result = await orchestrator.execute({
  task: "复杂任务描述",
  decomposition: "sequential" | "parallel" | "hybrid",
  context: { /* 上下文数据 */ }
});
```

### 2. Task Queue (任务队列)

**位置**: `harness/queue.js`

职责：
- 维护待执行任务队列
- 优先级调度
- 并发控制
- 任务状态追踪

### 3. Result Aggregator (结果聚合器)

**位置**: `harness/aggregator.js`

职责：
- 收集子任务输出
- 冲突检测与解决
- 结果合并与格式化
- 质量验证

---

## 任务分解模式

### 模式库位置：`harness/patterns/`

| 模式 | 描述 | 适用场景 |
|------|------|----------|
| `sequential.js` | 顺序执行，后一任务依赖前一任务输出 | 流水线处理、编译构建 |
| `parallel.js` | 完全并行，任务间无依赖 | 独立子任务、批量处理 |
| `map-reduce.js` | 先并行处理再聚合结果 | 数据分析、批量转换 |
| `fan-out.js` | 一个任务分解为多个独立子任务 | 多方案探索、A/B 测试 |
| `pipeline.js` | 多阶段流水线，每阶段可并行 | 代码审查→测试→部署 |
| `dag.js` | 有向无环图，复杂依赖关系 | 复杂工作流编排 |

### 模式示例：Parallel Pattern

```javascript
// harness/patterns/parallel.js
export const parallelPattern = {
  name: 'parallel',
  decompose: async (task, context) => {
    // 将任务分解为独立子任务
    return [
      { id: 'sub-1', task: '...', dependencies: [] },
      { id: 'sub-2', task: '...', dependencies: [] },
      { id: 'sub-3', task: '...', dependencies: [] },
    ];
  },
  aggregate: async (results) => {
    // 合并所有结果
    return results.filter(r => r.success).map(r => r.output);
  }
};
```

---

## 通信协议

### Agent 间消息格式

```json
{
  "messageId": "uuid",
  "type": "task-request" | "task-response" | "status-update" | "error",
  "from": "orchestrator" | "agent-id",
  "to": "agent-id" | "orchestrator",
  "timestamp": "ISO-8601",
  "payload": {
    "taskId": "uuid",
    "task": "任务描述",
    "context": { /* 共享上下文 */ },
    "deadline": "ISO-8601"
  }
}
```

### 状态机

```
┌─────────┐     ┌──────────┐     ┌──────────┐     ┌─────────┐
│ PENDING │────▶│ RUNNING  │────▶│ COMPLETED│     │ FAILED  │
└─────────┘     └──────────┘     └──────────┘     └─────────┘
                      │                                   │
                      │ timeout/error                     │ retry
                      ▼                                   │
                ┌──────────┐                             │
                │  FAILED  │─────────────────────────────┘
                └──────────┘
```

---

## 执行流程

```
┌─────────────────────────────────────────────────────────────┐
│                      1. 接收任务                            │
│                   (用户输入复杂任务)                         │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   2. 任务分解                               │
│         (根据模式选择分解策略，生成子任务列表)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   3. 任务调度                               │
│    (根据依赖关系和并发限制，安排执行顺序和并行度)              │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   4. 并行执行                               │
│          (创建子 Agent 会话，分发任务，监控状态)               │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   5. 结果聚合                               │
│         (收集所有输出，检测冲突，合并结果)                    │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   6. 质量验证                               │
│          (检查完整性、一致性，必要时触发重试)                 │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   7. 交付结果                               │
│              (返回最终输出，记录学习日志)                     │
└─────────────────────────────────────────────────────────────┘
```

---

## 错误处理

### 重试策略

```javascript
const retryConfig = {
  maxAttempts: 3,
  backoff: 'exponential',  // exponential | linear | fixed
  initialDelay: 1000,      // ms
  maxDelay: 30000,         // ms
  retryableErrors: [
    'TIMEOUT',
    'NETWORK_ERROR',
    'RATE_LIMITED'
  ]
};
```

### 降级策略

- **部分失败** - 返回已完成部分，标注失败项
- **完全失败** - 返回详细错误信息和恢复建议
- **超时处理** - 终止超时任务，继续其他任务

### 错误分类

| 类型 | 处理策略 |
|------|----------|
| `TIMEOUT` | 重试或标记为失败 |
| `VALIDATION_ERROR` | 不重试，直接失败 |
| `DEPENDENCY_ERROR` | 阻塞依赖任务，等待恢复 |
| `RESOURCE_EXHAUSTED` | 降级执行或排队等待 |

---

## 使用示例

### 示例 1: 并行代码审查

```javascript
const orchestrator = new HarnessOrchestrator();

const result = await orchestrator.execute({
  task: '审查这个 PR 的代码质量',
  context: {
    prNumber: 123,
    files: ['src/a.js', 'src/b.js', 'src/c.js']
  },
  pattern: 'parallel',
  subTasks: [
    { agent: 'linter', task: '检查代码风格' },
    { agent: 'security', task: '检查安全漏洞' },
    { agent: 'performance', task: '检查性能问题' },
    { agent: 'tests', task: '检查测试覆盖率' }
  ]
});

console.log(result.aggregated);
```

### 示例 2: 流水线处理

```javascript
const result = await orchestrator.execute({
  task: '发布新版本',
  pattern: 'pipeline',
  stages: [
    { name: 'build', tasks: ['compile', 'bundle'] },
    { name: 'test', tasks: ['unit-tests', 'integration-tests'] },
    { name: 'deploy', tasks: ['staging', 'production'] }
  ]
});
```

---

## 性能指标

| 指标 | 目标值 | 说明 |
|------|--------|------|
| 任务分解延迟 | < 500ms | 从接收到分解完成 |
| 并行效率 | > 80% | 实际并行度/理论并行度 |
| 任务成功率 | > 95% | 首次执行成功率 |
| 平均执行时间 | 根据任务 | 端到端完成时间 |

---

## 文件结构

```
harness/
├── orchestrator.js       # 核心编排器
├── queue.js              # 任务队列
├── aggregator.js         # 结果聚合器
├── patterns/             # 任务分解模式
│   ├── sequential.js
│   ├── parallel.js
│   ├── map-reduce.js
│   ├── fan-out.js
│   ├── pipeline.js
│   └── dag.js
└── utils/
    ├── logger.js         # 日志工具
    ├── validator.js      # 验证工具
    └── retry.js          # 重试工具
```

---

## 下一步

- [ ] 实现核心编排器 (`orchestrator.js`)
- [ ] 实现任务队列 (`queue.js`)
- [ ] 实现结果聚合器 (`aggregator.js`)
- [ ] 实现所有分解模式
- [ ] 编写单元测试
- [ ] 集成到现有工作流

---

*文档版本: 1.0 | 最后更新: 2026-04-18 | 作者：多比 🧦*
