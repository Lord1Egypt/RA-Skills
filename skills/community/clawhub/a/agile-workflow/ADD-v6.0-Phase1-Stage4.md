# ADD - 敏捷工作流 v6.0 Phase 1 阶段 4: 集成测试

**版本**: v6.0-Phase1-Stage4  
**状态**: 设计完成 → 实施中  
**原则**: 效率优先，保质保量（无时间计划）

---

## 1. 架构概述

### 1.1 设计目标

**核心目标**：验证所有模块协同工作正常，测试通过率 100%

**集成范围**：
```
质量验证器 ↔ 创造性评分 ↔ Token 控制器 ↔ Agent 管理 ↔ 熔断恢复
```

### 1.2 质量标准

- 集成成功率：100%
- 测试通过率：100%
- 质量评分：≥90 分
- 代码覆盖率：> 80%

---

## 2. 集成架构

### 2.1 模块关系图

```
┌─────────────────────────────────────────────────────────┐
│                  工作流引擎                              │
│  (workflow-engine.js)                                   │
└────────────┬────────────────────────────────────────────┘
             │
    ┌────────┼────────┬────────────┬────────────┐
    │        │        │            │            │
    ▼        ▼        ▼            ▼            ▼
┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
│质量验证│ │创造性  │ │Token   │ │Agent   │ │熔断    │
│验证器  │ │评分器  │ │控制器  │ │管理器  │ │恢复器  │
└────────┘ └────────┘ └────────┘ └────────┘ └────────┘
    │        │        │            │            │
    └────────┴────────┴────────────┴────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │   集成测试框架       │
              │   (integration-test)│
              └─────────────────────┘
```

### 2.2 数据流

```
任务输入
    ↓
[任务拆解] → 原子任务列表
    ↓
[智能排序] → 排序后任务队列
    ↓
[Agent 分配] → 检查状态 → 离线？→ 启动 → 验证
    ↓
[任务执行] → 执行任务 → 监控状态
    ↓
[Token 检查] → 计算 token → 检查限制 → 超限优化
    ↓
[质量验证] → 完整性/一致性/合规性/创造性
    ↓
[质量评分] → ≥80 分？→ 是→交付 / 否→返工
    ↓
[成果组装] → 统一整合 → 版本管理 → 交付
```

---

## 3. 测试策略

### 3.1 测试层级

```
┌────────────────────────────────────────┐
│          验收测试 (Acceptance)          │
│  - 端到端流程                           │
│  - 用户场景                             │
└────────────────────────────────────────┘
              ↑
┌────────────────────────────────────────┐
│          系统测试 (System)              │
│  - 完整功能                             │
│  - 性能测试                             │
│  - 压力测试                             │
└────────────────────────────────────────┘
              ↑
┌────────────────────────────────────────┐
│          集成测试 (Integration)         │
│  - 模块间接口                           │
│  - 数据流验证                           │
│  - 异常处理                             │
└────────────────────────────────────────┘
              ↑
┌────────────────────────────────────────┐
│          单元测试 (Unit)                │
│  - 单个模块功能                         │
│  - 边界条件                             │
│  - 错误处理                             │
└────────────────────────────────────────┘
```

### 3.2 测试用例设计

#### 集成测试用例

| ID | 测试场景 | 输入 | 预期输出 | 状态 |
|----|---------|------|---------|------|
| IT-001 | 质量验证器集成 | 任务结果 | 质量报告 | ⏳ |
| IT-002 | 创造性评分集成 | 创作内容 | 评分报告 | ⏳ |
| IT-003 | Token 控制器集成 | 请求内容 | 优化后内容 | ⏳ |
| IT-004 | Agent 管理器集成 | 任务分配 | Agent 状态 | ⏳ |
| IT-005 | 熔断恢复集成 | 连续失败 | 自动恢复 | ⏳ |
| IT-006 | 端到端流程 | 完整任务 | 交付成果 | ⏳ |

#### 端到端测试用例

| ID | 测试场景 | 流程 | 预期结果 | 状态 |
|----|---------|------|---------|------|
| E2E-001 | 正常流程 | 输入→拆解→执行→验证→交付 | 成功交付 | ⏳ |
| E2E-002 | 质量不达标 | 输入→执行→验证<80→返工 | 返工后交付 | ⏳ |
| E2E-003 | Token 超限 | 输入→执行→超限→优化→交付 | 优化后交付 | ⏳ |
| E2E-004 | Agent 离线 | 输入→分配→离线→启动→执行 | 启动后执行 | ⏳ |
| E2E-005 | 熔断恢复 | 输入→执行→失败→熔断→恢复 | 恢复后执行 | ⏳ |

---

## 4. 测试框架

### 4.1 测试运行器

