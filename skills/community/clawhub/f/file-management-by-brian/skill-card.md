## Description:

Organize and maintain AI agent workspaces with structured directories, clear naming, regular audits, dead file detection, and safe cleanup practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briandavisbikes-code](https://clawhub.ai/user/briandavisbikes-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to organize AI agent workspaces, audit file usage, identify dead or large files, and apply cleanup practices before restructuring or ongoing maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit output may expose filenames or workspace paths that reveal private context.

Mitigation: Review audit output before sharing it externally.

Risk: Documented Git cleanup commands could publish unintended files if used without review.

Mitigation: Run git status, inspect staged diffs, stage only intended paths, and avoid pushing until memory, logs, credentials, and personal configuration files are excluded.

## Reference(s):

- [File Management Reference](artifact/FILE-MANAGEMENT.md)
- [ClawHub skill page](https://clawhub.ai/briandavisbikes-code/skills/file-management-by-brian)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown guidance with inline shell commands and checklist-style procedures]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a read-only workspace audit script that reports executable scripts, recent changes, large files, file counts, directory sizes, and memory directory status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
