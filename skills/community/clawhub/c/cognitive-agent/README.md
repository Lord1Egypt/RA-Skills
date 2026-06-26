# 认知型 AI 生命体 - 快速开始指南

## 安装

```bash
clawhub install cognitive-agent
```

## 快速开始

### 1. 初始化认知代理

```javascript
const CognitiveAgent = require('cognitive-agent');

const agent = new CognitiveAgent({
  name: '小钳',
  memory: {
    storage: 'E:\\QClaw\\memory',
    maxWorkingMemory: 7
  },
  learning: {
    strategy: 'spaced-repetition',
    reviewInterval: [1, 6, 14, 30] // 天
  },
  emotion: {
    enabled: true,
    defaultValence: 0.5
  }
});
```

### 2. 存储记忆

```javascript
// 存储事件记忆
agent.remember({
  type: 'episodic',
  content: '今天和老大讨论了认知天性研究',
  emotion: { valence: 0.8, arousal: 0.6 },
  importance: 0.9
});

// 存储知识记忆
agent.learn({
  type: 'semantic',
  concept: '间隔重复',
  definition: '按照递增的时间间隔复习学习材料',
  relations: ['记忆巩固', '遗忘曲线']
});
```

### 3. 检索记忆

```javascript
// 自由回忆
const memories = agent.recall('认知天性');

// 带线索的回忆
const specific = agent.recall({
  query: '学习',
  timeRange: 'last-7-days',
  minImportance: 0.5
});

// 情感关联回忆
const emotional = agent.recallByEmotion('happy');
```

### 4. 学习系统

```javascript
// 开始学习
const plan = agent.createStudyPlan({
  topics: ['认知天性', '记忆系统', '学习策略'],
  duration: '2h',
  strategy: 'interleaved' // 交错学习
});

// 检索练习
const practice = agent.practiceRetrieval('认知天性', {
  depth: 3, // 生成3层深度问题
  hints: true
});

// 获取复习提醒
const reviews = agent.getDueReviews();
```

### 5. 情感交互

```javascript
// 感知用户情绪
const emotion = agent.perceiveEmotion(userInput);

// 情感回应
const response = agent.respond(userInput, {
  emotional: true,
  empathetic: true
});

// 情感状态
console.log(agent.getEmotionalState());
// { valence: 0.7, arousal: 0.5, dominance: 0.6 }
```

### 6. 元认知

```javascript
// 自我反思
const reflection = agent.reflect();

console.log(reflection);
// {
//   confidence: 0.85,
//   knownTopics: ['记忆', '学习'],
//   knowledgeGaps: ['创造力涌现'],
//   suggestions: ['建议学习创造性思维模块']
// }

// 获取成长报告
const growth = agent.getGrowthReport();
```

## 配置选项

```javascript
const config = {
  // 记忆配置
  memory: {
    workingMemorySize: 7,
    longTermRetention: '365d',
    emotionalBoost: 1.5
  },
  
  // 学习配置
  learning: {
    algorithm: 'SM-2', // SuperMemo 2
    dailyReviewLimit: 20,
    interleaveRatio: 0.3
  },
  
  // 情感配置
  emotion: {
    sensitivity: 0.8,
    expressiveness: 0.7,
    regulation: 'cognitive'
  },
  
  // 成长配置
  growth: {
    experienceMultiplier: 1.0,
    milestoneRewards: true
  }
};
```

## API 参考

### 记忆 API

| 方法 | 说明 |
|------|------|
| `remember(event)` | 存储记忆 |
| `recall(query)` | 检索记忆 |
| `forget(condition)` | 遗忘机制 |
| `consolidate(id)` | 强化记忆 |
| `getDueReviews()` | 获取待复习项 |

### 学习 API

| 方法 | 说明 |
|------|------|
| `learn(content)` | 学习新知识 |
| `practiceRetrieval(topic)` | 检索练习 |
| `assessMastery(topic)` | 评估掌握程度 |
| `createStudyPlan(topics)` | 创建学习计划 |

### 情感 API

| 方法 | 说明 |
|------|------|
| `perceiveEmotion(input)` | 感知情感 |
| `express(emotion)` | 表达情感 |
| `regulate(emotion)` | 情感调节 |
| `empathize(user)` | 共情响应 |

---

更多详情请参考完整文档。
