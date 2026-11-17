## Description:

A Sparki skill variant for faceless/no-face video workflows that guides agents through API key setup, video upload, prompt-driven editing, and command usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create faceless explainers, automation-style videos, and narration-focused video edits through the Sparki service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, and API keys may be sent to the configured Sparki service, and changing --base-url can route them outside the declared Sparki domain.

Mitigation: Use SPARKI_API_KEY from the environment when possible, avoid --base-url unless the endpoint is fully trusted, and review before using private videos or sensitive account keys.

Risk: The security verdict is suspicious because the skill promotes a broad external video-editing workflow.

Mitigation: Review the generated commands before execution and confirm that sending the selected media and prompt to Sparki matches the user's intent.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/fischerlam/skills/faceless-video-zh)
- [Sparki homepage](https://sparki.io)
- [Sparki Telegram upload](https://t.me/Sparki_AI_bot/upload)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; executed Sparki CLI commands return JSON status data and may download video files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and SPARKI_API_KEY; supports local video paths or the Sparki Telegram upload flow.]

## Skill Version(s):

1.0.12 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
