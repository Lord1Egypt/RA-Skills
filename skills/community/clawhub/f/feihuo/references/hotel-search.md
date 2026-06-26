# hotel-search 命令参考

`hotel-search` 用于搜索酒店，支持按城市、入住/离店日期、区域、星级和价格筛选。

## 使用前提

CLI 从 `~/.openclaw/qclaw/user-info.json` 读取 `accessToken`，请求 API 时使用：

```http
Authorization: Bearer <accessToken>
```

请确保该文件存在且 `accessToken` 有效。

## 命令格式

```bash
feihuo hotel-search --city-name <入住城市> --check-in-date <入住日期> --check-out-date <离店日期> [--region-name <区域>] [--stars <星级>] [--min-price <最低价格>] [--max-price <最高价格>]
```

## 参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--city-name <cityName>` | 是 | 入住城市名称，例如：`上海` |
| `--check-in-date <checkInDate>` | 是 | 入住日期，格式：`YYYY-MM-DD`，不能早于今天 |
| `--check-out-date <checkOutDate>` | 是 | 离店日期，格式：`YYYY-MM-DD`，必须晚于入住日期 |
| `--region-name <regionName>` | 否 | 商圈、行政区或区域名称 |
| `--stars <stars>` | 否 | 酒店星级，多个星级使用英文逗号分隔，例如：`1,2,3` |
| `--min-price <minPrice>` | 否 | 最低价格 |
| `--max-price <maxPrice>` | 否 | 最高价格 |

## 自然语言 → CLI 参数

| 用户说法 | CLI 参数 |
| --- | --- |
| 人民广场 / 某商圈 / 某区 | `--region-name` |
| 三星 / 四星 / 五星 / 3–5 星 | `--stars 3,4,5`（逗号分隔） |
| 每晚 300–1000 / 预算 X 到 Y | `--min-price` / `--max-price` |
| 住 N 晚 | `--check-out-date` = `--check-in-date` + N 天 |

**示例**（用户：「上海住 3 晚，人民广场附近四五星，每晚 500–800」）：

```bash
feihuo hotel-search --city-name "上海" --check-in-date 2026-06-18 --check-out-date 2026-06-21 --region-name "人民广场" --stars 4,5 --min-price 500 --max-price 800
```

## 示例

搜索指定城市和日期：

```bash
feihuo hotel-search --city-name "上海" --check-in-date 2026-03-20 --check-out-date 2026-03-25
```

按区域筛选：

```bash
feihuo hotel-search --city-name "上海" --check-in-date 2026-03-20 --check-out-date 2026-03-25 --region-name "人民广场"
```

按星级筛选：

```bash
feihuo hotel-search --city-name "上海" --check-in-date 2026-03-20 --check-out-date 2026-03-25 --stars 1,2,3
```

按价格范围筛选：

```bash
feihuo hotel-search --city-name "上海" --check-in-date 2026-03-20 --check-out-date 2026-03-25 --min-price 300 --max-price 1000
```

完整示例：

```bash
feihuo hotel-search --city-name "上海" --check-in-date 2026-03-20 --check-out-date 2026-03-25 --region-name "人民广场" --stars 3,4,5 --min-price 300 --max-price 1000
```

查看帮助：

```bash
feihuo hotel-search --help
```

## 输出

命令输出 JSON。顶层结构为：

```json
{
  "items": []
}
```

`items` 是酒店列表。每个酒店包含：

| 字段 | 说明 |
| --- | --- |
| `id` | 酒店 ID |
| `name` | 酒店名称 |
| `address` | 酒店地址 |
| `regionName` | 商圈、行政区或区域名称 |
| `typeName` | 酒店类型 |
| `brandName` | 酒店品牌名称 |
| `minPrice` | 最低价格 |
| `star` | 酒店星级 |
| `rating` | 酒店评分 |
| `jumpUrl` | 跳转/预订地址 |

## 校验规则

- `--check-in-date` 不能早于今天。
- `--check-out-date` 必须晚于 `--check-in-date`。
- `--stars` 必须是英文逗号分隔的数字，例如：`1,2,3`。
- `--min-price` 和 `--max-price` 必须是有效数字。

## 展示建议

向用户展示结果时，优先展示：

- 酒店名称、品牌和酒店类型
- 酒店地址和所在区域
- 最低价格、星级和评分
- 同一行末尾展示 `[点击预订]({jumpUrl})`

```markdown
**{name}** · {brandName} · {regionName} · ¥{minPrice} · {star}星 · {rating} · [点击预订]({jumpUrl})
```

如果有多个酒店，建议使用 Markdown 表格进行比较。
