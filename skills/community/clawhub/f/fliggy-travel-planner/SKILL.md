---
name: fliggy-travel-planner
description: Travel itinerary planning skill that automates end-to-end trip research and booking assistance. It searches Xiaohongshu (RedNote) for destination guides, extracts key travel insights (dates, itinerary, attractions), queries Fliggy for the cheapest flights, fetches weather forecasts, and compiles everything into a comprehensive trip report with budget breakdown. Optimized for 3-4 min execution via parallel queries and smart caching.
---

# 飞猪旅游攻略规划技能 v2.0（性能优化版）

自动从小红书获取旅游攻略，并整合飞猪机票信息，生成完整的行程规划！

**⚡ 性能优化：** 真正并行查询 + 数据缓存 + 精简提取，耗时从 9 分钟降至 3-4 分钟！

---

## 🔗 技能依赖

### 1. weather skill（天气查询）
**依赖原因：** 获取目的地天气预报

**使用场景：**
- 出行日期在未来 3 天内 → 使用 weather skill 查询真实天气
- 出行日期在未来 3 天后 → 使用气候数据估算，并标注"基于气候数据估算"

**调用方式：**
```bash
curl -s "wttr.in/{城市名}?format=j1"
```

### 2. flight-price-comparison skill（机票查询）
**依赖原因：** 查询飞猪机票价格

---

## ⚡ 性能优化 v2.0

### 优化后执行流程（目标：3-4 分钟）

```
用户输入："4.3 杭州到大理 4 天 3 晚攻略"
     ↓
t=0s    真正并行发起 3 个查询
        ├─ browser.open("小红书", 60 秒超时)
        ├─ exec("curl wttr.in/大理", 10 秒超时)
        └─ browser.open("飞猪", 60 秒超时)
     ↓
t=10s   天气查询完成 ✅
     ↓
t=60s   页面打开完成，并行 snapshot（30 秒）
     ↓
t=90s   数据抓取完成
     ↓
t=120s  精简数据提取（只取 5 个核心字段，30 秒）
     ↓
t=180s  生成行程文档（60 秒）
     ↓
✅ 完成！总计约 3 分钟
```

### 核心优化点

| 优化点 | 优化前 | 优化后 | 节省 |
|--------|--------|--------|------|
| 查询方式 | 串行执行 | 真正并行 | 2-3 分钟 |
| Snapshot | 完整 DOM（3000+ 元素） | 精准提取关键元素 | 1 分钟 |
| 天气查询 | 每次 API | 优先缓存 | 10-30 秒 |
| 数据提取 | 20+ 字段 | 5 个核心字段 | 20-30 秒 |
| **总计** | **~9 分钟** | **~3-4 分钟** | **60%+** |

### 并行查询实现（真正并行）

```javascript
// ✅ 正确做法：真正并行发起
const [xiaohongshuTab, weatherData, fliggyTab] = await Promise.all([
  browser.open({ 
    url: "https://www.xiaohongshu.com/search_result?keyword={目的地} 旅游攻略",
    timeoutMs: 60000
  }),
  exec({ 
    command: 'curl -s "wttr.in/{城市名}?format=j1"',
    timeout: 10
  }),
  browser.open({ 
    url: "https://sjipiao.fliggy.com/flight_search_result.htm?tripType=1&depCity={出发地}&arrCity={目的地}&depDate={日期}",
    timeoutMs: 60000
  })
])

// 并行抓取数据
const [xiaohongshuData, fliggyData] = await Promise.all([
  browser.snapshot({ targetId: xiaohongshuTab.targetId, refs: "aria", timeoutMs: 30000 }),
  browser.snapshot({ targetId: fliggyTab.targetId, refs: "aria", timeoutMs: 30000 })
])
```

### 数据缓存策略

**可缓存的数据：**

```javascript
const CACHE = {
  // 气候数据（季节性，基本固定）
  weather: {
    "大理_春季": { temp: "8-22℃", weather: "晴到多云", tips: "紫外线强，带防晒" },
    "北京_春季": { temp: "10-20℃", weather: "多云", tips: "防风沙" },
    "三亚_春季": { temp: "22-30℃", weather: "晴朗", tips: "带泳衣" },
  },
  
  // 高铁价格（相对固定）
  trains: {
    "杭州 - 北京": { time: "4.5-6 小时", price: "¥550-650" },
    "杭州 - 大理": { time: "无直达，昆明中转", price: "¥550-650" },
  }
}
```

