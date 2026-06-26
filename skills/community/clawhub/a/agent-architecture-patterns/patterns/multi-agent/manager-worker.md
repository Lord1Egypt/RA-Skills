# 主从模式 (Manager-Worker) - 多 Agent 协作

> **版本**: 1.0.0  
> **适用场景**: 任务可分解、需要协调、有明确管理逻辑的场景  
> **复杂度**: ⭐⭐⭐（中等）

---

## 🧠 核心思想

**主从模式 = 1 个 Manager + N 个 Workers**

- **Manager（管理者）**: 负责任务分解、分配、协调、整合
- **Worker（工作者）**: 负责执行具体子任务

**优势**：
- 职责清晰（管理 vs 执行分离）
- 易于扩展（添加更多 Worker）
- 容错性强（单个 Worker 失败不影响整体）

---

## 📊 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                      Input Task                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                    Manager Agent                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  1. Decompose (任务分解)                           │  │
│  │  2. Assign (任务分配)                              │  │
│  │  3. Monitor (进度监控)                             │  │
│  │  4. Integrate (结果整合)                           │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                    ↓           ↓           ↓
        ┌───────────┐   ┌───────────┐   ┌───────────┐
        │ Worker 1  │   │ Worker 2  │   │ Worker 3  │
        │  子任务 A  │   │  子任务 B  │   │  子任务 C  │
        └───────────┘   └───────────┘   └───────────┘
                ↓               ↓               ↓
            Result A        Result B        Result C
                    ↓           ↓           ↓
┌─────────────────────────────────────────────────────────┐
│                    Manager Agent                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │  5. Aggregate (结果聚合)                           │  │
│  │  6. Validate (质量验证)                            │  │
│  │  7. Output (最终输出)                              │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
                  Final Output
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class ManagerAgent {
  constructor(workerAgents, options = {}) {
    this.workers = workerAgents;
    this.maxRetries = options.maxRetries || 3;
    this.timeout = options.timeout || 30000;
  }

  async coordinate(task) {
    console.log(`[Manager] 接收任务：${task}`);
    
    // Step 1: 任务分解
    const subtasks = await this.decompose(task);
    console.log(`[Manager] 分解为 ${subtasks.length} 个子任务`);
    
    // Step 2: 任务分配
    const assignments = this.assign(subtasks);
    console.log(`[Manager] 分配任务给 ${assignments.size} 个 Worker`);
    
    // Step 3: 并行执行
    const results = await this.executeParallel(assignments);
    console.log(`[Manager] 收到 ${results.length} 个结果`);
    
    // Step 4: 结果整合
    const finalResult = await this.integrate(task, results);
    console.log(`[Manager] 任务完成`);
    
    return finalResult;
  }

  async decompose(task) {
    // 调用 LLM 进行任务分解
    const prompt = `
将以下任务分解为独立的子任务：
${task}

要求：
1. 每个子任务应该是独立的
2. 子任务数量适中（3-10 个）
3. 明确每个子任务的目标

请以 JSON 数组格式返回：
[
  {
    "id": "task-1",
    "description": "子任务描述",
    "requiredSkills": ["技能 1", "技能 2"]
  }
]

子任务列表：`;
    
    const response = await this.callLLM(prompt);
    return JSON.parse(response);
  }

  assign(subtasks) {
    // 根据 Worker 能力分配任务
    const assignments = new Map();
    
    for (const subtask of subtasks) {
      const worker = this.selectWorker(subtask);
      if (!assignments.has(worker.id)) {
        assignments.set(worker.id, []);
      }
      assignments.get(worker.id).push(subtask);
    }
    
    return assignments;
  }

  selectWorker(subtask) {
    // 根据子任务所需技能选择最合适的 Worker
    const requiredSkills = subtask.requiredSkills || [];
    
    let bestWorker = null;
    let bestScore = -1;
    
    for (const worker of this.workers) {
      const score = this.calculateMatchScore(worker, requiredSkills);
      if (score > bestScore) {
        bestScore = score;
        bestWorker = worker;
      }
    }
    
    return bestWorker || this.workers[0];
  }

  calculateMatchScore(worker, requiredSkills) {
    // 计算 Worker 技能匹配度
    const workerSkills = new Set(worker.skills || []);
    const matchedSkills = requiredSkills.filter(skill => 
      workerSkills.has(skill)
    );
    return matchedSkills.length / (requiredSkills.length || 1);
  }

  async executeParallel(assignments) {
    const promises = [];
    
    for (const [workerId, subtasks] of assignments) {
      const worker = this.workers.find(w => w.id === workerId);
      
      const promise = Promise.all(
        subtasks.map(subtask => this.executeWithRetry(worker, subtask))
      );
      
      promises.push(promise);
    }
    
    const results = await Promise.all(promises);
    return results.flat();
  }

  async executeWithRetry(worker, subtask) {
    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const result = await Promise.race([
          worker.execute(subtask),
          this.timeoutPromise(this.timeout)
        ]);
        
        return {
          taskId: subtask.id,
          success: true,
          result,
          worker: worker.id
        };
      } catch (error) {
        console.warn(`[Worker ${worker.id}] 尝试 ${attempt} 失败: ${error.message}`);
        
        if (attempt === this.maxRetries) {
          return {
            taskId: subtask.id,
            success: false,
            error: error.message,
            worker: worker.id
          };
        }
      }
    }
  }

  timeoutPromise(timeout) {
    return new Promise((_, reject) => {
      setTimeout(() => reject(new Error('Timeout')), timeout);
    });
  }

  async integrate(task, results) {
    // 调用 LLM 整合结果
    const successfulResults = results.filter(r => r.success);
    const failedResults = results.filter(r => !r.success);
    
    const prompt = `
原始任务：${task}

成功执行的结果 (${successfulResults.length}个):
${JSON.stringify(successfulResults.map(r => r.result), null, 2)}

失败的结果 (${failedResults.length}个):
${JSON.stringify(failedResults, null, 2)}

请整合所有成功结果，生成最终答案。如果有失败的任务，说明影响。

最终答案：`;
    
    return await this.callLLM(prompt);
  }

  async callLLM(prompt) {
    // 调用大语言模型
    const response = await llm.generate(prompt);
    return response;
  }
}

