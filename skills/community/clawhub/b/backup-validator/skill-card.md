## Description:

Validates OpenClaw backup artifacts before push by checking skill structure, secret leaks, Termux compatibility, and repository status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmuhammadagus-byte](https://clawhub.ai/user/pmuhammadagus-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to validate OpenClaw backup workspaces before committing or pushing them. It guides checks for required directories, skill file integrity, leaked secrets, git status, remote sync, platform compatibility, and metadata consistency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Secret scan output could expose sensitive values if copied verbatim into public channels.

Mitigation: Review matches manually, redact sensitive values, and share only summarized findings.

Risk: Broad EXTRA_PATHS values can expand local scans beyond the intended backup workspace.

Mitigation: Keep EXTRA_PATHS limited to known backup or workspace paths before running validation.

Risk: Suggested recovery steps involving reset or permission changes can alter local files if applied carelessly.

Mitigation: Do not allow destructive git or permission-changing actions unless explicitly intended and backed up.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pmuhammadagus-byte/skills/backup-validator)
- [Publisher profile](https://clawhub.ai/user/pmuhammadagus-byte)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown validation report with PASS, FAIL, or WARNING status, check details, and recovery actions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local shell commands and fallback steps for backup validation; secret scan results should be summarized without exposing sensitive values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
