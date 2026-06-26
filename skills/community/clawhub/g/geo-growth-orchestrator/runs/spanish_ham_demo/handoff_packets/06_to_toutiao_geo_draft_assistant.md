# Handoff Packet: toutiao-geo-draft-assistant

| Field | Value |
|---|---|
| target_skill | `toutiao-geo-draft-assistant` |
| target_skill_path | `../toutiao-geo-draft-assistant` |
| purpose | 生成 5 个今日头条科普/场景文章草稿 |
| input_files | 04_content_task_plan/content_task_plan.json, 05_content_assets/toutiao_article_seed.mock.md |
| expected_outputs | toutiao_article.md, toutiao_titles.md, toutiao_summary.md, toutiao_keywords.md, toutiao_publish_checklist.md |
| validation_rule | 必须通俗可读，不能编造故事和数据 |
| next_stage_after_completion | Stage 7 Delivery package |

## Copyable Instruction

```text
请使用本地 Skill `toutiao-geo-draft-assistant`，读取以下输入文件：04_content_task_plan/content_task_plan.json, 05_content_assets/toutiao_article_seed.mock.md。目标是：生成 5 个今日头条科普/场景文章草稿。请输出：toutiao_article.md, toutiao_titles.md, toutiao_summary.md, toutiao_keywords.md, toutiao_publish_checklist.md。所有内容必须标注待确认事实，发布前必须人工审核，不得承诺排名、收录或转化。
```
