## Description:

USE FOR news search. Returns news articles with title, URL, description, age, thumbnail. Supports freshness and date range filtering, SafeSearch filter and Goggles for custom ranking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sprintmint](https://clawhub.ai/user/sprintmint)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agents use this skill to query paid news-search endpoints and receive article results with filtering by freshness, date range, country, language, SafeSearch, and custom ranking rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic x402 payments can sign wallet transactions through an unpinned payment package.

Mitigation: Use a pinned, trusted version of the x402 payment client and verify the payment destination, network, asset, and amount before signing.

Risk: Running payment commands in a broad agent environment can expose unrelated secrets if the client or command is compromised.

Mitigation: Run payment commands in an environment with only the secrets required for that payment workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sprintmint/skills/cpbox-news-search)
- [x402 Payment Setup Prerequisites](https://github.com/springmint/cpbox-skills#prerequisites)
- [CPBox API Provider](https://www.cpbox.io)
- [CPPay Facilitator](https://www.cppay.finance)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP endpoint details, bash examples, parameter tables, and JSON response descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for paid x402 news-search requests; API responses include news result metadata such as titles, URLs, descriptions, ages, thumbnails, and optional fetch timestamps.]

## Skill Version(s):

1.0.0 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
