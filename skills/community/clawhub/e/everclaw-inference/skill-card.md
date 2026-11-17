## Description:

Everclaw connects OpenClaw agents to Morpheus decentralized inference with open-source-first model routing, OpenAI-compatible proxy setup, MOR staking workflows, gateway monitoring, and wallet/payment helpers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidajohnston](https://clawhub.ai/user/davidajohnston)

### License/Terms of Use:


## Use Case:

External users, developers, and OpenClaw operators use Everclaw to configure owned inference through Morpheus, manage local or gateway-backed model access, and keep agents running with monitoring, session, and payment support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and update paths may execute remote or unattended code.

Mitigation: Prefer a manual clone, inspect scripts before execution, and avoid curl-to-bash installation unless the source and command are reviewed.

Risk: Wallet workflows and token approvals can expose funds if keys, balances, or approvals are over-scoped.

Mitigation: Use your own API keys, keep only limited funds in any agent wallet, and avoid unlimited token approvals.

Risk: Persistent launchd services, local proxies, and OpenClaw configuration changes may increase host exposure.

Mitigation: Bind services to localhost, review persistent services before enabling them, and confirm OpenClaw configuration changes before applying.

Risk: The evidence security verdict is suspicious due to broad wallet, persistence, network exposure, and remote-code execution behavior.

Mitigation: Review the skill before installing and disable or patch unattended nuclear reinstall behavior.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/davidajohnston/skills/everclaw-inference)
- [Everclaw homepage](https://everclaw.com)
- [Everclaw API Reference](references/api.md)
- [Everclaw Available Models](references/models.md)
- [Everclaw MOR Staking Economics](references/economics.md)
- [Everclaw Acquiring MOR Tokens](references/acquiring-mor.md)
- [Everclaw Troubleshooting Guide](references/troubleshooting.md)
- [Morpheus AI](https://mor.org)
- [Morpheus Lumerin Node releases](https://github.com/MorpheusAIs/Morpheus-Lumerin-Node/releases)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [x402 Protocol](https://x402.org)
- [ERC-8004 specification](https://eips.ethereum.org/EIPS/eip-8004)
- [8004scan](https://www.8004scan.io)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JavaScript and JSON configuration snippets, and local script invocations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands that install dependencies, modify OpenClaw configuration, start local proxy services, and interact with MOR/Base wallet workflows.]

## Skill Version(s):

0.10.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
