---
name: financial-report-render-claw
description: "将数据分析结果转化为精美、可汇报的正式报告文件。激活场景：用户已有分析结论或数据结果，需要生成正式报告、排版文档、制作汇报材料、导出 PDF/Word/PPT/HTML 等格式文件。也适用于用户要求将分析结果美化、整理成报告、生成图表、制作仪表板截图、排版导出等场景。核心价值：交付即用——直接生成可供汇报的正式文件，无需人工排版。触发关键词：生成报告、做报告、出报告、排版、导出 PDF、导出 Word、生成 PPT、美化报告、渲染报告、正式报告、汇报材料、财务报告、经营报告、月报、季报、年报、制作报告、整理报告、格式化输出、生成图表、可视化报告、dashboard、仪表板。"
---

# 财务报表渲染虾 🦐

将数据分析结果转化为精美、可汇报的正式文件。交付即用，无需人工排版。

## 工作流程

### 1. 接收分析结果

明确输入：
- **数据来源**：已有分析结果（Markdown 文本、JSON 数据、Python DataFrame、或直接描述的结论）
- **报告类型**：财务报告、经营分析、月报/季报/年报、项目汇报、数据看板
- **输出格式**：PDF / Word（.docx） / HTML / Markdown / 图片（PNG）
- **受众**：管理层、投资人、内部团队、外部审计？（决定措辞和详略）

如果输入不完整，先向用户确认缺少的部分。

### 2. 规划报告结构

根据报告类型选择模板结构：

| 报告类型 | 推荐结构 |
|---------|---------|
| 财务报告 | 执行摘要 → 核心指标 → 收入分析 → 成本分析 → 利润分析 → 现金流 → 风险提示 → 建议 |
| 经营分析 | 执行摘要 → 业务概览 → KPI 达成 → 趋势分析 → 问题诊断 → 行动建议 |
| 月报/季报 | 本期概览 → 同比环比 → 重点项目 → 下期计划 |
| 项目汇报 | 项目背景 → 进展概览 → 关键成果 → 问题与风险 → 下一步 |

详细模板规范见 `references/report-templates.md`。

### 3. 生成图表

使用 `scripts/chart_generator.py` 生成专业图表：

```bash
# 折线图（趋势）
python3 scripts/chart_generator.py line -i {数据文件} -x {X轴列} -y {Y轴列} -o {输出路径} --title "{标题}"

# 柱状图（对比）
python3 scripts/chart_generator.py bar -i {数据文件} -x {分类列} -y {数值列} -o {输出路径} --title "{标题}" [--horizontal] [--stacked]

# 饼图（占比）
python3 scripts/chart_generator.py pie -i {数据文件} -x {分类列} -y {数值列} -o {输出路径} --title "{标题}"

# 组合图（柱+线）
python3 scripts/chart_generator.py combo -i {数据文件} -x {X轴列} -y-bar {柱状列} -y-line {折线列} -o {输出路径} --title "{标题}"
```

图表样式规范：
- 配色使用 `assets/chart_theme.json` 中的专业商务色板
- 中文字体自动适配（macOS: PingFang SC，Linux: Noto Sans CJK）
- 尺寸默认 10x6 英寸，300 DPI，适合印刷
- 图表标题使用报告语言（中文报告用中文标题）

### 4. 渲染报告文件

#### HTML 报告（推荐，支持丰富排版）

```bash
python3 scripts/report_renderer.py html {report_config.json} -o {输出目录} --theme professional
```

HTML 报告特点：
- 响应式布局，桌面和移动端均可阅读
- 支持图表嵌入、数据表格、高亮框
- 内置打印优化 CSS，Ctrl+P 可直接导出 PDF
- 可选深色/浅色主题

#### PDF 报告

方式一：HTML 转 PDF（推荐）
```bash
python3 scripts/report_renderer.py html {report_config.json} -o {输出目录} --theme professional
# 然后使用系统工具转换，或让用户在浏览器中打印为 PDF
```

方式二：直接生成 PDF（需 weasyprint）
```bash
python3 scripts/report_renderer.py pdf {report_config.json} -o {输出路径} --theme professional
```

