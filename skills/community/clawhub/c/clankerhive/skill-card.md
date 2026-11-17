## Description:

ClankerHive provides a local SQLite-backed context store for coordinating facts, alerts, and task claims across multiple agent sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use ClankerHive to share short-lived state, queue alerts, and reduce duplicate work across cron, heartbeat, sub-agent, and interactive sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The persistent SQLite store can retain coordination data and expose facts or alerts if placed in a shared or weakly protected path.

Mitigation: Keep the database in a private per-user location, avoid storing secrets or sensitive personal data, and restrict permissions when overriding CLANKERHIVE_DB.

Risk: Task claiming is intended for coordination and deduplication, not security-sensitive locking or exactly-once workflow execution.

Mitigation: Use task claims as best-effort coordination and add stronger locking or transactional controls for critical workflows.

## Reference(s):

- [ClankerHive ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/clankerhive)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON or plain-text command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Python 3 standard library commands and a persistent same-user SQLite database.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
