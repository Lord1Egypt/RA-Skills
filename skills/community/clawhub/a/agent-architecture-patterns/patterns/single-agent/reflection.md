# Reflection 模式 - 自我反思与改进

> **版本**: 1.0.0  
> **论文**: [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.11366)  
> **适用场景**: 需要高质量输出、可以自我评估、有时间迭代的任务

---

## 🧠 核心思想

**Reflection = Generate + Reflect + Revise**

传统方法的问题：
- **一次性生成**：输出质量依赖单次生成
- **无法改进**：生成后无法自我修正
- **缺乏反思**：不知道输出的问题在哪里

Reflection 的突破：
- **迭代改进**：生成 → 反思 → 修改 → 反思 → ...
- **自我反馈**：自己评估自己的输出
- **质量提升**：每次迭代都更接近最优

---

## 📊 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    Task Input                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Iteration 1:                                            │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Generate: 生成初始输出                            │  │
│  └───────────────────────────────────────────────────┘  │
│                          ↓                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Reflect: 评估输出，找出问题                       │  │
│  └───────────────────────────────────────────────────┘  │
│                          ↓                               │
│  ┌───────────────────────────────────────────────────┐  │
│  │  Revise: 根据反馈修改输出                          │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
                          ↓
                    是否满足标准？
                    /           \
                  否             是
                  ↓               ↓
            回到 Iteration 2    输出最终结果
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class ReflectionAgent {
  constructor(options = {}) {
    this.maxIterations = options.maxIterations || 5;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
    this.criteria = options.criteria || this.defaultCriteria;
  }

  async execute(task) {
    if (this.verbose) {
      console.log(`[Reflection] 开始任务：${task}`);
    }
    
    let output = await this.generate(task);
    
    if (this.verbose) {
      console.log(`[Initial] ${output}`);
    }
    
    for (let iteration = 1; iteration <= this.maxIterations; iteration++) {
      if (this.verbose) {
        console.log(`\n[Iteration ${iteration}/${this.maxIterations}]`);
      }
      
      // Reflect: 评估当前输出
      const feedback = await this.reflect(task, output);
      
      if (this.verbose) {
        console.log(`[Feedback] ${feedback}`);
      }
      
      // 检查是否满足标准
      if (this.isSatisfactory(feedback)) {
        if (this.verbose) {
          console.log('[Complete] 输出质量满足要求');
        }
        break;
      }
      
      // Revise: 根据反馈修改
      output = await this.revise(task, output, feedback);
      
      if (this.verbose) {
        console.log(`[Revised] ${output}`);
      }
    }
    
    return output;
  }

  /**
   * Generate: 生成初始输出
   */
  async generate(task) {
    const prompt = `
任务：${task}

请生成初始输出。

初始输出：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * Reflect: 评估输出，提供反馈
   */
  async reflect(task, output) {
    const prompt = `
任务：${task}

当前输出：
${output}

请评估这个输出，考虑以下标准：
${this.formatCriteria()}

反馈要求：
1. 指出具体问题（至少 3 个）
2. 说明为什么是问题
3. 提供改进建议

反馈：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * Revise: 根据反馈修改输出
   */
  async revise(task, output, feedback) {
    const prompt = `
任务：${task}

当前输出：
${output}

反馈：
${feedback}

请根据反馈修改输出，改进所有指出的问题。

修改后的输出：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 判断输出是否满足要求
   */
  isSatisfactory(feedback) {
    // 检查反馈中是否有严重问题
    const criticalKeywords = ['严重问题', '重大错误', '完全不符合', '无法接受'];
    const hasCriticalIssues = criticalKeywords.some(keyword => 
      feedback.includes(keyword)
    );
    
    // 如果没有严重问题，认为满足要求
    return !hasCriticalIssues;
  }

  /**
   * 格式化评估标准
   */
  formatCriteria() {
    return this.criteria.map((c, i) => `${i + 1}. ${c}`).join('\n');
  }

  /**
   * 默认评估标准
   */
  defaultCriteria = [
    '准确性：信息是否正确、无误',
    '完整性：是否覆盖所有要点',
    '清晰性：表达是否清晰易懂',
    '逻辑性：推理是否严密、自洽',
    '相关性：是否紧扣任务要求'
  ];

  /**
   * 默认 LLM
   */
  defaultLLM = {
    generate: async (prompt) => {
      console.warn('[Warning] Using default LLM.');
      return 'Generated output.';
    }
  };
}
```

---

### 使用示例

```javascript
// 创建 Agent
const agent = new ReflectionAgent({
  maxIterations: 5,
  verbose: true,
  criteria: [
    '代码正确性：是否能正确运行',
    '代码质量：是否遵循最佳实践',
    '性能：是否有性能问题',
    '可读性：是否易于理解',
    '安全性：是否有安全漏洞'
  ]
});

// 执行任务：代码审查
const task = '审查以下代码并提供改进建议：\n\n' + `
function calculateTotal(items) {
  let total = 0;
  for (let i = 0; i < items.length; i++) {
    total += items[i].price * items[i].quantity;
  }
  return total;
}
`;

const result = await agent.execute(task);
console.log(result);
```

---

### 执行轨迹示例

```
[Reflection] 开始任务：审查以下代码并提供改进建议

[Initial] 
代码审查结果：
1. 代码功能正确
2. 变量命名清晰
3. 逻辑简单明了

[Iteration 1/5]
[Feedback] 
评估结果：
问题 1：反馈过于简略，没有具体说明
问题 2：没有指出潜在问题（如边界条件、错误处理）
问题 3：没有提供改进建议
问题 4：没有考虑性能优化

[Revised] 
代码审查结果：

优点：
1. 功能正确，能正确计算总价
2. 变量命名清晰（total, items, price, quantity）
3. 逻辑简单，易于理解

需要改进的地方：
1. 缺少边界条件处理（items 为空数组时）
2. 缺少错误处理（price 或 quantity 为非数字时）
3. 可以使用 reduce 方法使代码更简洁
4. 缺少类型检查

改进建议：
function calculateTotal(items) {
  if (!Array.isArray(items) || items.length === 0) {
    return 0;
  }
  
  return items.reduce((total, item) => {
    const price = Number(item.price) || 0;
    const quantity = Number(item.quantity) || 0;
    return total + price * quantity;
  }, 0);
}

[Iteration 2/5]
[Feedback] 
评估结果：
这次反馈质量很好，覆盖了：
- 优点识别
- 具体问题
- 改进建议
- 代码示例

满足要求，可以结束。

[Complete] 输出质量满足要求

最终输出：（同上）
```

---

## 🎯 关键设计要点

### 1. 评估标准设计

**好的标准**：
- 具体可衡量（不是"好"而是"准确率>95%"）
- 覆盖关键维度（准确性、完整性、清晰性等）
- 与任务相关（代码审查 vs 文章写作的标准不同）

**示例**：
```javascript
// 代码审查标准
const codeReviewCriteria = [
  '正确性：代码是否能正确运行，无 bug',
  '性能：时间复杂度、空间复杂度是否合理',
  '可读性：命名、注释、结构是否清晰',
  '可维护性：是否易于修改和扩展',
  '安全性：是否有安全漏洞（注入、XSS 等）',
  '测试：是否有充分的测试覆盖'
];

// 文章写作标准
const writingCriteria = [
  '准确性：信息是否正确、来源可靠',
  '逻辑性：论点是否清晰、论证是否严密',
  '流畅性：语言是否通顺、易读',
  '吸引力：开头是否吸引人、结尾是否有力',
  '完整性：是否覆盖所有要点'
];
```

---

### 2. 反馈质量

**好的反馈**：
```
✅ "第 3 段缺少过渡句，导致逻辑跳跃。建议添加：'然而，这个观点存在争议...'。"
✅ "函数没有处理空数组的情况，会返回 undefined。应该返回 0。"
✅ "这个论点缺乏数据支持。建议引用 XX 研究报告的数据。"
```

**不好的反馈**：
```
❌ "写得不好"（太模糊）
❌ "有问题"（没说什么问题）
❌ "需要改进"（没说怎么改进）
```

---

### 3. 迭代终止条件

**终止策略**：
```javascript
isSatisfactory(feedback) {
  // 策略 1：没有严重问题
  const noCriticalIssues = !feedback.includes('严重问题');
  
  // 策略 2：反馈质量下降（改进空间变小）
  const issuesCount = (feedback.match(/问题/g) || []).length;
  const lowIssues = issuesCount < 2;
  
  // 策略 3：达到最大迭代次数
  const maxIterationsReached = this.currentIteration >= this.maxIterations;
  
  return noCriticalIssues || lowIssues || maxIterationsReached;
}
```

---

### 4. 避免无限循环

**保护机制**：
```javascript
async execute(task) {
  let output = await this.generate(task);
  let previousOutput = '';
  let noImprovementCount = 0;
  
  for (let iteration = 1; iteration <= this.maxIterations; iteration++) {
    const feedback = await this.reflect(task, output);
    
    if (this.isSatisfactory(feedback)) {
      break;
    }
    
    output = await this.revise(task, output, feedback);
    
    // 检测是否没有改进
    if (output === previousOutput) {
      noImprovementCount++;
      if (noImprovementCount >= 2) {
        console.warn('No improvement detected. Stopping.');
        break;
      }
    } else {
      noImprovementCount = 0;
    }
    
    previousOutput = output;
  }
  
  return output;
}
```

---

## ⚠️ 常见问题与解决方案

### 问题 1：反馈质量差

**现象**：反馈模糊、没有具体建议。

**解决方案**：
```javascript
async reflect(task, output) {
  // 提供反馈模板
  const template = `
反馈格式：
【优点】
1. ...
2. ...

【问题】
1. 问题描述：...
   原因：...
   改进建议：...

2. 问题描述：...
   原因：...
   改进建议：...

【总体评价】
...
`;

  const prompt = `...（任务描述）\n\n${template}`;
  return await this.llm.generate(prompt);
}
```

---

### 问题 2：迭代不收敛

**现象**：反复修改但质量不提升。

**解决方案**：
```javascript
async revise(task, output, feedback) {
  // 强调针对性修改
  const prompt = `
根据以下反馈修改输出：

反馈：
${feedback}

要求：
1. 针对性地解决每个问题
2. 保持原有优点
3. 不要引入新问题
4. 如果某些反馈不合理，说明原因

修改后的输出：`;
  
  return await this.llm.generate(prompt);
}
```

---

### 问题 3：迭代次数过多

**现象**：每次都找到新问题，无法结束。

**解决方案**：
```javascript
// 设置更严格的终止条件
isSatisfactory(feedback) {
  const issuesCount = (feedback.match(/问题/g) || []).length;
  
  // 问题少于 2 个就认为满足要求
  if (issuesCount < 2) {
    return true;
  }
  
  // 检查是否有严重问题
  const hasCritical = feedback.includes('严重') || feedback.includes('重大');
  return !hasCritical;
}

// 限制最大迭代次数
const agent = new ReflectionAgent({ maxIterations: 3 }); // 减少迭代次数
```

---

## 🔧 优化技巧

### 1. Few-shot 反馈示例

提供高质量反馈示例：

```javascript
async reflect(task, output) {
  const examples = `
示例 1:
输出："这个产品很好用"
反馈：
【问题】
1. 问题描述：评价过于笼统
   原因：没有说明具体哪里好
   改进建议：添加具体优点，如"界面简洁、响应快速、功能齐全"

示例 2:
输出：function add(a,b){return a+b}
反馈：
【问题】
1. 问题描述：代码格式不规范
   原因：缺少空格，不符合编码规范
   改进建议：function add(a, b) { return a + b }
`;

  const prompt = `${examples}\n当前任务：${task}...`;
  return await this.llm.generate(prompt);
}
```

---

### 2. 多维度评估

```javascript
async reflect(task, output) {
  const dimensions = [
    { name: '准确性', score: null, comments: [] },
    { name: '完整性', score: null, comments: [] },
    { name: '清晰性', score: null, comments: [] },
    { name: '逻辑性', score: null, comments: [] }
  ];
  
  // 要求对每个维度评分
  const prompt = `
请对以下维度进行评估（1-10 分）：

1. 准确性：___/10
   评价：...

2. 完整性：___/10
   评价：...

3. 清晰性：___/10
   评价：...

4. 逻辑性：___/10
   评价：...

平均分 < 7 分需要改进。`;
  
  return await this.llm.generate(prompt);
}
```

---

### 3. 专家角色反馈

```javascript
async reflect(task, output) {
  // 根据任务类型选择专家角色
  const role = this.selectExpertRole(task);
  
  const prompt = `
你是一位${role}专家。

任务：${task}
输出：${output}

请以${role}的专业视角评估这个输出，指出专业性问题。

反馈：`;
  
  return await this.llm.generate(prompt);
}

selectExpertRole(task) {
  if (task.includes('代码')) return '资深软件工程师';
  if (task.includes('文章')) return '专业编辑';
  if (task.includes('设计')) return '资深设计师';
  return '领域专家';
}
```

---

## 📊 性能评估

### 评估指标

| 指标 | 描述 | 目标 |
|------|------|------|
| **质量提升率** | 迭代后质量提升幅度 | >30% |
| **收敛迭代次数** | 达到满意质量的迭代次数 | <3 次 |
| **反馈准确率** | 反馈指出的问题是否真实存在 | >90% |
| **用户满意度** | 用户对最终输出的评分 | >8/10 |

---

### 优化方向

1. **提高反馈质量**：更好的评估标准、示例
2. **减少迭代次数**：更准确的初始生成
3. **加速收敛**：更有针对性的修改
4. **降低成本**：减少 LLM 调用次数

---

## 🔗 相关模式

- **ReAct**：可以结合 ReAct 进行工具调用
- **Self-Critique**：更严格的自我批评
- **Plan-and-Solve**：先规划再反思执行

---

## 📚 参考资源

- **原论文**: [Self-Refine: Iterative Refinement with Self-Feedback](https://arxiv.org/abs/2303.11366)
- **实现参考**: [LangChain Self-Refine](https://python.langchain.com/docs/modules/chains/popular/self_refine)
- **应用案例**: [Code Refinement with Self-Feedback](https://self-refine.github.io/)

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02  
**下次回顾**: 2026-04-09