```javascript
class IntegrationTestRunner {
  constructor() {
    this.results = [];
    this.passed = 0;
    this.failed = 0;
  }

  async runTest(testCase) {
    console.log(`\n🧪 运行测试：${testCase.id} - ${testCase.name}`);
    
    try {
      const result = await testCase.run();
      
      if (result.passed) {
        this.passed++;
        console.log(`✅ 通过：${testCase.id}`);
      } else {
        this.failed++;
        console.log(`❌ 失败：${testCase.id}`);
        console.log(`   原因：${result.reason}`);
      }
      
      this.results.push({
        id: testCase.id,
        name: testCase.name,
        passed: result.passed,
        reason: result.reason,
        duration: result.duration
      });
      
      return result.passed;
    } catch (error) {
      this.failed++;
      console.log(`❌ 异常：${testCase.id}`);
      console.log(`   错误：${error.message}`);
      
      this.results.push({
        id: testCase.id,
        name: testCase.name,
        passed: false,
        reason: error.message,
        duration: 0
      });
      
      return false;
    }
  }

  async runAll(testCases) {
    console.log('🚀 开始集成测试...\n');
    
    for (const testCase of testCases) {
      await this.runTest(testCase);
    }
    
    this.printReport();
    return this.failed === 0;
  }

  printReport() {
    const total = this.passed + this.failed;
    const passRate = (this.passed / total * 100).toFixed(1);
    
    console.log('\n📊 测试报告:');
    console.log(`   总计：${total}`);
    console.log(`   通过：${this.passed}`);
    console.log(`   失败：${this.failed}`);
    console.log(`   通过率：${passRate}%`);
    
    if (this.failed > 0) {
      console.log('\n❌ 失败用例:');
      this.results
        .filter(r => !r.passed)
        .forEach(r => {
          console.log(`   ${r.id}: ${r.reason}`);
        });
    }
  }
}
```

### 4.2 测试断言

```javascript
class Assert {
  static equal(actual, expected, message) {
    if (actual !== expected) {
      throw new Error(`${message || '断言失败'}: 期望 ${expected}, 实际 ${actual}`);
    }
  }

  static notEqual(actual, expected, message) {
    if (actual === expected) {
      throw new Error(`${message || '断言失败'}: 不应等于 ${expected}`);
    }
  }

  static greaterThan(actual, expected, message) {
    if (actual <= expected) {
      throw new Error(`${message || '断言失败'}: ${actual} 应大于 ${expected}`);
    }
  }

  static lessThan(actual, expected, message) {
    if (actual >= expected) {
      throw new Error(`${message || '断言失败'}: ${actual} 应小于 ${expected}`);
    }
  }

  static isTrue(actual, message) {
    if (!actual) {
      throw new Error(`${message || '断言失败'}: 期望为 true`);
    }
  }

  static isFalse(actual, message) {
    if (actual) {
      throw new Error(`${message || '断言失败'}: 期望为 false`);
    }
  }

  static isNull(actual, message) {
    if (actual !== null) {
      throw new Error(`${message || '断言失败'}: 期望为 null`);
    }
  }

  static isNotNull(actual, message) {
    if (actual === null) {
      throw new Error(`${message || '断言失败'}: 不应为 null`);
    }
  }

  static includes(actual, expected, message) {
    if (!actual.includes(expected)) {
      throw new Error(`${message || '断言失败'}: ${actual} 应包含 ${expected}`);
    }
  }

  static hasProperty(actual, property, message) {
    if (!actual.hasOwnProperty(property)) {
      throw new Error(`${message || '断言失败'}: 对象应包含属性 ${property}`);
    }
  }
}
```

---

## 5. 测试实施

### 5.1 模块集成测试

#### 测试 1: 质量验证器集成

```javascript
{
  id: 'IT-001',
  name: '质量验证器集成测试',
  async run() {
    const startTime = Date.now();
    
    // 准备测试数据
    const taskResult = {
      taskId: 'test_001',
      taskName: '测试任务',
      taskType: 'document',
      content: '这是一份测试文档，包含创新思路和深入分析。',
      wordCount: 1000
    };
    
    // 调用质量验证器
    const { QualityValidator } = require('./quality-validator.js');
    const validator = new QualityValidator();
    const report = validator.validate(taskResult);
    
    // 验证结果
    Assert.isNotNull(report, '质量报告不应为空');
    Assert.hasProperty(report, 'quality', '报告应包含质量属性');
    Assert.greaterThan(report.quality.score, 0, '评分应大于 0');
    
    return {
      passed: true,
      duration: Date.now() - startTime
    };
  }
}
```

#### 测试 2: 创造性评分集成

```javascript
{
  id: 'IT-002',
  name: '创造性评分集成测试',
  async run() {
    const startTime = Date.now();
    
    // 准备测试数据
    const content = '这是一个创新方案，采用了新的方法和技术。';
    
    // 调用创造性评分器
    const { CreativityScorer } = require('./creativity-scorer.js');
    const scorer = new CreativityScorer('document');
    const result = scorer.calculateCreativityScore(content);
    
    // 验证结果
    Assert.isNotNull(result, '评分结果不应为空');
    Assert.hasProperty(result, 'total', '结果应包含总分');
    Assert.hasProperty(result, 'level', '结果应包含等级');
    
    return {
      passed: true,
      duration: Date.now() - startTime
    };
  }
}
```

