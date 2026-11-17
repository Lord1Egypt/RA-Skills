## Description:

Daily news and hot topics via the 6551 API. Supports news categories, hot news articles, and trending tweets by category.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infra403](https://clawhub.ai/user/infra403)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch daily news categories, hot news articles, and trending tweets from the 6551 API without authentication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: News category and subcategory requests, plus normal network metadata such as IP address and timing, are sent to the 6551 API.

Mitigation: Use the skill only when sharing those requests and network metadata with the 6551 API is acceptable.

Risk: The API may return a 503 response while data is still being generated.

Mitigation: Handle 503 responses as temporary availability delays and retry later instead of treating them as final results.

## Reference(s):

- [Daily News ClawHub page](https://clawhub.ai/infra403/skills/6551-daily-news)
- [6551 API base URL](https://ai.6551.io)
- [News categories endpoint](https://ai.6551.io/open/free_categories)
- [Hot news endpoint](https://ai.6551.io/open/free_hot?category=macro)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; sends category and subcategory requests to https://ai.6551.io; no credentials required.]

## Skill Version(s):

0.1.0 (source: release metadata; artifact metadata.version is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
