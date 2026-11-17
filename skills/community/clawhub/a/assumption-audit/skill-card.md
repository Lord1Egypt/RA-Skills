## Description:

Part of the Overpowered skill suite, Assumption Audit exposes material assumptions, hidden premises, and unresolved unknowns in a plan, analysis, design, or decision before an incorrect assumption can change the approach.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and decision makers use this skill to audit plans, analyses, designs, or decisions for assumptions that could materially change the outcome. It helps separate verified facts, working assumptions, testable unknowns, and decisions that must be resolved before the next irreversible step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to inspect relevant files or use available tools while verifying assumptions.

Mitigation: Limit verification to task-relevant evidence and available tools, and escalate unavailable knowledge or genuinely ambiguous intent to the user.

Risk: An assumption audit can over-expand into a generic risk register for low-impact work.

Mitigation: Apply the skill's materiality filter and avoid listing assumptions that would not change the approach.

## Reference(s):

- [Overpowered skill suite](https://github.com/raguets/overpowered)
- [Assumption Audit on ClawHub](https://clawhub.ai/raguets/skills/assumption-audit)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown table with concise follow-up guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on material assumptions and the smallest unresolved set before the next irreversible step.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
