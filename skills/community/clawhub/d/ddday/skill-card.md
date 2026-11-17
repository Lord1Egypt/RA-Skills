## Description:

Daily work journal and machine migration toolkit that scans registered projects, generates daily dashboards, and provides export and restore workflows for machine migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cosmofang](https://clawhub.ai/user/cosmofang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and power users use ddday to record daily project activity, produce AI-readable work context, and package local work data for migration to another machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration exports can concentrate credentials, agent memory, business data, and cron state into an AI-readable archive.

Mitigation: Export only trusted local projects, exclude live credentials or agent memory unless necessary, and keep archives private and encrypted.

Risk: Restore scripts and recurring cron jobs can make broad local changes if executed without review.

Mitigation: Inspect setup scripts before running restore and add, remove, or edit cron jobs manually so recurring execution remains under user control.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cosmofang/skills/ddday)
- [Publisher profile](https://clawhub.ai/user/cosmofang)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell, Python, and JSON snippets; generated logs, dashboards, snapshots, and migration bundles.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local files, archives, symlinks, and optional cron entries when the user executes the workflows.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
