## Description:

Claw Search provides a web search API and CLI for AI agents, with support for search results, content extraction, suggestions, usage statistics, and optional search backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanchao193](https://clawhub.ai/user/yuanchao193)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to give agents web search capability through a hosted or self-deployed API, plus a local CLI wrapper for issuing queries. It is suited for retrieving search-result metadata and related web content for agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated service endpoints may allow command execution, internal-network browsing, or exposure of shared search history.

Mitigation: Do not run as a public or trusted service until patched; replace shell-based search execution with argument-based process calls, restrict URL extraction, remove shared history exposure, and deploy only in isolated environments without secrets or internal-network access.

Risk: Search queries and fetched content can be transmitted to external search or content sources.

Mitigation: Disclose query transmission and retention behavior, sanitize frontend rendering, and avoid submitting sensitive or confidential queries.

Risk: Dependency and deployment evidence indicates the release needs security review before production exposure.

Mitigation: Regenerate dependencies from HTTPS sources, apply security patches, and validate the patched service with security tests before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yuanchao193/skills/claw-search)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Search CLI Script](artifact/scripts/search.mjs)

## Skill Output:

**Output Type(s):** [JSON, Text, Shell commands]

**Output Format:** [JSON API responses and plain-text CLI summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search outputs include query text, result counts, titles, URLs, descriptions, source metadata, and optional cached or extracted content fields.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact package.json lists 1.0.0 and UNFLAG_REQUEST.md lists 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