// Worker Agent 类
class WorkerAgent {
  constructor(id, skills, capabilities) {
    this.id = id;
    this.skills = skills;
    this.capabilities = capabilities;
  }

  async execute(subtask) {
    console.log(`[Worker ${this.id}] 执行任务：${subtask.description}`);
    
    // 根据任务类型调用不同能力
    if (this.capabilities.codeReview) {
      return await this.reviewCode(subtask);
    } else if (this.capabilities.webSearch) {
      return await this.searchWeb(subtask);
    } else if (this.capabilities.dataAnalysis) {
      return await this.analyzeData(subtask);
    } else {
      return await this.genericExecute(subtask);
    }
  }

  async reviewCode(subtask) {
    // 代码审查实现
    const code = subtask.code;
    const issues = [];
    
    // 调用静态分析工具
    const analysis = await this.runStaticAnalysis(code);
    issues.push(...analysis);
    
    // 调用 LLM 进行代码审查
    const prompt = `审查以下代码：
${code}

关注点：
- 代码质量
- 潜在 bug
- 性能问题
- 安全漏洞

审查结果：`;
    
    const review = await this.callLLM(prompt);
    issues.push(review);
    
    return { issues, suggestions: review };
  }

  async searchWeb(subtask) {
    // 网络搜索实现
    const query = subtask.query;
    const results = await webSearch(query);
    return results;
  }

  async analyzeData(subtask) {
    // 数据分析实现
    const data = subtask.data;
    const analysis = await this.runAnalysis(data);
    return analysis;
  }

  async genericExecute(subtask) {
    // 通用执行
    const prompt = `执行以下任务：
${subtask.description}

结果：`;
    
    return await this.callLLM(prompt);
  }

  async callLLM(prompt) {
    const response = await llm.generate(prompt);
    return response;
  }

  async runStaticAnalysis(code) {
    // 调用静态分析工具（如 ESLint）
    // 这里简化实现
    return [];
  }

  async runAnalysis(data) {
    // 调用数据分析工具
    // 这里简化实现
    return { summary: 'Analysis result' };
  }
}
```

---

### 使用示例

```javascript
// 创建 Worker Agents
const workers = [
  new WorkerAgent('worker-1', ['javascript', 'python'], {
    codeReview: true,
    webSearch: false,
    dataAnalysis: false
  }),
  
  new WorkerAgent('worker-2', ['research', 'writing'], {
    codeReview: false,
    webSearch: true,
    dataAnalysis: false
  }),
  
  new WorkerAgent('worker-3', ['statistics', 'visualization'], {
    codeReview: false,
    webSearch: false,
    dataAnalysis: true
  })
];

// 创建 Manager Agent
const manager = new ManagerAgent(workers, {
  maxRetries: 3,
  timeout: 30000
});

// 执行复杂任务
const task = '分析这个 GitHub 项目的代码质量，并搜索相关技术文章';
const result = await manager.coordinate(task);

console.log(result);
```

---

### 执行轨迹示例

```
[Manager] 接收任务：分析这个 GitHub 项目的代码质量，并搜索相关技术文章

