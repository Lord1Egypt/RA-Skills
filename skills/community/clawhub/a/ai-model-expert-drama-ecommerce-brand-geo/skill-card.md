## Description:

Helps brand, content, short-drama, e-commerce, marketing, and AI-search operations teams turn e-commerce GEO and brand visibility goals into structured plans, evidence fields, generation tasks, and AI-HIVE image and video workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External brand, e-commerce, content, short-drama, and AI-search teams use this skill to plan GEO/AEO content, structure evidence-backed answers, create reusable project blueprints, and generate supporting image or video assets through AI-HIVE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be sent to arbitrary configured endpoints when a custom AI_HIVE_BASE_URL or base_url is used.

Mitigation: Use the official AI-HIVE endpoint unless the custom endpoint is fully trusted; use a dedicated revocable API key and rotate it if exposed.

Risk: Generated brand, product, pricing, certification, or AI-search visibility claims can be inaccurate or misleading.

Mitigation: Use only user-confirmed facts and source records, mark unknowns clearly, preserve update timestamps, and avoid promising third-party AI-search ranking or citation.

Risk: Downloaded task results may come from URLs returned by generation tasks.

Mitigation: Download only expected results to a controlled directory, scan files before reuse, and do not execute downloaded content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/ai-model-expert-drama-ecommerce-brand-geo)
- [AI-HIVE homepage](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE APIs, upload media, poll generation tasks, and optionally download generated image or video results.]

## Skill Version(s):

1.0.0 (source: server release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
