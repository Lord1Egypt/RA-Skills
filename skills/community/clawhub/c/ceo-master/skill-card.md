## Description: <br>
Transforms an agent into a strategic CEO and orchestrator for vision setting, decision-making, resource allocation, team dispatch, performance review, high-stakes planning, and operations scaling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[georges91560](https://clawhub.ai/user/georges91560) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent maintain a CEO-style operating rhythm: plan strategy, classify decisions, allocate resources, coordinate sub-agents, calculate business metrics, update CEO records, and prepare weekly reports for the principal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill encourages recurring updates to CEO records, learnings, decisions, metrics, and reports. <br>
Mitigation: Set explicit approval rules for persistent file updates and review changes to CEO and learnings files before relying on them operationally. <br>
Risk: The skill uses agent-mediated Telegram reporting for weekly reports, escalation alerts, and revenue milestones. <br>
Mitigation: Require user approval before any Telegram message is sent and restrict reports to intended recipients. <br>
Risk: The skill can influence high-impact business actions such as spending, outreach, trading-related actions, public posting, and one-way-door decisions. <br>
Mitigation: Require principal approval for spending, paid subscriptions, customer-facing outreach, public posting, trading-related actions, access grants, and irreversible business decisions. <br>
Risk: The metrics workflow may produce misleading recommendations if source data is stale or incomplete. <br>
Mitigation: Refresh and validate source metrics before running the calculator, and do not send or act on incomplete metric reports. <br>


## Reference(s): <br>
- [CEO Master ClawHub release](https://clawhub.ai/georges91560/ceo-master) <br>
- [Publisher profile: georges91560](https://clawhub.ai/user/georges91560) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [ceo_metrics.py](artifact/ceo_metrics.py) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with file updates, shell commands, and optional JSON or Telegram-ready metric summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local CEO workspace files and a standard-library Python metrics calculator; metadata indicates no direct network requests but does use agent-mediated Telegram reporting.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
