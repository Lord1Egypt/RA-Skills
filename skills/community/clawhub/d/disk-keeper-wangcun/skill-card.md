## Description:

DiskKeeper is a Windows disk-cleanup skill that helps agents run local health checks, preview cleanup plans, and remove whitelisted rebuildable cache and temporary files after explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mingyi-blog](https://clawhub.ai/user/mingyi-blog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Windows disk usage, preview cleanup actions, and execute local cleanup of whitelisted cache and temporary directories while preserving personal files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete local files when cleanup or recycle purge commands are explicitly confirmed.

Mitigation: Run doctor, plan, and clean without --yes first, inspect the listed paths carefully, avoid elevated or admin shells, and keep recycle --purge as a manual-only action.

Risk: Deletion safeguards rely on environment-derived Windows paths that may be altered in wrapped or modified environments.

Mitigation: Use a normal Windows user shell and avoid modified USERPROFILE, LOCALAPPDATA, APPDATA, SystemRoot, TEMP, or TMP values before running cleanup commands.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/mingyi-blog/skills/disk-keeper-wangcun)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain-text CLI output with command examples, cleanup plans, health reports, and shareable summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused; cleanup actions require explicit confirmation flags and local path review.]

## Skill Version(s):

2.3.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
