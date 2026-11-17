## Description:

Dealpilot helps agents compare shopping options across Taobao, Pinduoduo, JD, YHD, and Vipshop using product needs, budget, risk, timing, and alternatives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistant agents use Dealpilot to turn a product request, budget, urgency, and preferences into a cross-platform purchase recommendation. The current release is an MVP skeleton with mock platform data, so recommendations should be treated as prototype guidance until live adapters are connected.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The current release returns mock prices, subsidy claims, seller-risk claims, and buy-now advice.

Mitigation: Treat recommendations as prototype guidance and verify price, seller status, platform policy, and availability directly before purchase.

Risk: Users may mistake the MVP skeleton for live cross-platform comparison.

Mitigation: Add clear mock-data warnings and connect live platform adapters before relying on the skill for real purchase decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/dealpilot)
- [README](README.md)
- [Running and Testing Guide](RUNNING.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, text, JSON]

**Output Format:** [Markdown decision report and JSON-compatible DecisionReport structure]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current version returns mock prices, platform comparisons, risks, alternatives, and timing advice.]

## Skill Version(s):

0.1.0 (source: SKILL.md frontmatter, package.json, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
