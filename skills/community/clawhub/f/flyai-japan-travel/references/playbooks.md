# Playbooks — flyai-japan-travel

## 路线速查

| 路线 | 天数 | 城市 | 适合 |
|------|------|------|------|
| 东京深度 | 3-4 天 | 东京 | 首次赴日、购物 |
| 关西经典 | 4-5 天 | 大阪→京都→奈良 | 文化爱好者 |
| 东京+关西 | 5-7 天 | 东京→京都→大阪 | **最热门** |
| 北海道深度 | 5-7 天 | 札幌→小樽→富良野 | 自然/冬季 |
| 冲绳海岛 | 3-5 天 | 那霸→离岛 | 海岛度假 |

## 季节速查

| 月份 | 亮点 | 注意 |
|------|------|------|
| 3-4 月 | 🌸 樱花（东京3月底，京都4月初） | 酒店翻倍，提前2个月订 |
| 7-8 月 | 🎆 花火大会、夏祭 | 极热+台风 |
| 10-12 月 | 🍁 红叶（京都11月底最佳） | 11月京都酒店紧张 |
| 1-2 月 | ⛷️ 北海道滑雪、札幌雪祭 | 防寒装备 |

---

## Playbook A: 经典 5 天（东京→京都→大阪）

**触发**：用户首次赴日 / 无明确偏好 / 说"经典路线"。

```bash
# 签证
flyai fliggy-fast-search --query "日本旅游签证"

# 机票
flyai search-flight --origin "{出发}" --destination "东京" --dep-date "{day1}" --sort-type 3
flyai search-flight --origin "大阪" --destination "{出发}" --dep-date "{day5}" --sort-type 3

# 酒店
flyai search-hotels --dest-name "东京" --check-in-date "{day1}" --check-out-date "{day3}" --sort rate_desc
flyai search-hotels --dest-name "京都" --check-in-date "{day3}" --check-out-date "{day4}" --sort rate_desc
flyai search-hotels --dest-name "大阪" --check-in-date "{day4}" --check-out-date "{day5}" --sort rate_desc

# 景点
flyai search-poi --city-name "东京" --poi-level 5
flyai search-poi --city-name "京都" --category "宗教场所"
flyai search-poi --city-name "大阪" --category "市集"
```

**Day-by-Day**：
- Day 1-2: 东京（浅草寺→秋叶原→涩谷→新宿）
- Day 3: 新干线到京都（伏见稻荷→清水寺→祇园）
- Day 4: 京都→大阪（金阁寺→嵯峨野→道顿堀）
- Day 5: 大阪（大阪城→黑门市场）→回程

---

## Playbook B: 樱花季专题

**触发**：用户提到"樱花"、"cherry blossom"、或 3-4 月出行。

```bash
# 灵活日期机票
flyai search-flight --origin "{出发}" --destination "东京" \
  --dep-date-start "2026-03-25" --dep-date-end "2026-04-05" --sort-type 3

# 樱花景点
flyai search-poi --city-name "东京" --keyword "樱花"
flyai search-poi --city-name "京都" --keyword "樱花"

# 酒店（樱花季价格高，提前告知）
flyai search-hotels --dest-name "东京" \
  --check-in-date "2026-03-28" --check-out-date "2026-04-02" --sort rate_desc
```

**特别提示**：樱花季酒店 1.5-2 倍价格，建议提前 2 个月订。东京→京都花期差约 1 周，可以追着樱花前线走。

---

## Playbook C: 穷游日本

**触发**：用户说"省钱"、"穷游"、"budget"、"预算有限"。

```bash
# 飞关西（通常比东京便宜）
flyai search-flight --origin "{出发}" --destination "大阪" --dep-date "{date}" --sort-type 3

# 经济酒店
flyai search-hotels --dest-name "大阪" --max-price 400 --sort price_asc
flyai search-hotels --dest-name "京都" --max-price 400 --sort price_asc

# 免费/低价景点
flyai search-poi --city-name "京都" --category "宗教场所"
```

**省钱核心**：
- 飞关西 > 成田（省 ¥300-500）
- 住大阪 > 京都（便宜 30%+，新干线 15min 到京都）
- 京都寺庙多数免费或 ¥20-50
- JR Pass 7 日券约 ¥1500，多城市必买

---

## Playbook D: 北海道冬季（滑雪+温泉）

**触发**：用户提到"北海道"、"滑雪"、"雪"、或 12-2 月出行。

```bash
# 机票
flyai search-flight --origin "{出发}" --destination "札幌" --dep-date "{date}" --sort-type 3

# 滑雪场
flyai search-poi --city-name "札幌" --category "滑雪"

# 温泉酒店
flyai search-hotels --dest-name "登别" --key-words "温泉" --sort rate_desc

# 雪祭
flyai fliggy-fast-search --query "札幌雪祭 {year}"
```

**特别提示**：12-2 月需厚羽绒服+防滑靴。滑雪装备可现场租。推荐 Day 1-3 札幌/小樽 + Day 4-5 登别温泉。
