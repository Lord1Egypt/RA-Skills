## Description:

Provides cross-asset market event intelligence to help trading and research agents investigate events and explain potential asset impacts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tradewr333-lgtm](https://clawhub.ai/user/tradewr333-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Trading and research agents use the skill to investigate news-driven moves across stocks, ETFs, crypto, commodities, rates, and FX, and to review event evidence and exposure before decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market queries and watched tickers are sent to an external service; requests may include an API key.

Mitigation: Share only information you are comfortable sending to Degenscan Intel and protect the API key.

Risk: Calls beyond the free allowance may incur per-call charges.

Mitigation: Review the published prices and require approval before paid calls.

Risk: Market-impact signals may be incomplete or misleading if treated as trading advice.

Mitigation: Check primary evidence and independent sources before making trading decisions.

## Reference(s):

- [Degenscan Intel on ClawHub](https://clawhub.ai/tradewr333-lgtm/skills/degenscan-intel)
- [Degenscan Intel documentation](https://degenscan-intel.onrender.com/llms.txt)

## Skill Output:

**Output Type(s):** [Text, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with JSON and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Event and impact signals are research inputs, not trading advice.]

## Skill Version(s):

1.0.0 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
