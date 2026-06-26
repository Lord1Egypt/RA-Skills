# ReAct 模式 - Reasoning + Acting

> **版本**: 1.0.0  
> **论文**: [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)  
> **适用场景**: 需要工具调用、多步推理、环境交互的任务

---

## 🧠 核心思想

**ReAct = Reasoning + Acting**

传统方法的问题：
- **纯推理**：能思考但不能行动（无法调用工具）
- **纯行动**：能行动但不思考（盲目执行）

ReAct 的突破：
- **交替进行**：思考 → 行动 → 观察 → 思考 → ...
- **协同增强**：推理指导行动，行动结果反馈推理

---

## 📊 工作流程

```
┌─────────────────────────────────────────────────────────┐
│                    Task Input                            │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 1: Thought (思考)                                  │
│  "我需要做什么？当前有什么信息？下一步应该做什么？"       │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 2: Action (行动)                                   │
│  "调用工具 X，参数 Y"                                    │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Step 3: Observation (观察)                              │
│  "工具返回结果 Z"                                        │
└─────────────────────────────────────────────────────────┘
                          ↓
                    是否完成？
                    /       \
                  否         是
                  ↓           ↓
            回到 Step 1    输出最终答案
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class ReActAgent {
  constructor(tools, maxSteps = 10) {
    this.tools = tools;
    this.maxSteps = maxSteps;
  }

  async execute(task) {
    const history = [];
    
    for (let step = 0; step < this.maxSteps; step++) {
      // Step 1: Thought - 思考下一步
      const thought = await this.reason(task, history);
      console.log(`[Thought ${step + 1}] ${thought}`);
      
      // Step 2: Action - 决定行动
      const action = await this.decideAction(thought, history);
      console.log(`[Action ${step + 1}] ${action.name}(${JSON.stringify(action.args)})`);
      
      // Step 3: Observation - 执行并观察结果
      const observation = await this.observe(action);
      console.log(`[Observation ${step + 1}] ${observation}`);
      
      // 记录历史
      history.push({ thought, action, observation });
      
      // 判断是否完成
      if (this.isComplete(thought, observation)) {
        const answer = await this.finalize(task, history);
        console.log(`[Answer] ${answer}`);
        return answer;
      }
    }
    
    throw new Error(`Max steps (${this.maxSteps}) reached without completion`);
  }

  async reason(task, history) {
    // 调用 LLM 进行推理
    const context = this.buildContext(task, history);
    const prompt = `
当前任务：${task}
历史对话：${JSON.stringify(history, null, 2)}

请思考：
1. 当前已知什么信息？
2. 还需要什么信息？
3. 下一步应该做什么？

思考：`;
    
    const response = await this.callLLM(prompt);
    return response.trim();
  }

  async decideAction(thought, history) {
    // 根据思考决定行动
    const prompt = `
基于以下思考，决定采取什么行动：
${thought}

可用工具：
${this.listTools()}

请以 JSON 格式返回行动：
{
  "name": "工具名称",
  "args": { "参数名": "参数值" }
}

行动：`;
    
    const response = await this.callLLM(prompt);
    return JSON.parse(response);
  }

  async observe(action) {
    // 执行工具并返回结果
    const tool = this.tools[action.name];
    if (!tool) {
      throw new Error(`Unknown tool: ${action.name}`);
    }
    return await tool.execute(action.args);
  }

  isComplete(thought, observation) {
    // 判断是否完成任务
    return thought.toLowerCase().includes('finish') || 
           thought.toLowerCase().includes('answer is');
  }

  async finalize(task, history) {
    // 生成最终答案
    const prompt = `
任务：${task}
完整历史：${JSON.stringify(history, null, 2)}

请给出最终答案：`;
    
    return await this.callLLM(prompt);
  }

  buildContext(task, history) {
    // 构建上下文
    return { task, history };
  }

  listTools() {
    return Object.keys(this.tools).map(name => 
      `- ${name}: ${this.tools[name].description}`
    ).join('\n');
  }

  async callLLM(prompt) {
    // 调用大语言模型（这里用伪代码）
    // 实际实现中调用 OpenAI/Claude/Qwen 等 API
    const response = await llm.generate(prompt);
    return response;
  }
}
```

