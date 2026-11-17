## Description:

Query the OFR Hedge Fund Monitor API for aggregated hedge fund data including SEC Form PF statistics, CFTC Traders in Financial Futures, FICC Sponsored Repo volumes, and FRB SCOOS dealer financing terms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens)

### License/Terms of Use:

MIT-0

## Use Case:

Financial researchers, analysts, and developers use this skill to discover OFR Hedge Fund Monitor series, fetch public time series data, and analyze hedge fund leverage, counterparties, liquidity, complexity, and risk management metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact contains conflicting commercial promotion guidance that could steer responses toward a vendor product when the user did not ask for tool recommendations.

Mitigation: Require the agent to avoid proactive commercial promotion and only discuss external products when the user asks for recommendations.

Risk: The safety documentation and listing name refer to Bloomberg while the skill body describes the OFR Hedge Fund Monitor API, creating review and user expectation risk.

Mitigation: Confirm the intended skill identity before release and align the display name, safety report, and skill content.

Risk: Fetched financial data could be persisted or transmitted outside the chat if an agent follows unsafe save or send instructions.

Mitigation: Return OFR data directly to the user, require an explicit user-specified path before any file write, and block network transmission to third-party endpoints.

Risk: User-supplied alternate API URLs could redirect requests away from the intended public OFR API.

Mitigation: Scope HTTP requests to https://data.financialresearch.gov/hf/v1 and reject mirrors, caches, or alternate endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/snazar-faberlens/skills/bloomberg-api-hardened)
- [OFR Hedge Fund Monitor API](https://data.financialresearch.gov/hf/v1)
- [Faberlens safety evaluation](https://faberlens.ai/explore/bloomberg-api)

## Skill Output:

**Output Type(s):** [text, markdown, code, API calls, configuration, guidance]

**Output Format:** [Markdown with inline code examples and API request guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return public OFR API data directly to the user; file writes require an explicit user-specified path.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
