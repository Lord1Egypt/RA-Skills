## Description:

AI music generation assistant powered by MakebestMusic for creating AI-generated songs, audio tracks, and instrumental music from text prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sthk-mbm](https://clawhub.ai/user/sthk-mbm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and creators use this skill to generate vocal or instrumental AI music from text prompts and check the status of submitted music generation tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An undocumented MBM_API_BASE environment override can send the user's MakeBestMusic API key and prompts to an arbitrary server if the runtime environment is influenced.

Mitigation: Use only in an environment where other tools or workspace configuration cannot set MBM_API_BASE, or ask the publisher to remove or validate the override so credentials are sent only to the official HTTPS MakeBestMusic API.

Risk: Music prompts and generation status requests are sent to the MakeBestMusic service using the configured API key.

Mitigation: Review prompts before submission and avoid sending sensitive or confidential content unless the service is approved for that data.

## Reference(s):

- [Ai Music on ClawHub](https://clawhub.ai/sthk-mbm/skills/ai-music)
- [MakeBestMusic](https://makebestmusic.com/?pid=PIDcLjhgCXUQ)
- [MakeBestMusic API Base](https://api.makebestmusic.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell command invocations and JSON status responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a MakeBestMusic apiKey; completed generations return hosted music links when available.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
