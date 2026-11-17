## Description:

AI播客生成-专业版 helps enterprise teams and professional content creators turn documents and text into podcast assets with batch processing, custom dialogue styles, audio download, cover customization, and team collaboration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content teams, media organizations, publishers, and enterprise training teams use this skill to prepare commands, API requests, and configuration for converting text or document batches into podcast audio, cover assets, and downloadable deliverables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive documents, training material, publishing content, or customer material may be sent to an external podcast-generation API.

Mitigation: Use only with user-approved content, confirm submitted text may leave the local environment, and prefer the stated private deployment option for confidential enterprise material.

Risk: The skill's broad trigger and shell/API workflow can operate on unintended documents or unsafe command inputs.

Mitigation: Review generated commands before execution, keep API keys in environment variables or managed secrets, and avoid interpolating untrusted input into shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/ai-podcast-tool-pro)
- [MagicPodcast API endpoint](https://api.magicpodcast.app)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with bash commands, JSON payloads, environment-variable configuration, and file paths for generated podcast assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce MP3 or WAV audio downloads, cover image files, job identifiers, structured status responses, and execution logs through external API workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
