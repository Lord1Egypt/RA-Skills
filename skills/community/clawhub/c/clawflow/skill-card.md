## Description:

Protocol for multi-agent collaboration via OpenClaw's message-passing and recursive task DAGs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[srikanth235](https://clawhub.ai/user/srikanth235)

### License/Terms of Use:


## Use Case:

Developers and agent builders use Clawflow to coordinate complex work across multiple OpenClaw agents by decomposing tasks into recursive DAGs, dispatching subtasks, and synthesizing returned results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents may delegate work broadly to other configured agents.

Mitigation: Restrict delegation with explicit allow lists and require approval before dispatching sensitive or high-impact subtasks.

Risk: Message and task history may retain sensitive content in workspace logs.

Mitigation: Avoid secrets and regulated data unless redaction, retention limits, and access controls are in place.

Risk: Forwarding prior results between agents can disclose more context than a peer needs.

Mitigation: Minimize downstream context, redact unnecessary details, and define sender-authentication and approval rules for delegation.

Risk: The documented V1 behavior is fail-fast and does not provide retries or partial recovery.

Mitigation: Use manual review or external workflow controls for critical tasks until retry and recovery policies are added.

## Reference(s):

- [Clawflow Skill Source](artifact/SKILL.md)
- [Agent Loop](artifact/agent-loop.md)
- [Coordinating](artifact/coordinating.md)
- [Message & File Schemas](artifact/schemas.md)
- [ClawHub Skill Page](https://clawhub.ai/srikanth235/skills/clawflow)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML frontmatter examples, Python helper scripts, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes helper scripts that can create local task, mailbox, dispatch, and reply files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
