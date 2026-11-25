## Description:

A read-only skill for searching public Douyin trends, creators, videos, and comments and returning structured data for analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guaikei](https://clawhub.ai/user/guaikei)

### License/Terms of Use:

MIT

## Use Case:

Content operators, marketers, and analysts use this skill to review public Douyin trends, creator activity, video details, and comments for topic planning, competitor research, and sentiment analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment is incomplete: 22 files were only partially inspected and tool-misuse analysis was degraded.

Mitigation: Consider this uncertainty before installing and review the skill files before use.

Risk: The skill sends search terms or Douyin links to the Guaikei service and requires an API token.

Mitigation: Use only public data and avoid submitting sensitive search terms or links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guaikei/skills/dy-trend)
- [Guaikei API service](https://www.guaikei.com)
- [Usage options](references/options.md)
- [Output contract](references/contract.md)
- [Routing guide](references/routing.md)
- [Errors and limits](references/errors.md)
- [FAQ and setup](references/faq.md)
- [Demand mining guide](references/demand-mining.md)
- [Customer acquisition guide](references/customer-acquisition.md)

## Skill Output:

**Output Type(s):** [JSON, Analysis]

**Output Format:** [Structured JSON response envelope with search, creator, video, comment, or hot-list records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only public data; request limits vary by plan, and calls require a GUAIKEI_API_TOKEN.]

## Skill Version(s):

1.5.1 (source: frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
