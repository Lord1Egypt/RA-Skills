## Description:

ClawDNA helps an OpenClaw agent suggest, inspect, snapshot, restore, and sync identity backup workflows using the ClawDNA CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gitpcl](https://clawhub.ai/user/gitpcl)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to help agents protect identity files before risky changes, detect drift, sync backups, and guide recovery on new machines or after broken updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to install and trust an unpinned external CLI that handles sensitive agent identity files and sync tokens.

Mitigation: Review the ClawDNA CLI source and package provenance before installing, pin a known-good version when available, and avoid installing or running it with elevated privileges.

Risk: Identity backups may include private user or agent context, especially when daemon auto-push or hub sync is enabled.

Mitigation: Review diffs before push or pull operations, use dry-run modes where available, keep sync tokens in environment variables, and enable daemon auto-push only after confirming the destination and contents.

## Reference(s):

- [ClawDNA Documentation](https://github.com/clawco-io/clawdna#readme)
- [ClawDNA Repository](https://github.com/clawco-io/clawdna)
- [ClawHub Skill Listing](https://clawhub.ai/gitpcl/skills/clawco-clawdna)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are advisory and commonly include ClawDNA command suggestions, backup/recovery steps, and troubleshooting guidance.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
