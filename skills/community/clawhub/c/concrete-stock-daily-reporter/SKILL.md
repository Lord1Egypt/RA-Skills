---
name: stock-daily-report
description: 每日自选股报告生成与发送技能。当用户需要生成股票日报、查询自选股行情、KDJ技术指标、或设置定时股票报告时触发。用户需提供股票代码和名称列表。
---

# Stock Daily Report Skill

每日自选股报告生成与发送，涵盖行情数据、KDJ指标、重点关注信号。

## 使用方式

### 需要用户提供的参数

用户必须提供自选股列表，格式为 Python 字典：

```python
STOCKS = {
    "代码1": "名称1",
    "代码2": "名称2",
    # ...
}
```

**股票代码规则：**
- 以 `6` 开头 → 上交所（sh）
- 以 `0` 或 `3` 开头 → 深交所（sz）
- 上证指数 → `1A0001`（映射为 `sh000001`）
- 创业板 → 以 `3` 开头（深交所）

**示例：**
```python
STOCKS = {
    "1A0001": "上证指数",
    "000001": "平安银行",
    "600036": "招商银行",
    "000858": "五粮液",
}
```

### 生成报告

用户提供股票列表后，运行：

```bash
cd /root/.openclaw/workspace/skills/stock-daily-report/scripts
# 编辑 daily_report.py，将 STOCKS 替换为用户提供的列表
python3 daily_report.py
```

### 发送报告到飞书

```bash
cd /root/.openclaw/workspace/skills/stock-daily-report/scripts
bash send_report.sh
```

### 查看/修改定时任务

```bash
# 查看当前定时任务
crontab -l

# 编辑定时任务（每天08:30发送）
crontab -e
# 添加：30 8 * * * /root/.openclaw/workspace/skills/stock-daily-report/scripts/send_report.sh >> /tmp/stock_report.log 2>&1
```

## 报告内容结构

1. **涨跌幅排行** - 按当日涨跌幅排序
2. **KDJ 指标** - K/D/J 值，超买(≥80)⚠️ / 超卖(≤20)🚀
3. **详细行情** - 现价、昨收、涨跌额、涨幅、成交额
4. **重点关注** - 超卖/超买信号、涨幅前3
5. **今日统计** - 上涨/下跌/平盘数量、平均涨幅

## 数据来源

- 价格：新浪财经 API（`hq.sinajs.cn`）
- KDJ：东方财富 K线 API（`push2his.eastmoney.com`）

## 脚本说明

| 脚本 | 功能 |
|------|------|
| `daily_report.py` | 生成报告内容（行情+KDJ），输出纯文本 |
| `send_report.sh` | 调用 Python 生成报告，通过 openclaw 发送飞书消息 |

## 依赖

- Python3
- openclaw CLI（用于发送飞书消息）
- 网络访问（新浪/东方财富 API）

## 文件结构

```
stock-daily-report/
├── SKILL.md
└── scripts/
    ├── daily_report.py    # 报告生成脚本
    └── send_report.sh     # 发送脚本
```

## 修改股票列表

每次使用前，编辑 `scripts/daily_report.py` 中的 `STOCKS` 字典为用户提供的最新列表。