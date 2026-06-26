# Self-Critique 模式 - 自我批评与修正

> **版本**: 1.0.0  
> **论文**: [Self-Critique: Enhancing Language Model Outputs](https://arxiv.org/abs/2109.05508)  
> **适用场景**: 需要高准确性、容易出错、有明确错误类型的任务

---

## 🧠 核心思想

**Self-Critique = Generate + Critique + Fix**

传统方法的问题：
- **盲目自信**：LLM 容易生成看似正确但实际错误的内容
- **缺乏验证**：生成后不检查准确性
- **幻觉问题**：编造事实、数据、引用

Self-Critique 的突破：
- **主动找错**：专门寻找输出中的错误和问题
- **结构化批评**：按错误类型系统检查
- **修正改进**：针对每个错误进行修复

**与 Reflection 的区别**：
- Reflection：全面评估（优点 + 缺点），温和改进
- Self-Critique：专注找错（缺点为主），严格批评

---

## 📊 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    Task Input                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 1: Generate Initial Output                         │
│  "生成初始答案"                                          │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: Critique (Structured Error Detection)           │
│  按错误类型系统检查：                                    │
│  - 事实错误：信息是否真实准确                            │
│  - 逻辑错误：推理是否严密                                │
│  - 计算错误：数据计算是否正确                            │
│  - 遗漏错误：是否缺少关键信息                            │
│  - 格式错误：是否符合要求格式                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: Fix Errors                                      │
│  "针对每个错误进行修正"                                  │
└─────────────────────────────────────────────────────────┘
                          ↓
                    是否还有错误？
                    /           \
                  是             否
                  ↓               ↓
            回到 Step 2        输出最终结果
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class SelfCritiqueAgent {
  constructor(options = {}) {
    this.maxIterations = options.maxIterations || 3;
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
    this.errorTypes = options.errorTypes || this.defaultErrorTypes;
  }

  async execute(task) {
    if (this.verbose) {
      console.log(`[Self-Critique] 开始任务：${task}`);
    }
    
    // Step 1: 生成初始输出
    let output = await this.generate(task);
    
    if (this.verbose) {
      console.log(`[Initial Output] ${output}`);
    }
    
    for (let iteration = 1; iteration <= this.maxIterations; iteration++) {
      if (this.verbose) {
        console.log(`\n[Iteration ${iteration}/${this.maxIterations}]`);
      }
      
      // Step 2: 结构化批评（找错）
      const critique = await this.critique(task, output);
      
      if (this.verbose) {
        console.log(`[Critique] ${JSON.stringify(critique, null, 2)}`);
      }
      
      // 如果没有错误，结束
      if (critique.errors.length === 0) {
        if (this.verbose) {
          console.log('[Complete] 未发现错误');
        }
        break;
      }
      
      // Step 3: 修正错误
      output = await this.fix(task, output, critique);
      
      if (this.verbose) {
        console.log(`[Fixed Output] ${output}`);
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

请生成初始答案。

答案：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * Critique: 结构化批评，找出错误
   */
  async critique(task, output) {
    const prompt = `
任务：${task}

待检查的输出：
${output}

请按照以下错误类型进行系统检查：

${this.formatErrorTypes()}

对于每种错误类型：
1. 仔细检查是否存在此类错误
2. 如果存在，明确指出错误位置和内容
3. 说明为什么这是错误
4. 提供正确的信息或建议

请以 JSON 格式返回检查结果：
{
  "errors": [
    {
      "type": "错误类型",
      "location": "错误位置（如：第 2 段）",
      "description": "错误描述",
      "reason": "为什么这是错误",
      "suggestion": "修正建议"
    }
  ],
  "summary": "总体评价"
}

检查结果：`;
    
    const response = await this.llm.generate(prompt);
    
    try {
      const jsonMatch = response.match(/\{[\s\S]*\}/);
      if (jsonMatch) {
        return JSON.parse(jsonMatch[0]);
      }
      throw new Error('Invalid JSON');
    } catch (error) {
      // 降级方案：返回空错误列表
      console.warn('Failed to parse critique, assuming no errors');
      return { errors: [], summary: '检查完成' };
    }
  }

  /**
   * Fix: 修正错误
   */
  async fix(task, output, critique) {
    const errorsText = critique.errors.map((e, i) => 
      `${i + 1}. [${e.type}] ${e.location}: ${e.description}\n   修正建议：${e.suggestion}`
    ).join('\n');
    
    const prompt = `
任务：${task}

原始输出：
${output}

发现的错误：
${errorsText}

请修正所有错误，生成改进后的版本。

要求：
1. 逐一修正每个错误
2. 保持原有的正确信息
3. 不要引入新错误
4. 保持格式一致

修正后的输出：`;
    
    return await this.llm.generate(prompt);
  }

  /**
   * 格式化错误类型列表
   */
  formatErrorTypes() {
    return this.errorTypes.map((et, i) => 
      `${i + 1}. **${et.name}**: ${et.description}\n   检查要点：${et.checkpoints.join('; ')}`
    ).join('\n\n');
  }

  /**
   * 默认错误类型
   */
  defaultErrorTypes = [
    {
      name: '事实错误',
      description: '信息是否真实、准确、可验证',
      checkpoints: [
        '数据、日期、人名、地名是否准确',
        '引用的研究、报告是否真实存在',
        '是否有编造的信息（幻觉）'
      ]
    },
    {
      name: '逻辑错误',
      description: '推理是否严密、自洽',
      checkpoints: [
        '前提是否成立',
        '推理过程是否有漏洞',
        '结论是否从前提推出',
        '是否有自相矛盾'
      ]
    },
    {
      name: '计算错误',
      description: '数学计算、统计是否正确',
      checkpoints: [
        '加减乘除是否正确',
        '百分比、比例计算是否正确',
        '单位换算是否正确'
      ]
    },
    {
      name: '遗漏错误',
      description: '是否缺少关键信息',
      checkpoints: [
        '是否回答了所有问题',
        '是否缺少必要的背景信息',
        '是否缺少重要的限制条件'
      ]
    },
    {
      name: '格式错误',
      description: '是否符合要求的格式',
      checkpoints: [
        '是否符合指定的输出格式',
        '结构是否清晰',
        '语言是否规范'
      ]
    }
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
const agent = new SelfCritiqueAgent({
  maxIterations: 3,
  verbose: true,
  errorTypes: [
    {
      name: '代码错误',
      description: '代码是否有 bug 或问题',
      checkpoints: [
        '语法是否正确',
        '逻辑是否正确',
        '边界条件是否处理',
        '错误处理是否完整',
        '是否有安全漏洞'
      ]
    },
    {
      name: '性能问题',
      description: '代码性能是否合理',
      checkpoints: [
        '时间复杂度是否可接受',
        '空间复杂度是否合理',
        '是否有不必要的计算',
        '是否有优化空间'
      ]
    }
  ]
});

// 执行任务：代码生成
const task = '编写一个函数，计算数组中所有数字的平均值';

const result = await agent.execute(task);
console.log(result);
```

---

### 执行轨迹示例

```
[Self-Critique] 开始任务：编写一个函数，计算数组中所有数字的平均值

[Initial Output] 
function average(arr) {
  let sum = 0;
  for (let i = 0; i < arr.length; i++) {
    sum += arr[i];
  }
  return sum / arr.length;
}

[Iteration 1/3]
[Critique] {
  "errors": [
    {
      "type": "代码错误",
      "location": "第 4 行",
      "description": "没有处理空数组的情况",
      "reason": "当 arr.length 为 0 时，会返回 NaN（除以 0）",
      "suggestion": "添加空数组检查，返回 0 或抛出错误"
    },
    {
      "type": "代码错误",
      "location": "整个函数",
      "description": "没有处理非数字元素",
      "reason": "如果数组包含非数字元素，会导致意外结果",
      "suggestion": "添加类型检查或过滤"
    }
  ],
  "summary": "基本逻辑正确，但缺少边界条件处理"
}

[Fixed Output] 
function average(arr) {
  // 处理空数组
  if (!arr || arr.length === 0) {
    return 0;
  }
  
  // 过滤非数字元素
  const numbers = arr.filter(item => typeof item === 'number' && !isNaN(item));
  
  // 如果过滤后为空，返回 0
  if (numbers.length === 0) {
    return 0;
  }
  
  let sum = 0;
  for (let i = 0; i < numbers.length; i++) {
    sum += numbers[i];
  }
  
  return sum / numbers.length;
}

[Iteration 2/3]
[Critique] {
  "errors": [],
  "summary": "代码质量良好，覆盖了边界条件"
}

[Complete] 未发现错误

最终输出：（同上）
```

---

## 🎯 关键设计要点

### 1. 错误类型设计

**好的错误类型**：
- 具体明确（不是"错误"而是"事实错误"、"逻辑错误"）
- 可检查（有明确的检查要点）
- 可修正（能提供具体的修正建议）

**示例**：
```javascript
// 通用任务错误类型
const generalErrorTypes = [
  {
    name: '事实错误',
    checkpoints: ['数据准确性', '引用真实性', '无幻觉']
  },
  {
    name: '逻辑错误',
    checkpoints: ['前提成立', '推理严密', '无矛盾']
  },
  {
    name: '完整性',
    checkpoints: ['回答问题', '背景信息', '限制条件']
  }
];

// 代码任务错误类型
const codeErrorTypes = [
  {
    name: '语法错误',
    checkpoints: ['编译通过', '无语法错误']
  },
  {
    name: '运行时错误',
    checkpoints: ['边界条件', '空值处理', '异常处理']
  },
  {
    name: '安全漏洞',
    checkpoints: ['注入攻击', 'XSS', '权限检查']
  }
];
```

---

### 2. 批评质量

**好的批评**：
```
✅ "第 3 行的计算错误：5 * 3 = 15，不是 18"
✅ "缺少空数组处理：当输入为 [] 时，函数返回 NaN"
✅ "引用不存在：'Smith et al. (2020)' 在 Google Scholar 上找不到"
```

**不好的批评**：
```
❌ "有错误"（没说哪里错）
❌ "不够好"（太模糊）
❌ "需要改进"（没说怎么改进）
```

---

### 3. 避免过度批评

**问题**：批评过于苛刻，找不存在的错误。

**解决方案**：
```javascript
async critique(task, output) {
  const prompt = `
请**客观、公正**地检查以下输出。

重要：
1. 只指出真实存在的错误
2. 不要为了找错而找错
3. 如果没有错误，返回空列表
4. 区分"可以改进"和"错误"

输出：${output}

检查结果（JSON）：`;
  
  return await this.llm.generate(prompt);
}
```

---

### 4. 错误优先级

**给错误分级**：
```javascript
// 在 Critique 中添加优先级
{
  "errors": [
    {
      "type": "代码错误",
      "severity": "critical",  // critical | major | minor
      "description": "空指针异常风险",
      // ...
    }
  ]
}

// 优先修复严重错误
async fix(task, output, critique) {
  const criticalErrors = critique.errors.filter(e => e.severity === 'critical');
  
  if (criticalErrors.length === 0) {
    return output; // 没有严重错误，不需要修复
  }
  
  // 只修复严重错误
  // ...
}
```

---

## ⚠️ 常见问题与解决方案

### 问题 1：批评找不到错误

**现象**：即使有明显错误，批评也返回空列表。

**解决方案**：
```javascript
async critique(task, output) {
  // 提供错误示例，引导找错
  const examples = `
示例 1:
输出："珠穆朗玛峰高 8000 米"
批评：
{
  "errors": [{
    "type": "事实错误",
    "description": "高度不准确",
    "reason": "珠穆朗玛峰实际高度是 8848.86 米",
    "suggestion": "修正为 8848.86 米"
  }]
}

示例 2:
输出："2 + 2 = 5"
批评：
{
  "errors": [{
    "type": "计算错误",
    "description": "加法错误",
    "reason": "2 + 2 = 4",
    "suggestion": "修正为 4"
  }]
}
`;

  const prompt = `${examples}\n当前任务：${task}...`;
  return await this.llm.generate(prompt);
}
```

---

### 问题 2：修复引入新错误

**现象**：修正一个错误后，引入了新错误。

**解决方案**：
```javascript
async fix(task, output, critique) {
  const prompt = `
修正以下错误：
${critique.errors.map(e => `- ${e.description}: ${e.suggestion}`).join('\n')}

重要：
1. 只修正指出的错误
2. 不要修改正确的部分
3. 修正后检查是否引入新错误
4. 保持原有结构和风格

原始输出：${output}

修正后的输出：`;
  
  return await this.llm.generate(prompt);
}

// 添加验证步骤
async execute(task) {
  // ...
  output = await this.fix(task, output, critique);
  
  // 验证修复后的输出
  const newCritique = await this.critique(task, output);
  if (newCritique.errors.length > critique.errors.length) {
    console.warn('Fix introduced new errors. Reverting.');
    // 可以尝试重新修复或使用原始输出
  }
  // ...
}
```

---

### 问题 3：无限循环

**现象**：反复找错、修复，无法结束。

**解决方案**：
```javascript
async execute(task) {
  let output = await this.generate(task);
  let previousErrors = [];
  
  for (let iteration = 1; iteration <= this.maxIterations; iteration++) {
    const critique = await this.critique(task, output);
    
    // 检查错误是否重复
    const currentErrorHash = this.hashErrors(critique.errors);
    if (currentErrorHash === this.hashErrors(previousErrors)) {
      console.warn('Same errors detected. Stopping.');
      break;
    }
    
    if (critique.errors.length === 0) {
      break;
    }
    
    output = await this.fix(task, output, critique);
    previousErrors = critique.errors;
  }
  
  return output;
}

hashErrors(errors) {
  return errors.map(e => `${e.type}:${e.description}`).sort().join('|');
}
```

---

## 🔧 优化技巧

### 1. 专家角色批评

```javascript
async critique(task, output) {
  const role = this.selectCriticRole(task);
  
  const prompt = `
你是一位${role}，以严格、挑剔著称。

你的任务是找出输出中的**所有**错误和问题。

不要留情面，不要客气，直接指出问题。

输出：${output}

批评：`;
  
  return await this.llm.generate(prompt);
}

selectCriticRole(task) {
  if (task.includes('代码')) return '资深代码审查专家';
  if (task.includes('文章')) return '挑剔的编辑';
  if (task.includes('数据')) return '统计学教授';
  return '严格的领域专家';
}
```

---

### 2. 多轮批评

```javascript
async critique(task, output) {
  // 第 1 轮：快速扫描
  const quickCritique = await this.quickScan(task, output);
  
  // 第 2 轮：深度检查
  const deepCritique = await this.deepCheck(task, output, quickCritique);
  
  // 合并结果
  return {
    errors: [...quickCritique.errors, ...deepCritique.errors],
    summary: deepCritique.summary
  };
}

async quickScan(task, output) {
  // 快速扫描明显错误
  const prompt = `快速扫描以下输出的明显错误（10 秒内完成）：...`;
  return await this.llm.generate(prompt);
}

async deepCheck(task, output, quickCritique) {
  // 深度检查潜在问题
  const prompt = `深度检查以下输出的潜在问题，特别是 ${quickCritique.summary}：...`;
  return await this.llm.generate(prompt);
}
```

---

### 3. 交叉验证

```javascript
async critique(task, output) {
  // 使用多个 LLM 实例交叉验证
  const critiques = await Promise.all([
    this.llm1.generate(this.buildCritiquePrompt(task, output)),
    this.llm2.generate(this.buildCritiquePrompt(task, output)),
    this.llm3.generate(this.buildCritiquePrompt(task, output))
  ]);
  
  // 合并多个批评，只保留一致的发现
  const mergedErrors = this.mergeCritiques(critiques);
  
  return {
    errors: mergedErrors,
    summary: '交叉验证完成'
  };
}
```

---

## 📊 性能评估

### 评估指标

| 指标 | 描述 | 目标 |
|------|------|------|
| **错误检出率** | 检出的错误占真实错误的比例 | >90% |
| **误报率** | 错误批评的比例 | <10% |
| **修复成功率** | 修复后错误消除的比例 | >95% |
| **迭代次数** | 达到无错误状态的迭代次数 | <3 次 |

---

### 优化方向

1. **提高检出率**：更好的错误类型定义
2. **降低误报率**：更客观的批评标准
3. **提高修复率**：更有针对性的修复
4. **减少迭代**：一次性修复多个错误

---

## 🔗 相关模式

- **Reflection**：更温和的全面评估
- **ReAct**：可以结合工具调用进行验证
- **Plan-and-Solve**：先规划再批评执行

---

## 📚 参考资源

- **原论文**: [Self-Critique: Enhancing Language Model Outputs](https://arxiv.org/abs/2109.05508)
- **应用案例**: [Code Self-Critique](https://self-critique.github.io/)
- **相关研究**: [Teaching Language Models to Self-Critique](https://arxiv.org/abs/2206.05266)

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02  
**下次回顾**: 2026-04-09
