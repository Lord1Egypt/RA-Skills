# 自进化系统文档

> 从每次任务中学习、改进、沉淀最佳实践

## 📋 目录

- [概述](#概述)
- [WAL 协议](#wal-协议)
- [Working Buffer](#working-buffer)
- [Compaction Recovery](#compaction-recovery)
- [模式识别](#模式识别)
- [知识库沉淀](#知识库沉淀)
- [使用指南](#使用指南)

---

## 概述

自进化系统让多比能够从每次任务中学习，持续改进工作流和最佳实践，防止上下文丢失和知识遗忘。

### 核心组件

| 组件 | 位置 | 说明 |
|------|------|------|
| WAL Protocol | `memory/wal.js` | 预写日志协议 |
| Working Buffer | `memory/working-buffer.js` | 工作缓冲区 |
| Session State | `memory/templates/SESSION-STATE.md` | 会话状态模板 |
| Compaction | `memory/wal.js` | 日志压缩恢复 |

### 设计原则

1. **持久化优先** - 所有状态变更先写日志
2. **可恢复** - 崩溃后能恢复到一致状态
3. **可追溯** - 完整记录决策过程
4. **可学习** - 从成功和失败中提取模式
5. **可沉淀** - 将经验转化为最佳实践

---

## WAL 协议

### 什么是 WAL？

WAL (Write-Ahead Logging) 是一种确保数据持久性的协议：
- 所有变更先写入日志
- 日志写入成功后才算提交
- 崩溃后可通过日志恢复

### 使用示例

```javascript
import { WALProtocol } from './memory/wal.js';

const wal = new WALProtocol({
  walDir: './memory/wal',
  enableCompaction: true,
  compactionThreshold: 1000,
});

// 开始事务
await wal.begin('task-123', {
  type: 'code-review',
  prNumber: 456,
});

// 记录关键事件
await wal.log('task-123', 'start', {
  files: ['a.js', 'b.js'],
});

await wal.log('task-123', 'progress', {
  completed: 2,
  total: 5,
});

await wal.log('task-123', 'complete', {
  result: 'success',
  score: 0.85,
});

// 提交事务
await wal.commit('task-123');
```

### 日志条目类型

| 类型 | 说明 | 用途 |
|------|------|------|
| BEGIN | 事务开始 | 标记事务起点 |
| DATA | 数据变更 | 记录中间状态 |
| COMMIT | 事务提交 | 标记成功完成 |
| ABORT | 事务回滚 | 标记失败取消 |
| CHECKPOINT | 检查点 | 加速恢复 |

### 恢复流程

```javascript
// 系统启动时自动恢复
const recovery = await wal.recover();

console.log(`发现 ${recovery.incomplete.length} 个未完成的事务`);

for (const tx of recovery.incomplete) {
  console.log(`事务 ${tx.transactionId} 状态：${tx.status}`);
  // 可以选择重试或清理
}
```

---

## Working Buffer

### 什么是 Working Buffer？

Working Buffer 是一个持久化的键值存储，用于：
- 保存中间状态
- 防止上下文丢失
- 支持跨会话恢复

### 使用示例

```javascript
import { WorkingBuffer } from './memory/working-buffer.js';

const buffer = new WorkingBuffer({
  bufferDir: './memory/buffer',
  autoSave: true,
  autoSaveInterval: 60000,  // 60 秒自动保存
  maxAge: 7 * 24 * 60 * 60 * 1000,  // 7 天过期
});

// 保存状态
await buffer.set('task-123', {
  status: 'running',
  progress: 50,
  currentFile: 'src/auth.js',
  issues: [...],
});

// 获取状态
const { found, value } = await buffer.get('task-123');

if (found) {
  console.log(`任务进度：${value.progress}%`);
}

// 更新状态
await buffer.set('task-123', {
  ...value,
  progress: 75,
  currentFile: 'src/user.js',
});

// 获取带元数据的状态
const { found, value, metadata, version } = await buffer.get('task-123', {
  withMetadata: true,
});

console.log(`版本：${version}, 访问次数：${metadata.accessCount}`);
```

### 自动清理

```javascript
// 定期清理过期条目
setInterval(async () => {
  const { cleaned } = await buffer.cleanup();
  console.log(`清理了 ${cleaned} 个过期条目`);
}, 60 * 60 * 1000);  // 每小时
```

### 统计信息

```javascript
const stats = buffer.getStats();
console.log(stats);

// 输出：
// {
//   count: 15,
//   totalAccessCount: 234,
//   oldestUpdate: '2026-04-17T10:00:00.000Z',
//   newestUpdate: '2026-04-18T08:00:00.000Z',
//   autoSaveEnabled: true,
//   maxAge: '168h'
// }
```

---

## Compaction Recovery

### 什么是 Compaction？

Compaction 是日志压缩过程：
- 合并多个日志段
- 移除已提交/回滚的事务
- 只保留活跃状态
- 减少恢复时间

### 压缩策略

```javascript
const wal = new WALProtocol({
  enableCompaction: true,
  compactionThreshold: 1000,  // 日志条数达到阈值时触发
  maxSegmentSize: 10 * 1024 * 1024,  // 10MB 轮换日志文件
});
```

### 压缩流程

```
原始日志:
- BEGIN tx-1
- DATA tx-1 (step 1)
- DATA tx-1 (step 2)
- COMMIT tx-1        ← 已提交
- BEGIN tx-2
- DATA tx-2 (step 1)
- ABORT tx-2         ← 已回滚
- BEGIN tx-3
- DATA tx-3 (step 1) ← 活跃

压缩后:
- BEGIN tx-1
- COMMIT tx-1
- BEGIN tx-3
- DATA tx-3 (step 1)
```

### 手动触发压缩

```javascript
await wal.compact();
```

---

## 模式识别

### 什么是模式识别？

模式识别是从重复任务中自动发现最佳实践：

```
任务类型：代码审查
执行次数：50
平均耗时：120s
成功率：95%

常见模式:
1. 先检查代码风格 → 再检查安全 → 最后检查性能
2. 文件数 > 10 时，分组并行处理
3. 发现严重问题时，立即停止并报告
```

### 实现示例

```javascript
class PatternRecognizer {
  constructor() {
    this.patterns = new Map();
  }

  /**
   * 记录任务执行
   */
  record(taskType, execution) {
    if (!this.patterns.has(taskType)) {
      this.patterns.set(taskType, []);
    }
    
    this.patterns.get(taskType).push({
      timestamp: Date.now(),
      duration: execution.duration,
      success: execution.success,
      steps: execution.steps,
      issues: execution.issues,
    });
  }

  /**
   * 识别模式
   */
  recognize(taskType) {
    const executions = this.patterns.get(taskType);
    
    if (!executions || executions.length < 5) {
      return null;  // 数据不足
    }

    // 分析成功执行
    const successful = executions.filter(e => e.success);
    const avgDuration = successful.reduce((sum, e) => sum + e.duration, 0) / successful.length;
    
    // 提取常见步骤序列
    const stepSequences = successful.map(e => e.steps.join(' → '));
    const commonSequence = this.findMostCommon(stepSequences);
    
    // 提取常见问题
    const allIssues = successful.flatMap(e => e.issues);
    const frequentIssues = this.findFrequent(allIssues);
    
    return {
      taskType,
      executions: executions.length,
      successRate: successful.length / executions.length,
      avgDuration,
      bestPractice: commonSequence,
      commonIssues: frequentIssues,
      recommendations: this.generateRecommendations(successful),
    };
  }

  findMostCommon(sequences) {
    const counts = {};
    for (const seq of sequences) {
      counts[seq] = (counts[seq] || 0) + 1;
    }
    return Object.entries(counts).sort((a, b) => b[1] - a[1])[0]?.[0];
  }

  findFrequent(items, threshold = 0.3) {
    const counts = {};
    for (const item of items) {
      counts[item] = (counts[item] || 0) + 1;
    }
    
    const minCount = items.length * threshold;
    return Object.entries(counts)
      .filter(([_, count]) => count >= minCount)
      .map(([item, count]) => ({ item, count }));
  }

  generateRecommendations(executions) {
    const recommendations = [];
    
    // 分析耗时
    const slowExecutions = executions.filter(e => e.duration > 300000);
    if (slowExecutions.length > executions.length * 0.3) {
      recommendations.push({
        type: 'performance',
        suggestion: '考虑增加并行度或优化任务分解',
      });
    }
    
    // 分析失败
    const failedExecutions = executions.filter(e => !e.success);
    if (failedExecutions.length > 0) {
      const commonFailures = this.findFrequent(
        failedExecutions.flatMap(e => e.issues || [])
      );
      recommendations.push({
        type: 'reliability',
        suggestion: `注意避免以下问题：${commonFailures.map(i => i.item).join(', ')}`,
      });
    }
    
    return recommendations;
  }
}
```

---

## 知识库沉淀

### 学习日志系统

```markdown
# .learnings/LEARNINGS.md

## 2026-04-18: Harness Engineering 能力建设

### 学到了什么
- 多 Agent 编排的 5 种核心模式
- 工作流的可复用设计方法
- WAL 协议确保状态持久性

### 最佳实践
1. 并行优先：能并行的任务绝不串行
2. 容错设计：单个子任务失败不影响整体
3. 日志先行：所有状态变更先写 WAL

### 待改进
- 需要更多真实场景测试
- 错误处理可以更细粒度
```

### 错误日志

```markdown
# .learnings/ERRORS.md

## 2026-04-18: 任务分解失败

### 错误信息
```
Error: Task decomposition failed: max retries exceeded
```

### 根本原因
- 任务描述过于模糊
- 缺少必要的上下文

### 解决方案
- 增加任务描述详细度要求
- 自动补充项目上下文

### 预防措施
- 添加任务描述验证
- 提供任务描述模板
```

### 功能请求

```markdown
# .learnings/FEATURE_REQUESTS.md

## 2026-04-18: 支持 DAG 任务分解

### 需求描述
当前支持的模式无法表达复杂的依赖关系

### 使用场景
- 构建系统：复杂依赖图
- 数据处理：多源数据汇聚

### 优先级
Medium

### 实现建议
- 使用拓扑排序确定执行顺序
- 支持动态添加依赖
```

---

## 使用指南

### 完整示例：带恢复的任务执行

```javascript
import { WALProtocol } from './memory/wal.js';
import { WorkingBuffer } from './memory/working-buffer.js';

async function executeTaskWithRecovery(taskId, taskFn) {
  const wal = new WALProtocol();
  const buffer = new WorkingBuffer();
  
  // 检查是否有未完成的任务
  const recovery = await wal.recover();
  const incomplete = recovery.incomplete.find(tx => 
    tx.metadata?.taskId === taskId
  );
  
  if (incomplete) {
    console.log(`发现未完成的任务 ${taskId}，尝试恢复...`);
    
    // 从缓冲区恢复状态
    const { found, value } = await buffer.get(taskId);
    if (found) {
      console.log(`恢复到进度：${value.progress}%`);
      return continueTask(value);
    }
  }
  
  // 开始新任务
  await wal.begin(taskId, { taskId, type: 'custom' });
  
  try {
    // 初始化状态
    const state = { progress: 0, status: 'running' };
    await buffer.set(taskId, state);
    await wal.log(taskId, 'start', state);
    
    // 执行任务
    const result = await taskFn((progress) => {
      // 定期保存进度
      buffer.set(taskId, { ...state, progress });
      wal.log(taskId, 'progress', { progress });
    });
    
    // 完成任务
    await wal.log(taskId, 'complete', { result });
    await wal.commit(taskId);
    await buffer.delete(taskId);  // 清理
    
    return result;
    
  } catch (error) {
    // 记录错误
    await wal.log(taskId, 'error', { error: error.message });
    await wal.abort(taskId);
    
    // 保留状态以便恢复
    await buffer.set(taskId, {
      ...state,
      status: 'failed',
      error: error.message,
    });
    
    throw error;
  }
}

// 使用示例
executeTaskWithRecovery('task-123', async (updateProgress) => {
  for (let i = 0; i <= 100; i += 10) {
    await doWork();
    updateProgress(i);
  }
  return { success: true };
});
```

---

## 文件结构

```
memory/
├── wal.js                    # WAL 协议实现 (12KB)
├── working-buffer.js         # 工作缓冲区 (8KB)
├── templates/
│   └── SESSION-STATE.md      # 会话状态模板 (2KB)
└── wal/                      # WAL 日志目录
│   ├── wal-000000.log
│   ├── wal-000001.log
│   └── ...
└── buffer/
│   └── buffer.json           # 缓冲区数据
```

**总计**: ~22KB 核心代码

---

## 下一步

- [ ] 实现真实的模式识别算法
- [ ] 添加自动化建议生成
- [ ] 集成到所有工作流
- [ ] 支持分布式 WAL
- [ ] 添加可视化恢复界面

---

*文档版本：1.0 | 最后更新：2026-04-18 | 作者：多比 🧦*
