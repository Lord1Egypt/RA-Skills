## Description:

Content Gen helps agents generate social calendars, scripts, SEO articles, listing copy, newsletters, and related marketing content with scoring and rewrite metadata for review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drivenautoplex1](https://clawhub.ai/user/drivenautoplex1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, marketers, real estate operators, and developers use this skill to generate marketing content across multiple formats and receive structured score metadata and rewrite notes for review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Quality scores may be presented as proof even though the evidence does not include an auditable scoring implementation or methodology.

Mitigation: Treat scores as internal heuristics and review the methodology before using scores in customer-facing material.

Risk: Inputs may include private business or customer notes, and generation may involve external LLM data handling depending on configuration.

Mitigation: Avoid sensitive inputs unless external LLM transmission is acceptable and apply an appropriate data handling review.

Risk: The install evidence names a dependency but does not provide a pinned or locked install path.

Mitigation: Use a pinned dependency or lockfile-based installation before production use.

## Reference(s):

- [Content Gen on ClawHub](https://clawhub.ai/drivenautoplex1/skills/content-gen)
- [OpenClaw Skills homepage](https://github.com/drivenautoplex1/openclaw-skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown and structured JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include content, neural_score metadata, score_badge text, structured_output, and rewrite notes.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
