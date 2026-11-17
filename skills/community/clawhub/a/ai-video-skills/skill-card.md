## Description:

Build and execute skills.video video generation REST requests from OpenAPI specs. Use when user needs to create, debug, or document video generation calls on open.skills.video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chuyun](https://clawhub.ai/user/chuyun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to turn skills.video OpenAPI definitions into executable video-generation API requests, payload templates, and terminal-result workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts can send the bearer API key to arbitrary URLs when invoked with unsafe endpoint options.

Mitigation: Use only trusted publisher releases, prefer relative endpoints under https://open.skills.video/api/v1, avoid custom base URLs or full endpoint URLs unless intentional, and use limited or revocable API keys while monitoring credit usage.

## Reference(s):

- [skills.video Open Platform API Contract](artifact/references/open-platform-api.md)
- [Video Model Endpoints Snapshot](artifact/references/video-model-endpoints.md)
- [ClawHub skill page](https://clawhub.ai/chuyun/skills/ai-video-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated request templates, terminal generation status, retry guidance, or API key setup guidance.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
