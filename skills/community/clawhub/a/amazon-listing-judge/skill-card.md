## Description:

Grades Amazon product listing quality from an ASIN with a 0-100 score, dimension breakdown, and improvement suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linbeihanda](https://clawhub.ai/user/linbeihanda)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and developers can use this skill to assess Amazon product listing quality from an ASIN and prioritize listing improvements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A long-lived CLAW_KEY and requested ASIN URL are sent to the configured external scraping service.

Mitigation: Use only a trusted HTTPS CLAW_API_BASE, protect and rotate the CLAW_KEY, and avoid submitting sensitive or private product URLs.

Risk: The script depends on httpx without a pinned dependency version.

Mitigation: Pin dependencies and review dependency updates before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/linbeihanda/skills/amazon-listing-judge)
- [CLAW Key Provider](https://claw-school.com)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [JSON from the grading script, typically summarized as a structured Markdown report by the agent.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CLAW_KEY and CLAW_API_BASE; each run sends the requested ASIN URL to the configured external scraping service.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
