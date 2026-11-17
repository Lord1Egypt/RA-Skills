## Description:

Scaffold Celo dApps with Celo Composer. Use when starting new Celo projects, creating MiniPay apps, or setting up development environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[san-npm](https://clawhub.ai/user/san-npm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold Celo dApps, MiniPay Mini Apps, Farcaster Miniapps, and related Next.js/Web3 development environments with Celo Composer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends running an unpinned npm package with npx.

Mitigation: Use a pinned, vetted package version and run scaffolding in a clean workspace before adopting the generated project.

Risk: Deployment examples can broadcast blockchain transactions and may spend funds.

Mitigation: Test deployments on the intended network with low-privilege development keys before using any production keys or funded accounts.

Risk: Generated projects may require credentials such as WalletConnect, Alchemy, CeloScan, or deployment private keys.

Mitigation: Add credentials only after reviewing the generated files, and avoid exposing private keys in shells, logs, or committed environment files.

## Reference(s):

- [Celo Composer Templates](references/templates.md)
- [ClawHub skill page](https://clawhub.ai/san-npm/skills/celo-composer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include npm, pnpm, Hardhat, Foundry, and environment-variable setup steps.]

## Skill Version(s):

1.0.2010 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
