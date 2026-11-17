## Description:

Deterministic, evidence-gated controller templates for OpenClaw (HEARTBEAT/ACTIVITIES + sprint template + poll cron payload). Docs-only: installs no services and makes no config changes by itself.

This skill is ready for commercial/non-commercial use.

## Publisher:

[variable190](https://clawhub.ai/user/variable190)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to set up deterministic OpenClaw controller templates for heartbeat, polling, sprint planning, project queues, and evidence-gated worker completion. It is intended for manual installation and operator-reviewed automation rather than self-installing runtime changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous controller loops can dispatch workers, update activity state, import sprint plans, and persist scheduled polling if armed without review.

Mitigation: Keep cron and heartbeat disabled until reviewed, run a manual reconcile first, and validate sprint plans before activation.

Risk: Heartbeat refreshes may read memory and identity files that can contain sensitive information.

Mitigation: Review files read by HEARTBEAT_TICK for secrets and restrict Plan Path values to trusted workspace locations.

Risk: Optional Telegram logging and cross-context sends can move control-plane data outside the local workspace.

Mitigation: Enable external logging only with a strict destination allowlist and keep emitted logs minimal.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/variable190/skills/deterministic-controller)
- [README](README.md)
- [Security Notes](SECURITY.md)
- [OpenClaw Config Snippets](docs/openclaw_config_snippets.md)
- [Poll Cron Payload](docs/poll_cron_payload.txt)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown templates, copy/paste prompts, configuration snippets, and cron payload text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Docs-only release; produces operator-applied templates and guidance rather than executable services.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
