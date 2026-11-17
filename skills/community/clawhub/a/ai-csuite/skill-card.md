## Description:

Runs a script-backed AI C-Suite strategic debate for SaaS teams that builds a stage-aware executive roster, generates structured debate rounds, synthesizes a Chief-of-Staff brief, and outputs a CEO decision with action items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarezoe](https://clawhub.ai/user/clarezoe)

### License/Terms of Use:

MIT

## Use Case:

Founders, SaaS operators, and strategy teams use this skill to turn a decision topic and company context into a structured executive-style debate, CEO brief, CEO decision, action items, review trigger, confidence, and reversibility assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Company context and generated decision logs can include sensitive business details.

Mitigation: Keep company.local.yaml and generated logs out of public repositories and share them only with intended reviewers.

Risk: The optional --jev mode sends listed business context to TypeSafe.

Mitigation: Use --jev only when the operator intentionally wants that external judgment path and has configured TYPESAFE_API_KEY.

Risk: Strategic recommendations may be incomplete or unsuitable for the actual business context.

Mitigation: Review the CEO brief, decision, action owners, confidence, and reversibility assessment before acting on the output.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clarezoe/skills/ai-csuite)
- [README](README.md)
- [AI C-Suite Framework PRD](ai-csuite-framework-prd.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown decision brief with shell command guidance and local configuration inputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local markdown decision artifacts and validates required output sections.]

## Skill Version(s):

2.1.3 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
