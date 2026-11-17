## Description:

从共享记忆读取持仓，生成 A 股投资决策报告（止损/止盈/仓位管理）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hzx0385-cpu](https://clawhub.ai/user/hzx0385-cpu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to read A-share portfolio holdings, retrieve quote data, and generate a Markdown decision report with stop-loss, take-profit, position-sizing, and risk-warning guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make financial recommendations from quote data or silent fallback prices.

Mitigation: Independently verify market prices and analysis before acting on any trading recommendation.

Risk: The skill reads local portfolio holdings and saves financial reports on disk.

Mitigation: Use it only in a trusted workspace and protect saved reports under ~/.openclaw/decisions.

Risk: The security review notes that executable code is imported from a user-writable workspace.

Mitigation: Review trusted workspace files before installing or running the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hzx0385-cpu/skills/a-stock-decision-fugui)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, files, guidance]

**Output Format:** [Markdown investment decision report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns the report text and saves a timestamped Markdown report under ~/.openclaw/decisions.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
