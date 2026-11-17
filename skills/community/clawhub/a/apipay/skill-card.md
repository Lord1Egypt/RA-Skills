## Description:

apipay lets agents use prepaid web search, URL fetch, and weather APIs through a bearer-token MCP server without asking users for common vendor keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iamalanlui](https://clawhub.ai/user/iamalanlui)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect agents to prepaid search, URL fetch, weather, balance, and vault-link APIs while avoiding unnecessary vendor-key requests for supported no-key catalog paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP setup runs an unpinned remote `apipay-mcp` package with an Apipay bearer token.

Mitigation: Install a pinned and vetted `apipay-mcp` release and run the MCP server with only the Apipay token in its environment.

Risk: BYOK catalog slugs can receive third-party API keys without enough custody details in the evidence.

Mitigation: Use dedicated revocable vendor keys with strict limits and confirm storage, deletion, and protection practices before using BYOK slugs.

Risk: Bearer tokens or request and response bodies could expose sensitive usage details if mishandled.

Mitigation: Keep bearer tokens out of URLs and chat, use low-quota tokens, and follow the artifact guidance to avoid logging request or response bodies.

## Reference(s):

- [apipay homepage](https://apipay.fly.dev)
- [apipay signup API](https://apipay.fly.dev/v1/signup)
- [apipay hosted MCP endpoint](https://apipay.fly.dev/mcp)
- [ClawHub apipay skill page](https://clawhub.ai/iamalanlui/skills/apipay)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with JSON configuration snippets and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return live web search, fetched markdown, weather data, balance details, or payment/top-up guidance through Apipay API calls.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
