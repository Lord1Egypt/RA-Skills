## Description:

Provides a secure, least-privilege interface for managing user data, personas, memory, and configuration snapshots in a self-hosted MyVector MySQL database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paradoxfuzzle](https://clawhub.ai/user/paradoxfuzzle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use VectorClaw to give an OpenClaw-style agent controlled MySQL-backed memory, profile, relationship, mood, reminder, and usage-tracking operations in a self-hosted MyVector container. Administrators should review consent, retention, and deletion controls before enabling auto-extraction or profiling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent profiling of sensitive personal data and agent reasoning logs can create privacy and consent risk.

Mitigation: Disable auto-extraction, mood tracking, engagement tracking, and heartbeat jobs until each user has recorded opt-in consent; use extraction_config, data_retention_policy, audit_log, and rollback_user.sql for consent, retention, audit, and deletion workflows.

Risk: Setup and migration require credentials, Docker MyVector, and administrator schema changes.

Mitigation: Use a dedicated least-privilege MySQL user, avoid root/admin for agent-facing commands, keep .env chmod 600, back up before migrations, and run DDL upgrade scripts manually through docker exec rather than through sql_safe_exec.sh.

Risk: Unpinned container images and unresolved SQL validation concerns could weaken the intended safety controls.

Mitigation: Pin and verify the MyVector container image, route agent SQL through sql_safe_exec.sh, keep SELECT-only queries separate from confirmed DML, and complete the security review guidance before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/paradoxfuzzle/skills/custom-mysql)
- [SKILL.md](artifact/SKILL.md)
- [SETUP_GUIDE.md](artifact/SETUP_GUIDE.md)
- [CAPABILITIES.md](artifact/CAPABILITIES.md)
- [changelog.md](artifact/changelog.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and SQL scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Self-hosted MyVector/MySQL operations through reviewed scripts; DML requires interactive confirmation.]

## Skill Version(s):

5.0.1 (source: server release metadata and artifact/SKILL.md, released 2026-05-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
