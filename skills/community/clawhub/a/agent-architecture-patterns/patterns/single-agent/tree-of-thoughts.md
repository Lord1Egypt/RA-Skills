# Tree of Thoughts 模式 - 多路径探索

> **版本**: 1.0.0  
> **论文**: [Tree of Thoughts: Deliberate Problem Solving with Large Language Models](https://arxiv.org/abs/2305.10601)  
> **适用场景**: 需要创造性、有多个可能方案、可以评估方案质量的任务

---

## 🧠 核心思想

**Tree of Thoughts = Branch + Evaluate + Search**

传统方法的问题：
- **线性思考**：只沿着一条路径思考
- **容易陷入局部最优**：错过更好的解决方案
- **缺乏探索**：没有充分探索可能性

Tree of Thoughts 的突破：
- **多路径探索**：同时探索多个思考方向
- **评估选择**：评估每个路径的质量
- **智能搜索**：使用搜索算法（BFS/DFS/Beam）找到最优路径

---

## 📊 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    Task Input                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 1: Generate Initial Thoughts                       │
│  生成多个初始思考方向（3-5 个）                            │
│         Thought 1.1    Thought 1.2    Thought 1.3       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: Evaluate Thoughts                               │
│  评估每个思考的质量（1-10 分）                             │
│         7.5            8.2            6.1               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: Select Best Thoughts                            │
│  选择 top-k 个思考继续扩展（如 k=2）                        │
│         ✓              ✓              ✗                 │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 4: Expand Selected Thoughts                        │
│  为每个选中的思考生成子思考                               │
│      Thought 2.1  2.2          2.3  2.4                  │
└─────────────────────────────────────────────────────────┘
                          ↓
                    重复 Step 2-4
                    直到找到解决方案或达到深度限制
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class TreeOfThoughtsAgent {
  constructor(options = {}) {
    this.maxDepth = options.maxDepth || 3;
    this.branchFactor = options.branchFactor || 3;  // 每个节点生成几个子节点
    this.beamWidth = options.beamWidth || 2;        // 保留 top-k 个节点
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async execute(task) {
    if (this.verbose) {
      console.log(`[Tree of Thoughts] 开始任务：${task}`);
    }
    
    // 初始化根节点
    const root = {
      id: 'root',
      thought: '',
      depth: 0,
      score: 0,
      parent: null,
      children: []
    };
    
    // 生成初始思考
    const initialThoughts = await this.generateThoughts(task, root);
    root.children = initialThoughts;
    
    if (this.verbose) {
      console.log(`[Initial Thoughts] 生成 ${initialThoughts.length} 个初始思考`);
    }
    
    // Beam Search
    let currentLevel = initialThoughts;
    
    for (let depth = 1; depth <= this.maxDepth; depth++) {
      if (this.verbose) {
        console.log(`\n[Depth ${depth}/${this.maxDepth}]`);
      }
      
      // 评估当前层的所有思考
      const evaluatedThoughts = await this.evaluateThoughts(task, currentLevel);
      
      if (this.verbose) {
        evaluatedThoughts.forEach(t => {
          console.log(`  [${t.id}] Score: ${t.score} - ${t.thought.substring(0, 50)}...`);
        });
      }
      
      // 检查是否有解决方案
      const solution = evaluatedThoughts.find(t => t.score >= 9);
      if (solution) {
        if (this.verbose) {
          console.log(`[Solution Found] ${solution.thought}`);
        }
        return this.extractSolution(task, solution);
      }
      
      // 选择 top-k 个思考
      const selectedThoughts = this.selectTopK(evaluatedThoughts, this.beamWidth);
      
      if (this.verbose) {
        console.log(`[Selected] 保留 ${selectedThoughts.length} 个思考`);
      }
      
      // 为选中的思考生成子思考
      const nextLevel = [];
      for (const thought of selectedThoughts) {
        const children = await this.generateThoughts(task, thought);
        thought.children = children;
        nextLevel.push(...children);
      }
      
      if (nextLevel.length === 0) {
        if (this.verbose) {
          console.log('[No More Thoughts] 无法继续扩展');
        }
        break;
      }
      
      currentLevel = nextLevel;
    }
    
    // 没有达到 9 分，返回最佳方案
    const bestThought = currentLevel.sort((a, b) => b.score - a.score)[0];
    return this.extractSolution(task, bestThought);
  }

  /**
   * 生成思考（分支）
   */
  async generateThoughts(task, parent) {
    const prompt = `
任务：${task}

当前思考：${parent.thought || '（初始状态）'}

请生成 ${this.branchFactor} 个不同的思考方向。

要求：
1. 每个思考应该是不同的角度或方法
2. 思考应该具体、可执行
3. 思考之间应该有差异性

请以 JSON 数组格式返回：
[
  {
    "thought": "思考内容"
  }
]

思考：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\[[\s\S]*\]/);
      if (jsonMatch) {
        const thoughts = JSON.parse(jsonMatch[0]);
        return thoughts.map((t, i) => ({
          id: `${parent.id}-${i}`,
          thought: t.thought,
          depth: parent.depth + 1,
          score: 0,
          parent: parent.id,
          children: []
        }));
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      // 降级方案
      return [{
        id: `${parent.id}-0`,
        thought: '继续探索',
        depth: parent.depth + 1,
        score: 0,
        parent: parent.id,
        children: []
      }];
    }
  }

  /**
   * 评估思考
   */
  async evaluateThoughts(task, thoughts) {
    const evaluatedThoughts = [];
    
    for (const thought of thoughts) {
      const score = await this.evaluateThought(task, thought);
      evaluatedThoughts.push({ ...thought, score });
    }
    
    return evaluatedThoughts;
  }

  /**
   * 评估单个思考
   */
  async evaluateThought(task, thought) {
    const prompt = `
任务：${task}

思考：${thought.thought}

请评估这个思考的质量（1-10 分）：

评分标准：
- 10 分：完美解决方案，直接可以实施
- 8-9 分：很好的方案，少量改进即可
- 6-7 分：可行方案，需要一些改进
- 4-5 分：有潜力，但需要大量改进
- 1-3 分：不可行或方向错误

考虑因素：
1. 可行性：这个方案可以实施吗？
2. 有效性：能解决问题吗？
3. 效率：是高效的方法吗？
4. 完整性：覆盖了关键要点吗？

评分（只返回 1-10 的数字）：`;
    
    const response = await this.llm.generate(prompt);
    const score = parseFloat(response.match(/\d+(\.\d+)?/)?.[0] || '5');
    
    return Math.min(10, Math.max(1, score));
  }

  /**
   * 选择 top-k 个思考
   */
  selectTopK(thoughts, k) {
    return thoughts
      .sort((a, b) => b.score - a.score)
      .slice(0, k);
  }

  /**
   * 提取解决方案
   */
  async extractSolution(task, thought) {
    // 回溯到根节点，构建完整路径
    const path = [];
    let current = thought;
    
    while (current && current.id !== 'root') {
      path.unshift(current.thought);
      current = this.findThoughtById(current.parent, thought);
    }
    
    const prompt = `
任务：${task}

思考路径：
${path.join('\n→ ')}

请基于这个思考路径，生成最终的解决方案。

解决方案：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 根据 ID 查找思考（简化实现）
   */
  findThoughtById(id, thought) {
    // 实际实现需要在树中搜索
    return null;
  }

  /**
   * 默认 LLM
   */
  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Generated thought.';
    }
  };
}
```

---

### 使用示例

```javascript
// 创建 Agent
const agent = new TreeOfThoughtsAgent({
  maxDepth: 3,
  branchFactor: 3,
  beamWidth: 2,
  verbose: true
});

// 执行创造性任务
const task = '设计一个创新的移动应用，帮助人们养成健康习惯';

const result = await agent.execute(task);
console.log(result);
```

---

### 执行轨迹示例

```
[Tree of Thoughts] 开始任务：设计一个创新的移动应用，帮助人们养成健康习惯

[Initial Thoughts] 生成 3 个初始思考

[Depth 1/3]
  [root-0] Score: 7.5 - 基于游戏化的习惯追踪应用...
  [root-1] Score: 8.2 - AI 驱动的个性化健康教练...
  [root-2] Score: 6.1 - 社交监督习惯打卡应用...

[Selected] 保留 2 个思考

[Depth 2/3]
  [root-0-0] Score: 8.0 - 游戏化 + 成就系统...
  [root-0-1] Score: 7.2 - 游戏化 + 社交竞争...
  [root-1-0] Score: 8.8 - AI 教练 + 实时反馈...
  [root-1-1] Score: 8.5 - AI 教练 + 社区支持...

[Selected] 保留 2 个思考

[Depth 3/3]
  [root-1-0-0] Score: 9.2 - AI 教练 + 实时反馈 + 奖励机制...
  [root-1-0-1] Score: 8.9 - AI 教练 + 实时反馈 + 社交元素...

[Solution Found] AI 教练 + 实时反馈 + 奖励机制

最终解决方案：
## HealthAI - 智能健康习惯养成应用

### 核心功能
1. **AI 健康教练**
   -  personalized 习惯建议
   - 智能调整难度
   - 预测失败风险

2. **实时反馈**
   - 运动姿势识别
   - 饮食拍照分析
   - 睡眠质量监测

3. **奖励机制**
   - 成就系统
   - 积分兑换
   - 健康保险折扣

### 创新点
- AI 实时指导，不是简单追踪
- 与保险公司合作，提供实质奖励
- 预测性干预，防止习惯中断

### 商业模式
- 免费基础版
- 高级版 $9.99/月
- 保险公司合作分成
```

---

## 🎯 关键设计要点

### 1. 思考生成策略

**好的思考**：
- 具体明确（不是"做好一点"而是"添加用户反馈功能"）
- 可实现（不是"改变世界"而是"解决 X 问题"）
- 有差异性（不同思考代表不同方向）

**生成技巧**：
```javascript
async generateThoughts(task, parent) {
  // 提供思考角度提示
  const angles = [
    '技术创新角度',
    '用户体验角度',
    '商业模式角度',
    '市场需求角度',
    '竞争优势角度'
  ];
  
  const prompt = `
请从以下角度生成思考：
${angles.join(', ')}

每个角度生成 1 个思考：`;
  
  // ...
}
```

---

### 2. 评估函数设计

**评估维度**：
```javascript
async evaluateThought(task, thought) {
  const dimensions = [
    { name: '可行性', weight: 0.3 },
    { name: '有效性', weight: 0.3 },
    { name: '创新性', weight: 0.2 },
    { name: '完整性', weight: 0.2 }
  ];
  
  // 要求对每个维度评分
  const prompt = `
请对以下维度评分（1-10 分）：

${dimensions.map(d => `- ${d.name}: ___/10`).join('\n')}

加权总分 = ${dimensions.map(d => `${d.name}*${d.weight}`).join(' + ')}
`;
  
  // ...
}
```

---

### 3. 搜索策略

**Beam Search（推荐）**：
```javascript
// 保留 top-k 个节点，平衡探索和利用
const beamWidth = 2;  // 保留 2 个最佳路径
```

**DFS（深度优先）**：
```javascript
// 一条路走到底，适合有明确方向的任务
async dfs(task, thought, depth) {
  if (depth >= this.maxDepth) {
    return thought;
  }
  
  const children = await this.generateThoughts(task, thought);
  const bestChild = await this.getBestChild(task, children);
  
  return this.dfs(task, bestChild, depth + 1);
}
```

**BFS（广度优先）**：
```javascript
// 探索所有可能，适合需要全面探索的任务
async bfs(task, root) {
  const queue = [root];
  let bestThought = root;
  
  while (queue.length > 0) {
    const current = queue.shift();
    
    if (current.score > bestThought.score) {
      bestThought = current;
    }
    
    const children = await this.generateThoughts(task, current);
    queue.push(...children);
  }
  
  return bestThought;
}
```

---

### 4. 终止条件

**终止策略**：
```javascript
// 策略 1：找到高分解决方案
if (thought.score >= 9) {
  return thought;
}

// 策略 2：达到最大深度
if (depth >= maxDepth) {
  return bestThought;
}

// 策略 3：分数不再提升
if (bestScore - previousBestScore < 0.1) {
  console.warn('Score plateau. Stopping.');
  return bestThought;
}
```

---

## ⚠️ 常见问题与解决方案

### 问题 1：思考重复

**现象**：生成的思考很相似，缺乏多样性。

**解决方案**：
```javascript
async generateThoughts(task, parent) {
  // 添加多样性要求
  const prompt = `
生成 ${this.branchFactor} 个**完全不同**的思考方向。

要求：
1. 每个思考应该从不同角度切入
2. 避免重复或相似的想法
3. 鼓励创新和多样性

思考：`;
  
  // ...
}

// 过滤重复思考
filterDuplicateThoughts(thoughts) {
  const unique = [];
  const seen = new Set();
  
  for (const thought of thoughts) {
    const hash = this.hashThought(thought.thought);
    if (!seen.has(hash)) {
      seen.add(hash);
      unique.push(thought);
    }
  }
  
  return unique;
}
```

---

### 问题 2：评估不准确

**现象**：好方案评分低，差方案评分高。

**解决方案**：
```javascript
async evaluateThought(task, thought) {
  // 使用多个评估器
  const scores = await Promise.all([
    this.evaluateWithCriteria(task, thought, '可行性'),
    this.evaluateWithCriteria(task, thought, '有效性'),
    this.evaluateWithCriteria(task, thought, '创新性')
  ]);
  
  // 取平均
  return scores.reduce((a, b) => a + b, 0) / scores.length;
}

async evaluateWithCriteria(task, thought, criteria) {
  const prompt = `
请仅从"${criteria}"角度评估（1-10 分）：

任务：${task}
思考：${thought.thought}

评分：`;
  
  // ...
}
```

---

### 问题 3：搜索空间爆炸

**现象**：思考数量指数增长，无法处理。

**解决方案**：
```javascript
// 限制 beam width
const beamWidth = 2;  // 只保留 top-2

// 限制深度
const maxDepth = 3;   // 最多 3 层

// 剪枝：去掉低分思考
const prunedThoughts = thoughts.filter(t => t.score >= 6);
```

---

## 🔧 优化技巧

### 1. 启发式评估

```javascript
async evaluateThought(task, thought) {
  // 快速启发式评估
  const quickScore = this.heuristicEvaluate(task, thought);
  
  // 只对高分思考进行详细评估
  if (quickScore >= 7) {
    return await this.detailedEvaluate(task, thought);
  }
  
  return quickScore;
}

heuristicEvaluate(task, thought) {
  // 快速规则评估
  let score = 5;
  
  if (thought.thought.includes('AI')) score += 1;
  if (thought.thought.includes('用户')) score += 1;
  if (thought.thought.length > 20) score += 1;
  
  return score;
}
```

---

### 2. 思考链回溯

```javascript
async extractSolution(task, thought) {
  // 回溯完整路径
  const path = this.backtrack(thought);
  
  const prompt = `
任务：${task}

完整思考路径：
${path.map((t, i) => `Step ${i}: ${t.thought}`).join('\n')}

请基于这个思考路径，生成最终解决方案。

要求：
1. 整合路径中的所有要点
2. 说明为什么选择这个路径
3. 提供具体实施方案

解决方案：`;
  
  return await this.llm.generate(prompt);
}

backtrack(thought) {
  const path = [];
  let current = thought;
  
  while (current) {
    path.unshift(current);
    current = current.parent;
  }
  
  return path;
}
```

---

### 3. 并行评估

```javascript
async evaluateThoughts(task, thoughts) {
  // 并行评估所有思考
  const scores = await Promise.all(
    thoughts.map(t => this.evaluateThought(task, t))
  );
  
  return thoughts.map((t, i) => ({ ...t, score: scores[i] }));
}
```

---

## 📊 性能评估

### 评估指标

| 指标 | 描述 | 目标 |
|------|------|------|
| **解决方案质量** | 最终方案的评分 | >8/10 |
| **探索效率** | 找到好方案的思考数量 | <20 个 |
| **多样性** | 探索的不同方向数量 | >5 个 |
| **执行时间** | 从开始到完成的时间 | <2 分钟 |

---

### 优化方向

1. **提高评估准确性**：多维度评估
2. **减少搜索空间**：更好的剪枝策略
3. **加速评估**：并行评估、启发式
4. **提高多样性**：强制多样性生成

---

## 🔗 相关模式

- **ReAct**：可以在思考生成时使用工具
- **Plan-and-Solve**：可以将 ToT 用于规划阶段
- **Reflection**：可以在评估时进行反思

---

## 📚 参考资源

- **原论文**: [Tree of Thoughts: Deliberate Problem Solving](https://arxiv.org/abs/2305.10601)
- **实现参考**: [ToT GitHub](https://github.com/princeton-nlp/tree-of-thought-llm)
- **应用案例**: [Creative Writing with ToT](https://tree-of-thought.github.io/)

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02  
**下次回顾**: 2026-04-09
