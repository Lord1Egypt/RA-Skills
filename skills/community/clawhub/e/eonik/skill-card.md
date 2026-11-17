## Description:

Use eonik with Claude to ground marketing work in brand notes, competitor research, own-ad facts, ad breakdowns, memory, and receipt-bound briefs while keeping launch and budget decisions under human control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[techievena](https://clawhub.ai/user/techievena)

### License/Terms of Use:

MIT-0

## Use Case:

External marketers and their agents use this skill with a connected eonik workspace to read brand context, research competitor and own-ad evidence, save approved memory, and draft receipt-bound creative briefs. It supports analysis and drafting, not ad deployment or spend management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace-specific eonik context could be used in generic marketing conversations where that brand data should not apply.

Mitigation: Install and activate the skill only for the intended connected eonik workspace, and avoid applying saved eonik context outside that workspace or brand.

Risk: Durable brand notes, plans, or memory could preserve incorrect or premature decisions.

Mitigation: Review user intent before allowing the agent to save durable notes or plans, and store the marketer's wording rather than an agent summary.

Risk: Marketing analysis could be mistaken for predictive performance advice or ad-spend authority.

Mitigation: Keep outputs receipt-bound and descriptive, and preserve the documented bans on launch, pause, scale, kill, budget, and performance-prediction actions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/techievena/skills/eonik)
- [eonik website](https://www.eonik.ai)
- [eonik MCP setup](https://www.eonik.ai/mcp)
- [eonik MCP connector](https://github.com/eonik-ai/eonik-mcp)
- [eonik companion skill source](https://github.com/eonik-ai/eonik-mcp-skill)
- [Tool reference](reference.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, API Calls]

**Output Format:** [Markdown prose with bullet insights, receipt-bound creative briefs, and tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Grounded in eonik workspace receipts; no ad launch, pause, scale, kill, budget, or performance prediction authority.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
