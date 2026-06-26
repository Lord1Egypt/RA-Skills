---
name: beijing-pollen-monitor
description: 查询北京花粉实时监测和预报数据，生成包含区级浓度、站点趋势、总量预报与分类预报的结果。北京 16 个固定站点，每区一个，用区名指定。
user-invocable: true
argument-hint: "[report|overview|stations|history|forecast|daily] [--district 海淀] [options]"
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
---

查询北京公共花粉监测与预报数据。北京共 16 个固定监测站（每区一个），用区名指定查询目标。

## 使用场景

使用本 skill 当用户需要：
- 某个区今天的花粉情况和建议（优先用 `daily`）
- 某个区当前监测和全市概况（用 `report`）
- 北京全市花粉概览（用 `overview`）
- 全部站点实时读数（用 `stations`）
- 单站点 24 小时历史趋势（用 `history`）
- 查询某个区的花粉预报（用 `forecast`）
- 每天固定时间发送某个区的晨报（用 `daily`）
- 结构化 JSON 用于下游自动化

不要使用本 skill：
- 查询北京以外的花粉数据
- 直接发送通知（本 skill 只负责查询，通知由调用方处理）

## 入口

```bash
./scripts/beijing-pollen-query.sh query --mode <mode> [options]
```

## 推荐工作流：默认晨报

用户说"查一下海淀今天花粉"或"每天给我发花粉情况"时，优先使用 daily 模式：

```bash
# 文本格式 — 适合直接展示给用户或推送通知
./scripts/beijing-pollen-query.sh query --mode daily --district 海淀 --format text
```

读取返回 JSON 的 `.data.text` 字段即为可读晨报。

```bash
# JSON 格式 — 适合程序进一步处理
./scripts/beijing-pollen-query.sh query --mode daily --district 海淀
```

daily 模式自动完成：当前监测 + 24h 相对变化 + 今天总量预报 + 明后天趋势 + 分类提示，不再强调北京其他区。

## 推荐工作流：即时查询

用户说"看一下海淀现在花粉高不高"时，使用 report 模式：

```bash
./scripts/beijing-pollen-query.sh query --mode report --district 海淀 --format text
```

report 模式自动完成：查询全市概览 → 定位目标站点 → 获取 24h 历史 → 汇总为即时简报。

## 推荐工作流：预报查询

用户说"看一下海淀明天花粉"或"海淀区花粉预报怎么样"时，使用 forecast 模式：

```bash
./scripts/beijing-pollen-query.sh query --mode forecast --district 海淀 --format text
```

forecast 模式返回：目标区总量等级预报 + 分类花粉预报 + 对应解释。

## 推荐工作流：定时晨报

用户说"每天早上 8 点发朝阳区今天花粉情况"时，优先使用 daily 模式：

```bash
./scripts/beijing-pollen-query.sh query --mode daily --district 朝阳 --format text
```

daily 模式自动完成：当前监测 + 24h 相对变化 + 今天总量预报 + 明后天趋势 + 分类提示，不再强调北京其他区。

## 模式选择

| 用户意图 | 模式 | 命令 |
|---|---|---|
| 某个区今天花粉情况 | `daily` | `--mode daily --district 海淀` |
| 某个区的即时监测简报 | `report` | `--mode report --district 海淀` |
| 全市概况 | `overview` | `--mode overview` |
| 所有站点数据 | `stations` | `--mode stations` |
| 某站点 24h 变化 | `history` | `--mode history --district 朝阳` |
| 某个区的花粉预报 | `forecast` | `--mode forecast --district 海淀` |
| 每日定时晨报 | `daily` | `--mode daily --district 朝阳` |

## 参数

| 参数 | 说明 | 默认值 |
|---|---|---|
| `--district` | 区名，模糊匹配（海淀、海淀区均可） | — |
| `--station-id` | 站点 ID（history 替代方式） | — |
| `--format` | `json` 或 `text` | `json` |
| `--limit` | 热点站点数量 | `5` |
| `--timeout-ms` | HTTP 超时（毫秒） | `8000` |

可用区名：东城、西城、朝阳、海淀、丰台、石景山、门头沟、房山、通州、顺义、昌平、大兴、怀柔、平谷、密云、延庆

## 输出约定

- 始终输出 JSON
- 成功时 `ok: true`，失败时 `ok: false` 并附非零退出码
- text 格式将可读文本包裹在 `{"data":{"text":"..."}}` 中
- 无效区名时会列出所有可用区名
- 主结果对象包含 `value_family` 和 `meaning`，用于区分区级实时、站点观测、总量预报、分类预报的不同语义

详细 JSON 结构见 [references/api-contract.md](references/api-contract.md)。
