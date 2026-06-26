# 流水线模式 (Pipeline) - 多 Agent 协作

> **版本**: 1.0.0  
> **适用场景**: 多阶段处理、阶段间有依赖、需要专业化的场景  
> **复杂度**: ⭐⭐⭐（中高）

---

## 🧠 核心思想

**流水线模式 = 顺序处理 + 专业化分工**

- **顺序处理**：Input → Stage 1 → Stage 2 → ... → Output
- **专业化**：每个 Agent 专注于一个阶段
- **依赖传递**：前一阶段的输出是后一阶段的输入

**类比**：
- 工厂流水线：原材料 → 加工 → 组装 → 质检 → 成品
- 内容创作：选题 → 大纲 → 写作 → 编辑 → 发布

---

## 📊 架构设计

```
┌─────────────────────────────────────────────────────────┐
│                      Input                               │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Stage 1: Agent A (专业：X)                              │
│  Input: 原始数据                                         │
│  Output: 处理结果 A                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Stage 2: Agent B (专业：Y)                              │
│  Input: 处理结果 A                                       │
│  Output: 处理结果 B                                      │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│  Stage 3: Agent C (专业：Z)                              │
│  Input: 处理结果 B                                       │
│  Output: 最终结果                                        │
└─────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────┐
│                      Output                              │
└─────────────────────────────────────────────────────────┘
```

---

## 💻 实现示例

### 基础实现（JavaScript）

```javascript
class PipelineAgent {
  constructor(stages, options = {}) {
    this.stages = stages; // [{agent, name, description}]
    this.verbose = options.verbose || false;
    this.llm = options.llm || this.defaultLLM;
  }

  async process(input) {
    if (this.verbose) {
      console.log(`[Pipeline] 开始处理`);
      console.log(`[Pipeline] 输入：${input.substring(0, 100)}...`);
      console.log(`[Pipeline] 阶段数：${this.stages.length}`);
    }
    
    let currentData = input;
    const stageResults = [];
    
    for (let i = 0; i < this.stages.length; i++) {
      const stage = this.stages[i];
      
      if (this.verbose) {
        console.log(`\n[Stage ${i + 1}/${this.stages.length}] ${stage.name}`);
      }
      
      // 执行当前阶段
      const result = await stage.agent.process(currentData);
      
      if (this.verbose) {
        console.log(`[Stage ${i + 1}] 完成`);
        console.log(`  输出：${result.substring(0, 100)}...`);
      }
      
      // 记录结果
      stageResults.push({
        stage: stage.name,
        input: currentData,
        output: result
      });
      
      // 传递给下一阶段
      currentData = result;
    }
    
    if (this.verbose) {
      console.log(`\n[Pipeline] 处理完成`);
    }
    
    return {
      finalOutput: currentData,
      stageResults
    };
  }
}

/**
 * 流水线阶段 Agent
 */
class PipelineStageAgent {
  constructor(id, specialty, instructions) {
    this.id = id;
    this.specialty = specialty;
    this.instructions = instructions;
    this.llm = null;
  }

  async process(input) {
    const prompt = `
阶段：${this.specialty}
指令：${this.instructions}

输入：
${input}

请执行本阶段处理。

输出：`;
    
    return await this.llm.generate(prompt);
  }
}
```

---

### 使用示例 1：内容创作流水线

```javascript
// 创建各阶段 Agent
const outlineAgent = new PipelineStageAgent(
  'outline',
  '大纲设计',
  '根据主题创建详细大纲，包括主要章节和要点'
);

const draftAgent = new PipelineStageAgent(
  'draft',
  '初稿写作',
  '根据大纲撰写完整初稿，内容详实'
);

const editAgent = new PipelineStageAgent(
  'edit',
  '编辑润色',
  '修改语法错误、优化表达、提升可读性'
);

const reviewAgent = new PipelineStageAgent(
  'review',
  '质量审查',
  '检查事实准确性、逻辑一致性、整体质量'
);

// 创建流水线
const contentPipeline = new PipelineAgent([
  { agent: outlineAgent, name: '大纲设计', description: '创建大纲' },
  { agent: draftAgent, name: '初稿写作', description: '撰写初稿' },
  { agent: editAgent, name: '编辑润色', description: '编辑修改' },
  { agent: reviewAgent, name: '质量审查', description: '最终审查' }
], { verbose: true });

// 执行
const topic = '人工智能的未来发展趋势';
const result = await contentPipeline.process(topic);
console.log(result.finalOutput);
```

---

### 使用示例 2：代码开发流水线

```javascript
// 代码开发流水线
const designAgent = new PipelineStageAgent(
  'design',
  '架构设计',
  '设计系统架构、接口定义、数据模型'
);

const codeAgent = new PipelineStageAgent(
  'code',
  '代码实现',
  '根据设计编写高质量代码'
);

const testAgent = new PipelineStageAgent(
  'test',
  '测试编写',
  '编写单元测试、集成测试'
);

const reviewCodeAgent = new PipelineStageAgent(
  'code-review',
  '代码审查',
  '审查代码质量、安全性、性能'
);

const codePipeline = new PipelineAgent([
  { agent: designAgent, name: '架构设计' },
  { agent: codeAgent, name: '代码实现' },
  { agent: testAgent, name: '测试编写' },
  { agent: reviewCodeAgent, name: '代码审查' }
], { verbose: true });

// 执行
const requirement = '开发一个用户认证系统';
const result = await codePipeline.process(requirement);
```

