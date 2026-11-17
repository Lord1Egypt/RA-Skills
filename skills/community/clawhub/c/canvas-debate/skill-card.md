## Description:

Adversarial debate between a YC Partner challenger and a Business Strategist defender to stress-test and improve a business model, using two independent subagents with separated contexts to reduce confirmation bias and produce a battle-tested canvas and debate report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qianen6](https://clawhub.ai/user/qianen6)

### License/Terms of Use:

MIT-0

## Use Case:

Founders, product teams, and developers use this skill to stress-test a product's business model with an adversarial debate between a challenger and defender. It helps identify weak assumptions, update business canvas documents, and produce a debate report before investor, product, or strategy decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the relevant project codebase and creates or updates business-analysis documents under docs/business.

Mitigation: Install only when that project access and file-writing behavior is acceptable for the workspace.

Risk: Generated business conclusions may be incomplete or misleading if treated as authoritative.

Mitigation: Review the generated conclusions before using them for investor, product, or strategy decisions.

## Reference(s):

- [Canvas Debate ClawHub release](https://clawhub.ai/qianen6/skills/canvas-debate)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown documents under docs/business, including business canvases, test cards, an executive summary, a debate report, and a debate index]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated business conclusions should be reviewed before use in investor, product, or strategy decisions.]

## Skill Version(s):

1.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
