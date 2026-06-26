## Description: <br>
Set up and use 1Password CLI (op). Use when installing the CLI, enabling desktop app integration, signing in (single or multi-account), or reading/injecting/running secrets via op. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to install and operate the 1Password CLI, authenticate accounts, and read, inject, or run commands with secrets while following explicit handling guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Secret values may be exposed through logs, chat, code, or files when using commands that read, print, inject, or write 1Password items. <br>
Mitigation: Keep the app locked until needed, avoid commands that print unmasked secrets, prefer op run or op inject over writing secrets to disk, and intentionally specify the account, vault, and item path. <br>
Risk: Authentication can fail or target the wrong account when op commands run outside the expected session or without explicit account selection. <br>
Mitigation: Run op commands inside a fresh tmux session, verify access with op whoami before reading secrets, and use --account or OP_ACCOUNT when multiple accounts are available. <br>


## Reference(s): <br>
- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/) <br>
- [Skill page](https://clawhub.ai/steipete/1password) <br>
- [get-started.md](references/get-started.md) <br>
- [cli-examples.md](references/cli-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the 1Password CLI (op), a 1Password subscription, desktop app integration for normal authentication, and a fresh tmux session for op commands.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
