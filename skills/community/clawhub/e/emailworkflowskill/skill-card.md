## Description:

Use when Codex, Hermes, OpenClaw, Claude Code, Cowork, or another AI agent needs to plan, review, implement, audit, or improve email work focused on workflow maps, lifecycle routing, trigger ownership, and agent-readable operating paths.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polnikale](https://clawhub.ai/user/polnikale)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and email teams use this skill to map, audit, and improve lifecycle email workflows with clear routing, QA checks, ownership, and approval gates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recommendations may affect live email sends, contact imports, DNS or authentication settings, suppression rules, or production automations.

Mitigation: Review proposed live-system changes and require explicit user approval before execution.

Risk: Workflow plans may create duplicate enrollment, message collisions, or bypassed suppression logic if applied without QA.

Mitigation: Use trigger inventories, source-of-truth checks, collision audits, suppression checks, and operator-ready QA plans before deployment.

## Reference(s):

- [Email Workflow Skill Operating Checklist](references/operating-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance with workflow maps, trigger inventories, routing diffs, handoff notes, collision audits, and QA plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit approval before live sends, contact imports, DNS or authentication changes, suppression edits, or production automation changes.]

## Skill Version(s):

0.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
