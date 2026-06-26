# train-search 命令参考

`train-search` 用于搜索火车票，支持按火车类型、座位类型、排序方式、车次、出发小时和到达小时筛选。

## 使用前提

CLI 从 `~/.openclaw/qclaw/user-info.json` 读取 `accessToken`，请求 API 时使用：

```http
Authorization: Bearer <accessToken>
```

请确保该文件存在且 `accessToken` 有效。

## 命令格式

```bash
feihuo train-search --dep <出发地> --arr <目的地> --dep-date <出发日期> [--train-type <火车类型>] [--seat-type <座位类型>] [--sort-type <排序方式>] [--dep-hour-start <出发小时开始>] [--dep-hour-end <出发小时结束>] [--arr-hour-start <到达小时开始>] [--arr-hour-end <到达小时结束>] [--train-number <车次号>]
```

## 参数

| 参数 | 必填 | 说明 |
| --- | --- | --- |
| `--dep <dep>` | 是 | 出发地，例如：`上海` |
| `--arr <arr>` | 是 | 目的地，例如：`北京` |
| `--dep-date <depDate>` | 是 | 出发日期，格式：`YYYY-MM-DD`，不能早于今天 |
| `--train-type <trainType>` | 否 | 火车类型：`high-speed` 高铁/动车，`normal` 普通车 |
| `--seat-type <seatType>` | 否 | 座位类型，见下方「座位类型」 |
| `--sort-type <sortType>` | 否 | 排序方式，见下方「排序方式」；不传时默认按出发时间从早到晚 |
| `--dep-hour-start <depHourStart>` | 否 | 出发小时开始，0-23 |
| `--dep-hour-end <depHourEnd>` | 否 | 出发小时结束，0-23 |
| `--arr-hour-start <arrHourStart>` | 否 | 到达小时开始，0-23 |
| `--arr-hour-end <arrHourEnd>` | 否 | 到达小时结束，0-23 |
| `--train-number <trainNumber>` | 否 | 车次号，例如：`G2` |

`--train-type` 也兼容 `highspeed`、`高铁`、`动车`、`高铁/动车`、`普通`、`普通车` 等写法。

## 座位类型

| CLI 值 | 说明 |
| --- | --- |
| `second-class` | 二等座 |
| `first-class` | 一等座 |
| `business-class` | 商务座 |
| `hard-sleeper` | 硬卧 |
| `soft-sleeper` | 软卧 |

也兼容中文（如 `二等座`）及 camelCase API 枚举名（如 `secondClass`）。

指定 `--seat-type` 时：

- 只保留包含该席别的车次；无该席别的车次会被整趟过滤。
- 每个车次的 `seats` 仅保留匹配的席别，`minPrice` 按筛选后的座位计算。

## 排序方式

| CLI 值 | 说明 |
| --- | --- |
| `price-high-to-low` | 价格从高到低 |
| `price-low-to-high` | 价格从低到高 |
| `duration-short-to-long` | 耗时从短到长 |
| `duration-long-to-short` | 耗时从长到短 |
| `departure-early-to-late` | 出发时间从早到晚（默认） |
| `departure-late-to-early` | 出发时间从晚到早 |

也兼容 `price-desc`、`price-asc`、`dep-early`、`dep-late` 及 camelCase API 枚举名（如 `priceLowToHigh`）。

排序后最多返回 10 条车次。

## 自然语言 → CLI 参数

| 用户说法 | CLI 参数 |
| --- | --- |
| 高铁 / 动车 / 普通车 | `--train-type high-speed` / `normal` |
| 二等座 / 一等座 / 商务座 / 硬卧 / 软卧 | `--seat-type second-class` 等 |
| 上午走 / 8 点到 12 点出发 | `--dep-hour-start 8 --dep-hour-end 12` |
| 按价格从低到高 / 耗时最短 | `--sort-type price-low-to-high` / `duration-short-to-long` |
| G2 / 指定车次 | `--train-number G2` |

**示例**（用户：「明天上海到北京高铁，上午出发，二等座，按价格从低到高」）：

```bash
feihuo train-search --dep "上海" --arr "北京" --dep-date 2026-06-13 --train-type high-speed --seat-type second-class --dep-hour-start 8 --dep-hour-end 12 --sort-type price-low-to-high
```

## 示例

搜索指定城市和日期：

```bash
feihuo train-search --dep "上海" --arr "北京" --dep-date 2026-03-20
```

筛选高铁/动车：

```bash
feihuo train-search --dep "上海" --arr "北京" --dep-date 2026-03-20 --train-type high-speed
```

筛选二等座并按价格从低到高排序：

```bash
feihuo train-search --dep "上海" --arr "北京" --dep-date 2026-03-20 --seat-type second-class --sort-type price-low-to-high
```

按出发小时筛选：

```bash
feihuo train-search --dep "上海" --arr "北京" --dep-date 2026-03-20 --dep-hour-start 8 --dep-hour-end 12
```

按到达小时筛选：

```bash
feihuo train-search --dep "上海" --arr "北京" --dep-date 2026-03-20 --arr-hour-start 13 --arr-hour-end 18
```

指定车次：

```bash
feihuo train-search --dep "上海" --arr "北京" --dep-date 2026-03-20 --train-number G2
```

查看帮助：

```bash
feihuo train-search --help
```

## 输出

命令输出 JSON。顶层结构为：

```json
{
  "items": []
}
```

`items` 是火车票方案列表。每个方案包含：

| 字段 | 说明 |
| --- | --- |
| `minPrice` | 最低价格 |
| `totalDuration` | 总耗时，格式为 `H:mm` |
| `journeys` | 行程列表 |
| `jumpUrl` | 跳转/预订地址 |

`journeys` 中每个行程包含：

| 字段 | 说明 |
| --- | --- |
| `journeyType` | 行程类型，例如直达 |
| `totalDuration` | 行程总耗时，格式为 `H:mm` |
| `segments` | 行程段列表 |

`segments` 中每个行程段包含：

| 字段 | 说明 |
| --- | --- |
| `trainNumber` | 车次号 |
| `depStation` | 出发站 |
| `arrStation` | 到达站 |
| `depDate` | 乘车日期 |
| `depTime` | 出发时间 |
| `arrTime` | 到达时间 |
| `duration` | 当前行程段耗时，格式为 `H:mm` |
| `seats` | 座位列表 |

`seats` 中每个座位包含：

| 字段 | 说明 |
| --- | --- |
| `seatType` | 座位类型 |
| `price` | 票价 |
| `count` | 余票数量，`0` 表示没票，`99` 表示有票 |
| `allowStandby` | 是否允许候补 |

## 校验规则

- `--dep-date` 不能早于今天。
- 小时参数必须是有效数字，并且服务端要求范围为 0-23。
- 同一组小时筛选中，开始小时不能大于结束小时。
- `--train-type` 只支持高铁/动车或普通车。
- `--seat-type` 只支持上述五种座位类型。
- `--sort-type` 只支持上述六种排序方式。

## 展示建议

向用户展示结果时，优先展示：

- 车次、最低价格和总耗时
- 出发站、到达站、出发时间和到达时间
- 座位类型、票价、余票数量和是否允许候补
- 同一行末尾展示 `[点击预订]({jumpUrl})`

如果有多个车次，建议使用 Markdown 表格进行比较。
