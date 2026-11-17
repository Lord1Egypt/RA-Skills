## Description:

Transforms the agent into a strategic CEO and orchestrator for vision, decision-making, resource allocation, team dispatch, performance review, and scaling operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[georges91560](https://clawhub.ai/user/georges91560)

### License/Terms of Use:

MIT-0

## Use Case:

External users and business operators use this skill to have an agent structure CEO-level planning, OKRs, resource allocation, weekly reporting, escalation, and metrics review. It is intended for workspaces where the agent is expected to maintain business strategy records and produce operational guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify OKRs, decisions, metrics, weekly reports, learnings, and other business strategy records.

Mitigation: Install only in a workspace intended for business strategy operations and require explicit approval before the agent changes strategic records.

Risk: The skill asks the agent to send Telegram reports and escalation alerts.

Mitigation: Require explicit approval before any Telegram message is sent and review recipient, content, and trigger conditions.

Risk: The skill describes recurring CEO operations, schedules, and sub-agent dispatch.

Mitigation: Require explicit approval before creating schedules or dispatching sub-agents, and keep the agent scoped to approved operating records.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/georges91560/skills/ceo-master)
- [ClawHub publisher profile](https://clawhub.ai/user/georges91560)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python command examples and optional JSON metrics output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces business reports, OKRs, decision records, metrics summaries, Telegram-ready summaries, and local workspace file updates when authorized.]

## Skill Version(s):

1.0.0 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
