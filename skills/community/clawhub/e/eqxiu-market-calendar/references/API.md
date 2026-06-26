# API 参考

## 当前日期

```
GET https://msearch-api.eqxiu.com/yyyymm
```

- 响应：纯文本 `yyyy-MM-dd`
- 用途：避免 Agent 自行推断「今天」

## 月度节日

```
GET https://msearch-api.eqxiu.com/m/holiday/queryByMonth?year={YYYY}&month={MM}
```

- 响应：JSON，`success` 为 true 时节日在 `list` 数组
- `month` 使用两位数字（如 `06`）

### 主要字段

| 字段 | 含义 |
|------|------|
| `id` | 节日 ID（去重用） |
| `name` | 节日名称 |
| `searchWord` | 商城主搜索词（CLI 优先使用） |
| `keywords` | 备用关键词，`|` 分隔 |
| `startDate` / `endDate` | 节日起止日 `yyyy-MM-dd` |
| `promotStartDate` | 建议开始推广日 |
| `level` | 1=高优先级，2=中，3=低 |

## 模板商城链接

```
https://www.eqxiu.com/mall/search?keywords={urlencode(search_term)}
```

`search_term` 规则：优先 `searchWord`；为空则取 `keywords` 按 `|` 拆分后的第一个；仍为空则用 `name`。

## CLI 过滤规则

- 仅返回 **未来节日**：`startDate >= today`（`today` 来自 `/yyyymm`）
- `list --year --month` 不能指定早于今天的月份
- `upcoming --days N`：`today <= startDate <= today + N`
