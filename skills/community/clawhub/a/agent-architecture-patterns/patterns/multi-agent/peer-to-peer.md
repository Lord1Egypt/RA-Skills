# 对等模式 (Peer-to-Peer) - 多 Agent 协作

> **版本**: 1.0.0  
> **适用场景**: 任务可并行、Agent 能力相似、需要协作讨论的场景  
> **复杂度**: ⭐⭐（中低）

---

## 🧠 核心思想

**对等模式 = 多个平等 Agent + 协作共识**

- **平等关系**：没有管理者，所有 Agent 地位平等
- **协作讨论**：通过对话、辩论达成共识
- **并行执行**：各自执行独立任务，然后整合

**与主从模式的区别**：
- 主从模式：1 个 Manager 决策，Worker 执行
- 对等模式：所有 Agent 平等，共同决策

---

## 📊 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                      Input Task                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Distributed Discussion                      │
│    Agent1 ←→ Agent2 ←→ Agent3 ←→ ...                    │
│       ↑        ↑         ↑                               │
│       └────────┴─────────┘                               │
│            平等讨论、辩论、共识                           │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Parallel Execution                          │
│    Agent1      Agent2      Agent3                        │
│   子任务 A     子任务 B     子任务 C                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│              Result Integration                          │
│         投票/共识/合并 → Final Output                    │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class PeerToPeerAgent {
  constructor(agents, options = {}) {
    this.agents = agents;
    this.consensusThreshold = options.consensusThreshold || 0.6; // 60% 同意
    this.maxRounds = options.maxRounds || 3;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async collaborate(task) {
    if (this.verbose) {
      console.log(`[P2P] 开始协作任务：${task}`);
      console.log(`[P2P] 参与 Agent: ${this.agents.length}个`);
    }
    
    // Phase 1: 讨论
    const discussionResult = await this.discuss(task);
    
    if (this.verbose) {
      console.log(`[P2P] 讨论完成，达成共识：${discussionResult.consensus}`);
    }
    
    // Phase 2: 并行执行
    const executionResults = await this.executeParallel(task, discussionResult.plan);
    
    if (this.verbose) {
      console.log(`[P2P] 执行完成，收到 ${executionResults.length} 个结果`);
    }
    
    // Phase 3: 整合
    const finalResult = await this.integrate(task, executionResults);
    
    return finalResult;
  }

  /**
   * Phase 1: 讨论达成共识
   */
  async discuss(task) {
    const discussionHistory = [];
    
    for (let round = 1; round <= this.maxRounds; round++) {
      if (this.verbose) {
        console.log(`\n[Round ${round}/${this.maxRounds}]`);
      }
      
      // 每个 Agent 发表观点
      const opinions = await this.collectOpinions(task, discussionHistory);
      
      if (this.verbose) {
        opinions.forEach((op, i) => {
          console.log(`  [Agent ${i + 1}] ${opinion.summary}`);
        });
      }
      
      // 检查是否达成共识
      const consensus = this.checkConsensus(opinions);
      
      if (consensus.reached) {
        if (this.verbose) {
          console.log(`[Consensus Reached] ${consensus.agreement}`);
        }
        
        return {
          consensus: true,
          agreement: consensus.agreement,
          plan: consensus.plan
        };
      }
      
      // 记录讨论历史
      discussionHistory.push({ round, opinions });
    }
    
    // 未达到共识，取多数意见
    if (this.verbose) {
      console.log('[No Consensus] 使用多数意见');
    }
    
    const majorityOpinion = this.getMajorityOpinion(opinions);
    return {
      consensus: false,
      agreement: majorityOpinion.summary,
      plan: majorityOpinion.plan
    };
  }

  /**
   * 收集所有 Agent 的观点
   */
  async collectOpinions(task, history) {
    const opinions = await Promise.all(
      this.agents.map(agent => agent.formOpinion(task, history))
    );
    return opinions;
  }

  /**
   * 检查是否达成共识
   */
  checkConsensus(opinions) {
    // 计算相似度
    const similarityMatrix = this.calculateSimilarity(opinions);
    
    // 找到最大的共识群体
    const largestGroup = this.findLargestConsensusGroup(similarityMatrix);
    const agreementRatio = largestGroup.length / opinions.length;
    
    if (agreementRatio >= this.consensusThreshold) {
      return {
        reached: true,
        agreement: opinions[largestGroup[0]].summary,
        plan: opinions[largestGroup[0]].plan
      };
    }
    
    return { reached: false };
  }

  /**
   * 计算意见相似度矩阵
   */
  calculateSimilarity(opinions) {
    const n = opinions.length;
    const matrix = [];
    
    for (let i = 0; i < n; i++) {
      matrix[i] = [];
      for (let j = 0; j < n; j++) {
        if (i === j) {
          matrix[i][j] = 1.0;
        } else {
          matrix[i][j] = this.computeSimilarity(opinions[i], opinions[j]);
        }
      }
    }
    
    return matrix;
  }

  /**
   * 计算两个意见的相似度
   */
  computeSimilarity(op1, op2) {
    // 简化实现：基于关键词重叠
    const keywords1 = new Set(op1.summary.toLowerCase().split(/\s+/));
    const keywords2 = new Set(op2.summary.toLowerCase().split(/\s+/));
    
    const intersection = [...keywords1].filter(k => keywords2.has(k)).length;
    const union = new Set([...keywords1, ...keywords2]).size;
    
    return intersection / union;
  }

  /**
   * 找到最大的共识群体
   */
  findLargestConsensusGroup(similarityMatrix) {
    const n = similarityMatrix.length;
    const threshold = 0.7; // 相似度>70% 认为是一组
    const visited = new Set();
    const groups = [];
    
    for (let i = 0; i < n; i++) {
      if (!visited.has(i)) {
        const group = [i];
        visited.add(i);
        
        for (let j = i + 1; j < n; j++) {
          if (!visited.has(j) && similarityMatrix[i][j] >= threshold) {
            group.push(j);
            visited.add(j);
          }
        }
        
        groups.push(group);
      }
    }
    
    // 返回最大的群体
    return groups.sort((a, b) => b.length - a.length)[0] || [];
  }

  /**
   * 获取多数意见
   */
  getMajorityOpinion(opinions) {
    // 简化实现：返回第一个（实际应该聚类）
    return opinions[0];
  }

  /**
   * Phase 2: 并行执行
   */
  async executeParallel(task, plan) {
    const subtasks = this.decomposeByAgents(task, plan);
    
    const results = await Promise.all(
      subtasks.map((subtask, i) => 
        this.agents[i].execute(subtask)
      )
    );
    
    return results;
  }

  /**
   * 按 Agent 分解任务
   */
  decomposeByAgents(task, plan) {
    // 简化实现：平均分配
    const subtasks = [];
    for (let i = 0; i < this.agents.length; i++) {
      subtasks.push({
        description: `${task} - 部分 ${i + 1}/${this.agents.length}`,
        agent: this.agents[i]
      });
    }
    return subtasks;
  }

  /**
   * Phase 3: 整合结果
   */
  async integrate(task, results) {
    // 投票整合
    const votes = await Promise.all(
      results.map(result => this.vote(task, result))
    );
    
    // 选择得票最高的结果
    const bestIndex = votes.indexOf(Math.max(...votes));
    return results[bestIndex];
  }

  /**
   * 投票
   */
  async vote(task, result) {
    // 简化实现：返回随机分数
    return Math.random();
  }

  /**
   * 默认 LLM
   */
  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Generated.';
    }
  };
}

