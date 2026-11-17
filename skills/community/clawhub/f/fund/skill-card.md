## Description:

Adds USDC funds to a wallet through Coinbase Onramp or manual Base-network deposit instructions, with commands to check wallet status, address, and balance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[0xrag](https://clawhub.ai/user/0xrag)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to open a Coinbase Onramp funding flow, show a wallet address for manual USDC deposits on Base, and check wallet status or balance before and after funding.

### Deployment Geography for Use:

Coinbase Onramp supported regions, including the United States

## Known Risks and Mitigations:

Risk: The skill invokes an unpinned npm wallet tool in a real-money funding flow, so command behavior can change between runs.

Mitigation: Pin the CLI version before production use and review the resolved package before allowing wallet or funding actions.

Risk: Funding and manual deposit flows can expose users to fees, identity checks, regional restrictions, settlement delays, or funds sent to the wrong address.

Mitigation: Require explicit user confirmation before opening funding flows or sharing deposit instructions, and independently verify the wallet address before sending USDC.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/0xrag/skills/fund)
- [0xrag publisher profile](https://clawhub.ai/user/0xrag)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown instructions with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open wallet, browser, or payment-provider interfaces through the wallet companion app.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
