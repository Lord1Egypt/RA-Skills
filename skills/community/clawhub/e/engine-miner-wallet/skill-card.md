## Description:

Secure operating guidance for the Engine miner Taproot wallet plugin on OpenClaw, including registration signing, safe claim handling, and refusal of unsafe wallet actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kerimatalayturkish-dotcom](https://clawhub.ai/user/kerimatalayturkish-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use this skill to operate the Engine miner wallet plugin for wallet setup, Taproot payout address retrieval, registration challenge signing, and controlled reward-claim workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet recovery phrases may be exposed in chat during agent-created setup.

Mitigation: Prefer manual local wallet creation; if agent-created setup is used, warn the user first, require explicit confirmation, and direct the user to store the phrase offline without pasting it back into chat.

Risk: Passphrases included in chat or command-line arguments can leak wallet secrets.

Mitigation: Keep passphrases local, use environment or secret-management mechanisms, and avoid passing real wallet secrets as chat text or command arguments.

Risk: Claim settlement behavior is not fully complete in this release.

Mitigation: Treat claim commands as planned or guarded workflows, verify tool output before relying on settlement behavior, and require explicit confirmation before any broadcast.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kerimatalayturkish-dotcom/skills/engine-miner-wallet)
- [Publisher profile](https://clawhub.ai/user/kerimatalayturkish-dotcom)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline commands and workflow intent mapping]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Emphasizes local secret handling, explicit confirmation before wallet creation or broadcast, and refusal of generic Bitcoin transfer requests.]

## Skill Version(s):

0.1.2 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
