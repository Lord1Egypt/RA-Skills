## Description: <br>
Digital legacy agent: dead man's switch, final message executor, and ghost mode responder that preserves a user's digital presence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[afterself](https://clawhub.ai/user/afterself) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use Afterself to configure a consent-based digital legacy workflow: periodic check-ins, trusted-contact escalation, encrypted final action plans, optional Ghost Mode, and optional Solana mortality-pool handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The mortality pool can trigger irreversible full-balance crypto transfers. <br>
Mitigation: Enable it only after verifying the token mint, pool wallet, trigger conditions, and with limited assets in the connected wallet. <br>
Risk: Misconfigured heartbeat or trusted-contact escalation can trigger final actions prematurely. <br>
Mitigation: Configure trusted contacts carefully and test check-in, disarm, stand-down, and kill-switch behavior before arming. <br>
Risk: Vault credentials can be exposed through shell history or long-lived environment files. <br>
Mitigation: Avoid passing the vault password through shell history or persistent environment files. <br>


## Reference(s): <br>
- [Afterself ClawHub listing](https://clawhub.ai/afterself/afterself) <br>
- [Afterself homepage](https://afterself.xyz) <br>
- [Action schema](references/action-schema.md) <br>
- [Escalation protocol](references/escalation-protocol.md) <br>
- [Ghost persona prompt](references/ghost-persona-prompt.md) <br>
- [Heartbeat protocol](HEARTBEAT.md) <br>
- [Ethics and safety](ETHICS.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Node scripts for state, vault, persona, and mortality-pool operations when the skill is armed by the user.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; skill frontmatter reports 0.1.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
