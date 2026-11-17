## Description:

Provides Chinese-language guidance for using the ClawHub API, including authentication, endpoint references, examples, rate-limit handling, and security best practices.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason7602](https://clawhub.ai/user/jason7602)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill as ClawHub API reference material when integrating search, catalog, package, skill, plugin, security, and account endpoints. It helps agents produce implementation guidance, example API calls, and operational recommendations for ClawHub integrations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples for POST, DELETE, transfer, merge, rename, and admin operations can change ClawHub account or package state if run against real resources.

Mitigation: Run mutating examples only when the change is intended, and verify the target slug, package name, owner, and version before execution.

Risk: Bearer tokens shown in API examples could be copied into source code or logs.

Mitigation: Keep API tokens scoped, rotate them periodically, and store them outside source code, such as in environment variables or a secret manager.

Risk: Aggressive polling or retries can exceed ClawHub API limits.

Mitigation: Respect 429 responses, Retry-After, and rate-limit headers, and use caching or backoff for repeated catalog reads.

## Reference(s):

- [ClawHub API Guidance release page](https://clawhub.ai/jason7602/skills/clh-api-guidance)
- [API interface reference](artifact/reference/api-reference.md)
- [Data models](artifact/reference/data-models.md)
- [Enum reference](artifact/reference/enums.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with HTTP, cURL, and Python examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language API reference guidance; no hidden execution or persistence according to server security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
