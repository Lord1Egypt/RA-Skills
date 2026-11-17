## Description:

Decision Gate Verifier provides third-party verification that an AI agent's action matched a previously committed claim and returns a signed PASS, REFUSE, or IN_DOUBT receipt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vaahl-dev](https://clawhub.ai/user/vaahl-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they need an independently signed verdict that an autonomous action stayed within a prior policy or claim, such as for payouts, donations, spending, or irreversible releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can authorize real USDC payments using server-supplied payment terms.

Mitigation: Use a dedicated low-balance wallet funded only with the intended Base USDC amount, verify payment terms and endpoints before signing, and require explicit confirmation before automated use.

Risk: The client requires access to a wallet private key.

Mitigation: Use a separate operational wallet, keep the key out of shared logs and repositories, and rotate or retire it if exposure is suspected.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/vaahl-dev/skills/decision-gate-verifier)
- [Decision Gate](https://soulscore.xyz/decision-gate?src=clawhub)
- [Soulscore methodology](https://soulscore.xyz/methodology?src=clawhub)

## Skill Output:

**Output Type(s):** [text, JSON, code, shell commands, configuration]

**Output Format:** [Python client calls and JSON verdict receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns PASS, REFUSE, or IN_DOUBT receipts; optional on-chain receipt anchoring is described in the artifact.]

## Skill Version(s):

0.4.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
