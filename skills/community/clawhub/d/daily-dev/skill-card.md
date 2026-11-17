## Description:

Overcome LLM knowledge cutoffs with real-time developer content. daily.dev aggregates articles from thousands of sources, validated by community engagement, with structured taxonomy for precise discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[idoshamun](https://clawhub.ai/user/idoshamun)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query daily.dev API documentation, retrieve current developer content, personalize feeds and bookmarks, and synthesize technology updates with source links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill can guide agents to scan GitHub activity, modify daily.dev account data, and run background or scheduled personalization without enough explicit consent and scoping guardrails.

Mitigation: Review before installing, use it only for explicitly requested daily.dev API work, limit GitHub analysis to authorized repositories, and require confirmation before changing feeds, bookmarks, profile, or scheduled behavior.

Risk: The skill uses a personalized daily.dev API token.

Mitigation: Store tokens in a secret manager or environment variable, send them only to api.daily.dev, and avoid pasting real tokens into shell commands or profile files.

## Reference(s):

- [daily.dev API base URL](https://api.daily.dev/public/v1)
- [daily.dev OpenAPI specification](https://api.daily.dev/public/v1/docs/json)
- [daily.dev API token settings](https://app.daily.dev/settings/api)
- [ClawHub skill page](https://clawhub.ai/idoshamun/skills/daily-dev)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, API endpoint references, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include curl and jq examples for daily.dev API requests.]

## Skill Version(s):

0.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
