## Description:

botlearn-healthcheck is a BotLearn autonomous health inspector for OpenClaw instances across hardware, configuration, security, skills, and autonomy domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[calvinxhk](https://clawhub.ai/user/calvinxhk)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to inspect an OpenClaw installation, collect local health signals, score five operational domains, and receive report-backed repair guidance. It supports full health checks, targeted domain checks, scheduled heartbeat inspection, and post-change verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill performs broad local inspection of OpenClaw home directories, logs, configuration, workspace identity files, and secret-adjacent files.

Mitigation: Install only in environments where this inspection scope is acceptable, and review generated findings to ensure credentials remain redacted.

Risk: Security evidence reports outbound registry checks despite artifact claims that network requests stay local.

Mitigation: Review and approve any registry, package install, or pipe-to-shell command separately before execution.

Risk: Generated HTML reports may include dynamic diagnostic output.

Mitigation: Treat generated HTML as untrusted until output escaping has been reviewed.

Risk: The skill can recommend persistent automation, cleanup, package installation, chmod, cron, and .env edits during fix guidance.

Mitigation: Require explicit human approval for each state-changing command and verify the source, rollback command, and exact files affected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/calvinxhk/skills/botlearn-healthcheck)
- [README](artifact/README.md)
- [Data Collection Protocol](artifact/data_collect.md)
- [Security Risk Assessment](artifact/check_security.md)
- [OpenClaw Platform Knowledge](artifact/openclaw_knowledge.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports, HTML reports, diagnostic text, and shell command proposals]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces traffic-light status, numeric domain scores, findings, fix guidance, and rollback-aware command proposals.]

## Skill Version(s):

1.0.5 (source: server release metadata; artifact README/frontmatter: 0.1.5)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
