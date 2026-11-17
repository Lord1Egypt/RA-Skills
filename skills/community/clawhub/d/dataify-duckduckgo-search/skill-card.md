## Description:

Run a DuckDuckGo web search. Do not use when the user explicitly requests Google, Bing, or Yandex.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dataify-server](https://clawhub.ai/user/dataify-server)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to run DuckDuckGo searches through Dataify, map user search requests to supported parameters, and return result links or raw JSON/HTML when requested.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search queries and the Dataify API token are sent to Dataify.

Mitigation: Avoid sensitive, secret, or private internal text in search requests, and install the skill only where Dataify token use is acceptable.

Risk: The documented command pattern can allow shell command injection when untrusted request text is interpolated into a shell command.

Mitigation: Pass arguments safely without shell interpolation, review commands before execution, or require the publisher to fix the invocation pattern.

Risk: Token handling is broader than necessary.

Mitigation: Use least-privilege token handling, avoid printing token values, and confirm credential storage practices before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dataify-server/skills/dataify-duckduckgo-search)
- [Dataify search request endpoint](https://scraperapi.dataify.com/request)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, HTML, shell commands, guidance]

**Output Format:** [Markdown search results by default; raw JSON or HTML when explicitly requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a search query and a Dataify API token; maximum result count is clamped to 50.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
