## Description:

Generate PPT with Baidu AI. Smart template selection based on content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tigertamvip](https://clawhub.ai/user/tigertamvip)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate PowerPoint presentations from a user-provided topic through Baidu AI, either with automatic template selection or a manually selected template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation topics, source content, and prompts are sent to Baidu AI PPT services.

Mitigation: Use only with content that is appropriate for the configured Baidu account and data-handling requirements; avoid confidential, regulated, or proprietary material unless approved.

Risk: BAIDU_API_KEY is required for API calls.

Mitigation: Keep the key protected, scoped to the intended use where possible, and avoid exposing it in logs or shared shell history.

Risk: Generated presentations may contain inaccurate or unsuitable content.

Mitigation: Review the final PPT before sharing or using it in business, customer-facing, or regulated contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tigertamvip/skills/ai-ppt-generator-1)
- [Baidu AI PPT API base endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/)
- [Baidu AI PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and streamed JSON status or final PPT URL output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; PPT generation may take 2-5 minutes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
