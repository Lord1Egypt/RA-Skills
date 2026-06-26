---
name: forget-something
description: Implement forgetting mechanisms for AI systems to manage memory overload, improve performance, and maintain data privacy. Use when working with long-term AI systems, memory management, or privacy-preserving AI.
---

# Forget Something Skill
# 遗忘机制技能

This skill enables implementation of forgetting mechanisms for AI systems, particularly for OpenClaw agents, to manage memory overload, improve performance, and maintain data privacy.
该技能为AI系统（特别是OpenClaw智能体）实现遗忘机制，用于管理内存过载、提高性能和维护数据隐私。

## Overview
## 概述

Forgetting mechanisms are essential for AI systems that accumulate large amounts of data over time. They help:
- Prevent memory bloat and performance degradation
- Maintain data privacy by removing outdated or sensitive information
- Focus on relevant information by eliminating noise
- Comply with data retention policies and regulations

遗忘机制对于随时间积累大量数据的AI系统至关重要。它们有助于：
- 防止内存膨胀和性能下降
- 通过移除过时或敏感信息来维护数据隐私
- 通过消除噪音来专注于相关信息
- 遵守数据保留政策和法规

## Forgetting Strategies
## 遗忘策略

### 1. Time-Based Forgetting
### 1. 基于时间的遗忘

Remove data after a specified time period.
在指定时间段后移除数据。

```javascript
// Example: Remove memories older than 30 days
// 示例：删除超过30天的记忆
const forgetOldMemories = (memoryStore, days = 30) => {
  const cutoffTime = Date.now() - (days * 24 * 60 * 60 * 1000);
  memoryStore.filter(memory => memory.timestamp > cutoffTime);
};
```

### 2. Relevance-Based Forgetting
### 2. 基于相关性的遗忘

Remove data based on relevance score.
基于相关性分数移除数据。

```javascript
// Example: Remove memories with relevance score below threshold
// 示例：删除相关性分数低于阈值的记忆
const forgetIrrelevantMemories = (memoryStore, threshold = 0.3) => {
  memoryStore.filter(memory => memory.relevance >= threshold);
};
```

### 3. Frequency-Based Forgetting
### 3. 基于访问频率的遗忘

Remove data based on access frequency.
基于访问频率移除数据。

```javascript
// Example: Remove memories accessed less than N times
// 示例：删除访问次数少于N次的记忆
const forgetInfrequentMemories = (memoryStore, minAccessCount = 2) => {
  memoryStore.filter(memory => memory.accessCount >= minAccessCount);
};
```

### 4. Explicit Forgetting
### 4. 显式遗忘

Remove specific data based on user requests.
根据用户请求移除特定数据。

```javascript
// Example: Remove specific memory by ID
// 示例：通过ID删除特定记忆
const forgetSpecificMemory = (memoryStore, memoryId) => {
  memoryStore.filter(memory => memory.id !== memoryId);
};
```

### 5. Context-Based Forgetting
### 5. 基于上下文的遗忘

Remove data based on current context relevance.
基于当前上下文相关性移除数据。

```javascript
// Example: Remove memories unrelated to current task
// 示例：删除与当前任务无关的记忆
const forgetContextIrrelevant = (memoryStore, currentContext) => {
  memoryStore.filter(memory => {
    return memory.topics.some(topic => currentContext.topics.includes(topic));
  });
};
```

## Implementation for OpenClaw
## OpenClaw实现

### Memory Store Structure
### 记忆存储结构

```javascript
// Example memory structure
// 示例记忆结构
const memory = {
  id: "unique-id-123",
  content: "This is a memory content",
  timestamp: Date.now(),
  relevance: 0.8,
  accessCount: 5,
  topics: ["project", "meeting", "action-item"],
  source: "user-input",
  sensitivity: "low" // low, medium, high
  // 敏感度：低、中、高
};
```

### Forgetting Configuration
### 遗忘配置

```javascript
// OpenClaw forgetting configuration
// OpenClaw遗忘配置
const forgettingConfig = {
  strategies: [
    {
      type: "time-based",
      days: 30,
      enabled: true
    },
    {
      type: "relevance-based",
      threshold: 0.3,
      enabled: true
    },
    {
      type: "frequency-based",
      minAccessCount: 2,
      enabled: true
    }
  ],
  runInterval: "daily", // daily, weekly, monthly
  // 运行间隔：每日、每周、每月
  dryRun: false, // preview what would be deleted
  // 模拟运行：预览将要删除的内容
  backupBeforeForgetting: true
  // 遗忘前备份：是
};
```

### Integration with OpenClaw
### 与OpenClaw集成

