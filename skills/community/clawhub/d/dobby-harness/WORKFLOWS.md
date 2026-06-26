# 生产级工作流文档

> Harness Engineering 生产级工作流使用指南

## 📋 目录

- [概述](#概述)
- [代码审查工作流](#代码审查工作流)
- [测试生成工作流](#测试生成工作流)
- [文档生成工作流](#文档生成工作流)
- [CI/CD 集成工作流](#cicd 集成工作流)
- [工作流组合](#工作流组合)
- [最佳实践](#最佳实践)

---

## 概述

工作流是基于 Harness Engineering 编排能力构建的**可复用生产级流程**，每个工作流都：

- ✅ 预配置了任务分解模式
- ✅ 集成了多个专业 Agent
- ✅ 包含完整的错误处理
- ✅ 生成结构化输出
- ✅ 支持自定义配置

### 可用工作流

| 工作流 | 文件 | 说明 |
|--------|------|------|
| Code Review | `workflows/code-review.js` | 自动代码审查 |
| Test Gen | `workflows/test-gen.js` | 测试用例生成 |
| Doc Gen | `workflows/doc-gen.js` | 文档自动生成 |
| CI/CD | `workflows/cicd.js` | CI/CD 配置生成 |

---

## 代码审查工作流

### 功能

- 🔍 代码风格检查
- 🔒 安全漏洞扫描
- ⚡ 性能问题分析
- 🧪 测试覆盖率检查
- 📊 自动生成审查报告

### 使用示例

```javascript
import { CodeReviewWorkflow } from './workflows/code-review.js';

// 创建工作流实例
const workflow = new CodeReviewWorkflow({
  enableLint: true,
  enableSecurity: true,
  enablePerformance: true,
  enableTests: true,
  minApprovalScore: 0.8,  // 80 分通过
});

// 执行审查
const result = await workflow.execute({
  prNumber: 123,
  files: ['src/auth.js', 'src/user.js', 'src/api.js'],
  repo: 'my-org/my-repo',
  autoComment: true,  // 自动发布评论到 PR
});

console.log(result.report);
```

### 审查报告结构

```json
{
  "prNumber": 123,
  "timestamp": "2026-04-18T08:00:00.000Z",
  "filesReviewed": 3,
  "score": 0.85,
  "approval": true,
  "summary": {
    "total": 5,
    "critical": 0,
    "major": 1,
    "minor": 2,
    "suggestion": 2
  },
  "issues": {
    "critical": [],
    "major": [...],
    "minor": [...],
    "suggestion": [...]
  },
  "recommendations": [...]
}
```

### 配置选项

```javascript
const config = {
  maxParallel: 5,           // 最大并行审查数
  timeoutSeconds: 300,      // 超时时间
  enableLint: true,         // 启用代码风格检查
  enableSecurity: true,     // 启用安全检查
  enablePerformance: true,  // 启用性能检查
  enableTests: true,        // 启用测试检查
  autoComment: false,       // 自动发布评论
  minApprovalScore: 0.8,    // 最低通过分数
};
```

---

## 测试生成工作流

### 功能

- 📝 自动生成单元测试
- 🎯 生成边界条件测试
- 🔗 生成集成测试
- 📊 估算测试覆盖率
- 💾 自动保存测试文件

### 使用示例

```javascript
import { TestGenWorkflow } from './workflows/test-gen.js';

const workflow = new TestGenWorkflow({
  framework: 'jest',      // jest | mocha | vitest | pytest
  minCoverage: 80,        // 最低覆盖率要求 (%)
  includeEdgeCases: true, // 包含边界条件测试
  includeIntegration: true, // 包含集成测试
});

const result = await workflow.execute({
  files: ['src/auth.js', 'src/user.js'],
  framework: 'jest',
});

// 保存测试文件
await workflow.saveTests(result.tests, '__tests__');

// 运行测试
const testResults = await workflow.runTests(
  result.tests.map(t => `__tests__/${t.file}`)
);

console.log(`覆盖率：${testResults.coverage}%`);
```

### 生成的测试结构

```
__tests__/
├── auth.test.js          # 单元测试
├── auth.edge.test.js     # 边界条件测试
├── auth.integration.js   # 集成测试
├── user.test.js
├── user.edge.test.js
└── user.integration.js
```

### 配置选项

```javascript
const config = {
  framework: 'jest',        // 测试框架
  minCoverage: 80,          // 最低覆盖率
  includeEdgeCases: true,   // 边界条件测试
  includeIntegration: true, // 集成测试
  autoCommit: false,        // 自动提交
};
```

---

## 文档生成工作流

### 功能

- 📖 自动生成 API 文档
- 📄 生成 README.md
- 💡 生成使用示例
- 📝 生成变更日志
- 🗂️ 更新文档索引

### 使用示例

```javascript
import { DocGenWorkflow } from './workflows/doc-gen.js';

const workflow = new DocGenWorkflow({
  format: 'markdown',
  output: 'docs',
  includeExamples: true,
  includeTypes: true,
  language: 'zh-CN',
});

const result = await workflow.execute({
  files: ['src/*.js'],
  output: 'docs/api',
});

// 保存文档
await workflow.saveDocs(result.docs, 'docs');

// 生成报告
const report = workflow.generateReport(result.docs, analysis);
console.log(`生成了 ${report.docsGenerated} 个文档`);
```

### 生成的文档结构

```
docs/
├── README.md             # 项目说明
├── CHANGELOG.md          # 变更日志
├── api/
│   ├── auth.md           # Auth 模块 API
│   ├── user.md           # User 模块 API
│   └── api.md            # API 索引
├── examples/
│   ├── basic.js          # 基础示例
│   └── advanced.js       # 高级示例
└── index.json            # 文档索引
```

### 配置选项

```javascript
const config = {
  format: 'markdown',     // 输出格式
  output: 'docs',         // 输出目录
  includeExamples: true,  // 包含示例
  includeTypes: true,     // 包含类型定义
  autoCommit: false,      // 自动提交
  language: 'zh-CN',      // 文档语言
};
```

---

## CI/CD 集成工作流

### 功能

- ⚙️ 自动生成 CI 配置
- 🐳 生成 Dockerfile
- 📦 生成 Docker Compose
- 🚀 配置自动化部署
- 📊 生成监控配置

### 使用示例

```javascript
import { CICDWorkflow } from './workflows/cicd.js';

const workflow = new CICDWorkflow({
  platform: 'github',     // github | gitlab | jenkins
  target: 'production',   // staging | production
  autoDeploy: true,
  enableNotifications: true,
});

const result = await workflow.execute({
  platform: 'github',
  target: 'production',
});

// 保存配置
await workflow.saveConfigs(result.configs);

// 验证配置
const validation = await workflow.validateConfigs(result.configs);
console.log(`配置验证：${validation.allValid ? '通过' : '失败'}`);
```

### 生成的文件结构

```
.
├── .github/
│   └── workflows/
│       └── ci-cd.yml     # GitHub Actions 配置
├── .gitlab-ci.yml        # GitLab CI 配置
├── Dockerfile            # Docker 构建文件
├── docker-compose.yml    # Docker Compose 配置
├── deploy.sh             # 部署脚本
└── monitoring/
    ├── alerts.yml        # 告警配置
    └── dashboard.json    # 监控面板
```

### 配置选项

```javascript
const config = {
  platform: 'github',         // CI 平台
  target: 'production',       // 部署目标
  autoDeploy: false,          // 自动部署
  enableNotifications: true,  // 启用通知
};
```

---

## 工作流组合

### 完整开发流程

```javascript
import { runWorkflow } from './workflows/index.js';

// 1. 代码审查
const review = await runWorkflow('code-review', {
  prNumber: 123,
  files: changedFiles,
});

if (!review.report.approval) {
  console.log('代码审查未通过，需要修复');
  process.exit(1);
}

// 2. 生成测试
const tests = await runWorkflow('test-gen', {
  files: changedFiles,
  framework: 'jest',
});

// 3. 运行测试
const testResults = await runTests(tests.tests);

if (testResults.coverage < 80) {
  console.log('测试覆盖率不足');
  process.exit(1);
}

// 4. 生成文档
await runWorkflow('doc-gen', {
  files: allSourceFiles,
  output: 'docs',
});

// 5. 部署
await runWorkflow('cicd', {
  platform: 'github',
  target: 'production',
});
```

### 自定义工作流

```javascript
import { HarnessOrchestrator } from './harness/orchestrator.js';

// 创建自定义工作流
const orchestrator = new HarnessOrchestrator();

const result = await orchestrator.execute({
  task: '完整发布流程',
  pattern: 'pipeline',
  subTasks: [
    {
      task: '代码审查',
      agent: 'reviewer',
    },
    {
      task: '生成测试',
      agent: 'test-writer',
    },
    {
      task: '运行测试',
      agent: 'test-runner',
    },
    {
      task: '构建项目',
      agent: 'builder',
    },
    {
      task: '部署上线',
      agent: 'deployer',
    },
  ],
});
```

---

## 最佳实践

### 1. 工作流选择

| 场景 | 推荐工作流 |
|------|-----------|
| PR 审查 | Code Review |
| 新功能开发 | Test Gen + Doc Gen |
| 项目初始化 | CI/CD + Doc Gen |
| 发布前检查 | Code Review + Test Gen |

### 2. 配置建议

```javascript
// 开发环境
const devConfig = {
  maxParallel: 3,
  timeoutSeconds: 120,
  enableSecurity: false,  // 开发时跳过安全检查
};

// 生产环境
const prodConfig = {
  maxParallel: 10,
  timeoutSeconds: 600,
  enableSecurity: true,   // 生产必须安全检查
  minApprovalScore: 0.9,  // 更高要求
};
```

### 3. 错误处理

```javascript
try {
  const result = await workflow.execute(options);
  
  if (!result.success) {
    // 部分失败处理
    console.log('部分任务失败:', result.rawResult.errors);
    
    // 重试失败的任务
    const retryResult = await retryFailed(result.rawResult.errors);
  }
  
} catch (error) {
  // 完全失败
  console.error('工作流执行失败:', error);
  
  // 获取详细状态
  const status = workflow.getStatus();
  console.log(status);
}
```

### 4. 性能优化

```javascript
// 大项目：增加并行度
const workflow = new CodeReviewWorkflow({
  maxParallel: 20,  // 默认 5
});

// 小项目：减少超时
const workflow = new TestGenWorkflow({
  timeoutSeconds: 60,  // 默认 300
});

// 关键任务：增加重试
const workflow = new CICDWorkflow({
  retryAttempts: 5,  // 默认 2
});
```

---

## 文件结构

```
workflows/
├── index.js              # 工作流导出
├── code-review.js        # 代码审查工作流 (8KB)
├── test-gen.js           # 测试生成工作流 (8KB)
├── doc-gen.js            # 文档生成工作流 (8KB)
└── cicd.js               # CI/CD 工作流 (10KB)
```

**总计**: ~42KB 工作流代码

---

## 下一步

- [ ] 集成真实 Agent 实现
- [ ] 添加更多工作流模板
- [ ] 支持工作流可视化配置
- [ ] 添加性能监控
- [ ] 支持工作流版本管理

---

*文档版本：1.0 | 最后更新：2026-04-18 | 作者：多比 🧦*