/**
 * 对等 Agent
 */
class PeerAgent {
  constructor(id, expertise) {
    this.id = id;
    this.expertise = expertise;
    this.llm = null;
  }

  async formOpinion(task, history) {
    const prompt = `
任务：${task}

你的专业领域：${this.expertise}

讨论历史：
${this.formatHistory(history)}

请发表你的观点：
1. 你对任务的理解
2. 你建议的方案
3. 你的理由

观点：`;
    
    const summary = await this.llm.generate(prompt);
    
    return {
      agent: this.id,
      summary,
      plan: this.extractPlan(summary)
    };
  }

  async execute(subtask) {
    const prompt = `
执行任务：${subtask.description}

专业领域：${this.expertise}

结果：`;
    
    return await this.llm.generate(prompt);
  }

  formatHistory(history) {
    if (history.length === 0) return '（无）';
    
    return history.map(h => 
      `Round ${h.round}:\n${h.opinions.map(op => `  - ${op.agent}: ${op.summary}`).join('\n')}`
    ).join('\n\n');
  }

  extractPlan(summary) {
    // 从观点中提取计划
    return summary;
  }
}
```

---

### 使用示例

```javascript
// 创建对等 Agent
const agents = [
  new PeerAgent('agent-1', '前端开发'),
  new PeerAgent('agent-2', '后端开发'),
  new PeerAgent('agent-3', '数据库设计'),
  new PeerAgent('agent-4', '用户体验')
];

// 创建协作系统
const p2p = new PeerToPeerAgent(agents, {
  consensusThreshold: 0.6,
  maxRounds: 3,
  verbose: true
});

// 执行任务
const task = '设计一个电商网站的技术方案';
const result = await p2p.collaborate(task);
console.log(result);
```

---

## 🎯 适用场景

### ✅ 适合的场景

1. **需要多视角**：任务需要不同专业视角
2. **无明确领导**：没有天然的管理者
3. **鼓励创新**：需要多样化的想法
4. **并行任务**：任务可以分解为独立子任务

### ❌ 不适合的场景

1. **需要快速决策**：讨论耗时
2. **有明确权威**：已有专家或领导
3. **任务高度依赖**：子任务之间有强依赖
4. **资源有限**：Agent 数量少

---

## 🔗 相关模式

- **主从模式**：有明确管理者的场景
- **层级模式**：大型复杂项目
- **Reflection**：可以结合自我反思

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02
