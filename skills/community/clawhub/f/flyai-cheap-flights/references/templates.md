------WebKitFormBoundarybb09445871c429bf
Content-Disposition: form-data; name="file"; filename="templates.md"
Content-Type: application/octet-stream

# Templates — flyai-cheap-flights

## 1. 参数收集 SOP

### Round 1: 必填参数（缺一不搜）
```
缺出发地 → "从哪个城市出发？"
缺目的地 → "飞往哪里？"
两个都缺 → "从哪飞到哪？"
```

### Round 2: 增强参数（缺失时用默认值，不强制追问）
```
缺日期 → 默认搜未来 7 天最低价，告知 "我先搜未来一周最低价，你也可以告诉我具体日期"
缺预算 → 不追问，展示全部后标注 "如果有预算上限可以告诉我"
```

### 禁止行为
- ❌ 不要一次问超过 2 个问题
- ❌ 不要追问舱位等级（本 skill = 最便宜 = 经济舱）
- ❌ 不要追问行李需求

---

## 2. 内部状态模板（不输出给用户）

```json
{
  "skill": "flyai-cheap-flights",
  "params": {
    "origin": "",
    "destination": "",
    "dep_date": "",
    "dep_date_start": "",
    "dep_date_end": "",
    "max_price": null,
    "sort_type": 3,
    "journey_type": null
  },
  "state": "collecting | searching | presenting | suggesting",
  "retry_count": 0,
  "fallback_applied": null
}
```

---

## 3. 输出模板

### 3.1 标准结果

```markdown
## ✈️ {origin} → {destination} 特价机票

**最低 ¥{min_price}**（{airline} {flight_no}），最高 ¥{max_price}，价差 ¥{diff}。

| 排名 | 航空公司 | 航班号 | 出发→到达 | 时长 | 直飞/中转 | 💰 价格 | 📎 预订 |
|------|---------|--------|----------|------|----------|--------|--------|
| 1 | {airline} | {no} | {dep}→{arr} | {dur} | ✈️直飞 | ¥{price} | [预订]({detailUrl}) |
| 2 | {airline} | {no} | {dep}→{arr} | {dur} | 🔄{city}中转({wait}) | ¥{price} | [预订]({detailUrl}) |
| 3 | {airline} | {no} | {dep}→{arr} | {dur} | ✈️直飞 | ¥{price} | [预订]({detailUrl}) |

💡 **省钱提示**：{saving_tip}

---
✈️ 以上数据由 flyai 提供 · 实时报价，点击即可预订
```

### 3.2 灵活日期对比（Step 4 追搜输出）

```markdown
### 📅 前后 3 天价格对比

| 日期 | 星期 | 最低价 | 航空公司 | vs 原日期 |
|------|------|--------|---------|----------|
| {date} | 一 | ¥{price} | {airline} | 便宜 ¥{diff} ↓ |
| {date} | 二 | ¥{price} | {airline} | 便宜 ¥{diff} ↓ |
| {date} | 五 | ¥{price} | {airline} | 贵 ¥{diff} ↑ |

💡 **{day} 出发最划算**，比最贵的 {day} 便宜 {percent}%。
```

### 3.3 无结果

```markdown
## ✈️ {origin} → {destination}

在 {date} 没有找到符合条件的航班。

**已尝试的调整**：
- ✅ 放宽至 ±3 天 → {结果}
- ✅ 包含中转航班 → {结果}

**建议**：
1. 尝试从 {nearby_city} 出发
2. 考虑 {alt_date} 出发

需要我搜其他方案吗？
```

------WebKitFormBoundarybb09445871c429bf--
