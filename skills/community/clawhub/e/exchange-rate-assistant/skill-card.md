## Description:

Provides exchange-rate lookup, currency conversion, trend analysis, and historical exchange-rate lookup for major global currencies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luokeer52](https://clawhub.ai/user/luokeer52)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to request exchange-rate lookups, currency conversions, exchange-rate trend analysis, and historical rate information through a ClawHub/OpenClaw wrapper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The remote execution boundary is broad for an exchange-rate lookup skill.

Mitigation: Install only after the publisher clearly documents what remote service is invoked, what data is sent, and which HTTPS origins are trusted.

Risk: The client fetches, stores, and forwards API credentials, with plaintext persistence enabled by default in the artifact behavior.

Mitigation: Use environment-provided credentials where possible, set PRANA_SKILL_SKIP_WRITE_API_KEY=1 to avoid local plaintext key files, and rotate any PRANA_SKILL keys that were stored or exposed.

Risk: Purchase-history URL access is bundled with the exchange-rate wrapper.

Mitigation: Remove or separate purchase-history access unless that capability is explicitly required for the deployment.

Risk: Runtime dependencies are not pinned in the artifact instructions.

Mitigation: Pin and review the Node.js and Python dependencies before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luokeer52/skills/exchange-rate-assistant)
- [Runtime instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, json, guidance]

**Output Format:** [JSON response content from the remote exchange-rate assistant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session thread metadata for follow-up requests.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
