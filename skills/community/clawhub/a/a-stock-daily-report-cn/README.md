# A 股市场日报 Skill

📈 获取 A 股市场每日表现报告

## 快速开始

### 1. 安装依赖

```bash
pip install requests
```

### 2. 运行脚本

```bash
cd /home/node/.openclaw/workspace/skills/a-stock-daily-report
python3 scripts/a_stock_daily_report.py
```

### 3. 在代码中使用

```python
from scripts.a_stock_daily_report import AStockDailyReport

report = AStockDailyReport()

# 获取完整报告
print(report.generate_report())

# 或者单独获取数据
indices = report.get_index_data()      # 大盘指数
sectors = report.get_hot_sectors(10)   # 热门板块
leaders = report.get_sector_leaders("BK1128", 3)  # 某板块龙头股
```

## 功能特性

✅ **大盘指数** - 上证、深证、创业板实时数据
✅ **热门板块** - 按涨幅排序的 Top 10 概念板块
✅ **龙头股** - 热门板块的领涨个股
✅ **市场简评** - 自动生成的市场分析
✅ **无需 API Key** - 使用东方财富公开接口

## 输出示例

```
📈 A 股市场日报
📅 2026 年 03 月 10 日 23:22

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
    • 蘅东光 (920045): +17.04% 🚀
    ...
```

## 目录结构

```
a-stock-daily-report/
├── SKILL.md                    # Skill 说明文档
├── README.md                   # 本文件
└── scripts/
    └── a_stock_daily_report.py # 主脚本
```

## 注意事项

⚠️ 数据仅在交易时段实时更新（工作日 9:30-15:00）
⚠️ 非交易时段显示最后收盘价
⚠️ 仅供参考，不构成投资建议

## 许可证

MIT License
