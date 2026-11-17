## Description:

Helps agents use Volcengine Doubao Seedream, Seedance, and Seed Vision APIs for image generation, video generation, visual understanding, task management, and configuration guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ai-lychee](https://clawhub.ai/user/ai-lychee)

### License/Terms of Use:

MIT

## Use Case:

Developers and content teams use this skill to guide AI agents through Doubao image, video, and vision API workflows, including parameter validation, configuration, task tracking, and result download guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: One-click installation from a mutable branch can run code that has not been reviewed for the release being installed.

Mitigation: Review the installer source from a fixed release or commit before installation.

Risk: API keys can be exposed through persistent config files or unsafe handling.

Mitigation: Use a scoped Volcengine API key and prefer a temporary environment variable or secret manager over storing credentials in project files.

Risk: A project .volcengine/config.yaml file can override the API base URL and send credentials or requests to an unintended endpoint.

Mitigation: Verify base_url configuration before use and remove untrusted project-level overrides.

Risk: Generated downloads can be written into unexpected locations if output paths are not constrained.

Mitigation: Keep generated media downloads inside a dedicated output directory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ai-lychee/skills/doubao-seedream-seedance-skill)
- [Volcengine Ark console](https://console.volcengine.com/ark)
- [Publisher profile](https://clawhub.ai/user/ai-lychee)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, API workflow descriptions, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide agents to create API requests, validate media-generation parameters, track task state, and download generated media into an output directory.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
