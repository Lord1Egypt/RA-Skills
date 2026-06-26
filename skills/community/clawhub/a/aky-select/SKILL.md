---
name: AKY-select
description: A股选股器，9维度筛选符合AKY战法的中小盘强势股。涨幅2-5%、流通市值50-200亿、换手率4-10%、量比>1、量价齐升、均线多头排列、强于大盘、全天在均价线上方、近3日资金净流入。
version: 2.0.0
allowed-tools:
  - Bash(python:*)
  - Read
metadata:
  openclaw:
    requires:
      bins:
        - python3
    install:
      - kind: uv
        package: akshare
    emoji: 📊
    homepage: https://github.com/aky/aky-select
    os:
      - linux
      - darwin
---

# AKY-select — A股选股器 v2.0

基于 **akshare**（免费，无需 Token）实现 A 股实时筛选。涵盖量、价、时、空、资金 9 个维度。

## 选股逻辑

| # | 条件 | 数值 | 逻辑 |
|---|------|------|------|
| ① | 涨幅 | **+2% ~ +5%** | 收盘涨幅适中，不追高也不买冷门 |
| ② | 流通市值 | **50~200亿** | 中小盘，弹性好 |
| ③ | 换手率 | **4%~10%** | 交投活跃但不过热 |
| ④ | 量比 | **>1** | 今日量超过近5日均量 |
| ⑤ | 量价齐升 | 收阳+放量 | 今收 > 昨收 且 今量 > 昨量 |
| ⑥ | 均线多头 | MA5>MA10>MA20 | 短期趋势向上，且股价 > MA5 |
| ⑦ | 强于大盘 | 个股 > 上证指数 | 相对强势 |
| ⑧ | 均价线上方 | 价格 > 全天均价 | 全天强势运行 |
| ⑨ | 3日资金净流入 | 主力净流入累计 > 0 | 主力资金持续买入 |

## 使用方法

### 一键运行

```bash
cd ~/.openclaw/workspace && python3 skills/aky-select/scripts/aky_select.py
```

### 定时任务

每天 15:05（收盘后5分钟）自动跑：

```bash
mkdir -p ~/.openclaw/workspace/skills/aky-select/logs
(crontab -l 2>/dev/null; echo "5 15 * * 1-5 cd ~/.openclaw/workspace && python3 skills/aky-select/scripts/aky_select.py >> skills/aky-select/logs/aky_\$(date +\%Y\%m\%d).log 2>&1") | crontab -
```

## 依赖

- `akshare` ≥ 1.18.50（已预装）
- `pandas`（已预装）
- `numpy`（已预装）

## 数据来源

| 数据 | 接口 | 源站 |
|------|------|------|
| 实时行情 | `stock_zh_a_spot_em` | 东方财富 |
| 历史日线 | `stock_zh_a_hist` | 东方财富 |
| 上证指数 | `stock_zh_index_spot_em` | 东方财富 |
| Tick（均价） | `stock_zh_a_tick_tx_js` | 腾讯 |
| 资金流向 | `stock_individual_fund_flow` | 东方财富 |

## 输出样例

```
  代码      名称    价格    涨幅%   市值亿   换手%    量比   量价  MA  大盘  均价  资金
  ───────────────────────────────────────────────────────────────────────────────────────
  600XXX   XXXXX  12.34   +3.21   85.6     6.54    1.83   ✅  ✅  ✅  ⚪  ✅
```

## 注意事项

1. **数据实时性**：盘中跑是实时行情，盘后跑是最终数据
2. **条件⑧**：需要腾讯 tick 数据支持，不可用时标 ⚪
3. **条件⑨**：取最近3个交易日的主力净流入合计
4. **运行时长**：全A股 ~5850 只，含资金流向约 60-90 秒
5. **⚠️ 非投资建议**：仅为技术面筛选工具，请结合基本面判断

---

_版本：2.0 | 作者：AKY | 数据：akshare (东方财富/新浪/腾讯)_
