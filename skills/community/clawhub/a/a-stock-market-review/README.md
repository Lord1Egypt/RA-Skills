# A 股市场复盘 Skill

📈 收盘后专用 — 获取 A 股市场每日表现总结报告

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 运行脚本

```bash
cd /home/node/.openclaw/workspace/skills/a-stock-market-review
python3 scripts/a_stock_market_review.py
```

### 3. 在代码中使用

```python
from scripts.a_stock_market_review import AStockMarketReview

review = AStockMarketReview()

# 获取完整复盘报告
print(review.generate_report())

# 或者单独获取数据
indices = review.get_index_data()           # 大盘指数
sectors = review.get_hot_sectors(10)        # 热门板块
leaders = review.get_sector_leaders("BK1128", 3)  # 某板块龙头股
ath_stocks = review.get_all_time_high_stocks(20)  # 创新高股票
```

## 功能特性

✅ **大盘指数** — 上证、深证、创业板实时数据
✅ **热门板块** — 按涨幅排序的 Top 10 概念板块
✅ **龙头股** — 热门板块的领涨个股
✅ **创新高股票** — 历史新高 +20 日/60 日连续新高
✅ **市场简评** — 自动生成的市场分析
✅ **无需 API Key** — 使用东方财富公开接口

## 输出示例

```
==================================================
📈 A 股市场复盘
📅 2026 年 03 月 14 日 15:30 (Asia/Shanghai)
==================================================

【大盘指数】
  上证指数：4098.59 点 (+1.00%)
  深证成指：14239.30 点 (-0.83%)
  创业板指：3281.94 点 (-0.81%)

【🔥 今日最热板块 Top 10】
  🔥 1. CPO 概念：6518.76 (+6.66%)
  🔥 2. 光通信模块：3082.79 (+5.69%)
  ...

【🏆 板块龙头股】
  CPO 概念:
    • 中际旭创 (300308): +12.50% 🚀
    ...
```

## 目录结构

```
a-stock-market-review/
├── SKILL.md                      # Skill 说明文档
├── README.md                     # 本文件
└── scripts/
    └── a_stock_market_review.py  # 主脚本
```

## 注意事项

⚠️ **数据更新时间**：交易日 9:30-15:00 实时更新，非交易时段显示最后收盘价
⚠️ **最佳使用时机**：建议 15:00 收盘后使用，获取完整当日数据
⚠️ **仅供参考**：不构成投资建议，投资需谨慎

## 许可证

MIT License
