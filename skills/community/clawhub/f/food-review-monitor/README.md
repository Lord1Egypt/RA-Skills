# food-review-monitor

🍔 餐饮外卖评价智能监控系统

自动监控**美团外卖、饿了么/淘宝闪购、京东外卖**三大平台的顾客评价数据，智能检测口味变差、评分下滑、配送超时等服务异常，生成可视化HTML报告并推送告警。

## 核心功能

- **CSV/Excel一键导入** — 从各平台商家后台导出评价数据，自动识别格式
- **5维异常检测** — 口味异常、配送异常、服务异常、评分下滑、差评突增
- **智能情感分析** — 餐饮领域专属情感词典（200+词），无需外部API
- **可视化HTML报告** — ECharts交互图表，含评分趋势、维度分析、关键词云

## 快速开始

```bash
# 安装依赖
pip install pandas openpyxl jieba snownlp

# 初始化配置
python scripts/monitor.py --setup

# 导入评价数据
python scripts/monitor.py --file 评价数据.csv --platform meituan

# 快速检查（基于历史数据）
python scripts/monitor.py --check

# 对比两个时段
python scripts/monitor.py --compare 本周.csv 上周.csv
```

## 支持的平台

| 平台 | 数据来源 | 导入方式 |
|------|---------|---------|
| 美团外卖 | 美团开店宝 → 导出评价 | CSV |
| 饿了么/淘宝闪购 | 饿了么商家后台 → 导出 | CSV/XLSX |
| 京东外卖 | 京东商家后台 → 导出 | CSV |

## CSV格式要求

必须包含以下列之一：

| 必需 | 列名（自动识别） |
|------|-----------------|
| 评价内容 | 评价内容 / 评论内容 / 评价 / 评论 |
| 评分 | 评分 / 星级 / 综合评分 / star |
| 评价时间 | 评价时间 / 评论时间 / 时间 |
| 配送时长（可选） | 配送时长 / 送达时间 |
| 菜品（可选） | 菜品 / 商品 |

## 分析维度

| 维度 | 检测内容 | 默认告警线 |
|------|---------|-----------|
| 口味 | 好吃/难吃/咸淡/新鲜度 | 负面 > 30% |
| 配送 | 超时/破损/漏送/错送 | 提及率 > 15% |
| 服务 | 态度/回复/售后 | 负面 > 20% |
| 评分 | 平均分趋势 | 低于 4.0 |
| 趋势 | 差评率变化 | 超历史 2 倍 |

## 项目结构

```
food-review-monitor/
├── SKILL.md              # WorkBuddy 技能定义
├── README.md
├── scripts/
│   ├── monitor.py        # 主入口 CLI
│   ├── data_loader.py    # 数据加载与清洗
│   ├── analyzer.py       # 情感分析 + 异常检测
│   ├── reporter.py       # HTML 报告生成
│   └── config.template.json
└── .gitignore
```

## License

MIT