---

## 🎯 关键设计要点

### 1. 阶段设计

**好的阶段**：
- 职责单一（每个阶段只做一件事）
- 接口清晰（输入输出明确）
- 专业化（发挥 Agent 专长）

**示例**：
```javascript
const stages = [
  { agent: researchAgent, name: '信息收集' },
  { agent: analyzeAgent, name: '数据分析' },
  { agent: writeAgent, name: '报告撰写' },
  { agent: editAgent, name: '编辑校对' }
];
```

---

### 2. 错误处理

**阶段失败处理**：
```javascript
async process(input) {
  let currentData = input;
  
  for (const stage of this.stages) {
    try {
      currentData = await stage.agent.process(currentData);
    } catch (error) {
      console.error(`[Pipeline] 阶段 ${stage.name} 失败：${error.message}`);
      
      // 选项 1：重试
      // currentData = await this.retry(stage, currentData);
      
      // 选项 2：跳过
      // continue;
      
      // 选项 3：终止
      throw error;
    }
  }
  
  return currentData;
}
```

---

### 3. 缓冲机制

**阶段间缓冲**：
```javascript
class BufferedPipelineAgent {
  constructor(stages, bufferSize = 3) {
    this.stages = stages;
    this.bufferSize = bufferSize;
    this.buffers = stages.map(() => []);
  }

  async processBatch(inputs) {
    // 批量处理，提高吞吐量
    for (const input of inputs) {
      this.buffers[0].push(input);
    }
    
    // 流水线执行
    for (let i = 0; i < this.stages.length; i++) {
      while (this.buffers[i].length > 0) {
        const data = this.buffers[i].shift();
        const result = await this.stages[i].agent.process(data);
        
        if (i < this.stages.length - 1) {
          this.buffers[i + 1].push(result);
        }
      }
    }
    
    return this.buffers[this.buffers.length - 1];
  }
}
```

---

## ⚠️ 常见问题与解决方案

### 问题 1：瓶颈阶段

**现象**：某个阶段特别慢，阻塞整个流水线。

**解决方案**：
```javascript
// 为瓶颈阶段创建多个实例
const bottleneckStage = {
  agent: slowAgent,
  name: '瓶颈阶段',
  instances: 3  // 3 个并行实例
};

// 并行处理
async processStage(stage, input) {
  if (stage.instances > 1) {
    // 分割输入，并行处理
    const chunks = this.chunk(input, stage.instances);
    const results = await Promise.all(
      chunks.map(chunk => stage.agent.process(chunk))
    );
    return this.merge(results);
  }
  return stage.agent.process(input);
}
```

---

### 问题 2：质量下降

**现象**：后面阶段引入错误。

**解决方案**：
```javascript
// 添加质量检查点
async process(input) {
  let currentData = input;
  
  for (let i = 0; i < this.stages.length; i++) {
    currentData = await this.stages[i].agent.process(currentData);
    
    // 质量检查
    const quality = await this.checkQuality(currentData);
    if (quality.score < 0.7) {
      console.warn(`[Pipeline] 阶段 ${i} 质量低，返回修改`);
      currentData = await this.revise(this.stages[i].agent, currentData, quality.issues);
    }
  }
  
  return currentData;
}
```

---

## 🔧 优化技巧

### 1. 并行流水线

```javascript
// 多个输入并行处理
class ParallelPipelineAgent {
  constructor(stages, concurrency = 3) {
    this.stages = stages;
    this.concurrency = concurrency;
  }

  async processBatch(inputs) {
    const results = [];
    
    for (let i = 0; i < inputs.length; i += this.concurrency) {
      const batch = inputs.slice(i, i + this.concurrency);
      const batchResults = await Promise.all(
        batch.map(input => this.process(input))
      );
      results.push(...batchResults);
    }
    
    return results;
  }
}
```

---

### 2. 动态调整

```javascript
// 根据输入类型动态选择流水线
async process(input) {
  const pipelineType = this.classifyInput(input);
  const pipeline = this.pipelines[pipelineType];
  
  if (!pipeline) {
    throw new Error(`Unknown pipeline type: ${pipelineType}`);
  }
  
  return pipeline.process(input);
}
```

---

## 📊 性能评估

### 评估指标

| 指标 | 描述 | 目标 |
|------|------|------|
| **吞吐量** | 单位时间处理的任务数 | >10/分钟 |
| **延迟** | 从输入到输出的时间 | <1 分钟 |
| **质量** | 最终输出质量评分 | >8/10 |
| **稳定性** | 无错误处理的比例 | >99% |

---

## 🔗 相关模式

- **主从模式**：可以结合使用（Manager 协调流水线）
- **ReAct**：可以在阶段内使用 ReAct
- **Reflection**：可以在阶段间添加反思

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02
