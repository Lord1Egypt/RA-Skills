## Description:

Anima Identity helps agents create and operate an Anima-backed identity with email, US phone/SMS, voice, encrypted vault access, and MCP/API usage guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anima](https://clawhub.ai/user/anima)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to onboard an agent to Anima, configure MCP/API access, send and receive email, and use plan-gated phone, SMS, voice, and vault capabilities with human approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through account signup, email, SMS, phone call, and billing upgrade flows.

Mitigation: Require explicit human confirmation before signup, messaging, calls, or paid upgrades, and stop when the human has not approved the action.

Risk: The Anima API key enables access to the agent identity and could be misused if exposed.

Mitigation: Store the key only in a protected environment variable or secret store, avoid putting it in memory or transcripts, and send it only to Anima API or MCP endpoints.

Risk: Email, SMS, and voice capabilities can create abuse, consent, or regulatory exposure.

Mitigation: Use these channels only with required consent, do not spam, phish, or impersonate, and honor plan gates and TCPA-related restrictions.

Risk: The optional npm CLI is third-party executable code.

Mitigation: Install it only after deciding to trust the Anima package, and pin the version when used.

## Reference(s):

- [Anima product homepage](https://useanima.sh)
- [Anima documentation](https://docs.useanima.sh)
- [Anima MCP endpoint](https://mcp.useanima.sh/mcp)
- [Anima API base](https://api.useanima.sh)
- [Anima console](https://console.useanima.sh)
- [Anima pricing](https://useanima.sh/pricing)
- [Anima plan limits](https://docs.useanima.sh/pricing-and-limits.md)
- [Anima OAuth connect](https://connect.useanima.sh)
- [ClawHub publisher profile](https://clawhub.ai/user/anima)
- [ClawHub skill page](https://clawhub.ai/anima/skills/anima-identity)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Markdown, JSON]

**Output Format:** [Markdown guidance with bash, JSON, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service signup, verification, messaging, phone, voice, vault, MCP configuration, and paid upgrade guidance.]

## Skill Version(s):

1.0.7 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
