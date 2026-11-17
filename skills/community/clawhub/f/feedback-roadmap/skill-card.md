## Description:

Convert customer feedback, review themes, and complaint clusters into product improvement priorities with clear rationale and urgency ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leooooooow](https://clawhub.ai/user/leooooooow)

### License/Terms of Use:

MIT-0

## Use Case:

External operators, product managers, ecommerce teams, and customer-experience teams use this skill to convert reviews, surveys, support transcripts, return reasons, and social feedback into an auditable improvement roadmap.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Roadmap inputs may include raw customer communications, identifiers, sensitive transcript content, or verbatim quotes.

Mitigation: Use only sanitized and authorized feedback; remove or hash identifiers, redact sensitive quotes, and avoid unnecessary transcript detail.

Risk: Generated roadmap documents may expose customer feedback or internal priorities to unintended audiences.

Mitigation: Restrict report access and define retention and deletion rules before sharing the roadmap.

## Reference(s):

- [Output Template](references/output-template.md)
- [Prioritization Frameworks](references/prioritization-frameworks.md)
- [Feedback Clustering Guide](references/feedback-clustering-guide.md)
- [Quality Checklist](assets/quality-checklist.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown roadmap with structured tables, priority scores, owners, rationale, and monitor items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include representative customer quotes; sanitize and redact sensitive feedback before sharing.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
