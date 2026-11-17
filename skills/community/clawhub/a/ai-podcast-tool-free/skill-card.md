## Description:

将PDF、文本、链接转为双人对话播客，适合个人创作者快速制作音频内容。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, learners, and content distributors use this skill to turn PDFs, pasted text, notes, or links into a two-person conversational podcast through MagicPodcast.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Source text or PDF URLs may be sent to MagicPodcast for podcast generation.

Mitigation: Use this skill only with non-sensitive content unless external processing by MagicPodcast is approved.

Risk: The trigger language may match broader document-processing tasks than this podcast tool should handle.

Mitigation: Confirm the user wants podcast generation before requesting content or invoking MagicPodcast endpoints.

Risk: MagicPodcast API credentials are required for command examples.

Mitigation: Store API keys in environment variables or a local secrets mechanism and do not paste them into shared prompts, files, or logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-podcast-tool-free)
- [MagicPodcast skill platform](https://www.magicpodcast.app/skill-platform)
- [MagicPodcast app](https://www.magicpodcast.app/app)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return MagicPodcast job status, share URLs, and app URLs.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
