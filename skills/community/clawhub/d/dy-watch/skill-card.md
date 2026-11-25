## Description:

Provides read-only access to public Douyin search, creator posts, post details, comments, and trending lists, returning structured JSON for sentiment and brand-mention analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, customer support, and content teams can retrieve public Douyin posts, creator profiles, comments, and trending topics, then use the structured data to assess sentiment, track brand mentions, and compare reputation trends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queries send supplied keywords or Douyin links to the Guaikei service.

Mitigation: Avoid sending sensitive search terms or links, and use the skill only with public content.

Risk: The security scan has medium confidence and partial component coverage.

Mitigation: Review the skill's data handling and permissions before installation.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/guaikei/skills/dy-watch)
- [Guaikei service](https://www.guaikei.com)
- [Usage and output contract](references/contract.md)
- [Options and limits](references/options.md)
- [Errors and retry guidance](references/errors.md)
- [Setup and data handling FAQ](references/faq.md)

## Skill Output:

**Output Type(s):** [JSON, API data]

**Output Format:** [Structured JSON envelope containing result arrays or objects]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public Douyin search, profile, post, comment, and trending data; optional local JSON logging is documented.]

## Skill Version(s):

1.5.1 (source: SKILL.md frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
