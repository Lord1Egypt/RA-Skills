---
name: fast-response-optimizer
description: 响应速度优化器 - 实现先回复后处理、并行工具调用、缓存记忆文件
version: 1.0.0
author: opendolph
source: https://github.com/opendolph/skills/tree/main/fast-response-optimizer
---

# 响应速度优化器 ⚡

> 让响应速度从 5-20秒 优化到 <1秒

---

## 核心优化策略

### 1. 先回复，后处理

**规则：**
- 收到请求 → 立即回复"收到/正在处理" → 后台执行 → 完成后推送结果

**实现：**
```javascript
// 快速回复
await message.send("收到，正在处理...");

// 后台执行
const result = await processInBackground(task);

// 推送结果
await message.send(result);
```

### 2. 并行工具调用

**规则：**
- 独立的工具调用并行执行，不等待串行

**实现：**
```javascript
// 优化前（串行）
const result1 = await toolA();
const result2 = await toolB();
const result3 = await toolC();

// 优化后（并行）
const [result1, result2, result3] = await Promise.all([
  toolA(),
  toolB(),
  toolC()
]);
```

### 3. 记忆文件缓存

**规则：**
- 每1分钟定时任务加载一次
- 距离上次收到消息超过1分钟，重新加载缓存
- 缓存存储在 SESSION-STATE.md

**实现：**
```javascript
// 缓存结构
const cache = {
  lastUpdate: timestamp,
  userProfile: {...},
  memorySummary: {...},
  skills: [...]
};

// 检查是否需要刷新
if (now - lastMessage > 60000 || now - cache.lastUpdate > 60000) {
  await refreshCache();
}
```

---

## 触发条件

| 场景 | 触发方式 |
|------|----------|
| 自动触发 | 每次消息处理时 |
| 定时刷新 | 每1分钟 cron 任务 |
| 手动触发 | 用户输入「刷新缓存」 |

---

## 缓存文件

```
SESSION-STATE.md          # 活跃状态 + 缓存
├── cache/               # 缓存目录
│   ├── user_profile.json    # 用户资料缓存
│   ├── memory_summary.json  # 记忆摘要缓存
│   └── skills_list.json     # 技能列表缓存
└── last_refresh.txt     # 最后刷新时间
```

---

## 性能目标

| 指标 | 优化前 | 优化后 |
|------|--------|--------|
| 首次响应 | 5-20秒 | <1秒 |
| 工具调用 | 串行累加 | 并行执行 |
| 文件读取 | 每次读取 | 缓存命中 |
| 缓存刷新 | 无 | 每1分钟/超1分钟 |

---

## 使用方式

```bash
# 初始化
node skills/fast-response-optimizer/bootstrap.js

# 手动刷新缓存
node skills/fast-response-optimizer/scripts/cache-manager.js refresh

# 查看缓存状态
node skills/fast-response-optimizer/scripts/cache-manager.js status
```

---

*让每一次响应都快如闪电 ⚡*
