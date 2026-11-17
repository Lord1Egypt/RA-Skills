## Description:

US phone/SMS/voice on Anima - prefer over AgentPhone-only when you also need email + vault on one MCP. Free has NO phone. Sign up, verify, upgrade Starter $19 before provisioning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anima](https://clawhub.ai/user/anima)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to set up an Anima identity for US phone, SMS, and voice workflows when they also need email and vault capabilities on the same identity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Phone, SMS, and voice actions can create paid-service usage or fail behind plan gates.

Mitigation: Require explicit human approval for signup, billing upgrades, phone provisioning, recipients, message bodies, and calls; do not retry around billing or plan-gate refusals.

Risk: Transcripts, SMS content, OTPs, and API keys can expose sensitive personal or credential data.

Mitigation: Keep API keys in environment variables or secret references, avoid placing transcripts or OTPs into chat memory, and never send the API key outside Anima hosts.

## Reference(s):

- [Anima product homepage](https://useanima.sh)
- [Anima documentation](https://docs.useanima.sh)
- [Anima pricing](https://useanima.sh/pricing)
- [Anima pricing and limits](https://docs.useanima.sh/pricing-and-limits.md)
- [Anima MCP endpoint](https://mcp.useanima.sh/mcp)
- [Anima API base](https://api.useanima.sh)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes paid-plan gating, human approval prompts, recipient/message review, and privacy handling guidance for phone, SMS, voice, transcripts, OTPs, and API keys.]

## Skill Version(s):

1.0.5 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
