## Description:

Use when the user asks to pick a bid strategy, set a tCPA or tROAS target, or plan the learning-phase entry; produces a bid-strategy choice, starting target math, portfolio grouping map, and learning-phase entry plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing operators and growth teams use this skill to choose a paid-ad bidding strategy, derive starting tCPA or tROAS targets from their own campaign history, group bid portfolios, and plan learning-phase entry without churn.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bid recommendations can be misleading if CPA, ROAS, or conversion-volume inputs are missing, stale, or estimated.

Mitigation: Require the agent to label metrics as Measured, User-provided, Estimated, or needs-export, and avoid inventing target math when source data is absent.

Risk: Optional ad-platform API use may expose current campaign strategy and target data.

Mitigation: Use user-provided exports by default and grant API read access only when the operator is comfortable with that data access.

Risk: Large target or budget changes can reset campaign learning and create premature-scaling risk.

Mitigation: Flag reset-prone changes and route launch review to the account-auditor guardrail before execution.

## Reference(s):

- [Bid Strategy Matrix](artifact/references/bid-strategy-matrix.md)
- [Skill Homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [ClawHub Skill Page](https://clawhub.ai/aaron-he-zhu/skills/bid-strategy-planner)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration]

**Output Format:** [Markdown guidance with formulas, portfolio mapping, and a reusable handoff summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include measured, user-provided, estimated, or needs-export labels for input metrics.]

## Skill Version(s):

19.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
