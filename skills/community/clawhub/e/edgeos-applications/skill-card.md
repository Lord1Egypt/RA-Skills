## Description:

Apply to an EdgeOS popup city and buy tickets through OpenClaw. Use when users ask to authenticate by email OTP, submit/check popup applications, retrieve accepted applications and attendees, browse active products, purchase with checkout links, or settle crypto payments via /agent/buy-ticket (x402 + USDC on Base, optional AgentKit discount).

This skill is ready for commercial/non-commercial use.

## Publisher:

[franvinas](https://clawhub.ai/user/franvinas)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to authenticate with email OTP, submit and check EdgeOS popup-city applications, and purchase accepted tickets through checkout links or x402 USDC payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts the EdgeOS production API and may use application, profile, attendee, and payment data.

Mitigation: Use it only in a private workspace and confirm the target application, product, attendee mapping, and payment mode before submitting requests.

Risk: Login tokens are stored locally under the skill script state directory.

Mitigation: Clear scripts/.state after use, avoid shared machines, and re-authenticate only when needed.

Risk: The skill can help authorize real x402 USDC payments on Base.

Mitigation: Require the agent to show the exact amount, recipient, network, asset, and final consent before any wallet signature.

## Reference(s):

- [EdgeOS Applications ClawHub page](https://clawhub.ai/franvinas/skills/edgeos-applications)
- [API Contract](references/api-contract.md)
- [Conversation Flow](references/conversation-flow.md)
- [EdgeOS API Flow](references/flow.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON status and payment results from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns current status, concise next-step guidance, and operational IDs only when useful or explicitly requested.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
