# 估值数据 API（Open API · 估值分析）

## 简介

通过 Gangtise Open API 查询估值指标（peTtm、psTtm、pbMrq、peg、pcfTtm、em）及对应历史分位，脚本 **`scripts/valuation.py`**。

对同一证券会**并发 6 次**请求（每指标一次），`fieldList` 固定为 `value`、`percentileRank`，再合并为宽表。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `-sd` / `--start-date` | 否 | 开始日期 `yyyy-MM-dd`。未指定时默认**今天**。 |
| `-ed` / `--end-date` | 否 | 结束日期 `yyyy-MM-dd`。未指定时默认**今天**。 |
| `--securities` | 否* | **完整证券代码**，逗号分隔（如 `600519.SH`）。**不支持简称**。 |
| `--securities-file` | 否* | CSV 路径，须含列 **`security_code`**（完整代码）。 |
| `--limit` | 否 | 单次指标请求最大行数，默认 `2000`（接口上限以官方文档为准）。 |

\* 须至少提供 `--securities` 或 `--securities-file` 之一。

## 约束与说明

- **仅支持完整证券代码**（如 `600519.SH`），不进行键盘精灵或简称解析。
- 默认时间范围为当天（未传 `-sd/-ed` 时由脚本内默认值体现）。
- 本 OpenAPI 脚本**仅输出估值模块**（`module: valuation`），**不包含** skills-backend 版估值中可能附带的盈利预测（profit_forecast）表。

## 调用示例

```bash
python3 scripts/valuation.py --securities 600519.SH
```

```bash
python3 scripts/valuation.py --securities-file ./codes.csv -sd 2023-01-01 -ed 2026-12-31
```

## 返回说明

- **成功**：在 `workspace/gangtise/valuation/`（或当前环境解析出的 gangtise 工作目录下）生成 **`valuation_*.csv`**，返回文案中含绝对路径与样例 Markdown 表。
- **失败**：如未配置授权、证券代码无效、无数据等，返回错误说明字符串。

## 返回数据示例（CSV 列）

列名经 `format_response` 处理后，前几列为固定字段，其余为中文指标名（示例）：

| security_abbr | security_code | date | 市盈率TTM | 市盈率TTM在3年中所处分位 | 市销率TTM | … |
|---------------|---------------|------|------------|----------------------------|------------|---|
| 600519.SH | 600519.SH | 2026-01-01 | … | … | … | … |

（证券简称无单独解析时，可能与代码列一致，以实际输出为准。）
