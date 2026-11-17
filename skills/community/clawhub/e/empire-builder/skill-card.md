## Description:

Empire Builder AI skill for SmartVault treasuries, leaderboards, boosters, prepare-executeBatch-store distributions, burns, airdrops, and Clanker deploys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cryptorabble](https://clawhub.ai/user/cryptorabble)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide Empire Builder integrations for treasury reads and controlled mainnet write workflows, including distributions, burns, airdrops, leaderboards, boosters, staking, and Clanker-linked Empire launches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill guides live mainnet treasury and account-changing workflows.

Mitigation: Require human review before any signing or transaction broadcast, and confirm target chain, vault address, calldata, recipients, amounts, and mined receipts.

Risk: Some signing guidance is weakly scoped and captured signatures may be reusable outside the operator's intended context.

Mitigation: Use auditable messages with explicit action, empire identifier, timestamp, and nonce where supported, and treat signatures as sensitive credentials.

Risk: The documented API includes an unnecessary privateKey field.

Mitigation: Never send wallet private keys or seed material through Empire Builder API payloads or agent prompts.

## Reference(s):

- [Empire Builder skill homepage](https://empirebuilder.world/skill/SKILL.md)
- [ClawHub skill page](https://clawhub.ai/cryptorabble/skills/empire-builder)
- [HTTP API reference](references/http-api.md)
- [End-to-end workflows](references/workflows.md)
- [SmartVault contract reference](references/contracts.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with API payloads, command examples, and code-oriented integration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include live mainnet API and transaction steps that require human review before signing or broadcast.]

## Skill Version(s):

1.3.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
