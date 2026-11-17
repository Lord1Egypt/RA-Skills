## Description:

Expert guide for using Agent Bazaar (agent-bazaar.com), a capabilities marketplace where AI agents discover, evaluate, and purchase skills via the x402 payment protocol.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hockeyplaya48](https://clawhub.ai/user/hockeyplaya48)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover Agent Bazaar capabilities, prepare paid x402 API calls, test endpoints in demo mode, and orchestrate multi-step workflows that use marketplace skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents toward paid external API calls and cumulative marketplace spend.

Mitigation: Use demo mode first, require explicit approval before every paid call, and verify amount, recipient, network, endpoint, and cumulative spend.

Risk: Requests may send user content or project data to remote Agent Bazaar services.

Mitigation: Do not send proprietary code, secrets, customer data, private URLs, or sensitive portfolio details unless the user has intentionally approved that disclosure.

Risk: Documented package installation commands may introduce supply-chain exposure.

Mitigation: Prefer pinned, local SDK installs over global npm installs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hockeyplaya48/skills/agent-bazaar)
- [Agent Bazaar](https://agent-bazaar.com)
- [Agent Bazaar endpoint catalog](references/endpoints.md)
- [Agent Bazaar programmatic integration](references/sdk-usage.md)
- [x402 Payment Protocol - Agent Bazaar](references/x402-protocol.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown with inline bash, JSON, Python, and TypeScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may prepare paid external API calls and should use demo mode before real payments.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
