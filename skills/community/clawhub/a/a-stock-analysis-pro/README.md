# a-stock-analysis

A股个股深度策略研报生成技能。输入股票代码，自动采集实时行情、财务数据、资金流向、行业信息，生成专业HTML研报（可导出为PDF）。

## 功能特性

- 实时行情采集（东方财富/新浪财经/腾讯财经/同花顺）
- 财务数据分析（营收、净利润、毛利率、ROE等）
- 资金流向与龙虎榜
- 三情景模拟（乐观/基准/悲观）
- 风险提示与关键节点追踪
- 专业HTML报告输出，支持打印导出PDF

## 使用方式

适用于 OpenClaw AgentSkills 规范，安装后输入股票代码即可触发分析。

## 目录结构

```
a-stock-analysis/
├── SKILL.md                  # 技能入口文件
└── references/
    ├── analysis-prompts.md   # 分析维度与提示词
    ├── data-sources.md       # 数据源与采集规范
    └── report-template.md    # HTML报告模板与质量检查
```

## License

MIT
