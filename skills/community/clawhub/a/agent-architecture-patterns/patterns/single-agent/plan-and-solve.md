# Plan-and-Solve 模式 - 规划与执行

> **版本**: 1.0.0  
> **论文**: [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)  
> **适用场景**: 复杂多步骤任务、需要全局规划、步骤间有依赖的任务

---

## 🧠 核心思想

**Plan-and-Solve = Plan + Execute + Synthesize**

传统方法的问题：
- **盲目执行**：没有规划就开始做
- **缺乏全局**：只见树木不见森林
- **步骤混乱**：顺序错误、遗漏步骤

Plan-and-Solve 的突破：
- **先规划**：制定完整计划再执行
- **分步骤**：将复杂任务分解为可执行步骤
- **跟踪进度**：记录已完成和待完成步骤
- **灵活调整**：根据执行情况调整计划

---

## 📊 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    Task Input                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Phase 1: Understand (理解任务)                          │
│  - 分析任务目标                                          │
│  - 识别约束条件                                          │
│  - 确定成功标准                                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Phase 2: Plan (制定计划)                                │
│  - 分解为子任务                                          │
│  - 确定执行顺序                                          │
│  - 识别依赖关系                                          │
│  - 估算资源需求                                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Phase 3: Execute (执行计划)                             │
│  For each step in plan:                                  │
│    - 执行当前步骤                                        │
│    - 记录结果                                            │
│    - 检查进度                                            │
│    - 必要时调整计划                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Phase 4: Synthesize (整合结果)                          │
│  - 汇总所有步骤结果                                      │
│  - 验证是否满足目标                                      │
│  - 生成最终输出                                          │
└─────────────────────────────────────────────────────────┘
                          ↓
                  Final Output
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class PlanAndSolveAgent {
  constructor(options = {}) {
    this.maxSteps = options.maxSteps || 20;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async execute(task) {
    if (this.verbose) {
      console.log(`[Plan-and-Solve] 开始任务：${task}`);
    }
    
    // Phase 1: Understand
    const understanding = await this.understand(task);
    
    if (this.verbose) {
      console.log('[Understanding]');
      console.log(`  目标：${understanding.goal}`);
      console.log(`  约束：${understanding.constraints.join(', ')}`);
      console.log(`  成功标准：${understanding.successCriteria.join(', ')}`);
    }
    
    // Phase 2: Plan
    const plan = await this.plan(task, understanding);
    
    if (this.verbose) {
      console.log(`\n[Plan] 共 ${plan.steps.length} 步`);
      plan.steps.forEach((step, i) => {
        console.log(`  ${i + 1}. ${step.description}`);
      });
    }
    
    // Phase 3: Execute
    const executionResults = await this.executePlan(task, plan);
    
    if (this.verbose) {
      console.log(`\n[Execution Complete] ${executionResults.completed}/${executionResults.total} 步`);
    }
    
    // Phase 4: Synthesize
    const finalResult = await this.synthesize(task, understanding, executionResults);
    
    if (this.verbose) {
      console.log(`\n[Final Result] ${finalResult}`);
    }
    
    return finalResult;
  }

  /**
   * Phase 1: Understand - 理解任务
   */
  async understand(task) {
    const prompt = `
任务：${task}

请分析这个任务：

1. **任务目标**：要达成什么？
2. **约束条件**：有哪些限制？（时间、资源、技术等）
3. **成功标准**：如何判断任务完成？

请以 JSON 格式返回：
{
  "goal": "任务目标",
  "constraints": ["约束 1", "约束 2"],
  "successCriteria": ["标准 1", "标准 2"]
}

分析结果：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      // 降级方案
      return {
        goal: task,
        constraints: [],
        successCriteria: ['任务完成']
      };
    }
  }

  /**
   * Phase 2: Plan - 制定计划
   */
  async plan(task, understanding) {
    const prompt = `
任务：${task}

目标：${understanding.goal}

约束：${understanding.constraints.join(', ')}

成功标准：${understanding.successCriteria.join(', ')}

请制定详细的执行计划：

要求：
1. 将任务分解为具体的、可执行的步骤
2. 步骤之间可能有依赖关系（某步完成后才能执行下一步）
3. 每个步骤应该有清晰的完成标准
4. 步骤数量适中（5-15 步）

请以 JSON 格式返回：
{
  "steps": [
    {
      "id": 1,
      "description": "步骤描述",
      "dependencies": [],  // 依赖的步骤 ID
      "expectedOutput": "预期输出"
    }
  ]
}

计划：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      // 降级方案：返回单步计划
      return {
        steps: [{
          id: 1,
          description: task,
          dependencies: [],
          expectedOutput: '完成任务'
        }]
      };
    }
  }

  /**
   * Phase 3: Execute - 执行计划
   */
  async executePlan(task, plan) {
    const results = {
      total: plan.steps.length,
      completed: 0,
      failed: 0,
      stepResults: []
    };
    
    const completedSteps = new Set();
    
    for (let stepNum = 0; stepNum < plan.steps.length; stepNum++) {
      // 找到可执行的步骤（依赖已满足）
      const executableStep = plan.steps.find(step => 
        !completedSteps.has(step.id) &&
        step.dependencies.every(depId => completedSteps.has(depId))
      );
      
      if (!executableStep) {
        // 没有可执行的步骤，但还有未完成的
        console.warn('No executable steps found. Possible circular dependency.');
        break;
      }
      
      if (this.verbose) {
        console.log(`\n[Step ${executableStep.id}/${plan.steps.length}] ${executableStep.description}`);
      }
      
      // 执行步骤
      const result = await this.executeStep(task, executableStep, results.stepResults);
      
      results.stepResults.push({
        stepId: executableStep.id,
        description: executableStep.description,
        success: result.success,
        output: result.output,
        error: result.error
      });
      
      if (result.success) {
        completedSteps.add(executableStep.id);
        results.completed++;
        
        if (this.verbose) {
          console.log(`  ✅ 完成`);
        }
      } else {
        results.failed++;
        
        if (this.verbose) {
          console.log(`  ❌ 失败：${result.error}`);
        }
        
        // 关键步骤失败，可能无法继续
        if (this.isCriticalStep(executableStep)) {
          console.warn('Critical step failed. Stopping execution.');
          break;
        }
      }
    }
    
    return results;
  }

  /**
   * 执行单个步骤
   */
  async executeStep(task, step, previousResults) {
    const context = previousResults.map(r => 
      `步骤 ${r.stepId}: ${r.output}`
    ).join('\n');
    
    const prompt = `
任务：${task}

当前步骤：${step.description}
预期输出：${step.expectedOutput}

之前的执行结果：
${context || '（无）'}

请执行当前步骤。

结果：`;
    
    try {
      const output = await this.llm.generate(prompt);
      return { success: true, output };
    } catch (error) {
      return { success: false, error: error.message };
    }
  }

  /**
   * 判断是否是关键步骤
   */
  isCriticalStep(step) {
    // 如果其他步骤依赖这个步骤，则是关键步骤
    return false; // 简化实现
  }

  /**
   * Phase 4: Synthesize - 整合结果
   */
  async synthesize(task, understanding, executionResults) {
    const resultsText = executionResults.stepResults.map(r => 
      `步骤 ${r.stepId}: ${r.success ? '✅' : '❌'} ${r.output || r.error}`
    ).join('\n');
    
    const prompt = `
任务：${task}

目标：${understanding.goal}

成功标准：${understanding.successCriteria.join(', ')}

执行结果：
${resultsText}

完成进度：${executionResults.completed}/${executionResults.total} 步

请整合所有执行结果，生成最终输出。

如果所有步骤都完成且满足成功标准，给出完整答案。
如果有步骤失败，说明影响和替代方案。

最终输出：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 默认 LLM
   */
  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Task completed.';
    }
  };
}
```

---

### 使用示例

```javascript
// 创建 Agent
const agent = new PlanAndSolveAgent({
  maxSteps: 20,
  verbose: true
});

// 执行复杂任务
const task = '开发一个简单的待办事项应用，包括前端和后端';

const result = await agent.execute(task);
console.log(result);
```

---

### 执行轨迹示例

```
[Plan-and-Solve] 开始任务：开发一个简单的待办事项应用，包括前端和后端

[Understanding]
  目标：开发一个待办事项应用（前端 + 后端）
  约束：简单、快速开发
  成功标准：可以添加/删除/查看待办事项

[Plan] 共 8 步
  1. 设计数据模型
  2. 创建后端项目结构
  3. 实现 API 路由（GET /todos）
  4. 实现 API 路由（POST /todos）
  5. 实现 API 路由（DELETE /todos/:id）
  6. 创建前端项目结构
  7. 实现前端 UI 和交互
  8. 测试和部署

[Step 1/8] 设计数据模型
  ✅ 完成

[Step 2/8] 创建后端项目结构
  ✅ 完成

[Step 3/8] 实现 API 路由（GET /todos）
  ✅ 完成

[Step 4/8] 实现 API 路由（POST /todos）
  ✅ 完成

[Step 5/8] 实现 API 路由（DELETE /todos/:id）
  ✅ 完成

[Step 6/8] 创建前端项目结构
  ✅ 完成

[Step 7/8] 实现前端 UI 和交互
  ✅ 完成

[Step 8/8] 测试和部署
  ✅ 完成

[Execution Complete] 8/8 步

[Final Result] 
## 待办事项应用开发完成

### 后端（Node.js + Express）
- 数据模型：Todo { id, title, completed, createdAt }
- API 端点：
  - GET /todos - 获取所有待办
  - POST /todos - 创建待办
  - DELETE /todos/:id - 删除待办

### 前端（HTML + CSS + JavaScript）
- 功能：
  - 显示待办列表
  - 添加新待办
  - 删除待办
  - 标记完成

### 使用方法
1. 启动后端：node server.js
2. 打开前端：index.html
3. 访问 http://localhost:3000

所有功能已完成并测试通过。
```

---

## 🎯 关键设计要点

### 1. 任务理解

**好的理解**：
```javascript
{
  "goal": "开发一个待办事项应用",
  "constraints": [
    "使用 JavaScript 技术栈",
    "开发时间<1 天",
    "支持 100 个并发用户"
  ],
  "successCriteria": [
    "可以添加待办",
    "可以删除待办",
    "可以标记完成",
    "界面简洁易用"
  ]
}
```

---

### 2. 计划质量

**好的计划**：
- 步骤清晰（每个步骤做什么）
- 依赖明确（哪些步骤有先后顺序）
- 可执行（每个步骤都能完成）
- 可验证（有明确的完成标准）

**示例**：
```javascript
{
  "steps": [
    {
      "id": 1,
      "description": "设计数据库 schema",
      "dependencies": [],
      "expectedOutput": "数据库表结构文档"
    },
    {
      "id": 2,
      "description": "实现用户认证 API",
      "dependencies": [1],  // 依赖步骤 1
      "expectedOutput": "/login, /register 端点"
    },
    {
      "id": 3,
      "description": "实现待办事项 API",
      "dependencies": [1, 2],  // 依赖步骤 1 和 2
      "expectedOutput": "CRUD 端点"
    }
  ]
}
```

---

### 3. 进度跟踪

**跟踪信息**：
```javascript
const progress = {
  total: plan.steps.length,
  completed: 0,
  failed: 0,
  current: null,
  stepResults: [],
  blockedSteps: []  // 因依赖失败而阻塞的步骤
};
```

---

### 4. 灵活调整

**计划调整策略**：
```javascript
async executePlan(task, plan) {
  // ...
  
  if (result.success) {
    completedSteps.add(executableStep.id);
    results.completed++;
  } else {
    results.failed++;
    
    // 尝试调整计划
    const adjustedPlan = await this.adjustPlan(plan, executableStep, result.error);
    if (adjustedPlan) {
      plan = adjustedPlan;
      // 重试或跳过
    }
  }
  
  // ...
}

async adjustPlan(originalPlan, failedStep, error) {
  const prompt = `
原计划执行失败：
步骤：${failedStep.description}
错误：${error}

请调整计划以绕过这个问题。

选项：
1. 修改失败步骤的实现方式
2. 跳过这个步骤（如果不关键）
3. 添加新的步骤来解决问题

调整后的计划：`;
  
  return await this.llm.generate(prompt);
}
```

---

## ⚠️ 常见问题与解决方案

### 问题 1：计划过于复杂

**现象**：步骤太多（>20 步），难以执行。

**解决方案**：
```javascript
async plan(task, understanding) {
  const prompt = `
请制定计划：

要求：
1. 步骤数量控制在 5-15 步
2. 如果任务太复杂，可以分组为几个阶段
3. 优先关注关键步骤
4. 可选步骤标记为"可选"

计划：`;
  
  return await this.llm.generate(prompt);
}
```

---

### 问题 2：步骤依赖循环

**现象**：步骤 A 依赖 B，B 依赖 A，无法执行。

**解决方案**：
```javascript
async plan(task, understanding) {
  const prompt = `
制定计划时，确保：
1. **没有循环依赖**（A 依赖 B，B 依赖 A）
2. 依赖关系是**有向无环图**（DAG）
3. 至少有一个步骤没有依赖（可以作为起点）

计划：`;
  
  return await this.llm.generate(prompt);
}

// 执行时检测循环依赖
findExecutableStep(plan, completedSteps) {
  const visited = new Set();
  const recStack = new Set();
  
  // 检测循环依赖
  if (this.hasCycle(plan.steps, visited, recStack)) {
    throw new Error('Circular dependency detected');
  }
  
  // 找到可执行的步骤
  return plan.steps.find(step => 
    !completedSteps.has(step.id) &&
    step.dependencies.every(depId => completedSteps.has(depId))
  );
}
```

---

### 问题 3：步骤执行失败

**现象**：某一步无法完成。

**解决方案**：
```javascript
async executeStep(task, step, previousResults) {
  // 添加重试机制
  for (let attempt = 1; attempt <= 3; attempt++) {
    try {
      const output = await this.llm.generate(prompt);
      return { success: true, output };
    } catch (error) {
      if (attempt === 3) {
        // 最后一次失败，尝试替代方案
        return await this.executeAlternative(task, step, previousResults);
      }
      await this.sleep(1000 * attempt);
    }
  }
}

async executeAlternative(task, step, previousResults) {
  const prompt = `
步骤无法按原计划执行：
${step.description}

请提供替代方案来完成这个步骤的目标。

替代方案：`;
  
  return await this.llm.generate(prompt);
}
```

---

## 🔧 优化技巧

### 1. 分阶段执行

```javascript
async execute(task) {
  const understanding = await this.understand(task);
  const plan = await this.plan(task, understanding);
  
  // 将计划分为几个阶段
  const phases = this.groupIntoPhases(plan.steps);
  
  for (const phase of phases) {
    console.log(`\n[Phase: ${phase.name}]`);
    const phasePlan = { steps: phase.steps };
    const results = await this.executePlan(task, phasePlan);
    
    // 阶段完成后评估
    const phaseAssessment = await this.assessPhase(phase.name, results);
    if (!phaseAssessment.pass) {
      console.warn(`Phase ${phase.name} failed assessment.`);
      // 可以调整后续阶段
    }
  }
  
  // ...
}
```

---

### 2. 并行执行独立步骤

```javascript
async executePlan(task, plan) {
  // 找到所有可并行执行的步骤（没有相互依赖）
  const independentSteps = this.findIndependentSteps(plan.steps);
  
  // 并行执行
  const parallelResults = await Promise.all(
    independentSteps.map(step => this.executeStep(task, step, []))
  );
  
  // ...
}

findIndependentSteps(steps) {
  // 找到没有依赖且不被依赖的步骤
  const allDependencies = new Set(
    steps.flatMap(s => s.dependencies)
  );
  
  return steps.filter(step => 
    step.dependencies.length === 0 &&
    !allDependencies.has(step.id)
  );
}
```

---

### 3. 进度可视化

```javascript
visualizeProgress(plan, results) {
  const progressBar = (completed, total) => {
    const percentage = Math.round(completed / total * 100);
    const filled = '█'.repeat(percentage / 5);
    const empty = '░'.repeat(20 - percentage / 5);
    return `[${filled}${empty}] ${percentage}%`;
  };
  
  console.log(`\n进度：${progressBar(results.completed, results.total)}`);
  console.log(`完成：${results.completed}/${results.total}`);
  console.log(`失败：${results.failed}`);
}
```

---

## 📊 性能评估

### 评估指标

| 指标 | 描述 | 目标 |
|------|------|------|
| **计划完成率** | 成功完成的计划比例 | >90% |
| **步骤成功率** | 成功执行的步骤比例 | >95% |
| **平均执行时间** | 从开始到完成的时间 | <5 分钟 |
| **计划质量** | 计划合理性评分 | >8/10 |

---

### 优化方向

1. **提高计划质量**：更好的任务分解
2. **减少执行时间**：并行执行独立步骤
3. **提高成功率**：更好的错误处理
4. **灵活调整**：根据执行情况动态调整计划

---

## 🔗 相关模式

- **ReAct**：可以在执行步骤时使用 ReAct
- **Tree of Thoughts**：可以在规划阶段探索多个计划
- **Manager-Worker**：可以将步骤分配给不同 Worker

---

## 📚 参考资源

- **原论文**: [Plan-and-Solve Prompting](https://arxiv.org/abs/2305.04091)
- **实现参考**: [LangChain Planning](https://python.langchain.com/docs/modules/agents/agent_types/planning)
- **应用案例**: [Complex Task Planning with LLMs](https://plan-and-solve.github.io/)

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02  
**下次回顾**: 2026-04-09