### 精简数据提取（只取核心字段）

**优化后 Prompt（30 秒完成）：**
```
只提取 5 个核心信息：
1. 行程天数（如"4 天 3 晚"）
2. 必去景点 Top3（数组）
3. 住宿推荐区域
4. 人均预算范围（不含机票）
5. 最佳季节
```

---

## 🚀 快速开始

### 使用示例

```
# 简单查询
帮我规划一下去大理的旅行，看下小红书的攻略和机票价格

# 指定日期
查一下 3 月 20 日去三亚的攻略，顺便看看机票多少钱

# 往返行程
计划 4 月 1 日 -4 月 5 日去日本旅游，帮我找攻略和机票
```

---

## 📋 核心流程

### 1️⃣ 小红书攻略搜索
- 搜索目的地相关攻略
- 提取高互动内容（点赞/收藏>平均值）
- 解析攻略关键信息

### 2️⃣ 信息结构化处理
使用大模型提取核心数据（5 个字段）

### 3️⃣ 飞猪机票查询
- 查询往返机票价格
- 提取最低价航班信息

### 4️⃣ 生成整合报告
输出完整行程规划

---

## 📝 行程输出标准格式

### 必须包含的内容（按顺序）

```markdown
## ✅ 行程规划完成

### 🚄 交通推荐

| 方式 | 时间 | 价格 | 推荐 |
|------|------|------|------|
| [方式 1](链接) | X 小时 | ¥XXX | ⭐推荐 |
| [方式 2](链接) | X 小时 | ¥XXX | 备选 |

### 🗓️ 行程亮点

- **Day 1:** ...
- **Day 2:** ...
- ...

### 🌤️ 天气预报

| 日期 | 天气 | 温度 |
|------|------|------|
| X 月 X 日 | 晴/多云 | XX-XX℃ |

### 💰 总预算

| 类别 | 费用 | 说明 |
|------|------|------|
| 交通 | ¥XXX | 高铁/机票往返 |
| 酒店 | ¥XXX | X 晚住宿 |
| 门票 | ¥XXX | 景点门票 |
| 餐饮 | ¥XXX | X 天餐费 |
| 其他 | ¥XXX | 应急备用 |
| **总计** | **¥XXX** | 经济型 |

### 📖 小红书攻略来源

[查看小红书原文](链接)（XX 赞）
```

---

## ⚠️ 注意事项

1. **并行查询：** 必须同时发起所有查询，不要串行
2. **超时控制：** 所有网络请求设置超时（browser 60 秒，curl 10 秒）
3. **缓存优先：** 天气/高铁价格优先查缓存
4. **精简提取：** 只取 5 个核心字段，不要贪多
5. **小红书链接格式：** 必须返回 `/explore/{noteId}` 格式的真实笔记链接，不要返回 `/search_result/{id}` 链接（会显示"安全限制"）

---

## 🔧 故障排查

**Q1: 执行时间超过 5 分钟**
- 检查是否真正并行执行（用 Promise.all）
- 检查 snapshot 是否设置了 timeoutMs
- 检查是否在使用完整 DOM 抓取

**Q2: 数据提取不准确**
- 增加参考笔记数量到前 5 篇
- 检查 Prompt 是否过于复杂

**Q3: 小红书链接打不开（显示"安全限制"）**
- 原因：返回了 `/search_result/{id}` 链接
- 解决：从 snapshot 中提取笔记卡片的真实链接（`/explore/{noteId}` 格式）
- 正确示例：`https://www.xiaohongshu.com/explore/69b01f9500000000150236a9`
- 错误示例：`https://www.xiaohongshu.com/search_result/69b01f9500000000150236a9` ❌

---

**版本：** v2.0（性能优化版）  
**最后更新：** 2026-03-16  
**维护者：** Luna 🌙  
**性能目标：** 3-4 分钟完成行程规划
