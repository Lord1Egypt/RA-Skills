# 盈利预测数据调用指导（Open API · earning_forecast）

## 简介

通过 Gangtise Open API 获取券商一致预期盈利预测数据，脚本：`scripts/earning_forecast.py`。

- 支持并发查询多只证券（按证券逐个请求并合并结果）。
- 支持按日期区间筛选：`startDate`、`endDate`。
- 支持按指标筛选：`consensusList`。
- 默认不传指标时返回全部可选字段，并展开为扁平表：
  `security_code | date | 预测年份 | ...`。

## 参数

| 参数 | 必填 | 说明 |
|------|------|------|
| `--securities` | 否* | 完整证券代码，逗号分隔，如 `600519.SH,000858.SZ`。 |
| `--securities-file` | 否* | CSV 路径，须含 `security_code` 列。 |
| `-sd` / `--start-date` | 否 | 开始日期 `yyyy-MM-dd`；默认今天。 |
| `-ed` / `--end-date` | 否 | 结束日期 `yyyy-MM-dd`；默认今天。 |
| `--consensus-list` | 否 | 一致预期指标，逗号分隔；不传默认返回全部。 |

\* 须至少提供 `--securities` 或 `--securities-file` 之一。

`--consensus-list` 可选值：

- `netIncome`：归母净利润
- `netIncomeYoy`：归母净利润同比增速（%）
- `eps`：每股收益
- `pe`：市盈率
- `bps`：每股净资产
- `pb`：市净率
- `peg`：PEG
- `roe`：净资产收益率
- `ps`：市销率

## 约束与说明

- 仅支持完整证券代码，不支持简称解析。
- 对于单日查询（`start-date == end-date`），若当天无数据，脚本会自动仅向前回退一天重试一次；不会继续向前回退。

## 调用示例

**并发查询多证券并返回全部字段：**

```bash
python3 scripts/earning_forecast.py --securities 600519.SH,000858.SZ -sd 2026-03-20 -ed 2026-03-25
```

**从文件读取证券并仅返回部分一致预期指标：**

```bash
python3 scripts/earning_forecast.py --securities-file ./codes.csv -sd 2026-03-20 -ed 2026-03-25 --consensus-list netIncome,eps,pe
```

## 返回说明

- 成功时在 `workspace/gangtise/earning_forecast/` 下生成 `earning_forecast_*.csv`。
- 每一行对应「某日 + 某预测年份」的一条记录。
- 字段默认顺序：
  - `security_code`
  - `date`
  - `预测年份`
  - 其余为所选一致预期指标（中文列名）

## 返回数据示例（CSV 结构）

| security_code | date | 预测年份 | 归母净利润 | 每股收益 | 市盈率 |
|---------------|------|----------|------------|----------|--------|
| 600519.SH | 2026-03-25 | 2026E | 1250.50 | 62.50 | 28.60 |
| 600519.SH | 2026-03-25 | 2027E | 1450.80 | 72.50 | 24.80 |
| 600519.SH | 2026-03-25 | 2028E | 1680.20 | 84.00 | 21.50 |
