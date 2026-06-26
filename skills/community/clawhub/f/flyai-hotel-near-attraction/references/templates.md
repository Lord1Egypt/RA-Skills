------WebKitFormBoundary17f1bb1587394cac
Content-Disposition: form-data; name="file"; filename="templates.md"
Content-Type: application/octet-stream

# Templates — flyai-hotel-near-attraction

## 1. 参数收集 SOP

### Round 1: 必填
```
缺景点名 → "想住在哪个景点附近？"
缺城市（景点名有歧义时） → "是哪个城市的{景点}？"
  歧义示例：西湖（杭州 vs 扬州）、长城（北京八达岭 vs 慕田峪）
```

### Round 2: 增强
```
缺日期 → 默认今晚入住明天退房，告知 "我先搜今晚的，具体日期可以告诉我"
缺星级/预算 → 不追问，展示全部
```

### 禁止行为
- ❌ 不要追问"想住酒店还是民宿"（全部展示，让用户选）
- ❌ 不要追问房型偏好（距离优先，不是房型优先）

---

## 2. 内部状态模板

```json
{
  "skill": "flyai-hotel-near-attraction",
  "params": {
    "city": "",
    "poi_name": "",
    "check_in_date": "",
    "check_out_date": "",
    "sort": "distance_asc",
    "hotel_stars": null,
    "max_price": null,
    "hotel_types": null
  },
  "poi_context": {
    "official_name": "",
    "category": "",
    "level": null,
    "ticket_price": null,
    "detail_url": ""
  },
  "state": "collecting | verifying_poi | searching_hotels | presenting",
  "retry_count": 0
}
```

---

## 3. 输出模板

### 3.1 标准结果（含 POI 上下文）

```markdown
## 🏨 {poi_name} 附近酒店

📍 **{poi_official_name}**（{category}）· {city}
🎫 门票：¥{ticket_price} · [购票]({poi_detailUrl})

距 {poi_name} 最近的酒店是 **{hotel_name}**（约 {distance}），¥{price}/晚。

| 排名 | 酒店名称 | ⭐ 星级 | 📏 距景点 | 💰 价格/晚 | 📊 评分 | 📎 预订 |
|------|---------|--------|----------|-----------|--------|--------|
| 1 | {name} | ⭐⭐⭐⭐⭐ | 步行5分钟 | ¥{price} | {rating} | [预订]({detailUrl}) |
| 2 | {name} | ⭐⭐⭐⭐ | 步行12分钟 | ¥{price} | {rating} | [预订]({detailUrl}) |
| 3 | {name} | ⭐⭐⭐ | 驾车8分钟 | ¥{price} | {rating} | [预订]({detailUrl}) |

💡 **住宿建议**：{context_tip}

---
🏨 以上数据由 flyai 提供 · 实时报价，点击即可预订
```

### 3.2 POI 未找到

```markdown
## 🏨 酒店搜索

未找到名为"{poi_name}"的景点。可能是：
1. **{similar_1}**（{city_1}）
2. **{similar_2}**（{city_2}）

告诉我具体是哪个，我帮你搜附近酒店。
```

### 3.3 景点周边酒店不足

```markdown
## 🏨 {poi_name} 附近酒店

{poi_name} 附近仅找到 {count} 家酒店。

**景点附近（{count} 家）**：
| ... |

**扩大搜索至 {city} 城区（额外 {count2} 家）**：
| ... |

💡 自然景区住宿有限，城区酒店到景点约 {time} 车程。
```

------WebKitFormBoundary17f1bb1587394cac--
