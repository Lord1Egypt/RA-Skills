# 图表化 PDF 报告 · spec 结构说明

生成命令：

```bash
PY="python3"
S="<skill-dir>/scripts"
"$PY" "$S/report_pdf.py" --spec report.json --out ./报告.pdf
"$PY" "$S/pdf_verify.py" --pdf ./报告.pdf --pages 3 --charts 3 --tables 1 \
      --expect-text "保本ROI" "1.85" --json-out verify.json
```

## 顶层字段

```json
{
  "title": "报告标题",
  "subtitle": "副标题（SKU/平台/数据区间）",
  "meta": {"生成时间": "2026-09-27", "数据来源": "抖音罗盘", "口径": "支付买家数"},
  "blocks": [ ... ]
}
```

## blocks 类型

| type | 字段 | 说明 |
|---|---|---|
| `h1` / `h2` | `text` | 一级/二级标题 |
| `p` | `text`, `size`(默认10.5), `muted`(bool) | 段落，自动换行 |
| `bullets` | `items[]`, `size` | 项目符号列表 |
| `kv` | `items[[k,v],...]`, `per_row`(默认3), `h` | 指标卡片 |
| `callout` | `text`, `tone`: `warn`/`ok`/`info` | 提示框（结论/风险） |
| `bar` | `title`, `labels[]`, `values[]`, `unit`, `h`, `colors[]` | 柱状图（正值红、负值绿） |
| `line` | `title`, `labels[]`, `series[{name,values}]`, `unit`, `h` | 折线图（多系列） |
| `pie` | `title`, `labels[]`, `values[]`, `size` | 饼图（占比） |
| `table` | `header[]`, `rows[[...]]`, `widths[]`, `size` | 表格（自动换行分页） |
| `checklist` | `items[{ok,text}]` | 打勾清单（交付复核用） |
| `spacer` | `h` | 留白 |

## 配色语义（与 PALETTE 一致）

- `up` 红 = 增长 / 正向；`down` 绿 = 下降 / 负向（中国区财务惯例）
- `brand` 蓝 = 主色；`accent` 橙 = 次系列；`warn` 橙红 = 风险

## 验真可校验项（脚本自动）

- 内容流内写入 `% CHART:bar:标题` / `% CHART:line:...` / `% CHART:pie:...` / `% CHART:table:...` 注释标记
- `pdf_verify.py` 统计图表/表格数量、页数、字体嵌入、文本层可提取关键词

## 字段来源要求

报告里所有数值必须来自：① 用户提供的真实数据；② 脚本输出（JSON 字段直接引用）。**禁止在写 spec 时手改数值。**
