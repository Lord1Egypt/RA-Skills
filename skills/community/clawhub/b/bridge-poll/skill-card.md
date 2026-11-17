## Description:

Perfect Agent Comms enables two OpenClaw agents to exchange messages through an authenticated HTTP bridge with cron-based polling across instances, containers, or machines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joelsalespossible](https://clawhub.ai/user/joelsalespossible)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to deploy and maintain a self-hosted bridge that lets trusted OpenClaw agents exchange tasks and replies asynchronously.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous cross-agent HTTP messaging can expose tasks, workspace context, or agent outputs to any agent that has the bridge token.

Mitigation: Install only for agents and bridge hosts you control, keep the bridge local, tunneled, or behind TLS, and rotate the shared token when access changes.

Risk: Polling agents may read workspace files and use configured tools while processing bridge messages.

Mitigation: Limit the files and tools available to the polling agent, and review bridge messages before writing them into persistent memory.

Risk: Unsafe deployment patterns such as public port exposure or unattended helper use can increase operational risk.

Mitigation: Avoid the public-port option, prefer localhost, SSH tunnels, or a TLS reverse proxy, and address the unsafe timestamp helper and monitoring snippet before unattended use.

Risk: Cursor timestamp mistakes, stale polling, or unpruned JSONL logs can cause missed messages, duplicate replies, or degraded bridge performance.

Mitigation: Use the documented ts field for cursors, add health checks for future timestamps and stale polls, and run regular JSONL pruning.

## Reference(s):

- [Cron Job Templates](artifact/references/cron-templates.md)
- [Known Bugs & Gotchas](artifact/references/gotchas.md)
- [Monitoring & Health Checks](artifact/references/monitoring.md)
- [ClawHub Skill Page](https://clawhub.ai/joelsalespossible/skills/bridge-poll)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON cron templates and Python/shell helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bridge URL and shared-token configuration; bridge messages are stored in local JSONL files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
