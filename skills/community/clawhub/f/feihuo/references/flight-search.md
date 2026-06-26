# flight-search 命令参考

`flight-search` 用于搜索航班，支持单程和往返查询。

## 使用前提

CLI 从 `~/.openclaw/qclaw/user-info.json` 读取 `accessToken`，请求 API 时使用：

```http
Authorization: Bearer <accessToken>
```

请确保该文件存在且 `accessToken` 有效。

## 命令格式

```bash
feihuo flight-search --dep <出发地> --arr <到达地> --dep-date <出发日期> [--back-date <返程日期>] [--berth-type <舱位等级>] [--airlines <航司>] [--aircraft-type <机型>] [--baggage-piece-require <行李>] [--min-price <最低价>] [--max-price <最高价>]
```

## 参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--dep <dep>` | 是 | 出发地，可以是城市或机场名称，例如：`上海` |
| `--arr <arr>` | 是 | 到达地，可以是城市或机场名称，例如：`东京` |
| `--dep-date <depDate>` | 是 | 出发日期，格式：`YYYY-MM-DD`，不能早于今天 |
| `--back-date <backDate>` | 否 | 返程日期，格式：`YYYY-MM-DD`，不能早于出发日期 |
| `--berth-type <berthType>` | 否 | 舱位等级：`Y` 经济舱，`C` 公务舱，`F` 头等舱 |
| `--airlines <airlines>` | 否 | 指定航司，英文逗号分隔的 IATA 二字码，例如：`CA,MU` |
| `--aircraft-type <aircraftType>` | 否 | 机型标签喜好：`large` 大型机，`medium` 中型机，`small` 小型机，`lowCarbon` 低碳 |
| `--baggage-piece-require <baggagePieceRequire>` | 否 | 行李要求：`0`/`zero` 无行李，`1`/`one` 1件，`2`/`two` 2件，`3`/`three` 3件，`4`/`four` 4件 |
| `--min-price <minPrice>` | 否 | 价格范围最小值 |
| `--max-price <maxPrice>` | 否 | 价格范围最大值，不能小于 `--min-price` |

## 自然语言 → CLI 参数

用户口语中的条件**必须**映射为下列参数传给 CLI，**不要**拿到 JSON 后再按价格/舱位等自行过滤。

| 用户说法 | CLI 参数 |
| --- | --- |
| 往返 / 来回 / N 天后回 / 住 N 天回来 | `--back-date`（= 出发日 + N 天；或用户指定的返程日） |
| 下周四 / 明天 / 后天 | `--dep-date`（先 `date +%Y-%m-%d` 换算为 `YYYY-MM-DD`） |
| 经济舱 / 公务舱 / 头等舱 | `--berth-type Y` / `C` / `F` |
| 价格 2000–4000 / 预算 X 到 Y / 不超过 Z 元 | `--min-price 2000 --max-price 4000`（仅上限则只传 `--max-price`） |
| 国航+东航 / 指定航司 | `--airlines CA,MU`（IATA 二字码，逗号分隔） |
| 大型机 / 中型机 / 小型机 / 低碳 | `--aircraft-type large` / `medium` / `small` / `lowCarbon` |
| 带 1 件行李 / 无行李 | `--baggage-piece-require one` / `zero`（也支持 0–4 或 zero–four） |

**完整示例**（用户：「下周四广州到东京往返，3 天后回，价格 2000–4000」）：

```bash
feihuo flight-search --dep "广州" --arr "东京" --dep-date 2026-06-18 --back-date 2026-06-21 --min-price 2000 --max-price 4000
```

## 示例

单程：

```bash
feihuo flight-search --dep "上海" --arr "东京" --dep-date 2026-03-20
```

往返：

```bash
feihuo flight-search --dep "上海" --arr "东京" --dep-date 2026-03-20 --back-date 2026-03-25
```

指定舱位：

```bash
feihuo flight-search --dep "上海" --arr "东京" --dep-date 2026-03-20 --back-date 2026-03-25 --berth-type Y
```

指定航司与价格范围：

```bash
feihuo flight-search --dep "上海" --arr "东京" --dep-date 2026-03-20 --airlines CA,MU --min-price 1000 --max-price 5000
```

查看帮助：

```bash
feihuo flight-search --help
```

## 输出

命令输出 JSON。顶层结构为：

```json
{
  "items": []
}
```

`items` 是航班方案列表。每个方案包含：

| 字段 | 说明 |
| --- | --- |
| `basePrice` | 票面基础价格 |
| `tax` | 税费 |
| `totalPrice` | 总价，包含基础价格和税费 |
| `journeys` | 行程列表 |
| `jumpUrl` | 跳转/预订地址 |

`journeys` 中每个行程包含：

| 字段 | 说明 |
| --- | --- |
| `segmentCode` | 航段编码 |
| `totalDuration` | 行程总飞行时长，格式为 `H:mm`，例如 `1:25` 表示 1 小时 25 分钟 |
| `journeyType` | 行程类型，例如直达或转机 |
| `segments` | 行程段列表 |

`segments` 中每个行程段包含：

| 字段 | 说明 |
| --- | --- |
| `depCityName` | 出发城市名称 |
| `depDateTime` | 出发日期时间 |
| `depAirportName` | 出发机场名称 |
| `depTerm` | 出发航站楼 |
| `arrCityName` | 到达城市名称 |
| `arrDateTime` | 到达日期时间 |
| `arrAirportName` | 到达机场名称 |
| `arrTerm` | 到达航站楼 |
| `airlineName` | 航空公司名称 |
| `flightNumber` | 格式化后的航班号 |
| `berthTypeName` | 舱位类型名称 |
| `duration` | 当前航班飞行时长，格式为 `H:mm` |

## 展示建议

向用户展示结果时，优先展示：

- 总价、基础价和税费
- 出发/到达城市、机场、航站楼
- 出发/到达时间
- 航空公司和航班号
- 总飞行时长和航班飞行时长
- 同一行末尾展示 `[点击预订]({jumpUrl})`

如果有多个方案，建议使用 Markdown 表格进行比较。
