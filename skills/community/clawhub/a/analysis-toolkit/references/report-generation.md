# 报告生成

## 适用场景

将任一分析场景的结果（图表、数据表、结论）组装为结构化Word 报告。

## 使用方式

```python
from scripts.docgen.report_gen import generate_report, export_to_pdf

sections = [
    {"type": "heading", "level": 1, "title": "一、室内精密度分析"},
    {"type": "chart", "title": "各水平阳性率对比", "figure": fig1,
     "analysis": "精密度分析结论..."},
    {"type": "table", "title": "统计明细表", "dataframe": df_result},
    {"type": "text", "content": "综合结论..."},
    {"type": "page_break"},
    {"type": "heading", "level": 1, "title": "二、标准曲线"},
    ...
]

generate_report(sections, "分析报告.docx", title="质控分析报告")
export_to_pdf("分析报告.docx")
```

## 章节类型

| type | 参数 | 说明 |
|------|------|------|
| `heading` | level, title | 章节标题 |
| `chart` | title, figure, analysis | 图表+结论 |
| `table` | title, dataframe | 数据表格 |
| `text` | content | 文本段落 |
| `page_break` | (无) | 分页 |
