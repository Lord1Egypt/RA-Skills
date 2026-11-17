## Description:

面向 Vlog 场景的 Sparki skill 变体，沿用最新版官方 Sparki 安装、API key、上传和命令说明，同时保留 Vlog 场景定位。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fischerlam](https://clawhub.ai/user/fischerlam)

### License/Terms of Use:

MIT-0

## Use Case:

External creators and agents use this skill to turn raw daily-life, travel, lifestyle, and creator-style footage into Vlog-oriented edits through Sparki commands and prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos and prompts are uploaded to Sparki for processing.

Mitigation: Confirm the user is comfortable sending that media to Sparki, avoid private footage, and offer local video-processing options before upload when privacy matters.

Risk: Credential handling includes a saved config file and an environment variable.

Mitigation: Prefer SPARKI_API_KEY for temporary use, inspect permissions on ~/.openclaw/config/sparki.json, and avoid storing keys when not needed.

Risk: A custom --base-url can redirect API key validation and media requests away from the declared Sparki service.

Mitigation: Use the default Sparki endpoint unless the alternate endpoint is fully trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fischerlam/skills/ai-vlog-editor-zh)
- [Publisher profile](https://clawhub.ai/user/fischerlam)
- [Sparki homepage](https://sparki.io)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with inline shell commands; Sparki CLI commands return JSON and may download MP4 files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv and SPARKI_API_KEY; reads local video paths, uploads selected MP4 or MOV files to Sparki, and writes configuration or output videos under OpenClaw paths.]

## Skill Version(s):

1.0.12 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
