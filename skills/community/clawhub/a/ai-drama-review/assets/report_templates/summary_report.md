# 合规审查摘要

**文件**: {{input_file}} | **时间**: {{generated_at}}

## 结论: {{overall_risk_level}} ({{overall_score}}/100)

{{#if violations}}
### 发现的问题:
{{#each violation_summary}}
- {{description}}
{{/each}}

### 建议:
{{#each remediation_suggestions}}
- {{this}}
{{/each}}
{{else}}
未发现明显合规风险。
{{/if}}

---
*仅供参考，不作为法律依据。*
