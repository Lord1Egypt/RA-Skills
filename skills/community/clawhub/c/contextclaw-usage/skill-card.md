## Description:

Guides agents in using the ContextClaw plugin to analyze OpenClaw session usage, prune old sessions, clean orphaned files, and view session statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rmruss2022](https://clawhub.ai/user/rmruss2022)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to manage ContextClaw plugin workflows for analyzing session usage, identifying large or orphaned sessions, previewing cleanup, and launching the dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live cleanup commands can delete old or orphaned OpenClaw session files.

Mitigation: Use the documented dry-run previews first and require explicit user approval before running live cleanup with --dryRun false.

Risk: The plugin can inspect OpenClaw session files and should be installed only from a trusted package source.

Mitigation: Install only if the @rmruss2022/contextclaw npm package is trusted, and prefer reviewing or pinning a known version before global installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rmruss2022/skills/contextclaw-usage)
- [ContextClaw GitHub repository](https://github.com/rmruss2022/ContextClaw)
- [ContextClaw npm package](https://www.npmjs.com/package/@rmruss2022/contextclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes dry-run cleanup guidance and dashboard usage notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
