## Description:

Real-time token usage and cost tracking across OpenClaw agents with budget alerts and optimization recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neal-collab](https://clawhub.ai/user/neal-collab)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to ask an agent for cost reports across OpenClaw sessions, identify high-spend agents, compare usage against budgets, and receive cost optimization recommendations. It also provides optional scheduled reporting, alert threshold, memory, and AGENTS.md configuration examples.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Monitoring reports may expose usage metadata across multiple agents.

Mitigation: Run the skill only with agents and users that should be able to view usage metadata and budget information.

Risk: Optional cron, memory, AGENTS.md, or Telegram alert settings can create recurring reports, persistent instructions, or outbound notifications.

Mitigation: Enable only the reporting and alert destinations you intend to use, and review schedules, stored thresholds, and notification channels before deployment.

Risk: Cost estimates may differ from actual billing when provider pricing, custom model rates, cache hits, or rate limits change.

Mitigation: Keep model rates current and treat generated totals as estimates that should be checked against provider billing records for financial decisions.

## Reference(s):

- [Agent Cost Monitor on ClawHub](https://clawhub.ai/neal-collab/skills/agent-cost-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown cost reports with tables, budget warnings, recommendations, and JSON or Markdown configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cost estimates depend on available token usage, configured budget thresholds, model pricing, and cache behavior.]

## Skill Version(s):

1.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