[Manager] 分解为 4 个子任务：
  - task-1: 下载并分析项目代码结构
  - task-2: 执行代码静态分析
  - task-3: 搜索项目相关技术文章
  - task-4: 总结分析结果

[Manager] 分配任务给 3 个 Worker：
  - worker-1: [task-1, task-2] (代码分析能力)
  - worker-2: [task-3] (搜索能力)
  - worker-3: [task-4] (分析总结能力)

[Worker worker-1] 执行任务：下载并分析项目代码结构
[Worker worker-1] 执行任务：执行代码静态分析
[Worker worker-2] 执行任务：搜索项目相关技术文章

[Manager] 收到 4 个结果

[Manager] 整合结果，生成最终答案

[Manager] 任务完成

最终答案：
## 代码质量分析报告

### 项目结构
- 语言：JavaScript/TypeScript
- 文件数：156
- 代码行数：12,450

### 静态分析结果
- 代码风格问题：23 个
- 潜在 Bug：5 个
- 性能问题：3 个
- 安全漏洞：1 个（中危）

### 相关技术文章
1. "Modern JavaScript Best Practices" - Medium
2. "TypeScript for Large Projects" - Dev.to
3. "Security in Node.js Applications" - OWASP

### 建议
1. 修复 1 个安全漏洞（优先级高）
2. 重构 3 个性能热点
3. 统一代码风格
```

---

## 🎯 关键设计要点

### 1. 任务分解策略

**好的分解**：
- 子任务独立（可并行执行）
- 粒度适中（不太大也不太小）
- 目标明确（有清晰的完成标准）

**分解示例**：
```javascript
// ❌ 不好的分解（子任务有依赖）
[
  "写代码",
  "测试代码",  // 依赖"写代码"完成
  "部署代码"   // 依赖"测试代码"通过
]

// ✅ 好的分解（子任务独立）
[
  "编写用户认证模块",
  "编写数据访问模块",
  "编写 API 路由模块"
]
```

---

### 2. Worker 选择策略

**选择维度**：
- **技能匹配**：Worker 技能与任务需求匹配度
- **负载均衡**：避免某些 Worker 过载
- **历史表现**：选择历史成功率高的 Worker

**实现**：
```javascript
selectWorker(subtask) {
  const scores = this.workers.map(worker => ({
    worker,
    skillMatch: this.calculateMatchScore(worker, subtask.requiredSkills),
    load: this.getCurrentLoad(worker),
    successRate: worker.getSuccessRate()
  }));
  
  // 综合评分
  scores.forEach(score => {
    score.total = score.skillMatch * 0.5 + 
                  (1 - score.load) * 0.3 + 
                  score.successRate * 0.2;
  });
  
  return scores.sort((a, b) => b.total - a.total)[0].worker;
}
```

---

### 3. 容错机制

**重试策略**：
```javascript
async executeWithRetry(worker, subtask) {
  for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
    try {
      return await worker.execute(subtask);
    } catch (error) {
      if (attempt === this.maxRetries) {
        // 最后一次失败，尝试重新分配
        const backupWorker = this.findBackupWorker(worker);
        if (backupWorker) {
          return await backupWorker.execute(subtask);
        }
        throw error;
      }
      // 等待后重试（指数退避）
      await this.sleep(1000 * Math.pow(2, attempt));
    }
  }
}
```

---

### 4. 结果整合策略

**整合方式**：
- **简单拼接**：结果直接拼接
- **摘要总结**：LLM 总结关键点
- **结构化整合**：按模板组织结果

**实现**：
```javascript
async integrate(task, results) {
  const template = `
# ${task}

## 执行摘要
${this.generateSummary(results)}

## 详细结果
${this.formatResults(results)}

## 质量评估
${this.assessQuality(results)}

## 建议
${this.generateRecommendations(results)}
`;
  
  return template;
}
```

---

## ⚠️ 常见问题与解决方案

### 问题 1：任务分解不合理

**现象**：子任务之间有强依赖，无法并行。

**解决方案**：
```javascript
async decompose(task) {
  const prompt = `
将任务分解为**独立可并行执行**的子任务：
${task}

约束：
1. 子任务之间不能有依赖
2. 每个子任务可以单独完成
3. 所有子任务完成后，可以整合出最终结果
`;
  // ...
}
```

---

### 问题 2：Worker 负载不均

**现象**：某些 Worker 很忙，某些空闲。

**解决方案**：
```javascript
assign(subtasks) {
  // 考虑当前负载
  const assignments = new Map();
  const loads = new Map(this.workers.map(w => [w.id, 0]));
  
  for (const subtask of subtasks) {
    // 选择负载最低且技能匹配的 Worker
    const worker = this.workers
      .filter(w => this.skillsMatch(w, subtask))
      .sort((a, b) => loads.get(a.id) - loads.get(b.id))[0];
    
    if (!assignments.has(worker.id)) {
      assignments.set(worker.id, []);
    }
    assignments.get(worker.id).push(subtask);
    loads.set(worker.id, loads.get(worker.id) + 1);
  }
  
  return assignments;
}
```

---

### 问题 3：结果质量不一致

**现象**：不同 Worker 输出质量差异大。

**解决方案**：
```javascript
// 添加质量验证
async validate(result) {
  const prompt = `
评估以下结果的质量：
${JSON.stringify(result)}

评估维度：
1. 完整性（0-10）
2. 准确性（0-10）
3. 相关性（0-10）

如果任何维度<7，返回需要改进的地方。

评估结果：`;
  
  const evaluation = await this.callLLM(prompt);
  return evaluation;
}

