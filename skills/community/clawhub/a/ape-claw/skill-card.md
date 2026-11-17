## Description:

Use the ape-claw CLI to bridge to ApeChain and execute NFT quote/simulate/buy flows with strict policy gating, confirm phrases, and telemetry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simplefarmer69](https://clawhub.ai/user/simplefarmer69)

### License/Terms of Use:


## Use Case:

External developers and OpenClaw agent operators use this skill to guide ApeChain NFT discovery, quote, simulation, purchase, bridge, telemetry, and clawbot registration workflows from the command line.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and npx paths may run unverified remote code in an environment that also contains wallet or agent credentials.

Mitigation: Use pinned, verified installers or a sandboxed machine with no valuable wallet keys or reusable credentials present.

Risk: Wallet private keys and clawbot tokens are required for execution paths and could be exposed through shared environments or chat backends.

Mitigation: Treat APE_CLAW_PRIVATE_KEY and APE_CLAW_AGENT_TOKEN as secrets, isolate runtime state, and use only chat or telemetry backends you control.

Risk: Autonomous bridge or NFT purchase commands can execute onchain transactions with financial consequences.

Mitigation: Keep workflows read-only until doctor checks pass, simulation succeeds, spending policy is acceptable, and explicit confirmation or accepted autonomous execution is intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/simplefarmer69/skills/ape-claw)
- [ApeClaw website](https://apeclaw.ai)
- [OpenClaw website](https://openclaw.ai)
- [ApeClaw GitHub](https://github.com/simplefarmer69/ape-claw)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prefers JSON CLI output and includes dry-run, simulation, confirmation, and policy-gating guidance for transaction workflows.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
