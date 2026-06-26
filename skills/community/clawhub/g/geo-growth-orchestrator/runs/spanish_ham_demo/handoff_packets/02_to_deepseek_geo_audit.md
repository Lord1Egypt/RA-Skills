# Handoff Packet: deepseek-geo-audit-skill

| Field | Value |
|---|---|
| target_skill | `deepseek-geo-audit-skill` |
| target_skill_path | `../deepseek-geo-audit-skill` |
| purpose | 评估 DeepSeek 对西班牙火腿在中国市场的理解和推荐 readiness |
| input_files | 01_brand_knowledge_base/brand_knowledge_base.mock.json, 03_gap_matrix/geo_gap_matrix.json |
| expected_outputs | deepseek_geo_audit_report.md |
| validation_rule | 报告必须明确无法判断项，不得编造真实模型排名 |
| next_stage_after_completion | Stage 3 Gap Matrix refresh |

## Copyable Instruction

```text
请使用本地 Skill `deepseek-geo-audit-skill`，读取以下输入文件：01_brand_knowledge_base/brand_knowledge_base.mock.json, 03_gap_matrix/geo_gap_matrix.json。目标是：评估 DeepSeek 对西班牙火腿在中国市场的理解和推荐 readiness。请输出：deepseek_geo_audit_report.md。所有内容必须标注待确认事实，发布前必须人工审核，不得承诺排名、收录或转化。
```
