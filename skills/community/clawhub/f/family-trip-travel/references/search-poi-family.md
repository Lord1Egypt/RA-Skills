# search-poi · 亲子 / 儿童友好类目

完整参数与 **`--category` 全部合法取值**以终端为准：

```bash
flyai search-poi --help
```

## 使用要点

- **`--category` 必须与 help 中的中文枚举完全一致**（例如是 **`主题乐园`** 而不是「主题公园」）。完整列表见 **`cli-capabilities.md`**。
- **`--keyword`**：缩小到具体园区/馆名（如 `迪士尼`、`长隆`）。
- **`--poi-level`**：`1`～`5`，可用于筛高等级景区（是否更适合亲子仍要结合目的地判断）。

## 亲子向常用 `category`

| 场景 | 建议 `category` |
|------|-----------------|
| 乐园 / 室内游乐 | 主题乐园、公园乐园 |
| 动物 | 动物园、海洋馆 |
| 玩水 | 水上乐园、温泉 |
| 文化 + 室内（雨天备选） | 博物馆、纪念馆、展览馆 |
| 演出（大龄） | 演出赛事、剧院剧场 |
| 轻松户外 | 沙滩海岛、城市观光、文创街区（视年龄与步行量） |

## 示例

```bash
flyai search-poi --city-name "广州" --category "动物园"
flyai search-poi --city-name "上海" --category "主题乐园" --keyword "迪士尼"
flyai search-poi --city-name "杭州" --category "博物馆"
flyai search-poi --city-name "北京" --category "海洋馆"
```

若结果偏成人向或缺少「推车友好」等信息：**再跑** `fliggy-fast-search --query "… 亲子 推车 低龄 …"` 补一轮；CLI 的 POI JSON 若无母婴室等字段，回答中写 **「出行前向场馆/平台确认」**。
