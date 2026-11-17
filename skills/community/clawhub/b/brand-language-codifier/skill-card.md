## Description:

Codifies a brand-level language canon covering voice, tone spectrum, banned phrases, few-shot examples from the brand's own material, and product, feature, and tier naming rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, brand, and product teams use this skill to turn existing brand material and a durable message house into reusable voice and naming rules before channel-specific copy scales. It helps agents produce canon-ready guidance while separating unresolved product claims for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that the skill asks to write persistent project memory even though its manifest advertises inline output and read access.

Mitigation: Review capability approvals before installation; require the skill either to declare persistent write scope or to return proposed registry records inline for a separately authorized writer.

Risk: Voice examples, naming terms, and implied product claims can be incorrect or unsupported if source material is incomplete or untrusted.

Mitigation: Use only the brand's own material, label each data point by source confidence, and route unresolved claims to a separate claims review before treating them as canon.

## Reference(s):

- [Brand Language Codifier on ClawHub](https://clawhub.ai/aaron-he-zhu/skills/brand-language-codifier)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown with structured canon blocks, tables, handoff summaries, and proposed registry records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses only the brand's own published or user-provided material for few-shot examples and labels terms as measured, user-provided, or estimated.]

## Skill Version(s):

19.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
