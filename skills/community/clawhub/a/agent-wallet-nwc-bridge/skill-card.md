## Description: <br>
Expose a local @moneydevkit/agent-wallet as a Nostr Wallet Connect (NIP-47) wallet-service (systemd user service). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kristapsk](https://clawhub.ai/user/kristapsk) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
Developers and operators use this skill to run a local Nostr Wallet Connect bridge for a self-custodial Bitcoin Lightning wallet, allowing NWC clients such as Stacker.News to request invoice creation and payment through @moneydevkit/agent-wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bridge can expose Bitcoin Lightning spending authority more broadly than users may expect. <br>
Mitigation: Use only with a small isolated wallet, avoid sharing generated NWC URIs, and keep NWC connection state and logs protected. <br>
Risk: Payment permissions may not enforce receive-only or send-only separation before payment execution. <br>
Mitigation: Keep NWC_AUTO_REGISTER disabled and do not rely on receive-only or send-only separation until allow_methods enforcement is verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kristapsk/agent-wallet-nwc-bridge) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup, operation, and wallet-bridge usage guidance; runtime files may include NWC connection secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