```javascript
// Example integration with OpenClaw agent
// 与OpenClaw智能体集成示例
const OpenClawForgettingMechanism = {
  init(agent) {
    this.agent = agent;
    this.memoryStore = agent.memory;
    this.config = agent.config.forgettingMechanism || {};
    this.setupScheduler();
  },
  
  setupScheduler() {
    const interval = this.config.runInterval || "daily";
    const cronExpression = this.getCronExpression(interval);
    
    // Schedule forgetting based on configuration
    // 根据配置安排遗忘任务
    this.agent.scheduler.addJob({
      name: "forgetting-mechanism",
      cron: cronExpression,
      task: () => this.runForgetting()
    });
  },
  
  getCronExpression(interval) {
    const expressions = {
      daily: "0 0 * * *",
      weekly: "0 0 * * 0",
      monthly: "0 0 1 * *"
    };
    return expressions[interval] || "0 0 * * *";
  },
  
  async runForgetting() {
    this.agent.logger.info("Running forgetting mechanism...");
    
    const originalCount = this.memoryStore.size;
    
    // Apply all enabled strategies
    // 应用所有启用的策略
    this.config.strategies?.forEach(strategy => {
      if (strategy.enabled) {
        this.applyStrategy(strategy);
      }
    });
    
    const finalCount = this.memoryStore.size;
    const removedCount = originalCount - finalCount;
    
    this.agent.logger.info(`Forgetting mechanism completed: Removed ${removedCount} memories`);
    
    return {
      originalCount,
      finalCount,
      removedCount
    };
  },
  
  applyStrategy(strategy) {
    switch (strategy.type) {
      case "time-based":
        this.forgetTimeBased(strategy.days);
        break;
      case "relevance-based":
        this.forgetRelevanceBased(strategy.threshold);
        break;
      case "frequency-based":
        this.forgetFrequencyBased(strategy.minAccessCount);
        break;
      case "context-based":
        this.forgetContextBased(strategy.context);
        break;
      default:
        this.agent.logger.warn(`Unknown forgetting strategy: ${strategy.type}`);
    }
  },
  
  forgetTimeBased(days = 30) {
    const cutoffTime = Date.now() - (days * 24 * 60 * 60 * 1000);
    this.memoryStore.filter(memory => memory.timestamp > cutoffTime);
  },
  
  forgetRelevanceBased(threshold = 0.3) {
    this.memoryStore.filter(memory => memory.relevance >= threshold);
  },
  
  forgetFrequencyBased(minAccessCount = 2) {
    this.memoryStore.filter(memory => memory.accessCount >= minAccessCount);
  },
  
  forgetContextBased(context) {
    this.memoryStore.filter(memory => {
      return memory.topics.some(topic => context.topics.includes(topic));
    });
  },
  
  // Manual forgetting methods
  // 手动遗忘方法
  forgetSpecificMemory(memoryId) {
    return this.memoryStore.filter(memory => memory.id !== memoryId);
  },
  
  forgetByTopic(topic) {
    return this.memoryStore.filter(memory => !memory.topics.includes(topic));
  },
  
  forgetAll() {
    return this.memoryStore.clear();
  }
};
```

## Usage Examples
## 使用示例

### 1. Configure Forgetting Mechanism
### 1. 配置遗忘机制

```javascript
// In agent configuration
// 在智能体配置中
const agentConfig = {
  // ... other config
  // ... 其他配置
  forgettingMechanism: {
    strategies: [
      {
        type: "time-based",
        days: 30,
        enabled: true
      },
      {
        type: "relevance-based",
        threshold: 0.4,
        enabled: true
      }
    ],
    runInterval: "daily",
    backupBeforeForgetting: true
  }
};
```

### 2. Manual Forgetting
### 2. 手动遗忘

```javascript
// In agent code
// 在智能体代码中
await agent.forgettingMechanism.forgetSpecificMemory("memory-id-123");
await agent.forgettingMechanism.forgetByTopic("confidential");
```

### 3. Run Forgetting on Demand
### 3. 按需运行遗忘

```javascript
// Trigger forgetting manually
// 手动触发遗忘
const result = await agent.forgettingMechanism.runForgetting();
console.log(`Removed ${result.removedCount} memories`);
```

## Best Practices
## 最佳实践

1. **Backup Strategy**: Always backup memories before running forgetting operations
1. **备份策略**：在运行遗忘操作前始终备份记忆

2. **Dry Run First**: Use dryRun mode to preview what would be deleted
2. **先模拟运行**：使用dryRun模式预览将要删除的内容

3. **Gradual Implementation**: Start with conservative settings and adjust over time
3. **逐步实施**：从保守设置开始，随着时间推移进行调整

4. **Monitor Impact**: Track performance and user experience after forgetting operations
4. **监控影响**：在遗忘操作后跟踪性能和用户体验

5. **Combine Strategies**: Use multiple strategies for more effective memory management
5. **组合策略**：使用多种策略进行更有效的记忆管理

6. **Privacy Compliance**: Ensure forgetting mechanisms comply with data protection regulations
6. **隐私合规**：确保遗忘机制符合数据保护法规

