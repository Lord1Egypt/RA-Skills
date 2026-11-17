## Description:

Guides an agent through helping a user add funds to a Finance District wallet by checking authentication, retrieving wallet addresses, and explaining onramp or direct-transfer options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachidjarray-hk-qa-fdt](https://clawhub.ai/user/rachidjarray-hk-qa-fdt)

### License/Terms of Use:

MIT-0

## Use Case:

External users and wallet-support agents use this skill when a user needs to top up, deposit, onramp, or transfer tokens into a Finance District wallet, including after an insufficient-balance event.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad funding-related triggers that could invoke it in the wrong financial context.

Mitigation: Confirm the user intends to fund a Finance District wallet before retrieving or sharing wallet details.

Risk: The allowed tools include an unused account-information command.

Mitigation: Review the tool allowlist and remove getMyInfo unless a documented workflow needs it.

Risk: Sending tokens on the wrong chain may result in lost funds.

Mitigation: Ask the user to confirm the target chain and verify the displayed address before any transfer.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rachidjarray-hk-qa-fdt/skills/fund-wallet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and human-facing wallet-funding guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include chain-specific wallet address guidance and funding confirmation steps.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
