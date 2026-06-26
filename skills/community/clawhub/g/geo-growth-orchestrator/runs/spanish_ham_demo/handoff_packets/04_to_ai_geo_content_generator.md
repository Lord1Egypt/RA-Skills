# Handoff Packet: ai-geo-content-generator

| Field | Value |
|---|---|
| target_skill | `ai-geo-content-generator` |
| target_skill_path | `../AI-geo-content-generator` |
| purpose | 把 Gap Matrix 和 Content Task Plan 转成官网 FAQ、知乎/头条基础稿和可引用句库 |
| input_files | 01_brand_knowledge_base/brand_knowledge_base.mock.json, 04_content_task_plan/content_task_plan.json |
| expected_outputs | website_faq.md, zhihu_answer.md, toutiao_article.md, llms.txt, quote_sentence_library.md |
| validation_rule | 内容必须使用待确认占位，不得编造价格、渠道、资质 |
| next_stage_after_completion | Stage 6 Platform drafts |

## Copyable Instruction

```text
请使用本地 Skill `ai-geo-content-generator`，读取以下输入文件：01_brand_knowledge_base/brand_knowledge_base.mock.json, 04_content_task_plan/content_task_plan.json。目标是：把 Gap Matrix 和 Content Task Plan 转成官网 FAQ、知乎/头条基础稿和可引用句库。请输出：website_faq.md, zhihu_answer.md, toutiao_article.md, llms.txt, quote_sentence_library.md。所有内容必须标注待确认事实，发布前必须人工审核，不得承诺排名、收录或转化。
```
