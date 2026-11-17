## Description:

Generate PPT with Baidu Wenku AI. Smart template selection based on content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ide-rea](https://clawhub.ai/user/ide-rea)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to generate Baidu Wenku AI presentations from a topic, either by selecting a template or by using automated template selection.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPT topics and optional web content are sent to Baidu's API using the configured BAIDU_API_KEY.

Mitigation: Do not submit secrets, private business plans, regulated data, or other sensitive content unless the user's Baidu account and policies allow that use.

Risk: The skill depends on a live external API and credentialed network access to complete generation.

Mitigation: Confirm BAIDU_API_KEY is configured for the intended account and expect generation to fail or delay if the Baidu service is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ide-rea/skills/ai-ppt-generator)
- [Baidu Qianfan AI PPT API endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/)
- [Baidu Qianfan PPT theme endpoint](https://qianfan.baidubce.com/v2/tools/ai_ppt/get_ppt_theme)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [Markdown guidance with shell commands and JSON status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and BAIDU_API_KEY; final output is a generated PPT URL when the Baidu API reports completion.]

## Skill Version(s):

1.1.5 (source: server release metadata; artifact _meta.json reports 1.1.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
