## Description:

Publishes OpenClaw skills to the ClawHub marketplace, covering pre-publish checks, personal information sanitization, version selection, CLI publishing, and post-publish records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jini92](https://clawhub.ai/user/jini92)

### License/Terms of Use:


## Use Case:

Developers and skill maintainers use this skill to prepare and publish OpenClaw skills to ClawHub with language, sanitization, versioning, and CLI workflow checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes personal-account URLs and local C:\MAIBOT paths that may not fit other users' environments.

Mitigation: Replace the account URL and local paths with the intended publisher profile and workspace paths before using the workflow.

Risk: The post-publish record updates target private memory and Obsidian locations.

Mitigation: Remove those steps unless the user intentionally maintains the same private records.

Risk: The workflow installs and runs the ClawHub CLI.

Mitigation: Install the CLI from a trusted source and avoid administrator privileges where possible.

## Reference(s):

- [ClawHub Pre-Publish Checklist](references/checklist.md)
- [ClawHub skill page](https://clawhub.ai/jini92/skills/clawhub-publish-mai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline PowerShell and CLI command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes checklist-driven publishing steps, versioning guidance, and common error handling.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
