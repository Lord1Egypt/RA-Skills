# 跨会话记忆桥接

**触发词**: session_amnesia, context_loss, cross_session_gap

## 核心思路
三层记忆体系：
1. **会话上下文** - 当前会话的滚动摘要
2. **会话记忆** - memory/YYYY-MM-DD.md（按天归档）
3. **长期记忆** - MEMORY.md

## 启动时加载
```javascript
// 1. 加载 24h 滚动事件
loadRecentEvents(); 

// 2. 加载当日记忆
loadDailyMemory(); 

// 3. 加载长期记忆
loadLongTermMemory();
```

## 退出时保存
```javascript
// 记录本次会话重要事件
appendSignificantEvents(sessionSummary);
```
