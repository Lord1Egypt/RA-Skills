## Description:

Searches the web with DuckDuckGo and fetches readable content from URLs without requiring API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mengbin92](https://clawhub.ai/user/mengbin92)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform DuckDuckGo web searches and retrieve readable page text when built-in web search or fetch tooling is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Arbitrary URL fetching could reach internal services from the agent environment.

Mitigation: Avoid private URLs, localhost, intranet hosts, cloud metadata addresses, and token-bearing URLs; run the skill in a network-restricted environment.

Risk: Outbound web requests may disclose sensitive search terms or URLs.

Mitigation: Use the skill only for non-sensitive searches and public URLs.

Risk: The artifact instructs users to install a dependency that the current scripts do not require.

Mitigation: Remove or pin the unnecessary dependency instruction before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mengbin92/skills/ddg-search-fetch)
- [DuckDuckGo Lite endpoint](https://lite.duckduckgo.com/lite/)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands]

**Output Format:** [JSON search results or fetched URL content, with optional plain text output for fetched pages]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search results are capped at 20; fetched page text is truncated to 10000 characters.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
