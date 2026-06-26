# AI Agent 架构模式库

> **完整模式文档** - 包含详细实现、示例、最佳实践

---

## 📁 目录结构

```
patterns/
├── README.md                 # 本文件（模式总览）
├── single-agent/             # 单 Agent 模式
│   ├── react.md              # ReAct 模式
│   ├── reflection.md         # Reflection 模式
│   ├── self-critique.md      # Self-Critique 模式
│   ├── plan-and-solve.md     # Plan-and-Solve 模式
│   └── tree-of-thoughts.md   # Tree of Thoughts 模式
└── multi-agent/              # 多 Agent 模式
    ├── manager-worker.md     # 主从模式
    ├── peer-to-peer.md       # 对等模式
    ├── hierarchical.md       # 层级模式
    ├── market-based.md       # 市场模式
    └── pipeline.md           # 流水线模式
```

---

## 🎯 单 Agent 模式 ✅ 全部完成

### ReAct (Reasoning + Acting)

**核心思想**：交替进行推理和行动。

**流程**：
```
Thought → Action → Observation → Thought → Action → ... → Answer
```

**适用场景**：
- 需要调用外部工具
- 需要多步推理
- 需要与环境交互

**实现要点**：
- 清晰的思考格式
- 明确的动作定义
- 结果观察记录

📄 详细文档：`single-agent/react.md`

---

### Reflection (反思)

**核心思想**：执行后反思，迭代改进。

**流程**：
```
Generate → Reflect → Revise → Reflect → ... → Final
```

**适用场景**：
- 需要高质量输出
- 可以自我评估
- 有时间迭代

**实现要点**：
- 明确的评估标准
- 具体的改进建议
- 迭代次数限制

📄 详细文档：`single-agent/reflection.md`

---

### Self-Critique (自我批评)

**核心思想**：主动寻找自己输出的问题。

**流程**：
```
Generate → Critique (find flaws) → Fix → Critique → ... → Final
```

**适用场景**：
- 需要高准确性
- 容易出错的任务
- 有明确错误类型

**实现要点**：
- 结构化的批评框架
- 常见错误清单
- 修复策略

📄 详细文档：`single-agent/self-critique.md`

---

### Plan-and-Solve (规划与执行)

**核心思想**：先制定完整计划，再逐步执行。

**流程**：
```
Understand → Plan → Execute Step 1 → Execute Step 2 → ... → Synthesize
```

**适用场景**：
- 复杂多步骤任务
- 需要全局规划
- 步骤间有依赖

**实现要点**：
- 完整的计划制定
- 进度跟踪
- 灵活调整

📄 详细文档：`single-agent/plan-and-solve.md`

---

### Tree of Thoughts (思维树)

**核心思想**：探索多个思考路径，选择最优。

**流程**：
```
        Root
       / | \
      /  |  \
   Thought Thoughts → Evaluate → Select Best → Expand
```

**适用场景**：
- 需要创造性
- 有多个可能方案
- 可以评估方案质量

**实现要点**：
- 思维生成策略
- 评估函数
- 搜索算法（BFS/DFS/Beam）

📄 详细文档：`single-agent/tree-of-thoughts.md`

---

## 🤝 多 Agent 模式 ✅ 全部完成

### 主从模式 (Manager-Worker)

**核心思想**：一个主 Agent 分解任务，多个从 Agent 执行。

**架构**：
```
        Manager
       /   |   \
      /    |    \
  Worker1 Worker2 Worker3
```

**适用场景**：
- 任务可分解
- 需要协调
- 有明确的管理逻辑

**实现要点**：
- 任务分解策略
- 结果整合机制
- 负载均衡

📄 详细文档：`multi-agent/manager-worker.md`

---

### 对等模式 (Peer-to-Peer)

**核心思想**：多个 Agent 平等协作，共同完成任务。

**架构**：
```
Agent1 ←→ Agent2
   ↑        ↑
   └──→ Agent3 ←→ ...
```

**适用场景**：
- 任务可并行
- Agent 能力相似
- 需要协作讨论

**实现要点**：
- 通信协议
- 冲突解决
- 共识机制

📄 详细文档：`multi-agent/peer-to-peer.md`

---

### 层级模式 (Hierarchical)

**核心思想**：多层管理结构，适合大型系统。

**架构**：
```
         CEO
         |
      Managers
      /   |   \
   Teams ...  Teams
   / | \       / | \
```

**适用场景**：
- 大型复杂项目
- 需要多层协调
- 有明确组织结构

**实现要点**：
- 层级设计
- 信息传递
- 决策权限

📄 详细文档：`multi-agent/hierarchical.md`

---

### 市场模式 (Market-Based)

**核心思想**：Agent 通过竞价获取任务。

**流程**：
```
Task Posted → Agents Bid → Select Best Bid → Execute → Pay
```

**适用场景**：
- 动态任务分配
- Agent 能力差异大
- 需要优化资源

**实现要点**：
- 竞价机制
- 评估标准
- 支付/奖励系统

📄 详细文档：`multi-agent/market-based.md`

---

### 流水线模式 (Pipeline)

**核心思想**：顺序处理，前一个输出是后一个输入。

**架构**：
```
Input → Agent1 → Agent2 → Agent3 → ... → Output
```

**适用场景**：
- 多阶段处理
- 阶段间有依赖
- 需要专业化

**实现要点**：
- 接口定义
- 错误处理
- 缓冲机制

📄 详细文档：`multi-agent/pipeline.md`

---

## 🔧 使用指南

### 选择模式

1. **分析任务**：复杂度、步骤数、是否需要协作
2. **评估资源**：可用 Agent 数量、能力、时间
3. **考虑约束**：性能要求、可靠性、成本
4. **选择模式**：参考上面的决策树

### 实现步骤

1. **定义接口**：输入、输出、错误处理
2. **实现核心逻辑**：按照模式流程
3. **添加容错**：重试、降级、超时
4. **添加监控**：日志、指标、追踪
5. **测试优化**：单元测试、集成测试、性能测试

### 组合模式

模式可以组合使用：
- ReAct + Reflection = 更高质量的单 Agent
- Manager-Worker + Pipeline = 分层流水线
- Tree of Thoughts + Market = 多路径竞价

---

## 📚 参考资源

### 学术论文
- ReAct: https://arxiv.org/abs/2210.03629
- Tree of Thoughts: https://arxiv.org/abs/2305.10601
- Reflection: https://arxiv.org/abs/2303.11366

### 开源实现
- CrewAI: https://github.com/joaomdmoura/crewAI
- AutoGen: https://github.com/microsoft/autogen
- LangChain: https://github.com/langchain-ai/langchain

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02
