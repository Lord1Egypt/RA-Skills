## Description:

FinStep Tools helps agents retrieve FinStep financial market, sector, company, macroeconomic, research, and news data through shell wrappers around the FinStep service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zacbai](https://clawhub.ai/user/zacbai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to query A-share market quotes, sector rankings, company fundamentals, macroeconomic indicators, trading calendars, and finance-related search results through FinStep's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends the FINSTEP API signature and user financial queries over plaintext HTTP, with the signature included in the request URL.

Mitigation: Use only a low-value or short-lived signature, avoid sensitive queries, and prefer a restricted network environment until the publisher supports HTTPS and non-query-string credential handling.

Risk: General web and URL fetching features are present but underdocumented.

Mitigation: Review or restrict use of the web search and URL parsing commands before deployment, especially in environments handling confidential data.

Risk: User-provided inputs are passed into shell-built request payloads.

Mitigation: Avoid passing untrusted strings directly to the scripts and review input serialization before using the skill in automated workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zacbai/skills/finstep-tools)
- [FinStep MCP API base URL](http://fintool-mcp.finstep.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON responses from the FinStep service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a FINSTEP_SIGNATURE environment variable before script execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
