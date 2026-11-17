## Description:

Run user-facing EasyClaw DEX actions from a self-contained skill folder. Use when an agent needs to submit user orders or check wallet/margin/order balances on EasyClaw without depending on external project directories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ice-coldbell](https://clawhub.ai/user/ice-coldbell)

### License/Terms of Use:


## Use Case:

External developers and trading operators use this skill to let an agent inspect EasyClaw wallet, margin, order, market, and portfolio state; submit DEX orders; manage authenticated agent and strategy controls; monitor websocket channels; and run signal-driven auto-trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can grant an agent live trading authority, including order submission and signal-driven auto-trading.

Mitigation: Use devnet or dry-run first, set a finite --max-orders limit, and require explicit review before enabling live execution.

Risk: Backend controls include authenticated agent, strategy, risk, and kill-switch commands that can affect account behavior.

Mitigation: Scope API tokens narrowly, keep tokens separate from wallet keys, and review backend control commands before allowing an agent to invoke them.

Risk: Arbitrary or untrusted API, websocket, RPC, or program ID settings could route actions to unintended infrastructure.

Mitigation: Use trusted endpoint values only and confirm ORDER_ENGINE_PROGRAM_ID and MARKET_REGISTRY_PROGRAM_ID before placing orders.

Risk: Onboarding writes wallet path selections and strategy files into local skill state.

Mitigation: Treat wallet paths, .env contents, and strategy files as sensitive local configuration and restrict access to the skill directory.

## Reference(s):

- [EasyClaw skill source homepage](https://github.com/ice-coldbell/easyclaw/tree/main/easyclaw-skill)
- [ClawHub EasyClaw skill page](https://clawhub.ai/ice-coldbell/skills/easyclaw)
- [EasyClaw User DEX Env Reference](references/dex-env.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-capable command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may read wallet and backend credentials from environment variables and local config, write onboarding state under the skill directory, call Solana RPC and EasyClaw API or websocket endpoints, and submit live orders when not run in dry-run mode.]

## Skill Version(s):

0.0.2 (source: ClawHub release metadata; artifact frontmatter and package.json report 0.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
