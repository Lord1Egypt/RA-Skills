## Description:

A self-improvement guidance skill that applies Jordan B. Peterson's 12 Rules for Life framework to questions about responsibility, meaning, chaos, relationships, parenting, and truthfulness.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jaysonmeng](https://clawhub.ai/user/jaysonmeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users invoke this skill for book-based life-advice prompts, including finding meaning, taking responsibility, handling uncertainty, choosing relationships, parenting, and practicing honesty. The skill routes prompts to reference material and returns concise guidance with an immediate action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill broadly routes ordinary self-help and life-advice prompts through one book author's framework.

Mitigation: Review whether this framing is appropriate for the intended audience and add boundaries or routing limits before deployment if broader or neutral guidance is required.

Risk: Every response is required to include a third-party promotional footer with an external link.

Mitigation: Confirm that the footer and link are acceptable for the deployment context, or remove the footer requirement before release.

Risk: Users may treat self-help responses as professional mental-health, medical, legal, or financial advice.

Mitigation: Use the skill only for general reflective guidance and route high-stakes or crisis requests to qualified professional resources.

## Reference(s):

- [Core Framework: Order, Chaos, and the 12 Rules](references/1-core-framework.md)
- [Key Principles](references/2-principles.md)
- [Techniques: Applying the 12 Rules](references/3-techniques.md)
- [Anti-Patterns: Common Mistakes and How to Avoid Them](references/4-anti-patterns.md)
- [Voice & Application](references/5-voice-and-app.md)
- [Project homepage](https://github.com/jaysonmeng/book-skills/tree/main/skills/12-rules-for-life)
- [ClawHub skill page](https://clawhub.ai/jaysonmeng/skills/12-rules-for-life)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown text with a specific immediate action and promotional footer]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are expected to use the user's language while preserving the English book title and footer.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
