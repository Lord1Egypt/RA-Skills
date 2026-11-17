## Description:

Clawpilot is your skill installation advisor. It analyzes task intent, recommends suitable skills, compares tradeoffs, explains risk, and suggests an installation order.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use Clawpilot to map natural-language tasks to candidate ClawHub skills, compare recommendation tradeoffs, understand risk labels, and decide an installation order. The current release is strongest for Chinese-language task prompts and provides advice only.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese keyword triggers can overmatch and recommend skills for ambiguous prompts.

Mitigation: Review the detected intent and recommended skills before installing anything, and ask the user to clarify ambiguous tasks.

Risk: Risk labels are manually maintained and may be incomplete for legal, medical, mental-health, shopping, and travel categories.

Mitigation: Treat recommendations as decision support only and consult qualified professionals for high-impact decisions.

Risk: The advisor can recommend medium- or high-risk skills but cannot verify their safety or suitability.

Mitigation: Scan and review each recommended skill before deployment or installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrylabsj/skills/clawpilot-advisor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown recommendation report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes detected intent, recommended skills, installation order, risk labels, disclaimers for medium or high risk recommendations, and boundaries.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
