---
name: workflow
description: |
  编排 CreatiVault 达人发现、相似扩展、搜索结果 CSV 导出、视频搜索和拆解、邮件建联与跟进。
  用于找达人并发合作邮件、批量建联，或从视频定位发布达人并联系合作等多步骤需求。
compatibility: Node.js 20.6+
metadata:
  layer: workflow
  parent: creator-scraper-cv
---

# 达人合作工作流

根据用户目标选择剧本，复用子 Skill 的参数说明、权限规则和实际返回结果。

| 用户目标 | 剧本 |
| --- | --- |
| 按目标画像找达人，可补充相似账号，再整理名单、确认邮件并跟进 | [达人合作](workflows/full-campaign.md) |
| 已有收件人或只需按条件找名单，再批量发送邮件 | [批量建联](workflows/batch-outreach.md) |
| 找相关视频并拆解，再联系发布达人 | [内容合作](workflows/brand-video-to-outreach.md) |

## 执行原则

- 从用户已有的名单、主页或视频链接开始，执行完成目标所需的步骤。搜索和拆解使用对应子 Skill 和 CreatiVault OpenAPI，复用同一次对话已获取的结果。
- 传递达人数据时保留平台、达人 ID、主页和实际返回的邮箱。缺少必要字段时，先用达人搜索补齐可查资料，或列出未命中的候选。
- 按剧本确认待拆解的视频。邮件发送遵循 [邮件建联](../outreach/creator-outreach/SKILL.md) 的确认规则，展示收件人、主题和正文。
- 按用户确认的条件执行。搜索命中不足时报告实际数量，调整条件需要用户确认。
- 以接口结果报告执行进度。异步任务仍在处理中时保留任务编号，已失败则说明原因。发送结果不明确时先查原任务，避免重复发信。

可交付搜索结果、用户确认的名单、视频拆解摘要、邮件发送结果与跟进待办。用户需要导出时，使用 [达人搜索](../discovery/creator-search/SKILL.md) 的 CSV 导出说明。
