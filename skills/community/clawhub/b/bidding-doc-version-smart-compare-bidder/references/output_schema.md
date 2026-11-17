# 报告结构与 findings JSON Schema

## findings.json（阶段⑤最终输出）

```json
{
  "meta": {
    "old_file": "A.docx",
    "new_file": "B.pdf",
    "old_date": "2026-05-01",
    "new_date": "2026-05-20",
    "bid_deadline": "2026-06-10",
    "generated_at": "ISO 时间"
  },
  "summary": {
    "total": 12,
    "by_sentiment": { "风险": 4, "中性": 5, "利好": 3 },
    "redline_count": 1
  },
  "items": [ { "classified 字段 + 阶段⑤追加字段" } ]
}
```

每条 item 字段：

| 字段 | 来源 | 说明 |
|------|------|------|
| clause_id | ③ | 条款编号或锚点 |
| change_type | ③ | 新增/删除/修改 |
| old_text / new_text | ③ | 新旧原文 |
| numeric_delta | ③ | 旧值→新值 单位 |
| context | ③ | 定位信息（章节/页码），报告回溯原文用 |
| dimension | ④ | 变更维度 |
| sentiment | ④ | 利好/风险/中性 |
| is_redline | ④ | 是否触碰强制性红线（独立布尔，可与「风险」并存，不互斥） |
| severity | ④ | 高/中/低 |
| impact | ④ | 实质影响一句话 |
| basis | ④ | 依据要点 |
| basis_source | ④ | IMA 出处 |
| action | ④ | 应对建议 |
| confidence | ④ | 0–1 |
| compliance_check | ⑤ | 核查结论 |
| timeliness_warning | ⑤ | 是否触发顺延 |
| final_severity | ⑤ | 最终严重度 |

## 报告章节（build_report.py 渲染）

1. 标题与元信息（原版/新版/日期/截止日）
2. 影响概览（按情感统计）
3. 红线与高风险明细（优先，含依据与建议）
4. 全部差异明细（条款定位 | 旧文 | 新文 | 变更类型 | 维度/情感 | 严重度 | 影响 | 依据 | 建议）
5. 时限校验提示（若有）
6. 免责声明

## 呈现顺序

- 先 Markdown 概览给用户；红线/风险条目置顶。
- 再提供 `.docx` 下载。
