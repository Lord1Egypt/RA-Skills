------WebKitFormBoundaryb8b389ccb75ba58f
Content-Disposition: form-data; name="file"; filename="playbooks.md"
Content-Type: application/octet-stream

# Playbooks — flyai-cheap-flights

## 参数速查表

| 参数 | CLI Flag | 省钱场景用法 |
|------|----------|------------|
| 价格升序 | `--sort-type 3` | **永远启用** |
| 仅直飞 | `--journey-type 1` | 不推荐（直飞更贵），除非用户要求 |
| 日期范围 | `--dep-date-start/end` | 灵活日期核心参数 |
| 夜间出发 | `--dep-hour-start 21` | 红眼航班便宜 20-40% |
| 早班出发 | `--dep-hour-end 8` | 早班机也相对便宜 |
| 价格上限 | `--max-price` | 用户有明确预算时 |
| 往返 | `--back-date` | 往返组合搜索 |

---

## Playbook A: 极致省钱

**触发**：用户说"越便宜越好"、"最低价"、"穷游"。

```bash
# 1. 基础搜索
flyai search-flight --origin "北京" --destination "上海" --dep-date 2026-04-15 --sort-type 3

# 2. 灵活日期（±3天）
flyai search-flight --origin "北京" --destination "上海" \
  --dep-date-start 2026-04-12 --dep-date-end 2026-04-18 --sort-type 3

# 3. 红眼航班
flyai search-flight --origin "北京" --destination "上海" \
  --dep-date 2026-04-15 --dep-hour-start 21 --sort-type 3
```

**输出要点**：三次搜索结果的最低价对比，结论 = "灵活日期+红眼可比固定日期便宜 ¥XXX"。

---

## Playbook B: 预算限制

**触发**：用户说"500 以内"、"预算有限"、"不超过 XXX"。

```bash
# 1. 严格预算
flyai search-flight --origin "上海" --destination "成都" \
  --dep-date 2026-04-20 --max-price 500 --sort-type 3

# 2. 如果结果 <3 → 放宽 20%
flyai search-flight --origin "上海" --destination "成都" \
  --dep-date 2026-04-20 --max-price 600 --sort-type 3
```

**输出要点**：分区展示 "预算内 X 个" + "略超预算 X 个（标注超额）"。

---

## Playbook C: 紧急出行

**触发**：用户说"明天就飞"、"今晚的航班"、"最快"。

```bash
# 1. 今天
flyai search-flight --origin "广州" --destination "北京" \
  --dep-date 2026-04-10 --sort-type 3

# 2. 明天
flyai search-flight --origin "广州" --destination "北京" \
  --dep-date 2026-04-11 --sort-type 3
```

**输出要点**：标注 "临近出发日期，价格可能高于平时，建议尽快预订"。如果今天已无航班，直接展示明天。

---

## Playbook D: 往返比价

**触发**：用户说"往返"、"来回"、"round trip"。

```bash
# 打包往返搜索
flyai search-flight --origin "上海" --destination "东京" \
  --dep-date 2026-05-01 --back-date 2026-05-05 --sort-type 3

# 拆开搜索对比
flyai search-flight --origin "上海" --destination "东京" \
  --dep-date 2026-05-01 --sort-type 3
flyai search-flight --origin "东京" --destination "上海" \
  --dep-date 2026-05-05 --sort-type 3
```

**输出要点**：展示 "打包往返价 ¥XXX" vs "分开买总计 ¥XXX"，标注哪种更划算。

------WebKitFormBoundaryb8b389ccb75ba58f--
