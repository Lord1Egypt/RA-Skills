# 📊 Chinese Interest Rate Monitor

全面追踪中国利率数据，每日检查，有变化立即推送通知。
**触发词：利率, 存款利率, LPR, 国债收益率, SHIBOR, 利率监测, 今天利率, 利率查询, 利息**

> Monitor China interest rates comprehensively. Daily check with change alerts.

## Metadata

- **name**: chinese-interest-rate
- **version**: 3.0.0
- **description**: 全面追踪中国利率数据（中英文双语）：LPR、存款基准利率、国债收益率、SHIBOR、房贷利率等，有变化立即推送。可配置语言：中文/English。适用金融从业者、房贷用户、投资者、经济研究者。
- **language**: zh-CN / en (configurable)
- **tags**: finance, china, interest-rate, LPR, SHIBOR, bank-deposit, bond-yield, mortgage, monitor, 利率, 贷款市场报价利率, 国债收益率, 房贷利率, china-finance, CNY rates

---

## Overview

| Feature | Description |
|---------|-------------|
| 🏦 基准利率 | 1Y/3Y/5Y 定期存款基准利率 |
| 📊 LPR | 1Y/5Y 贷款市场报价利率 |
| 📉 国债收益率 | 1Y/3Y/10Y 国债收益率 |
| 💧 SHIBOR | 隔夜/1周/1月/3M 银行间同业拆借利率 |
| 🏠 房贷利率 | 5年期以上LPR（基准房贷利率） |
| 🔄 逆回购 | 7天/14天 公开市场操作利率 |
| 💰 存款准备金 | 大型金融机构存款准备金率 |
| Daily Check | 每日自动检查 |
| Change Alert | 有变化立即推送，无变化静默 |

---

## 语言配置 (Language Config)

| 配置值 | 通知语言 |
|--------|---------|
| `zh` / `zh-CN` / `中文` | 🇨🇳 全中文通知 |
| `en` / `en-US` / `英文` | 🇺🇸 全英文通知 |
| `bilingual` / `双语` | 🇨🇳🇺🇸 中英双语通知 |

在 `data/config.json` 中设置语言偏好：

```json
{
  "language": "bilingual"
}
```

---

## Data Points Tracked

### 🏦 银行存款利率（基准）

| 期限 | Description |
|------|-------------|
| 1年 | 定期存款一年期基准利率 |
| 3年 | 定期存款三年期基准利率 |
| 5年 | 定期存款五年期基准利率 |

### 📊 LPR（贷款市场报价利率）

| 期限 | Description |
|------|-------------|
| 1年期 | 贷款市场报价利率（实体经济） |
| 5年期以上 | 贷款市场报价利率（房地产） |

### 📉 国债收益率

| 期限 | Description |
|------|-------------|
| 1年期 | 1年期国债收益率 |
| 3年期 | 3年期国债收益率 |
| 10年期 | 10年期国债收益率（重要风向标） |

### 💧 SHIBOR（上海银行间同业拆借利率）

| 期限 | Description |
|------|-------------|
| O/N 隔夜 | 隔夜拆借利率（最短资金成本） |
| 1W 一周 | 1周期限 |
| 1M 一月 | 1月期限 |
| 3M 三月 | 3月期限（重要参考） |

---

## 数据来源与抓取

### 数据抓取方式

本 skill 有两种运行模式：

| 模式 | 说明 |
|------|------|
| **独立抓取** | `python scripts/check_rates.py` 直接运行，脚本自动从网络抓取数据 |
| **Agent 喂数据** | OpenClaw agent 通过 web_search 获取数据后，以 JSON 参数传入脚本 |

### 实际抓取的数据源

| 类型 | 来源 | 抓取方式 |
|------|------|---------|
| 国债收益率 | Yahoo Finance (CN10Y=X 等) | ✅ 自动抓取 |
| SHIBOR | 中国货币网 shibor.org | ✅ 自动抓取 |
| LPR | Yahoo Finance (CNLPR1Y=X) | ✅ 自动抓取 |
| 存款基准利率 | 中国人民银行官网 | ⚠️ 需 agent 辅助 |
| 公开市场操作利率 | 中国人民银行官网 | ⚠️ 需 agent 辅助 |

> ⚠️ 注意：脚本可独立运行，但部分数据（存款基准利率、OMO利率）可能因网络限制需要 agent 辅助补充。

---

## 通知格式

### 有变化时

**中文配置 (zh):**
```
📊 中国利率变动日报 | {日期}

🏦 银行存款利率（基准）
- 1年: X.XX% (±Xbp)
...

📊 LPR 贷款市场报价利率
...

📉 国债收益率
...
```

**英文配置 (en):**
```
📊 China Interest Rate Daily | {date}

🏦 Bank Deposit Base Rates
- 1Y: X.XX% (±Xbp)
...

📊 LPR (Loan Prime Rate)
...

📉 Government Bond Yields
...
```

**双语配置 (bilingual):**
上下两语言并排显示。

### 无变化时

静默，不发送任何通知。

---

## 数据文件格式

`data/config.json`:
```json
{
  "language": "bilingual",
  "notifyOnChange": true
}
```

`data/rates.json`:
```json
{
  "updateDate": "2026-03-30",
  "depositRates": { "1year": "", "3year": "", "5year": "" },
  "LPR": { "1year": "", "5yearPlus": "" },
  "bondYields": { "1year": "", "3year": "", "10year": "" },
  "SHIBOR": { "ON": "", "1W": "", "1M": "", "3M": "" },
  "mortgageLPR": { "5yearPlus": "" },
  "OMO": { "repo7d": "", "repo14d": "", "MLF1Y": "" }
}
```

---

## 安装

```bash
openclaw skills install chinese-interest-rate
```

---

## Cron Schedule

建议每日 10:00（北京时间）执行：

```json
{
  "schedule": {
    "kind": "cron",
    "expr": "0 10 * * *",
    "tz": "Asia/Shanghai"
  }
}
```

---

## 适用场景

- 📊 金融从业者（银行、证券、基金）
- 🏠 房贷用户（LPR变动直接影响月供）
- 💼 投资理财（LPR是资本市场重要指标）
- 📈 经济研究者（利率是宏观经济的核心变量）

---

## License

MIT License

---

_追踪利率变化，把握理财先机 📊_
_Track rate changes, stay ahead in finance 📈_
