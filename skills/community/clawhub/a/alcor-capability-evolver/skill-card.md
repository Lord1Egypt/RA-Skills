## Description:

A self-evolution engine for AI agents that analyzes runtime history to identify improvements and applies protocol-constrained evolution.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roamer-remote](https://clawhub.ai/user/roamer-remote)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to inspect runtime history, identify failures or inefficiencies, and generate or apply improvements to agent code, memory, and evolution assets. It is intended for controlled workspaces where shell execution, network publishing, and rollback behavior can be reviewed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: High-impact automation can modify code, write memory and asset files, run shell commands, and perform rollback behavior.

Mitigation: Install only in an isolated disposable workspace with no secrets or valuable uncommitted work; review changes before allowing solidification.

Risk: External publishing, auto-issue reporting, proactive questions, and remote memory sync can send data to external services.

Mitigation: Disable auto-publish, auto-issue reporting, proactive questions, auto-update, and remote integrations unless the outbound data and credentials have been reviewed.

Risk: Hard rollback behavior can discard local workspace changes.

Mitigation: Prefer stash or review modes and keep version control backups before enabling automated rollback.

Risk: A2A authentication secrets and node identity are used for networked operation.

Mitigation: Rotate the A2A secret before use and avoid running the skill in environments containing unrelated secrets.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roamer-remote/skills/alcor-capability-evolver)
- [Publisher profile](https://clawhub.ai/user/roamer-remote)
- [EvoMap Hub](https://evomap.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command examples, generated code changes, JSON assets, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update workspace assets, memory files, and source files during evolution workflows.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
