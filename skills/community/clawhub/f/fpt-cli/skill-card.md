## Description:

Guides OpenClaw through installing, configuring, and using fpt-cli for Autodesk Flow Production Tracking / ShotGrid authentication, schema and entity queries, searches, and safe write previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[loonghao](https://clawhub.ai/user/loonghao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and production teams use this skill to set up fpt-cli authentication and safely inspect, search, and update ShotGrid / Flow Production Tracking data through OpenClaw.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ShotGrid credentials or tokens may be exposed during setup.

Mitigation: Use the documented secure profile flow or a secret store; avoid passing secrets on command lines.

Risk: Write commands can change or delete production records.

Mitigation: Review dry-run plans before writes and require explicit confirmation for deletes.

Risk: Self-updates can replace the installed CLI binary.

Mitigation: Treat self-updates as a manual administrator action rather than an automatic agent step.

## Reference(s):

- [Installation and authentication guide](references/install-and-auth.md)
- [Query patterns and write safety](references/query-patterns.md)
- [ClawHub skill listing](https://clawhub.ai/loonghao/skills/fpt-cli)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers targeted JSON responses and dry-run previews before writes.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
