## Description:

Validates OpenClaw agent configuration against agent directories and core documentation, detects stale references, and can generate reports or apply scoped configuration fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[starai-2026](https://clawhub.ai/user/starai-2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers maintaining OpenClaw multi-agent systems use this skill to verify that openclaw.json, agent directories, and core documents remain consistent after adding, deleting, merging, or modifying agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fix mode can persistently edit .openclaw/openclaw.json.

Mitigation: Run read-only or dry-run mode first, keep safe mode enabled, and review backups and configuration diffs before accepting changes.

Risk: The packaged test runner can execute a validator path derived from OPENCLAW_ROOT.

Mitigation: Do not run test-skill.js with an untrusted OPENCLAW_ROOT value; invoke the main validator only from trusted OpenClaw workspaces.

Risk: Full repair mode may affect sensitive configuration such as agents, models, channels, or authentication settings.

Mitigation: Use interactive confirmation for sensitive changes and avoid unattended full repair runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/starai-2026/skills/agent-config-validator)
- [README-en.md](artifact/README-en.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown diagnostic reports with command examples and optional configuration updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; fix mode can create backups and update openclaw.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
