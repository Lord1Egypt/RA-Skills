## Description:

AI video auto pipeline: from idea to final video in one command, covering script generation, repair, assets, video, audio, and subtitles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jinxuchen2020](https://clawhub.ai/user/jinxuchen2020)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, operators, and developers use this skill to turn prompts, documents, or URLs into structured short-video projects and run an automated pipeline through final video output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can send local media, prompts, project metadata, or task data to external services.

Mitigation: Review configured providers before use, avoid sensitive local paths or internal URLs, and send only content intended for external processing.

Risk: The workflow can install dependencies and launch long-running generation jobs.

Mitigation: Run in an isolated project and virtual environment, review commands before execution, and pin dependencies before production use.

Risk: Optional GitHub image hosting can expose generated assets depending on repository ownership and visibility.

Mitigation: Use only a repository the user owns and has reviewed for appropriate access controls.

Risk: Optional Feishu task tracking can write project status outside the local workspace.

Mitigation: Use the local tracker unless Feishu writes are explicitly intended and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jinxuchen2020/skills/ai-video-auto-generator)
- [Agnes AI platform](https://platform.agnes-ai.com)
- [Provider configuration](references/provider-config.md)
- [Setup guide](references/setup-guide.md)
- [End-to-end walkthrough](references/e2e-walkthrough.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, JSON project specifications, Python and shell commands, and generated project files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger external AI media generation services and local video assembly when the user runs the generated workflow.]

## Skill Version(s):

2.7.1 (source: server release metadata; artifact frontmatter reports 2.7.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
