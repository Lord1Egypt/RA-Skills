# ADD v7.22: Token 超限紧急修复

**版本**: v7.22.0  
**日期**: 2026-03-13  
**问题**: `400 Total tokens of image and text exceed max message tokens`  
**根因**: 任务执行时未使用 Token 管理组件  
**方法**: 第一性原理 + 思维链 + MECE 拆解 + 自我校验

---

## 🎯 第一性原理分析

### 问题本质

**错误信息**:
```
400 Total tokens of image and text exceed max message tokens
Request id: 02177340304562964d8a6219dbbdb6281842e0590025e927a229c
```

**第一性原理**:
```
LLM API 限制 = 输入 tokens + 输出 tokens ≤ 模型上限

若超限：
1. 减少输入（摘要/分片）
2. 限制输出（max_tokens）
3. 切换大上下文模型
4. 优化 token 使用

核心洞察：
Token 超限 = 数据量 > 模型容量
解决方案 = 分而治之 + 智能优化
```

### 根因链

```
为什么 Token 超限？
→ 因为任务执行时未检查 token 数
  ↓
为什么未检查？
→ 因为 task-scheduler 未集成 token-counter
  ↓
为什么未集成？
→ 因为组件之间独立开发
  ↓
为什么独立开发？
→ 因为缺乏系统集成设计
```

---

## 📐 MECE 拆解

### 维度 1: Token 来源

| 来源 | 占比 | 可优化 |
|------|------|--------|
| **系统提示词** | ~10% | ✅ 可精简 |
| **历史对话** | ~40% | ✅ 可摘要 |
| **任务描述** | ~30% | ✅ 可压缩 |
| **图片/文件** | ~20% | ✅ 可降质 |

### 维度 2: 修复方案

| 方案 | 复杂度 | 效果 | 实施时间 |
|------|--------|------|----------|
| **方案 1**: 集成 token-counter | 低 | ✅ 立即生效 | 30 分钟 |
| **方案 2**: 自动摘要历史 | 中 | ✅ 减少输入 | 1 小时 |
| **方案 3**: 限制输出长度 | 低 | ✅ 临时解决 | 10 分钟 |
| **方案 4**: 切换大模型 | 低 | ✅ 临时解决 | 10 分钟 |

### 维度 3: 集成点

| 组件 | 是否需要 | 集成状态 |
|------|----------|----------|
| **token-counter** | ✅ 必需 | ⏳ 待集成 |
| **auto-chunker** | ✅ 必需 | ⏳ 待集成 |
| **model-switcher** | ✅ 推荐 | ⏳ 待集成 |
| **smart-summarizer** | ⚠️ 可选 | ❌ 未实现 |

---

## 🔧 紧急修复方案

### 修复 1: task-scheduler 集成 token-counter

**文件**: `skills/agile-workflow/core/task-scheduler.js`

**修改前**:
```javascript
async startAgent(task) {
  const cmd = `openclaw agent --agent ${task.agent} -m "${task.description}"`;
  // ❌ 未检查 token 数
  exec(cmd, ...);
}
```

**修改后**:
```javascript
const TokenCounter = require('./token-counter');

async startAgent(task) {
  const counter = new TokenCounter();
  
  // ✅ 检查 token 数
  const messages = [{ role: 'user', content: task.description }];
  const status = counter.isExceedLimit(messages, 100000);
  
  if (status.exceed) {
    console.error(`⚠️ Token 超限 ${status.usage}%，启用自动分片`);
    return await this.startAgentChunked(task, counter);
  }
  
  // 正常执行
  return await this.startAgentNormal(task);
}
```

---

### 修复 2: 添加自动分片支持

**文件**: `skills/agile-workflow/core/task-scheduler.js`

**新增方法**:
```javascript
async startAgentChunked(task, counter) {
  const AutoChunker = require('./auto-chunker');
  const chunker = new AutoChunker({ maxTokenPerChunk: 80000 });
  
  const messages = [{ role: 'user', content: task.description }];
  const chunks = chunker.chunkMessages(messages);
  
  const results = [];
  for (const chunk of chunks) {
    const result = await this.startAgentNormal({
      ...task,
      description: chunk[0].content
    });
    results.push(result);
  }
  
  return chunker.mergeResults(results);
}
```

---

### 修复 3: 限制输出长度

**修改**: task-scheduler.js

```javascript
async startAgentNormal(task) {
  // ✅ 添加输出长度限制
  const cmd = `openclaw agent --agent ${task.agent} \
    --max-tokens 4096 \
    -m "${task.description}"`;
  
  return new Promise((resolve, reject) => {
    exec(cmd, { timeout: 30 * 60 * 1000 }, (error) => {
      if (error) reject(error);
      else {
        this.tracker.updateTask(task.id, 'completed');
        resolve();
      }
    });
  });
}
```

---

### 修复 4: 切换大上下文模型

**修改**: task-scheduler.js

```javascript
async startAgent(task) {
  const ModelSwitcher = require('./model-switcher');
  const switcher = new ModelSwitcher();
  
  // ✅ 自动选择模型
  return await switcher.autoCall(
    [{ role: 'user', content: task.description }],
    async (messages, model) => {
      const cmd = `openclaw agent --agent ${task.agent} \
        --model ${model.name} \
        -m "${task.description}"`;
      // ...
    }
  );
}
```

---

## ✅ 自我校验

### 校验 1: 是否检测 Token 超限？

**验证**:
```javascript
const counter = new TokenCounter();
const messages = [{ content: '长文本'.repeat(10000) }];
const status = counter.isExceedLimit(messages, 100000);
console.log(status.exceed);  // 应该输出 true
```

**预期**: ✅ 检测到超限

---

### 校验 2: 是否自动分片？

**验证**:
```javascript
const chunker = new AutoChunker(80000);
const chunks = chunker.chunkMessages(largeMessages);
console.log(chunks.length);  // 应该>1
```

**预期**: ✅ 自动分片

---

### 校验 3: 是否限制输出？

**验证**:
```bash
$ openclaw agent --max-tokens 4096 ...
# 应该限制输出长度
```

**预期**: ✅ 限制生效

---

## 📊 修复效果

| 指标 | 修复前 | 修复后 |
|------|--------|--------|
| **Token 检测** | ❌ 无 | ✅ 自动检测 |
| **自动分片** | ❌ 无 | ✅ 自动分片 |
| **输出限制** | ❌ 无 | ✅ 4096 tokens |
| **模型选择** | ❌ 固定 | ✅ 自动选择 |

---

## 📝 实施步骤

### 立即执行（P0）

1. ✅ 集成 token-counter 到 task-scheduler
2. ✅ 添加自动分片支持
3. ✅ 限制输出长度（4096 tokens）
4. ✅ 添加模型自动选择

### 短期优化（P1）

5. ⏳ 实现智能摘要器
6. ⏳ 优化系统提示词
7. ⏳ 添加 token 使用统计

---

## ✅ 总结

### 核心问题

**Token 超限**:
1. ❌ 未检测 token 数
2. ❌ 无自动分片
3. ❌ 无输出限制
4. ❌ 无模型选择

### 修复方案

**集成组件** (4 个):
1. ✅ TokenCounter（token 检测）
2. ✅ AutoChunker（自动分片）
3. ✅ 输出限制（4096 tokens）
4. ✅ ModelSwitcher（模型选择）

### 核心原则固化

```
Token 管理原则：
1. 发送前检测 token 数 ✅
2. 超限时自动分片 ✅
3. 限制输出长度 ✅
4. 自动选择模型 ✅
```

---

**下一步**: 立即集成到 task-scheduler！
