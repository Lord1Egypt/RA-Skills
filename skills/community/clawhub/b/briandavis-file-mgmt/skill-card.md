## Description:

Organize and maintain AI agent workspaces using structured directories, clear naming, regular audits, and safe cleanup of unused or dead files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[briandavisbikes-code](https://clawhub.ai/user/briandavisbikes-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI-agent operators use this skill to structure OpenClaw-style workspaces, audit files, identify stale or risky cleanup candidates, and apply safer file retention practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented Git cleanup flow could accidentally publish private workspace data.

Mitigation: Inspect the diff, stage only intended files, scan for secrets, and confirm the remote destination before running git add, commit, or push.

Risk: Workspace audit output can expose local paths, filenames, and file sizes that may be sensitive when shared.

Mitigation: Review audit output locally and redact sensitive paths or project names before sharing it outside the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/briandavisbikes-code/skills/briandavis-file-mgmt)
- [File Management Reference](artifact/FILE-MANAGEMENT.md)
- [Skill Instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands and a Bash audit script.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a read-only workspace audit script; users choose the workspace path to inspect.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
