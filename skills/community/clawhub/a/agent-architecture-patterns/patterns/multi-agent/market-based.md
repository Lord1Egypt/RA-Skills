# 市场模式 (Market-Based) - 多 Agent 协作

> **版本**: 1.0.0  
> **适用场景**: 动态任务分配、Agent 能力差异大、需要优化资源的场景  
> **复杂度**: ⭐⭐⭐⭐（高）

---

## 🧠 核心思想

**市场模式 = 任务竞价 + 市场机制**

- **任务发布**：任务作为"商品"在市场上发布
- **Agent 竞价**：Agent 根据自身能力出价
- **价高者得**：选择最优 bid 的 Agent 执行
- **支付机制**：完成后获得"报酬"（积分、优先级等）

**核心优势**：
- **自组织**：无需中央计划，市场自动调节
- **效率优化**：任务自动流向最合适的 Agent
- **动态适应**：Agent 负载变化时自动调整

---

## 📊 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                   Task Marketplace                       │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐     │
│  │   Task A    │  │   Task B    │  │   Task C    │     │
│  │ Budget: 100 │  │ Budget: 200 │  │ Budget: 150 │     │
│  └─────────────┘  └─────────────┘  └─────────────┘     │
└─────────────────────────────────────────────────────────┘
              ↓               ↓               ↓
        ┌─────┴─────┐   ┌─────┴─────┐   ┌─────┴─────┐
        ↓           ↓   ↓           ↓   ↓           ↓
   ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐
   │ Agent 1 │ │ Agent 2 │ │ Agent 3 │ │ Agent 4 │
   │  Bid: 90│ │  Bid: 95│ │ Bid: 140│ │ Bid: 160│
   └─────────┘ └─────────┘ └─────────┘ └─────────┘
        ↓           ↓           ↓           ↓
   ✅ 获得     ❌ 失败    ✅ 获得     ❌ 失败
   Task A      Task A    Task C      Task C
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class MarketBasedAgent {
  constructor(options = {}) {
    this.agents = options.agents || [];
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
    this.market = new Marketplace();
  }

  async execute(tasks) {
    if (this.verbose) {
      console.log(`[Market] 开始分配 ${tasks.length} 个任务`);
    }
    
    // Phase 1: 发布任务
    const postedTasks = await this.postTasks(tasks);
    
    if (this.verbose) {
      console.log(`[Market] 发布 ${postedTasks.length} 个任务`);
    }
    
    // Phase 2: Agent 竞价
    const bids = await this.collectBids(postedTasks);
    
    if (this.verbose) {
      console.log(`[Market] 收到 ${bids.length} 个竞价`);
    }
    
    // Phase 3: 分配任务
    const assignments = this.assignTasks(postedTasks, bids);
    
    if (this.verbose) {
      console.log(`[Market] 分配 ${assignments.length} 个任务`);
    }
    
    // Phase 4: 执行任务
    const results = await this.executeTasks(assignments);
    
    // Phase 5: 结算
    await this.settlePayments(assignments, results);
    
    return results;
  }

  async postTasks(tasks) {
    const postedTasks = [];
    
    for (const task of tasks) {
      const postedTask = await this.market.postTask(task);
      postedTasks.push(postedTask);
    }
    
    return postedTasks;
  }

  async collectBids(tasks) {
    const allBids = [];
    
    for (const task of tasks) {
      const bids = await Promise.all(
        this.agents.map(agent => agent.submitBid(task))
      );
      allBids.push(...bids);
    }
    
    return allBids;
  }

  assignTasks(tasks, bids) {
    const assignments = [];
    
    for (const task of tasks) {
      // 找到所有对该任务的竞价
      const taskBids = bids.filter(bid => bid.taskId === task.id);
      
      if (taskBids.length === 0) {
        if (this.verbose) {
          console.warn(`[Market] 任务 ${task.id} 无竞价`);
        }
        continue;
      }
      
      // 选择最优竞价（最高分/最低价格）
      const bestBid = taskBids.sort((a, b) => b.score - a.score)[0];
      
      assignments.push({
        task,
        agent: bestBid.agent,
        bid: bestBid
      });
      
      if (this.verbose) {
        console.log(`[Market] 任务 ${task.id} → Agent ${bestBid.agent.id} (分数：${bestBid.score})`);
      }
    }
    
    return assignments;
  }

  async executeTasks(assignments) {
    const results = [];
    
    for (const assignment of assignments) {
      const result = await assignment.agent.execute(assignment.task);
      results.push({
        task: assignment.task,
        agent: assignment.agent,
        result,
        success: true
      });
    }
    
    return results;
  }

  async settlePayments(assignments, results) {
    for (const result of results) {
      if (result.success) {
        await this.market.pay(result.agent, result.task.budget);
      }
    }
  }

  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Completed.';
    }
  };
}

