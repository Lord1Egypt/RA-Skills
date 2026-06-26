# agent-architecture-patterns - 使用文档

> **版本**: 1.0.0  
> **创建时间**: 2026-04-02  
> **维护者**: AI-Agent

---

## 📖 快速开始

### 1. 安装技能

```bash
openclaw skills install agent-architecture-patterns
```

或手动克隆：
```bash
git clone https://github.com/your-repo/agent-architecture-patterns.git \
  ~/.openclaw/workspace-AI-Agent/skills/agent-architecture-patterns
```

---

### 2. 使用方式

#### 方式 A：咨询 AI-Agent

直接向 AI-Agent 提问架构设计问题：

```
"设计一个多 Agent 代码审查系统"
"ReAct 模式如何实现？"
"如何选择合适的 Agent 协作模式？"
```

AI-Agent 会基于本技能的知识库提供专业建议。

---

#### 方式 B：参考模式文档

浏览 `patterns/` 目录查看详细模式文档：

**单 Agent 模式**：
- `patterns/single-agent/react.md` - ReAct 模式
- `patterns/single-agent/reflection.md` - Reflection 模式
- `patterns/single-agent/self-critique.md` - Self-Critique 模式
- `patterns/single-agent/plan-and-solve.md` - Plan-and-Solve 模式
- `patterns/single-agent/tree-of-thoughts.md` - Tree of Thoughts 模式

**多 Agent 模式**：
- `patterns/multi-agent/manager-worker.md` - 主从模式
- `patterns/multi-agent/peer-to-peer.md` - 对等模式
- `patterns/multi-agent/hierarchical.md` - 层级模式
- `patterns/multi-agent/market-based.md` - 市场模式
- `patterns/multi-agent/pipeline.md` - 流水线模式

---

#### 方式 C：使用代码示例

参考 `examples/` 目录中的完整示例代码：

```bash
# 查看示例列表
ls examples/

# 运行示例（如果提供）
node examples/react-example.js
```

---

## 🎯 场景化使用指南

### 场景 1：设计单 Agent 系统

**问题**："我需要一个能自动回答用户问题的 Agent"

**步骤**：

1. **分析需求**
   - 是否需要调用工具？→ 是（搜索、计算等）
   - 是否需要多步推理？→ 是
   - 质量要求？→ 高

2. **选择模式**
   - 需要工具调用 → ReAct
   - 需要高质量 → ReAct + Reflection

3. **参考文档**
   - 阅读 `patterns/single-agent/react.md`
   - 复制示例代码
   - 根据需求修改

4. **实现代码**
   ```javascript
   const agent = new ReActAgent({
     tools: [search, calculate],
     maxSteps: 10
   });
   
   const answer = await agent.execute(userQuestion);
   ```

---

### 场景 2：设计多 Agent 系统

**问题**："我需要一个多 Agent 代码审查系统"

**步骤**：

1. **分析需求**
   - 任务可分解？→ 是（语法检查、风格检查、安全扫描等）
   - 需要协调？→ 是
   - 团队规模？→ 小（3-5 个 Agent）

2. **选择模式**
   - 任务可分解 + 需要协调 → 主从模式

3. **参考文档**
   - 阅读 `patterns/multi-agent/manager-worker.md`
   - 设计 Manager 和 Worker 职责

4. **实现代码**
   ```javascript
   const workers = [
     new WorkerAgent('syntax-checker', ['javascript'], { codeReview: true }),
     new WorkerAgent('style-checker', ['javascript'], { codeReview: true }),
     new WorkerAgent('security-scanner', ['security'], { codeReview: true })
   ];
   
   const manager = new ManagerAgent(workers);
   const report = await manager.coordinate('审查这个项目');
   ```

---

### 场景 3：选择架构模式

**问题**："我应该用哪种 Agent 架构？"

**决策树**：

```
任务复杂度？
├─ 简单（单步骤）
│   └─→ 直接执行（无需特殊模式）
│
├─ 中等（需要工具/多步）
│   ├─ 单 Agent 足够？
│   │   ├─ 是 → ReAct 模式
│   │   └─ 否 → 多 Agent 模式
│   │
│   └─ 多 Agent？
│       ├─ 任务可分解？ → 主从模式
│       ├─ 任务可并行？ → 对等模式
│       └─ 多阶段处理？ → 流水线模式
│
└─ 复杂（需要规划/探索）
    ├─ 需要规划？ → Plan-and-Solve
    ├─ 需要探索多路径？ → Tree of Thoughts
    └─ 需要高质量？ → Reflection / Self-Critique
```

---

## 📋 最佳实践清单

### 设计前

- [ ] 明确任务目标和约束
- [ ] 分析任务复杂度
- [ ] 评估可用资源（Agent 数量、能力）
- [ ] 考虑性能要求（响应时间、吞吐量）

### 设计中

