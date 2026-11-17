## Description:

Guides agents to use the Cutrix Python SDK for video translation, dubbing, subtitles, task polling, and API error handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wallacerao](https://clawhub.ai/user/wallacerao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to generate guidance, Python code, installation commands, and configuration for submitting Cutrix video translation tasks, polling task status, and handling subtitle-related parameters.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, audio, subtitles, and task metadata may be sent to Cutrix for cloud processing.

Mitigation: Use the skill only when that data transfer is acceptable for the user's content and environment.

Risk: API keys and ClawHub tokens can be exposed if copied into code, logs, or shared transcripts.

Mitigation: Store secrets outside generated code, prefer environment variables such as CUTRIX_API_KEY, and remove credentials from logs and transcripts.

Risk: The SDK dependency may change over time, which can affect reproducibility or supply-chain controls.

Mitigation: In controlled environments, pin and hash-lock the SDK dependency before deployment.

## Reference(s):

- [Cutrix](https://www.cutrix.cc)
- [Cutrix Video Translate on ClawHub](https://clawhub.ai/wallacerao/skills/cutrix-video-translate)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include SDK installation steps, environment-variable guidance, task polling patterns, language-code tables, and error-handling examples.]

## Skill Version(s):

v1.1.4 (source: ClawHub release evidence; artifact frontmatter says 1.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
