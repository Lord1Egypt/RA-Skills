## Description:

Provides a Chinese-language Windows C drive cleanup workflow that scans approved cache and temporary-file locations, asks for user confirmation before deletion, and produces a Markdown cleanup log.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wanyvo](https://clawhub.ai/user/wanyvo)

### License/Terms of Use:

MIT-0

## Use Case:

Windows users and support agents use this skill when a user explicitly wants to free space on the C drive while keeping cleanup limited to approved temporary, cache, log, and application-cache directories. It is intended to guide per-directory explanations, confirmations, cleanup actions, and audit logging rather than broad disk scanning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release documents a cleanup script, but the script file is absent from the provided artifact evidence.

Mitigation: Use DryRun only until the PowerShell script is included in the release package and reviewed before execution.

Risk: The documented cleanup behavior can delete files from cache, backup, WPS, or AppData paths after confirmation.

Mitigation: Approve deletion only after inspecting the exact resolved path and contents, and keep cleanup limited to exact approved directories.

Risk: The documented command uses PowerShell ExecutionPolicy Bypass.

Mitigation: Remove the bypass where possible or pin execution to a trusted, reviewed package path.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wanyvo/skills/c-drive-safe-cleanup-skill)
- [Safety Boundary Reference](artifact/references/safety.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples and cleanup-log output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Designed for Windows C drive cleanup workflows with explicit user confirmations and Markdown logging.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
