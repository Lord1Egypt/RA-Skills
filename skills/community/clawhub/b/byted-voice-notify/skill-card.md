## Description:

Sends voice notifications to specified phone numbers using Volcengine Voice Service APIs, including number-pool lookup and voice-resource selection by language or keyword.

This skill is ready for commercial/non-commercial use.

## Publisher:

[volcengine-skills](https://clawhub.ai/user/volcengine-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to have an agent query Volcengine voice resources and number pools, then send a voice notification to a supplied phone number.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place real phone calls through a configured Volcengine voice-service account and may act on broad prompts without an explicit confirmation step.

Mitigation: Require confirmation of the phone number, selected voice resource, number pool, provider, and expected cost or privacy impact before every send action.

## Reference(s):

- [Volcengine signing mechanism](https://www.volcengine.com/docs/6358/166389?lang=zh)
- [Query available voice resources](https://www.volcengine.com/docs/6358/1722078?lang=zh)
- [Send a single voice notification](https://www.volcengine.com/docs/6358/172952?lang=zh)
- [Query number pool list](https://www.volcengine.com/docs/6358/173339?lang=zh)
- [ClawHub skill page](https://clawhub.ai/volcengine-skills/skills/byted-voice-notify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, JSON, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires VOLCENGINE_ACCESS_KEY and VOLCENGINE_SECRET_KEY environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
