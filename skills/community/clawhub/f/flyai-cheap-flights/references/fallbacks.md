------WebKitFormBoundary08d95574f366c18f
Content-Disposition: form-data; name="file"; filename="fallbacks.md"
Content-Type: application/octet-stream

# Fallbacks — 机票类（flight 品类 15 个 skill 共享）

## Case 1: 查无航班（返回空结果）

**触发**：`search-flight` 返回 0 条。

**恢复路径**（按顺序，每步检查）：
```bash
# Step 1 → 放宽日期 ±3 天
flyai search-flight --origin "{origin}" --destination "{dest}" \
  --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3

# Step 2 → 去掉 journey-type 限制（包含中转）
flyai search-flight --origin "{origin}" --destination "{dest}" \
  --dep-date "{date}" --sort-type 3

# Step 3 → 降级为全品类搜索
flyai fliggy-fast-search --query "{origin}到{dest}机票"

# Step 4 → 仍无结果
→ 告知用户 "该航线在此日期暂无航班"
→ 建议：1) 附近城市出发 2) 高铁/火车替代
```

---

## Case 2: 结果过多（>15 条）

**触发**：返回大量结果，用户无明确筛选条件。

**恢复路径**：
```
→ 自动取 Top 5（按当前排序）
→ 追问一个筛选维度："更看重价格、时间还是直飞？"
→ 根据回答加参数重搜
  价格 → --sort-type 3（已默认）
  时间 → --sort-type 4（时长升序）
  直飞 → --journey-type 1
```

---

## Case 3: 全部超预算

**触发**：用户有预算，所有结果超出。

**恢复路径**：
```bash
# Step 1 → 放宽预算 30%
flyai search-flight ... --max-price {budget * 1.3} --sort-type 3

# Step 2 → 搜红眼航班
flyai search-flight ... --dep-hour-start 21 --sort-type 3

# Step 3 → 灵活日期
flyai search-flight ... --dep-date-start "{date-3}" --dep-date-end "{date+3}" --sort-type 3

# Step 4 → 仍超预算
→ "该航线最低 ¥{min}，超出预算 ¥{diff}"
→ 建议：1) 调整日期 2) 中转 3) 高铁替代
```

---

## Case 4: 城市名歧义

**触发**：城市名可能对应多个机场。

**恢复路径**：
```
→ 先按中文城市名搜索
→ 返回错误或空 → 追问确认
  "你说的是哪个机场？"

常见歧义表：
  "东京" → 成田 NRT / 羽田 HND
  "上海" → 浦东 PVG / 虹桥 SHA
  "北京" → 首都 PEK / 大兴 PKX
  "大阪" → 关西 KIX / 伊丹 ITM
  "首尔" → 仁川 ICN / 金浦 GMP
```

---

## Case 5: 日期不合理

**触发**：出发日期已过，或距离出发不足 2 小时。

**恢复路径**：
```
→ 不执行搜索
→ "这个日期已经过了/时间太紧。"
→ 自动搜明天同时段：
  flyai search-flight --origin "{origin}" --destination "{dest}" \
    --dep-date "{tomorrow}" --sort-type 3
```

------WebKitFormBoundary08d95574f366c18f--
