## Description:

Dual-Mode Reasoner helps an agent choose between quick and deliberate reasoning based on task risk, then exposes assumptions, counterexamples, recommendations, and stop conditions in a fixed response structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarkchenkai](https://clawhub.ai/user/clarkchenkai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and employees can use this skill when a task needs explicit reasoning-depth selection for mixed-risk decisions. It is intended to make risk signals, assumptions, counterexamples, recommendations, and escalation conditions visible rather than implicit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation can make decision-oriented answers more structured and explicit than some users expect.

Mitigation: Review the activation triggers and narrow implicit invocation wording when manual activation is preferred.

Risk: The skill may be used on high-stakes or governance-sensitive decisions where an agent recommendation should not be the final authority.

Mitigation: Use the required stop condition to identify when to act, pause, or escalate for human or policy review.

## Reference(s):

- [Deliberation Patterns](references/deliberation-patterns.md)
- [Kahneman Reference](references/kahneman.md)
- [Mode Triggers](references/mode-triggers.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown sections with concise prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed six-part response structure: mode selection, risk signals, working assumptions, counterexamples, decision or recommendation, and stop condition.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
