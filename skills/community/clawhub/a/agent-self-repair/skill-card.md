## Description:

Automatically captures runtime errors, analyzes root causes, generates and applies fixes, and verifies repairs without manual intervention.

This skill is ready for commercial/non-commercial use.

## Publisher:

[benxiao2026](https://clawhub.ai/user/benxiao2026)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to diagnose runtime failures, generate repair plans, apply fixes, and verify whether the agent workflow recovers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic self-repair can make system-affecting changes without clear approval or working safeguards.

Mitigation: Run only in a sandbox until package installs, service restarts, deletion, and retry behavior require explicit approval.

Risk: Package installation, service restart, and cache deletion behavior can destabilize the environment or remove useful state.

Mitigation: Use package allowlists, backups, rollback steps, result checking, and avoid --break-system-packages before enabling automatic repair.

Risk: Captured errors and repair logs can expose sensitive runtime context.

Mitigation: Redact logs before sharing or persisting them and limit collection to information needed for diagnosis.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/benxiao2026/skills/agent-self-repair)
- [Publisher profile](https://clawhub.ai/user/benxiao2026)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code blocks, shell commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend or carry out repair actions such as retries, configuration edits, package installs, service restarts, and cache cleanup; use sandboxing and review for automatic changes.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact version note)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
