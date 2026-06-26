# Handoff Packet: brand-knowledge-base-builder

| Field | Value |
|---|---|
| target_skill | `brand-knowledge-base-builder` |
| target_skill_path | `../Knowledge-Base-Builder/brand-knowledge-base-builder` |
| purpose | 构建西班牙火腿品类与品牌知识母库 |
| input_files | 00_input/spanish_ham_input.json |
| expected_outputs | brand_knowledge_base.json, faq.md, llms.txt |
| validation_rule | 检查缺失字段是否标记为待确认 |
| next_stage_after_completion | Stage 2 DeepSeek / Doubao GEO audit |

## Copyable Instruction

```text
请使用本地 Skill `brand-knowledge-base-builder`，读取以下输入文件：00_input/spanish_ham_input.json。目标是：构建西班牙火腿品类与品牌知识母库。请输出：brand_knowledge_base.json, faq.md, llms.txt。所有内容必须标注待确认事实，发布前必须人工审核，不得承诺排名、收录或转化。
```