## Privacy Considerations
## 隐私考虑

- **Right to be Forgotten**: Implement explicit forgetting for user requests
- **被遗忘权**：为用户请求实现显式遗忘

- **Data Minimization**: Only retain data that is necessary for the system's purpose
- **数据最小化**：只保留系统目的所需的数据

- **Sensitive Data**: Apply stricter forgetting rules to sensitive information
- **敏感数据**：对敏感信息应用更严格的遗忘规则

- **Audit Trail**: Maintain logs of forgetting operations for accountability
- **审计跟踪**：保留遗忘操作的日志以确保问责制

## Performance Benefits
## 性能优势

- **Reduced Memory Footprint**: Smaller memory stores use less system resources
- **减少内存占用**：更小的记忆存储使用更少的系统资源

- **Faster Retrieval**: Queries run faster on smaller datasets
- **更快的检索**：在较小的数据集上查询运行更快

- **Improved Relevance**: Focus on more recent and relevant information
- **提高相关性**：专注于更新的相关信息

- **Lower Storage Costs**: Reduce storage requirements for long-term operations
- **降低存储成本**：减少长期运营的存储需求

## Testing and Validation
## 测试与验证

```javascript
// Example test for forgetting mechanism
// 遗忘机制测试示例
const testForgettingMechanism = () => {
  // Create test memories
  // 创建测试记忆
  const testMemories = [
    {
      id: "mem1",
      content: "Old memory",
      timestamp: Date.now() - (40 * 24 * 60 * 60 * 1000), // 40 days old
      // 40天前
      relevance: 0.2,
      accessCount: 1
    },
    {
      id: "mem2",
      content: "Recent relevant memory",
      timestamp: Date.now() - (10 * 24 * 60 * 60 * 1000), // 10 days old
      // 10天前
      relevance: 0.8,
      accessCount: 5
    },
    {
      id: "mem3",
      content: "Recent irrelevant memory",
      timestamp: Date.now() - (5 * 24 * 60 * 60 * 1000), // 5 days old
      // 5天前
      relevance: 0.1,
      accessCount: 1
    }
  ];
  
  // Initialize memory store
  // 初始化记忆存储
  const memoryStore = new MemoryStore(testMemories);
  
  // Create forgetting mechanism
  // 创建遗忘机制
  const forgetting = new OpenClawForgettingMechanism();
  forgetting.memoryStore = memoryStore;
  forgetting.config = {
    strategies: [
      { type: "time-based", days: 30, enabled: true },
      { type: "relevance-based", threshold: 0.3, enabled: true }
    ]
  };
  
  // Run forgetting
  // 运行遗忘
  forgetting.runForgetting();
  
  // Verify results
  // 验证结果
  const remainingMemories = memoryStore.getAll();
  console.log(`Remaining memories: ${remainingMemories.length}`);
  console.log(remainingMemories.map(m => m.content));
  
  // Should only keep mem2
  // 应该只保留mem2
  return remainingMemories.length === 1 && remainingMemories[0].id === "mem2";
};
```

## Integration Points
## 集成点

- **OpenClaw Agents**: Integrate with agent memory systems
- **OpenClaw智能体**：与智能体记忆系统集成

- **Schedulers**: Run forgetting operations on a schedule
- **调度器**：按计划运行遗忘操作

- **API Endpoints**: Expose forgetting functionality via API
- **API端点**：通过API公开遗忘功能

- **User Interfaces**: Allow users to configure and trigger forgetting
- **用户界面**：允许用户配置和触发遗忘

## Future Enhancements
## 未来增强

- **Machine Learning-Based Forgetting**: Use ML to predict which memories to forget
- **基于机器学习的遗忘**：使用ML预测哪些记忆需要被遗忘

- **Adaptive Strategies**: Automatically adjust forgetting parameters based on usage patterns
- **自适应策略**：根据使用模式自动调整遗忘参数

- **Memory Compression**: Compress less important memories instead of deleting them
- **记忆压缩**：压缩不太重要的记忆而不是删除它们

- **Cross-Agent Forgetting**: Coordinate forgetting across multiple connected agents
- **跨智能体遗忘**：在多个连接的智能体之间协调遗忘

## References
## 参考资料

- [Memory Management in AI Systems](https://arxiv.org/abs/2106.05237)
- [AI系统中的记忆管理](https://arxiv.org/abs/2106.05237)

- [Forgetting in Artificial Intelligence](https://link.springer.com/article/10.1007/s10462-020-09844-0)
- [人工智能中的遗忘](https://link.springer.com/article/10.1007/s10462-020-09844-0)

- [Data Privacy Regulations (GDPR, CCPA)](https://gdpr.eu/right-to-be-forgotten/)
- [数据隐私法规（GDPR, CCPA）](https://gdpr.eu/right-to-be-forgotten/)