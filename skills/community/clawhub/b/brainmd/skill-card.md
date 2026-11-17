## Description:

Neuroplastic self-modifying runtime for AI agents that creates a file-based brain for reflexes, habits, weighted pathways, reinforcement, and a cortex self-review loop.

This skill is ready for commercial/non-commercial use.

## Publisher:

[p0lish](https://clawhub.ai/user/p0lish)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use brainmd to add persistent file-based behavioral memory to an AI agent, record outcomes as weighted pathways, and run review cycles that strengthen, weaken, decay, or prune behavior patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is designed to create persistent self-modifying agent behavior and the server security verdict is suspicious because safeguards for unattended use are limited.

Mitigation: Install only when persistent behavioral memory is intentional; keep the brain directory private and require human approval before enabling heartbeat or cron automation.

Risk: Pathway records can influence future actions if raw notes or untrusted pathway text are incorporated into prompts.

Mitigation: Review and sanitize pathway notes before use, avoid placing raw notes in system or developer prompts, and require manual approval for new behavior pathways that affect future decisions.

Risk: Review and prune operations can mutate or remove behavior state.

Mitigation: Review and back up pathways.json before automated review cycles or pruning, and preserve mutation logs for auditability.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/p0lish/skills/brainmd)
- [Artifact README](artifact/README.md)
- [Artifact skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript snippets, JSON examples, and generated local files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initializes and updates a local file-based brain directory, including pathway state and mutation logs.]

## Skill Version(s):

0.1.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
