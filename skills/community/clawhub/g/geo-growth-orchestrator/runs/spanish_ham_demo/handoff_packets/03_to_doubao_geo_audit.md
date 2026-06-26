# Handoff Packet: doubao-geo-audit-skill

| Field | Value |
|---|---|
| target_skill | `doubao-geo-audit-skill` |
| target_skill_path | `../geo-analysis-doubao` |
| purpose | 评估 Doubao 对西班牙火腿消费场景、送礼场景和本地化内容的理解 |
| input_files | 01_brand_knowledge_base/brand_knowledge_base.mock.json |
| expected_outputs | doubao_geo_audit_report.md |
| validation_rule | 报告必须包含总体评分、最大问题、优化建议和 FAQ |
| next_stage_after_completion | Stage 3 Gap Matrix refresh |

## Copyable Instruction

```text
请使用本地 Skill `doubao-geo-audit-skill`，读取以下输入文件：01_brand_knowledge_base/brand_knowledge_base.mock.json。目标是：评估 Doubao 对西班牙火腿消费场景、送礼场景和本地化内容的理解。请输出：doubao_geo_audit_report.md。所有内容必须标注待确认事实，发布前必须人工审核，不得承诺排名、收录或转化。
```
