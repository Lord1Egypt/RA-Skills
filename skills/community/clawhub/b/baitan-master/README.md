# baitan-master — 摆摊创业全流程助手

> 🛒 从选品到出摊，一站式摆摊创业辅助工具。7大模块覆盖全流程决策。

[![Skill](https://img.shields.io/badge/WorkBuddy-Skill-orange)](https://www.codebuddy.cn)
[![License](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

## 核心能力

| 模块 | 功能 | 说明 |
|------|------|------|
| 🎯 品类推荐 | 智能匹配最佳品类 | 基于预算/城市/季节/经验 4维筛选，内置40+品类数据 |
| 💰 利润精算 | 多维度成本核算 | 日/月/年利润 + 盈亏平衡点 + 回本周期 + 健康度评分 |
| 📍 选址评估 | 5维加权评分 | 人流(25%) + 客群(25%) + 竞争(20%) + 交通(15%) + 成本(15%) |
| ☔ 天气策略 | 季节性应对方案 | 雨季/高温/寒冬 3套预案 |
| 🔍 竞品分析 | 周边摊位分析 | 距离/价格带/优势评估 + 差异化策略 |
| ✅ 出摊检查 | P0/P1/P2 优先级清单 | 10大痛点预检 |
| 📊 综合报告 | 交互式HTML可视化 | 一键生成完整决策报告 |

## 触发词

摆摊、地摊、夜市摆摊、摆摊创业、地摊经济、摆摊选品、摆摊选址、摆摊利润、摆摊成本、摆摊分析、摆摊报告、出摊、摊位、摆地摊、小吃摊

## 工作流程

```
需求理解 → 品类推荐 → 利润精算 → 选址评估 → 天气策略 → 痛点预检 → 综合报告
```

## 安装

将整个目录放入 WorkBuddy 的 skills 目录：

```bash
cp -r baitan-master ~/.workbuddy/skills/
```

## 文件结构

```
baitan-master/
├── SKILL.md                    # 主工作流
├── scripts/
│   ├── product_matcher.py      # 品类智能匹配
│   ├── profit_calculator.py    # 利润精算器
│   ├── location_scorer.py      # 5维选址评估
│   └── report_generator.py     # HTML报告生成
└── references/
    ├── product_catalog.md      # 40+品类利润数据
    ├── location_factors.md     # 选址因子详解
    └── pain_points_guide.md    # 10大痛点方案
```

## 数据来源

基于2025年市场调研数据，覆盖美食饮品/手作文创/日用百货/儿童玩具/季节爆品 5大类40+细分品类。

## License

MIT
