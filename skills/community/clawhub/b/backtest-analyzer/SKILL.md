---
name: backtest-analyzer
description: |
  回测分析工具。从交易记录CSV计算回测核心指标：
  胜率、盈亏比、最大回撤、夏普比率、获利因子、
  最佳/最差单笔交易。支持JSON报告导出。

  Use when: 需要评估交易策略表现、分析回测结果、
  计算策略风险指标、对比不同策略。

  🎉 v1.0.0 指标:
  - 总交易数 / 盈利交易 / 亏损交易
  - 胜率 / 盈亏比 / 获利因子
  - 总收益率 / 平均每笔收益
  - 最大回撤 / 夏普比率
  - 最佳/最差单笔交易

  触发关键词：回测分析、策略评估、量化交易、交易统计
  适用范围：CSV 交易记录
  运行模式：纯本地
---

# 📊 Backtest Analyzer

## Overview
从交易记录CSV自动计算回测核心指标。支持自动列名识别（pnl/profit/盈亏、price/成交价等），无需手动配置数据格式。

## Usage
```bash
# 标准分析
python3 scripts/backtest_analyzer.py --file trades.csv

# 指定本金
python3 scripts/backtest_analyzer.py --file trades.csv --capital 500000

# 导出JSON报告
python3 scripts/backtest_analyzer.py --file trades.csv --output report.json --json
```

## 输出示例
```
📊 回测分析报告
    =============================================
    总交易数:    342
    盈利交易:    198 (57.9%)
    亏损交易:    144 (42.1%)
    =============================================
    总收益:     +128,450.00 (+12.85%)
    平均每笔:   +0.04%
    胜率:       57.9%
    盈亏比:     2.35
    获利因子:   2.81
    =============================================
    最大回撤:    8.45%
    夏普比率:    1.62
    最佳交易:   +12,500.00
    最差交易:   -8,200.00
```

## JSON Output
```json
{
  "total_trades": 342,
  "win_trades": 198,
  "loss_trades": 144,
  "win_rate_pct": 57.9,
  "total_pnl": 128450.0,
  "total_return_pct": 12.85,
  "max_drawdown_pct": 8.45,
  "sharpe_ratio": 1.62,
  "profit_factor": 2.81
}
```

## CSV列自动识别
自动匹配的列名（优先级顺序）：
| 字段 | 匹配列名 |
|------|---------|
| 盈亏 | pnl, profit, 盈亏, return, net_pnl |
| 价格 | price, 成交价, avg_price, close |
| 日期 | date, 日期, trade_date |
| 股票 | stock, 代码, symbol |
| 数量 | shares, 数量, qty |

## Use Cases
- **策略回测**: 导入回测引擎输出，计算策略指标
- **实盘复盘**: 导入实际交易记录，分析交易质量
- **对比分析**: 对比不同策略的报告，选择最优

## Security
- ✅ 纯本地运行，无网络请求
- ✅ 只读CSV输入文件
- ❌ 无任意代码执行
