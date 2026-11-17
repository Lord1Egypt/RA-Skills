## Description:

帮助拥有品牌 IP、数字人或虚拟代言人的内容团队，把品牌定位、授权角色、产品日历、平台、节日和发布频率转化为 30 天栏目、脚本、场景、服装、图片视频任务和一致性看板。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, ecommerce, advertising, social media, and content operations teams use this skill to plan digital spokesperson campaigns and produce reviewable scripts, shot plans, prompts, task records, and acceptance checklists. It can also guide optional AI-HIVE image and video generation after human review of prompts, routing, budget, and authorized source materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scripts handle API keys, configurable endpoints, uploads, downloads, prompts, media, account metadata, and generated results.

Mitigation: Use only the official AI-HIVE endpoint, avoid untrusted AI_HIVE_BASE_URL or --base-url values, prefer limited-scope API keys, treat uploaded and downloaded media as sensitive, and verify output directories before running generation tasks.

Risk: Generated campaign content can include unverified brand claims, unauthorized reference material, or misleading digital spokesperson representations.

Mitigation: Confirm brand authorization, source-material rights, factual product claims, platform constraints, and human approval before submitting paid generation tasks or publishing outputs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/brand-avatar-content-calendar-ai-hive)
- [AI-HIVE chat entry](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API base endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured sections, inline bash commands, JSON task records, and review checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include prompts, scripts, storyboard and shot tables, AI-HIVE routing choices, task IDs, price snapshots, file locations, and continuity checks when generation tasks are used.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