#### 测试 3: Token 控制器集成

```javascript
{
  id: 'IT-003',
  name: 'Token 控制器集成测试',
  async run() {
    const startTime = Date.now();
    
    // 准备测试数据
    const content = {
      messages: [
        { role: 'user', content: '测试内容'.repeat(100) }
      ]
    };
    
    // 调用 Token 控制器
    const { TokenController } = require('./token-manager/token-controller.js');
    const controller = new TokenController('qwen3.5-plus');
    const result = controller.checkBeforeSend(content);
    
    // 验证结果
    Assert.hasProperty(result, 'approved', '结果应包含批准状态');
    Assert.hasProperty(result, 'tokens', '结果应包含 token 数');
    
    return {
      passed: result.approved,
      reason: result.approved ? undefined : 'Token 检查未通过',
      duration: Date.now() - startTime
    };
  }
}
```

### 5.2 端到端测试

#### 测试：完整流程

```javascript
{
  id: 'E2E-001',
  name: '端到端完整流程测试',
  async run() {
    const startTime = Date.now();
    
    try {
      // 1. 任务输入
      const task = {
        id: 'e2e_test_001',
        name: '端到端测试任务',
        type: 'document',
        requirements: {
          minWordCount: 500,
          qualityThreshold: 80
        }
      };
      
      // 2. 任务拆解
      const { AgileWorkflowEngineV5 } = require('./agile-workflow-engine-v5.js');
      const workflow = new AgileWorkflowEngineV5();
      const atomicTasks = await workflow.recursiveDecompose(task);
      Assert.greaterThan(atomicTasks.length, 0, '应拆解出子任务');
      
      // 3. 任务分配
      const { AgentStateManager } = require('./agent-manager.js');
      const agentManager = new AgentStateManager();
      const agentName = 'test_agent';
      await agentManager.assignTask(agentName, atomicTasks[0]);
      
      // 4. 执行任务 (模拟)
      const taskResult = {
        taskId: atomicTasks[0].id,
        content: '测试内容',
        wordCount: 600
      };
      
      // 5. Token 检查
      const { TokenController } = require('./token-manager/token-controller.js');
      const tokenController = new TokenController();
      const tokenResult = tokenController.checkBeforeSend(taskResult);
      Assert.isTrue(tokenResult.approved, 'Token 检查应通过');
      
      // 6. 质量验证
      const { QualityValidator } = require('./quality-validator.js');
      const validator = new QualityValidator();
      const qualityReport = validator.validate(taskResult);
      Assert.greaterThan(qualityReport.quality.score, 0, '应有质量评分');
      
      // 7. 创造性评分
      const { CreativityScorer } = require('./creativity-scorer.js');
      const scorer = new CreativityScorer('document');
      const creativityResult = scorer.calculateCreativityScore(taskResult.content);
      Assert.hasProperty(creativityResult, 'total', '应有创造性评分');
      
      return {
        passed: true,
        duration: Date.now() - startTime
      };
    } catch (error) {
      return {
        passed: false,
        reason: error.message,
        duration: Date.now() - startTime
      };
    }
  }
}
```

---

## 6. 验收标准

### 6.1 功能验收

- [ ] 所有集成测试通过
- [ ] 所有端到端测试通过
- [ ] 测试覆盖率 > 80%
- [ ] 无严重缺陷

### 6.2 质量验收

- [ ] 质量评分 ≥ 90 分
- [ ] 代码审查通过
- [ ] 性能指标达标
- [ ] 文档完整

### 6.3 性能验收

| 指标 | 目标值 | 测试方法 |
|------|--------|---------|
| **集成测试时间** | < 5 分钟 | 自动化测试 |
| **端到端测试时间** | < 10 分钟 | 自动化测试 |
| **测试通过率** | 100% | 测试报告 |
| **代码覆盖率** | > 80% | 覆盖率工具 |

---

## 7. 交付物

### 7.1 测试代码

- [ ] integration-test.js (测试运行器)
- [ ] test-cases.js (测试用例集)
- [ ] assert.js (断言库)
- [ ] test-report.js (报告生成器)

### 7.2 测试报告

- [ ] 集成测试报告
- [ ] 端到端测试报告
- [ ] 覆盖率报告
- [ ] 性能测试报告

### 7.3 文档

- [ ] 测试计划
- [ ] 测试用例文档
- [ ] 缺陷报告
- [ ] 验收报告

---

**ADD 设计完成，开始实施阶段 4！** 🚀

**原则**: 效率优先，保质保量  
**时间计划**: ❌ 禁止  
**质量标准**: ✅ ≥90 分  
**验证机制**: ✅ 自动测试
