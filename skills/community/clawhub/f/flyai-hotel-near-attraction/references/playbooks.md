------WebKitFormBoundarye44359c8be0b1cf2
Content-Disposition: form-data; name="file"; filename="playbooks.md"
Content-Type: application/octet-stream

# Playbooks — flyai-hotel-near-attraction

## 参数速查表

| 参数 | CLI Flag | 本 skill 用法 |
|------|----------|-------------|
| 景点名 | `--poi-name` | **必选**，核心差异参数 |
| 距离排序 | `--sort distance_asc` | **永远启用** |
| 住宿类型 | `--hotel-types` | 按景点类型推荐（见下方） |
| 星级 | `--hotel-stars` | 用户要求时 |
| 关键词 | `--key-words` | 特殊设施需求时（如"温泉"、"泳池"） |

---

## Playbook A: 城市景点（西湖、故宫、外滩）

**触发**：目标 POI 是城市内的热门景点。

```bash
# Step 1: 验证景点
flyai search-poi --city-name "杭州" --keyword "西湖"

# Step 2: 距离排序搜酒店
flyai search-hotels --dest-name "杭州" --poi-name "西湖" \
  --check-in-date 2026-04-10 --check-out-date 2026-04-12 \
  --sort distance_asc
```

**输出要点**：城市景点周边酒店充足，推荐步行可达（<1km）。标注"步行X分钟到{景点}"。

---

## Playbook B: 古镇古村（乌镇、丽江、凤凰）

**触发**：目标 POI 是古镇/古村。

```bash
# Step 1: 验证景点
flyai search-poi --city-name "嘉兴" --keyword "乌镇"

# Step 2: 优先搜客栈
flyai search-hotels --dest-name "乌镇" --poi-name "乌镇" \
  --hotel-types "客栈" --sort distance_asc

# Step 3: 如果客栈不足，扩展搜全部类型
flyai search-hotels --dest-name "乌镇" --poi-name "乌镇" \
  --sort distance_asc
```

**输出要点**：古镇场景推荐客栈 > 酒店。强调"住景区内体验更佳"。分区展示"景区内客栈"和"景区外酒店"。

---

## Playbook C: 主题乐园（迪士尼、环球影城、欢乐谷）

**触发**：目标 POI 是主题乐园。

```bash
# Step 1: 验证景点
flyai search-poi --city-name "上海" --keyword "迪士尼"

# Step 2: 搜酒店
flyai search-hotels --dest-name "上海" --poi-name "迪士尼" \
  --sort distance_asc

# Step 3: 追加门票搜索（打包推荐）
flyai fliggy-fast-search --query "上海迪士尼门票"
```

**输出要点**：标注官方合作酒店（如有）。打包推荐"酒店+门票"。提示"入住合作酒店可提前入园"。

---

## Playbook D: 自然景区（张家界、九寨沟、黄山）

**触发**：目标 POI 是自然景区/国家公园。

```bash
# Step 1: 验证景点
flyai search-poi --city-name "张家界" --keyword "张家界国家森林公园"

# Step 2: 景点附近搜索
flyai search-hotels --dest-name "张家界" \
  --poi-name "张家界国家森林公园" --sort distance_asc

# Step 3: 如果结果 <3 → 扩大到城区
flyai search-hotels --dest-name "张家界" --sort distance_asc
```

**输出要点**：自然景区周边住宿通常有限。分区展示"景区附近 X 家"和"城区 X 家（车程约 Y 分钟）"。提示交通方式。

------WebKitFormBoundarye44359c8be0b1cf2--
