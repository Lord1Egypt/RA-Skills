## Description:

Creates local AI team directory structures and Markdown configuration files for projects with single, dual, or custom team modes and Chinese or English output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sylvanxiao](https://clawhub.ai/user/sylvanxiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to scaffold local ai-team folders, team member documentation, workflow documentation, and progress tracking for generic, web app, ecommerce, or mobile app projects without external services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill writes generated files and optional logs to filesystem paths selected at runtime, and the security summary says file-writing behavior is broader than documentation says.

Mitigation: Run it only on trusted project directories, avoid elevated privileges, avoid external --log-file paths, and review generated ai-team documentation before relying on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sylvanxiao/skills/auto-create-ai-team)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown files and JSON configuration generated under a local ai-team directory, plus CLI status text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes files under the user-specified project path; supports zh/en language output and single, dual, or custom team modes.]

## Skill Version(s):

2.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
