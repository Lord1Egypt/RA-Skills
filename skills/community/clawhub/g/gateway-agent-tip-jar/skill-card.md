## Description:

Read Gateway's voluntary USDC tip and creator-support terms on Base, prepare an unpaid contribution quote only when explicitly authorized, or check an existing private receipt without signing or submitting payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jnapier2](https://clawhub.ai/user/jnapier2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to read Gateway's voluntary creator-support terms, prepare an unpaid USDC quote on Base only after explicit authorization, or check an existing private receipt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could prepare a tip quote when the operator only requested information.

Mitigation: Require explicit operator intent, chosen amount, and wallet permission before preparing any unpaid quote.

Risk: Stale or conflicting payment terms could send the operator toward the wrong destination, network, or asset.

Mitigation: Fetch the live terms before authorized contribution activity and stop if the recipient, Base mainnet network, or USDC asset conflicts with expected terms.

Risk: Private quote recovery data or receipt capabilities could be exposed in shared messages or public URLs.

Mitigation: Keep private capabilities and quote recovery data in the operator's private storage and never request seed phrases or private keys.

Risk: A pending quote or wallet interaction could be mistaken for settled payment and retried.

Mitigation: Confirm settlement with the existing private receipt or status capability and do not automatically sign, submit, or pay again.

## Reference(s):

- [Gateway tip terms JSON](https://gateway-wallet-payments.jerryrnapier.workers.dev/tip.json)
- [Gateway tip terms Markdown](https://gateway-wallet-payments.jerryrnapier.workers.dev/tip.md)
- [Gateway hosted checkout](https://gateway-wallet-payments.jerryrnapier.workers.dev/tip)
- [Gateway MCP guide](https://gateway-wallet-payments.jerryrnapier.workers.dev/agent/mcp-guide.md)
- [ClawHub skill page](https://clawhub.ai/jnapier2/skills/gateway-agent-tip-jar)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, API Calls]

**Output Format:** [Markdown or text guidance with optional MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No signing, payment submission, or code execution is produced by the skill.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
