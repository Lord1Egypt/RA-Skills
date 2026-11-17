## Description:

Systematic content quality audit based on 80 CORE-EEAT standards for evaluating GEO and SEO potential with 8-dimension scoring, weighted totals, veto item detection, and prioritized improvement recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[281862066-a11y](https://clawhub.ai/user/281862066-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Content strategists, SEO/GEO practitioners, editors, and developers use this skill to audit supplied content or URLs against an 80-item CORE-EEAT rubric and produce scoring, veto checks, and prioritized remediation guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The audit can be incomplete when supplied content lacks site-level signals such as backlinks, schema markup, policy pages, or organization authority data.

Mitigation: Provide relevant site-level context when available, and mark inaccessible items as N/A with reasons rather than scoring them as failures.

Risk: The skill may analyze private files, exact URLs, or pasted content if the user gives an agent access to them.

Mitigation: Use pasted content or exact paths intentionally, and avoid providing private files unless the agent is meant to read and analyze them.

Risk: Rubric-based recommendations may be misleading if input content, competitor examples, or content type are incomplete or incorrect.

Mitigation: Confirm the content type and review generated scores and recommendations before using them for publication or business decisions.

## Reference(s):

- [CORE-EEAT Content Quality Benchmark](references/core-eeat-benchmark.md)
- [CORE-EEAT Item Reference Table](references/item-reference.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Markdown audit report with tables, scores, veto status, and action-plan checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes item-level Pass/Partial/Fail scoring, dimension scores, GEO and SEO system scores, weighted total scoring, and top-priority recommendations.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
