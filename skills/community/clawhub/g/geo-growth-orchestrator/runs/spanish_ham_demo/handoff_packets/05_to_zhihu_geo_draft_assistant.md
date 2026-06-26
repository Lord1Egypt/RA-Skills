# Handoff Packet: zhihu-geo-draft-assistant

| Field | Value |
|---|---|
| target_skill | `zhihu-geo-draft-assistant` |
| target_skill_path | `../zhihu-geo-draft-assistant` |
| purpose | 生成 5 个知乎问答/专栏草稿 |
| input_files | 04_content_task_plan/content_task_plan.json, 05_content_assets/zhihu_answer_seed.mock.md |
| expected_outputs | zhihu_questions.md, zhihu_answer_long.md, zhihu_answer_short.md, zhihu_titles.md, zhihu_publish_checklist.md |
| validation_rule | 必须保留人工审核清单，不能自动发布 |
| next_stage_after_completion | Stage 7 Delivery package |

## Copyable Instruction

```text
请使用本地 Skill `zhihu-geo-draft-assistant`，读取以下输入文件：04_content_task_plan/content_task_plan.json, 05_content_assets/zhihu_answer_seed.mock.md。目标是：生成 5 个知乎问答/专栏草稿。请输出：zhihu_questions.md, zhihu_answer_long.md, zhihu_answer_short.md, zhihu_titles.md, zhihu_publish_checklist.md。所有内容必须标注待确认事实，发布前必须人工审核，不得承诺排名、收录或转化。
```
