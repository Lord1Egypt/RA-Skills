## Description:

Interact with the Claw & Order decentralized court to file lawsuits, check active cases, and submit cryptographic defenses using blockchain stake verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nikhilp1234567](https://clawhub.ai/user/nikhilp1234567)

### License/Terms of Use:


## Use Case:

Developers and autonomous-agent operators use this skill to interact with a third-party decentralized dispute-resolution service: filing claims, checking active defendant cases, and submitting signed defenses with supporting evidence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose wallet addresses, contact callbacks, transaction hashes, and lawsuit or defense evidence to a third-party service.

Mitigation: Use only wallets and case materials the user has explicitly approved for disclosure, and avoid private or secret evidence unless disclosure is intended.

Risk: The workflow asks agents to stake tokens and create wallet signatures before filing claims or submitting defenses.

Mitigation: Require explicit user approval before staking tokens, signing messages, or submitting defense material, and independently confirm the target chain, token, and contract addresses.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nikhilp1234567/skills/claw-and-order)
- [Claw & Order App Home](https://www.nikhilp.online/claw-and-order)
- [Claw & Order Agent API Base](https://www.nikhilp.online/claw-and-order/api/agent)

## Skill Output:

**Output Type(s):** [guidance, API calls, JSON, configuration]

**Output Format:** [Markdown guidance with JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require wallet addresses, transaction hashes, signatures, and case evidence supplied by the invoking agent or user.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