---

### 使用示例

```javascript
// 定义工具
const tools = {
  search: {
    description: '搜索网络信息',
    execute: async ({ query }) => {
      const result = await webSearch(query);
      return result.snippets.join('\n');
    }
  },
  
  calculate: {
    description: '执行数学计算',
    execute: async ({ expression }) => {
      return eval(expression).toString();
    }
  },
  
  readFile: {
    description: '读取文件内容',
    execute: async ({ path }) => {
      return await fs.readFile(path, 'utf-8');
    }
  }
};

// 创建 Agent
const agent = new ReActAgent(tools, { maxSteps: 10 });

// 执行任务
const task = '北京今天的气温是多少？比上海高还是低？';
const answer = await agent.execute(task);

console.log(answer);
```

---

### 执行轨迹示例

```
Task: 北京今天的气温是多少？比上海高还是低？

[Thought 1] 我需要查询北京和上海的今天气温，然后比较。
           首先查询北京的气温。

[Action 1] search({"query": "北京 今天 气温"})

[Observation 1] 北京今天晴，最高气温 25°C，最低气温 15°C

[Thought 2] 我已经知道北京的气温了。现在需要查询上海的气温。

[Action 2] search({"query": "上海 今天 气温"})

[Observation 2] 上海今天多云，最高气温 22°C，最低气温 18°C

[Thought 3] 我有了两个城市的气温数据。
           北京最高 25°C，上海最高 22°C。
           北京比上海高 3°C。
           可以给出最终答案了。

[Answer] 北京今天气温 15-25°C，上海今天气温 18-22°C。
         北京的最高气温比上海高 3°C。
```

---

## 🎯 关键设计要点

### 1. 思考格式（Thought Format）

**好的思考**：
```
✅ "我需要先查询 X，因为 Y 信息是必需的"
✅ "已经有 A 和 B 信息，下一步需要 C"
✅ "根据上一步结果，我应该..."
```

**不好的思考**：
```
❌ "我不知道"（太模糊）
❌ "继续"（没有具体计划）
❌ "完成"（但没有给出答案）
```

---

### 2. 行动设计（Action Design）

**行动类型**：
- **工具调用**：search、calculate、readFile 等
- **信息提取**：从历史中提取已知信息
- **完成声明**：表示任务完成，准备输出答案

**行动格式**：
```json
{
  "name": "工具名称",
  "args": {
    "参数 1": "值 1",
    "参数 2": "值 2"
  }
}
```

---

### 3. 观察处理（Observation Handling）

**观察内容**：
- 工具执行结果
- 错误信息
- 状态更新

**观察处理**：
```javascript
async observe(action) {
  try {
    const result = await this.tools[action.name].execute(action.args);
    return { success: true, data: result };
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

---

### 4. 完成判断（Completion Detection）

**判断信号**：
- 思考中包含"finish"、"answer is"等关键词
- 已收集所有必需信息
- 达到最大步数

**优雅完成**：
```javascript
isComplete(thought, observation) {
  const finishKeywords = ['finish', 'answer is', '最终答案是', '完成任务'];
  return finishKeywords.some(keyword => 
    thought.toLowerCase().includes(keyword)
  );
}
```

---

## ⚠️ 常见问题与解决方案

### 问题 1：无限循环

**现象**：Agent 反复执行相同行动。

**原因**：
- 没有正确更新历史
- 完成判断条件太严格

**解决方案**：
```javascript
// 添加步数限制
for (let step = 0; step < this.maxSteps; step++) {
  // ...
}

