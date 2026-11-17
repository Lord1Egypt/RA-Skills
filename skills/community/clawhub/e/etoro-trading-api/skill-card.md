## Description:

eToro Public API for trading, market data, social feed, and watchlist integration with SSO, Bearer, and API key authentication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoniassia](https://clawhub.ai/user/yoniassia)

### License/Terms of Use:


## Use Case:

External developers and agents use this skill to work with eToro account, trading, market data, social feed, and watchlist API workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated trading endpoints can place, close, or cancel real-money orders because trading tools default to real mode.

Mitigation: Default agent workflows to demo mode and require explicit transaction-specific confirmation before any live open, close, cancel, or limit order.

Risk: Full request details are logged before trading execution, which can expose sensitive account, order, or credential-adjacent data in logs.

Mitigation: Review logging before deployment, restrict log access, and redact sensitive request fields where possible.

## Reference(s):

- [eToro Public API Docs](https://etoro-6fc30280.mintlify.app/)
- [eToro Public API Base URL](https://public-api.etoro.com/api/v1)
- [ClawHub Skill Page](https://clawhub.ai/yoniassia/skills/etoro-trading-api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline commands and configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May describe authenticated live or demo trading API calls and related request parameters.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
