## Description:

Private payments for AI agents with no on-chain link between sender and recipient.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mmchougule](https://clawhub.ai/user/mmchougule)

### License/Terms of Use:


## Use Case:

Developers and agent builders use Clawpay to produce code, command, and API guidance for private USDT or USDC payments on BSC through the ClawPay API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks an agent to handle wallet private keys and reusable signatures.

Mitigation: Use a dedicated low-balance wallet, avoid primary wallet keys, and prefer a managed signing flow where available.

Risk: The skill can guide real token transfers to an external invoice or recipient address.

Mitigation: Verify the recipient, amount, token, chain, and invoice destination before any transfer, and test in a sandbox or testnet flow first.

Risk: The flow depends on external API calls, dependencies, and signatures that may not be nonce-bound.

Mitigation: Review responses before acting, pin dependencies, and prefer flows with nonce-bound signatures, signed invoices, and explicit confirmations.

## Reference(s):

- [ClawPay API and homepage](https://clawpay.dev)
- [ClawHub skill page](https://clawhub.ai/mmchougule/skills/clawpay-2)
- [BSC public RPC endpoint](https://bsc-dataseed.binance.org/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown with JavaScript, JSON, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes executable payment examples and API request guidance; does not execute transfers by itself.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter says 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
