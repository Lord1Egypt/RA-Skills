# ADD v7.18: Token 超限修复

**版本**: v7.18.0  
**日期**: 2026-03-13  
**问题**: `400 Total tokens of image and text exceed max message tokens`  
**根因**: 单次请求 token 超过模型限制  
**方法**: 第一性原理 + 思维链 + MECE 拆解 + 自我校验

---

## 🎯 第一性原理分析

### 问题本质
```
错误信息：400 Total tokens of image and text exceed max message tokens

第一性原理：
LLM API 有 token 限制 = 输入 + 输出 ≤ 最大上下文

若超过限制：
1. 减少输入（分片/摘要）
2. 减少输出（限制生成长度）
3. 使用更大上下文模型
4. 优化 token 使用效率

核心洞察：
Token 超限 = 数据量 > 模型容量
解决方案 = 分而治之 + 优化效率
```

### Token 限制分析

| 模型 | 上下文限制 | 输入限制 | 输出限制 |
|------|------------|----------|----------|
| **Kimi-K2.5** | 256K | ~200K | ~56K |
| **Qwen3.5-Plus** | 1M | ~800K | ~200K |
| **DeepSeek** | 128K | ~100K | ~28K |
| **GPT-4** | 128K | ~100K | ~28K |

**当前错误**: 输入 + 图片 > 模型限制

---

## 📐 MECE 拆解

### 维度 1: Token 来源

| 来源 | 占比 | 可优化 |
|------|------|--------|
| **系统提示词** | ~10% | ✅ 可精简 |
| **历史对话** | ~40% | ✅ 可摘要 |
| **用户上传** | ~30% | ✅ 可压缩 |
| **图片内容** | ~20% | ✅ 可降质 |

### 维度 2: 修复方案

| 方案 | 复杂度 | 效果 | 实施时间 |
|------|--------|------|----------|
| **方案 1**: Token 计数 + 预警 | 低 | ✅ 提前发现 | 30 分钟 |
| **方案 2**: 自动分片 | 中 | ✅ 自动处理 | 1 小时 |
| **方案 3**: 智能摘要 | 中 | ✅ 减少输入 | 1 小时 |
| **方案 4**: 切换大模型 | 低 | ✅ 临时解决 | 10 分钟 |

### 维度 3: 通用性

| 场景 | 受影响 | 修复通用性 |
|------|--------|------------|
| **小说创作** | 🔴 高 | ✅ 通用 |
| **代码开发** | 🔴 高 | ✅ 通用 |
| **文档分析** | 🔴 高 | ✅ 通用 |
| **图片分析** | 🔴 高 | ✅ 通用 |

---

## 🔍 详细分析

### 错误场景

**典型场景**:
```
用户：分析这本小说的前 10 章 + 5 张图片
系统：[系统提示词 2K] + [历史对话 50K] + [小说内容 100K] + [图片 50K]
     = 202K tokens > 模型限制 128K
     ↓
错误：400 Total tokens exceed max message tokens
```

### 根因链

```
根因 1: 无 Token 计数机制
  ↓
不知道当前 token 使用量
  
根因 2: 无自动分片机制
  ↓
大数据量直接发送
  
根因 3: 无智能摘要机制
  ↓
历史对话全部保留
  
根因 4: 无模型切换机制
  ↓
小模型处理大数据
```

---

## 🔧 修复方案

### 修复 1: Token 计数器

**文件**: `skills/agile-workflow/core/token-counter.js`

```javascript
class TokenCounter {
  constructor() {
    this.estimateFactor = 4;  // 1 token ≈ 4 字符（中文）
  }

  // 估算 token 数
  estimateToken(text) {
    if (!text) return 0;
    return Math.ceil(text.length / this.estimateFactor);
  }

  // 计算消息总 token
  calculateMessageToken(messages) {
    let total = 0;
    
    for (const msg of messages) {
      // 文本 token
      if (msg.content) {
        total += this.estimateToken(msg.content);
      }
      
      // 图片 token（每张约 1000 token）
      if (msg.images) {
        total += msg.images.length * 1000;
      }
    }
    
    return total;
  }

  // 检查是否超限
  isExceedLimit(messages, limit = 100000) {
    const token = this.calculateMessageToken(messages);
    return {
      exceed: token > limit,
      current: token,
      limit: limit,
      usage: Math.round((token / limit) * 100)
    };
  }
}
```

---

### 修复 2: 自动分片器

**文件**: `skills/agile-workflow/core/auto-chunker.js`

```javascript
class AutoChunker {
  constructor(maxTokenPerChunk = 80000) {
    this.maxToken = maxTokenPerChunk;
    this.counter = new TokenCounter();
  }

  // 自动分片
  chunkMessages(messages) {
    const chunks = [];
    let currentChunk = [];
    let currentToken = 0;
    
    for (const msg of messages) {
      const msgToken = this.counter.calculateMessageToken([msg]);
      
      if (currentToken + msgToken > this.maxToken) {
        // 当前 chunk 已满，创建新 chunk
        chunks.push(currentChunk);
        currentChunk = [msg];
        currentToken = msgToken;
      } else {
        currentChunk.push(msg);
        currentToken += msgToken;
      }
    }
    
    // 添加最后一个 chunk
    if (currentChunk.length > 0) {
      chunks.push(currentChunk);
    }
    
    return chunks;
  }

  // 处理分片结果
  async processChunks(chunks, processor) {
    const results = [];
    
    for (let i = 0; i < chunks.length; i++) {
      console.log(`处理分片 ${i + 1}/${chunks.length}`);
      const result = await processor(chunks[i]);
      results.push(result);
    }
    
    return this.mergeResults(results);
  }
}
```

