## Description:

Coordination layer for OpenClaw agent fleets (tasks, messaging, activity feed, dashboard).

This skill is ready for commercial/non-commercial use.

## Publisher:

[lludlow](https://clawhub.ai/user/lludlow)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use Clawctl to coordinate OpenClaw agent fleets through a shared task board, inter-agent messaging, activity feed, and optional live dashboard backed by SQLite.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The dashboard exposes a persistent token-bearing web UI with task mutation authority.

Mitigation: Review before installing if the dashboard will be used, prefer running it only on localhost, avoid sharing token URLs, and rotate or delete ~/.openclaw/.clawctl-token if exposed.

Risk: The local SQLite database contains task, message, and activity history for participating agents.

Mitigation: Treat the database as sensitive operational data and restrict access to the database file and host account.

## Reference(s):

- [Clawctl ClawHub listing](https://clawhub.ai/lludlow/skills/clawctl)
- [OpenClaw project](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, text]

**Output Format:** [Markdown guidance with inline shell commands and CLI output text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the clawctl command-line tool and a local SQLite database.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata, released 2026-02-09; artifact package files declare 0.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
