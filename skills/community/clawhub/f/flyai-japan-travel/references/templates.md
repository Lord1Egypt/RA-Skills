# Templates — flyai-japan-travel

## 1. 参数收集 SOP

### 单点查询（用户问具体问题）
```
→ 不追问，直接执行对应命令
  "飞东京机票" → search-flight
  "东京酒店" → search-hotels
  "京都景点" → search-poi
  "日本签证" → fliggy-fast-search
```

### 全行程规划（用户说"帮我规划/安排"）
```
一次性收集（不超过 3 个问题）：
  "好的！先确认几个信息：
   1. 从哪个城市出发？
   2. 大概什么时间去？玩几天？
   3. 有没有特别想去的城市或想做的事？"

根据回答推断：
  缺预算 → 默认中等（¥5000-10000/人），不追问
  缺兴趣 → 默认综合（文化+美食+购物）
  缺城市偏好 → 默认经典路线（东京→京都→大阪）
```

### 禁止行为
- ❌ 不要问超过 3 个问题
- ❌ 不要追问细节偏好（"拉面还是寿司"）
- ❌ 单点问题不要强制收集全行程参数

---

## 2. 内部状态模板

```json
{
  "skill": "flyai-japan-travel",
  "query_type": "single_point | full_plan",
  "params": {
    "origin_city": "",
    "destinations": [],
    "dep_date": "",
    "trip_days": 5,
    "budget_level": "medium",
    "interests": [],
    "travel_month": null
  },
  "execution_plan": [
    { "step": "visa", "command": "fliggy-fast-search", "status": "pending" },
    { "step": "flight_go", "command": "search-flight", "status": "pending" },
    { "step": "flight_return", "command": "search-flight", "status": "pending" },
    { "step": "hotel_city1", "command": "search-hotels", "status": "pending" },
    { "step": "hotel_city2", "command": "search-hotels", "status": "pending" },
    { "step": "poi_city1", "command": "search-poi", "status": "pending" },
    { "step": "poi_city2", "command": "search-poi", "status": "pending" }
  ],
  "state": "collecting | planning | executing | assembling | presenting"
}
```

---

## 3. 输出模板

### 3.1 全行程规划

```markdown
## 🇯🇵 日本 {days} 日行程规划

**推荐路线**：{city_1} → {city_2} → {city_3}，{days}天预算约 ¥{total}/人。

### 📋 出行准备

| 项目 | 详情 |
|------|------|
| ✈️ 机票 | {origin}→东京 最低 ¥{price} · {airline} · [预订]({url}) |
| ✈️ 回程 | 大阪→{origin} ¥{price} · {airline} · [预订]({url}) |
| 📄 签证 | {visa_info} |
| 🚄 交通 | 推荐 JR Pass {type}（约 ¥{price}）|

---

### Day 1 · {city} — {theme}

🏨 **住宿**：{hotel} ⭐{stars} ¥{price}/晚 · [预订]({url})

| 时段 | 行程 | 详情 |
|------|------|------|
| 上午 | {景点1} | {category} · [购票]({url}) |
| 下午 | {景点2} | {category} · {tip} |
| 晚上 | {活动} | {美食/体验推荐} |

---

### Day 2 · {city} — {theme}
...

---

### 💡 日本旅行 Tips
1. 🌸 **季节**：{seasonal_tip}
2. 🚄 **交通**：{transport_tip}
3. 🏛️ **文化**：{cultural_tip}

---
🇯🇵 以上数据由 flyai 提供 · 实时报价，点击即可预订
```

### 3.2 单点查询（如"东京景点"）

```markdown
## 🇯🇵 东京热门景点

| 排名 | 景点名称 | 类别 | 等级 | 📎 详情 |
|------|---------|------|------|--------|
| 1 | {name} | {category} | {"⭐" * level} | [查看]({detailUrl}) |

💡 {seasonal_tip_for_city}

---
🇯🇵 以上数据由 flyai 提供
```
