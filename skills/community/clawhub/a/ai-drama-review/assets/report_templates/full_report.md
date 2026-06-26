# AI短剧合规审查报告

**报告 ID**: {{report_id}}
**生成时间**: {{generated_at}}
**输入文件**: {{input_file}}

## 总体评估

| 项目 | 结果 |
|------|------|
| 风险等级 | {{overall_risk_level}} |
| 合规得分 | {{overall_score}}/100 |

## 违规摘要

{{#each violation_summary}}
- [{{severity}}] **{{type}}**: {{description}}
{{/each}}

## 版权侵权检测

- 总段落数: {{copyright.total_paragraphs}}
- 可疑段落: {{copyright.suspicious_paragraphs}}
- 最高相似度: {{copyright.max_similarity_score}}
- 风险等级: {{copyright.risk_level}}

## 年龄分级合规

- 建议分级: {{age_rating.suggested_rating}}
- 目标分级: {{age_rating.target_rating}}
- 是否合规: {{age_rating.is_compliant}}
- 总命中数: {{age_rating.total_hits}}

## 小说改编检测

- 偏离度: {{adaptation.deviation_score}}/100
- 改编类型: {{adaptation.adaptation_type}}
- 总偏离数: {{adaptation.total_deviations}}

## 整改建议

{{#each remediation_suggestions}}
{{@index}}. {{this}}
{{/each}}

---
*本报告由 ai-drama-review 自动生成，仅供参考，不作为法律依据。*
