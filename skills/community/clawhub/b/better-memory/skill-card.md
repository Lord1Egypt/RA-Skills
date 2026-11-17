## Description:

Better Memory V2 installs and maintains a native OpenClaw memory stack with daily logs, structured sidecar summaries, weekly rollups, migration tooling, typed capture, and review workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fuuuuujichaos](https://clawhub.ai/user/fuuuuujichaos)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to install persistent memory support, capture typed memory, migrate legacy memory safely, and run daily, weekly, and monthly memory distillation or cleanup-review workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies persistent workspace memory and agent guidance files.

Mitigation: Review AGENTS.md, MEMORY.md, HEARTBEAT.md, .openclaw-memory-os, and generated review artifacts before relying on the installed memory stack.

Risk: Scheduled runs can repeatedly apply memory distillation or review behavior after installation.

Mitigation: Inspect the generated cron template and enable scheduled commands only after confirming the workspace path, timing, and intended memory lifecycle.

Risk: Untrusted captured or migrated memory text could affect future agent behavior.

Mitigation: Import legacy memory only through reviewed migration plans and avoid capturing untrusted memory text until marker handling is fixed.

## Reference(s):

- [Better Memory V2 Schema (Native-Fusion)](references/memory-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces persistent workspace memory files, managed guidance blocks, review reports, migration plans, cleanup plans, and cron template text.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
