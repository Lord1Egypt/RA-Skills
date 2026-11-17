## Description:

Drift detection and baseline integrity guard for agent workspace files with automatic alerting support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davida-ps](https://clawhub.ai/user/davida-ps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Soul Guardian to monitor OpenClaw workspace prompt and instruction files for unexpected drift, produce reviewable diffs and audit records, and optionally restore protected files to approved baselines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release scanner marked the skill suspicious because its filesystem and install behavior can affect files outside the intended workspace.

Mitigation: Review the skill before installing, run it only in workspaces and state directories you control, and avoid broad or untrusted policy.json entries.

Risk: Restore mode intentionally overwrites protected workspace files back to approved baselines.

Mitigation: Limit restore-mode targets to critical files, use alert-only checks or --no-restore when reviewing behavior, and approve intentional edits before recurring checks run.

Risk: The guardian state directory can contain sensitive snapshots, diffs, audit records, and quarantined copies.

Mitigation: Store state outside the workspace when possible and apply restrictive permissions such as chmod 700 or chmod go-rwx.

Risk: Cron or launchd scheduling can create recurring background checks.

Mitigation: Keep scheduling opt-in, inspect generated cron or launchd configuration before enabling it, and verify the workspace, state directory, and log paths.

Risk: An unpinned npx install command is documented for convenience.

Mitigation: Prefer the signed-release verification path before trusting or extracting SKILL.md, skill.json, or the release archive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/davida-ps/skills/clawsec-openclaw-soul-guardian)
- [Project homepage](https://clawsec.prompt.security)
- [Publisher profile](https://clawhub.ai/user/davida-ps)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and local text or JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local baseline, audit, patch, quarantine, and launchd plist files when invoked.]

## Skill Version(s):

0.0.9 (source: server release, SKILL.md frontmatter, skill.json, CHANGELOG released 2026-06-23)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
