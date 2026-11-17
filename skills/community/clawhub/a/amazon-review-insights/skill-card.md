## Description:

Fetches and analyzes Amazon product reviews to identify recurring issues, uncover negative feedback in positive reviews, suggest improvements, and track review trends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sparkbayes](https://clawhub.ai/user/sparkbayes)

### License/Terms of Use:

MIT-0

## Use Case:

External e-commerce sellers and their teams use the skill to collect or query Amazon review data, understand customer feedback, prioritize product improvements, and monitor review trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key is sent to AstrMap for authentication, and direct analysis calls can consume account points without an additional confirmation prompt.

Mitigation: Keep the key in an environment variable, use a read-only key when only retrieving existing results, and confirm point spending before running analysis.

Risk: Review collection requires an external browser extension used with an Amazon buyer account; the extension package was not included in the inspected skill.

Mitigation: Review the extension's source and requested permissions before installation, verify downloads come from AstrMap over HTTPS, and use a dedicated buyer account isolated from seller or primary accounts.

## Reference(s):

- [AstrMap API Reference](references/api_reference.md)
- [AstrMap Browser Extension Security Guide](references/security.md)
- [AstrMap Extension Download Guide](https://www.astrmap.com/en/#download)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown, JSON]

**Output Format:** [Structured review data and analysis summarized as text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results vary by product, marketplace, task, and pagination.]

## Skill Version(s):

1.2.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
