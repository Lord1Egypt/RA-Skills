## Description: <br>
Set up and use 1Password CLI (op) for installation, desktop app integration, sign-in, and reading, injecting, or running secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaozewen0519](https://clawhub.ai/user/zhaozewen0519) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure local 1Password CLI access, authenticate through the desktop app, and safely run commands that read or inject secrets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples can expose secrets in terminal output, captured panes, shell history, or plaintext files. <br>
Mitigation: Keep masking enabled where possible, avoid printing secrets, prefer op run or op inject over writing files, and clean up any generated secret-bearing files or terminal captures. <br>
Risk: Commands that access 1Password may fail or prompt repeatedly when the desktop app is locked, integration is disabled, or the account is not signed in. <br>
Mitigation: Confirm the app is unlocked, desktop app integration is enabled, and op whoami succeeds in the dedicated tmux session before reading secrets. <br>


## Reference(s): <br>
- [1Password CLI get-started](https://developer.1password.com/docs/cli/get-started/) <br>
- [get-started.md](references/get-started.md) <br>
- [cli-examples.md](references/cli-examples.md) <br>
- [Install 1Password CLI (brew)](brew:1password-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands are intended for local terminal execution with 1Password CLI and tmux.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
