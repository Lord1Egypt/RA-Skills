## Description:

A Sparki skill variant for caption-first video editing that helps agents add readable captions and tighten short-form video pacing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to route caption-focused video editing requests through Sparki, including adding readable subtitles, making videos understandable without sound, and producing caption-first short videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, and project metadata may be sent to Sparki for remote processing.

Mitigation: Use only with content approved for remote processing, and avoid local-only or privacy-sensitive video workflows.

Risk: API credentials can be persisted in local OpenClaw configuration.

Mitigation: Prefer SPARKI_API_KEY for session-scoped credentials and review stored configuration before sharing or reusing the environment.

Risk: A custom base URL can route requests to a different endpoint.

Mitigation: Avoid --base-url unless the endpoint is fully trusted and expected for the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/ai-caption-zh)
- [Publisher profile](https://clawhub.ai/user/fischerlam)
- [Sparki homepage](https://sparki.io)
- [Sparki Telegram upload](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Files]

**Output Format:** [Markdown guidance with shell commands, JSON CLI responses, and downloaded video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Sparki API key and remote processing through Sparki endpoints.]

## Skill Version(s):

1.0.12 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