/**
 * 市场
 */
class Marketplace {
  constructor() {
    this.tasks = new Map();
    this.agents = new Map();
    this.taskIdCounter = 0;
  }

  async postTask(task) {
    const id = `task-${++this.taskIdCounter}`;
    const postedTask = {
      id,
      description: task.description,
      budget: task.budget || 100,
      requirements: task.requirements || [],
      deadline: task.deadline || Date.now() + 3600000
    };
    this.tasks.set(id, postedTask);
    return postedTask;
  }

  async pay(agent, amount) {
    // 简化实现
    console.log(`[Market] 支付 ${amount} 给 Agent ${agent.id}`);
  }
}

/**
 * 市场 Agent
 */
class MarketAgent {
  constructor(id, skills, budget = 1000) {
    this.id = id;
    this.skills = skills || [];
    this.budget = budget;
    this.completedTasks = 0;
    this.llm = null;
  }

  async submitBid(task) {
    // 计算能力匹配度
    const skillMatch = this.calculateSkillMatch(task.requirements);
    
    // 计算负载（预算越少越不想接）
    const loadFactor = this.budget / 1000;
    
    // 计算竞价分数
    const score = skillMatch * 0.7 + loadFactor * 0.3;
    
    return {
      taskId: task.id,
      agent: this,
      score,
      bid: task.budget * (1 - skillMatch * 0.2) // 技能越匹配，要价越低
    };
  }

  calculateSkillMatch(requirements) {
    if (requirements.length === 0) return 0.5;
    
    const matchedSkills = requirements.filter(skill => 
      this.skills.includes(skill)
    ).length;
    
    return matchedSkills / requirements.length;
  }

  async execute(task) {
    const prompt = `
执行任务：${task.description}

技能：${this.skills.join(', ')}

结果：`;
    
    return await this.llm.generate(prompt);
  }
}
```

---

### 使用示例

```javascript
// 创建 Agent
const agents = [
  new MarketAgent('agent-1', ['javascript', 'react'], 1000),
  new MarketAgent('agent-2', ['python', 'ml'], 800),
  new MarketAgent('agent-3', ['javascript', 'nodejs'], 1200),
  new MarketAgent('agent-4', ['python', 'data'], 900)
];

// 创建市场系统
const market = new MarketBasedAgent({
  agents,
  verbose: true
});

// 发布任务
const tasks = [
  { description: '开发 React 组件', budget: 150, requirements: ['javascript', 'react'] },
  { description: '训练 ML 模型', budget: 200, requirements: ['python', 'ml'] },
  { description: '开发 Node.js API', budget: 180, requirements: ['javascript', 'nodejs'] }
];

// 执行
const results = await market.execute(tasks);
console.log(results);
```

---

## 🎯 适用场景

### ✅ 适合的场景

1. **动态任务**：任务随时到达
2. **异构 Agent**：Agent 能力差异大
3. **资源优化**：需要最优分配
4. **大规模系统**：Agent 数量多

### ❌ 不适合的场景

1. **任务有依赖**：需要协调
2. **紧急任务**：竞价耗时
3. **同质 Agent**：能力相似
4. **小系统**：过度复杂

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02
