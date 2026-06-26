------WebKitFormBoundary27869650fe2f984a
Content-Disposition: form-data; name="file"; filename="fallbacks.md"
Content-Type: application/octet-stream

# Fallbacks — 酒店类（hotel 品类 20 个 skill 共享）

## Case 1: 景点附近酒店不足（<3 条）

**触发**：`search-hotels --poi-name` 返回少于 3 条结果。常见于自然景区、偏远景点。

**恢复路径**：
```bash
# Step 1 → 去掉 poi-name，改为城市级搜索
flyai search-hotels --dest-name "{city}" \
  --check-in-date "{checkin}" --check-out-date "{checkout}" \
  --sort distance_asc

# Step 2 → 降级为全品类搜索
flyai fliggy-fast-search --query "{city} {poi_name} 附近住宿"

# Step 3 → 仍不足
→ 展示已有结果 + 标注"景区住宿有限"
→ 建议城区酒店并标注车程
```

---

## Case 2: 全部超预算

**触发**：用户有预算上限，所有结果超出。

**恢复路径**：
```bash
# Step 1 → 放宽预算 30%，标注"略超预算"
flyai search-hotels --dest-name "{city}" --poi-name "{poi}" \
  --max-price {budget * 1.3} --sort distance_asc

# Step 2 → 搜索民宿/客栈（通常更便宜）
flyai search-hotels --dest-name "{city}" --poi-name "{poi}" \
  --hotel-types "民宿" --sort price_asc

# Step 3 → 扩大搜索范围到城区
flyai search-hotels --dest-name "{city}" --max-price {budget} --sort price_asc

# Step 4 → 仍超预算
→ "景点附近最低 ¥{min}/晚，超预算 ¥{diff}"
→ 建议距景点较远但更便宜的区域
```

---

## Case 3: 日期不可用（满房或特殊日期）

**触发**：热门日期（节假日/樱花季/黄金周）大面积满房。

**恢复路径**：
```bash
# Step 1 → 前后调 1 天
flyai search-hotels --dest-name "{city}" --poi-name "{poi}" \
  --check-in-date "{checkin+1}" --check-out-date "{checkout+1}" \
  --sort distance_asc

# Step 2 → 去掉 poi 限制，搜城区
flyai search-hotels --dest-name "{city}" \
  --check-in-date "{checkin}" --check-out-date "{checkout}" \
  --sort price_asc

# Step 3 → 仍无房
→ "该日期 {city} 酒店紧张（可能是节假日/旅游旺季）"
→ 建议：1) 调整日期 2) 周边城市
```

---

## Case 4: POI 不存在（景点名无法匹配）

**触发**：`search-poi --keyword "{poi}"` 返回空，景点名拼写错误或不在数据库中。

**恢复路径**：
```bash
# Step 1 → 模糊搜索（去掉精确 keyword，用 category）
flyai search-poi --city-name "{city}" --category "{inferred_category}"

# Step 2 → 全品类搜索
flyai fliggy-fast-search --query "{city} {poi_name}"

# Step 3 → 仍未找到
→ "未找到名为 {poi_name} 的景点"
→ 展示该城市的热门景点列表供选择
→ "你是不是在找：1. {similar_1} 2. {similar_2}"
```

---

## Case 5: 城市名歧义

**触发**：用户说的城市可能对应多个地区。

**恢复路径**：
```
常见歧义：
  "西湖" → 杭州西湖 / 扬州瘦西湖 / 惠州西湖
  "长城" → 八达岭 / 慕田峪 / 金山岭 / 司马台
  "迪士尼" → 上海 / 香港
  "环球影城" → 北京 / 大阪

→ 追问确认："你说的是{选项A}还是{选项B}？"
→ 确认后重新执行 Step 2
```

------WebKitFormBoundary27869650fe2f984a--