// 检测重复行动
const lastActions = history.slice(-3).map(h => h.action.name);
if (new Set(lastActions).size === 1) {
  throw new Error('Detected infinite loop');
}
```

---

### 问题 2：工具调用失败

**现象**：工具返回错误或无效结果。

**解决方案**：
```javascript
async observe(action) {
  try {
    return await this.tools[action.name].execute(action.args);
  } catch (error) {
    // 返回错误信息，让 Agent 可以重试或调整
    return `Error: ${error.message}. Please try again with different parameters.`;
  }
}
```

---

### 问题 3：思考质量差

**现象**：思考模糊、没有指导行动。

**解决方案**：
- 改进 Prompt，要求具体思考
- 提供思考示例（Few-shot）
- 添加思考模板

```javascript
async reason(task, history) {
  const examples = `
示例 1:
思考：我需要查询 X 的信息，因为这是完成任务的第一步。
行动：search({"query": "X"})

示例 2:
思考：已经有 X 信息，现在需要 Y 信息来比较。
行动：search({"query": "Y"})
`;

  const prompt = `${examples}\n当前任务：${task}...`;
  // ...
}
```

---

## 🔧 优化技巧

### 1. Few-shot Learning

在 Prompt 中提供示例：

```javascript
const examples = `
任务：珠穆朗玛峰有多高？比 K2 高多少？

思考：我需要查询珠穆朗玛峰和 K2 的高度。首先查询珠穆朗玛峰。
行动：search({"query": "珠穆朗玛峰 高度"})
观察：8848.86 米

思考：现在查询 K2 的高度。
行动：search({"query": "K2 高度"})
观察：8611 米

思考：两座山峰高度都知道了。珠峰 8848.86 米，K2 8611 米。
       珠峰比 K2 高 237.86 米。可以给出答案了。
行动：finish

答案：珠穆朗玛峰高 8848.86 米，K2 高 8611 米，珠峰比 K2 高 237.86 米。
`;
```

---

### 2. 工具描述优化

清晰的工具描述帮助 Agent 正确选择：

```javascript
const tools = {
  search: {
    description: '搜索网络信息。适用于查询事实、新闻、数据等。参数：query（搜索关键词）',
    execute: ...
  },
  calculate: {
    description: '执行数学计算。适用于加减乘除、幂运算等。参数：expression（数学表达式）',
    execute: ...
  }
};
```

---

### 3. 历史压缩

当历史过长时，压缩旧信息：

```javascript
buildContext(task, history) {
  if (history.length > 5) {
    // 压缩早期历史
    const earlyHistory = history.slice(0, -3);
    const recentHistory = history.slice(-3);
    
    const summary = `早期步骤摘要：共${earlyHistory.length}步，查询了${earlyHistory.length}次工具`;
    
    return {
      task,
      historySummary: summary,
      recentHistory
    };
  }
  return { task, history };
}
```

---

## 📊 性能评估

### 评估指标

| 指标 | 描述 | 目标 |
|------|------|------|
| **任务完成率** | 成功完成的任务比例 | >90% |
| **平均步数** | 完成任务的平均步数 | <5 步 |
| **工具调用准确率** | 正确选择工具的比例 | >95% |
| **平均响应时间** | 从输入到输出的时间 | <10 秒 |

---

### 优化方向

1. **减少步数**：改进推理，减少不必要的工具调用
2. **提高准确率**：更好的工具描述和示例
3. **加快速度**：并行工具调用（当独立时）
4. **降低成本**：减少 LLM 调用次数

---

## 🔗 相关模式

- **Reflection**：在 ReAct 基础上添加反思
- **Self-Critique**：在 ReAct 基础上添加自我批评
- **Plan-and-Solve**：先规划再 ReAct 执行

---

## 📚 参考资源

- **原论文**: [ReAct: Synergizing Reasoning and Acting](https://arxiv.org/abs/2210.03629)
- **实现参考**: [LangChain ReAct Agent](https://python.langchain.com/docs/modules/agents/agent_types/react)
- **示例应用**: [ReAct for Question Answering](https://react-lm.github.io/)

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02  
**下次回顾**: 2026-04-09
