# Harness Engineering 使用示例

> 多 Agent 编排实战示例

## 📋 目录

- [快速开始](#快速开始)
- [模式示例](#模式示例)
- [实际场景](#实际场景)
- [高级用法](#高级用法)

---

## 快速开始

### 基础用法

```javascript
import { HarnessOrchestrator } from './harness/orchestrator.js';

// 创建编排器
const orchestrator = new HarnessOrchestrator({
  maxParallel: 5,
  timeoutSeconds: 300,
  retryAttempts: 2,
});

// 执行任务
const result = await orchestrator.execute({
  task: '分析这个项目的代码质量',
  pattern: 'parallel',
  subTasks: [
    { task: '检查代码风格', agent: 'linter' },
    { task: '检查安全漏洞', agent: 'security' },
    { task: '检查性能问题', agent: 'performance' },
  ]
});

console.log(result);
```

### 监听事件

```javascript
orchestrator.on('start', ({ task, context }) => {
  console.log(`Starting: ${task}`);
});

orchestrator.on('task-start', (task) => {
  console.log(`Task started: ${task.id}`);
});

orchestrator.on('task-complete', (task) => {
  console.log(`Task completed: ${task.id} (${task.duration}ms)`);
});

orchestrator.on('task-failed', ({ task, error }) => {
  console.error(`Task failed: ${task.id} - ${error}`);
});

orchestrator.on('complete', (result) => {
  console.log(`All done! Success: ${result.success}`);
});
```

---

## 模式示例

### 1. Parallel Pattern - 并行审查

```javascript
// 场景：同时审查多个文件
const result = await orchestrator.execute({
  task: '审查 PR #123 的代码',
  pattern: 'parallel',
  subTasks: [
    { task: '审查 src/auth.js', agent: 'reviewer', context: { file: 'auth.js' } },
    { task: '审查 src/user.js', agent: 'reviewer', context: { file: 'user.js' } },
    { task: '审查 src/api.js', agent: 'reviewer', context: { file: 'api.js' } },
    { task: '审查 tests/auth.test.js', agent: 'reviewer', context: { file: 'auth.test.js' } },
  ]
});

// 结果
console.log(result.outputs); // 所有审查结果
console.log(result.errors);  // 失败的任务
```

### 2. Sequential Pattern - 构建发布

```javascript
// 场景：顺序执行构建发布流程
const result = await orchestrator.execute({
  task: '发布 v2.0.0',
  pattern: 'sequential',
  subTasks: [
    { task: '安装依赖 npm install', agent: 'builder' },
    { task: '编译 TypeScript', agent: 'builder', dependencies: ['task-1'] },
    { task: '运行单元测试', agent: 'tester', dependencies: ['task-2'] },
    { task: '构建 Docker 镜像', agent: 'builder', dependencies: ['task-3'] },
    { task: '推送到生产环境', agent: 'deployer', dependencies: ['task-4'] },
  ]
});

if (!result.success) {
  console.log(`Failed at step: ${result.failurePoint}`);
}
```

### 3. Map-Reduce Pattern - 批量分析

```javascript
// 场景：分析 100 个文件，生成汇总报告
const files = await getProjectFiles(); // ['a.js', 'b.js', ...]

const result = await orchestrator.execute({
  task: '分析项目代码质量',
  pattern: 'map-reduce',
  map: {
    items: files,
    taskFn: (file) => `分析 ${file} 的质量指标`,
    agent: 'analyzer',
  },
  reduce: {
    task: '汇总所有分析结果，生成质量报告',
    agent: 'reporter',
  }
});

console.log(result.reduceOutput); // 汇总报告
```

### 4. Pipeline Pattern - CI/CD 流水线

```javascript
// 场景：完整的 CI/CD 流水线
const result = await orchestrator.execute({
  task: 'CI/CD Pipeline',
  pattern: 'pipeline',
  stages: [
    {
      name: 'build',
      tasks: [
        { task: 'npm install', agent: 'builder' },
        { task: 'npm run build', agent: 'builder' },
        { task: 'npm run lint', agent: 'linter' },
      ]
    },
    {
      name: 'test',
      tasks: [
        { task: '单元测试', agent: 'tester' },
        { task: '集成测试', agent: 'tester' },
        { task: 'E2E 测试', agent: 'tester' },
      ]
    },
    {
      name: 'deploy',
      tasks: [
        { task: '部署到 Staging', agent: 'deployer' },
        { task: '冒烟测试', agent: 'tester' },
        { task: '部署到 Production', agent: 'deployer' },
      ]
    }
  ]
});

console.log(result.stageStats); // 各阶段状态
```

### 5. Fan-Out Pattern - 多方案设计

```javascript
// 场景：探索多种架构方案
const result = await orchestrator.execute({
  task: '设计用户认证系统',
  pattern: 'fan-out',
  subTasks: [
    { task: '方案 1: JWT + Refresh Token', agent: 'architect', variation: 'jwt' },
    { task: '方案 2: Session + Cookie', agent: 'architect', variation: 'session' },
    { task: '方案 3: OAuth 2.0', agent: 'architect', variation: 'oauth' },
    { task: '方案 4: Passkey/WebAuthn', agent: 'architect', variation: 'passkey' },
  ],
  fanIn: {
    task: '对比所有方案，考虑安全性、易用性、性能，推荐最佳选择',
    agent: 'chief-architect',
  }
});

console.log(result.variations); // 所有方案
console.log(result.fanInOutput); // 最终推荐
```

---

## 实际场景

### 场景 1: 自动代码审查工作流

```javascript
import { HarnessOrchestrator } from './harness/orchestrator.js';

async function reviewPullRequest(prNumber) {
  const orchestrator = new HarnessOrchestrator();
  
  // 获取 PR 变更文件
  const changedFiles = await getChangedFiles(prNumber);
  
  const result = await orchestrator.execute({
    task: `审查 PR #${prNumber}`,
    pattern: 'parallel',
    subTasks: [
      {
        task: '代码风格检查',
        agent: 'linter-agent',
        context: { files: changedFiles },
      },
      {
        task: '安全漏洞扫描',
        agent: 'security-agent',
        context: { files: changedFiles },
      },
      {
        task: '性能问题分析',
        agent: 'performance-agent',
        context: { files: changedFiles },
      },
      {
        task: '测试覆盖率检查',
        agent: 'test-agent',
        context: { prNumber },
      },
    ]
  });
  
  // 生成审查报告
  const report = generateReviewReport(result);
  await postCommentToPR(prNumber, report);
  
  return result;
}
```

### 场景 2: 批量数据处理

```javascript
async function processUserRecords(userIds) {
  const orchestrator = new HarnessOrchestrator({ maxParallel: 10 });
  
  const result = await orchestrator.execute({
    task: '处理用户记录',
    pattern: 'map-reduce',
    map: {
      items: userIds,
      taskFn: (userId) => `处理用户 ${userId} 的数据`,
      agent: 'data-processor',
    },
    reduce: {
      task: '汇总处理结果，生成统计报告',
      agent: 'reporter',
    }
  });
  
  return result.reduceOutput;
}
```

### 场景 3: 多模型答案对比

```javascript
async function getBestAnswer(question) {
  const orchestrator = new HarnessOrchestrator();
  
  const result = await orchestrator.execute({
    task: '回答技术问题',
    pattern: 'fan-out',
    subTasks: [
      { task: `回答：${question}`, agent: 'qwen-agent', variation: 'qwen' },
      { task: `回答：${question}`, agent: 'gemini-agent', variation: 'gemini' },
      { task: `回答：${question}`, agent: 'claude-agent', variation: 'claude' },
    ],
    fanIn: {
      task: '对比所有答案的准确性、完整性、清晰度，选择最佳答案',
      agent: 'evaluator',
    }
  });
  
  return result.fanInOutput;
}
```

---

## 高级用法

### 自定义模式

```javascript
import { registerPattern } from './harness/patterns/index.js';

// 注册自定义模式
registerPattern('custom-tree', {
  name: 'custom-tree',
  description: '树形分解模式',
  
  decompose: async (task, context) => {
    // 自定义分解逻辑
    return [
      { id: 'root', task, dependencies: [] },
      { id: 'left', task: '左子任务', dependencies: ['root'] },
      { id: 'right', task: '右子任务', dependencies: ['root'] },
    ];
  },
  
  aggregate: async (results) => {
    // 自定义聚合逻辑
    return { /* ... */ };
  },
  
  validate: async (aggregated) => {
    // 自定义验证逻辑
    return { valid: true, issues: [] };
  },
});

// 使用自定义模式
const result = await orchestrator.execute({
  task: '树形任务',
  pattern: 'custom-tree',
});
```

### 自定义验证器

```javascript
import { createValidator, validators } from './harness/utils/validator.js';

const myValidator = createValidator({
  required: ['output', 'metadata'],
  minItems: 1,
  custom: [
    validators.atLeastOneSuccess(),
    validators.noErrors(),
    validators.withinTimeLimit(60000), // 60 秒内完成
    validators.outputNotEmpty(),
    
    // 自定义验证规则
    (result) => {
      if (result.outputs.length > 10) {
        return {
          type: 'TOO_MANY_OUTPUTS',
          message: 'Too many outputs',
          severity: 'warning',
        };
      }
      return null;
    },
  ],
});

const validation = myValidator(result);
if (!validation.valid) {
  console.log('Validation failed:', validation.issues);
}
```

### 错误处理与恢复

```javascript
const orchestrator = new HarnessOrchestrator({
  retryAttempts: 3,
  retryDelay: 1000,
  timeoutSeconds: 300,
});

try {
  const result = await orchestrator.execute({
    task: '执行关键任务',
    pattern: 'sequential',
    subTasks: [/* ... */]
  });
  
  if (!result.success) {
    // 部分失败处理
    console.log('Partial failure:', result.errors);
    
    // 可以尝试重试失败的任务
    const retryResult = await retryFailedTasks(result.errors);
  }
  
} catch (error) {
  // 完全失败
  console.error('Execution failed:', error);
  
  // 获取详细状态
  const status = orchestrator.getStatus();
  console.log('Queue status:', status.queue);
  console.log('Task states:', status.tasks);
}
```

---

## 性能优化建议

### 1. 合理设置并行度

```javascript
// CPU 密集型任务：并行度 = CPU 核心数
const cpuOrchestrator = new HarnessOrchestrator({ maxParallel: 4 });

// I/O 密集型任务：可以更高
const ioOrchestrator = new HarnessOrchestrator({ maxParallel: 20 });

// API 调用：注意速率限制
const apiOrchestrator = new HarnessOrchestrator({ maxParallel: 5 });
```

### 2. 任务分组

```javascript
// 将相关任务分到同一组，减少上下文切换
const result = await orchestrator.execute({
  task: '处理项目',
  pattern: 'pipeline',
  stages: [
    { name: 'frontend', tasks: frontendTasks },
    { name: 'backend', tasks: backendTasks },
    { name: 'integration', tasks: integrationTasks },
  ]
});
```

### 3. 超时控制

```javascript
// 短任务设置短超时
const quickOrchestrator = new HarnessOrchestrator({ timeoutSeconds: 30 });

// 长任务设置长超时
const longOrchestrator = new HarnessOrchestrator({ timeoutSeconds: 600 });
```

---

## 调试技巧

### 启用详细日志

```javascript
const orchestrator = new HarnessOrchestrator({
  enableLogging: true,
});

// 监听所有事件
orchestrator.on('start', (data) => console.log('START', data));
orchestrator.on('task-start', (task) => console.log('TASK-START', task.id));
orchestrator.on('task-complete', (task) => console.log('TASK-COMPLETE', task.id));
orchestrator.on('task-failed', (data) => console.error('TASK-FAILED', data));
orchestrator.on('complete', (result) => console.log('COMPLETE', result));
orchestrator.on('error', (error) => console.error('ERROR', error));
```

### 查看执行状态

```javascript
// 执行中查询状态
const status = orchestrator.getStatus();
console.log('Pending:', status.queue.pending);
console.log('Running:', status.queue.running);
console.log('Completed:', status.queue.completed);
console.log('Failed:', status.queue.failed);

// 查看每个任务的详细信息
for (const task of status.tasks) {
  console.log(`${task.id}: ${task.status} (${task.duration}ms)`);
}
```

---

*示例版本：1.0 | 最后更新：2026-04-18*