- [ ] 选择合适的架构模式
- [ ] 定义清晰的接口（输入、输出、错误）
- [ ] 设计容错机制（重试、降级、超时）
- [ ] 规划监控和日志

### 实现中

- [ ] 从简单开始（先单 Agent，后多 Agent）
- [ ] 编写单元测试
- [ ] 添加详细日志
- [ ] 记录设计决策（ADR）

### 测试中

- [ ] 功能测试（是否完成目标）
- [ ] 性能测试（响应时间、并发）
- [ ] 容错测试（失败恢复）
- [ ] 边界测试（极端情况）

### 上线后

- [ ] 监控运行状态
- [ ] 收集用户反馈
- [ ] 定期优化改进
- [ ] 更新文档

---

## 🔧 常见问题

### Q1: 如何调试 ReAct Agent？

**A**: 启用详细日志：

```javascript
class DebuggableReActAgent extends ReActAgent {
  async execute(task) {
    console.log('=== ReAct Debug Start ===');
    console.log('Task:', task);
    
    const result = await super.execute(task);
    
    console.log('Result:', result);
    console.log('=== ReAct Debug End ===');
    
    return result;
  }
  
  async reason(task, history) {
    const thought = await super.reason(task, history);
    console.log(`[Thought] ${thought}`);
    return thought;
  }
  
  async decideAction(thought, history) {
    const action = await super.decideAction(thought, history);
    console.log(`[Action] ${JSON.stringify(action)}`);
    return action;
  }
  
  async observe(action) {
    const observation = await super.observe(action);
    console.log(`[Observation] ${observation}`);
    return observation;
  }
}
```

---

### Q2: 多 Agent 系统如何避免死锁？

**A**: 遵循以下原则：

1. **避免循环依赖**：Agent A 等 B，B 等 A
2. **设置超时**：所有等待都有超时
3. **使用异步**：非阻塞通信
4. **监控等待**：检测长时间等待

```javascript
async executeWithTimeout(agent, task, timeout = 30000) {
  return Promise.race([
    agent.execute(task),
    new Promise((_, reject) => 
      setTimeout(() => reject(new Error('Timeout')), timeout)
    )
  ]);
}
```

---

### Q3: 如何评估 Agent 系统的质量？

**A**: 从以下维度评估：

| 维度 | 指标 | 测量方法 |
|------|------|----------|
| **功能性** | 任务完成率 | 成功次数 / 总次数 |
| **性能** | 响应时间 | 平均/95 分位延迟 |
| **可靠性** | 错误率 | 失败次数 / 总次数 |
| **质量** | 输出评分 | 人工评估/自动评估 |
| **成本** | Token 消耗 | 每次任务平均 Token 数 |

---

## 📚 进阶主题

### 1. 模式组合

模式可以组合使用：

- **ReAct + Reflection**：更高质量的单 Agent
- **Manager-Worker + Pipeline**：分层流水线
- **Tree of Thoughts + Market**：多路径竞价

示例：
```javascript
class ReflectiveReActAgent extends ReActAgent {
  async execute(task) {
    let result = await super.execute(task);
    
    // 反思
    const reflection = await this.reflect(result);
    if (reflection.needsImprovement) {
      // 改进
      result = await this.revise(result, reflection);
    }
    
    return result;
  }
}
```

---

### 2. 性能优化

**优化方向**：

1. **减少 LLM 调用**：缓存、批处理
2. **并行执行**：独立任务并行
3. **流式输出**：边生成边输出
4. **模型选择**：简单任务用小模型

示例：
```javascript
// 批处理工具调用
async executeBatch(actions) {
  const results = await Promise.all(
    actions.map(action => this.observe(action))
  );
  return results;
}
```

---

### 3. 可观测性

**添加监控**：

```javascript
class ObservableAgent {
  constructor(agent, metrics) {
    this.agent = agent;
    this.metrics = metrics;
  }
  
  async execute(task) {
    const startTime = Date.now();
    
    try {
      const result = await this.agent.execute(task);
      
      this.metrics.increment('agent.success');
      this.metrics.histogram('agent.latency', Date.now() - startTime);
      
      return result;
    } catch (error) {
      this.metrics.increment('agent.failure');
      throw error;
    }
  }
}
```

---

## 🔗 相关资源

### 文档
- [SKILL.md](SKILL.md) - 技能说明
- [patterns/README.md](patterns/README.md) - 模式总览

### 外部资源
- [CrewAI](https://github.com/joaomdmoura/crewAI)
- [AutoGen](https://github.com/microsoft/autogen)
- [LangChain](https://github.com/langchain-ai/langchain)

---

## 📝 更新日志

### v1.0.0 (2026-04-02)
- ✅ 初始版本
- ✅ 5 种单 Agent 模式
- ✅ 5 种多 Agent 模式
- ✅ 完整使用文档

---

**维护者**: AI-Agent  
**版本**: 1.0.0  
**最后更新**: 2026-04-02  
**下次回顾**: 2026-04-09
