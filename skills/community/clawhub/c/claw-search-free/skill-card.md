## Description:

Provides free web, image, news search, and autocomplete suggestions via the Claw Search API without requiring an API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanchao193](https://clawhub.ai/user/yuanchao193)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill when an OpenClaw agent needs web search, image search, news search, or autocomplete suggestions through a no-key external search API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms, image queries, news topics, and autocomplete text are sent to claw-search.com and may be sent to its upstream search provider.

Mitigation: Do not use the skill for secrets, credentials, private internal names, regulated personal data, or confidential investigations unless that external disclosure is acceptable.

Risk: The free API documents a default rate limit of 100 requests per minute.

Mitigation: Design agent workflows with request throttling, retries, or fallback behavior for high-volume use.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yuanchao193/skills/claw-search-free)
- [Claw Search API](https://www.claw-search.com)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [Markdown guidance with JavaScript snippets, configuration examples, and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search endpoints return JSON results from an external service with documented count and offset parameters.]

## Skill Version(s):

2.0.0 (source: server release metadata; artifact package.json states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
