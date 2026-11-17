## Description:

Transaction round-up helper. Calculates spare change from payments and builds unsigned Solana transfer instructions for user review. Server-side fee enforcement. REST API for any language.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nightcode112](https://clawhub.ai/user/nightcode112)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agents use this skill to calculate transaction round-ups, request unsigned Solana transfer or swap instructions, and present those instructions for user review and signing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial loss or unintended transfers could occur if unsigned transaction instructions are not inspected before signing.

Mitigation: Independently inspect every unsigned transaction for the expected wallet, treasury, asset, amount, and program before signing.

Risk: API key exposure could allow unauthorized use of the Buff API.

Mitigation: Use a scoped, rotatable API key and rotate it if exposure is suspected.

Risk: Unexpected investment amounts may result from configuration or service behavior.

Mitigation: Start with small amounts and verify round-up breakdowns before approving executable instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nightcode112/skills/buff-roundup)
- [Buff documentation](https://buff.finance/docs)
- [Buff REST API reference](https://buff.finance/docs/api/rest)
- [Buff swap documentation](https://buff.finance/docs/swaps)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with TypeScript and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for API-backed round-up calculations and unsigned transaction review; it does not sign transactions or hold private keys.]

## Skill Version(s):

2.3.5 (source: server evidence release.version and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
