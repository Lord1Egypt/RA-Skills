## Description:

Generate PPT with Baidu AI. Smart template selection based on content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[binbin](https://clawhub.ai/user/binbin)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate PowerPoint presentations from a topic with either automatic Baidu AI template selection or a chosen template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Presentation topics, generated outlines, and optional web_content are sent to Baidu AI for processing.

Mitigation: Avoid submitting confidential, regulated, or secret material unless the user's organization permits Baidu processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/binbin/skills/ai-ppt-generator-1-1-3)
- [Baidu AI PPT API](https://qianfan.baidubce.com/v2/tools/ai_ppt/)
- [Baidu AI PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON status output that includes a generated PPT URL when complete.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; generation may take 2-5 minutes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
