## Description:

综合生成工具-专业版 helps agents use dlazy workflows for image, video, audio, vector asset generation, and multi-step media pipelines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content teams, and automation workflow builders use this skill to prepare dlazy CLI commands and batch pipelines for multimedia generation. It is intended for image, video, audio, SVG, and chained media production workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for command execution and file read/write access for CLI-driven media workflows.

Mitigation: Install only when dlazy media generation is intended, review generated commands before execution, and run workflows in an appropriate sandbox.

Risk: The skill depends on external API calls and may trigger paid media generation usage.

Mitigation: Configure the dlazy API key carefully, monitor account balance or quotas, and use dry runs where available before starting costly batch jobs.

Risk: Batch scenario data may be interpolated into sample automation commands.

Mitigation: Validate scenario inputs before use and avoid feeding untrusted batch data into automation scripts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/thcjp/skills/dlazy-gen-tool-pro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, Python, and JSON examples for dlazy CLI workflows]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dlazy command sequences, pipeline references, generated workflow code, and API key configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
