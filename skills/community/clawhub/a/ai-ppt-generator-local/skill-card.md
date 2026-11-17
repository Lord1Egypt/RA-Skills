## Description:

Generate PPT with Baidu Wenku AI. Smart template selection based on content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuliyuan2026](https://clawhub.ai/user/wuliyuan2026)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate PowerPoint presentations from a topic with either selected or automatically matched Baidu Wenku AI templates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation topics and optional content are sent to Baidu's remote AI PPT service using the user's Baidu API key.

Mitigation: Use only with content permitted by the user's organization and avoid submitting secrets, regulated data, private business plans, or personal information.

Risk: Generated presentations may reflect limitations or inaccuracies from the remote generation service.

Mitigation: Review the final PPT before sharing or relying on it for business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuliyuan2026/skills/ai-ppt-generator-local)
- [Baidu Qianfan AI PPT API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/)
- [Baidu Qianfan AI PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires BAIDU_API_KEY and may return a hosted PPT URL after streamed generation completes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
