# Report Configuration Specification

完整的报告配置 JSON 字段说明。

## 根级字段

| 字段 | 类型 | 必需 | 说明 |
|------|------|------|------|
| `title` | string | ✅ | 报告主标题 |
| `subtitle` | string | | 报告副标题（如"机密"、"初稿"） |
| `metadata` | object | ✅ | 报告元信息 |
| `metadata.period` | string | ✅ | 报告周期（如"2025-Q1"） |
| `metadata.author` | string | | 作者/部门 |
| `metadata.date` | string | ✅ | 报告日期（YYYY-MM-DD） |
| `metadata.version` | string | | 版本号（默认"1.0"） |
| `company` | object | | 公司信息 |
| `company.name` | string | | 公司名称（显示在页眉） |
| `company.logo` | string | | Logo 路径（相对于报告目录） |
| `sections` | array | ✅ | 报告章节（有序） |
| `appendix` | array | | 附录章节 |

## Section 类型

### summary — 执行摘要

```json
{
  "title": "执行摘要",
  "type": "summary",
  "content": "本季度核心发现概述...",
  "highlights": [
    {"label": "营业收入", "value": "1,234万", "change": "+15.2%", "positive": true},
    {"label": "净利润", "value": "156万", "change": "-3.1%", "positive": false}
  ]
}
```

- `highlights`：关键指标卡片，最多 6 个
- `change`：支持 `+15.2%`、`-3.1%`、`持平` 等文本
- `positive`：控制颜色（绿色=正面，红色=负面）

### kpi-cards — KPI 指标卡

```json
{
  "title": "核心 KPI",
  "type": "kpi-cards",
  "items": [
    {"label": "毛利率", "value": "42.3%", "target": "40%", "status": "达标"},
    {"label": "周转天数", "value": "45天", "target": "<60天", "status": "达标"},
    {"label": "客户满意度", "value": "88%", "target": "90%", "status": "未达标"}
  ]
}
```

- `status`：`达标` / `未达标` / `关注`，影响卡片边框颜色

### chart — 图表

```json
{
  "title": "收入趋势",
  "type": "chart",
  "image": "charts/revenue_trend.png",
  "caption": "图1：各月营业收入及同比增长率",
  "analysis": "Q3 增速放缓，主要受..."
}
```

- `image`：图表文件路径（相对于报告输出目录）
- `caption`：图表说明文字
- `analysis`：图表解读（可选，作为图表下方的分析段落）

### table — 数据表格

```json
{
  "title": "收入明细",
  "type": "table",
  "columns": ["产品线", "Q1收入", "Q2收入", "同比增长"],
  "rows": [
    ["产品A", "100万", "120万", "+20%"],
    ["产品B", "80万", "75万", "-6.3%"],
    ["合计", "180万", "195万", "+8.3%"]
  ],
  "footnote": "单位：万元"
}
```

- `rows` 最后一行若为"合计"/"小计"，自动加粗
- `footnote`：表格脚注

### text — 纯文本段落

```json
{
  "title": "市场环境分析",
  "type": "text",
  "content": "## 行业趋势\n本季度行业整体..."
}
```

- `content` 支持 Markdown 子集（h2、bold、list）

### advisory — 风险与建议

```json
{
  "title": "风险提示与行动建议",
  "type": "advisory",
  "risks": [
    {"level": "高", "description": "应收账款增速高于收入增速"},
    {"level": "中", "description": "原材料价格波动风险"},
    {"level": "低", "description": "汇率波动对海外业务的影响"}
  ],
  "recommendations": [
    "加强应收账款管理，缩短账期至 30 天以内",
    "建立原材料价格对冲机制",
    "关注汇率走势，适时调整定价策略"
  ]
}
```

- `level`：`高`（红色）/ `中`（橙色）/ `低`（黄色）
- 风险按 level 降序排列
- 建议使用动词开头的行动句式

## 默认值与约定

- 数字格式：金额自动添加千分位分隔符，保留 2 位小数
- 百分比：保留 1 位小数
- 日期格式：YYYY-MM-DD
- 图表尺寸：默认 10×6 英寸，300 DPI
- 配色：使用 `assets/chart_theme.json` 中的商务色板
