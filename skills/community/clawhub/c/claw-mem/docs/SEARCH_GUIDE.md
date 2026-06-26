# 🔍 ClawMem 搜索功能使用指南

## 概述

ClawMem v0.0.3 引入了强大的搜索功能，支持多种搜索方式：

- 🔑 **关键词搜索** - 在 L0 索引中搜索关键词
- 📅 **时间范围搜索** - 在 L1 时间线中按时间搜索
- 🏷️ **标签搜索** - 按标签搜索相关记录
- 💬 **会话搜索** - 获取完整会话记录
- 🔬 **高级搜索** - 组合多种搜索条件

---

## 使用示例

### 1. 关键词搜索

```javascript
import { memorySearch } from './clawmem/src/index.js';

// 搜索包含"TSLA"的记录
const results = memorySearch.searchByKeyword('TSLA', {
  category: 'session',
  limit: 10
});

console.log(results);
```

**返回结果：**
```javascript
[
  {
    record_id: "uuid",
    category: "session",
    summary: "用户查询 TSLA 股价",
    timestamp: 1234567890,
    token_cost: 25
  },
  // ...
]
```

---

### 2. 时间范围搜索

```javascript
// 搜索最近 1 小时的记录
const oneHourAgo = Math.floor(Date.now() / 1000) - 3600;
const now = Math.floor(Date.now() / 1000);

const results = memorySearch.searchByTimeRange({
  start: oneHourAgo,
  end: now
}, {
  session_id: 'session_001',
  limit: 20
});

console.log(results);
```

---

### 3. 标签搜索

```javascript
// 搜索包含特定标签的记录
const results = memorySearch.searchByTags(['stock', 'query'], {
  limit: 10
});

console.log(results);
```

---

### 4. 会话搜索

```javascript
// 获取完整会话记录
const session = memorySearch.searchBySession('session_001', {
  includeDetails: true // 包含 L2 详情
});

console.log(`L0: ${session.l0.length} 条`);
console.log(`L1: ${session.l1.length} 条`);
console.log(`L2: ${session.l2.length} 条`);
```

---

### 5. 高级搜索

```javascript
// 组合搜索
const result = await memorySearch.advancedSearch({
  keyword: '股价',
  category: 'session',
  timeRange: {
    start: oneHourAgo,
    end: now
  },
  includeDetails: true,
  limit: 10
});

console.log(`找到 ${result.count} 条记录`);
console.log(result.results);
```

---

### 6. 获取搜索统计

```javascript
const stats = memorySearch.getStats();

console.log('总记录数:', stats.total_records);
console.log('按分类:', stats.categories);
console.log('按事件类型:', stats.event_types);
console.log('最近活动:', stats.recent_activity);
```

**返回结果：**
```javascript
{
  total_records: {
    l0: 100,
    l1: 80,
    l2: 50
  },
  categories: [
    { category: 'session', count: 50 },
    { category: 'tool', count: 30 },
    { category: 'memory', count: 20 }
  ],
  event_types: [
    { event_type: 'tool.call', count: 40 },
    { event_type: 'session.start', count: 20 }
  ],
  recent_activity: [
    { event_type: 'tool.call', timestamp: 1234567890 },
    // ...
  ]
}
```

---

## 搜索性能

| 搜索类型 | 速度 | Token 消耗 |
|---------|------|-----------|
| **关键词搜索** | < 10ms | 极低 |
| **时间范围搜索** | < 50ms | 低 |
| **标签搜索** | < 50ms | 低 |
| **会话搜索** | < 100ms | 中 |
| **高级搜索** | < 100ms | 中 - 高 |

---

## 最佳实践

### 1. 优先使用 L0 搜索

```javascript
// ✅ 推荐：先搜索 L0 索引
const l0Results = memorySearch.searchByKeyword('keyword');

// 然后按需加载 L1/L2
if (l0Results.length > 0) {
  const details = memorySearch.advancedSearch({
    includeDetails: true
  });
}
```

### 2. 使用时间范围限制

```javascript
// ✅ 推荐：限制时间范围
const results = memorySearch.searchByTimeRange({
  start: Date.now() / 1000 - 3600, // 最近 1 小时
  end: Date.now() / 1000
});
```

### 3. 合理使用 includeDetails

```javascript
// ✅ 推荐：仅在需要时加载 L2 详情
const result = memorySearch.advancedSearch({
  keyword: 'query',
  includeDetails: false // 默认 false
});

// 仅当需要详情时才加载
if (needDetails) {
  const l2 = clawMem.getL2(result.results[0].record_id);
}
```

---

## API 参考

### `searchByKeyword(keyword, options)`

**参数：**
- `keyword` (string) - 搜索关键词
- `options.category` (string) - 分类过滤
- `options.timeRange` (object) - 时间范围 `{start, end}`
- `options.limit` (number) - 结果数量限制

**返回：** Array - 搜索结果列表

---

### `searchByTimeRange(timeRange, options)`

**参数：**
- `timeRange` (object) - 时间范围 `{start, end}`
- `options.session_id` (string) - 会话 ID
- `options.event_type` (string) - 事件类型
- `options.limit` (number) - 结果数量限制

**返回：** Array - 搜索结果列表

---

### `searchByTags(tags, options)`

**参数：**
- `tags` (Array) - 标签列表
- `options.limit` (number) - 结果数量限制

**返回：** Array - 搜索结果列表（去重）

---

### `searchBySession(sessionId, options)`

**参数：**
- `sessionId` (string) - 会话 ID
- `options.includeDetails` (boolean) - 是否包含 L2 详情

**返回：** Object - 完整会话记录

---

### `advancedSearch(query)`

**参数：**
- `query.keyword` (string) - 关键词
- `query.category` (string) - 分类
- `query.tags` (Array) - 标签列表
- `query.session_id` (string) - 会话 ID
- `query.timeRange` (object) - 时间范围
- `query.event_type` (string) - 事件类型
- `query.includeDetails` (boolean) - 是否包含 L2 详情
- `query.limit` (number) - 结果数量限制

**返回：** Object - 搜索结果

---

### `getStats()`

**参数：** 无

**返回：** Object - 搜索统计信息

---

## 示例场景

### 场景 1: 查找最近的股票查询

```javascript
const oneHourAgo = Math.floor(Date.now() / 1000) - 3600;

const stocks = memorySearch.advancedSearch({
  keyword: '股价',
  timeRange: {
    start: oneHourAgo,
    end: Date.now() / 1000
  },
  limit: 5
});

console.log(`最近查询的股票：${stocks.count} 次`);
```

### 场景 2: 回顾完整会话

```javascript
const session = memorySearch.searchBySession('session_001', {
  includeDetails: true
});

// 重放会话
session.l1.forEach(record => {
  console.log(`${new Date(record.timestamp * 1000).toLocaleString()}: ${record.semantic_summary}`);
});
```

### 场景 3: 分析工具使用情况

```javascript
const stats = memorySearch.getStats();

console.log('工具调用统计:');
stats.event_types
  .filter(e => e.event_type === 'tool.call')
  .forEach(e => console.log(`  ${e.count} 次`));
```

---

**Happy Searching! 🔍**