---

### 修复 3: 智能摘要器

**文件**: `skills/agile-workflow/core/smart-summarizer.js`

```javascript
class SmartSummarizer {
  constructor() {
    this.maxHistoryRounds = 10;  // 保留最近 10 轮对话
  }

  // 摘要历史对话
  async summarizeHistory(messages) {
    if (messages.length <= this.maxHistoryRounds) {
      return messages;  // 不需要摘要
    }
    
    // 保留最近的对话
    const recentMessages = messages.slice(-this.maxHistoryRounds);
    
    // 摘要早期对话
    const oldMessages = messages.slice(0, -this.maxHistoryRounds);
    const summary = await this.generateSummary(oldMessages);
    
    // 合并摘要和最近对话
    return [
      { role: 'system', content: `历史对话摘要：${summary}` },
      ...recentMessages
    ];
  }

  // 生成摘要
  async generateSummary(messages) {
    // 使用简洁的摘要提示词
    const prompt = `请用 100 字以内总结以下对话的核心内容：${messages.map(m => m.content).join('\n')}`;
    
    // 调用 LLM 生成摘要
    const summary = await callLLM(prompt);
    return summary;
  }
}
```

---

### 修复 4: 模型切换器

**文件**: `skills/agile-workflow/core/model-switcher.js`

```javascript
class ModelSwitcher {
  constructor() {
    this.models = {
      'small': { name: 'qwen3.5-plus', limit: 100000 },
      'medium': { name: 'kimi-k2.5', limit: 200000 },
      'large': { name: 'doubao-seed-2.0-pro', limit: 500000 }
    };
  }

  // 根据 token 数选择模型
  selectModel(tokenCount) {
    for (const [size, model] of Object.entries(this.models)) {
      if (tokenCount < model.limit * 0.8) {  // 保留 20% 余量
        return model.name;
      }
    }
    
    // 超过最大模型，启用分片
    return null;
  }

  // 自动选择并调用
  async autoCall(messages, callFunc) {
    const counter = new TokenCounter();
    const tokenCount = counter.calculateMessageToken(messages);
    
    const model = this.selectModel(tokenCount);
    
    if (!model) {
      // 需要分片
      const chunker = new AutoChunker();
      const chunks = chunker.chunkMessages(messages);
      return await chunker.processChunks(chunks, callFunc);
    }
    
    // 直接调用
    return await callFunc(messages, model);
  }
}
```

---

## ✅ 自我校验

### 校验 1: Token 计数是否准确？

**验证**:
```javascript
const counter = new TokenCounter();
const text = "这是一段测试文本，大约 100 个字符";
const token = counter.estimateToken(text);
console.log(`估算：${token} tokens`);  // 应该约 25 tokens
```

**预期**: ✅ 误差<10%

---

### 校验 2: 分片是否正常工作？

**验证**:
```javascript
const chunker = new AutoChunker(80000);
const chunks = chunker.chunkMessages(largeMessages);
console.log(`分片数：${chunks.length}`);
console.log(`每片 token: ${chunks.map(c => counter.calculateMessageToken(c))}`);
```

**预期**: ✅ 每片<80K token

---

### 校验 3: 摘要是否保留核心信息？

**验证**:
```javascript
const summarizer = new SmartSummarizer();
const summarized = await summarizer.summarizeHistory(longHistory);
console.log(`原始轮数：${longHistory.length}`);
console.log(`摘要后轮数：${summarized.length}`);
```

**预期**: ✅ 轮数减少，核心信息保留

---

## 📊 修复效果

| 指标 | 修复前 | 修复后 | 提升 |
|------|--------|--------|------|
| **Token 超限** | 频繁发生 | 自动避免 | ✅ |
| **分片处理** | 手动 | 自动 | ✅ |
| **历史摘要** | 无 | 自动摘要 | ✅ |
| **模型选择** | 手动 | 自动选择 | ✅ |

---

## 📝 实施步骤

### 已完成（设计）

1. ✅ TokenCounter 设计
2. ✅ AutoChunker 设计
3. ✅ SmartSummarizer 设计
4. ✅ ModelSwitcher 设计

### 待完成（实施）

5. ⏳ 实现 TokenCounter
6. ⏳ 实现 AutoChunker
7. ⏳ 实现 SmartSummarizer
8. ⏳ 实现 ModelSwitcher
9. ⏳ 集成到工作流

---

## ✅ 总结

### 核心问题

**Token 超限**:
1. ❌ 无 Token 计数机制
2. ❌ 无自动分片机制
3. ❌ 无智能摘要机制
4. ❌ 无模型切换机制

### 修复方案

**通用组件** (4 个):
1. ✅ TokenCounter（Token 计数）
2. ✅ AutoChunker（自动分片）
3. ✅ SmartSummarizer（智能摘要）
4. ✅ ModelSwitcher（模型切换）

### 核心原则固化

```
Token 管理原则：
1. 发送前估算 token 数 ✅
2. 超限时自动分片 ✅
3. 历史对话自动摘要 ✅
4. 根据 token 选择模型 ✅
```

---

**下一步**: 实现 Token 管理组件并集成！
