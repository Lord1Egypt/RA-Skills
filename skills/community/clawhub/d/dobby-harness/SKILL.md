# Dobby-harness Skill

> 多 Agent 编排 · 生产级工作流 · 自进化系统

## 📖 技能描述

Harness Engineering 提供完整的多 Agent 编排能力，包括任务分解、并行执行、结果聚合、自进化系统等功能。适用于需要协调多个子 Agent 完成复杂任务的场景。

## 🎯 适用场景

当以下情况时使用此 Skill：

1. **复杂任务分解** - 需要将大任务分解为多个可并行执行的子任务
2. **多 Agent 协作** - 需要协调多个专业 Agent 协同工作
3. **生产工作流** - 需要代码审查、测试生成、文档自动化等标准化流程
4. **状态持久化** - 需要防止上下文丢失、支持崩溃恢复
5. **知识沉淀** - 需要从任务中学习并沉淀最佳实践

## 🚀 快速开始

### 基础用法

```javascript
import { HarnessOrchestrator } from 'dobby-harness/harness/orchestrator.js';

// 创建编排器
const orchestrator = new HarnessOrchestrator({
  maxParallel: 5,
  timeoutSeconds: 300,
});

// 执行并行任务
const result = await orchestrator.execute({
  task: '分析项目代码质量',
  pattern: 'parallel',
  subTasks: [
    { task: '检查代码风格', agent: 'linter' },
    { task: '检查安全漏洞', agent: 'security' },
    { task: '检查性能问题', agent: 'performance' },
  ]
});

console.log(`完成：${result.completed}/${result.total}`);
```

### 使用工作流

```javascript
import { CodeReviewWorkflow } from 'dobby-harness/workflows/code-review.js';

const workflow = new CodeReviewWorkflow();

const result = await workflow.execute({
  prNumber: 123,
  files: ['src/auth.js', 'src/user.js'],
  autoComment: true,
});

console.log(`审查评分：${result.report.score * 100}`);
```

## 📚 核心组件

### 1. Harness Orchestrator

多 Agent 编排核心，支持 5 种任务分解模式：

| 模式 | 说明 | 适用场景 |
|------|------|----------|
| `parallel` | 完全并行 | 独立子任务 |
| `sequential` | 顺序执行 | 有依赖关系 |
| `map-reduce` | 映射归约 | 批量处理 + 聚合 |
| `pipeline` | 流水线 | 多阶段处理 |
| `fan-out` | 扇出探索 | 多方案对比 |

### 2. Production Workflows

预配置的生产级工作流：

- **Code Review** - 自动代码审查
- **Test Gen** - 测试用例生成
- **Doc Gen** - 文档自动生成
- **CI/CD** - 持续集成配置

### 3. Self-Improvement System

自进化系统组件：

- **WAL Protocol** - 预写日志协议
- **Working Buffer** - 工作缓冲区
- **Pattern Recognition** - 模式识别

## 📁 文件结构

```
harness-engineering/
├── SKILL.md                  # 本文件
├── README.md                 # 项目文档
├── HARNESS-ARCHITECTURE.md   # 架构设计
├── WORKFLOWS.md              # 工作流指南
├── SELF-IMPROVEMENT.md       # 自进化文档
├── SECURITY-AUDIT.md         # 安全审计
├── harness/
│   ├── orchestrator.js       # 核心编排器
│   ├── patterns/             # 任务分解模式
│   └── utils/                # 工具模块
├── workflows/
│   ├── code-review.js        # 代码审查
│   ├── test-gen.js           # 测试生成
│   ├── doc-gen.js            # 文档生成
│   └── cicd.js               # CI/CD 集成
├── memory/
│   ├── wal.js                # WAL 协议
│   └── working-buffer.js     # 工作缓冲区
├── examples/
│   └── harness-demo.js       # 完整演示
└── tests/
    ├── test-suite.js         # 测试套件
    └── quick-test.js         # 快速验证
```

## 🔧 配置选项

### Orchestrator 配置

```javascript
const config = {
  maxParallel: 5,           // 最大并行数
  timeoutSeconds: 300,      // 超时时间
  retryAttempts: 2,         // 重试次数
  retryDelay: 1000,         // 重试延迟 (ms)
  enableLogging: true,      // 启用日志
};
```

### Workflow 配置

```javascript
const config = {
  // Code Review
  enableLint: true,
  enableSecurity: true,
  enablePerformance: true,
  enableTests: true,
  minApprovalScore: 0.8,
  
  // Test Gen
  framework: 'jest',
  minCoverage: 80,
  includeEdgeCases: true,
  
  // 通用
  autoCommit: false,
  autoComment: false,
};
```

## 📊 性能指标

根据基准测试：

| 组件 | 平均耗时 | 说明 |
|------|---------|------|
| Orchestrator | ~50ms | 5 个子任务并行 |
| WAL | ~2ms | 单次事务 |
| Buffer | ~1ms | 单次读写 |

**测试通过率**: 100% (23+ 测试用例)

## 🛡️ 安全状态

- **总体评分**: 82.5/100
- **严重风险**: 0
- **高风险**: 0
- **中风险**: 2 (待修复)

详见 [SECURITY-AUDIT.md](./SECURITY-AUDIT.md)

## 📖 使用示例

### 示例 1: 并行代码审查

```javascript
const result = await orchestrator.execute({
  task: '审查 PR #123',
  pattern: 'parallel',
  subTasks: [
    { task: '代码风格检查', agent: 'linter' },
    { task: '安全漏洞扫描', agent: 'security' },
    { task: '性能分析', agent: 'performance' },
  ]
});
```

### 示例 2: CI/CD 流水线

```javascript
const result = await orchestrator.execute({
  task: '发布 v1.0.0',
  pattern: 'pipeline',
  stages: [
    { name: 'build', tasks: ['npm install', 'npm run build'] },
    { name: 'test', tasks: ['npm test', 'npm run lint'] },
    { name: 'deploy', tasks: ['deploy to prod'] },
  ]
});
```

### 示例 3: 多方案设计

```javascript
const result = await orchestrator.execute({
  task: '设计认证系统',
  pattern: 'fan-out',
  subTasks: [
    { task: '方案 1: JWT', agent: 'architect' },
    { task: '方案 2: Session', agent: 'architect' },
    { task: '方案 3: OAuth', agent: 'architect' },
  ],
  fanIn: {
    task: '对比方案，推荐最佳',
    agent: 'chief-architect',
  }
});
```

## 🧪 测试

### 运行测试

```bash
node tests/test-suite.js
```

### 运行演示

```bash
node examples/harness-demo.js
```

## 📚 相关文档

- [HARNESS-ARCHITECTURE.md](./HARNESS-ARCHITECTURE.md) - 核心架构设计
- [WORKFLOWS.md](./WORKFLOWS.md) - 工作流使用指南
- [SELF-IMPROVEMENT.md](./SELF-IMPROVEMENT.md) - 自进化系统
- [SECURITY-AUDIT.md](./SECURITY-AUDIT.md) - 安全审计报告
- [README.md](./README.md) - 项目总览

## 🤝 贡献

1. Fork 项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

贡献代码时请在 `.learnings/LEARNINGS.md` 记录学习内容。

## 📄 许可证

MIT License

## 🙏 致谢

- 多比 (Dobby) - 原始作者
- OpenClaw 社区 - 平台支持

---

*Skill 版本：1.0.0 | 最后更新：2026-04-18*