#### Word 报告（.docx）

```bash
python3 scripts/report_renderer.py docx {report_config.json} -o {输出路径}
```

Word 报告特点：
- 使用标准样式，兼容 Microsoft Office 和 WPS
- 图表以高分辨率 PNG 嵌入
- 目录自动生成
- 页眉页脚包含公司名称和日期

### 5. 报告配置

所有格式共用相同的 JSON 配置结构：

```json
{
  "title": "2025年度财务分析报告",
  "subtitle": "内部管理报告 · 机密",
  "metadata": {
    "period": "2025-01 至 2025-12",
    "author": "数据分析部门",
    "date": "2025-01-15",
    "version": "1.0"
  },
  "company": {
    "name": "XX有限公司",
    "logo": "assets/logo.png"
  },
  "sections": [
    {
      "title": "执行摘要",
      "type": "summary",
      "content": "本期实现营业收入 1,234 万元，同比增长 15.2%...",
      "highlights": [
        {"label": "营业收入", "value": "1,234万", "change": "+15.2%", "positive": true},
        {"label": "净利润", "value": "156万", "change": "+8.7%", "positive": true}
      ]
    },
    {
      "title": "核心指标",
      "type": "kpi-cards",
      "items": [
        {"label": "毛利率", "value": "42.3%", "target": "40%", "status": "达标"},
        {"label": "应收账款周转天数", "value": "45天", "target": "<60天", "status": "达标"}
      ]
    },
    {
      "title": "收入趋势分析",
      "type": "chart",
      "image": "charts/revenue_trend.png",
      "caption": "图1：2025年各月营业收入及同比增长率",
      "analysis": "Q3收入增速放缓，主要受..."
    },
    {
      "title": "成本结构",
      "type": "chart",
      "image": "charts/cost_structure.png",
      "caption": "图2：成本构成分析",
      "analysis": "原材料成本占比 38%，同比上升 2.1 个百分点..."
    },
    {
      "title": "风险与建议",
      "type": "advisory",
      "risks": [
        {"level": "高", "description": "应收账款增速高于收入增速，关注回款风险"},
        {"level": "中", "description": "原材料价格波动可能影响毛利率"}
      ],
      "recommendations": [
        "加强应收账款管理，缩短账期",
        "建立原材料价格对冲机制"
      ]
    }
  ],
  "appendix": [
    {"title": "数据来源说明", "content": "本报告数据来源于公司财务系统..."},
    {"title": "计算方法", "content": "同比增长率 = (本期 - 去年同期) / 去年同期 × 100%"}
  ]
}
```

详细的 section type 和配置选项见 `references/report-config-spec.md`。

### 6. 质量检查

渲染完成后，检查：
- [ ] 所有图表清晰可读，无乱码
- [ ] 数字格式统一（千分位分隔、小数位数）
- [ ] 同比/环比标注完整
- [ ] 页面布局无溢出、无截断
- [ ] 公司名称、日期等元信息正确
- [ ] 如有要求，确认敏感信息已脱敏

## 设计原则

1. **专业优先**：商务配色、清晰层级、适当留白，拒绝花哨
2. **数据准确**：所有数字必须与源数据一致，图表标注数据来源
3. **结论前置**：执行摘要放在最前面，让读者 30 秒抓住重点
4. **一图胜千言**：能用图表表达的，不用纯文字堆砌
5. **可复现**：保存配置文件，下次更新数据只需替换数据源

## 依赖

- Python 3.8+
- 必需：`pandas`、`matplotlib`、`jinja2`
- 可选：`weasyprint`（PDF 直出）、`python-docx`（Word 输出）
- 运行前检查依赖：`pip3 list | grep -E "pandas|matplotlib|jinja2"`

## 与数据分析虾的协作

本 skill 专注**渲染和排版**，与 `auto-data-analysis-claw`（数据分析虾）形成上下游关系：
- 数据分析虾完成数据清洗、分析计算、产出结论
- 本 skill 接收分析结论，负责排版、图表生成、文件导出

两个 skill 可在同一个对话中串联使用，也可独立工作。
