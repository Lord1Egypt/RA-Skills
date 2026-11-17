## Description:

Provides Bitcoin market intelligence over Lightning L402, including live price, Fear & Greed, mempool fees, ETF flows, on-chain metrics, prediction market odds, curated news, and breaking alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr0zen80](https://clawhub.ai/user/fr0zen80)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to call a paid Bitcoin intelligence API that returns market briefs, alert status, and service health over Lightning. It is intended for agents that can use lnget, access Tor, and pay L402 invoices from a funded Lightning node.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid examples can spend Lightning funds from a funded node.

Mitigation: Call the free health endpoint first and require explicit user approval or spending limits before running paid lnget commands.

Risk: The skill depends on Tor access, lnget, and a configured Lightning node, so calls may fail or hang if those prerequisites are unavailable.

Mitigation: Check local Tor, lnget, LND, and channel funding status before attempting paid endpoint calls.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fr0zen80/skills/derek-bitcoin-intel)
- [lnget](https://github.com/lightninglabs/lnget)
- [Derek Health Endpoint](http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/health)
- [Derek Market Brief Endpoint](http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/market-brief)
- [Derek Latest Alert Endpoint](http://jnfaphddbeubdgpsbrw4d2z6wjew57djdzyrzkbt2ta7bi3wfzmfsfyd.onion/api/latest-alert)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with inline bash commands and endpoint descriptions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Paid API calls may spend 50 to 100 sats through lnget and require Tor plus a funded Lightning node.]

## Skill Version(s):

3.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
