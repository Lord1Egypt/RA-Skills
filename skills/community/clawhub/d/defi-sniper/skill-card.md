## Description:

Meta-skill for early token-launch intelligence and execution orchestration across Solana and Base using minara, torchmarket, and torchliquidationbot.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h4gen](https://clawhub.ai/user/h4gen)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to coordinate early token-launch detection, on-chain risk triage, social-signal confirmation, and bounded swap execution decisions for Solana and Base workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup uses unpinned latest installers and a broad update-all command in a wallet and trading context.

Mitigation: Use a dedicated least-privileged environment, avoid update --all, and pin reviewed installer and dependency versions before connecting wallet secrets.

Risk: Live execution can submit real trades through signer or vault-routed paths.

Mitigation: Require manual confirmation unless the execution path and limits have been separately audited, and enforce configured entry-size and slippage caps.

Risk: On-chain and social checks do not provide a single definitive rug, honeypot, or safety verdict.

Mitigation: Require multiple independent indicators, keep ambiguous cases in observe or paper mode, and prefer no_trade when evidence conflicts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/h4gen/skills/defi-sniper)
- [Publisher profile](https://clawhub.ai/user/h4gen)
- [Inspected upstream skills](references/inspected-skills.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured decision sections and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs include detection, on-chain risk, social signal, execution decision, and audit trail sections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
