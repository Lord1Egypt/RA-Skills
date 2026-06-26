---
name: a-stock-paper-trade
description: A股模拟炒股系统。当用户需要模拟炒股、查询行情、买卖下单、查看持仓盈亏时触发。支持实时行情、买卖下单、持仓管理、盈亏计算、涨跌排行。关键词：炒股、买入、卖出、持仓、盈亏、行情、涨停、跌停、选股、大盘。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "os": ["darwin", "linux", "win32"]
      }
  }
---

优化日期: 2026-04-02

# A股模拟炒股

本地纸面交易系统，基于 akshare 实时行情。无需任何外部账号，纯模拟。

## 快速开始

```bash
# 初始化账户（100万虚拟资金）
source ~/.agent-reach-venv/bin/activate
python3 {baseDir}/scripts/trader.py init

# 查大盘
python3 {baseDir}/scripts/trader.py quote --all

# 查个股行情
python3 {baseDir}/scripts/trader.py quote 600519 000001

# 搜索股票
python3 {baseDir}/scripts/trader.py search 茅台

# 买入（1手=100股，市价）
python3 {baseDir}/scripts/trader.py buy 600519 1

# 买入（指定价格）
python3 {baseDir}/scripts/trader.py buy 600519 2 --price 1700

# 卖出
python3 {baseDir}/scripts/trader.py sell 600519 1

# 查持仓
python3 {baseDir}/scripts/trader.py positions

# 账户总览
python3 {baseDir}/scripts/trader.py balance

# 交易记录
python3 {baseDir}/scripts/trader.py history --limit 10

# K线
python3 {baseDir}/scripts/trader.py kline 600519 --days 60

# 涨幅TOP10
python3 {baseDir}/scripts/trader.py rank --top 10

# 跌幅TOP10
python3 {baseDir}/scripts/trader.py rank --bottom --top 10
```

## 交易规则

- 最小单位：1手 = 100股
- 佣金：万三（最低5元）
- 印花税：千一（仅卖出）
- 不支持涨跌停价格下单（但当前版本未强制校验，agent 应自行判断）
- 数据来源：东方财富（akshare），仅交易时间内有效

## 费用计算

| 费用 | 买入 | 卖出 |
|------|------|------|
| 佣金 | 万三（最低5元） | 万三（最低5元） |
| 印花税 | — | 千一 |
| 过户费 | — | 忽略（模拟简化） |

## 数据存储

- 位置：`~/.openclaw/paper-trade/portfolio.json`
- 重置：`python3 {baseDir}/scripts/trader.py init --reset`

## 注意

- 行情数据来自 akshare，依赖网络（不需要代理，东方财富国内直连）
- 非 A 股交易时间行情可能不准确
- 所有操作输出 JSON，方便 agent 解析