// 低质量结果要求重新执行
if (qualityScore < 7) {
  return await this.executeWithRetry(worker, subtask);
}
```

---

## 🔧 优化技巧

### 1. 动态 Worker 池

根据任务需求动态创建/销毁 Worker：

```javascript
class DynamicManagerAgent extends ManagerAgent {
  async coordinate(task) {
    // 分析任务需要的技能
    const requiredSkills = await this.analyzeTaskSkills(task);
    
    // 检查现有 Worker
    const availableSkills = new Set(
      this.workers.flatMap(w => w.skills)
    );
    
    // 创建缺失技能的 Worker
    for (const skill of requiredSkills) {
      if (!availableSkills.has(skill)) {
        const newWorker = await this.createWorker(skill);
        this.workers.push(newWorker);
      }
    }
    
    return await super.coordinate(task);
  }
  
  async createWorker(skill) {
    // 动态创建 specialized Worker
    return new WorkerAgent(`worker-${skill}`, [skill], {
      [skill]: true
    });
  }
}
```

---

### 2. 结果缓存

避免重复执行相同任务：

```javascript
class CachedManagerAgent extends ManagerAgent {
  constructor(...args) {
    super(...args);
    this.cache = new Map();
  }
  
  async executeWithRetry(worker, subtask) {
    const cacheKey = this.hashSubtask(subtask);
    
    if (this.cache.has(cacheKey)) {
      console.log(`[Cache Hit] ${cacheKey}`);
      return this.cache.get(cacheKey);
    }
    
    const result = await super.executeWithRetry(worker, subtask);
    this.cache.set(cacheKey, result);
    
    return result;
  }
  
  hashSubtask(subtask) {
    return crypto
      .createHash('md5')
      .update(subtask.description)
      .digest('hex');
  }
}
```

---

### 3. 进度监控

实时监控任务执行进度：

```javascript
class MonitoredManagerAgent extends ManagerAgent {
  async coordinate(task) {
    const progress = {
      total: 0,
      completed: 0,
      failed: 0,
      startTime: Date.now()
    };
    
    const subtasks = await this.decompose(task);
    progress.total = subtasks.length;
    
    // 定期报告进度
    const progressInterval = setInterval(() => {
      console.log(`[Progress] ${progress.completed}/${progress.total} ` +
                  `(失败：${progress.failed}, 耗时：${Date.now() - progress.startTime}ms)`);
    }, 5000);
    
    try {
      const results = await this.executeParallel(/* ... */);
      progress.completed = results.filter(r => r.success).length;
      progress.failed = results.filter(r => !r.success).length;
      
      return await this.integrate(task, results);
    } finally {
      clearInterval(progressInterval);
      console.log(`[Progress] 完成：${progress.completed}/${progress.total}`);
    }
  }
}
```

---

## 📊 性能评估

### 评估指标

| 指标 | 描述 | 目标 |
|------|------|------|
| **任务完成率** | 成功完成的任务比例 | >95% |
| **并行效率** | 并行执行时间 / 串行执行时间 | <0.3 |
| **Worker 利用率** | Worker 忙碌时间比例 | >70% |
| **结果质量** | 整合结果的质量评分 | >8/10 |

---

### 优化方向

1. **提高并行度**：更好地任务分解
2. **减少等待**：优化任务分配
3. **提高质量**：添加质量验证
4. **降低成本**：复用 Worker、缓存结果

---

## 🔗 相关模式

- **流水线模式**：顺序处理，适合有依赖的任务
- **对等模式**：平等协作，适合讨论型任务
- **ReAct**：单 Agent 的推理 + 行动模式

---

## 📚 参考资源

- **CrewAI**: https://github.com/joaomdmoura/crewAI
- **AutoGen**: https://github.com/microsoft/autogen
- **Multi-Agent Collaboration Survey**: https://arxiv.org/abs/2308.01126

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02  
**下次回顾**: 2026-04-09
