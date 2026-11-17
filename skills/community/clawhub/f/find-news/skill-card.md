## Description:

Multi-engine search API skill for web, news, social, video, and code search, with optional full-content crawling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lazyboyjgn99](https://clawhub.ai/user/lazyboyjgn99)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search general web results, news, social platforms, video platforms, and GitHub, and to optionally retrieve full page content when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries, sensitive URLs, and crawled content may be exposed because the skill sends requests to a third-party plaintext HTTP API.

Mitigation: Avoid sending secrets, personal information, confidential business terms, or sensitive URLs through the skill unless the provider replaces HTTP with HTTPS and documents query and content handling.

Risk: The bundled instructions use a shared hardcoded bearer token, creating credential exposure and abuse risk.

Mitigation: The provider should remove the shared token, rotate it, and use a per-user secret or managed authentication flow outside the public skill instructions.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, JSON, API Calls, Guidance]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search responses include result titles, URLs, snippets, optional crawled content, result totals, and cache status.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
