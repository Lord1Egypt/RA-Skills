## Description:

Scan, audit, and clean up Python virtual environments, conda environments, node_modules, and development artifacts that consume disk space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mahimairaja](https://clawhub.ai/user/mahimairaja)

### License/Terms of Use:

BSD-3-Clause

## Use Case:

Developers and engineers use this skill to inspect workspace environment sprawl, identify stale or broken Python and JavaScript environments, and prepare dry-run cleanup plans before deleting disk-heavy development artifacts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unverified package installation examples and broad cleanup commands can affect local development environments.

Mitigation: Prefer pinned package versions, confirm the package source before installation, and start scans on narrow project paths.

Risk: Non-dry-run cleanup or --yes deletion can remove environments or generated artifacts the user still needs.

Mitigation: Run scan and dry-run modes first, review the exact deletion list, and require explicit confirmation before destructive cleanup.

## Reference(s):

- [Commands Reference](references/commands.md)
- [Safety Guide](references/safety.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub Skill Page](https://clawhub.ai/mahimairaja/skills/envoic)
- [Publisher Profile](https://clawhub.ai/user/mahimairaja)
- [Repository Metadata Link](https://github.com/mahimailabs/envoic)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and cleanup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-report commands when requested; destructive cleanup should be presented as a reviewed dry run before execution.]

## Skill Version(s):

0.0.9 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
